# 经济政策追踪专栏（搭建分线骨架）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在战略库搭建第三条研究根源——"经济政策追踪专栏"的可用骨架：目录结构 + 各 README + 方法论框架 + 近10年政策追踪台账 + 诚实边界 + 信源脚手架。深度主线复盘与全量语料留作后续扩展轮次。

**Architecture:** 镜像现有根源模式：原文源料进 `strategy/references/policy_archive/`，专栏（新子层）`strategy/economic_policy/` 放方法论框架 + 追踪台账 + 边界。本轮**不动引擎**（无 `skills/data` / `router.py` / `tools.py` 改动，无需跑 build_packs——`strategy/` 不是派生包来源）。

**Tech Stack:** Markdown 知识文件；WebFetch/WebSearch 做政策信源核实；无 Python、无自动化测试，按 doc-based 验证（文件齐全 + 台账年份齐 + grep 无个股 + README 与实际文件一致）。

**设计依据：** `docs/superpowers/specs/2026-06-24-economic-policy-column-design.md`（注意其中"本轮交付=搭建分线骨架"的收窄说明）。

**全局约定（每个任务都遵守）：**
- 中文优先；提交信息中文，结尾加 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`。
- **诚实/中立**：如实记录政策原文与官方/统计局可查结果；政策↔结果按观察性关联表述，不下严格因果；不做政治评判、不做投资建议、不出个股代码/涨幅。
- **READMEs 只描述真实存在的文件**：本轮只建 README/00/01/05；`02/03/04` 在 README 里只作为"后续扩展路线"用"下一轮将新增…"措辞描述，**不**列进"当前文件"清单、**不**创建空壳文件。
- 抓不到的锚点：只在信源清单登记 URL，正文用官方可引的公开摘要，不伪造原文。

---

## 已核实/待核实的政策事实（写台账时用，逐条仍需实现者核实并附来源）

**中央经济工作会议历年核心定调（2016—2025，搜索已得主体，标注待核实项）：**
- 2016：延续"稳中求进"；深化供给侧结构性改革；**首提"房子是用来住的、不是用来炒的"**（待核实确切表述）
- 2017：**首提习近平新时代中国特色社会主义经济思想（"七个坚持"）**；高质量发展
- 2018："五个必须"；部署"六稳"（稳就业等）
- 2019：稳字当头（待核实当年框架）
- 2020："五个根本"；**双碳目标**进入部署；强化反垄断、防止资本无序扩张
- 2021："四个必须"，"稳字当头、稳中求进"；提出**需求收缩、供给冲击、预期转弱**三重压力（共同富裕由 2021 中央财经委会议提出）
- 2022："六个坚持"；着力扩大内需、提振信心
- 2023："五个必须"，"稳中求进、以进促稳、先立后破"；**新质生产力**（2023 年首次提出）
- 2024："根本保证""五个必须统筹"；**货币政策转向"适度宽松"（多年来首次）、财政"更加积极"**；提振消费居首
- 2025："五个必须"（挖掘潜能 / 政策支持与改革创新并举 / 既"放得活"又"管得好" / 投资于物与投资于人结合 / 苦练内功应对外部挑战）；"十五五"开局

**6 条标志性主线的起点（供后续复盘轮次，本轮台账只标时间点不深挖）：**
供给侧结构性改革(2015) → 双碳(2020) → 共同富裕(2021) → 新质生产力(2023) → 货币"稳健→适度宽松"(2024) → 财政"积极→更加积极"(2024)。

**信源（实现者核实/抓取时用）：**
- 共产党员网·历次中央经济工作会议专题 https://www.12371.cn/special/lczyjjgzhy/
- 国务院政策文件库 https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary ；中国政府网政策 https://www.gov.cn/zhengce/
- 国家发改委文件库 https://www.ndrc.gov.cn/xxgk/wjk/ ；国家统计局 https://www.stats.gov.cn/
- 官方回顾示例：供给侧改革深度观察 https://www.gov.cn/yaowen/liebiao/202506/content_7026829.htm

**劳动者视角翻译表（写进 00-方法论框架）：**
| 政策研究的常规用途 | 共富·劳动者版 |
| 读懂政策定调 | 看国家在"扶什么/卡什么"：政策风口往哪吹，哪些行业/区域/岗位有顺风 |
| 政策有时滞 | 提前布局：政策出台到见效有时间差，劳动者怎么卡在见效前 |
| 政策↔真实结果规律 | 别只听口号看落地：哪些政策真传导到就业/收入，哪些雷声大雨点小 |
| 政策主线演进 | 呼应方法论库的实事求是 / 抓主要矛盾：跟住主线、不追噪声 |

---

## File Structure

**Create（原文源料脚手架）：**
- `strategy/references/policy_archive/README.md` — 定位 + 诚实声明
- `strategy/references/policy_archive/00-信源清单.md` — 锚点/官方回顾/统计口径来源台账
- `strategy/references/policy_archive/01-样本-2025中央经济工作会议公报.md` — 1 份样本锚点整理
- `strategy/references/policy_archive/02-样本-十四五规划要点.md` — 1 份样本锚点整理

**Create（专栏骨架）：**
- `strategy/economic_policy/README.md` — 专栏定位 + 两期规划 + 与 analysis/perspective 分工 + 当前文件(00/01/05) + 后续扩展路线(02/03/04)
- `strategy/economic_policy/00-方法论框架.md` — 政策→现实分析法 + 劳动者视角翻译
- `strategy/economic_policy/01-政策追踪台账.md` — 近10年锚点时间线（核心骨架）
- `strategy/economic_policy/05-边界与诚实.md` — 规律复盘不是预言；中立、可追溯、关联非因果

**Modify（文档同步）：**
- `strategy/README.md` — 十个子层→十一个；加第三条研究根源说明

---

## Task 1: 原文源料脚手架 `strategy/references/policy_archive/`

**Files:**
- Create: `strategy/references/policy_archive/README.md`
- Create: `strategy/references/policy_archive/00-信源清单.md`
- Create: `strategy/references/policy_archive/01-样本-2025中央经济工作会议公报.md`
- Create: `strategy/references/policy_archive/02-样本-十四五规划要点.md`

- [ ] **Step 1: 抓样本锚点**

用 WebFetch（先 `ToolSearch "select:WebFetch"` 加载）抓取并提炼：
- 2025 年中央经济工作会议公报（核心定调"五个必须"+ 主要任务），来源优先共产党员网/新华网/中国政府网。
- 十四五规划纲要要点（主要目标 + 重点任务），来源中国政府网。
若某源抓取失败，用本 plan 顶部已核实事实 + 在信源清单标注"⚠仅登记 URL"。

- [ ] **Step 2: 写 `README.md`**

必含：(a) 定位——国家经济政策的**原文源料层**，是专栏 `strategy/economic_policy/` 的源，与第一根源 `references/十五五规划纲要-全文.md`、第二根源 `references/serenity/` 并列；(b) **诚实声明**——公开官方源为主，每篇标来源 URL+日期，抓不到的只登记 URL 不伪造；(c) 指向 `00-信源清单.md`；(d) 提炼去向：经 `economic_policy/` 复盘提炼。

- [ ] **Step 3: 写 `00-信源清单.md`**

把本 plan 顶部"信源"逐条登记：`名称 — URL —（性质/抓取状态）— 一句话提要`。分组：**政策原文库**（国务院政策文件库 / 政府网 / 发改委文件库 / 共产党员网会议专题）、**真实结果数据**（国家统计局 / 官方回顾）。日期用 2026-06，状态标 ✅可抓 / ⚠仅登记。

- [ ] **Step 4: 写两份样本锚点**

每份顶部 `> 来源：<名称> <URL>　抓取日期：2026-06-24　说明：官方公开源整理`，正文如实整理核心定调/要点。**无个股、无投资建议。**

- [ ] **Step 5: 验证**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
ls strategy/references/policy_archive/
grep -rEn '\$[A-Z]{2,5}\b' strategy/references/policy_archive/ || echo "OK: 无股票代码"
grep -q "诚实" strategy/references/policy_archive/README.md && echo "OK: 含诚实声明"
```
Expected: 4 文件；`OK: 无股票代码`；`OK: 含诚实声明`。

