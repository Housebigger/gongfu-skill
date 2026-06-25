# 经济政策专栏 Phase 2 推演（情景化议题推演）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为经济政策专栏补 Phase 2 推演（知识层）：一个推演方法+外部约束框架（06）+ 对 6 个关键议题各做基准/上行/下行三情景推演（07/08），调用规律库（04）外推，给方向不给时间表。

**Architecture:** 在已建专栏 `strategy/economic_policy/`（00–05 已就位）新增 06/07/08 三个文件。06 是推演版"方法框架"（方法 + 国际形势/国情共用假设 + 诚实边界与复盘机制）；07/08 各 3 个议题，按统一六要素模板（现状锚点→规律库外推→外部约束→三情景→可证伪点→劳动者含义），组织镜像 Phase 1 的 02/03。**本轮不动引擎**（无 `skills/data`/`engine/` 改动，无需 build_packs——`strategy/` 不是派生包来源），**不升版本**。

**Tech Stack:** Markdown；WebSearch/WebFetch 核实现状数据与国际形势；无 Python、无自动化测试，doc-based 验证（文件齐全 + 每议题六要素 + 三情景带假设 + 可证伪点 + grep 无个股 + 情景条件式非断言）。

**设计依据：** `docs/superpowers/specs/2026-06-25-economic-policy-phase2-deduction-design.md`。承接 Phase 1（01 台账 / 02·03 主线复盘 / 04 作用规律，均已合并入 main）。

