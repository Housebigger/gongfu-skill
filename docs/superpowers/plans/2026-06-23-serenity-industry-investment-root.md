# 战略库第二核心根源（Serenity 产业链分析法）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在战略库新增第二核心根源——Serenity 产业链分析法，建立 `strategy/` 知识层并接入 `engine/`，让 `gongfu_consult` 在行业判断/趋势前瞻类咨询中真正用上"找产业链卡点"的劳动者版思想武器。

**Architecture:** 镜像第一根源（十五五规划）的组织法：原文源料进 `strategy/references/serenity/`，人读提炼进新子层 `strategy/industry_investment/`；核心方法蒸馏进 `skills/data/industrial-chain-tools.yaml`，由 `engine/router.py` 模块级加载、`get_chain_tools_for_cluster()` 取卡、`engine/tools.py:_handle_analyze` 在命中 `industry-scan`/`opportunity-radar` 且有 cluster 时注入。剥离一切个股/仓位/买卖点，只取分析框架。

**Tech Stack:** Markdown 知识文件、YAML 数据、Python 3.12（pyyaml）、`scripts/build_packs.py` 派生包生成。本仓库无自动化测试套件，验证用"YAML 可加载 + 合成包直跑引擎断言 + doc-based 测试用例"。

**设计依据：** `docs/superpowers/specs/2026-06-23-serenity-industry-investment-root-design.md`

