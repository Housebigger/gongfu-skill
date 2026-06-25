# 逐集群行业前景推演（首批 6 集群·知识层）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 扩充经济政策专栏原料库 + 新增 `09-行业前景推演/` 子层，为 6 个高政策敏感集群（C/K/E/G/A/D）各产出一份"政策机制驱动·三情景"行业前景推演（知识层）。

**Architecture:** 把 07/08 的宏观议题推演**下沉**到具体产业集群：先扩原料库（行业政策信源 + 锚点政策），再建方法文件，然后逐集群按统一六要素模板（复用 06 方法 + 04 规律 + 05/06 边界）产出推演，最后更新 README/CHANGELOG。纯知识内容，**不动引擎、不升版本**。

**Tech Stack:** Markdown（中文）。无 pytest / 无构建——"测试"是 doc-based `grep` 校验。内容用 **WebSearch 先搜后确认**，带官方来源；抓不到的标"待核实"，不伪造。

---

## 约定（每个任务都适用）

- **工作目录**：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`。命令在此根下跑。
- **分支**：`feat/policy-industry-forecasts`（已建）。
- **先搜后确认**：行业政策名称、官方数据均以 WebSearch 在线核实为准，引用国家统计局/央行/财政部/各行业主管部门（发改委 ndrc.gov.cn、工信部 miit.gov.cn、能源局 nea.gov.cn、农业农村部 moa.gov.cn、民政部 mca.gov.cn、住建部 mohurd.gov.cn、生态环境部 mee.gov.cn、卫健委 nhc.gov.cn、商务部 mofcom.gov.cn）官方渠道；带链接。抓不到链接的条目正文里标注"（来源待核实）"。
- **内容红线（贯穿全程）**：不出现个股名/证券代码、不给买卖点/仓位/资产配置、不预测政治走势或人事、不评判政策对错；不用 `必将/一定会/建议买入/包涨/稳赚` 等断言/荐股式措辞；政策↔结果用"伴随/在…之后观察到/与…同期"等观察性措辞，不用"由于…导致"。情景一律"若…则…"条件式，给方向不给时间表/点位。
- **无版本变更**：纯知识内容。不改 `engine/`、不改 `skills/`、不动版本号。收尾在 `CHANGELOG.md [未发布]` 累计。

---

## 共用 A：集群文件六要素模板（Task 3–8 都用这一份）

每个集群文件 `strategy/economic_policy/09-行业前景推演/<集群ID>.md` 一律按下面结构写（`<…>` 是该集群的具体内容，由对应任务的"锚点"小节给出 + WebSearch 核实）：

````markdown
# 行业前景推演：<集群ID（如 C-绿色能源全链）>

日期：2026-06-25
主驱动议题：<主驱动议题>（见 `08-关键议题推演（下）` / `07-关键议题推演（上）` 对应议题）
一句话定位：政策机制驱动的逐行业三情景推演——给方向不给时间表，不投资建议、不政治预测。

> **必读边界**：本篇为情景分析、非预言（见 `05-边界与诚实.md` + `06` 第四节 + 本层 `00-方法与边界.md`）。
> **与既有面分工**：`perspective/` 给该领域主题式中长期前瞻；`industry-signals.yaml` 给静态信号卡；本篇给"政策→三情景"的动态推演。

---

## 一、现状锚点
- 该集群当前行业事实 + 锚点政策（引 `03-行业政策锚点-六集群.md`）+ 官方数据（带口径与来源，先搜后确认）。
- 数据时效标"截至成文 2026-06"。

## 二、规律库外推（引 `04-作用规律总结.md`）
- 明确引用 `04` 的哪条规律（时滞分层 / 传导节点 / 就业收入传导）外推本集群；做传导节点检查（配套财政信贷？部门分工考核？落到价格/产能/岗位/收入？）。

## 三、外部约束与国情（引 `06-推演方法与外部约束.md`）
- 套 `06` 第二/三节国际/国情共用假设，对本集群做顺风 / 逆风 / 待观察的方向定性（只定性、不量化）。

## 四、三情景：基准 / 上行 / 下行
- 表格：每情景给「触发条件（可观察指标）｜关键假设｜对劳动者方向含义」；一律"若…则…"，不给时间表点位。

## 五、可证伪点与观察指标
- 2–4 个官方可查指标，说明"看到什么数据说明在走哪条情景"，区分规律前提失效信号 vs 下行情景触发信号。

## 六、劳动者含义
- 落到岗位/技能/区域/卡位窗口；挂 `skills/data/industry-signals.yaml` 本集群的 growth_roles / shrink_roles + 产业链卡点（Serenity）思路；含"下行信号出现时留意什么"；不承诺一定涨薪/一定有工作；末句提示"这是方向判断，不是你的个人职业规划"。

---

*截至成文 2026-06-25。外部假设有时效，按 `06` 第五节复盘机制定期更新。*
````

## 共用 B：单个集群文件的验证脚本（Task 3–8 都用，替换 `F` 即可）

```bash
F="strategy/economic_policy/09-行业前景推演/<集群ID>.md"
test -f "$F" || { echo "!! 文件不存在: $F"; exit 1; }
for kw in 现状锚点 规律库外推 外部约束 三情景 基准 上行 下行 可证伪点 劳动者含义; do
  grep -q "$kw" "$F" || echo "缺要素: $kw"
