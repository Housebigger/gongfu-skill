# 经济政策推演法引擎接入 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把经济政策专栏 `06` 的通用推演方法（六要素 + 诚实边界，evergreen）接进 `gongfu_consult`，在趋势前瞻/行业判断类咨询时注入 `knowledge_context.policy_deduction`。

**Architecture:** 新增一个无 `cluster_match` 的数据文件 `skills/data/policy-deduction-tools.yaml`（方法是通用宏观推演法）；`engine/router.py` 模块级加载它并暴露 `get_policy_deduction_method()`（无 cluster 参数）；`engine/tools.py` 的 `_handle_analyze` 在 `route_to` 含 `opportunity-radar`/`industry-scan` 时注入，`_build_execution_guide` 补一句方法引导。只注入方法与诚实边界，不注入时效宏观假设与 07/08 议题结论。

**Tech Stack:** Python 3.12，pyyaml（唯一运行期依赖）。仓库**无 pytest / 无自动化测试框架**——"测试"用 CLAUDE.md 记录的"合成包 `gongfu_engine`"直跑引擎来验证。

---

## 约定（每个任务都适用）

- **工作目录**：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`。所有命令在此根目录下执行。
- **解释器**：用 `.venv/bin/python`（已装 pyyaml）。不要用裸 `python`（PATH 上没有）。
- **验证脚本**：本仓库没有 pytest。每个任务的"测试"是一段独立 Python 验证脚本，用 `here-doc` 喂给 `.venv/bin/python` 运行；脚本不入库、不提交。失败时脚本用 `assert` 抛错并打印原因，成功时打印 `OK taskN`。
- **合成包样板**（任务 2/3 用）：从仓库根把 `engine/` 挂成 `gongfu_engine` 包：
  ```python
  import sys, importlib, types
  p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
  sys.modules['gongfu_engine'] = p
  router = importlib.import_module('gongfu_engine.router')
  tools  = importlib.import_module('gongfu_engine.tools')
  ```
- **红线（贯穿全程）**：方法文件里不得出现个股/仓位/买卖点、不得出现 `必将/一定会/建议买入/包涨/稳赚` 等断言式或荐股式措辞；诚实边界必须保留"情景非预言 / 不投资建议 / 不政治预测"。

---

## Task 1: 新增推演方法数据文件

**Files:**
- Create: `skills/data/policy-deduction-tools.yaml`

- [ ] **Step 1: 写验证脚本，先跑一遍确认失败（文件还不存在）**

把下面存为 `/tmp/verify_task1.py`：

```python
import yaml, re, pathlib
p = pathlib.Path("skills/data/policy-deduction-tools.yaml")
assert p.exists(), "文件不存在"
d = yaml.safe_load(p.read_text(encoding="utf-8"))
steps = d["method_steps"]; bnd = d["honest_boundaries"]
assert len(steps) == 6, f"expected 6 steps, got {len(steps)}"
assert len(bnd) == 4, f"expected 4 boundaries, got {len(bnd)}"
names = [s["step"] for s in steps]
expected = ["现状锚点", "规律库外推", "套外部约束与国情",
            "基准上行下行三情景", "可证伪点与观察指标", "劳动者含义"]
assert names == expected, f"步骤名/顺序不符: {names}"
for s in steps:
    assert s.get("principle") and s.get("one_liner") and s.get("quote_source"), f"卡片字段缺失: {s}"
text = p.read_text(encoding="utf-8")
assert "$" not in text, "出现 $（疑似资产/货币符号）"
assert not re.search(r"\d{6}", text), "出现 6 位数字（疑似 A 股代码）"
assert not re.search(r"必将|一定会|建议买入|包涨|稳赚", text), "出现断言/荐股式措辞"
for kw in ["情景非预言", "不投资建议", "不政治预测"]:
    assert any(kw in b for b in bnd), f"诚实边界缺: {kw}"