**全局约定（每个任务都遵守）：**
- 中文优先；所有 `json.dumps` 保持 `ensure_ascii=False`（引擎已有）。
- 不输出任何股票代码、涨幅、仓位、买卖点；案例只保留**产业链环节名**（InP 衬底、CPO 光源、谐波减速器）。
- 提交信息中文，结尾加 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`。
- 跑引擎用 `.venv/bin/python`（3.12，带 pyyaml），**不要**用系统 `python3`（3.9 无 pyyaml）。

---

## 已抓取的方法论事实（写内容时直接用，无需再检索）

**五大框架：**
1. **瓶颈理论**：不买 AI 龙头，找产业链里最难替代、最易断供的卡点环节。类比：全球约 20% 石油经霍尔木兹海峡——卡住咽喉的那一段最关键。
2. **紫苏叶理论**：找最稀缺、不可或缺的上游节点。寿司店没了紫苏叶就停摆；AI 产业里某材料/零件一断供，整个系统瘫痪。落点在"小而垄断"。
3. **约束条件导向**：从物理硬约束倒推，不从"什么火"出发。核心问法："数据中心扩到什么规模，铜线就撑不住？"
4. **逐层下钻五步**：需求 → 传输方式 → 物理极限 → 替代方案 → 具体节点，一路追溯到上游；过程中绘制供应链图谱+产能分布、读材料学论文与专利壁垒、追产能扩张与供应商认证周期、盯地缘政治与出口管制。
5. **对抗性验证**：判断先喂多个 AI 模型，专门找漏洞/替代威胁/估值偏差，证伪后才公开。

**代表案例——AI 算力光通信/硅光子供应链七层：**
1. 原材料（镓、铟、砷）→ 2. pBN 坩埚与晶体生长设备（单一供应商瓶颈）→ 3. InP（磷化铟）衬底加工——"皇冠上的明珠"，供给最紧 → 4. 连续波激光器/CPO 光源——2027–2028 拐点 → 5. 光模块组装（市场易见环节）→ 6. 测试与验证（早期机会）→ 7. 光缆与光纤（传输基础层）。
关键术语：InP 衬底="未来 AI 光子时代的石油"；CPO=光电共封装；硅光子；GaAs=砷化镓（替代衬底）；外置连续波激光光源；物理瓶颈。
另一案例：机器人产业链瓶颈（谐波减速器，如绿的谐波）。

**劳动者视角翻译（灵魂）：**
| Serenity 的用法 | 共富·劳动者版 |
|---|---|
| 找供应链卡点买入 | 行业判断：我的岗位/行业在产业链哪一层？是"卡点"（难替代、有议价权、抗 AI）还是"易替代"（谁都能干、产能过剩）？ |
| 小而垄断的紫苏叶节点 | 创业切入：别冲龙头红海，找"需求刚性+供给稀缺+难复制"的小卡点 |
| 从物理硬约束倒推 | 趋势前瞻：不追"什么火"，问"什么是绕不开的硬约束"，硬约束处确定性最高 |
| 对抗性证伪 | 呼应方法论库的实事求是/矛盾分析：任何判断先找反例再信 |

**诚实边界事实（写进 04 文件）：**
- 身份成谜：白发动漫头像，实际运营者身份不明；自称前 AI 研究科学家+RISC-V 基金会成员+硅光子工程师。
- 跨境"吹票"争议：2026-06-05 一句话带动 A 股绿的谐波两日累涨超 30%（含一个 20cm 涨停）；被国盛证券分析师赵丕业公开批评，被监管层面提示"信息倒灌""跨境吹票"风险。
- 共富立场区别：这是"分析框架"不是"操作建议"；个人投资者照搬其个股结论风险极高；共富取其"看产业链卡点"的判断方法服务于劳动者的行业/职业选择，不服务于炒股。

**信源 URL（写 00-信源清单 时用）：**
- 鉅亨/链文《看懂「AI 供應鏈教父」的投資邏輯》https://news.cnyes.com/news/id/6476861 （✅ 可抓取）
- Foresight News《一年赚 45 倍是怎么做到的》https://foresightnews.pro/article/detail/97459 （✅ 可抓取）
- 知乎《白毛股神 Serenity：寻找产业链中的瓶颈点》https://zhuanlan.zhihu.com/p/2048164170990871994 （⚠ 抓取曾 403，仅登记 URL）
- 知乎问题《如何看待最近（2026 年）推特爆火的散户 Serenity》https://www.zhihu.com/question/2043660509396865080
- 雪球《拆解「推特第一美股股神」Serenity》https://xueqiu.com/9636250874/390740400
- X 长推汇总（0xKevin）https://x.com/0xKevin00/status/2059886422249680924
- 东方财富《一篇推文带火机器人龙头"白毛股神"Serenity 究竟是谁》https://wap.eastmoney.com/a/202606073762682238.html
- 争议：财联社《大 V"白毛股神"跨境吹票》https://www.cls.cn/detail/2394549 ；新浪财经《国盛分析师赵丕业怒怼"白毛股神"》https://finance.sina.com.cn/roll/2026-06-09/doc-iniauvas6471198.shtml

---

## File Structure

**Create（知识层）：**
- `strategy/references/serenity/README.md` — 原文源料层入口 + 诚实声明
- `strategy/references/serenity/00-信源清单.md` — 信源 URL+日期+提要
- `strategy/references/serenity/01-鉅亨-AI供应链教父投资逻辑.md` — 鉅亨源整理
- `strategy/references/serenity/02-Foresight-一年45倍方法论.md` — Foresight 源整理
- `strategy/industry_investment/README.md` — 提炼子层入口
- `strategy/industry_investment/00-方法论框架.md` — 五框架 + 劳动者视角翻译
- `strategy/industry_investment/01-瓶颈理论与紫苏叶理论-卡点判断法.md`
- `strategy/industry_investment/02-产业链下钻五步法-从大趋势到价值节点.md`
- `strategy/industry_investment/03-案例-AI算力光通信链七层拆解.md`
- `strategy/industry_investment/04-边界与诚实-照搬风险·吹票争议·与共富的区别.md`

**Create（引擎数据）：**
- `skills/data/industrial-chain-tools.yaml`

**Modify（引擎）：**
- `engine/router.py` — 加 `_CHAIN` 加载 + `get_chain_tools_for_cluster()`
- `engine/tools.py` — `_handle_analyze` 注入 `chain_tools`

**Modify（接口/文档）：**
- `skills/industry-scan/SKILL.md` — 来源映射 + 测试用例
- `skills/opportunity-radar/SKILL.md` — 来源映射 + 测试用例
- `strategy/README.md` — 9→10 子层 + 第二根源说明
- `strategy/references/README.md` — 补 serenity/
- `CHANGELOG.md` — `[未发布]` 段

---

## Task 1: 原文源料层 `strategy/references/serenity/`

**Files:**
- Create: `strategy/references/serenity/README.md`
- Create: `strategy/references/serenity/00-信源清单.md`
- Create: `strategy/references/serenity/01-鉅亨-AI供应链教父投资逻辑.md`
- Create: `strategy/references/serenity/02-Foresight-一年45倍方法论.md`

- [ ] **Step 1: 抓取两个已验证可抓的源，留底**

Run（用已加载的 WebFetch；若环境无该工具则跳过、直接用本 plan 顶部"已抓取的方法论事实"）：
- WebFetch `https://news.cnyes.com/news/id/6476861` — prompt：提取 Serenity 投资逻辑的框架/术语/七层供应链案例。
- WebFetch `https://foresightnews.pro/article/detail/97459` — prompt：提取 Serenity 的分析框架/步骤/术语/案例。

Expected: 至少拿到七层供应链表 + 紫苏叶理论 + 五步分析法（与 plan 顶部事实一致即可）。

- [ ] **Step 2: 写 `README.md`（诚实声明）**

