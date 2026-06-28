# 更新日志 / Changelog

本文件是共富参谋（gongfu-skill）面向使用者的**版本升级说明**，按 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 组织，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

**版本号管理约定**

- 版本号统一维护在三处，发布时一起改：`pyproject.toml`、`api_server/server.py`（`/` 接口的 `version`）、`engine/plugin.yaml`。
- 版本号跟踪**引擎 / 接口 / 分发结构**的变化。纯知识内容的增补（新增思想转译、集群框架等）**不单独升版本**，在「未发布」段落累计，随下次发布一并记录。
- 每次发版：更新三处版本号 → 在本文件顶部加一段 → 同步 `README.md` 顶部的版本行。

---

## [未发布]

### Added
- **安装脚本版本检查 + `--update`**（`install.sh` / `install.ps1`）：默认运行对已安装系统只读——打印「当前版本 ｜ 最新版本」并在有新版本时提示；更新需显式 `--update`（远程 `curl … | bash -s -- --update` / `… -Update`）。远程版本抓取 best-effort + 超时降级。引擎/接口/版本号不变。
- **战略库 `semiconductor_outlook/` 专题新增「AI 硬件产业链」系列（知识层）**：`05` 技术架构视角 9 节点全景测绘、`06` 投资产业视角（景气周期位置 / 价值分配 / 国产替代兑现度 / 估值陷阱）、`07` 上中下游关系总图（Mermaid + ASCII；第六节叠加「三棵树」近端下一棒演化视图：根=电力·硬约束/干=硅光·内生延续/枝=机器人·应用外延，接 `09`）、`08` 景气时序图（景气周期位置 × 催化时间轴的时间维度图）。均经多源检索 + 对抗式核查、**零证券代码、非投资建议**，落点 A 集群（先进制造与硬科技）劳动者岗位/技能方向。引擎/接口/版本号不变。
- **AI 硬件产业链卡位方向蒸馏进引擎**（`skills/data/industry-forecast-tools.yaml` 的 `A-先进制造与硬科技` 卡）：在 `positioning/watch_indicators/one_liner/source` 注入 AI 硬件链的劳动者卡位「方向骨架」——先进封装/液冷基础设施/PCB-CCL-MLCC 高端产线最实、向上游材料与「高良率+认证」迁移、组装端薄利可替代、「送样≠量产」，并指向详版 `semiconductor_outlook/05-08`。引擎在「行业判断/趋势前瞻」且识别 A 集群时即注入（`get_industry_forecast_for_cluster`，已有接线）。仅慢变量/方向骨架、不含点位/年份/个股，引擎逻辑/接口/版本号不变。
- **AI 硬件近端下一棒裁决（知识层 + 蒸馏进引擎）**：新增 `semiconductor_outlook/09-AI硬件近端下一棒裁决.md`（电力/能源 vs 机器人 vs 硅光对照裁决，"三种不同性质的下一棒"非单选题）；并把"电力/能源"骨架蒸馏进 `C-绿色能源全链` 卡、"机器人/具身"骨架蒸馏进 `H-新兴未来产业` 卡（硅光已含于 `A` 卡）。零代码、慢变量/方向骨架、引擎逻辑/接口/版本号不变。

## [1.7.0] - 2026-06-27

### Changed
- **对外技能统一为单一入口 `gongfu-skill`。** 原 `situation-triage` 改名为 `gongfu-skill` 作为唯一对外技能；原 6 个能力 skill（industry-scan / startup-feasibility / growth-planner / collaboration-match / opportunity-radar / problem-diagnosis）下沉为 `skills/gongfu-skill/references/<能力>.md` 内部参考，不再单独上架。用户在 Hermes / Claude Code / ZCode 中只看到、只键入一个名字，agent 显示的"当前技能"也只剩 `gongfu-skill`。
- **Hermes 触发词 `/gongfu` → `/gongfu-skill`**；toolset `gongfu` → `gongfu-skill`（插件名、toolset、技能名三者对齐）。
- `scripts/build_packs.py` 现会把每个 skill 的 `references/` 子目录一并复制进三处派生包。

