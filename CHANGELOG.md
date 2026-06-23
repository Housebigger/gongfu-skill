# 更新日志 / Changelog

本文件是共富参谋（gongfu-skill）面向使用者的**版本升级说明**，按 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 组织，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

**版本号管理约定**

- 版本号统一维护在三处，发布时一起改：`pyproject.toml`、`api_server/server.py`（`/` 接口的 `version`）、`engine/plugin.yaml`。
- 版本号跟踪**引擎 / 接口 / 分发结构**的变化。纯知识内容的增补（新增思想转译、集群框架等）**不单独升版本**，在「未发布」段落累计，随下次发布一并记录。
- 每次发版：更新三处版本号 → 在本文件顶部加一段 → 同步 `README.md` 顶部的版本行。

---

## [未发布]

### 新增 Added

- **战略库新增第二核心根源：Serenity 产业链分析法**。在十五五规划之外，新增"读懂任意产业链卡点"的微观方法体系：原文源料 `strategy/references/serenity/`、提炼子层 `strategy/industry_investment/`（瓶颈理论/紫苏叶理论/约束倒推/下钻五步/对抗性验证，全部翻译为劳动者版的行业判断与创业切入工具，剥离个股）。
- **引擎接入产业链卡点工具**：新增 `skills/data/industrial-chain-tools.yaml`，`engine/router.py` 增 `get_chain_tools_for_cluster`，`gongfu_consult` 在行业判断/趋势前瞻类咨询且识别出集群时注入 `chain_tools`。

> 说明：本项含引擎改动（新增加载器与注入），发版时建议升至 `1.3.0`（三处版本号同步 + 本段移入正式版本号）。

## [1.2.0] - 2026-06-23

一轮仓库梳理：理顺应用层结构、补齐四思想体系的引擎接入、清理文档。对终端使用者（在 Hermes / Claude / Cursor 等里问共富参谋）**功能只增不减**；对维护者和自建部署者有目录结构变化，见下方升级提示。

### ⚠️ 升级提示

- **引擎目录已从 `skills/gongfu-skill/` 上移到仓库顶层 `engine/`。**
  - **Hermes 插件用户**：拉取新版后旧的符号链接会失效，重新运行一次安装脚本即可重新链接：`./install.sh`（Windows：`.\install.ps1`）。
  - **MCP / HTTP API 自建部署者**：无需改动——`mcp_server` / `api_server` 已指向新路径；按原命令启动即可。
- **派生知识包不再进 git，改为安装时生成。** `claude-skills/`、`agents/zcode-skills/`、`engine/skills/` 现由 `scripts/build_packs.py` 从单一源 `skills/` 生成。刚 `git clone` 的仓库若要直接取用这些包，先运行一次 `python scripts/build_packs.py`（跑任一安装脚本会自动生成）。

### 新增 Added

- **毛泽东思想、习近平思想的启发库接入引擎实时检索**。此前只有马克思主义、邓小平的启发库会按用户处境实时匹配；现在四大思想体系（马 / 毛 / 邓 / 习）的启发库都会被检索，分析输出里新增 `mao_inspiration`、`xi_inspiration`。毛泽东启发库有 1500+ 篇，采用模块级缓存（每个目录仅首次读盘一次），不影响响应速度。
- 新增 `scripts/build_packs.py`：从单一源生成各平台知识包。
- 新增顶层 `strategy/README.md`、`strategy/references/README.md` 与本 `CHANGELOG.md`。

### 变更 Changed

- **引擎 / Hermes 插件从 `skills/gongfu-skill/` 移至顶层 `engine/`**，`skills/` 回归纯知识源（`SKILL.md` + `data/` + 设计规范），职责分明。
- **应用层去重：`skills/` 成为 `SKILL.md` 与 `data/` 的唯一可编辑来源**，其余三处副本改为生成产物（已 gitignore），消除「改一处漏三处」的漂移风险。
- 三处版本号统一为 `1.2.0`（此前 `plugin.yaml` 为 `1.0.0`，其余为 `1.1.0`）。

### 修复 Fixed

- 修正 `engine/router.py` 的数据目录路径在 Hermes 符号链接加载下可能算错的隐患（统一改用 `.resolve()` 基准）。
- 文档清理：`methodology/README` 补上缺失的习近平体系并加各体系完成度表；标注四体系启发库的引擎接入方式；修正脆弱的文件计数；删除 10 个空主题目录与无引用的 `docs/banner.svg`；`claude-skills/CLAUDE.md`、`agents/AGENTS.md` 的知识库清单补齐至 11 个。

## [1.1.0] - 2026-06-20

- **多平台适配**：在 Hermes 插件之外，新增标准 **MCP Server**（适配 Claude Desktop / Cursor / Cline / Windsurf / Continue 等）与 **HTTP API**（适配 Coze / Dify / FastGPT 等），三个壳复用同一套引擎。
- 新增 **Claude Code 静态知识包**（`claude-skills/`）与 **ZCode / Codex** 适配文件（`agents/`）。

## [1.0.0] - 2026-05-06

- 初始版本：确立「全民共享、共同富裕」宗旨与《共富宣言》。
- 方法论库（思想武器）与战略库（现实指引）知识基础，16 集群认知框架，多思想体系的原料库与启发库。
- 共富参谋 Hermes 插件：`gongfu_consult` 工具，借鉴心理咨询原则的双模式（intake / analyze）交互。

> 1.2.0 之前的详细逐次提交历史见 `git log`。
