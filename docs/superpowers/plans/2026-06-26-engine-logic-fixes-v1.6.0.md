# v1.6.0 引擎逻辑修复 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修掉 2026-06-26 全仓审计发现的引擎正确性缺陷（analyze 空壳、年龄截错、地域死数据、危机词误命中、situation-triage SKILL 缺验证段 + 廉价 NIT），并兑现"地域分析"能力，作为 v1.6.0 发布。

**Architecture:** 全部改动在 `engine/`（router/tools/schemas）+ `skills/situation-triage/SKILL.md` + `skills/data/methodology-tools.yaml` + 版本/文档。镜像既有 `get_*_for_cluster` 注入与 triage 抽取模式，不新增运行文件。

**Tech Stack:** Python 3.10+（项目 pin 3.12）；无 pytest——验证用合成包 `gongfu_engine` 引导脚本（断言式：改前 FAIL / 改后 PASS）。`pyyaml` 必需。

---

## 约定（每个任务都适用）

- **工作目录**：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`，命令在此根下跑。
- **分支**：`feat/engine-logic-fixes-v1.6.0`（已建，spec 已提交其上）。
- **验证 = 合成包断言脚本**（无 pytest）。每个验证脚本用下面这段引导（PYBOOT）：每次 `.venv/bin/python` 是全新进程，会重新 import 引擎 + 重新读 YAML（所以改 YAML 后无需特殊处理）。若无 `.venv`，先 `uv venv --python 3.12 .venv && source .venv/bin/activate && uv pip install mcp pyyaml`。
- **契约不变量**：引擎只返回"给 LLM 的指令"；危机检测仍在最前、不可绕过；稳定标识符（集群 ID/intent 名/区域符号 ①–⑤）不改名。
- **TDD 适配**：先写验证脚本跑出 FAIL（证明问题存在），再实现，再跑出 PASS。

**PYBOOT 引导（粘进每个 `.venv/bin/python - <<'PY'` 脚本顶部）：**
```python
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
router = importlib.import_module('gongfu_engine.router')
```

---

## Task 1: A1 — `analyze` 短路 `need_more_info`（不再产空壳"假分析"）

**Files:** Modify `engine/tools.py`（`gongfu_consult`，危机分支之后 ~115-119 行）

- [ ] **Step 1: 写验证脚本跑出 FAIL**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
out = json.loads(tools.gongfu_consult({"situation": "你好啊", "mode": "analyze"}))
assert out.get("type") == "intake" and out.get("phase") == "need_basic_info", \
    f"FAIL: 信息过少的 analyze 仍产出 {out.get('type')}/{out.get('phase')}（应回退 intake/need_basic_info）"
print("PASS A1")
PY
```
预期（改前）：FAIL，打印 `type=analysis`（空壳）。

- [ ] **Step 2: 实现** —— 在 `engine/tools.py` `gongfu_consult` 的危机分支（`if triage_result.get("special_handling") == "crisis":` 整块）之后、`if mode == "intake":` 之前，插入：
```python
    # ── 信息过少 → 无论 mode 都先请用户补基本信息（不产出空壳分析）──
    if triage_result.get("special_handling") == "need_more_info":
        return _handle_intake(situation, triage_result)

```

- [ ] **Step 3: 跑验证 → PASS**；并确认正常 analyze 不受影响：
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
out = json.loads(tools.gongfu_consult({"situation": "你好啊", "mode": "analyze"}))
assert out.get("type") == "intake" and out.get("phase") == "need_basic_info", out.get("type")
ok = json.loads(tools.gongfu_consult({"situation": "我45岁钢铁厂下岗想转行", "mode": "analyze"}))
assert ok.get("type") == "analysis", "正常 analyze 被误伤"
print("PASS A1 + 回归")
PY
```

- [ ] **Step 4: 提交**
```bash
git add engine/tools.py
git commit -m "fix(engine): analyze 模式短路 need_more_info，不再产出空壳假分析（C1）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: A2 — 年龄正则修正 + `import re` 上移

**Files:** Modify `engine/router.py`（顶部 import 区 ~7-9 行；`extract` 内 Age 块 ~226-230 行）

