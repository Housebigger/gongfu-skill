# 逐集群行业前景接入引擎（evergreen 卡片·v1.5.0）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 16 个集群的行业前景蒸馏成 evergreen 卡片接进 `gongfu_consult`，在行业判断/趋势前瞻类咨询且识别出 cluster 时注入 `knowledge_context.industry_forecast`。

**Architecture:** 新增 `skills/data/industry-forecast-tools.yaml`（16 张 evergreen 卡 + cluster_match，从 `09-行业前景推演/<cluster>.md` 蒸馏，只含慢变量）；`engine/router.py` 加载它并暴露 `get_industry_forecast_for_cluster(cluster)`（镜像 `get_chain_tools_for_cluster`）；`engine/tools.py` 的 `_handle_analyze` 在 chain_tools/policy_deduction 注入块之后按 cluster + route_to 注入。时效数据不进引擎，留在知识层。

**Tech Stack:** Python 3.12，pyyaml。仓库**无 pytest**——"测试"用合成包 `gongfu_engine` 直跑引擎验证（`.venv/bin/python`，从仓库根运行）。

---

## 约定（每个任务都适用）

- **工作目录**：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`。所有命令在此根下跑。
- **分支**：`feat/industry-forecast-engine`（已建）。
- **解释器**：`.venv/bin/python`（已装 pyyaml）。不要用裸 `python`。
- **合成包样板**（任务 2/3/5 验证用，从仓库根）：
  ```python
  import sys, importlib, types
  p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
  sys.modules['gongfu_engine'] = p
  router = importlib.import_module('gongfu_engine.router')
  tools  = importlib.import_module('gongfu_engine.tools')
  ```
- **evergreen 红线（贯穿全程）**：卡片只放慢变量——不得出现带年份的统计数字、三情景阈值、待核实项、个股/证券代码、`必将/一定会/建议买入/包涨/稳赚`、政治预测式断言。时效内容一律留在知识层 `09-行业前景推演/<cluster>.md`，卡片用 `source` 指过去。

## 16 个集群 ID（与 `09-行业前景推演/` 文件名、引擎 cluster IDs 一致）

```
A-先进制造与硬科技  B-数字与智能产业  C-绿色能源全链  D-农业与乡村振兴
E-民生服务  F-文化创意与出海  G-基建物流房地产  H-新兴未来产业
I-传统矿业与资源开采  J-传统轻纺与日用制造  K-传统重化工与建材  L-商贸零售与餐饮住宿
M-金融与商务服务  N-教育与培训  O-居民生活服务  P-公用事业与市政服务
```

---

## Task 1: 新增逐集群行业前景卡片数据文件（16 卡蒸馏）

**Files:**
- Create: `skills/data/industry-forecast-tools.yaml`

**这是从 `09-行业前景推演/<cluster>.md` 16 个文件蒸馏 evergreen 卡片**——纯提取，不需联网，不得引入文件里没有的判断。

- [ ] **Step 1: 写验证脚本，先跑确认失败（文件不存在）**

存为 `/tmp/verify_fc1.py`：

```python
import yaml, re, pathlib
p = pathlib.Path("skills/data/industry-forecast-tools.yaml")
assert p.exists(), "文件不存在"
d = yaml.safe_load(p.read_text(encoding="utf-8"))
fc = d["forecasts"]; cm = d["cluster_match"]
clusters = ["A-先进制造与硬科技","B-数字与智能产业","C-绿色能源全链","D-农业与乡村振兴",
            "E-民生服务","F-文化创意与出海","G-基建物流房地产","H-新兴未来产业",
            "I-传统矿业与资源开采","J-传统轻纺与日用制造","K-传统重化工与建材","L-商贸零售与餐饮住宿",
            "M-金融与商务服务","N-教育与培训","O-居民生活服务","P-公用事业与市政服务"]
