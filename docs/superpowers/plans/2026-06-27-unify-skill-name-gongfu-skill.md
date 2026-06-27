# 技能入口统一为单一 gongfu-skill 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把对外技能从 7 个折叠为唯一的 `gongfu-skill` 前门，6 个能力下沉为内部参考，三标识符（插件名/toolset/技能名）全部对齐 `gongfu-skill`，运行时引擎逻辑零改动、知识零损失。

**Architecture:** `skills/situation-triage/` 改名为 `skills/gongfu-skill/`（唯一对外技能）；原 6 个能力 `SKILL.md` 移入 `skills/gongfu-skill/references/<name>.md`（内部参考，不再注册为技能）；`engine/__init__.py` 仅把 toolset `gongfu` 改名为 `gongfu-skill`；`build_packs.py` 扩展为连 `references/` 子目录一起复制到三处派生包；`gongfu_consult` 工具与 `/consult` 接口保持不变。

**Tech Stack:** Python 3.12（仓库 `.venv` 已就绪）、标准库 `shutil`/`pathlib`；无 pytest——验证一律走"合成包 `gongfu_engine` bootstrap"脚本（与 `mcp_server`/`api_server` 同款）+ 文件系统/grep 静态检查。

**前置说明（关键事实，执行者必读）：**
- `engine/tools.py::gongfu_consult` 对所有路径都返回 **JSON 字符串**（不是 dict）。断言前必须 `json.loads(...)`。
- intake 模式：`route_to` 在**顶层**；`need_basic_info` 路径**没有** `route_to` 字段。
- analyze 模式：返回 `{"type":"analysis", "triage":{"route_to":[...],"extracted_info":{...}}, "tone_instruction","knowledge_context","execution_guide"}`——`route_to` 嵌在 `triage` 下，**不在顶层**。
- 工作目录：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`，所有命令在此根下跑。
- 分支：已在 `feat/unify-skill-name-gongfu-skill` 上（spec 已提交于此）。
- 每个能力 skill 目录当前**只含 `SKILL.md`**（已核实），`git mv` 后原目录会变空、需删除。
- `route_to` 取值（`problem-diagnosis`/`industry-scan`/`startup-feasibility`/`growth-planner`/`collaboration-match`/`opportunity-radar`）是引擎内部路由标签，**本计划不改动任何引擎路由分支**；它们与 `references/<name>.md` 文件名一一对应。

---

## Task 1: 特征化安全网（动手前先建立基线）

> 这是 refactor，不是新功能。这里写的是**特征化测试**：它必须在**未改动**的引擎上就 PASS（证明断言与当前行为一致、锁定基线），改造后还要继续 PASS。

**Files:**
- 无需创建仓库内文件（用内联 heredoc 运行，不污染 git）。

- [ ] **Step 1: 在当前（未改动）引擎上运行特征化脚本，确认全部 PASS**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
import sys, types, importlib, json
p = types.ModuleType('gongfu_engine'); p.__path__ = ['engine']
sys.modules['gongfu_engine'] = p
tools = importlib.import_module('gongfu_engine.tools')
consult = tools.gongfu_consult

def J(situation, mode="intake"):
    return json.loads(consult({"situation": situation, "mode": mode}))

# 1. intake：有行业无意图 → 默认 industry-scan
r = J("我在光伏电站做运维")
assert r.get("route_to") == ["industry-scan"], ("case1", r.get("route_to"))

# 2. intake：多意图 → 困境优先 + 创业
r = J("我38岁做芯片封测十年，怕被替代，也想搞点副业")
assert r.get("route_to") == ["problem-diagnosis", "startup-feasibility"], ("case2", r.get("route_to"))

# 3. 危机信号 → 特殊态，不路由
r = J("我不想活了，感觉没有出路")
assert r.get("type") == "special" and r.get("handling") == "crisis", ("case3", r)

# 4. 无行业无意图 → need_basic_info
r = J("你好啊")
assert r.get("type") == "intake" and r.get("phase") == "need_basic_info", ("case4", r)

# 5. analyze：注入知识（route_to 在 triage 下）
r = J("我38岁在长三角做光伏运维，想了解这个行业前景，该不该转", mode="analyze")
assert r.get("type") == "analysis", ("case5-type", r.get("type"))
assert "industry-scan" in r.get("triage", {}).get("route_to", []), ("case5-route", r.get("triage"))
assert isinstance(r.get("knowledge_context"), dict) and r["knowledge_context"], ("case5-kc", list(r.keys()))
assert r.get("execution_guide"), ("case5-guide",)

print("REGRESSION ALL PASS")
PY
```
Expected: 末行打印 `REGRESSION ALL PASS`，进程退出码 0。