- [ ] **Step 1: 写验证脚本跑出 FAIL**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
router = importlib.import_module('gongfu_engine.router')
def age(s): return router.triage(s).get("extracted_info", {}).get("age")
assert age("我45岁了想转行") == 45, age("我45岁了想转行")
assert age("我120岁了") != 20, "120岁被截成20"
assert age("我活了100岁") not in (0,), "100岁产生age=0"
router.triage("我2岁半")  # 不崩即可
print("PASS A2")
PY
```
预期（改前）：FAIL（`120→20` 或 `100→0`）。

- [ ] **Step 2: 实现（两处）** ——
  1. `engine/router.py` 顶部，在 `from pathlib import Path` 之后加一行：
```python
import re
```
  2. 替换 `extract` 内 Age 块（当前为）：
```python
    # Age
    import re
    age_match = re.search(r'(\d{2})\s*岁', situation_text)
    if age_match:
        extracted["age"] = int(age_match.group(1))
```
改为：
```python
    # Age（负向前瞻避免从多位数尾部误截；范围校验剔除 0 与不合理值）
    age_match = re.search(r'(?<!\d)(\d{1,3})\s*岁', situation_text)
    if age_match:
        age_val = int(age_match.group(1))
        if 14 <= age_val <= 80:
            extracted["age"] = age_val
```

- [ ] **Step 3: 跑验证 → PASS**

- [ ] **Step 4: 提交**
```bash
git add engine/router.py
git commit -m "fix(engine): 年龄正则修正——避免从3位数截错、剔除age=0；import re 上移（C2）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: A3 — region 接线注入 `analyze`（兑现"地域分析"）

**Files:** Modify `engine/router.py`（新增 `get_regional_context`；给 `get_regional_score` 补 docstring）+ `engine/tools.py`（`_handle_analyze` 注入块）

- [ ] **Step 1: 写验证脚本跑出 FAIL**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
out = json.loads(tools.gongfu_consult({"situation": "我在成都做新能源，想看看前景", "mode": "analyze"}))
kc = out["knowledge_context"]
assert "regional" in kc, "FAIL: analyze 未注入 regional"
r = kc["regional"]
assert r.get("region_profile") and r.get("region_scores") and r.get("regional_advice"), "regional 三块不全"
# 无 region 的句子不应注入
out2 = json.loads(tools.gongfu_consult({"situation": "我做新能源想看看前景", "mode": "analyze"}))
assert "regional" not in out2["knowledge_context"], "无 region 却注入了 regional"
print("PASS A3")
PY
```
预期（改前）：FAIL（无 `regional`）。

- [ ] **Step 2: 实现（router.py）** —— 在 `get_regional_score` 函数**之前**新增（镜像 `get_*_for_cluster` 风格）：
```python
def get_regional_context(region: str) -> dict:
    """Get evergreen regional knowledge for analyze injection. Returns {} if missing.

    region 形如 "②新兴增长极"（带圈号）；按首字符 ①②③④⑤ 从 opportunity_matrix 取该区域整列评分。
    """
    if not region:
        return {}
    regions = _REGIONAL.get("regions", {})
    profile = regions.get(region, {})
    if not profile:
        return {}
    region_key = region[0]  # ①②③④⑤
    matrix = _REGIONAL.get("opportunity_matrix", {})
    region_scores = {
        opp: scores[region_key]
        for opp, scores in matrix.items()
        if region_key in scores
    }
    return {
        "region_profile": profile,
        "region_scores": region_scores,
        "regional_advice": _REGIONAL.get("regional_advice", {}),
    }
```
并给已存在的 `get_regional_score` 补一行 docstring 说明它保留用途（在其 docstring 末尾追加）：
```python
    """Get the opportunity score for a region from the matrix.

    单格查询（机会×区域）。当前 analyze 经 get_regional_context 注入整列；
    本函数保留供未来按 cluster→机会 精确取分之需，勿删。
    """