print("OK task1")
```

Run: `.venv/bin/python /tmp/verify_task1.py`
Expected: FAIL（`AssertionError: 文件不存在` 或 `FileNotFoundError`）。

- [ ] **Step 2: 创建数据文件**

写入 `skills/data/policy-deduction-tools.yaml`，内容完全如下：

```yaml
# 经济政策推演方法速查
# 蒸馏自 strategy/economic_policy/06-推演方法与外部约束.md（§1 六要素 + §4 诚实边界）
# 只含推演"方法"与"诚实边界"，evergreen：
#   不含国际/国情时效性宏观假设（06 §2/§3），不含 07/08 议题三情景结论。
# 与 industrial-chain-tools.yaml 互补：Serenity 卡片回答"怎么读一条产业链"，
#   本文件回答"怎么从政策作用规律向前推演未来方向"。
# 注意：只含推演方法，不含任何个股/仓位/买卖点/政治预测。

method_steps:          # 六要素推演法，有序（对应 06 §1 ①—⑥）
  - step: 现状锚点
    principle: 用可查证的官方"已发生"数据锁定起点，注明口径与时间窗口，不从假设出发
    one_liner: 先钉住"现在确实发生了什么"，再往前推
    quote_source: strategy/economic_policy/06 §1①
  - step: 规律库外推
    principle: 用已摸透的政策作用规律（时滞分层 / 传导节点 / 就业收入传导）向前延伸，并对传导节点逐项检查；只外推已有证据的机制
    one_liner: 不是凭空预测，是拿"已验证的规律"当推演引擎
    quote_source: strategy/economic_policy/06 §1② + 04
  - step: 套外部约束与国情
    principle: 任何推演都不在真空里——先检查规律外推是否被外部约束（国际博弈/外需/供应链）和国情（资产负债表/灰犀牛/人口）压制、放大或不变；只做方向定性
    one_liner: 给推演套上"现实约束框"，判断是顺风、逆风还是待观察
    quote_source: strategy/economic_policy/06 §1③
  - step: 基准上行下行三情景
    principle: 给方向谱不给单点；每个情景各带"触发条件（可观察指标）+ 关键假设 + 对劳动者方向含义"；一律"若…则…"条件式，不给时间表点位
    one_liner: 给三条路和各自的岔路口信号，不给一句"会怎样"的预言
    quote_source: strategy/economic_policy/06 §1④
  - step: 可证伪点与观察指标
    principle: 列 2—4 个官方可查指标，说明"看到什么数据说明在走哪条情景"；区分"规律前提失效信号（回去重审规律）"与"下行情景触发信号（切换路径）"
    one_liner: 让推演可被现实检验——事后怎么都能自圆其说的不是推演是诡辩
    quote_source: strategy/economic_policy/06 §1⑤
  - step: 劳动者含义
    principle: 把宏观推演翻成一线劳动者可操作的职业/行业/技能/区域方向，含基准情景方向与"下行信号出现时留意什么"；不承诺一定涨薪/一定有工作
    one_liner: 落到"岗位机会和卡位窗口"，不落到"哪个板块涨"
    quote_source: strategy/economic_policy/06 §1⑥ + 00 第三节

honest_boundaries:     # 推演诚实边界（对应 06 §4 四条）
  - 情景非预言：给方向不给点位和时间表，只用"若…则…"条件式，不预测"某年某指标到某点"
  - 规律有条件：推演建立在历史观察性规律上，规律非铁律，遇外部冲击/政策叠加/口径调整会失效
  - 不投资建议：服务对象是劳动者的职业方向判断，落点在岗位/就业/技能，不出个股、不出资产配置
  - 不政治预测：不预测政治走势、不评判政策对错、不做人事变动预测，不超出已公开官方文件推断意图
```

- [ ] **Step 3: 再跑验证脚本，确认通过**

Run: `.venv/bin/python /tmp/verify_task1.py`
Expected: PASS（打印 `OK task1`）。

- [ ] **Step 4: 提交**

```bash
git add skills/data/policy-deduction-tools.yaml
git commit -m "feat(engine): 新增经济政策推演方法数据文件（六要素+诚实边界·evergreen）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: router 加载器 + 访问函数

**Files:**
- Modify: `engine/router.py`（模块级 `_DEDUCTION` 加载，约第 28 行后；新函数 `get_policy_deduction_method()`，放在 `get_chain_tools_for_cluster` 之后、`get_regional_score` 之前）

- [ ] **Step 1: 写验证脚本，先跑一遍确认失败（函数还不存在）**

把下面存为 `/tmp/verify_task2.py`：