### 兼容性（未变更）
- MCP 工具名 `gongfu_consult`、HTTP `POST /consult`、引擎路由逻辑与 `route_to` 取值、`skills/data/*.yaml` 内容与文件名**均保持不变**——现有 MCP / Coze / Dify / API 接入无需改动。

## [1.6.0] - 2026-06-27

### 修复 Fixed（引擎逻辑·源自全仓审计）
- **analyze 模式短路 need_more_info**：信息过少时不再产出空壳"假分析"，回退为温柔请补基本信息。
- **年龄抽取修正**：负向前瞻 + 范围校验（14–80），消除"120岁→20""100岁→age=0"的静默错误。
- **危机词收紧并扩真信号覆盖**：删歧义词"无所谓了"、"了结"→"了结自己/了结生命"，新增"死了算了/不如死/生无可恋/轻生/活着真没意思"等明确信号，排除"想死/没意思"等高误判词；降低正常咨询被误判危机，同时不削弱真危机捕获。
- **NIT 清理**：execution_guide 死参数、region_name 去圈号展示、schemas 补特殊返回说明、启发加载器裸 except 收窄、路由优先级注释。

### 新增 Added
- **地域分析接线**：`regional-matrix.yaml` 经新增的 `get_regional_context()` 在行业判断/趋势前瞻且识别出地域时注入 analyze（区域画像 + 该区域机会评分列 + 决策建议），兑现 schemas/SKILL 早已声明的"地域分析"能力。
- **situation-triage/SKILL.md** 补齐规范段（测试用例 + 源文档映射 + 输入/输出/执行规格）。
- **战略库新增「华为韬（τ）定律 → 半导体产业发展逻辑与方向」研究专题（知识层）**（原 [未发布] 累计条目，随本版发布）：原料库 `strategy/references/huawei_tau/` + 提炼/预测 `strategy/semiconductor_outlook/`（00–04），三分陈述 + 情景非预言 + 中立 + 不个股，落点 A 集群劳动者。

## [1.5.0] - 2026-06-26

逐集群行业前景接入引擎（战略库第三根源·09 行业前景推演蒸馏），并把此前累计的两批"逐集群行业前景推演"知识层随本版一并记录。对终端使用者**功能只增不减**：在行业判断 / 趋势前瞻类咨询且识别出产业集群时，多一张该集群"政策→前景"的方向卡片（`industry_forecast`：主驱动议题 / 基调 / 卡位方向 / 观察指标 / 详版指引），给方向不给时间表、不个股、不政治预测。

### 新增 Added

- **引擎接入：逐集群行业前景卡片（evergreen）**。新增 `skills/data/industry-forecast-tools.yaml`（16 集群 evergreen 卡片，**只含**主驱动议题/基调/卡位方向/观察指标名/一句话方向/详版指引，**不含**三情景阈值、带年份统计、待核实项等时效内容——后者留在 `09-行业前景推演/<cluster>.md`）；`engine/router.py` 增 `get_industry_forecast_for_cluster()`；`gongfu_consult` 在行业判断 / 趋势前瞻类咨询且识别出 cluster 时注入 `industry_forecast`，与 `industry`（静态信号）/`chain_tools`（产业链卡点）/`policy_deduction`（通用方法）互补。

- **经济政策专栏新增「逐集群行业前景推演」层（首批 6 集群·知识层）**。把 07/08 宏观议题推演下沉到具体产业集群：原料库扩充行业政策信源 + 六集群锚点政策（`policy_archive/00`、新增 `03`）；新增 `economic_policy/09-行业前景推演/`（方法与边界 `00` + C/K/E/G/A/D 六集群文件），每集群按 06 六要素法给基准/上行/下行三情景，含触发条件、关键假设、可证伪点与劳动者含义，数据带官方来源、先搜后确认。情景为方向研判非预言，不个股、不政治预测。随 v1.5.0 一并记录。
- **经济政策专栏「逐集群行业前景推演」层补齐其余 10 集群（B/F/H/I/J/L/M/N/O/P，知识层）**，至此 16 产业集群全覆盖。原料库续扩十集群行业政策信源 + 锚点（`policy_archive/04`）；`09-行业前景推演/` 新增 10 个集群文件，每集群按 06 六要素法给基准/上行/下行三情景，含触发条件、关键假设、可证伪点与劳动者含义，数据带官方来源、先搜后确认；对偏市场/结构驱动的集群（O/L/J/F）如实交代政策成色，不硬凑政策叙事。情景为方向研判非预言，不个股、不政治预测。随 v1.5.0 一并记录；引擎接入见本版"引擎接入"条目。

