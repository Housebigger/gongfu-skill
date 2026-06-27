# 设计：把对外技能入口统一为 `gongfu-skill`（单一前门）

- **日期**：2026-06-27
- **类型**：engine / 接口 / 分发结构变更 → 需升版（目标 **v1.7.0**）
- **状态**：已通过 brainstorm 评审，待写 plan

## 1. 背景与问题

用户希望：在 Hermes 或其他 agent 里**显式调用本插件时只键入一个标记名 `/gongfu-skill`**，且 agent 思考过程中显示的"当前调用的技能"也统一为这一个名字。

### 现状盘点（碎片化——这正是要修的）

| 维度 | 现在的名字 | 来源 |
|---|---|---|
| 插件名 | `gongfu-skill` | `engine/plugin.yaml` |
| 工具名 / toolset | `gongfu_consult` / `gongfu` | `engine/__init__.py` `register_tool(...)` |
| Hermes 文档里的手动触发 | `/gongfu` | `README.md`（唯一写明的斜杠触发，对应 toolset `gongfu`） |
| 被注册的 skill | `situation-triage`、`industry-scan`、`opportunity-radar`、`startup-feasibility`、`growth-planner`、`collaboration-match`、`problem-diagnosis`（7 个） | `engine/__init__.py` 用目录名逐个 `register_skill(child.name, ...)` |
| ZCode 包 | `$industry-scan` 等（按单技能名，`$` 前缀） | `README.md` |
| Claude Code 包 | `/situation-triage` 等（按目录名） | 包自动发现 |
| MCP / HTTP API | 工具 `gongfu_consult` / `POST /consult` | `mcp_server/server.py`、`api_server/server.py` |

根因：这 6 个能力被当成**独立技能注册**，所以"当前调用的技能"会显示 7 个不同名字；而 `situation-triage` 是路由/接待层，本就不是与其余 6 个并列的能力。

## 2. 决策记录（brainstorm 三问）

1. **统一范围 = 单一前门**：对外只暴露一个技能 `gongfu-skill` 作为唯一入口；内部仍按现有逻辑路由到 6 个能力；其余 6 个不再作为技能名出现。
2. **能力保留 = 转为内置参考**：6 个能力文档（含输出模板/测试用例）移入 `skills/gongfu-skill/references/`，前门技能按引擎返回的 `route_to` 指向对应参考取输出模板。**零知识损失**。
3. **工具/接口 = 保持不变**：MCP 工具名 `gongfu_consult`、HTTP `POST /consult` 是集成契约，**不改名**（工具是函数，不是技能名；改名会破坏现有 Coze/Dify/MCP 接入）。

## 3. 目标终态

不管在哪个 agent，用户只看到、只键入一个名字 `gongfu-skill`，agent 显示的"当前技能"也只有这一个。原 7 个技能的能力一个不丢。

### 各 shell 入口对照

| Shell | 改前 | 改后 |
|---|---|---|
| Hermes 手动触发 | `/gongfu` | `/gongfu-skill` |
| Hermes 显示的技能 | `situation-triage` / 6 个能力名 | **仅** `gongfu-skill` |
| Claude Code 包 | `/situation-triage` …（7 个） | `/gongfu-skill`（1 个） |
| ZCode 包 | `$industry-scan` …（7 个） | `$gongfu-skill`（1 个） |
| MCP / HTTP API | 工具 `gongfu_consult` / `POST /consult` | **不变** |

## 4. 架构改动：技能层 7 → 1，能力下沉为内置参考

```
skills/
  gongfu-skill/                ← 由 situation-triage 改名而来，唯一对外技能（前门）
    SKILL.md                   ← name: gongfu-skill；描述拓宽覆盖全场景；
                                  新增"能力分派"段：按 gongfu_consult 返回的 route_to
                                  读取 references/<能力>.md 的输出模板
    references/                 ← 原 6 个能力 SKILL.md 移入此处（内部参考，不再是技能）
      industry-scan.md
      startup-feasibility.md
      growth-planner.md
      collaboration-match.md
      opportunity-radar.md
      problem-diagnosis.md
  data/                        ← 不动（引擎运行时仍直接读这里）
```

### 关键不变量（折叠技能层不触碰引擎路由逻辑）