```python
import sys, importlib, types
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
router = importlib.import_module('gongfu_engine.router')
m = router.get_policy_deduction_method()
assert isinstance(m, dict) and m, "返回空"
assert len(m["method_steps"]) == 6, f"步骤数={len(m['method_steps'])}"
assert len(m["honest_boundaries"]) == 4, f"边界数={len(m['honest_boundaries'])}"
assert m["method_steps"][0]["step"] == "现状锚点", m["method_steps"][0]
print("OK task2")
```

Run: `.venv/bin/python /tmp/verify_task2.py`
Expected: FAIL（`AttributeError: module 'gongfu_engine.router' has no attribute 'get_policy_deduction_method'`）。

- [ ] **Step 2: 加模块级加载**

在 `engine/router.py` 中，把：

```python
# 产业链卡点分析工具（Serenity 方法·战略库第二根源）
_CHAIN = _load_yaml("industrial-chain-tools.yaml")
```

改成：

```python
# 产业链卡点分析工具（Serenity 方法·战略库第二根源）
_CHAIN = _load_yaml("industrial-chain-tools.yaml")
# 经济政策推演方法（战略库第三根源·Phase 2 方法框架·evergreen）
_DEDUCTION = _load_yaml("policy-deduction-tools.yaml")
```

- [ ] **Step 3: 加访问函数**

在 `engine/router.py` 中，把：

```python
    return result


def get_regional_score(opportunity: str, region: str) -> int:
```

改成：

```python
    return result


def get_policy_deduction_method() -> dict:
    """Get the evergreen economic-policy deduction method (six steps + honest boundaries).

    Universal macro-forecasting method distilled from strategy/economic_policy/06 —
    NOT cluster-specific. Returns {} if the data file is missing or empty.
    """
    if not _DEDUCTION:
        return {}
    steps = _DEDUCTION.get("method_steps", [])
    boundaries = _DEDUCTION.get("honest_boundaries", [])
    if not steps and not boundaries:
        return {}
    return {"method_steps": steps, "honest_boundaries": boundaries}


def get_regional_score(opportunity: str, region: str) -> int:
```

> 注意：上面 `return result` + 两空行 + `def get_regional_score` 的组合在文件中唯一（`get_regional_score` 只出现一次），可安全匹配。

- [ ] **Step 4: 再跑验证脚本，确认通过**

Run: `.venv/bin/python /tmp/verify_task2.py`
Expected: PASS（打印 `OK task2`）。

- [ ] **Step 5: 提交**

```bash
git add engine/router.py
git commit -m "feat(engine): router 加载推演方法 + get_policy_deduction_method()

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: tools 注入 + execution_guide 引导

**Files:**
- Modify: `engine/tools.py`（`_handle_analyze` 注入块，紧接现有 `chain_tools` 注入之后；`_build_execution_guide` 在最后"收尾"步前补一步）

- [ ] **Step 1: 写验证脚本，先跑一遍确认失败（还没注入）**

把下面存为 `/tmp/verify_task3.py`：

```python
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')

def analyze(situation):
    return json.loads(tools.gongfu_consult({"situation": situation, "mode": "analyze"}))

def kc(situation):
    return analyze(situation).get("knowledge_context", {})

# 1) 趋势前瞻 + 无行业 → 证明"不依赖 cluster"也注入
r1 = analyze("我30岁，想看看未来几年的趋势和机会")
assert "opportunity-radar" in r1["triage"]["route_to"], r1["triage"]["route_to"]
assert "policy_deduction" in r1["knowledge_context"], "趋势前瞻未注入"
assert len(r1["knowledge_context"]["policy_deduction"]["method_steps"]) == 6

# 2) 行业判断 + 有行业（光伏→C） → 注入
r2 = analyze("我在光伏厂干了几年，想知道这个行业方向好不好")
assert "industry-scan" in r2["triage"]["route_to"], r2["triage"]["route_to"]
assert "policy_deduction" in r2["knowledge_context"], "行业判断未注入"

# 3) 纯创业、无趋势/行业判断路由 → 不注入
r3 = analyze("我想自己开个小吃店，手里有十万存款")
assert "opportunity-radar" not in r3["triage"]["route_to"]
assert "industry-scan" not in r3["triage"]["route_to"]
assert "policy_deduction" not in r3["knowledge_context"], "不该注入却注入了"