- [ ] **Step 2: 若任一断言失败**

说明我对当前行为的判断有误（不是代码 bug）。把失败用例的实际输出贴出来，**修正脚本里的期望值**使其匹配当前引擎，再次运行至 PASS。这一步只校准基线，不改任何源码。

- [ ] **Step 3: 把这段脚本原文存到便笺，供 Task 6/Task 10 复用**

Run:
```bash
mkdir -p /private/tmp/claude-501/-Users-housebigger-Documents-01-work-playground-hermes-gongfu-skill/ab3afe89-5a7f-4e05-835d-4cdbc821b0b4/scratchpad
```
把 Step 1 的 heredoc 脚本体（`import` 到 `print("REGRESSION ALL PASS")`）写入 `.../scratchpad/regress_unify.py`，后续用 `.venv/bin/python .../scratchpad/regress_unify.py` 复跑。（scratchpad 在仓库外，不进 git。）

> 本任务无代码改动、无提交。

---

## Task 2: 重构源目录树（纯 git mv，不改内容）

**Files:**
- Rename: `skills/situation-triage/` → `skills/gongfu-skill/`
- Create dir: `skills/gongfu-skill/references/`
- Move: 6 个 `skills/<cap>/SKILL.md` → `skills/gongfu-skill/references/<cap>.md`
- Delete: 6 个空的 `skills/<cap>/` 目录

- [ ] **Step 1: 把前门技能目录改名**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git mv skills/situation-triage skills/gongfu-skill
mkdir -p skills/gongfu-skill/references
```

- [ ] **Step 2: 把 6 个能力 SKILL.md 移入 references/（文件名取能力名）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
for c in industry-scan startup-feasibility growth-planner collaboration-match opportunity-radar problem-diagnosis; do
  git mv "skills/$c/SKILL.md" "skills/gongfu-skill/references/$c.md"
  rmdir "skills/$c"
done
```

- [ ] **Step 3: 核对结构**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
echo "--- skills/ 顶层（应只剩 gongfu-skill/ 和 data/ 及说明 md）---"; ls -1 skills/
echo "--- gongfu-skill/ ---"; ls -1 skills/gongfu-skill/
echo "--- references/（应有 6 个 .md）---"; ls -1 skills/gongfu-skill/references/
```
Expected:
- `skills/` 顶层只有 `gongfu-skill/`、`data/`、`00-skill设计规范.md`、`README.md`（无 6 个能力目录、无 `situation-triage/`）。
- `skills/gongfu-skill/` 含 `SKILL.md` 和 `references/`。
- `references/` 含 `industry-scan.md`、`startup-feasibility.md`、`growth-planner.md`、`collaboration-match.md`、`opportunity-radar.md`、`problem-diagnosis.md`。

- [ ] **Step 4: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add -A
git commit -q -m "refactor(skills): situation-triage 改名 gongfu-skill；6 能力 SKILL.md 下沉 references/

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: 改写前门 SKILL.md（name/描述/标题/能力分派段）

**Files:**
- Modify: `skills/gongfu-skill/SKILL.md`

> 只做 5 处定点编辑，不动 crisis/intake/交互流程/测试用例/源文档映射等既有内容。

- [ ] **Step 1: 改 frontmatter（name + version + description）**

把开头的：
```yaml
name: situation-triage
description: "Use as the router/intake layer when a worker comes for consultation — FIRST listen and connect with the person (borrowing from Carl Rogers' person-centered counseling), THEN gradually understand their situation through gentle multi-turn dialogue, CONFIRM before concluding."
version: 3.0.0
```
改为：
```yaml
name: gongfu-skill
description: "共富参谋——一线劳动者的随身参谋（唯一统一入口）。当劳动者想了解行业前景、评估创业、走出职业困境、规划成长、寻找协作、或看清未来趋势时使用。先倾听接住情绪，再用温柔的多轮对话了解情况，确认后才下判断；内部按意图路由到 6 类能力（困境诊断/行业判断/创业评估/成长规划/协作匹配/趋势前瞻），通过 gongfu_consult 工具加载知识。直接把用户原话传进来即可。"
version: 4.0.0
```

- [ ] **Step 2: 改标题行**

把：
```markdown
# 情况分诊 skill（路由层 · 春风化雨版 v3）
```
改为：
```markdown
# 共富参谋 skill（统一入口 · 春风化雨版 v4）
```

- [ ] **Step 3: 改概述首段（说明这是唯一入口 + 能力下沉）**

把：
```markdown
这个 skill 是整个共富参谋体系的**路由入口**。用户用自然语言描述自己的处境，skill 解析意图、抽取结构化信息，并决定调用哪些下游 skill（problem-diagnosis / industry-scan / startup-feasibility / growth-planner / collaboration-match / opportunity-radar）。
```
改为：
```markdown
这个 skill 是整个共富参谋体系**对外的唯一入口**。用户用自然语言描述自己的处境，skill 解析意图、抽取结构化信息，并决定走哪几类能力。原先的 6 个能力（problem-diagnosis / industry-scan / startup-feasibility / growth-planner / collaboration-match / opportunity-radar）已下沉为本目录的**内部参考**（`references/`），不再单独作为技能上架——对外只有 `gongfu-skill` 一个名字。
```

- [ ] **Step 4: 在概述之后插入"能力分派与内部参考"新段**

在概述小节末尾（即"### 3. 真诚（Genuineness）"那一段之后、`## 何时使用 / 不要用于` 之前）插入：
```markdown
## 能力分派与内部参考

运行时由引擎 `gongfu_consult` 返回的 `route_to` 决定走哪几类能力；每类能力的详细**输出模板**见对应内部参考文档：

| route_to 取值 | 能力 | 输出模板参考 |
|---|---|---|
| problem-diagnosis | 困境诊断（主要矛盾 / 阶段判断） | `references/problem-diagnosis.md` |
| industry-scan | 行业判断（增/转/缩 + 地域校准） | `references/industry-scan.md` |
| startup-feasibility | 创业评估（四路径 + 劝退红线） | `references/startup-feasibility.md` |
| growth-planner | 成长规划（四画像成长地图） | `references/growth-planner.md` |
| collaboration-match | 协作匹配（五形态 + 分钱规则） | `references/collaboration-match.md` |
| opportunity-radar | 趋势前瞻（5—10 年 + 确定性增量） | `references/opportunity-radar.md` |

用法：拿到 `route_to` 后，对其中每个能力，读取对应 `references/<能力>.md` 的「输出规格」段，按模板组织该部分回复。引擎返回的 `execution_guide` / `tone_instruction` 决定语气与顺序，两者配合使用——参考给"输出长什么样"，execution_guide 给"用什么语气、按什么次序说"。

```