内容必须包含：
- 这是什么：Serenity（白毛股神）产业链分析法的**原文源料层**，是战略库第二核心根源的"源"，对应第一根源的 `strategy/references/十五五规划纲要-全文.md`。
- **诚实声明**：Serenity 最硬的内容在 X 付费订阅墙后（3.7 万付费），X 难抓取；本目录以**公开二手深度梳理**为主，每篇标注来源 URL+日期，定位"可获得的最佳公开源料"，**不假装抓到付费原文**。
- 提炼去向：经人读提炼进 `strategy/industry_investment/`，再蒸馏进 `skills/data/industrial-chain-tools.yaml` 才进引擎。
- 一句话指向 `00-信源清单.md`。

- [ ] **Step 3: 写 `00-信源清单.md`**

把 plan 顶部"信源 URL"全部登记，每条一行：`标题 — URL —（日期/抓取状态）— 一句话提要`。分两组：**方法论源**（鉅亨/Foresight/知乎/雪球/X/东方财富）与**争议源**（财联社/新浪财经）。日期统一用 2026-06，抓取状态标 ✅可抓 / ⚠仅登记。

- [ ] **Step 4: 写 `01-鉅亨-AI供应链教父投资逻辑.md` 与 `02-Foresight-一年45倍方法论.md`**

每篇结构：顶部 `> 来源：<标题> <URL>　抓取日期：2026-06-23　说明：公开二手梳理，非付费原文` + 正文按抓取内容如实整理（鉅亨篇=瓶颈理论+七层供应链表+术语；Foresight 篇=紫苏叶理论+五步分析法+对抗性验证）。**只保留产业链环节名，删除股票代码/涨幅/市值数字。**

- [ ] **Step 5: 验证文件齐全且无个股代码**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
ls strategy/references/serenity/
grep -rEn '\$[A-Z]{2,5}\b' strategy/references/serenity/ || echo "OK: 无股票代码"
```
Expected: 4 个文件齐全；`OK: 无股票代码`。

- [ ] **Step 6: Commit**

```bash
git add strategy/references/serenity/
git commit -m "feat: 战略库第二根源——Serenity 原文源料层（references/serenity/）

公开二手深度梳理为主，诚实标注来源，剥离个股代码。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: 提炼子层核心 —— `industry_investment/` 的 README + 00 + 01 + 02

**Files:**
- Create: `strategy/industry_investment/README.md`
- Create: `strategy/industry_investment/00-方法论框架.md`
- Create: `strategy/industry_investment/01-瓶颈理论与紫苏叶理论-卡点判断法.md`
- Create: `strategy/industry_investment/02-产业链下钻五步法-从大趋势到价值节点.md`

- [ ] **Step 1: 写 `README.md`（子层入口）**

参照其他子层 README 风格（先看 `strategy/perspective/README.md` 一眼对齐语气）。必须包含：
- 子层定位：战略库第二核心根源的**人读提炼层**，把 Serenity 的产业链分析法翻译成劳动者的行业判断/趋势前瞻/创业切入工具。
- 编号约定：`00` 为方法论框架，`01`–`04` 顺序展开。
- 文件清单（00–04 各一行提要）。
- 与第一根源的关系：十五五规划=国家产业方向；本根源=读懂任意产业链"卡点在哪"的微观方法，二者一宏一微互补。

- [ ] **Step 2: 写 `00-方法论框架.md`（核心，含劳动者视角翻译）**

必含小节：
1. 一句话总纲：Serenity 的打法本质是"在不可逆大趋势里，找最难被替代的那个卡点"。
2. 五大框架（用 plan 顶部事实，每个框架：原意一段 + "对劳动者意味着什么"一段）。
3. **劳动者视角翻译表**（照搬 plan 顶部四行表，每行展开 2–3 句）。
4. 与方法论库的接口：对抗性验证↔实事求是/矛盾分析；卡点判断↔抓主要矛盾。明示这是战略库工具，思想根基仍在 methodology/。
5. 诚实提示一行：本方法剥离了个股，只取框架；争议见 `04`。

- [ ] **Step 3: 写 `01-瓶颈理论与紫苏叶理论-卡点判断法.md`**

必含：
- 瓶颈理论详解（霍尔木兹海峡类比）。
- 紫苏叶理论详解（寿司店类比，落点"小而垄断"）。
- **劳动者卡点四问**（可执行清单）：① 我的岗位/行业在产业链哪一层？② 这一层是"卡点"（难替代、供给稀缺、有议价权、抗 AI）还是"易替代"（谁都能干、产能过剩、可外包/可自动化）？③ 卡点正在往哪一层转移？④ 我怎么往卡点靠（换岗/升级技能/换赛道切入）？
- 一个非科技行业的迁移示例（如养老护理/汽修：哪类技能是"紫苏叶"——稀缺且难替代）。