**全局约定：**
- 中文优先；提交信息中文，结尾 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`。
- **诚实/中立/推演纪律**：情景措辞用**条件式**（"若…则…/在…假设下…"），**不给点位预测、不给时间表、不出个股/投资建议、不做政治预测**；每个情景讲清**触发条件 + 关键假设**；现状锚点带**官方/权威来源链接**（先搜后确认，抓不到只登记不伪造）。
- **推演调用规律库**：每个议题的外推都要引 `04 作用规律`（时滞/传导/对就业收入）作为依据，注"见 04 哪条"，不脱离已复盘规律凭空预测。
- 时间双视角：近期（2026—2027）+ 十五五期（2026—2030，方向性）。

---

## 已搜集的锚点（写作据此并逐条在线复核 + 补来源；2026 视角）

**国际形势共用假设（写进 06）：**
- 中美博弈"常态化、结构化"、"以关税换让步"，但 2026 维持"战略稳定点"沟通；关税/科技出口管制是持续变量。2025 关税一度达 145%、对美进出口占中国外贸比重降至 8.8%。
- 全球增长回落（约 2.7%—3.1%），WTO 下调 2026 全球货物贸易增速至 0.5%；供应链重构 / 产业政策民族主义抬头。
- 全球南方 / 一带一路是出海增量方向。
- 来源：[新华网《2026 世界经济五问》](https://www.news.cn/world/20260103/d58bff34577547bf8c813f69f2288d02/c.html)、[复旦 FDDI《管理性贸易：2026 美国对华贸易政策》](https://fddi.fudan.edu.cn/c8/91/c21253a772241/page.htm)、[中外对话《2026 国际局势前瞻》](https://www.chinanews.com.cn/dxw/2026/01-01/10544449.shtml)。

**国情共用设定（写进 06）：** 2026 十五五开局（GDP 预测约 4.5%—5%，财政加力、货币适度宽松）；居民资产负债表受房价调整、内需修复需时间；房地产 + 地方债两只"灰犀牛"化解中未出清；人口负增长 / 老龄化（结构性慢变量）；共同富裕/收入分配长期主线。来源：[北大光华 2026 展望](https://www.gsm.pku.edu.cn/info/1316/31120.htm)、[第一财经"十五五"机遇挑战](https://www.yicai.com/news/102936303.html)。

**6 议题各自的现状锚点 + 规律库挂钩（实现者据此并在线复核）：**

1. **内需/消费**：居民消费偏弱、储蓄动机增强、服务消费是 2026 促消费重点；居民人均可支配收入 2024 年 41314 元。规律挂钩：04 四（财政消费补贴/共同富裕对收入成本传导）+ 04 二（货币传导受有效需求制约）。
2. **房地产**：灰犀牛、2026 或进一步支持（收储、"好房子"）；居民资产负债表受房价调整。规律挂钩：04 一/三（去库存类政策落地节奏、财政收储传导）。
3. **财政与地方债**："6+4+2"万亿化债、2025 赤字率 4%、专项债 4.4 万亿。规律挂钩：04 二（配套财政落地→传导到项目/岗位）。
4. **AI+新质生产力**：高技术制造业增加值 2024 +8.9%、占规上 16.3%；新能源汽车 1316.8 万辆 +38.7%；R&D 强度 2.69%。规律挂钩：04 一（长周期、局部快）+ 04 四（直接创岗类型）。
5. **外需与制造出海**：美元计出口增速或约 5%（贸易斗争边际缓和 + 产业链韧性）；中美博弈常态化、供应链重构、全球南方。规律挂钩：04 一/三 + 06 国际假设。
6. **人口与劳动力**：人口负增长、老龄化加速；中等收入群体占比约 38.86%（2021）。规律挂钩：04 长周期慢变量 + `perspective/02 人口` 呼应。

---

## File Structure

**Create:**
- `strategy/economic_policy/06-推演方法与外部约束.md` — 推演方法（六要素模板说明）+ 国际形势/国情共用假设 + 推演诚实边界 + 定期复盘机制
- `strategy/economic_policy/07-关键议题推演（上）.md` — 内需/消费、房地产、财政与地方债（各六要素 + 三情景）
- `strategy/economic_policy/08-关键议题推演（下）.md` — AI+新质、外需与出海、人口与劳动力（各六要素 + 三情景）

**Modify:**
- `strategy/economic_policy/README.md` — 当前文件加 06/07/08；Phase 2 状态更新（推演内容已建，引擎接入仍待）
- `CHANGELOG.md` — `[未发布]` 段补 Phase 2 推演

---

## Task 1: 推演方法与外部约束 `06-推演方法与外部约束.md`

**Files:**
- Create: `strategy/economic_policy/06-推演方法与外部约束.md`

- [ ] **Step 1: 核实国际形势/国情共用假设**

用 WebSearch/WebFetch（`ToolSearch "select:WebSearch,WebFetch"`）复核本 plan 顶部国际形势 + 国情共用假设的关键事实与数字（中美博弈常态化、全球增长~2.7-3.1%、WTO 贸易 0.5%、2026 GDP 预测、十五五开局财政货币基调），每条能附一个权威来源。

- [ ] **Step 2: 写文件**

先读 `strategy/economic_policy/00-方法论框架.md`、`04-作用规律总结.md`、`05-边界与诚实.md`、`strategy/perspective/00-方法论框架.md` 对齐语气与诚实口径。必含小节：
1. **推演方法（六要素模板）**：说明每个议题怎么推——①现状锚点（带来源）②规律库外推（引 04 时滞/传导/就业收入规律）③套外部约束+国情④基准/上行/下行三情景（各带触发条件+关键假设）⑤可证伪点/观察指标⑥劳动者含义。强调情景条件式、调用规律库而非凭空预测。
2. **国际形势共用假设**（写进本 plan 顶部国际假设，带来源；标"截至成文 2026-06"）。
3. **国情共用设定**（本 plan 顶部国情设定，带来源）。
4. **推演的诚实边界**：情景非预言、给方向不给点位/时间表、不投资建议、不政治预测；呼应 `05` 与 `perspective/` 诚实边界。
5. **定期复盘机制**：列"观察指标→看到什么说明在走哪条情景"的检验思路，写明"建议每半年/年度回看：哪些情景在兑现、假设是否还成立、到点更新"。
6. 指向 07/08（议题推演）、04（规律引擎）。
**无个股、无投资建议、无政治预测、无时间表。**

- [ ] **Step 3: 验证**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f="strategy/economic_policy/06-推演方法与外部约束.md"
grep -q "情景\|基准\|上行\|下行" "$f" && grep -q "假设" "$f" && grep -q "可证伪\|观察指标" "$f" && echo "OK: 含方法要素"
grep -q "复盘\|回看\|校验" "$f" && echo "OK: 含复盘机制"
grep -q "不预测\|不给时间表\|非预言\|不构成投资建议" "$f" && echo "OK: 含诚实边界"
grep -qi "http" "$f" && echo "OK: 含来源"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
```
Expected: 含方法要素 / 含复盘机制 / 含诚实边界 / 含来源 / 无股票代码.