```

- [ ] **Step 3: 实现（tools.py）** —— 在 `_handle_analyze` 的 `industry_forecast` 注入块（`knowledge_context["industry_forecast"] = forecast` 那段）**之后**加：
```python
    # ── 注入地域知识（regional-matrix·evergreen：区域画像+机会评分列+决策建议）──
    # 行业判断/趋势前瞻类路由且识别出 region 时注入
    if info.get("region") and (
        "industry-scan" in route_to or "opportunity-radar" in route_to
    ):
        regional = router.get_regional_context(info["region"])
        if regional:
            knowledge_context["regional"] = regional
```

- [ ] **Step 4: 跑验证 → PASS**

- [ ] **Step 5: 提交**
```bash
git add engine/router.py engine/tools.py
git commit -m "feat(engine): regional-matrix 接线注入 analyze（get_regional_context·兑现地域分析）（A3）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: B1 — 危机词收紧（降误命中，仍偏安全）

**Files:** Modify `skills/data/methodology-tools.yaml`（`crisis_signals.危机`，第 96 行）

- [ ] **Step 1: 写验证脚本跑出 FAIL**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
router = importlib.import_module('gongfu_engine.router')
def crisis(s): return router.triage(s).get("special_handling") == "crisis"
assert not crisis("我想了结这个项目然后转行"), "FAIL: 了结项目被误判危机"
assert not crisis("无所谓了我继续干"), "FAIL: 无所谓了被误判危机"
assert crisis("我不想活了"), "FAIL: 真危机信号漏判"
assert crisis("活着没意思"), "FAIL: 真危机信号漏判"
print("PASS B1")
PY
```
预期（改前）：FAIL（前两句被误判 crisis）。

- [ ] **Step 2: 实现** —— `skills/data/methodology-tools.yaml` 第 96 行：
```yaml
  危机: [不想活了, 无所谓了, 活着没意思, 了结]
```
改为：
```yaml
  危机: [不想活了, 活着没意思, 了结自己, 了结生命, 不想活, 轻生]
```
（删 `无所谓了`、把 `了结`→`了结自己`/`了结生命`，并补 `不想活`/`轻生` 两个明确信号以不削弱真危机覆盖。）

- [ ] **Step 3: 跑验证 → PASS**（新进程会重读 YAML）

- [ ] **Step 4: 提交**
```bash
git add skills/data/methodology-tools.yaml
git commit -m "fix(data): 危机词收紧——了结→了结自己/了结生命、删无所谓了、补不想活/轻生（B1）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: B2 — `situation-triage/SKILL.md` 补全规范段

**Files:** Modify `skills/situation-triage/SKILL.md`

先 Read `skills/situation-triage/SKILL.md`（现状）、`skills/00-skill设计规范.md`（必备段）、`skills/industry-scan/SKILL.md`（同仓格式范本）。本 skill 是路由层，行为源自 `engine/router.py` `triage()` + `skills/data/methodology-tools.yaml` 的 `intent_keywords`/`crisis_signals`。

- [ ] **Step 1: 补齐缺失段** —— 在保留现有"行为指南"内容的基础上，补齐规范必备段（用同仓 industry-scan/SKILL.md 的标题风格）：
  - **什么时候用 / 何时不用**：用户给出自由描述、需要判断"该用哪几个 skill"时用；已明确单一诉求时可直接用对应 skill。
  - **输入规格**：用户自由文本（原话；多轮则拼接）。
  - **执行逻辑（分步）**：① 危机检测（最先，命中即停、给热线、不路由）→ ② 意图识别（困境迷茫/行业判断/创业意向/成长需求/协作需求/趋势前瞻）→ ③ 结构化抽取（行业/集群、地域、年龄、财务、家庭、情绪）→ ④ 路由（困境/耗竭优先 problem-diagnosis，其余按意图去重追加；无意图但有行业→industry-scan；无意图无行业→need_more_info）→ ⑤ 完整度评估与温柔追问。
  - **输出规格**：`route_to`、`detected_intents`、`extracted_info`、`completeness`/`next_question`，或特殊态 `crisis`/`need_more_info`。
  - **测试用例（≥3，含边界）**，例如：
    1. 「我38岁在制造业干了十年，最近想转行，也在考虑搞点副业」→ 识别 困境/成长 + 创业意向；route 含 problem-diagnosis + startup-feasibility；抽出 age=38、cluster=制造相关。
    2. 「我在光伏电站做运维」（仅行业、无明确意图）→ 无意图但有行业 → route=[industry-scan]，cluster=C-绿色能源全链。
    3. （边界）「你好啊」（无行业无意图）→ `need_more_info`（不路由，温柔请补：行业/城市/诉求）。
  - **源文档映射**：`engine/router.py::triage`、`skills/data/methodology-tools.yaml::intent_keywords` / `crisis_signals`。
  - **边界**：路由非 100% 准确，允许多路由；危机优先于一切。