引擎 `route_to` 的取值（`industry-scan`、`startup-feasibility`、`growth-planner`、`collaboration-match`、`opportunity-radar`、`problem-diagnosis`）只是**内部路由标签**，被 `engine/tools.py` 消费。这些标签与三处文件名一一对应：

- 路由标签（`tools.py` 的 `_handle_analyze` / `_build_execution_guide` 分支）
- `skills/data/*.yaml` 数据文件
- 折叠后 `skills/gongfu-skill/references/<name>.md`

三者保持 1:1 映射，因此下沉能力**不需要改任何引擎路由分支**，知识与数据零损失。引擎运行时返回的 `execution_guide` 提供每能力的**语气/步骤**指引；`references/<name>.md` 提供该能力的**详细输出模板**——前门 SKILL.md 把两者衔接起来。

### references 必须随技能进入全部三个派生包

前门 SKILL.md 会指示 agent"按 route_to 读取 `references/<name>.md`"，因此这些参考文件必须与 SKILL.md **同目录物理存在于每个 shell 的包里**：Hermes（`engine/skills/gongfu-skill/`）、Claude Code（`claude-skills/skills/gongfu-skill/`）、ZCode（`agents/zcode-skills/gongfu-skill/`）。这要求改造 `build_packs.py`（见 §5）——它当前**只复制单个 `SKILL.md` 文件**，不复制子目录。

## 5. 逐文件改动清单

### 引擎 / 注册（触发与显示的根源）
- `engine/__init__.py`
  - `register_tool(name="gongfu_consult", toolset="gongfu" → "gongfu-skill", ...)`（工具名不变，仅 toolset 改名，使 Hermes `/gongfu-skill` 成立）。
  - 技能注册循环：重构后 `skills/` 下只剩 `gongfu-skill` 一个目录满足 `is_dir() and SKILL.md exists`（`references/` 在其内部、`data/` 无 SKILL.md，均不会被当技能）。确认/收紧为只注册该前门技能。
  - 首轮 `pre_llm_call` hook 提示语措辞对齐（仍指向 `gongfu_consult` 工具即可）。
- `engine/plugin.yaml`：版本号 → 1.7.0；`provides_tools` 不变。

### 源（单一真相）
- `skills/situation-triage/` → 改名为 `skills/gongfu-skill/`：
  - SKILL.md `name: situation-triage → gongfu-skill`；版本号升（如 3.0.0 → 4.0.0）。
  - description 拓宽：从"路由/接待层"拓为覆盖全场景的统一入口（行业判断/创业评估/职业困惑/成长规划/协作/趋势），确保 agent 在任何劳动者咨询场景都选它。
  - 新增"能力分派"段：根据 `gongfu_consult` 返回的 `route_to`，读取 `references/<能力>.md` 的输出模板。
  - 把"不要用于……直接用 industry-scan / startup-feasibility / opportunity-radar"等措辞改为"直接描述即可，引擎会路由到对应能力"（不再暗示存在可独立调用的子技能）。
  - 标题由"情况分诊 skill（路由层）"改为体现"统一入口"。
- 6 个能力 `SKILL.md` → `skills/gongfu-skill/references/<name>.md`（保留其输出模板与测试用例），删除原 6 个空目录。

### 生成 / 分发
- `scripts/build_packs.py`：**需实际改造**。当前每个 skill 只复制单个 `SKILL.md`（`shutil.copy2(d/"SKILL.md", ...)`，line 61），不复制子目录。改为：每个 skill 复制 `SKILL.md` **加上 `references/` 子目录**到全部三个目标（含 `engine/skills`，该目标当前 `data=None`、无任何子目录拷贝）。仍走标准库、跨平台（如对 `references/` 用 `shutil.copytree`）。旧 6 个技能目录因脚本"先 `rmtree` 后重建"会自然清除（line 56-57），无需额外处理。改后手动跑一次 `python scripts/build_packs.py`。