assert len(fc) == 16, f"卡片数={len(fc)}"
for c in clusters:
    assert c in fc, f"缺卡: {c}"
    card = fc[c]
    for f in ["main_issue","tone","positioning","watch_indicators","one_liner","source"]:
        assert card.get(f), f"{c} 缺字段 {f}"
    assert card["source"].endswith(f"{c}.md"), f"{c} source 不对: {card['source']}"
    assert c in cm, f"cluster_match 缺 {c}"
text = p.read_text(encoding="utf-8")
assert not re.search(r"\d{6}", text), "出现 6 位数字（疑似时效数据/A股代码）"
assert not re.search(r"20\d{2}", text), "出现 4 位年份（疑似时效内容，应留知识层）"
assert "$" not in text
assert not re.search(r"必将|一定会|建议买入|包涨|稳赚", text), "出现断言/荐股式措辞"
print("OK fc1")
```

Run: `.venv/bin/python /tmp/verify_fc1.py`
Expected: FAIL（文件不存在）。

- [ ] **Step 2: 逐集群 Read 09 文件并蒸馏卡片**

对 16 个集群，逐个 Read `strategy/economic_policy/09-行业前景推演/<cluster>.md`，按下列规则提取 6 字段（**只取慢变量，剔除一切数字/年份/阈值**）：
- `main_issue`：取文件头"主驱动议题"行（含其 07/08 议题归属），如"双碳 + 新动能（08 议题④）"。
- `tone`：基调——顺风/逆风/分化/托底/转型（参考文件头与 `industry-signals` 的 signal 增/缩/转；用一个词 + 极简限定）。
- `positioning`：卡位方向——从该文件"六、劳动者含义"提炼 growth/转岗 方向（岗位类别，**不带薪资/数字**）。
- `watch_indicators`：从"五、可证伪点"取**指标名**（如"风光新增装机、新能源发电量占比"），**去掉一切阈值/数值**。
- `one_liner`：一句话方向（概括该集群"政策→前景"的方向，慢变、不含数据）。
- `source`：`strategy/economic_policy/09-行业前景推演/<cluster>.md`。

- [ ] **Step 3: 写文件 `skills/data/industry-forecast-tools.yaml`**

头部注释 + `forecasts:`（16 卡）+ `cluster_match:`（16 个 1:1）。**C 集群示范卡（按此格式产出其余 15 张）**：

```yaml
# 逐集群行业前景卡片速查（evergreen 蒸馏）
# 蒸馏自 strategy/economic_policy/09-行业前景推演/<cluster>.md（16 集群）
# 只含「慢变量」：主驱动议题 / 基调 / 卡位方向 / 观察指标名 / 一句话方向 / 详版指引。
# 不含时效数据：三情景阈值、带年份统计、待核实项一律留在知识层 09 文件（见各卡 source）。
# 维护：集群「基调」翻转时同步更新本卡；本卡是知识层的「指针+方向骨架」，不是数据副本。
# 不含个股/证券代码、不给点位时间表、不投资建议、不政治预测。

forecasts:
  C-绿色能源全链:
    main_issue: 双碳 + 新动能（08 议题④新质生产力 + 双碳长周期）
    tone: 顺风（后市场/运维被低估）
    positioning: 增量方向——储能系统工程师、电站运维、电网技术、碳资产管理；低端组件/电池片产能承压，宜往运维/回收/碳管理后市场卡位
    watch_indicators: 风光新增装机、新能源发电量占比、新型储能装机、弃电率（看方向不看点位）
    one_liner: 方向不可逆的长周期顺风，后市场比前市场大——往运维/储能/碳管理卡位
    source: strategy/economic_policy/09-行业前景推演/C-绿色能源全链.md
  # …其余 15 个集群同格式（A/B/D/E/F/G/H/I/J/K/L/M/N/O/P）…