- [ ] **Step 5: 改"不要用于"小节（子技能已不可单独调用 → 改为内部快进语义）**

把：
```markdown
## 何时使用 / 不要用于
```
改为：
```markdown
## 何时使用 / 何时快进
```
并把该小节里的"**不要用于**"块：
```markdown
**不要用于**：
- 用户已明确说"我就想知道行业前景"——直接用 industry-scan
- 用户已明确问创业可行性——直接用 startup-feasibility
- 下游 skill 已经开始、正在收集信息的中途——不要再触发 triage
- 纯趋势/政策问题（AI 会不会替代某职业）——可直接用 opportunity-radar
```
改为：
```markdown
**何时快进（跳过铺垫，让引擎直接路由）**：
- 用户已明确说"我就想知道行业前景"——引擎直接路由到 industry-scan 能力（输出模板见 `references/industry-scan.md`）
- 用户已明确问创业可行性——引擎直接路由到 startup-feasibility 能力（见 `references/startup-feasibility.md`）
- 已在多轮收集信息的中途——不要重复分诊、不要重问已经问过的内容
- 纯趋势/政策问题（AI 会不会替代某职业）——引擎直接路由到 opportunity-radar 能力（见 `references/opportunity-radar.md`）
```

- [ ] **Step 6: 自检并提交**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
head -12 skills/gongfu-skill/SKILL.md
grep -n "能力分派与内部参考\|何时快进\|name: gongfu-skill\|version: 4.0.0" skills/gongfu-skill/SKILL.md
```
Expected: frontmatter `name: gongfu-skill`、`version: 4.0.0`；能找到"能力分派与内部参考"和"何时快进"。
```bash
git add skills/gongfu-skill/SKILL.md
git commit -q -m "refactor(skill): 前门 SKILL.md 改名 gongfu-skill + 拓宽描述 + 能力分派段

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: engine/__init__.py — toolset 改名

**Files:**
- Modify: `engine/__init__.py`（约 28 行）

> 工具名 `gongfu_consult` 不变（集成契约）；技能注册循环代码不动（重建派生包后 `engine/skills` 下只剩 `gongfu-skill`，循环自然只注册一个）。本任务只改 toolset 字符串。

- [ ] **Step 1: 改 toolset**

把：
```python
    ctx.register_tool(
        name="gongfu_consult",
        toolset="gongfu",
```
改为：
```python
    ctx.register_tool(
        name="gongfu_consult",
        toolset="gongfu-skill",
```