- [ ] **Step 4: 写 `02-产业链下钻五步法-从大趋势到价值节点.md`**

必含：
- 五步法（需求→传输/实现方式→物理/资源极限→替代方案→具体价值节点），每步配一个"劳动者怎么用这步"的问法。
- 约束条件导向：从硬约束（物理/资源/政策/人口）倒推，而非追热点。
- 配套四件事的劳动者简化版：看供应链图谱（这行的上下游是谁）、看壁垒（专利/牌照/资质/规模）、看产能与认证周期（进入门槛多高）、看政策与出口管制（哪些是国家在卡/在扶）。
- 一个完整走查示例（用机器人或新能源链，走完五步，落到"哪个环节是劳动者值得卡位的价值节点"）。

- [ ] **Step 5: 验证**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
ls strategy/industry_investment/
grep -lq "劳动者" strategy/industry_investment/00-方法论框架.md && echo "OK: 00 含劳动者视角"
grep -rEn '\$[A-Z]{2,5}\b' strategy/industry_investment/0[0-2]*.md || echo "OK: 无股票代码"
```
Expected: 4 文件在；`OK: 00 含劳动者视角`；`OK: 无股票代码`。

- [ ] **Step 6: Commit**

```bash
git add strategy/industry_investment/README.md strategy/industry_investment/00-方法论框架.md strategy/industry_investment/01-瓶颈理论与紫苏叶理论-卡点判断法.md strategy/industry_investment/02-产业链下钻五步法-从大趋势到价值节点.md
git commit -m "feat: 战略库第二根源——产业链分析提炼子层（方法论+卡点判断+下钻五步）

把 Serenity 的找卡点打法翻译成劳动者的行业判断/创业切入工具。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: 提炼子层 —— 案例 03 + 边界 04

**Files:**
- Create: `strategy/industry_investment/03-案例-AI算力光通信链七层拆解.md`
- Create: `strategy/industry_investment/04-边界与诚实-照搬风险·吹票争议·与共富的区别.md`

- [ ] **Step 1: 写 `03-案例-AI算力光通信链七层拆解.md`**

必含：
- 开篇说明：本篇是"怎么读一条产业链"的范例，**不是荐股**，全程不出现股票代码。
- 七层表（用 plan 顶部七层 + 关键术语），每层标注：这一层卡不卡（供给松紧）、为什么。
- 用这条链演示卡点四问与下钻五步如何落地（指向 01/02）。
- 一句迁移提示：同样的读法可套用到任意产业链（新能源、机器人、生物医药…）。

- [ ] **Step 2: 写 `04-边界与诚实-照搬风险·吹票争议·与共富的区别.md`**

必含（用 plan 顶部"诚实边界事实"）：
- 身份成谜与自述背景（标注"自称，未经独立核实"）。
- 跨境"吹票"争议始末（绿的谐波事件、赵丕业批评、监管风险提示）。
- 个人投资者照搬其**个股结论**的风险（信息倒灌、流量造神、跨境合规）。
- 共富立场区别：取"框架"弃"操作"；服务劳动者的行业/职业判断，不服务炒股；与"共同富裕"宗旨的关系。
- 这是 SKILL 设计规范"诚实"质量条在本根源的落地。

- [ ] **Step 3: 验证**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
ls strategy/industry_investment/0[34]*.md
grep -lq "吹票" strategy/industry_investment/04-边界与诚实-照搬风险·吹票争议·与共富的区别.md && echo "OK: 04 含争议"
grep -rEn '\$[A-Z]{2,5}\b' strategy/industry_investment/0[34]*.md || echo "OK: 无股票代码"
```
Expected: 2 文件在；`OK: 04 含争议`；`OK: 无股票代码`。

- [ ] **Step 4: Commit**

```bash
git add strategy/industry_investment/03-案例-AI算力光通信链七层拆解.md strategy/industry_investment/04-边界与诚实-照搬风险·吹票争议·与共富的区别.md
git commit -m "feat: 战略库第二根源——产业链案例（光通信七层）与诚实边界

案例只讲怎么读链不荐股；边界篇写明吹票争议与照搬风险。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: 引擎数据文件 `skills/data/industrial-chain-tools.yaml`

**Files:**
- Create: `skills/data/industrial-chain-tools.yaml`

- [ ] **Step 1: 写 YAML（schema 照 `marxism-tools.yaml`：`tools` + `cluster_match`）**