cluster_match:
  A-先进制造与硬科技: [A-先进制造与硬科技]
  B-数字与智能产业: [B-数字与智能产业]
  C-绿色能源全链: [C-绿色能源全链]
  # …A–P 各映射到自己的卡（1:1）…
```

> 注：`cluster_match` 1:1 是为与同目录其它 tool 文件结构一致、并备未来"一卡多集群"之需；运行期 `get_industry_forecast_for_cluster` 直接用 cluster 键取卡。

- [ ] **Step 4: 再跑验证，确认通过**

Run: `.venv/bin/python /tmp/verify_fc1.py`
Expected: PASS（`OK fc1`）。

- [ ] **Step 5: 人工/grep 复核 evergreen 红线**

```bash
F=skills/data/industry-forecast-tools.yaml
grep -nE '20[0-9]{2}|[0-9]{4,}|[0-9]+\.[0-9]+%|[0-9]+万|[0-9]+亿' "$F" && echo "!! 疑似时效数字，需移回知识层" || echo "无时效数字 OK"
grep -c 'source: strategy/economic_policy/09-行业前景推演/' "$F"   # 期望 16
```
Expected: 第一行打印"无时效数字 OK"（若有命中，把对应数字从卡片删除，只留指标名/方向）；第二行 `16`。

- [ ] **Step 6: 提交**

```bash
git add skills/data/industry-forecast-tools.yaml
git commit -m "feat(engine): 新增逐集群行业前景卡片数据文件（16 卡·evergreen 蒸馏）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: router 加载器 + 访问函数

**Files:**
- Modify: `engine/router.py`（模块级 `_FORECAST` 加载，紧接 `_DEDUCTION` 之后；新函数 `get_industry_forecast_for_cluster`，放在 `get_policy_deduction_method` 之后、`get_regional_score` 之前）

- [ ] **Step 1: 写验证脚本，先跑确认失败**

存为 `/tmp/verify_fc2.py`：

```python
import sys, importlib, types
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
router = importlib.import_module('gongfu_engine.router')
clusters = ["A-先进制造与硬科技","B-数字与智能产业","C-绿色能源全链","D-农业与乡村振兴",
            "E-民生服务","F-文化创意与出海","G-基建物流房地产","H-新兴未来产业",
            "I-传统矿业与资源开采","J-传统轻纺与日用制造","K-传统重化工与建材","L-商贸零售与餐饮住宿",
            "M-金融与商务服务","N-教育与培训","O-居民生活服务","P-公用事业与市政服务"]
for c in clusters:
    card = router.get_industry_forecast_for_cluster(c)
    assert card and all(card.get(f) for f in ["main_issue","tone","positioning","watch_indicators","one_liner","source"]), f"{c} 卡不全: {card}"
assert router.get_industry_forecast_for_cluster("") == {}, "空 cluster 应返回 {}"
assert router.get_industry_forecast_for_cluster("不存在的集群") == {}, "未知 cluster 应返回 {}"
print("OK fc2")
```

Run: `.venv/bin/python /tmp/verify_fc2.py`
Expected: FAIL（`AttributeError: ... has no attribute 'get_industry_forecast_for_cluster'`）。

- [ ] **Step 2: 加模块级加载**

在 `engine/router.py` 中，把：

```python
_DEDUCTION = _load_yaml("policy-deduction-tools.yaml")
```

改成：

```python
_DEDUCTION = _load_yaml("policy-deduction-tools.yaml")
# 逐集群行业前景卡片（战略库第三根源·09 行业前景推演蒸馏·evergreen）
_FORECAST = _load_yaml("industry-forecast-tools.yaml")
```

- [ ] **Step 3: 加访问函数**

在 `engine/router.py` 中，把：

```python
    return {"method_steps": steps, "honest_boundaries": boundaries}


def get_regional_score(opportunity: str, region: str) -> int:
```

改成：