- [ ] **Step 6: Commit**

```bash
git add strategy/references/policy_archive/
git commit -m "feat: 经济政策专栏——原文源料脚手架（references/policy_archive/）

信源清单 + 2 份样本锚点（2025中央经济工作会议公报、十四五要点），
公开官方源为主，诚实标注来源。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: 专栏框架与边界 `economic_policy/` 的 README + 00 + 05

**Files:**
- Create: `strategy/economic_policy/README.md`
- Create: `strategy/economic_policy/00-方法论框架.md`
- Create: `strategy/economic_policy/05-边界与诚实.md`

- [ ] **Step 1: 写 `README.md`（专栏入口）**

先读 `strategy/perspective/README.md` 对齐语气。必含：
- 专栏定位：战略库**第三条研究根源**——追踪国家经济政策发布 + 摸透"政策↔真实经济社会"的作用规律。三根源分工：规划=国家要往哪走（宏观方向）｜Serenity=产业链微观卡点｜本专栏=政策与现实的作用规律（宏观实证）。
- 两期规划：Phase 1（本期=搭建骨架 + 后续分批扩展复盘语料）；Phase 2（推演，另开 spec，含引擎接入）。
- 与现有层分工：`analysis/`(读单一规划文本) / `perspective/`(行业主题中长期前瞻) / `industry_investment/`(产业链微观) 的区别。
- **当前文件**（只列真实存在的）：`00-方法论框架.md`、`01-政策追踪台账.md`、`05-边界与诚实.md`。
- **后续扩展路线**（用"下一轮将新增"措辞，不列为现有文件）：`02/03 政策主线深度复盘`、`04 作用规律总结` 将在内容扩展轮次补齐。

- [ ] **Step 2: 写 `00-方法论框架.md`（核心，含劳动者视角翻译）**

必含：
1. 一句话总纲：读政策不是背文件，是看"国家把资源往哪引、把真实经济社会带向何处"。
2. **政策→现实四步分析法**：①政策意图（原文定调）→②落地举措→③真实结果（官方/统计局可查数据）→④观察到的规律（时滞、传导机制、对就业/收入的传导）。强调④是观察性关联，非严格因果。
3. **劳动者视角翻译表**（照搬本 plan 顶部表，每行展开 2–3 句）。
4. 与方法论库接口：读政策↔实事求是、抓主要矛盾（跟主线不追噪声）。明示思想根基在 `methodology/`，本专栏是战略库应用层。
5. 诚实提示一行：本专栏只复盘规律、不预言；推演见 Phase 2；边界见 `05`。

- [ ] **Step 3: 写 `05-边界与诚实.md`**

必含：①这是**规律复盘不是预言**，方向非时间表；②**中立**——记录政策与可查结果，不做政治评判、不做宣传；③政策↔结果是**观察性关联**，多因素、反事实不可得，不下严格因果；④数据口径以统计局/官方已公布为准，承认挑选性偏差风险；⑤不构成投资建议、不出个股；⑥这是 SKILL 设计规范"诚实"质量条在本专栏的落地。

- [ ] **Step 4: 验证**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
ls strategy/economic_policy/
grep -lq "劳动者" strategy/economic_policy/00-方法论框架.md && echo "OK: 00 含劳动者视角"
grep -lq "不是预言\|非严格因果\|观察性关联" strategy/economic_policy/05-边界与诚实.md && echo "OK: 05 含边界"
# README 不应把 02/03/04 列入"当前文件"——人工确认措辞为"后续/下一轮"
grep -n "02\|03\|04" strategy/economic_policy/README.md || true
```
Expected: 3 文件（README/00/05）；两个 OK；README 中 02/03/04 仅出现在"后续扩展路线"语境。