done
grep -q '关键议题推演' "$F" || echo "缺 07/08 交叉引用"
grep -q '作用规律'     "$F" || echo "缺 04 规律引用"
grep -q 'industry-signals\|growth_roles\|岗位' "$F" || echo "缺劳动者岗位落点"
grep -nE '必将|一定会|建议买入|包涨|稳赚' "$F" && echo "!! 断言/荐股式措辞"
grep -nF '$' "$F" && echo "!! 出现 \$ 符号"
echo "--- 人工复核：① 官方来源链接齐全/待核实已标注 ② 情景为条件式 ③ 若有6位数字确认非个股代码 ---"
echo "(上面若无 '缺…' / '!!' 行即自动校验通过)"
```

---

## Task 1: 原料库扩充（信源清单 + 行业政策锚点）

**Files:**
- Modify: `strategy/references/policy_archive/00-信源清单.md`（新增"行业政策信源"段）
- Create: `strategy/references/policy_archive/03-行业政策锚点-六集群.md`

**本任务先做**——后续 6 个集群文件都引用 `03` 的锚点政策。

- [ ] **Step 1: WebSearch 核实 6 集群的锚点政策与官方来源**

用 WebSearch 逐集群核实下列锚点政策的**现行官方名称 + 发布部门 + 链接**（每集群 2–3 条；以下为待核实的检索起点）：
- **C 绿色能源全链**：碳达峰碳中和"1+N"政策体系；构建新型电力系统/新型能源体系（来源：发改委、能源局）。
- **K 传统重化工与建材**：重点行业节能降碳改造、超低排放改造、产能治理/过剩产能（来源：发改委、工信部、生态环境部）。
- **E 民生服务**：基本养老服务体系/基本养老服务清单、积极应对人口老龄化国家战略、普惠托育、医养结合（来源：民政部、卫健委、发改委）。
- **G 基建物流房地产**：超长期特别国债与"两重"建设、新型城镇化、城市更新、保交楼/收购存量商品房、地方化债"6+4+2"（来源：发改委、住建部、财政部）。
- **A 先进制造与硬科技**：制造业数字化转型、专精特新、新质生产力、工业母机/首台套（来源：工信部、发改委）。
- **D 农业与乡村振兴**：乡村全面振兴、粮食安全（藏粮于地藏粮于技）、高标准农田、种业振兴（来源：农业农村部、中央一号文件）。

- [ ] **Step 2: 扩 `00-信源清单.md` —— 新增"行业政策信源"段**

先 Read `strategy/references/policy_archive/00-信源清单.md`，在文末追加一节，列出本轮 6 集群相关的**行业主管部门官方渠道**（机构名 + 官网域名 + 该机构对应哪些集群），以及检索到的具体行业政策文件条目（名称 + 链接，抓不到标"（链接待核实）"）。格式与文件现有信源条目一致。

- [ ] **Step 3: 创建 `03-行业政策锚点-六集群.md`**

按 6 集群分节，每集群列 2–3 条锚点政策，每条：`政策名称`（发布部门·年份）— 一句话政策要点 — 来源链接（或"待核实"）。开头写一句说明："本文件是 `09-行业前景推演/` 各集群推演的政策原料锚点，先搜后确认，只录官方政策与要点，不含个股、不含推演结论。"

- [ ] **Step 4: 验证**

```bash
test -f strategy/references/policy_archive/03-行业政策锚点-六集群.md || echo "!! 03 缺失"
for c in 绿色能源 重化工 民生 基建 先进制造 农业; do grep -q "$c" strategy/references/policy_archive/03-行业政策锚点-六集群.md || echo "锚点缺集群: $c"; done
grep -q '行业政策信源' strategy/references/policy_archive/00-信源清单.md || echo "!! 信源清单未加行业政策信源段"
grep -nE '必将|一定会|建议买入|包涨|稳赚' strategy/references/policy_archive/03-行业政策锚点-六集群.md && echo "!! 红线措辞"
echo "(无 '!!'/'缺' 即通过；人工核对来源链接)"
```

- [ ] **Step 5: 提交**

```bash
git add strategy/references/policy_archive/00-信源清单.md strategy/references/policy_archive/03-行业政策锚点-六集群.md
git commit -m "feat(strategy): 原料库扩充——行业政策信源 + 六集群锚点政策（先搜后确认）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: `09-行业前景推演/` 方法与边界文件

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/00-方法与边界.md`

- [ ] **Step 1: 撰写方法文件**

先 Read `strategy/economic_policy/06-推演方法与外部约束.md`（六要素 + 边界）与 `05-边界与诚实.md`，再创建 `09-行业前景推演/00-方法与边界.md`，内容包含：
1. **本层定位**：把 07/08 宏观议题推演"下沉"到具体产业集群；与 `perspective/`（主题前瞻）、`industry-signals.yaml`（静态卡）的分工。
2. **下沉方法**：单集群推演如何套用 `06` 六要素 + 引 `04` 规律；每集群须显式锚定其主驱动的 07/08 议题。
3. **逐行业推演专属诚实边界**：情景非预言/给方向不给时间表/不投资建议/不个股/不政治预测/观察性关联非因果；明确"本层结论继承 06/05 全部边界"。
4. **本轮覆盖与扩展**：首批 6 集群（C/K/E/G/A/D），其余 10 个分批；按 `06` 第五节复盘机制更新。

- [ ] **Step 2: 验证**

```bash
F=strategy/economic_policy/09-行业前景推演/00-方法与边界.md
test -f "$F" || echo "!! 缺文件"
for kw in 下沉 六要素 情景非预言 不投资建议 不政治预测 perspective industry-signals; do grep -q "$kw" "$F" || echo "缺: $kw"; done
echo "(无 '!!'/'缺' 即通过)"
```

- [ ] **Step 3: 提交**

```bash
git add strategy/economic_policy/09-行业前景推演/00-方法与边界.md
git commit -m "feat(strategy): 09行业前景推演——方法与边界（宏观议题下沉法 + 逐行业诚实边界）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: C-绿色能源全链 前景推演

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/C-绿色能源全链.md`

**集群锚点（写作依据，须 WebSearch 核实数据/来源）：**
- **主驱动议题**：双碳 + 新动能（见 `08`）。基调：**顺风**，后市场（运维/回收/碳管理）被低估。
- **锚点政策**（引 Task 1 的 `03`）：双碳"1+N"；新型电力系统/新型能源体系；新能源占比逐步提高。
- **04 规律**：长周期慢变量（双碳 35 年）+ "提前 2–4 年卡位"时滞规律。
- **industry-signals roles**（读 `skills/data/industry-signals.yaml` 的 `C-绿色能源全链`）：growth=储能系统工程师/电网电力系统/电站运维/碳资产管理；shrink=光伏组件低端产能、电池片低端产能。
- **搜索目标**：2025–2026 风光装机/新增装机、储能装机、新能源发电占比（国家能源局）；双碳"1+N"现行表述。

- [ ] **Step 1: WebSearch 核实** 上述数据与政策来源。
- [ ] **Step 2: 写文件** 按【共用 A】模板，填入本集群锚点内容。
- [ ] **Step 3: 验证** 用【共用 B】脚本，`F=strategy/economic_policy/09-行业前景推演/C-绿色能源全链.md`，无 `缺`/`!!` 输出。
- [ ] **Step 4: 提交**
```bash
git add strategy/economic_policy/09-行业前景推演/C-绿色能源全链.md
git commit -m "feat(strategy): 行业前景推演 C-绿色能源全链（政策驱动三情景·知识层）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: K-传统重化工与建材 前景推演

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/K-传统重化工与建材.md`

**集群锚点：**
- **主驱动议题**：双碳（逆风）+ 房地产需求（见 `07`）。基调：**逆风/转型压力**。
- **锚点政策**：重点行业节能降碳改造、超低排放改造、过剩产能治理。
- **04 规律**：供给侧改革规律（见 `02`）+ 房地产下行对建材需求的传导（见 `07`）。
- **industry-signals roles**（读 `industry-signals.yaml` 的 `K-传统重化工与建材`）：按文件实际填；典型 shrink=低端钢铁/水泥产能，growth/转型=绿色冶炼/节能改造/工艺升级岗。
- **搜索目标**：2025–2026 粗钢/水泥产量与价格、行业利润、超低排放/节能降碳现行政策（统计局、工信部、生态环境部）。

- [ ] **Step 1: WebSearch 核实**。
- [ ] **Step 2: 写文件**（【共用 A】模板）。
- [ ] **Step 3: 验证**（【共用 B】，`F=…/K-传统重化工与建材.md`）。
- [ ] **Step 4: 提交**
```bash
git add strategy/economic_policy/09-行业前景推演/K-传统重化工与建材.md
git commit -m "feat(strategy): 行业前景推演 K-传统重化工与建材（政策驱动三情景·知识层）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: E-民生服务 前景推演

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/E-民生服务.md`

**集群锚点：**
- **主驱动议题**：人口老龄化（见 `08`）+ 共同富裕。基调：**结构性顺风**。
- **锚点政策**：基本养老服务体系/清单、积极应对人口老龄化国家战略、普惠托育、医养结合。
- **04 规律**：长周期慢变量（人口）+ 银发经济长周期增量（见 `04` 第一节）。
- **industry-signals roles**（读 `industry-signals.yaml` 的 `E-民生服务`）：按文件实际填；典型 growth=养老护理/医养/托育/健康服务。
- **搜索目标**：2025 末 65 岁以上占比、老年人口、养老床位/护理人才缺口、普惠托育位（统计局、民政部、卫健委）。

- [ ] **Step 1: WebSearch 核实**。
- [ ] **Step 2: 写文件**（【共用 A】模板）。
- [ ] **Step 3: 验证**（【共用 B】，`F=…/E-民生服务.md`）。
- [ ] **Step 4: 提交**
```bash
git add strategy/economic_policy/09-行业前景推演/E-民生服务.md
git commit -m "feat(strategy): 行业前景推演 E-民生服务（政策驱动三情景·知识层）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: G-基建物流房地产 前景推演

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/G-基建物流房地产.md`

**集群锚点：**
- **主驱动议题**：财政与地方债（见 `07`）+ 房地产（见 `07`）。基调：**分化**（基建顺风 / 地产承压）。
- **锚点政策**：超长期特别国债与"两重"建设、新型城镇化、城市更新、保交楼/收储、化债"6+4+2"。
- **04 规律**：中等时滞（专项债→施工用工高峰 6–18 月）+ 房地产直接就业偏弱（见 `04` / `07`）。
- **industry-signals roles**（读 `industry-signals.yaml` 的 `G-基建物流房地产`）：按文件实际填；典型 growth=物流/基建施工（看财政），承压=房地产开发。
- **搜索目标**：2025–2026 基建投资增速、专项债/特别国债规模、70 城房价、商品房销售面积（统计局、财政部）。

- [ ] **Step 1: WebSearch 核实**。
- [ ] **Step 2: 写文件**（【共用 A】模板）。
- [ ] **Step 3: 验证**（【共用 B】，`F=…/G-基建物流房地产.md`）。
- [ ] **Step 4: 提交**
```bash
git add strategy/economic_policy/09-行业前景推演/G-基建物流房地产.md
git commit -m "feat(strategy): 行业前景推演 G-基建物流房地产（政策驱动三情景·知识层）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: A-先进制造与硬科技 前景推演

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/A-先进制造与硬科技.md`

**集群锚点：**
- **主驱动议题**：新动能 + 外需出海/中美博弈（见 `08`）。基调：**政策顺风 + 外部（科技管制）约束**。
- **锚点政策**：制造业数字化转型、专精特新、新质生产力、工业母机/首台套。
- **04 规律**：新质生产力长周期 + "提前卡位"时滞；外部约束套 `06` 中美博弈假设。
- **industry-signals roles**（读 `industry-signals.yaml` 的 `A-先进制造与硬科技`）：按文件实际填；典型 growth=高端装备/工业软件/嵌入式，承压=低端代工。
- **搜索目标**：2025–2026 制造业投资/高技术制造业增加值增速、专精特新企业数、半导体/工业母机国产化进展（统计局、工信部）。

- [ ] **Step 1: WebSearch 核实**。
- [ ] **Step 2: 写文件**（【共用 A】模板）。
- [ ] **Step 3: 验证**（【共用 B】，`F=…/A-先进制造与硬科技.md`）。
- [ ] **Step 4: 提交**
```bash
git add strategy/economic_policy/09-行业前景推演/A-先进制造与硬科技.md
git commit -m "feat(strategy): 行业前景推演 A-先进制造与硬科技（政策驱动三情景·知识层）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: D-农业与乡村振兴 前景推演

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/D-农业与乡村振兴.md`

**集群锚点：**
- **主驱动议题**：乡村振兴 + 粮食安全。基调：**政策托底、慢变量**。
- **锚点政策**：乡村全面振兴、粮食安全（藏粮于地藏粮于技）、高标准农田、种业振兴。
- **04 规律**：长周期 + 政策托底传导（财政补贴直达）。
- **industry-signals roles**（读 `industry-signals.yaml` 的 `D-农业与乡村振兴`）：按文件实际填；典型 growth=农技/农机/种业/农产品流通。
- **搜索目标**：2025–2026 粮食产量、高标准农田面积、农村居民收入增速、中央一号文件要点（统计局、农业农村部）。

- [ ] **Step 1: WebSearch 核实**。
- [ ] **Step 2: 写文件**（【共用 A】模板）。
- [ ] **Step 3: 验证**（【共用 B】，`F=…/D-农业与乡村振兴.md`）。
- [ ] **Step 4: 提交**
```bash
git add strategy/economic_policy/09-行业前景推演/D-农业与乡村振兴.md
git commit -m "feat(strategy): 行业前景推演 D-农业与乡村振兴（政策驱动三情景·知识层）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: 子层 README + 上层 README 更新 + CHANGELOG