```python
    return {"method_steps": steps, "honest_boundaries": boundaries}


def get_industry_forecast_for_cluster(cluster: str) -> dict:
    """Get the evergreen per-cluster industry-forecast card.

    Distilled from strategy/economic_policy/09-行业前景推演/<cluster>.md — slow-moving
    fields only (main_issue/tone/positioning/watch_indicators/one_liner/source); the
    time-sensitive specifics live in the knowledge file pointed to by `source`.
    Returns {} if cluster is empty or has no card.
    """
    if not cluster:
        return {}
    forecasts = _FORECAST.get("forecasts", {})
    card = forecasts.get(cluster, {})
    if not card:
        return {}
    return {
        "main_issue": card.get("main_issue", ""),
        "tone": card.get("tone", ""),
        "positioning": card.get("positioning", ""),
        "watch_indicators": card.get("watch_indicators", ""),
        "one_liner": card.get("one_liner", ""),
        "source": card.get("source", ""),
    }


def get_regional_score(opportunity: str, region: str) -> int:
```

> 注：`return {"method_steps": steps, "honest_boundaries": boundaries}` 是 `get_policy_deduction_method` 的唯一返回，组合 `def get_regional_score` 后匹配唯一，可安全替换。

- [ ] **Step 4: 再跑验证，确认通过**

Run: `.venv/bin/python /tmp/verify_fc2.py`
Expected: PASS（`OK fc2`）。

- [ ] **Step 5: import 健康检查**

Run: `.venv/bin/python -c "import sys,types,importlib; p=types.ModuleType('gongfu_engine'); p.__path__=['engine']; sys.modules['gongfu_engine']=p; importlib.import_module('gongfu_engine.router'); print('import OK')"`
Expected: `import OK`。

- [ ] **Step 6: 提交**

```bash
git add engine/router.py
git commit -m "feat(engine): router 加载行业前景卡片 + get_industry_forecast_for_cluster()

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: tools 注入

**Files:**
- Modify: `engine/tools.py`（`_handle_analyze`，紧接 `policy_deduction` 注入块之后）

- [ ] **Step 1: 写验证脚本，先跑确认失败**

存为 `/tmp/verify_fc3.py`：

```python
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')

def analyze(s):
    return json.loads(tools.gongfu_consult({"situation": s, "mode": "analyze"}))

# 1) 行业判断 + 有行业（光伏→C） → 注入
r1 = analyze("我在光伏厂干了几年，想知道这个行业方向好不好")
assert "industry-scan" in r1["triage"]["route_to"], r1["triage"]["route_to"]
assert r1["triage"]["extracted_info"].get("cluster") == "C-绿色能源全链"
assert "industry_forecast" in r1["knowledge_context"], "行业判断+集群未注入"
card = r1["knowledge_context"]["industry_forecast"]
assert all(card.get(f) for f in ["main_issue","tone","positioning","watch_indicators","one_liner","source"]), card

# 2) 趋势前瞻 + 有行业（养老→E） → 注入
r2 = analyze("我做养老护理，想看看这个行业未来的趋势和机会")
assert "industry_forecast" in r2["knowledge_context"], "趋势前瞻+集群未注入"

# 3) 趋势前瞻 + 无行业 → 不注入（卡片依赖 cluster）
r3 = analyze("我30岁，想看看未来几年的趋势和机会")
assert r3["triage"]["extracted_info"].get("cluster") in (None, ""), r3["triage"]["extracted_info"].get("cluster")
assert "industry_forecast" not in r3["knowledge_context"], "无集群却注入了"

# 4) 纯创业、无趋势/行业判断路由 → 不注入
r4 = analyze("我想自己开个小吃店，手里有十万存款")
assert "industry_forecast" not in r4["knowledge_context"], "不该注入却注入了"
print("OK fc3")
```

Run: `.venv/bin/python /tmp/verify_fc3.py`
Expected: FAIL（断言"行业判断+集群未注入"）。

- [ ] **Step 2: 加注入块**

在 `engine/tools.py` 的 `_handle_analyze` 中，把：

```python
    if "opportunity-radar" in route_to or "industry-scan" in route_to:
        deduction = router.get_policy_deduction_method()
        if deduction:
            knowledge_context["policy_deduction"] = deduction

    # 优势视角：提炼用户已经拥有的