```yaml
# 产业链卡点分析工具速查
# 蒸馏自 strategy/industry_investment/（Serenity 产业链分析法的劳动者版）
# 与 methodology-tools.yaml / marxism-tools.yaml 互补：
#   思想武器库回答"怎么想"，本文件回答"怎么读一条产业链、找自己的价值卡点"
# 来源：strategy/references/serenity/ + strategy/industry_investment/
# 注意：只含分析框架，不含任何个股/仓位/买卖点。

tools:
  瓶颈定位-找产业链卡点:
    principle: 不盯龙头盯卡点——产业链里最难替代、最易断供的那一段最有议价权（像全球石油过霍尔木兹海峡）
    use_when: 用户判断行业前景/担心被替代/想知道自己岗位在产业链里值不值钱
    one_liner: 别问哪个行业火，问哪个环节卡——卡点处才有抗替代的议价权
    quote_source: Serenity 瓶颈理论（strategy/industry_investment/01）

  卡点四问-我在产业链哪一层:
    principle: 用四问给自己定位——在哪层？是卡点还是易替代？卡点在往哪转移？怎么往卡点靠
    use_when: 用户做行业判断/职业选择/担心岗位被淘汰
    one_liner: 四问定位：我在哪层、卡不卡、卡点往哪走、我怎么靠过去
    quote_source: Serenity 瓶颈理论·劳动者版（strategy/industry_investment/01）

  紫苏叶切入-小而垄断的价值节点:
    principle: 切入新领域别冲龙头红海，找需求刚性+供给稀缺+难复制的小节点（寿司店的紫苏叶）
    use_when: 用户想创业/转行/找细分切入点/做副业选方向
    one_liner: 找你的紫苏叶——需求刚、供给缺、别人难复制的小卡点
    quote_source: Serenity 紫苏叶理论（strategy/industry_investment/01）

  约束倒推-从硬约束找确定性:
    principle: 不追热点，从绕不开的硬约束（物理/资源/政策/人口）倒推——硬约束处确定性最高
    use_when: 用户做趋势前瞻/纠结追不追风口/想找确定性方向
    one_liner: 不追什么火，问什么绕不开——硬约束处才是确定性
    quote_source: Serenity 约束条件导向（strategy/industry_investment/02）

  对抗性验证-先证伪再相信:
    principle: 任何判断先主动找反例、替代威胁、被高估的地方，证伪后才信——呼应实事求是
    use_when: 用户对某个行业判断/创业点子过度乐观/需要泼冷水校准
    one_liner: 先使劲否定它，否定不掉再信——这才是实事求是
    quote_source: Serenity 对抗性验证 ×（methodology 实事求是/矛盾分析）

cluster_match:
  A-先进制造与硬科技: [瓶颈定位-找产业链卡点, 卡点四问-我在产业链哪一层, 约束倒推-从硬约束找确定性]
  B-数字与智能产业: [瓶颈定位-找产业链卡点, 卡点四问-我在产业链哪一层, 对抗性验证-先证伪再相信]
  C-绿色能源全链: [瓶颈定位-找产业链卡点, 约束倒推-从硬约束找确定性, 卡点四问-我在产业链哪一层]
  D-农业与乡村振兴: [紫苏叶切入-小而垄断的价值节点, 卡点四问-我在产业链哪一层]
  E-民生服务: [紫苏叶切入-小而垄断的价值节点, 卡点四问-我在产业链哪一层]
  F-文化创意与出海: [紫苏叶切入-小而垄断的价值节点, 约束倒推-从硬约束找确定性]
  G-基建物流房地产: [卡点四问-我在产业链哪一层, 瓶颈定位-找产业链卡点]
  H-新兴未来产业: [瓶颈定位-找产业链卡点, 约束倒推-从硬约束找确定性, 对抗性验证-先证伪再相信]
  I-传统矿业与资源开采: [瓶颈定位-找产业链卡点, 约束倒推-从硬约束找确定性]
  J-传统轻纺与日用制造: [卡点四问-我在产业链哪一层, 紫苏叶切入-小而垄断的价值节点]
  K-传统重化工与建材: [瓶颈定位-找产业链卡点, 卡点四问-我在产业链哪一层]
  L-商贸零售与餐饮住宿: [紫苏叶切入-小而垄断的价值节点, 卡点四问-我在产业链哪一层]
  M-金融与商务服务: [对抗性验证-先证伪再相信, 卡点四问-我在产业链哪一层]
  N-教育与培训: [紫苏叶切入-小而垄断的价值节点, 对抗性验证-先证伪再相信]
  O-居民生活服务: [紫苏叶切入-小而垄断的价值节点, 卡点四问-我在产业链哪一层]
  P-公用事业与市政服务: [卡点四问-我在产业链哪一层, 约束倒推-从硬约束找确定性]
```