- [ ] **Step 2: 验证（doc-based）**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
F=skills/situation-triage/SKILL.md
for seg in 什么时候用 输入 执行 输出 测试用例 源文档 边界; do grep -q "$seg" "$F" && echo "有: $seg" || echo "!! 缺: $seg"; done
echo "测试用例数（≥3）: $(grep -cE '^\s*[0-9]+\.' "$F")"
```
预期：各段都"有"，测试用例 ≥3，无 `!!`。

- [ ] **Step 3: 提交**
```bash
git add skills/situation-triage/SKILL.md
git commit -m "docs(skill): situation-triage 补全规范段+测试用例+源文档映射（B2）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: 廉价 NIT 批（C1 死参数 / C2 region_name / C3 schemas / C4 裸except / C5 注释）

**Files:** Modify `engine/tools.py`（_build_execution_guide 签名+调用）、`engine/router.py`（region_name、裸except×3、route_to 注释）、`engine/schemas.py`（特殊返回说明）

- [ ] **Step 1: 写回归脚本（先确保现状 PASS，改后仍 PASS）**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
out = json.loads(tools.gongfu_consult({"situation": "我45岁在上海钢铁厂下岗想转行", "mode": "analyze"}))
assert out["execution_guide"].startswith("第1步：先说优势"), out["execution_guide"][:30]
# region_name 应去圈号（上海→①三大动力源；展示名应为"三大动力源"）
intake = json.loads(tools.gongfu_consult({"situation": "我在上海做制造业", "mode": "intake"}))
assert "①" not in intake.get("user_profile", ""), "region_name 仍带圈号"
print("PASS C-batch（改后应仍 PASS）")
PY
```
（改前：execution_guide 断言会 PASS（恒非空），region_name 断言会 FAIL（仍带圈号）——这条 FAIL 正是 C2 要修的。）

- [ ] **Step 2: C1 死参数** —— `engine/tools.py`：
  - 改签名（第 381 行）：`def _build_execution_guide(route_to: list, info: dict, triage_result: dict) -> str:` → `def _build_execution_guide(route_to: list, info: dict, triage_result: dict, strengths: list) -> str:`
  - 删函数内重算（第 387 行 `strengths = _identify_strengths(info, triage_result.get("extracted_info", {}).get("situation", ""))`），直接用传入的 `strengths`。
  - 改调用（第 357 行）：`"execution_guide": _build_execution_guide(route_to, info, triage_result),` → `"execution_guide": _build_execution_guide(route_to, info, triage_result, strengths),`（`strengths` 已在第 343 行算好）。

- [ ] **Step 3: C2 region_name 去圈号** —— `engine/router.py` Region 抽取块（第 221 行）：
```python
                extracted["region"] = region
                extracted["region_name"] = region
```
改为：
```python
                extracted["region"] = region
                extracted["region_name"] = region[1:] if region[:1] in "①②③④⑤" else region
```

- [ ] **Step 4: C4 裸except收窄** —— `engine/router.py` 第 374、463、530 行三处 `except Exception:` → `except (OSError, UnicodeDecodeError):`（均为启发文件读取的吞错跳过）。

- [ ] **Step 5: C5 route_to 优先级注释** —— `engine/router.py` 在路由优先级块（`route_to = []` 那行之前，约 156 行）加注释：
```python
    # 路由优先级：困境/耗竭先置 problem-diagnosis（情绪/处境优先），
    # 其余意图按 intent_keywords 出现序去重追加；无显式优先级表（行序即意图）。