- [ ] **Step 4: Commit**
```bash
git add "strategy/economic_policy/06-推演方法与外部约束.md"
git commit -m "feat: 经济政策专栏 Phase 2——推演方法与外部约束（06）

六要素推演模板 + 国际形势/国情共用假设 + 诚实边界 + 定期复盘机制。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: 关键议题推演（上）`07-…内需·房地产·财政与地方债.md`

**Files:**
- Create: `strategy/economic_policy/07-关键议题推演（上）-内需·房地产·财政与地方债.md`

- [ ] **Step 1: 核实三议题现状锚点**

在线核实议题①内需/消费、②房地产、③财政与地方债的现状数据（本 plan 顶部锚点 + 最新可查值），每条附官方/权威来源。

- [ ] **Step 2: 写文件**

先读 `06`（用其共用假设与模板）与 `04`（取外推规律）。顶部说明：本篇按 `06` 六要素模板，对需求与风险侧三议题做情景化推演；情景为条件式、非预言；外推依据见 04，外部约束见 06。
对议题①②③各写一节，每节六要素：
- ①现状锚点（数据+来源）
- ②规律库外推（引 04 对应条，如内需↔04 二有效需求制约 / 房地产↔04 一去库存 / 财政↔04 二配套传导）
- ③外部约束+国情（引 06）
- ④三情景 **基准/上行/下行**，每个给**触发条件 + 关键假设**，并区分近期（2026-27）与十五五期（2026-30）方向
- ⑤可证伪点/观察指标（盯哪些指标知道走哪条情景）
- ⑥劳动者含义（各情景下行业/岗位/技能/区域怎么准备，含负面情形）
结尾指向 `08`（下篇）与 `06`（方法/复盘）。**无个股、无投资建议、无政治预测、无时间表；措辞条件式。**

- [ ] **Step 3: 验证**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f="strategy/economic_policy/07-关键议题推演（上）-内需·房地产·财政与地方债.md"
grep -q "内需\|消费" "$f" && grep -q "房地产" "$f" && grep -q "地方债\|财政" "$f" && echo "OK: 三议题齐"
grep -q "基准" "$f" && grep -q "上行" "$f" && grep -q "下行" "$f" && echo "OK: 三情景齐"
grep -q "触发\|假设" "$f" && grep -q "可证伪\|观察指标" "$f" && echo "OK: 含假设与可证伪"
grep -q "见 04\|04 " "$f" && echo "OK: 引规律库"
grep -qi "http" "$f" && echo "OK: 含来源"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
```
Expected: 三议题齐 / 三情景齐 / 含假设与可证伪 / 引规律库 / 含来源 / 无股票代码.

- [ ] **Step 4: Commit**
```bash
git add "strategy/economic_policy/07-关键议题推演（上）-内需·房地产·财政与地方债.md"
git commit -m "feat: 经济政策专栏 Phase 2——关键议题推演（上）内需·房地产·财政地方债

需求与风险侧三议题，基准/上行/下行三情景+触发条件假设+可证伪点+劳动者含义，调用规律库外推。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: 关键议题推演（下）`08-…新动能·外需出海·人口劳动力.md`

**Files:**
- Create: `strategy/economic_policy/08-关键议题推演（下）-新动能·外需出海·人口劳动力.md`

- [ ] **Step 1: 核实三议题现状锚点**

在线核实议题④AI+新质、⑤外需与出海、⑥人口与劳动力的现状数据（本 plan 顶部锚点 + 最新可查值），每条附官方/权威来源。

- [ ] **Step 2: 写文件**

同 Task 2 的模板与顶部说明（改为供给与结构侧三议题）。对议题④⑤⑥各写一节，六要素：
- 议题④AI+新质：现状（高技术制造+8.9%等）→04 一长周期局部快/04 四创岗→外部约束（科技脱钩/出口管制，引06）→三情景（新动能接棒快慢）→可证伪点（高技术占比、投资、就业）→劳动者含义（用修调机器人、新能源链、技能往难自动化靠）
- 议题⑤外需出海：现状（出口~5%韧性、中美博弈）→04 出海规律 + 06 国际假设→三情景（脱钩深浅/全球南方）→可证伪点（出口增速、对美占比、出海投资）→劳动者含义（出海岗位、跨境、制造迁移）
- 议题⑥人口劳动力：现状（负增长、老龄化、中等收入群体38.86%）→04 长周期 + perspective/02 呼应→三情景（老龄化应对、人力资本）→可证伪点（劳动年龄人口、银发经济、技能溢价）→劳动者含义（养老照护、技能升级、延迟退休应对）
三情景均区分近期与十五五期。结尾指向 `06`（方法/复盘）、`07`（上篇）。**无个股、无投资建议、无政治预测、无时间表；条件式。**

- [ ] **Step 3: 验证**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f="strategy/economic_policy/08-关键议题推演（下）-新动能·外需出海·人口劳动力.md"
grep -q "新质\|新动能\|AI" "$f" && grep -q "外需\|出海\|出口" "$f" && grep -q "人口\|老龄化\|劳动力" "$f" && echo "OK: 三议题齐"
grep -q "基准" "$f" && grep -q "上行" "$f" && grep -q "下行" "$f" && echo "OK: 三情景齐"
grep -q "触发\|假设" "$f" && grep -q "可证伪\|观察指标" "$f" && echo "OK: 含假设与可证伪"
grep -q "见 04\|04 \|perspective" "$f" && echo "OK: 引规律库/前瞻"
grep -qi "http" "$f" && echo "OK: 含来源"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
```
Expected: 三议题齐 / 三情景齐 / 含假设与可证伪 / 引规律库 / 含来源 / 无股票代码.