- [ ] **Step 2: 验证 YAML 可加载且 cluster_match 引用的 key 都存在**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python -c "
import yaml
d = yaml.safe_load(open('skills/data/industrial-chain-tools.yaml'))
tools = set(d['tools'])
bad = [(c,k) for c,ks in d['cluster_match'].items() for k in ks if k not in tools]
assert not bad, f'cluster_match 引用了不存在的工具: {bad}'
assert len(d['cluster_match'])==16, f'应覆盖16个集群，实际 {len(d[\"cluster_match\"])}'
print('OK: tools', len(tools), '| clusters', len(d['cluster_match']))
"
```
Expected: `OK: tools 5 | clusters 16`（无断言报错）。

- [ ] **Step 3: Commit**

```bash
git add skills/data/industrial-chain-tools.yaml
git commit -m "feat: 产业链卡点分析工具卡（industrial-chain-tools.yaml）

Serenity 方法论蒸馏的5张工具卡 + 16集群映射，schema 对齐 marxism-tools。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: 引擎接入 `router.py` + `tools.py`（TDD：先写断言脚本）

**Files:**
- Create: `/tmp/verify_chain.py`（验证脚本，不进 git）
- Modify: `engine/router.py`（模块级加载区 + 新增 `get_chain_tools_for_cluster`）
- Modify: `engine/tools.py:_handle_analyze`（注入 `chain_tools`）

- [ ] **Step 1: 写验证脚本 `/tmp/verify_chain.py`**

```python
import sys, importlib, types, json
REPO = "/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill"
p = types.ModuleType("gongfu_engine"); p.__path__ = [REPO + "/engine"]
sys.modules["gongfu_engine"] = p
tools = importlib.import_module("gongfu_engine.tools")
router = importlib.import_module("gongfu_engine.router")

# 先确认 triage 把这句话分到某个 cluster 且路由到 industry-scan/opportunity-radar
tr = router.triage("我在半导体工厂的产线上做设备维护，想了解这个行业以后的前景和趋势")
print("cluster:", tr["extracted_info"].get("cluster"), "| route_to:", tr["route_to"])

raw = tools.gongfu_consult({
    "situation": "我在半导体工厂的产线上做设备维护，想了解这个行业以后的前景和趋势",
    "mode": "analyze",
})
res = json.loads(raw)
kc = res.get("knowledge_context", {})
assert "chain_tools" in kc, f"FAIL: knowledge_context 缺 chain_tools；现有键={list(kc)}"
assert kc["chain_tools"], "FAIL: chain_tools 为空"
print("PASS: chain_tools 已注入 ->", [t["name"] for t in kc["chain_tools"]])
```

- [ ] **Step 2: 运行，确认失败（功能未实现）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python /tmp/verify_chain.py
```
Expected: 先打印 `cluster: A-先进制造与硬科技 | route_to: [...industry-scan...]`，随后 `AssertionError: FAIL: knowledge_context 缺 chain_tools`。
（若 `cluster` 为 None 或 route_to 不含 industry-scan/opportunity-radar，换一句更明确的 situation，如加入"产线/设备/制造"等关键词，使其落到某集群且触发行业判断意图，再继续。）

- [ ] **Step 3: 在 `engine/router.py` 模块级加载区加 `_CHAIN`**

在已有 `_REGIONAL = _load_yaml("regional-matrix.yaml")`（约第 26 行）之后加一行：

```python
_CHAIN = _load_yaml("industrial-chain-tools.yaml")
```

- [ ] **Step 4: 在 `engine/router.py` 加 `get_chain_tools_for_cluster`**

紧跟 `get_marxism_tools_for_cluster` 之后（约第 326 行后）新增，结构与之对齐：

```python
def get_chain_tools_for_cluster(cluster: str) -> list:
    """Get the most relevant industrial-chain (Serenity 方法) tools for a cluster.

    Returns a list of tool dicts with principle, one_liner, use_when, quote_source.
    """
    if not cluster:
        return []
    cluster_match = _CHAIN.get("cluster_match", {})
    tool_keys = cluster_match.get(cluster, [])
    all_tools = _CHAIN.get("tools", {})
    result = []
    for key in tool_keys:
        tool = all_tools.get(key, {})
        if tool:
            result.append({
                "name": key,
                "principle": tool.get("principle", ""),
                "one_liner": tool.get("one_liner", ""),
                "use_when": tool.get("use_when", ""),
                "quote_source": tool.get("quote_source", ""),
            })
    return result
```

- [ ] **Step 5: 在 `engine/tools.py:_handle_analyze` 注入 `chain_tools`**

紧跟习近平思想工具注入块（`if xi_tools: knowledge_context["xi_tools"] = xi_tools` 之后，约第 309 行后）新增：

```python
    # ── 注入产业链卡点分析工具（Serenity 方法·战略库第二根源）──
    # 仅在行业判断/趋势前瞻类路由且识别出 cluster 时注入
    if info.get("cluster") and (
        "industry-scan" in route_to or "opportunity-radar" in route_to
    ):
        chain_tools = router.get_chain_tools_for_cluster(info["cluster"])
        if chain_tools:
            knowledge_context["chain_tools"] = chain_tools