**Files:**
- Create: `strategy/economic_policy/09-行业前景推演/README.md`
- Modify: `strategy/economic_policy/README.md`
- Modify: `strategy/references/policy_archive/README.md`
- Modify: `CHANGELOG.md`（`[未发布]` 段）

- [ ] **Step 1: 创建子层 README**

`09-行业前景推演/README.md`：本层定位（政策驱动逐集群三情景，下沉自 07/08）+ 与 perspective/industry-signals 的分工 + **已做/待做集群表**（已做：C/K/E/G/A/D；待做：B/F/H/I/J/L/M/N/O/P）+ 边界指引（指向 `00-方法与边界` 与 `05`/`06`）。

- [ ] **Step 2: 更新 `strategy/economic_policy/README.md`**

先 Read。在"五、当前文件"表后或"六、后续扩展路线"处，加入 `09-行业前景推演/` 层条目（说明：把 07/08 宏观议题下沉到具体集群；首批 6 集群已建，其余分批）。

- [ ] **Step 3: 更新 `strategy/references/policy_archive/README.md`**

先 Read。注明信源清单已扩"行业政策信源"段、新增 `03-行业政策锚点-六集群.md`。

- [ ] **Step 4: 更新 `CHANGELOG.md [未发布]`**

先 Read。在 `## [未发布]` 段下新增一条（纯知识内容）：