```

- [ ] **Step 6: C3 schemas 补特殊返回说明** —— `engine/schemas.py` 在 description 的"交互流程：…→ 温暖的判断。\n"之后、"直接传用户的原话就行…"之前插入：
```python
        "两种特殊返回：信息过少时返回 need_basic_info（先请补行业/城市/诉求，不分析）；"
        "检测到情绪危机时返回 crisis（不做职业判断、提供热线）。两者结构与常规返回不同。\n"
```

- [ ] **Step 7: 跑回归脚本 → 全 PASS**（含 region_name 去圈号）；并确认引擎可导入无语法错：
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
schemas = importlib.import_module('gongfu_engine.schemas')
out = json.loads(tools.gongfu_consult({"situation": "我45岁在上海钢铁厂下岗想转行", "mode": "analyze"}))
assert out["execution_guide"].startswith("第1步：先说优势")
intake = json.loads(tools.gongfu_consult({"situation": "我在上海做制造业", "mode": "intake"}))
assert "①" not in intake.get("user_profile", "")
assert "need_basic_info" in schemas.GONGFU_CONSULT["description"] and "crisis" in schemas.GONGFU_CONSULT["description"]
print("PASS C-batch")
PY
```

- [ ] **Step 8: 提交**
```bash
git add engine/tools.py engine/router.py engine/schemas.py
git commit -m "refactor(engine): NIT批——死参数清理/region_name去圈号/schemas补特殊返回/裸except收窄/路由注释（C1-C5）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: 升版本 v1.6.0 + CHANGELOG + build_packs + CLAUDE.md

**Files:** Modify `pyproject.toml`、`api_server/server.py`、`engine/plugin.yaml`、`README.md`、`CHANGELOG.md`、`CLAUDE.md`；运行 `scripts/build_packs.py`

- [ ] **Step 1: 三处版本号 1.5.0 → 1.6.0** —— 先定位再改：
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -nE '1\.5\.0' pyproject.toml engine/plugin.yaml api_server/server.py README.md
```
分别把 `pyproject.toml` 的 `version = "1.5.0"`、`engine/plugin.yaml` 的 `version: 1.5.0`、`api_server/server.py` 的 `/` index `"version": "1.5.0"`、`README.md` 顶部"当前版本 v1.5.0"行 → `1.6.0` / `v1.6.0`。

- [ ] **Step 2: CHANGELOG `[1.6.0]`** —— 先 Read `CHANGELOG.md` 顶部。新开 `## [1.6.0] - 2026-06-26` 段（在 `[未发布]` 与 `[1.5.0]` 之间）；把 `[未发布]` 里"华为韬定律半导体研究专题（知识层）"那条**移入** `[1.6.0]`（随本版发布），并在 `[1.6.0]` 增引擎修复条目：
```
## [1.6.0] - 2026-06-26

### 修复 Fixed（引擎逻辑·源自全仓审计）
- **analyze 模式短路 need_more_info**：信息过少时不再产出空壳"假分析"，回退为温柔请补基本信息。
- **年龄抽取修正**：负向前瞻 + 范围校验（14–80），消除"120岁→20""100岁→age=0"的静默错误。
- **危机词收紧**：`了结`→`了结自己`/`了结生命`、删 `无所谓了`、补 `不想活`/`轻生`，降低正常咨询被误判危机的概率，同时保留真信号。
- **NIT 清理**：execution_guide 死参数、region_name 去圈号展示、schemas 补特殊返回说明、启发加载器裸 except 收窄、路由优先级注释。

### 新增 Added
- **地域分析接线**：`regional-matrix.yaml` 经新增的 `get_regional_context()` 在行业判断/趋势前瞻且识别出地域时注入 analyze（区域画像 + 该区域机会评分列 + 决策建议），兑现 schemas/SKILL 早已声明的"地域分析"能力。
- **situation-triage/SKILL.md** 补齐规范段（测试用例 + 源文档映射 + 输入/输出/执行规格）。
- **战略库新增「华为韬（τ）定律 → 半导体产业发展逻辑与方向」研究专题（知识层）**（原 [未发布] 累计条目，随本版发布）：原料库 `strategy/references/huawei_tau/` + 提炼/预测 `strategy/semiconductor_outlook/`（00–04），三分陈述 + 情景非预言 + 中立 + 不个股，落点 A 集群劳动者。
```
（保留 `[未发布]` 标题为空段。）