```

- [ ] **Step 6: 运行验证脚本，确认通过**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python /tmp/verify_chain.py
```
Expected: `PASS: chain_tools 已注入 -> ['瓶颈定位-找产业链卡点', '卡点四问-我在产业链哪一层', '约束倒推-从硬约束找确定性']`。

- [ ] **Step 7: 回归——确认旧功能未坏（四思想体系仍注入）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python -c "
import sys,importlib,types,json
p=types.ModuleType('gongfu_engine'); p.__path__=['engine']; sys.modules['gongfu_engine']=p
tools=importlib.import_module('gongfu_engine.tools')
res=json.loads(tools.gongfu_consult({'situation':'我45岁钢铁厂下岗想转行','mode':'analyze'}))
kc=res.get('knowledge_context',{})
print('keys:', sorted(kc))
assert 'marxism_tools' in kc or 'marxism_inspiration' in kc, '回归失败：马克思主义注入丢失'
print('OK: 回归通过')
"
```
Expected: 打印 keys 列表，含马克思主义相关键；`OK: 回归通过`。

- [ ] **Step 8: Commit**

```bash
git add engine/router.py engine/tools.py
git commit -m "feat: 引擎接入产业链卡点工具——router 加载器 + analyze 注入

行业判断/趋势前瞻命中且识别出 cluster 时注入 chain_tools，
仿四思想体系工具的接入方式，零回归。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: SKILL.md 来源映射 + 测试用例 + 重建派生包

**Files:**
- Modify: `skills/industry-scan/SKILL.md`
- Modify: `skills/opportunity-radar/SKILL.md`

- [ ] **Step 1: 先读两个 SKILL.md，找到来源映射段与测试用例段的现有写法**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -nE "source_layers|来源映射|来源|测试|Test|源" skills/industry-scan/SKILL.md
grep -nE "source_layers|来源映射|来源|测试|Test|源" skills/opportunity-radar/SKILL.md
```
Expected: 定位到来源映射/源映射小节与测试用例小节的行号，照其既有格式追加（不破坏 frontmatter）。

- [ ] **Step 2: 在 `industry-scan/SKILL.md` 来源映射处补一行**

在来源映射小节追加（措辞对齐该文件既有条目）：
> `strategy/industry_investment/`（Serenity 产业链卡点分析法）｜ `skills/data/industrial-chain-tools.yaml`（产业链卡点工具卡）

并在测试用例段追加一条：
> 输入"我在半导体工厂产线做设备维护，想了解行业前景" → 期望输出体现"产业链卡点/瓶颈定位/我在哪一层"的判断视角（来自 chain_tools）。

- [ ] **Step 3: 在 `opportunity-radar/SKILL.md` 来源映射处补一行**

来源映射追加：
> `strategy/industry_investment/`（约束倒推·从硬约束找确定性）｜ `skills/data/industrial-chain-tools.yaml`

测试用例追加：
> 输入"未来几年哪个方向确定性高，我想提前卡位" → 期望输出体现"从硬约束倒推、找产业链价值节点"的视角。

- [ ] **Step 4: 重建派生包并验证一致**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python scripts/build_packs.py
git status --porcelain skills/ claude-skills/ engine/skills/ agents/ | head
```
Expected: `build_packs.py` 正常结束；派生位置已被 gitignore（`git status` 不应出现 `engine/skills/`、`claude-skills/skills/`、`agents/zcode-skills/` 的改动；只有 `skills/` 源的改动）。

- [ ] **Step 5: Commit**

```bash
git add skills/industry-scan/SKILL.md skills/opportunity-radar/SKILL.md
git commit -m "docs: industry-scan/opportunity-radar 补产业链卡点来源映射与测试用例

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: 文档同步（strategy README × 2 + CHANGELOG）

**Files:**
- Modify: `strategy/README.md`
- Modify: `strategy/references/README.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: 更新 `strategy/README.md`**

- 开头"战略库是共富参谋的第二个底层思想源……"段后，补一句点明**现有两个核心根源**：十五五规划（宏观国家产业方向）+ Serenity 产业链分析法（微观读懂任意产业链卡点）。
- "九个子层"标题改为"十个子层"，表格新增一行：
  > `industry_investment/` ｜ Serenity 产业链卡点分析法（劳动者版：瓶颈/紫苏叶/约束倒推/下钻五步/对抗验证）｜ `00`–`04`
- "维护原则"不变。