```

改成：

```python
    if "opportunity-radar" in route_to or "industry-scan" in route_to:
        deduction = router.get_policy_deduction_method()
        if deduction:
            knowledge_context["policy_deduction"] = deduction

    # ── 注入逐集群行业前景卡片（09 行业前景推演蒸馏·evergreen）──
    # 仅 evergreen 方向骨架（主驱动/基调/卡位/观察指标名/详版指引），不含时效数据；
    # 行业判断/趋势前瞻类路由且识别出 cluster 时注入
    if info.get("cluster") and (
        "industry-scan" in route_to or "opportunity-radar" in route_to
    ):
        forecast = router.get_industry_forecast_for_cluster(info["cluster"])
        if forecast:
            knowledge_context["industry_forecast"] = forecast

    # 优势视角：提炼用户已经拥有的
```

> 注：上面 `policy_deduction` 注入三行 + 空行 + `# 优势视角` 的组合在文件中唯一，可安全匹配。

- [ ] **Step 3: 再跑验证，确认通过**

Run: `.venv/bin/python /tmp/verify_fc3.py`
Expected: PASS（`OK fc3`）。

- [ ] **Step 4: 提交**

```bash
git add engine/tools.py
git commit -m "feat(engine): gongfu_consult 在行业判断/趋势前瞻且识别集群时注入 industry_forecast

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: 升版本 v1.5.0 + CHANGELOG + README + CLAUDE.md

**Files:** `pyproject.toml:3`、`engine/plugin.yaml:2`、`api_server/server.py:100`、`README.md:7`、`CHANGELOG.md`、`CLAUDE.md:78`

> 引擎改动，按约定升版本。目标 **v1.5.0**。控制器在 merge 阶段会与用户确认版本号。

- [ ] **Step 1: 三处版本号 1.4.0 → 1.5.0**
`pyproject.toml`：`version = "1.4.0"` → `version = "1.5.0"`。
`engine/plugin.yaml`：`version: 1.4.0` → `version: 1.5.0`。
`api_server/server.py`：`"version": "1.4.0",` → `"version": "1.5.0",`。

- [ ] **Step 2: README 版本行**
`README.md`：`> 当前版本 **v1.4.0** ｜ 升级与变更说明见 [CHANGELOG.md](CHANGELOG.md)` → 把 `v1.4.0` 改为 `v1.5.0`。

- [ ] **Step 3: CHANGELOG —— 新开 [1.5.0]，把累计的两条行业前景知识条目转入本版**
先 Read `CHANGELOG.md`。把：

```
## [未发布]

### 新增 Added（纯知识内容，不升版本）

```

改成：

```
## [未发布]

## [1.5.0] - 2026-06-26

逐集群行业前景接入引擎（战略库第三根源·09 行业前景推演蒸馏），并把此前累计的两批"逐集群行业前景推演"知识层随本版一并记录。对终端使用者**功能只增不减**：在行业判断 / 趋势前瞻类咨询且识别出产业集群时，多一张该集群"政策→前景"的方向卡片（`industry_forecast`：主驱动议题 / 基调 / 卡位方向 / 观察指标 / 详版指引），给方向不给时间表、不个股、不政治预测。

### 新增 Added

- **引擎接入：逐集群行业前景卡片（evergreen）**。新增 `skills/data/industry-forecast-tools.yaml`（16 集群 evergreen 卡片，**只含**主驱动议题/基调/卡位方向/观察指标名/一句话方向/详版指引，**不含**三情景阈值、带年份统计、待核实项等时效内容——后者留在 `09-行业前景推演/<cluster>.md`）；`engine/router.py` 增 `get_industry_forecast_for_cluster()`；`gongfu_consult` 在行业判断 / 趋势前瞻类咨询且识别出 cluster 时注入 `industry_forecast`，与 `industry`（静态信号）/`chain_tools`（产业链卡点）/`policy_deduction`（通用方法）互补。

