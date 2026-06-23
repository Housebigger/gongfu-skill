# 设计文档：战略库第二核心根源 —— Serenity 产业链分析法

- 日期：2026-06-23
- 状态：已通过设计评审，待落地
- 涉及层：`strategy/`（知识根）+ `skills/data/` + `engine/`（引擎接入）

## 1. 背景与目标

战略库（`strategy/`）此前只有**一个核心根源**：十五五规划（原文在 `strategy/references/`，逐句解读在 `strategy/analysis/`）。本设计为战略库新增**第二核心根源**——投资博主 **Serenity（网名"白毛股神"）的产业链分析方法论**，用来构建"产业投资 / 产业链价值判断"相关的战略体系。

**目标（本轮交付到全闭环）：**

1. 在 `strategy/` 建立第二根源的知识层（原文源料 + 人读提炼），结构镜像第一根源。
2. 把核心方法论蒸馏进 `skills/data/*.yaml`，并接入 `engine/`，让 `gongfu_consult` 在行业判断/趋势前瞻类咨询中真正用上。

## 2. 提炼角度（已与用户确认）

- **方法论 + 案例**，**剥离具体个股 / 仓位 / 买卖点**。
- 价值定位：把 Serenity 的"找产业链卡点"的投资打法，**翻译成一线劳动者可用的"行业判断 / 趋势前瞻 / 创业切入"思想武器**——这是它配得上"共富战略库"的关键，而非一份荐股摘要。
- 诚实边界：Serenity 近期因**跨境"吹票"**（一句话带动 A 股 20cm 涨停，如绿的谐波）被国盛分析师公开批评、被监管层面提示风险；其身份成谜（白发动漫头像，实际运营者身份不明）。本根源**只取其分析框架**，并在专门文件中写明争议与照搬风险。

## 3. 方法论内核（抓取自公开二手深度梳理，剥离个股后）

| 框架 | Serenity 原意 |
|---|---|
| **瓶颈理论** | 不买 AI 龙头，找产业链里**最难替代、最易断供**的卡点环节（类比：全球约 20% 石油经霍尔木兹海峡） |
| **紫苏叶理论** | 找最稀缺、不可或缺的上游节点（寿司店没紫苏叶就停摆，断供则全系统瘫痪） |
| **约束条件导向** | 从**物理硬约束**倒推（核心问法："数据中心扩到多大，铜线就撑不住？"） |
| **逐层下钻五步** | 需求 → 传输方式 → 物理极限 → 替代方案 → 具体节点，一路追溯到上游 |
| **对抗性验证** | 判断先喂多个 AI 模型找漏洞 / 找替代威胁 / 找估值偏差，证伪后才公开 |

**三大个人优势（背景，不是方法）**：深度技术背景（前 AI 研究科学家 + RISC-V 基金会成员 + 硅光子工程师）、衬底级文献研究能力、抢在机构资金前布局。

**代表案例 —— AI 算力光通信 / 硅光子供应链七层：**

1. 原材料（镓、铟、砷）
2. pBN 坩埚与晶体生长设备（单一供应商瓶颈）
3. InP（磷化铟）衬底加工 ——"皇冠上的明珠"，供给最紧
4. 连续波激光器 / CPO 光源 —— 2027–2028 拐点
5. 光模块组装（市场易见环节）
6. 测试与验证（早期机会）
7. 光缆与光纤（传输基础层）

另一案例：机器人产业链瓶颈（谐波减速器等）。

## 4. 知识层结构（方案 A：镜像十五五根源）

### 4.1 原文源料 —— `strategy/references/serenity/`

`references/` 的定位是"原文源料，不加工"。Serenity 最硬的内容在 X 付费订阅墙后（3.7 万付费），X 本身也难抓取，因此本目录**以公开的二手深度梳理为主**，每篇诚实标注来源 URL + 日期，定位为"可获得的最佳公开源料"，不假装抓到了付费原文。

```
strategy/references/serenity/
├── README.md            # 是什么 + 诚实声明（二手为主，付费原文未抓取）
├── 00-信源清单.md       # 每条带 URL + 日期 + 一句话提要，可追溯
└── NN-<来源>.md         # 每篇一档的来源整理（鉅亨/Foresight/雪球/知乎/公开长推…）
```

候选信源（落地时正式整理）：

- 知乎：白毛股神 Serenity：寻找产业链中的瓶颈点 — https://zhuanlan.zhihu.com/p/2048164170990871994
- 知乎问题：如何看待最近（2026 年）推特爆火的散户 Serenity — https://www.zhihu.com/question/2043660509396865080
- 雪球：拆解「推特第一美股股神」Serenity — https://xueqiu.com/9636250874/390740400
- 鉅亨 / 链文：看懂「AI 供應鏈教父」的投資邏輯 — https://news.cnyes.com/news/id/6476861
- Foresight News：这个叫 Serenity 的 AI 新股神，是怎么在一年内赚到 45 倍的 — https://foresightnews.pro/article/detail/97459
- X 长推汇总（0xKevin）：她所有推文 + 方法论全解析 — https://x.com/0xKevin00/status/2059886422249680924
- 争议侧（用于"边界与诚实"文件）：财联社《大 V"白毛股神"跨境吹票》https://www.cls.cn/detail/2394549 ；新浪财经《国盛分析师赵丕业怒怼"白毛股神"》https://finance.sina.com.cn/roll/2026-06-09/doc-iniauvas6471198.shtml