- [ ] **Step 4: Commit**
```bash
git add "strategy/economic_policy/08-关键议题推演（下）-新动能·外需出海·人口劳动力.md"
git commit -m "feat: 经济政策专栏 Phase 2——关键议题推演（下）新动能·外需出海·人口劳动力

供给与结构侧三议题，三情景+触发假设+可证伪点+劳动者含义，调用规律库与前瞻层。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: 文档同步 + 整体复核

**Files:**
- Modify: `strategy/economic_policy/README.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: `economic_policy/README.md`**

读 README。把 `06`/`07`/`08` 加入"当前文件"表（提要：06=推演方法与外部约束；07=关键议题推演上·内需/房地产/财政地方债；08=关键议题推演下·新动能/外需出海/人口劳动力）。更新 Phase 2 状态：推演内容已建，**引擎接入仍待（再下一轮）**。"后续扩展路线"改为只剩"Phase 2 引擎接入（另开 spec）"+ 推演需定期复盘更新。当前文件表只列真实存在的文件（00–08）。

- [ ] **Step 2: `CHANGELOG.md [未发布]`**

在现有经济政策专栏条目下补一条：Phase 2 推演（知识层）——新增推演方法与外部约束（06）+ 6 个关键议题情景化推演（07/08，基准/上行/下行 + 触发条件/假设/可证伪点/劳动者含义，调用规律库外推）。仍为纯知识内容、未改引擎、不升版本；引擎接入另开 spec。

- [ ] **Step 3: 验证 + 整体复核**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
echo "=== 专栏文件 ===" && ls strategy/economic_policy/
echo "=== 06/07/08 存在 ===" && for n in 06 07 08; do ls strategy/economic_policy/ | grep -q "^$n-" && echo "$n 存在" || echo "缺 $n"; done
echo "=== 无引擎/数据改动 ===" && git diff --stat main..HEAD -- engine/ skills/ && echo "(应为空)"
echo "=== 全专栏无个股 ===" && grep -rEn '\$[A-Z]{2,5}\b' strategy/economic_policy/ || echo "OK: 无股票代码"
echo "=== 无断言式预测词（粗查） ===" && grep -rnE "必将|一定会|肯定会|势必" strategy/economic_policy/0[678]*.md && echo "注意:疑似断言式预测" || echo "OK: 未见断言式预测"
grep -q "推演" strategy/economic_policy/README.md && grep -q "推演\|Phase 2\|情景" CHANGELOG.md && echo "OK: 文档同步"
```
Expected: 06/07/08 存在；engine/skills diff 为空；无股票代码；未见断言式预测；OK: 文档同步.

- [ ] **Step 4: Commit**
```bash
git add strategy/economic_policy/README.md CHANGELOG.md
git commit -m "docs: Phase 2 推演收尾——README 加 06/07/08 + CHANGELOG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review（写完即查）

**1. Spec coverage（对照 spec §4/§5/§6）：**
- 06 推演方法 + 外部约束 + 诚实边界 + 复盘机制（spec §6）→ Task 1 ✅
- 07 议题①②③（spec §4 1-3）→ Task 2 ✅
- 08 议题④⑤⑥（spec §4 4-6）→ Task 3 ✅
- 每议题六要素模板（spec §5）→ Task 2/3 Step 2 ✅
- 三情景+触发条件+假设+可证伪点+劳动者含义（spec §5）→ 验证步骤 ✅
- 调用规律库 04 外推（spec §2/§5）→ 各任务约束 + grep "见04" ✅
- 双时间跨度（spec §2）→ Task 2/3 模板 ✅
- 诚实底线·不预测/不时间表/不投资建议/不政治预测（spec §5/§9/§10）→ 全程约束 + grep 断言词 ✅
- 不动引擎、不升版本（spec §1/§8）→ Task 4 复核 ✅
- README/CHANGELOG 同步（spec §8）→ Task 4 ✅

**2. Placeholder scan：** 每议题给了锚点 + 规律库挂钩 + 来源，并要求在线复核；无 TBD/TODO。六议题模板统一非"同上"占位。✅

**3. 一致性：** 文件名 06/07/08 与 spec §6 一致；六要素模板各任务一致；议题①—⑥ 与 spec §4 一一对应；情景三分（基准/上行/下行）全文一致；一律引 04 + 带来源。✅