- [ ] **Step 2: 确认工具名未被误改、toolset 已改**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -n 'name="gongfu_consult"\|toolset=' engine/__init__.py
```
Expected: `name="gongfu_consult"` 仍在；`toolset="gongfu-skill"`。

- [ ] **Step 3: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add engine/__init__.py
git commit -q -m "refactor(engine): toolset gongfu→gongfu-skill（工具名 gongfu_consult 不变）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: build_packs.py — 让 references/ 随技能进入三处派生包

**Files:**
- Modify: `scripts/build_packs.py`（复制循环，当前 line 58-61）

- [ ] **Step 1: 扩展复制逻辑，携带 references/ 子目录**

把：
```python
        for d in skill_dirs:
            dest = skills_dest / d.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(d / "SKILL.md", dest / "SKILL.md")
```
改为：
```python
        for d in skill_dirs:
            dest = skills_dest / d.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(d / "SKILL.md", dest / "SKILL.md")
            # 携带 skill 的内部参考文档（references/）——前门 SKILL.md 会按 route_to 读取，
            # 故三处派生包（含 engine/skills）都必须带上，否则 agent 找不到输出模板。
            refs = d / "references"
            if refs.is_dir():
                shutil.copytree(refs, dest / "references", dirs_exist_ok=True)
```

- [ ] **Step 2: 单独验证脚本可运行、无语法错**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python -c "import ast; ast.parse(open('scripts/build_packs.py').read()); print('SYNTAX OK')"
```
Expected: `SYNTAX OK`

- [ ] **Step 3: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add scripts/build_packs.py
git commit -q -m "build(packs): 复制 skill 时一并携带 references/ 子目录到三处派生包

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: 重建派生包并做整体回归（结构 + 注册 + 引擎行为）

**Files:**
- 生成（gitignored）：`engine/skills/`、`claude-skills/skills/`+`claude-skills/data/`、`agents/zcode-skills/`

- [ ] **Step 1: 重建派生包**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python scripts/build_packs.py
```
Expected: 输出三行 `[build_packs] ...: 1 skills...`（每处只有 1 个 skill），末行 `done`。

- [ ] **Step 2: 验证三处派生包都只含 gongfu-skill 且 references/ 完整**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
for base in engine/skills claude-skills/skills agents/zcode-skills; do
  echo "=== $base ==="
  ls -1 "$base"
  echo "  refs:"; ls -1 "$base/gongfu-skill/references" 2>/dev/null
done
```
Expected: 每个 base 顶层只有 `gongfu-skill`（zcode 处可能另有 `data/`，正常）；每个 `gongfu-skill/references/` 都含 6 个 `.md`；无 `situation-triage` 或其它旧能力目录。

- [ ] **Step 3: 静态验证注册面（toolset + 实际会被注册的技能集合）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python - <<'PY'
from pathlib import Path
# 复刻 engine/__init__.py 注册循环的判定：engine/skills 下含 SKILL.md 的目录
skills_dir = Path("engine/skills")
registered = sorted(c.name for c in skills_dir.iterdir()
                    if c.is_dir() and (c / "SKILL.md").exists())
assert registered == ["gongfu-skill"], registered
src = Path("engine/__init__.py").read_text(encoding="utf-8")
assert 'toolset="gongfu-skill"' in src, "toolset 未改名"
assert 'name="gongfu_consult"' in src, "工具名被误改"
print("REGISTRATION OK:", registered)
PY
```
Expected: `REGISTRATION OK: ['gongfu-skill']`

- [ ] **Step 4: 复跑特征化安全网（引擎行为必须不变）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python /private/tmp/claude-501/-Users-housebigger-Documents-01-work-playground-hermes-gongfu-skill/ab3afe89-5a7f-4e05-835d-4cdbc821b0b4/scratchpad/regress_unify.py
```
Expected: `REGRESSION ALL PASS`

- [ ] **Step 5: 无需提交**（派生包已 gitignore）。若 `git status` 显示派生包为已追踪文件而出现改动，停止并报告（说明 .gitignore 与预期不符，需先处理）。

---

## Task 7: 文档更新 — README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 手动触发 `/gongfu` → `/gongfu-skill`**

把：
```
/gongfu 我30岁在工厂干了10年，最近产线上了机器人，我怕被替代，该怎么办
```
改为：
```
/gongfu-skill 我30岁在工厂干了10年，最近产线上了机器人，我怕被替代，该怎么办
```

- [ ] **Step 2: claude-skills 段落 "7 个 SKILL.md" → 单一入口**