- [ ] **Step 5: Commit**

```bash
git add strategy/economic_policy/README.md strategy/economic_policy/00-方法论框架.md strategy/economic_policy/05-边界与诚实.md
git commit -m "feat: 经济政策专栏——框架与边界（README + 方法论 + 诚实边界）

政策→现实四步分析法 + 劳动者视角翻译；明确规律复盘非预言、中立可追溯。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: 政策追踪台账 `economic_policy/01-政策追踪台账.md`（骨架核心）

**Files:**
- Create: `strategy/economic_policy/01-政策追踪台账.md`

- [ ] **Step 1: 核实历年定调**

用 WebSearch/WebFetch 核实 2016—2025 每年中央经济工作会议的核心定调框架与关键新提法（本 plan 顶部已给主体，重点补 2016、2019 两年，并核实"房住不炒(2016)""新质生产力(2023)""货币适度宽松(2024)"等提法首次出现年份）。每条要能附一个权威来源（共产党员网/新华网/中国政府网）。

- [ ] **Step 2: 写台账正文**

结构：
- 顶部说明：本台账是专栏骨架，逐年记录国家经济政策的"锚点"，是后续主线复盘的索引；**只记定调与提法变化，不深挖结果**（结果复盘在后续 `02/03`）。
- **主表（2016—2025 逐年一行）**，列：`年份 | 中央经济工作会议核心定调 | 关键新提法/转向 | 配套（政府工作报告/五年规划节点）| 来源`。十年齐全，每行带来源链接。
- **标志性提法时间线**（独立小节）：供给侧改革(2015)→房住不炒(2016)→习近平经济思想(2017)→双碳(2020)→共同富裕(2021)→新质生产力(2023)→货币适度宽松·财政更加积极(2024)，每条一句话 + 年份。
- 结尾：指向 `00` 的分析法、指向后续 `02/03/04` 复盘（用"将在扩展轮次补齐"措辞）。
- **无个股、无投资建议、无政治评判**；定调表述贴合官方原文。

- [ ] **Step 3: 验证**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f=strategy/economic_policy/01-政策追踪台账.md
for y in 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025; do grep -q "$y" "$f" || echo "缺年份 $y"; done; echo "年份检查完"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
grep -q "供给侧\|新质生产力\|双碳" "$f" && echo "OK: 含标志性提法"
```
Expected: `年份检查完`（无"缺年份"行）；`OK: 无股票代码`；`OK: 含标志性提法`。