### 4.2 提炼子层 —— `strategy/industry_investment/`（新增第 10 个子层）

镜像 `analysis/` 的编号约定（`00` 恒为方法论框架，其后顺序展开），每层自带 README。

```
strategy/industry_investment/
├── README.md
├── 00-方法论框架.md                        # 五大框架 + 劳动者视角翻译（核心）
├── 01-瓶颈理论与紫苏叶理论-卡点判断法.md
├── 02-产业链下钻五步法-从大趋势到价值节点.md
├── 03-案例-AI算力光通信链七层拆解.md       # 教"怎么读一条链"，不含个股
└── 04-边界与诚实-照搬风险·吹票争议·与共富的区别.md
```

### 4.3 劳动者视角翻译（子层的灵魂，主要写进 `00`）

| Serenity 的用法 | 共富·劳动者版 |
|---|---|
| 找供应链卡点买入 | **行业判断**：我的岗位 / 行业在产业链哪一层？是"卡点"（难替代、有议价权、抗 AI）还是"易替代"（谁都能干、产能过剩）？ |
| 小而垄断的紫苏叶节点 | **创业切入**：别冲龙头红海，找"需求刚性 + 供给稀缺 + 难复制"的小卡点 |
| 从物理硬约束倒推 | **趋势前瞻**：不追"什么火"，问"什么是绕不开的硬约束"，硬约束处确定性最高 |
| 对抗性证伪 | 呼应方法论库的**实事求是 / 矛盾分析**：任何判断先找反例再信 |

## 5. 引擎接入（全闭环）

接入点已勘明：每个 `skills/data/*.yaml` 在 `engine/router.py` 模块级加载 → `get_*_for_cluster()` 取卡 → `engine/tools.py:_handle_analyze` 按 `route_to` 注入 `knowledge_context`。新方法论照此套路：

1. **新数据文件** `skills/data/industrial-chain-tools.yaml`：产业链卡点分析工具卡，schema 照 `methodology-tools.yaml` / `marxism-tools.yaml`（`tools` 映射，每张卡含 `principle` / `one_liner` / 劳动者用法 / 适配的 cluster）。工具卡至少覆盖：瓶颈定位、卡点四问、紫苏叶切入、约束倒推、对抗性验证。
2. **`engine/router.py`**：模块级 `_CHAIN = _load_yaml("industrial-chain-tools.yaml")`；新增 `get_chain_tools_for_cluster(cluster)`，仿 `get_marxism_tools_for_cluster`。（无独立启发语料库，故不加 inspiration 加载器；蒸馏只进 YAML。）
3. **`engine/tools.py:_handle_analyze`**：在 `route_to` 命中 `industry-scan` 或 `opportunity-radar`、且 `info.get("cluster")` 存在时，注入 `knowledge_context["chain_tools"]`（仿马 / 邓 / 习工具块）。
4. **SKILL.md**：`industry-scan`、`opportunity-radar` 两个 skill 的来源映射（source mapping / `source_layers`）补上新子层 `strategy/industry_investment/` 与数据文件 → 跑 `python scripts/build_packs.py` 重新生成派生包。
5. **文档**：`strategy/README.md`（9→10 子层 + 第二核心根源说明）、`strategy/references/README.md`（补 `serenity/`）、`CHANGELOG.md` 的 `[未发布]`。

## 6. 验证方式（本仓库无自动化测试，按 SKILL 规范做 doc-based + 直跑引擎）

1. **YAML 可加载**：`python -c "import yaml; yaml.safe_load(open('skills/data/industrial-chain-tools.yaml'))"`。
2. **引擎端到端**：用 `.venv/bin/python`（3.12，带 pyyaml）跑 `gongfu_consult` analyze 模式，传一个行业判断类 situation（带可识别 cluster，如"半导体/光模块/机器人"），断言输出 JSON 的 `knowledge_context` 含 `chain_tools`。
3. **派生包一致**：跑 `build_packs.py` 后确认三处派生位置字节一致、gitignore 未漏。
4. **SKILL 测试用例**：在改动的 SKILL.md 的 Test Cases 段补一条产业链卡点判断的用例。

## 7. 版本影响

本轮**改动了 `engine/router.py` + `engine/tools.py`（新增加载器与注入）= 引擎变更**，按 `CLAUDE.md` 约定属于应升版本的范畴（非纯知识内容增补）。建议在落地完成、收尾时评估打 **`1.3.0`**（三处版本号同步 + CHANGELOG 段 + README 版本行）。本设计阶段先把内容累计进 `[未发布]`，发版决策放到实现收尾。

## 8. 非目标（YAGNI）

- 不做独立启发语料库（inspiration 目录 + 评分检索）——四思想体系才有这个量级的原料，Serenity 单一来源不需要。
- 不抓取 / 转述付费订阅原文。
- 不输出任何个股、代码、仓位或买卖点。
- 不改动除 `industry-scan` / `opportunity-radar` 外的其他 skill 路由。

## 9. 待确认 / 风险

- 二手信源可抓取性：知乎 `zhuanlan` 抓取曾返回 403；落地时以可抓取的源（鉅亨 / Foresight 已验证可抓）为主，抓不到的只在信源清单登记 URL，不伪造内容。
- 个股案例名：按"方法论 + 案例"角度，案例保留**产业链环节名**（InP 衬底、CPO 光源、谐波减速器），不保留股票代码 / 涨幅作为操作信号。