# 4) execution_guide 在趋势/行业判断下应含方法引导关键词
assert "六要素情景法" in r1["execution_guide"], "execution_guide 未引导方法"
assert "不预测政局" in r1["execution_guide"], "execution_guide 未强调诚实边界"

print("OK task3")
```

Run: `.venv/bin/python /tmp/verify_task3.py`
Expected: FAIL（在断言 `"趋势前瞻未注入"` 处 `AssertionError`）。

- [ ] **Step 2: 加注入块**

在 `engine/tools.py` 的 `_handle_analyze` 中，把：

```python
        chain_tools = router.get_chain_tools_for_cluster(info["cluster"])
        if chain_tools:
            knowledge_context["chain_tools"] = chain_tools

    # 优势视角：提炼用户已经拥有的
```

改成：

```python
        chain_tools = router.get_chain_tools_for_cluster(info["cluster"])
        if chain_tools:
            knowledge_context["chain_tools"] = chain_tools

    # ── 注入经济政策推演方法（战略库第三根源·Phase 2 方法框架·evergreen）──
    # 仅"方法 + 诚实边界"，不含时效宏观假设/议题结论；
    # 趋势前瞻或行业判断时注入，不依赖 cluster（方法通用）
    if "opportunity-radar" in route_to or "industry-scan" in route_to:
        deduction = router.get_policy_deduction_method()
        if deduction:
            knowledge_context["policy_deduction"] = deduction

    # 优势视角：提炼用户已经拥有的