```
### 新增 Added（纯知识内容，随下次发版一并记录）

- **经济政策专栏新增「逐集群行业前景推演」层（首批 6 集群·知识层）**。把 07/08 宏观议题推演下沉到具体产业集群：原料库扩充行业政策信源 + 六集群锚点政策（`policy_archive/00`、新增 `03`）；新增 `economic_policy/09-行业前景推演/`（方法与边界 `00` + C/K/E/G/A/D 六集群文件），每集群按 06 六要素法给基准/上行/下行三情景，含触发条件、关键假设、可证伪点与劳动者含义，数据带官方来源、先搜后确认。情景为方向研判非预言，不个股、不政治预测。纯知识内容、未改引擎、不升版本；其余 10 集群与引擎接入另开 spec。
```

> 注：若 `[未发布]` 下已无"### 新增 Added（纯知识内容…）"子标题（上一版发布时清空过），就新建该子标题再加条目；若已存在则在其下追加本条。

- [ ] **Step 5: 验证**

```bash
test -f strategy/economic_policy/09-行业前景推演/README.md || echo "!! 子层README缺"
grep -q '09-行业前景推演\|行业前景推演' strategy/economic_policy/README.md || echo "!! 上层README未提09层"
grep -q '03-行业政策锚点\|行业政策信源' strategy/references/policy_archive/README.md || echo "!! 原料库README未更新"
grep -q '逐集群行业前景推演\|行业前景推演' CHANGELOG.md || echo "!! CHANGELOG未加条目"
ls strategy/economic_policy/09-行业前景推演/*.md | wc -l   # 期望 8（README + 00 + 6 集群）
echo "--- 确认不动引擎/不升版本 ---"
git diff --stat main..HEAD -- engine/ skills/ pyproject.toml engine/plugin.yaml api_server/server.py | grep . && echo "!! 误改了引擎/版本文件" || echo "engine/skills/版本 未改 OK"
```
Expected: `8`，且最后一行打印 `engine/skills/版本 未改 OK`，无 `!!`。