```

（这把 `### 新增 Added（纯知识内容…）` 子标题替换为 `## [1.5.0]` 段 + 引擎条目 + 普通 `### 新增 Added`；原标题下方那两条行业前景知识条目位置不动，自然落到 `[1.5.0]` 之下。）

- [ ] **Step 4: 修正两条知识条目里"不升版本/引擎接入另开 spec"的过期措辞**
在 `CHANGELOG.md` 中，把首批条目结尾：
```
情景为方向研判非预言，不个股、不政治预测。纯知识内容、未改引擎、不升版本；其余 10 集群与引擎接入另开 spec。
```
改成：
```
情景为方向研判非预言，不个股、不政治预测。随 v1.5.0 一并记录。
```
再把第二批条目结尾：
```
对偏市场/结构驱动的集群（O/L/J/F）如实交代政策成色，不硬凑政策叙事。情景为方向研判非预言，不个股、不政治预测。纯知识内容、未改引擎、不升版本；逐集群引擎接入另开 spec。
```
改成：
```
对偏市场/结构驱动的集群（O/L/J/F）如实交代政策成色，不硬凑政策叙事。情景为方向研判非预言，不个股、不政治预测。随 v1.5.0 一并记录；引擎接入见本版"引擎接入"条目。
```

- [ ] **Step 5: CLAUDE.md 数据清单 13 → 14**
先 Read `CLAUDE.md`。把第 78 行末尾的 `policy-deduction-tools` 描述句号前补一项，并把 `13 files` 改为 `14 files`。具体：把
```
13 files: `industry-signals`,
```
改为
```
14 files: `industry-signals`,
```
并在该行结尾 `...在趋势前瞻/行业判断时注入 `policy_deduction`).` 之后追加：
```
, `industry-forecast-tools` (逐集群行业前景 evergreen 卡片，战略库第三根源·09 蒸馏，由 `get_industry_forecast_for_cluster()` 在行业判断/趋势前瞻且识别集群时注入 `industry_forecast`).
```
（即在 13→14 文件清单里把 `industry-forecast-tools` 列入。注意句子通顺：原句以 `).` 结尾，改为 `), 加 industry-forecast-tools (...).`。实现时 Read 该行后做一次完整替换以保证语句通顺。）

- [ ] **Step 6: 验证版本一致 + 提交**
```bash
grep -n '1.5.0' pyproject.toml engine/plugin.yaml api_server/server.py README.md
grep -c 'industry-forecast-tools' CLAUDE.md   # 期望 ≥1
grep -q '14 files' CLAUDE.md && echo "数据清单 14 OK" || echo "!! 清单未更新"
```
Expected: 四个版本文件各出现 1.5.0；CLAUDE.md 含 industry-forecast-tools 且"14 files"。
```bash
git add pyproject.toml engine/plugin.yaml api_server/server.py README.md CHANGELOG.md CLAUDE.md
git commit -m "chore: 升版本 v1.5.0 + CHANGELOG/README/CLAUDE 同步（行业前景引擎接入）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: 重建派生包 + 四壳一致 + 端到端冒烟

**Files:** 无源改动（`build_packs.py` 输出 gitignored）。

- [ ] **Step 1: 重建派生包**
Run: `.venv/bin/python scripts/build_packs.py`
Expected: 正常结束、无报错。

- [ ] **Step 2: 四壳一致——源与生成副本字节一致**
存为 `/tmp/verify_fc5.py`：
```python
import pathlib
src = pathlib.Path("skills/data/industry-forecast-tools.yaml").read_bytes()
copies = [
    "claude-skills/data/industry-forecast-tools.yaml",
    "agents/zcode-skills/data/industry-forecast-tools.yaml",
]
missing = [c for c in copies if not pathlib.Path(c).exists()]
assert not missing, f"派生副本缺失（先跑 build_packs）: {missing}"
for c in copies:
    assert pathlib.Path(c).read_bytes() == src, f"副本与源不一致: {c}"