### 文档
- `README.md`：`/gongfu` → `/gongfu-skill`；ZCode 示例 `$industry-scan …` → `$gongfu-skill …`；"7 个技能"叙述改为"1 个入口技能 + 6 个内部能力"；顶部当前版本行 → v1.7.0。
- `skills/README.md`：7 技能 → 1 入口技能 + 6 references。
- `agents/AGENTS.md`、`claude-skills/CLAUDE.md`：技能列表/调用说明同步为单一 `gongfu-skill`。
- 仓库 `CLAUDE.md`：架构段对"7 skills""skills/<name>/SKILL.md"的描述同步为单一前门 + references 结构。
- `skills/00-skill设计规范.md`：补一句说明 `references/` 是下沉的内部能力文档（非对外技能，不要求作为技能上架，但保留测试用例供 doc-based 验证）。
- `CHANGELOG.md`：新增 `## [1.7.0]` 条目（Changed：技能入口统一为单一 `gongfu-skill`、toolset 改名、6 能力下沉 references；Unchanged/Compat：`gongfu_consult` 工具与 `/consult` 接口不变）。

### 版本（三处同步 + README 版本行 + CHANGELOG）
- `pyproject.toml`、`api_server/server.py`（`/` index `version`）、`engine/plugin.yaml` → **1.7.0**。

## 6. 验证计划

### 6.1 引擎回归（合成包脚本，无 pytest）
用 `gongfu_engine` 合成包 bootstrap（与现有 servers 一致），确认折叠后引擎行为不变：
- `gongfu_consult({situation, mode:"intake"})` 对代表性输入仍返回正确 `route_to`（如"光伏运维"→ `["industry-scan"]`、"38岁芯片封测怕被替代想搞副业"→ `["problem-diagnosis","startup-feasibility"]`、危机词 → `type=special,handling=crisis`）。
- `mode:"analyze"` 仍正确注入 `knowledge_context` / `execution_guide` / `tone_instruction` / 地域 / 行业前景 等（与 v1.6.0 行为一致）。
- 目的：证明"技能层折叠"对引擎运行时**零影响**。

### 6.2 注册面验证
- 静态检查 `engine/__init__.py`：注册的技能集合 == `{gongfu-skill}`；toolset == `gongfu-skill`；工具名仍 `gongfu_consult`。
- `python scripts/build_packs.py` 后，确认三处派生包（`engine/skills`、`claude-skills/skills`、`agents/zcode-skills`）各自只含一个 `gongfu-skill` 技能目录，且每个目录内 `SKILL.md` 与 `references/`（6 个文件）完整随行、无旧 6 技能目录残留。

### 6.3 Hermes 实测（环境相关，无法在本仓库环境验证）
**诚实边界**：Hermes 斜杠命令究竟解析技能名 / toolset 名 / 插件名，以及"当前调用的技能"显示哪个字符串，无法从仓库 100% 确证。对策：把**插件名、toolset、技能名三个标识符全部对齐为 `gongfu-skill`**，使 `/gongfu-skill` 在任何解析模型下都成立、显示也都是 `gongfu-skill`。装后在 Hermes 实测一次定论：
- `/gongfu-skill <一句话情况>` 能触发。
- 自然语言描述能自动触发（description 拓宽后）。
- agent 思考显示的当前技能为 `gongfu-skill`，无 `situation-triage` 等旧名残留。

## 7. 风险与缓解

- **R1：折叠后能力输出模板在运行时不再随技能下发** → 已通过"转为内置参考 + 前门按 route_to 指向 references"缓解，知识零损失。
- **R2：Hermes 解析模型不确定** → 三标识符全对齐 + 装后实测（§6.3）。
- **R3：派生包残留旧 6 技能目录** → build_packs 清后重建并核对（§6.2）；旧包为 gitignore，不影响 fresh clone。
- **R4：前门 description 过窄导致 agent 不自动选它** → 拓宽描述覆盖全部 6 类诉求。
- **R5：文档遗漏旧技能名** → 全仓 `grep` 旧 7 名 + `/gongfu`、`$industry-scan` 等收尾核对。

## 8. 不在本次范围（YAGNI）

- 不改 `gongfu_consult` 工具名、不改 `/consult` 接口、不改 MCP server 协议。
- 不改引擎路由逻辑、`route_to` 取值、`data/*.yaml` 内容与文件名。
- 不扩充知识内容（deng/xi 语料、mao-tools.yaml 等仍按既有 roadmap，不在此版）。