## [1.4.0] - 2026-06-25

经济政策追踪专栏（战略库**第三核心根源**）的推演方法接入引擎，并把此前累计的 Phase 1 / Phase 2 知识层随本版一并记录。对终端使用者**功能只增不减**：在行业判断 / 趋势前瞻类咨询中，多一套"政策作用规律 → 情景化推演"的方法框架与诚实边界（`policy_deduction`），给方向不给时间表、不荐资产、不预测政局。

### 新增 Added

- **引擎接入：经济政策推演法（方法框架·evergreen）**。新增 `skills/data/policy-deduction-tools.yaml`（六要素推演法 + 四条推演诚实边界，**不含**时效宏观假设与 07/08 议题结论）；`engine/router.py` 增 `get_policy_deduction_method()`（不依赖集群）；`gongfu_consult` 在趋势前瞻 / 行业判断类咨询时注入 `policy_deduction`，`execution_guide` 同步引导用六要素情景法并守住诚实边界。

- **经济政策追踪专栏 Phase 1 内容补全**。在骨架（方法论框架 + 台账 + 诚实边界）基础上，新增六条政策主线"政策↔真实结果"复盘：`02-政策主线复盘（上）`（供给侧结构性改革·双碳·新质生产力，数据带国家统计局/国家能源局官方来源）与 `03-政策主线复盘（下）`（共同富裕·货币政策转向·财政政策转向，数据带统计局/央行/财政部官方来源）；以及 `04-作用规律总结`（政策时滞规律/六条传导机制对就业收入的影响 + 读政策五条心法）。信源清单同步补入统计局、能源局、央行、政府网等七条真实结果数据源（条目 8—14）。随 v1.4.0 一并记录。
- **经济政策追踪专栏 Phase 2 推演（知识层）**。新增推演方法与外部约束（`06`：六要素情景化推演模板 + 国际形势/国情共用假设 + 诚实边界与定期复盘机制）；新增 6 个关键议题情景化推演：`07`（内需/房地产/财政与地方债）与 `08`（新动能/外需出海/人口劳动力），各议题均给出基准/上行/下行三情景，含触发条件、关键假设、可证伪点与劳动者含义，并调用规律库 04 的规律外推。情景定位为方向研判而非预言，给方向不给时间表。随 v1.4.0 一并记录；引擎接入见本版"引擎接入"条目。

## [1.3.0] - 2026-06-23

战略库新增第二核心根源——Serenity 产业链分析法，并接入引擎。对终端使用者**功能只增不减**：在行业判断 / 趋势前瞻类咨询中，当识别出产业集群时，会多一组"找产业链卡点"的劳动者版分析视角（`chain_tools`）。

### 新增 Added

- **战略库新增第二核心根源：Serenity 产业链分析法**。在十五五规划之外，新增"读懂任意产业链卡点"的微观方法体系：原文源料 `strategy/references/serenity/`、提炼子层 `strategy/industry_investment/`（瓶颈理论/紫苏叶理论/约束倒推/下钻五步/对抗性验证，全部翻译为劳动者版的行业判断与创业切入工具，剥离个股）。
- **引擎接入产业链卡点工具**：新增 `skills/data/industrial-chain-tools.yaml`，`engine/router.py` 增 `get_chain_tools_for_cluster`，`gongfu_consult` 在行业判断/趋势前瞻类咨询且识别出集群时注入 `chain_tools`。

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