```

- [ ] **Step 3: 加 execution_guide 引导步**

在 `engine/tools.py` 的 `_build_execution_guide` 中，把：

```python
        step_num += 1

    steps.append(f"第{step_num}步：收尾。用一句话总结，但不是冷冰冰的结论。"
```

改成：

```python
        step_num += 1

    if "opportunity-radar" in route_to or "industry-scan" in route_to:
        steps.append(f"第{step_num}步：谈未来方向时用「六要素情景法」——先钉现状锚点（已发生的官方数据），"
                     "再用政策作用规律外推，给基准/上行/下行三条路和各自的观察信号。"
                     "守住四条线：情景非预言、给方向不给时间表、不荐资产/个股、不预测政局。")
        step_num += 1

    steps.append(f"第{step_num}步：收尾。用一句话总结，但不是冷冰冰的结论。"
```

> 注意：上面以 `        step_num += 1`（for 循环末尾）+ 空行 + `    steps.append(f"第{step_num}步：收尾。...` 这一组合定位，组合唯一（收尾那句在文件中只出现一次）。

- [ ] **Step 4: 再跑验证脚本，确认通过**

Run: `.venv/bin/python /tmp/verify_task3.py`
Expected: PASS（打印 `OK task3`）。

- [ ] **Step 5: 提交**

```bash
git add engine/tools.py
git commit -m "feat(engine): gongfu_consult 在趋势前瞻/行业判断时注入 policy_deduction

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: 升版本 + CHANGELOG + README + CLAUDE.md

**Files:**
- Modify: `pyproject.toml:3`、`engine/plugin.yaml:2`、`api_server/server.py:100`、`README.md:7`、`CHANGELOG.md`、`CLAUDE.md`

> 这是引擎改动，按仓库约定升版本。目标版本 **v1.4.0**（minor，新增引擎能力）。控制器在 merge 阶段会与用户最终确认版本号；若用户要别的号，仅需在本任务的字符串里替换。

- [ ] **Step 1: 三处版本号 1.3.0 → 1.4.0**

`pyproject.toml`，把 `version = "1.3.0"` 改成 `version = "1.4.0"`。
`engine/plugin.yaml`，把 `version: 1.3.0` 改成 `version: 1.4.0`。
`api_server/server.py`，把 `"version": "1.3.0",` 改成 `"version": "1.4.0",`。

- [ ] **Step 2: README 版本行**

`README.md`，把：

```
> 当前版本 **v1.3.0** ｜ 升级与变更说明见 [CHANGELOG.md](CHANGELOG.md)
```

改成：

```
> 当前版本 **v1.4.0** ｜ 升级与变更说明见 [CHANGELOG.md](CHANGELOG.md)
```

- [ ] **Step 3: CHANGELOG —— 新开 [1.4.0]，并把累计的两条知识条目转入本版**

先 Read `CHANGELOG.md`。把：

```
## [未发布]

### 新增 Added（纯知识内容，随下次发版一并记录）

```

改成：

```
## [未发布]

## [1.4.0] - 2026-06-25

经济政策追踪专栏（战略库**第三核心根源**）的推演方法接入引擎，并把此前累计的 Phase 1 / Phase 2 知识层随本版一并记录。对终端使用者**功能只增不减**：在行业判断 / 趋势前瞻类咨询中，多一套"政策作用规律 → 情景化推演"的方法框架与诚实边界（`policy_deduction`），给方向不给时间表、不荐资产、不预测政局。

### 新增 Added

- **引擎接入：经济政策推演法（方法框架·evergreen）**。新增 `skills/data/policy-deduction-tools.yaml`（六要素推演法 + 四条推演诚实边界，**不含**时效宏观假设与 07/08 议题结论）；`engine/router.py` 增 `get_policy_deduction_method()`（不依赖集群）；`gongfu_consult` 在趋势前瞻 / 行业判断类咨询时注入 `policy_deduction`，`execution_guide` 同步引导用六要素情景法并守住诚实边界。

```

> 这一步把原来 `### 新增 Added（纯知识内容…）` 标题替换成 `## [1.4.0]` 段 + 引擎条目 + `### 新增 Added`；原标题下方那两条知识条目（Phase 1 内容补全、Phase 2 推演知识层）位置不动，自然落到 `[1.4.0]` 的 `### 新增 Added` 之下。

- [ ] **Step 4: 修正两条知识条目里"不升版本"的过期措辞**

在 `CHANGELOG.md` 中，把 Phase 1 条目结尾：

```
信源清单同步补入统计局、能源局、央行、政府网等七条真实结果数据源（条目 8—14）。仍为纯知识内容、未改引擎、不升版本。Phase 2 推演另开 spec，尚未启动。
```

改成：

```
信源清单同步补入统计局、能源局、央行、政府网等七条真实结果数据源（条目 8—14）。随 v1.4.0 一并记录。
```

再把 Phase 2 条目结尾：

```
情景定位为方向研判而非预言，给方向不给时间表。仍为纯知识内容、未改引擎、不升版本；引擎接入另开 spec。
```

改成：

```
情景定位为方向研判而非预言，给方向不给时间表。随 v1.4.0 一并记录；引擎接入见本版"引擎接入"条目。
```

- [ ] **Step 5: CLAUDE.md 数据清单 12 → 13**

先 Read `CLAUDE.md`。把：

```
- `skills/data/*.yaml` — the structured knowledge the engine loads (`_DATA_DIR = <repo>/skills/data`, resolved from `engine/router.py`). 12 files: `industry-signals`, `startup-paths`, `growth-profiles`, `collaboration-forms`, `opportunities`, `methodology-tools`, `regional-matrix`, `counseling-principles`, `marxism-tools` / `deng-tools` / `xi-tools`, plus `industrial-chain-tools` (Serenity 产业链卡点分析法，战略库第二根源).
```

改成：

```
- `skills/data/*.yaml` — the structured knowledge the engine loads (`_DATA_DIR = <repo>/skills/data`, resolved from `engine/router.py`). 13 files: `industry-signals`, `startup-paths`, `growth-profiles`, `collaboration-forms`, `opportunities`, `methodology-tools`, `regional-matrix`, `counseling-principles`, `marxism-tools` / `deng-tools` / `xi-tools`, `industrial-chain-tools` (Serenity 产业链卡点分析法，战略库第二根源), plus `policy-deduction-tools` (经济政策推演方法，战略库第三根源·evergreen 方法框架，由 `get_policy_deduction_method()` 在趋势前瞻/行业判断时注入 `policy_deduction`).
```

- [ ] **Step 6: 验证版本一致 + 提交**

Run:
```bash
grep -n '1.4.0' pyproject.toml engine/plugin.yaml api_server/server.py README.md
```
Expected: 四个文件各出现一次（pyproject 第 3 行、plugin.yaml 第 2 行、server.py 第 100 行附近、README 第 7 行），且不再有 `1.3.0` 作为"当前版本"。

```bash
git add pyproject.toml engine/plugin.yaml api_server/server.py README.md CHANGELOG.md CLAUDE.md
git commit -m "chore: 升版本 v1.4.0 + CHANGELOG/README/CLAUDE 同步（推演法引擎接入）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: 重建派生包 + 四壳一致 + 端到端冒烟

**Files:**
- 无新增源文件改动。运行 `scripts/build_packs.py`（其输出目录 `engine/skills/`、`claude-skills/`、`agents/zcode-skills/` 均 gitignored，不提交）。

- [ ] **Step 1: 重建派生包**

Run: `.venv/bin/python scripts/build_packs.py`
Expected: 正常结束、无异常报错（脚本为 stdlib-only，逐文件复制）。

- [ ] **Step 2: 四壳一致——校验源与生成副本字节一致**

把下面存为 `/tmp/verify_task5.py`：

```python
import pathlib
src = pathlib.Path("skills/data/policy-deduction-tools.yaml").read_bytes()
copies = [
    "claude-skills/data/policy-deduction-tools.yaml",
    "agents/zcode-skills/data/policy-deduction-tools.yaml",
]
missing = [c for c in copies if not pathlib.Path(c).exists()]
assert not missing, f"派生副本缺失（先跑 build_packs）: {missing}"
for c in copies:
    assert pathlib.Path(c).read_bytes() == src, f"副本与源不一致: {c}"
print("OK task5 (四壳数据一致)")
```

Run: `.venv/bin/python /tmp/verify_task5.py`
Expected: PASS（打印 `OK task5 (四壳数据一致)`）。

> 若某派生 `data/` 目录在本机不存在（fresh clone 未建过），说明该壳的 `data` 子目录尚未生成——以 `build_packs.py` 实际产出为准；至少 `claude-skills/data/` 应存在。如该路径确实不在 build_packs 的产出集合内，则在脚本里移除该条 copy 并在收尾说明里记录（不要静默跳过）。

- [ ] **Step 3: 端到端冒烟——三类路由各跑一遍 analyze**

把下面存为 `/tmp/verify_e2e.py`：

```python
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')

def run(s):
    return json.loads(tools.gongfu_consult({"situation": s, "mode": "analyze"}))

cases = [
    ("我30岁，想看看未来几年的趋势和机会", True),
    ("我在光伏厂干了几年，想知道这个行业方向好不好", True),
    ("我想自己开个小吃店，手里有十万存款", False),
]
for s, want in cases:
    has = "policy_deduction" in run(s).get("knowledge_context", {})
    assert has == want, f"路由判定错: {s!r} 期望注入={want} 实际={has}"
    print(f"  {'注入' if has else '不注入'} <- {s}")
print("OK e2e")
```

Run: `.venv/bin/python /tmp/verify_e2e.py`
Expected: PASS（打印三行路由结果 + `OK e2e`）。

- [ ] **Step 4: 收尾**

本任务无源文件改动需提交（派生产物 gitignored）。若 `git status` 显示有未忽略的改动，停下来核对——理论上应为干净。

```bash
git status --porcelain
```
Expected: 空（无未提交改动）。

---

## Self-Review（写完计划后的自检）

**Spec 覆盖**：
- spec §3 数据文件 → Task 1 ✅
- spec §4.1 router 加载器+访问函数 → Task 2 ✅
- spec §4.2 tools 注入 + §4.3 execution_guide 轻触 → Task 3 ✅（schemas.py 按 spec 不动 ✅）
- spec §6 验证（单元/注入/红线/四壳/版本）→ Task 1 红线、Task 2 单元、Task 3 注入正负例、Task 5 四壳+端到端、Task 4 版本一致 ✅
- spec §7 版本与文档（三处版本/CHANGELOG/README/CLAUDE 12→13）→ Task 4 ✅
- spec §8 非目标（不注入时效假设/议题结论、无 cluster_match、不改 schemas、不碰 perspective）→ 计划中均无相关改动 ✅

**Placeholder 扫描**：无 TBD/TODO；每个改代码的步骤都给了完整代码与精确锚点；每个验证脚本都是完整可跑代码。✅

**类型/命名一致性**：函数名全程 `get_policy_deduction_method()`；返回键 `method_steps` / `honest_boundaries`；注入键 `knowledge_context["policy_deduction"]`；数据文件名 `policy-deduction-tools.yaml`——Task 1/2/3/5 用词一致。✅