- [ ] **Step 4: Commit**

```bash
git add strategy/economic_policy/01-政策追踪台账.md
git commit -m "feat: 经济政策专栏——近10年政策追踪台账（骨架核心）

2016-2025 中央经济工作会议逐年定调 + 标志性提法时间线，每条带权威来源。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: 文档同步 `strategy/README.md`

**Files:**
- Modify: `strategy/README.md`

- [ ] **Step 1: 读现状**

Run: `grep -n "个子层\|industry_investment\|两个核心根源\|references" strategy/README.md` 定位"十个子层"标题、子层表、根源说明句。

- [ ] **Step 2: 改子层数与表格**

- "## 十个子层" → "## 十一个子层"（及任何"十个"prose）。
- 子层表新增一行（匹配现有 `子层 | 内容 | 编号约定` 格式）：
  `| \`economic_policy/\` | 经济政策追踪专栏（政策追踪台账 + 政策↔现实作用规律；推演见 Phase 2） | \`00\`/\`01\`/\`05\`（骨架，后续扩展） |`
- 在介绍"两个核心根源"的句子处改为**三条研究根源**：十五五规划（宏观方向）+ Serenity 产业链分析法（产业链微观）+ 经济政策追踪专栏（政策↔现实作用规律）。

- [ ] **Step 3: 改 references 行（说明新增 policy_archive）**

`references/` 表格行描述补上第三根源源料，例如：
`战略库根源文档（十五五规划纲要全文；Serenity 产业链分析法源料 serenity/；国家经济政策源料 policy_archive/），只放源文档不加工`。

- [ ] **Step 4: 验证 + Commit**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -q "economic_policy" strategy/README.md && grep -q "十一个子层" strategy/README.md && grep -q "三条研究根源\|第三" strategy/README.md && echo "OK: README 同步"
grep -q "policy_archive" strategy/README.md && echo "OK: references 行已补"
```
Expected: `OK: README 同步`、`OK: references 行已补`。

```bash
git add strategy/README.md
git commit -m "docs: 战略库 README 升至十一子层 + 第三条研究根源（经济政策专栏）说明

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5（收尾·可选）: 整体复核

- [ ] **Step 1: 骨架完整性复核**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
echo "=== 专栏文件 ===" && ls strategy/economic_policy/ strategy/references/policy_archive/
echo "=== 全专栏无个股 ===" && grep -rEn '\$[A-Z]{2,5}\b' strategy/economic_policy/ strategy/references/policy_archive/ || echo "OK: 无股票代码"
echo "=== README 不描述不存在的文件 ===" && ls strategy/economic_policy/ | grep -E "02|03|04" && echo "注意:发现02/03/04文件(本轮不应创建)" || echo "OK: 本轮未创建 02/03/04"
```
Expected: `economic_policy/` 含 README/00/01/05；`OK: 无股票代码`；`OK: 本轮未创建 02/03/04`。

- [ ] **Step 2: 确认无引擎改动**

Run: `git diff --stat main..HEAD -- engine/ skills/` → 应为空（本轮不动引擎/数据）。

---

## Self-Review（写完即查）

**1. Spec coverage（对照 spec 的"本轮交付=搭建分线骨架"）：**
- 信源脚手架（references/policy_archive: README+信源清单+1–2样本）→ Task 1 ✅
- 专栏 README（含已建/待扩展标注）→ Task 2 Step 1 ✅
- 00 方法论框架 + 劳动者视角翻译 → Task 2 Step 2 ✅
- 05 边界与诚实 → Task 2 Step 3 ✅
- 01 政策追踪台账（近10年锚点骨架）→ Task 3 ✅
- strategy/README 11 子层 + 第三根源 → Task 4 ✅
- 不动引擎、推演留 Phase 2、02/03/04 不建 → 全程约束 + Task 5 复核 ✅
- 诚实/中立、无个股 → 各任务 grep + 边界文件 ✅

**2. Placeholder scan：** 内容文件给出"必含小节 + 已核实事实 + 需核实项明确标注"，台账要求逐年附来源；无 TBD/TODO 式占位。02/03/04 是**明确的后续范围**不是占位。✅

**3. 命名一致性：** 子层 `economic_policy/`、源料 `references/policy_archive/`、文件 `00/01/05`、台账列结构、三根源表述，全文一致。✅