把 line 200 一带：
```
`claude-skills/` 目录是一个自包含的知识包，可以直接放进 Claude Code 项目。包含 7 个 SKILL.md + 14 个 YAML 知识库 + 一个 CLAUDE.md 入口。
```
改为：
```
`claude-skills/` 目录是一个自包含的知识包，可以直接放进 Claude Code 项目。包含 1 个 SKILL.md（gongfu-skill，内附 6 个能力参考 references/）+ 14 个 YAML 知识库 + 一个 CLAUDE.md 入口。
```

- [ ] **Step 3: 手动指定模块的两处示例 → 单一技能**

把 line 208：
```
也可以手动指定模块：`请读取 skills/industry-scan/SKILL.md，帮我分析制造业产线工人的前景`。
```
改为：
```
也可以手动指定：`请读取 skills/gongfu-skill/SKILL.md，帮我分析制造业产线工人的前景`（行业判断的输出模板在 `skills/gongfu-skill/references/industry-scan.md`）。
```
把 line 251（ZCode 调用示例）：
```
然后在 ZCode 中：Settings → Skills → Refresh，对话中用 `$industry-scan 分析制造业前景` 调用。
```
改为：
```
然后在 ZCode 中：Settings → Skills → Refresh，对话中用 `$gongfu-skill 分析制造业前景` 调用。
```

- [ ] **Step 4: 目录树（line 283-298）里的 7 SKILL.md 表述**

把：
```
├── skills/                第三阶段知识源：7 个 SKILL.md + data/（★单一源）
```
改为：
```
├── skills/                第三阶段知识源：gongfu-skill/（前门 SKILL.md + references/ 6 能力）+ data/（★单一源）
```
把：
```
│   ├── problem-diagnosis/ | industry-scan/ | startup-feasibility/
│   ├── growth-planner/    | collaboration-match/ | opportunity-radar/
│   ├── situation-triage/  路由层
```
改为：
```
│   ├── gongfu-skill/      唯一对外技能（前门）
│   │   ├── SKILL.md       统一入口：分诊/路由/情绪优先
│   │   └── references/    6 能力内部参考：problem-diagnosis / industry-scan /
│   │                      startup-feasibility / growth-planner /
│   │                      collaboration-match / opportunity-radar
```
把两处 `⚙生成：内嵌 7 个 SKILL.md` 和 `⚙生成：7 个 SKILL.md`（line 291、298）各自改为 `⚙生成：内嵌 gongfu-skill（含 references/）` 与 `⚙生成：gongfu-skill（含 references/）`。

- [ ] **Step 5: 顶部版本行**（与 Task 9 一致，此处先一并改）

把 line 7：
```
> 当前版本 **v1.6.0** ｜ 升级与变更说明见 [CHANGELOG.md](CHANGELOG.md)
```
改为：
```
> 当前版本 **v1.7.0** ｜ 升级与变更说明见 [CHANGELOG.md](CHANGELOG.md)
```

- [ ] **Step 6: 核对无残留并提交**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -nE "/gongfu |\$industry-scan|7 个 SKILL|内嵌 7 个|situation-triage" README.md || echo "NO STALE REFS"
```
Expected: `NO STALE REFS`（若有命中，逐条按上面规则修正）。注意用 `grep -E`（macOS 自带 BSD grep 不把 `\|` 当或，必须用 `-E` 的 `|`）。
```bash
git add README.md
git commit -q -m "docs(readme): 触发词 /gongfu→/gongfu-skill、ZCode \$gongfu-skill、单一入口表述、版本行 v1.7.0

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: 文档更新 — 其余手写文档

**Files:**
- Modify: `skills/README.md`、`agents/AGENTS.md`、`claude-skills/CLAUDE.md`、`CLAUDE.md`、`skills/00-skill设计规范.md`

- [ ] **Step 1: `agents/AGENTS.md` 的"7 个知识模块"表 → 单一入口 + 6 能力**

把 line 21 标题与 line 25-31 的表（`## 7 个知识模块` 起到 opportunity-radar 行止）整体替换为：
```markdown
## 一个技能，六类能力

对外只有一个技能 `gongfu-skill`（唯一入口）。用户用大白话描述处境，引擎按意图在内部路由到下面六类能力；每类能力的输出模板见 `gongfu-skill/references/<能力>.md`。

| 内部能力（route_to） | 何时触发 |
|---|---|
| problem-diagnosis | 面临困境/迷茫——用矛盾分析、持久战等工具诊断主要矛盾 |
| industry-scan | 想了解行业前景——16 集群信号（增/转/缩）+ 5 大地域校准 |
| startup-feasibility | 考虑创业——4 条零成本路径评估 + 止损红线 |
| growth-planner | 想规划成长——4 种画像的成长地图 |
| collaboration-match | 找人合作——5 种协作形态 + 分钱规则 |
| opportunity-radar | 看未来趋势——5-10 年前瞻 + 十大确定性增量 |
```