- [ ] **Step 3: CLAUDE.md 一句话补充** —— 在数据清单描述 `regional-matrix` 处补"（现经 `get_regional_context()` 在 analyze 注入）"。先 `grep -n 'regional-matrix' CLAUDE.md` 定位再改（若 CLAUDE.md 未逐个点名 regional-matrix，则跳过，不强加）。

- [ ] **Step 4: 重建派生包 + 校验干净**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
python scripts/build_packs.py
git status --porcelain    # 派生包 gitignore，应只见已改的源/版本/文档
```

- [ ] **Step 5: 验证版本同步 + 引擎可跑**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
echo "pyproject:"; grep -m1 '1\.6\.0' pyproject.toml
echo "plugin:"; grep -m1 '1\.6\.0' engine/plugin.yaml
echo "api:"; grep -m1 '1\.6\.0' api_server/server.py
echo "readme:"; grep -m1 'v1\.6\.0' README.md
grep -q '1\.5\.0' pyproject.toml engine/plugin.yaml api_server/server.py && echo "!! 仍有残留 1.5.0" || echo "三处版本已升 OK"
.venv/bin/python - <<'PY'
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']; sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
print("引擎可跑:", json.loads(tools.gongfu_consult({"situation":"我45岁钢铁厂下岗想转行","mode":"analyze"}))["type"])
PY
```
预期：三处显示 1.6.0、README v1.6.0、无残留、引擎可跑。

- [ ] **Step 6: 提交**
```bash
git add pyproject.toml engine/plugin.yaml api_server/server.py README.md CHANGELOG.md CLAUDE.md
git commit -m "chore: 升版本 v1.6.0 + CHANGELOG（引擎逻辑修复+地域分析接线，韬定律知识随本版发布）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review（写完计划后的自检）

**Spec 覆盖：**
- A1 analyze 短路 → Task 1 ✅；A2 年龄正则 → Task 2 ✅；A3 region 接线 → Task 3 ✅
- B1 危机词 → Task 4 ✅；B2 situation-triage SKILL → Task 5 ✅
- C1 死参数 / C2 region_name / C3 schemas / C4 裸except / C5 注释 → Task 6 ✅
- 版本/CHANGELOG/build_packs/CLAUDE.md → Task 7 ✅
- spec §4 契约不变量（危机最前、只给指令、稳定标识符）→ A1 短路放危机之后、不改危机；各任务不碰标识符 ✅
- spec §5 验证（含回归既有注入）→ Task 1 Step3 回归 + Task 6/7 回归 ✅
- spec §7 非目标（不建 cluster→机会映射、不删 get_regional_score/yaml、不扩成品话术例外、不补 deng/xi 语料、不建优先级表、不改 schemas 参数）→ 计划均遵守 ✅

**Placeholder 扫描：** 无 TBD/TODO；每处代码改动给了 old→new 或精确插入点 + 完整代码块；Task 5 给了具体三段测试用例内容与必备段清单（非占位符）。✅

**一致性：** `get_regional_context`（router）↔ `knowledge_context["regional"]`（tools）字段名一致（region_profile/region_scores/regional_advice）；`_build_execution_guide` 新签名（+strengths）与调用处一致；版本号 1.6.0 五处一致；危机词新列表前后一致。✅

**执行提示（给控制器）：** 全部顺序执行（subagent 串行，tools.py/router.py 多任务改同文件但不并行，无冲突）。每任务"实现→spec合规→质量/回归"两段评审；B1 危机词评审须双向验证（误命中转正常 + 真危机仍触发）；A3 评审验证注入字段齐全且无 region 不注入；最后整支跑全部验证脚本 + 四壳一致 + 版本同步，再收尾合并 v1.6.0（打 tag + Release 按用户定）。