- [ ] **Step 6: 提交**

```bash
git add strategy/economic_policy/09-行业前景推演/README.md strategy/economic_policy/README.md strategy/references/policy_archive/README.md CHANGELOG.md
git commit -m "docs: 09行业前景推演子层README + 上层README/原料库README + CHANGELOG[未发布]

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review（写完计划后的自检）

**Spec 覆盖：**
- spec §4 原料库扩充（信源 + 03 锚点）→ Task 1 ✅
- spec §5 分析池新层（09 子层 + 00 方法 + 6 集群文件，六要素模板）→ Task 2（方法）+ Task 3–8（6 集群，共用 A 模板）✅
- spec §5.2 六集群↔议题锚定 → 每个集群任务的"集群锚点·主驱动议题"✅
- spec §6 诚实纪律 → 共用约定的红线 + 共用 A 模板的边界块 + 共用 B 的红线 grep ✅
- spec §7 README/CHANGELOG/不升版本 → Task 9 ✅
- spec §8 验证（六要素齐全/条件式/红线/交叉引用 07-08/官方来源/不动引擎）→ 共用 B + Task 9 Step 5 ✅
- spec §9 非目标（不引擎接入/只 6 集群/不重复 perspective·signals）→ 计划未含相关改动；共用 A 模板含"与既有面分工"块 ✅

**Placeholder 扫描：** 无 TBD/TODO。内容任务给的是**模板 + 该集群锚点 + 搜索目标 + 验证脚本**（先搜后确认要求内容在执行时检索，不能预写死，这是设计决策，非占位符）。✅

**一致性：** 文件路径全程 `strategy/economic_policy/09-行业前景推演/<集群ID>.md`；集群 ID（C-绿色能源全链 等）与引擎/cluster_frameworks 命名一致；六要素小节名（现状锚点/规律库外推/外部约束/三情景/可证伪点/劳动者含义）在共用 A 模板与共用 B 验证里一致。✅

**执行提示（给控制器）：** 派发 Task 3–8 的实现 subagent 时，把【共用 A 模板】+【共用 B 验证】+ 该任务的"集群锚点"一并贴进 prompt（subagent 不读本计划文件）。Task 3–8 内容互相独立，但仍按 subagent-driven 串行执行（不并发实现 subagent）。每个集群 subagent 需用 WebSearch。