- [ ] **Step 2: `claude-skills/CLAUDE.md` 同款表 + 概述句 + 示例**

把 line 7：
```
共富参谋是一套面向中国一线劳动者的职业判断知识体系。它把行业前景、创业可行性、成长规划、协作方法、趋势前瞻，蒸馏成 7 个可调用的知识模块。
```
改为：
```
共富参谋是一套面向中国一线劳动者的职业判断知识体系。它把行业前景、创业可行性、成长规划、协作方法、趋势前瞻，蒸馏成一个可调用的技能 gongfu-skill（统一入口），内部按意图路由到 6 类能力。
```
把 line 21 标题与 line 25-31 表整体替换为：
```markdown
## 一个技能，六类能力

对外只有一个技能 `gongfu-skill`。用户用大白话描述处境，引擎在内部路由到下面六类能力；每类能力的输出模板见 `skills/gongfu-skill/references/<能力>.md`。

| 内部能力（route_to） | 何时触发 | 输出模板 |
|---|---|---|
| problem-diagnosis | 面临困境/迷茫——矛盾分析、持久战诊断主要矛盾 | skills/gongfu-skill/references/problem-diagnosis.md |
| industry-scan | 想了解行业前景——16 集群信号 + 5 大地域校准 | skills/gongfu-skill/references/industry-scan.md |
| startup-feasibility | 考虑创业——4 条零成本路径 + 止损红线 | skills/gongfu-skill/references/startup-feasibility.md |
| growth-planner | 想规划成长——4 种画像成长地图 | skills/gongfu-skill/references/growth-planner.md |
| collaboration-match | 找人合作——5 种协作形态 + 分钱规则 | skills/gongfu-skill/references/collaboration-match.md |
| opportunity-radar | 看未来趋势——5-10 年前瞻 + 十大确定性增量 | skills/gongfu-skill/references/opportunity-radar.md |
```
把 line 67 示例：
```
请读取 skills/industry-scan/SKILL.md，然后帮我分析制造业产线工人的行业前景
```
改为：
```
请读取 skills/gongfu-skill/SKILL.md（行业判断模板见 references/industry-scan.md），然后帮我分析制造业产线工人的行业前景
```

- [ ] **Step 3: `skills/README.md` —— 7 skill 体系 → 单一入口 + references**

把 line 9 标题 `## 7 个 skill（环环相扣的判断体系）` 与其下表（line 13-19）替换为：
```markdown
## 一个入口技能 + 六类内部能力

对外只有一个技能 `gongfu-skill/`（前门：意图识别 + 信息提取 + 路由 + 情绪优先）。原先环环相扣的 6 类判断能力已下沉为 `gongfu-skill/references/` 内部参考，由引擎 `route_to` 调度：

| 内部能力（references/<能力>.md） | 回答的问题 | 知识来源 |
|---|---|---|
| `problem-diagnosis` | 我这个处境的主要矛盾是什么 | methodology 毛泽东战略思维工具箱 |
| `industry-scan` | 我这个行业在我这个地方行不行 | worker_guidance 16 集群 + regional 五大区域 |
| `startup-feasibility` | 我该不该创业、创什么、怎么起步 | entrepreneurship 四条路径 + 诚实劝退 |
| `growth-planner` | 我该怎么一步步成长 | growth_path 四种画像 + 学习地图 |
| `collaboration-match` | 我该找什么合作、怎么分钱 | collaboration 五种形态 + 信任分配 |
| `opportunity-radar` | 未来 5—10 年机会在哪 | perspective 六大前瞻 + new_value 十大增量 |
```
把 line 25 里 `（7 个 \`SKILL.md\` + \`data/\` + 设计规范）` 改为 `（1 个前门 \`SKILL.md\` + \`references/\` 6 能力 + \`data/\` + 设计规范）`。
把 line 27 `7 个 skill 封装成一个 Hermes 插件……` 改为 `这一个技能封装成一个 Hermes 插件……`。
把 line 43-45 生成树里：
```
├── router.py            # 路由逻辑（situation-triage 的代码版）
└── skills/              # ⚙生成：内嵌 7 个 SKILL.md（由 scripts/build_packs.py 生成，gitignore）
    ├── situation-triage/SKILL.md
```
改为：
```
├── router.py            # 路由逻辑（前门分诊的代码版）
└── skills/              # ⚙生成：内嵌 gongfu-skill（含 references/，由 scripts/build_packs.py 生成，gitignore）
    └── gongfu-skill/SKILL.md + references/
```
line 69-75 的流程示例里把 `situation-triage 路由` 改为 `前门分诊路由`（两处），其余 `problem-diagnosis`/`industry-scan` 等作为能力名保留不动。