print("OK fc5 (四壳数据一致)")
```
Run: `.venv/bin/python /tmp/verify_fc5.py`
Expected: PASS。

- [ ] **Step 3: 端到端冒烟——含集群 vs 无集群 vs 纯创业**
存为 `/tmp/verify_fc_e2e.py`：
```python
import sys, importlib, types, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
def run(s): return json.loads(tools.gongfu_consult({"situation": s, "mode": "analyze"}))
cases = [
    ("我在光伏厂干了几年，想知道这个行业方向好不好", True),
    ("我做养老护理，想看看这个行业未来的趋势和机会", True),
    ("我30岁，想看看未来几年的趋势和机会", False),   # 无集群
    ("我想自己开个小吃店，手里有十万存款", False),       # 纯创业
]
for s, want in cases:
    has = "industry_forecast" in run(s).get("knowledge_context", {})
    assert has == want, f"判定错: {s!r} 期望={want} 实际={has}"
    print(f"  {'注入' if has else '不注入'} <- {s}")
print("OK fc e2e")
```
Run: `.venv/bin/python /tmp/verify_fc_e2e.py`
Expected: PASS（三行 + `OK fc e2e`）。

- [ ] **Step 4: 收尾**
派生产物 gitignored、无需提交。
```bash
git status --porcelain
```
Expected: 空。若非空，停下核对（不应有未忽略改动）。

---

## Self-Review（写完计划后的自检）

**Spec 覆盖：**
- spec §3 卡片 6 字段 → Task 1（YAML）+ Task 2（函数返回 6 字段）✅
- spec §4 数据文件（forecasts + cluster_match，16 卡）→ Task 1 ✅
- spec §5.1 router 加载器+访问函数 → Task 2 ✅
- spec §5.2 tools 注入（cluster + route_to）→ Task 3 ✅；schemas 不动 ✅
- spec §6 evergreen 防过时（卡只放慢变量、source 指知识层）→ Task 1 蒸馏规则 + Step 5 红线 grep ✅
- spec §10 验证（单元 16 卡 / 注入正负例 / 红线无时效数字 / 四壳 / 版本）→ Task 1/2/3/5 + Task 4 ✅
- spec §9 版本与文档（v1.5.0 三处 + CHANGELOG 转入两批知识条目 + README + CLAUDE 13→14）→ Task 4 ✅
- spec §11 非目标（不搬时效数据/不改 schemas/不动 industry-signals）→ 计划无相关改动 ✅

**Placeholder 扫描：** 无 TBD/TODO。Task 1 给了 C 示范卡 + 逐字段蒸馏规则（其余 15 卡按同格式从文件提取，非占位符——内容须从 09 文件蒸馏，不能预写死）。每个改代码步骤都给了完整代码 + 精确锚点。✅

**一致性：** 函数名全程 `get_industry_forecast_for_cluster`；返回/卡片 6 字段全程 `main_issue/tone/positioning/watch_indicators/one_liner/source`；注入键 `knowledge_context["industry_forecast"]`；数据文件 `industry-forecast-tools.yaml`；模块变量 `_FORECAST`——Task 1–5 一致。✅

**执行提示（给控制器）：** Task 1 是从 16 个 09 文件蒸馏 evergreen 卡——派实现 subagent 时要它逐个 Read 09 文件、严格剔除年份/数字/阈值（evergreen 红线），不得引入文件外判断。Task 2/3 机械（完整代码+锚点）。每任务走"实现 → spec 合规 → 代码质量"两段评审；最后整支 opus 终审，再收尾。