- [ ] **Step 2: 更新 `strategy/references/README.md`**

补说明：`references/` 现含两个根源的原文源料——`十五五规划纲要-全文.md`（第一根源）与 `serenity/`（第二根源，公开二手梳理为主，付费原文未抓取）。

- [ ] **Step 3: 更新 `CHANGELOG.md` 的 `[未发布]` 段**

把 `（暂无）` 替换为：

```markdown
### 新增 Added

- **战略库新增第二核心根源：Serenity 产业链分析法**。在十五五规划之外，新增"读懂任意产业链卡点"的微观方法体系：原文源料 `strategy/references/serenity/`、提炼子层 `strategy/industry_investment/`（瓶颈理论/紫苏叶理论/约束倒推/下钻五步/对抗性验证，全部翻译为劳动者版的行业判断与创业切入工具，剥离个股）。
- **引擎接入产业链卡点工具**：新增 `skills/data/industrial-chain-tools.yaml`，`engine/router.py` 增 `get_chain_tools_for_cluster`，`gongfu_consult` 在行业判断/趋势前瞻类咨询且识别出集群时注入 `chain_tools`。

> 说明：本项含引擎改动（新增加载器与注入），发版时建议升至 `1.3.0`（三处版本号同步 + 本段移入正式版本号）。
```

- [ ] **Step 4: 验证 + Commit**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -q "industry_investment" strategy/README.md && grep -q "serenity" strategy/references/README.md && grep -q "第二核心根源" CHANGELOG.md && echo "OK: 文档已同步"
```
Expected: `OK: 文档已同步`。

```bash
git add strategy/README.md strategy/references/README.md CHANGELOG.md
git commit -m "docs: 战略库 README 升至十子层 + 第二根源说明 + CHANGELOG 未发布段

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8（收尾·可选）: 端到端复核 + 版本决策

- [ ] **Step 1: 端到端冒烟（HTTP 壳，确认四壳共用引擎都拿到 chain_tools）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
.venv/bin/python -c "
import sys,importlib,types,json
p=types.ModuleType('gongfu_engine'); p.__path__=['engine']; sys.modules['gongfu_engine']=p
tools=importlib.import_module('gongfu_engine.tools')
for s in ['我在光伏电站做运维，想知道这行以后还有没有前途','未来几年哪个方向确定性高我想提前卡位']:
    res=json.loads(tools.gongfu_consult({'situation':s,'mode':'analyze'}))
    print(s[:12],'->','chain_tools' in res.get('knowledge_context',{}))
"
```
Expected: 至少有命中行业判断/趋势且识别出集群的句子打印 `True`（识别不出集群的句子为 `False` 属正常——注入是 cluster-gated）。

- [ ] **Step 2: 版本决策**

与用户确认是否本轮升 `1.3.0`。若升：改 `pyproject.toml`、`api_server/server.py`（index `version`）、`engine/plugin.yaml` 三处为 `1.3.0`；把 CHANGELOG `[未发布]` 段落迁为 `## [1.3.0] - <发版日>`；更新 `README.md` 顶部版本行；按需打 tag + GitHub Release（沿用既有发布流程）。

---

## Self-Review（写完即查）

**1. Spec coverage：**
- 知识层原文源料（spec 4.1）→ Task 1 ✅
- 提炼子层 README+00–04（spec 4.2）→ Task 2/3 ✅
- 劳动者视角翻译（spec 4.3）→ Task 2 Step 2/3 ✅
- 引擎数据文件（spec 5.1）→ Task 4 ✅
- router 加载器（spec 5.2）→ Task 5 Step 3/4 ✅
- tools 注入（spec 5.3）→ Task 5 Step 5 ✅
- SKILL 来源映射 + build_packs（spec 5.4）→ Task 6 ✅
- 文档同步（spec 5.5）→ Task 7 ✅
- 验证方式（spec 6）→ Task 4/5/6/8 的验证步骤 ✅
- 版本影响（spec 7）→ Task 7 Step 3 提示 + Task 8 Step 2 决策 ✅
- 非目标（spec 8：不建启发库/不抓付费/不出个股）→ 全程 grep 个股代码守护 + 不加 inspiration 加载器 ✅

**2. Placeholder scan：** 引擎/YAML 步骤均为完整可粘贴代码；内容文件给出"必含小节 + 已抓取事实"，无 TBD/TODO。✅

**3. Type/命名一致性：** `_CHAIN`、`get_chain_tools_for_cluster`、`knowledge_context["chain_tools"]`、`industrial-chain-tools.yaml`、子层 `industry_investment/` 全文一致。`cluster_match` 的 key 与 `tools` 的 key 在 Task 4 Step 2 用脚本断言一致。✅