- [ ] **Step 4: 仓库 `CLAUDE.md` —— 架构段同步**

在 `CLAUDE.md` 的 "Single source + generated packs" 表的 SOURCE 行
```
| **`skills/<name>/SKILL.md` + `skills/data/*.yaml`** | **SOURCE — the only place you edit.** The running engine reads `skills/data/` directly. |
```
之后补一句（紧跟该行下方新增一行说明，不破坏表结构——放在表格之后的段落里）：在该表格下方已有的"Rules:"列表前，插入一段：
```markdown
> 自 v1.7.0：对外只有**一个**技能 `skills/gongfu-skill/`（唯一入口）。原 6 个能力 skill 已下沉为 `skills/gongfu-skill/references/<能力>.md` 内部参考——不再单独注册/上架，但仍是 `route_to` 标签与 `data/*.yaml` 的一一对应。`build_packs.py` 会把 `references/` 一并复制进三处派生包。
```
并把 "Engine internals" 里 `router.py` 描述中 "route_to skills" 一语保持不变（仍准确）。

- [ ] **Step 5: `skills/00-skill设计规范.md` —— 补一句 references 说明**

在文件靠前的"性质"段（line 4 一带）之后，新增一段：
```markdown
> 自 v1.7.0：对外只有一个技能 `gongfu-skill`（统一入口）。本规范中作为范例引用的 `industry-scan` / `startup-feasibility` / `problem-diagnosis` 等，现已下沉为 `skills/gongfu-skill/references/<能力>.md` 内部能力参考——它们不再单独作为技能上架，但其 `SKILL.md` 结构（含测试用例）仍按本规范维护，供 doc-based 验证与输出模板使用。
```

- [ ] **Step 6: 核对并提交**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -rnE "7 个知识模块|7 个 skill|7 个 SKILL|蒸馏成 7 个" skills/README.md agents/AGENTS.md claude-skills/CLAUDE.md || echo "NO STALE COUNTS"
```
Expected: `NO STALE COUNTS`（用 `grep -E`）
```bash
git add skills/README.md agents/AGENTS.md claude-skills/CLAUDE.md CLAUDE.md "skills/00-skill设计规范.md"
git commit -q -m "docs: 各包/规范文档同步为单一 gongfu-skill 入口 + references 能力

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: 版本升 v1.7.0 + CHANGELOG

**Files:**
- Modify: `pyproject.toml`、`api_server/server.py`、`engine/plugin.yaml`、`CHANGELOG.md`
- （`README.md` 顶部版本行已在 Task 7 Step 5 改过）

- [ ] **Step 1: 三处版本号 1.6.0 → 1.7.0**

`pyproject.toml`：把 `version = "1.6.0"` 改为 `version = "1.7.0"`。
`api_server/server.py`：把 `"version": "1.6.0",` 改为 `"version": "1.7.0",`。
`engine/plugin.yaml`：把 `version: 1.6.0` 改为 `version: 1.7.0`。

- [ ] **Step 2: CHANGELOG 新增条目**

在 `CHANGELOG.md` 顶部 `[未发布]` 段之后（或紧接最新版本之前）插入：
```markdown
## [1.7.0] - 2026-06-27

### Changed
- **对外技能统一为单一入口 `gongfu-skill`。** 原 `situation-triage` 改名为 `gongfu-skill` 作为唯一对外技能；原 6 个能力 skill（industry-scan / startup-feasibility / growth-planner / collaboration-match / opportunity-radar / problem-diagnosis）下沉为 `skills/gongfu-skill/references/<能力>.md` 内部参考，不再单独上架。用户在 Hermes / Claude Code / ZCode 中只看到、只键入一个名字，agent 显示的"当前技能"也只剩 `gongfu-skill`。
- **Hermes 触发词 `/gongfu` → `/gongfu-skill`**；toolset `gongfu` → `gongfu-skill`（插件名、toolset、技能名三者对齐）。
- `scripts/build_packs.py` 现会把每个 skill 的 `references/` 子目录一并复制进三处派生包。

### Unchanged（兼容性）
- MCP 工具名 `gongfu_consult`、HTTP `POST /consult`、引擎路由逻辑与 `route_to` 取值、`skills/data/*.yaml` 内容与文件名**均保持不变**——现有 MCP / Coze / Dify / API 接入无需改动。
```
若 `[未发布]` 段有内容，保留；若为空，维持空。

- [ ] **Step 3: 校验版本一致**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -rn "1.7.0" pyproject.toml api_server/server.py engine/plugin.yaml README.md | sort
grep -c "1.6.0" pyproject.toml api_server/server.py engine/plugin.yaml || true
```
Expected: 四个文件各出现 `1.7.0`；`pyproject.toml`/`api_server/server.py`/`engine/plugin.yaml` 里不再有 `1.6.0`（CHANGELOG 里保留历史 1.6.0 属正常）。

- [ ] **Step 4: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add pyproject.toml api_server/server.py engine/plugin.yaml CHANGELOG.md
git commit -q -m "chore: 升版本 v1.7.0 + CHANGELOG（技能入口统一为单一 gongfu-skill）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: 最终验收扫描

**Files:** 无改动（只读校验）。如发现遗漏，回到对应任务修正后再提交。

- [ ] **Step 1: 全仓搜残留的旧触发词/旧"7 技能"表述（排除 references 内容、CHANGELOG 历史、设计文档历史范例）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
echo "=== /gongfu （非 /gongfu-skill）残留 ==="
grep -rn "/gongfu" README.md skills/README.md agents/AGENTS.md claude-skills/CLAUDE.md | grep -v "/gongfu-skill" | grep -v "/gongfu-skill.git" || echo OK
echo "=== \$industry-scan 调用残留 ==="
grep -rn '\$industry-scan' README.md agents/*.md claude-skills/*.md || echo OK
echo "=== '7 个技能/7 个 skill/蒸馏成 7 个' 残留 ==="
grep -rnE "7 个知识模块|7 个 skill|蒸馏成 7 个|7 个 SKILL" README.md skills/README.md agents/AGENTS.md claude-skills/CLAUDE.md || echo OK
```
Expected: 三组都打印 `OK`。（均用基础匹配或 `grep -E`，不用 BSD 不支持的 `\|`/`\b`。注意 README 里 `install.sh`/clone 路径含 `gongfu-skill` 不算残留，已通过 `grep -v` 滤除；如仍有 `/gongfu`+空格 的裸触发词命中需修正。）

- [ ] **Step 2: 确认源树形态**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
test -d skills/gongfu-skill/references && [ "$(ls skills/gongfu-skill/references | wc -l | tr -d ' ')" = "6" ] && echo "SRC OK" || echo "SRC BAD"
test ! -d skills/situation-triage && echo "NO OLD TRIAGE" || echo "OLD TRIAGE STILL THERE"
```
Expected: `SRC OK` 和 `NO OLD TRIAGE`。

- [ ] **Step 3: 重建派生包并复跑注册+特征化回归（端到端）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python scripts/build_packs.py
.venv/bin/python - <<'PY'
from pathlib import Path
reg = sorted(c.name for c in Path("engine/skills").iterdir() if c.is_dir() and (c/"SKILL.md").exists())
assert reg == ["gongfu-skill"], reg
for base in ["engine/skills","claude-skills/skills","agents/zcode-skills"]:
    refs = Path(base)/"gongfu-skill"/"references"
    assert refs.is_dir() and len(list(refs.glob("*.md"))) == 6, (base, refs)
print("PACKS+REGISTRATION OK")
PY
.venv/bin/python /private/tmp/claude-501/-Users-housebigger-Documents-01-work-playground-hermes-gongfu-skill/ab3afe89-5a7f-4e05-835d-4cdbc821b0b4/scratchpad/regress_unify.py
```
Expected: `PACKS+REGISTRATION OK` 然后 `REGRESSION ALL PASS`。

- [ ] **Step 4: git 状态干净**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git status --porcelain
```
Expected: 空输出（派生包 gitignore，源改动已全部提交）。若有未提交改动，检查归属并补提交或报告。

---

## 验收标准（全绿即完成）

1. `skills/` 顶层只有 `gongfu-skill/` + `data/` + 两个说明 md；`gongfu-skill/references/` 含 6 个能力文档。
2. `engine/__init__.py`：`toolset="gongfu-skill"`、`name="gongfu_consult"`（工具名不变）。
3. `build_packs.py` 重建后，三处派生包各自只含 `gongfu-skill`（含完整 `references/`）。
4. 特征化回归（5 个用例）在改造后仍 `REGRESSION ALL PASS`——证明引擎行为零变化。
5. 文档无 `/gongfu`（裸）、`$industry-scan`、"7 个技能/skill" 等残留；README 顶部与三处版本号均 v1.7.0。
6. `git status` 干净。

## 装后实测（交付给用户，非本计划自动步骤）

在 Hermes 安装本分支后人工确认（仓库环境无法验证 Hermes 解析/显示）：
- `/gongfu-skill <一句话情况>` 能触发。
- 自然语言描述能自动触发（description 已拓宽）。
- agent 思考过程显示的当前技能为 `gongfu-skill`，无 `situation-triage` 等旧名。
