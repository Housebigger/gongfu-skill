# 华为韬定律 → 半导体产业发展逻辑与方向研究 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在战略库新增"华为韬（τ）定律 → 半导体产业发展逻辑与方向"独立研究专题：搜集论文/资料建原料库，再据此情景化推演半导体产业未来方向，并落到一线劳动者。

**Architecture:** 镜像 Serenity 模式——`strategy/references/huawei_tau/`（原料库，先搜后确认）+ `strategy/semiconductor_outlook/`（劳动者版提炼/预测：韬定律是什么 → 产业逻辑 → 未来方向情景推演 → 对劳动者含义 → 边界）。纯知识内容，不动引擎、不升版本。诚实三分陈述（事实/主张/预测）+ 情景非预言 + 中立贯穿全程。

**Tech Stack:** Markdown（中文）。无 pytest/无构建——"测试"是 doc-based `grep`/文件检查。内容用 **WebSearch 先搜后确认**，带权威来源；抓不到标"待核实"，不伪造。

---

## 约定（每个任务都适用）

- **工作目录**：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`。命令在此根下跑。
- **分支**：`feat/huawei-tau-semiconductor-outlook`（已建）。
- **先搜后确认**：load WebSearch/WebFetch via `ToolSearch select:WebSearch,WebFetch`。权威来源优先：华为官网 huawei.com、IEEE（ISCAS / ieeexplore）、新华网 news.cn、求是网 qstheory.cn、观察者网 guancha.cn、人民网、权威科技/半导体媒体（IT之家、21经济网、财联社、半导体行业观察等）。抓不到可靠链接 → 正文标"（来源待核实）"，绝不伪造 URL 或数字。
- **诚实三分陈述（强制）**：凡涉及韬定律/半导体进展的陈述，标注属于 **①已发生/可核实** / **②厂商主张/方法论** / **③远期预测/目标** 中的哪类，不混淆。
- **中立红线（贯穿全程）**：不用 `伟大/必将/遥遥领先/碾压/吊打/秒杀/完爆` 等吹捧或贬低式措辞，不站队；不出个股/证券代码、不给 `建议买入/投资建议/目标价/买卖点`、不预测股价。预测部分一律情景条件式（"若…则…"），给方向不给时间表/点位。
- **无版本变更**：纯知识内容，不改 `engine/`、`skills/`、版本号。收尾在 `CHANGELOG.md [未发布]` 累计。

## 共用：单文件中立/红线验证脚本（替换 `F`）

```bash
F="<目标文件路径>"
test -f "$F" || { echo "!! 文件不存在: $F"; exit 1; }
grep -nE '伟大|必将|遥遥领先|碾压|吊打|秒杀|完爆' "$F" && echo "!! 吹捧/贬低式措辞" || echo "中立 OK"
grep -nE '建议买入|投资建议|目标价|买入评级|加仓|减仓' "$F" && echo "!! 投资建议" || echo "无投资建议 OK"
grep -nF '$' "$F" && echo "!! 出现 \$ 符号" || echo "无\$ OK"
echo "(无 '!!' 即通过)"
```

---

## Task 1: 原料库 `strategy/references/huawei_tau/`（先搜后确认）

**Files:**
- Create: `strategy/references/huawei_tau/00-信源清单.md`
- Create: `strategy/references/huawei_tau/01-韬定律原文与权威解读.md`
- Create: `strategy/references/huawei_tau/02-背景资料.md`

**本任务先做**——后续提炼/预测都引用本原料库。

- [ ] **Step 1: WebSearch 搜集核实**（检索起点）
  - 韬定律本体：华为官网 ISCAS 2026 韬(τ)定律发布、何庭波 ISCAS 论文要点（"时间缩微/τ scaling"、逻辑折叠 logic folding）、新华网/求是网/观察者网解读；已量产 381 款芯片、麒麟 2026 秋逻辑折叠、2031 年 1.4nm 同等密度预测。
  - 背景：摩尔定律放缓现状；先进制程与 EGA/光刻/EDA/设备封锁（出口管制）；中国半导体国产替代进展（设计/制造/封测/设备/材料/EDA 各环节）。
  - 每条记录：标题 — 发布方/日期 — 一句要点 — 链接（抓不到标"（链接待核实）"）。

- [ ] **Step 2: 写 `00-信源清单.md`** —— 分两组（韬定律本体信源 / 半导体产业背景信源），逐条 机构·日期 + 链接 + 一句要点。开头一句说明：本清单是本专题原料信源，先搜后确认，抓不到只登记。

- [ ] **Step 3: 写 `01-韬定律原文与权威解读.md`** —— 韬定律核心内容（时间缩微 vs 几何缩微、逻辑折叠、多层级协同）+ 何庭波 ISCAS 要点 + 官方/权威媒体解读。**每条陈述标注 ①事实/②主张/③预测**；带来源。开头声明：只录原文与权威解读、不含本专题推演结论。

- [ ] **Step 4: 写 `02-背景资料.md`** —— 摩尔定律放缓 / 先进制程与设备·EDA·光刻封锁 / 国产替代各环节进展。带官方或权威来源；数据标口径与时间；抓不到标"待核实"。这是预测的事实底座。

- [ ] **Step 5: 验证**
```bash
for f in 00-信源清单 01-韬定律原文与权威解读 02-背景资料; do
  F="strategy/references/huawei_tau/$f.md"; test -f "$F" || echo "!! 缺 $f"
  grep -nE '伟大|必将|遥遥领先|碾压|吊打' "$F" && echo "!! 吹捧措辞 $f"
done
grep -q '①\|事实' "strategy/references/huawei_tau/01-韬定律原文与权威解读.md" && echo "01 含三分标注 OK" || echo "!! 01 缺三分标注"
echo "(无 '!!' 即通过；人工核对来源链接齐全/待核实已标)"
```

- [ ] **Step 6: 提交**
```bash
git add strategy/references/huawei_tau/
git commit -m "feat(strategy): 韬定律研究原料库——信源清单+原文权威解读+半导体背景资料（先搜后确认）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: `semiconductor_outlook/00-韬定律是什么.md`（技术原理说人话）

**Files:** Create `strategy/semiconductor_outlook/00-韬定律是什么.md`

先 Read `strategy/references/huawei_tau/01-韬定律原文与权威解读.md`（引用其内容，不重复搜集；如缺细节可补 WebSearch）。

- [ ] **Step 1: 写文件** —— 用大白话讲清：
  - 摩尔定律的"几何缩微"（拼制程纳米数）为何放缓 / 受封锁；
  - 韬定律的"时间缩微（τ）"是什么——衡量从"几纳米"转向"完成一项任务要多少时间"，靠逻辑折叠 + 器件/电路/芯片/系统多层级协同压缩时延、提密度；
  - 为何能在先进制程受限下另辟路径（绕开单一制程封锁）；
  - **三分陈述**：哪些是已发生事实（381 款已量产、ISCAS 发表）、哪些是华为主张的方法论、哪些是远期预测（2031）。
  - 头部加必读边界块（指向 `04-边界与诚实.md` + `references/huawei_tau`）。

- [ ] **Step 2: 验证**（共用脚本，`F=strategy/semiconductor_outlook/00-韬定律是什么.md`）+ `grep -q '时间缩微\|τ' "$F"` 与 `grep -q '事实\|主张\|预测' "$F"`。无 `!!`。

- [ ] **Step 3: 提交**
```bash
git add strategy/semiconductor_outlook/00-韬定律是什么.md
git commit -m "feat(strategy): 半导体前瞻 00-韬定律是什么（技术原理说人话+三分陈述）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: `semiconductor_outlook/01-半导体产业发展逻辑.md`

**Files:** Create `strategy/semiconductor_outlook/01-半导体产业发展逻辑.md`

先 Read `00-韬定律是什么.md` + `references/huawei_tau/02-背景资料.md`。

- [ ] **Step 1: 写文件** —— 韬定律如何**重构产业逻辑**：
  - 从"单一制程尺寸竞赛"→"系统级协同 / 时间维度优化"的范式转移意味着什么（对设计、封装、EDA、设备的影响重心变化）；
  - 中国方案在全球半导体格局中的位置 / 与摩尔定律的关系（是替代、补充还是并行路径——中立陈述，标注主张 vs 共识）；
  - 这套逻辑成立/不成立分别依赖什么（为后续情景推演埋下假设）。
  - 中立：客观比较，不吹捧不贬低；三分陈述标注。

- [ ] **Step 2: 验证**（共用脚本，`F=…/01-半导体产业发展逻辑.md`）+ `grep -q '摩尔\|系统级\|缩微' "$F"`。无 `!!`。

- [ ] **Step 3: 提交**
```bash
git add strategy/semiconductor_outlook/01-半导体产业发展逻辑.md
git commit -m "feat(strategy): 半导体前瞻 01-产业发展逻辑（韬定律范式转移·中立）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: `semiconductor_outlook/02-未来方向情景推演.md`（**预测核心·纪律最严**）

**Files:** Create `strategy/semiconductor_outlook/02-未来方向情景推演.md`

先 Read `01-半导体产业发展逻辑.md`、`references/huawei_tau/02-背景资料.md`，并参考 `strategy/economic_policy/06-推演方法与外部约束.md` 的情景纪律（给方向不给时间表 + 可证伪点）与 `09-行业前景推演/00-方法与边界.md`。

- [ ] **Step 1: 写文件** —— 半导体产业未来方向的**情景化推演**：
  - **现状锚点**（已发生事实，带来源）；
  - **三情景**（基准 / 上行 / 下行，或多路径），每条带：触发条件（可观察指标）+ 关键假设 + 方向含义；一律"若…则…"，**不给时间表/点位**；
  - **可证伪观察指标（2–4 个）**：如先进制程良率与产能、EDA/设备/材料国产化率、Chiplet/先进封装放量、韬定律/系统级路线被同行采纳程度、AI 算力需求对架构的牵引；
  - **三分陈述全程标注**（情景假设属②主张/③预测，须显式区分于①事实）；
  - 头部必读边界块（情景非预言，指向 `04`）。

- [ ] **Step 2: 验证**（共用脚本，`F=…/02-未来方向情景推演.md`）+:
```bash
F=strategy/semiconductor_outlook/02-未来方向情景推演.md
grep -q '若' "$F" && echo "条件式 OK" || echo "!! 缺条件式"
grep -qE '基准|上行|下行|情景' "$F" && echo "情景 OK" || echo "!! 缺情景"
grep -q '可证伪\|观察指标' "$F" && echo "可证伪点 OK" || echo "!! 缺可证伪点"
grep -nE '20[0-9]{2} *年.*(实现|达到|将达)|第[一二三四]季度.*达' "$F" && echo "!! 疑似时间表/点位预测" || echo "无时间表点位 OK"
```
无 `!!`（最后一项若命中需改为方向性条件式表述）。

- [ ] **Step 3: 提交**
```bash
git add strategy/semiconductor_outlook/02-未来方向情景推演.md
git commit -m "feat(strategy): 半导体前瞻 02-未来方向情景推演（情景非预言+可证伪点+三分陈述）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: `semiconductor_outlook/03-对劳动者的含义.md`（**落点**）

**Files:** Create `strategy/semiconductor_outlook/03-对劳动者的含义.md`

先 Read `02-未来方向情景推演.md`、`strategy/economic_policy/09-行业前景推演/A-先进制造与硬科技.md`、`skills/data/industry-signals.yaml`（A 集群 growth/shrink roles）。

- [ ] **Step 1: 写文件** —— 把产业逻辑/未来方向翻译成一线劳动者可用：
  - 半导体链条各环节（芯片设计/EDA/封测/设备/材料/国产替代）的**岗位机会、技能卡位、窗口判断**；
  - 哪些方向是结构性增量、哪些承压；不同情景下劳动者怎么准备（含"下行信号出现时留意什么"）；
  - **挂回** `09-行业前景推演/A-先进制造与硬科技.md` 与 industry-signals A 集群 roles；
  - 诚实：不承诺"一定涨薪/一定有岗"；门槛/不确定如实说；末句留退路"这是方向判断，不是你的个人职业规划"。

- [ ] **Step 2: 验证**（共用脚本，`F=…/03-对劳动者的含义.md`）+ `grep -q '岗位\|技能\|卡位' "$F"` 与 `grep -q 'A-先进制造\|industry-signals\|A 集群' "$F"`。无 `!!`。

- [ ] **Step 3: 提交**
```bash
git add strategy/semiconductor_outlook/03-对劳动者的含义.md
git commit -m "feat(strategy): 半导体前瞻 03-对劳动者的含义（链条岗位/技能卡位·挂A集群）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: `semiconductor_outlook/04-边界与诚实.md`

**Files:** Create `strategy/semiconductor_outlook/04-边界与诚实.md`

先 Read `strategy/economic_policy/05-边界与诚实.md`（承接其中立/诚实风格，不复制）。

- [ ] **Step 1: 写文件** —— 本专题诚实边界：
  - **三分陈述原则**（①事实/②主张/③预测，全程标注）；
  - **情景非预言**（给方向不给时间表/点位）；
  - **中立**（只录可查事实与权威解读，不吹捧不贬低、不站队；区分"华为主张"与"行业共识"）；
  - **不投资建议、不出个股、不预测股价**；
  - 题材时效性（2026-05 新发布，按需复盘更新）；
  - 与 `references/huawei_tau` 原料、`economic_policy/05·06` 推演边界的衔接。

- [ ] **Step 2: 验证**（共用脚本，`F=…/04-边界与诚实.md`）+ `grep -qE '事实.*主张.*预测|三分|①.*②.*③' "$F"` 与 `grep -q '情景非预言\|不预言\|不给时间表' "$F"`。无 `!!`。

- [ ] **Step 3: 提交**
```bash
git add strategy/semiconductor_outlook/04-边界与诚实.md
git commit -m "feat(strategy): 半导体前瞻 04-边界与诚实（三分陈述+情景非预言+中立）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: README + CHANGELOG

**Files:**
- Create: `strategy/semiconductor_outlook/README.md`
- Modify: `strategy/references/huawei_tau/` 下加 `README.md`（原料库索引，可选但建议）
- Modify: `CHANGELOG.md`（`[未发布]` 段）
- Modify: `strategy/README.md`（若其列了子层清单，则补本专题；先 Read 确认是否需要）

- [ ] **Step 1: 写 `semiconductor_outlook/README.md`** —— 专题定位（韬定律→半导体产业逻辑与未来方向，落到劳动者）+ 与既有层分工（A 集群前景 09 / perspective / 经济政策专栏）+ 诚实边界指引（指向 `04` + `references/huawei_tau`）+ 文件索引（00–04）。

- [ ] **Step 2: 写 `strategy/references/huawei_tau/README.md`** —— 原料库索引（00/01/02 各一句）+ "只录原料、不含推演结论"声明。

- [ ] **Step 3: 更新 `CHANGELOG.md [未发布]`** —— 先 Read。`[未发布]` 段当前为空（无 `### 新增 Added` 子标题则新建）。加一条：
```
### 新增 Added（纯知识内容，不升版本）

- **战略库新增「华为韬（τ）定律 → 半导体产业发展逻辑与方向」研究专题（知识层）**。原料库 `strategy/references/huawei_tau/`（信源清单 + 韬定律原文权威解读 + 半导体背景资料，先搜后确认带权威来源）；提炼/预测 `strategy/semiconductor_outlook/`（00 韬定律是什么 → 01 产业发展逻辑 → 02 未来方向情景推演 → 03 对劳动者的含义 → 04 边界与诚实）。全程诚实三分陈述（事实/厂商主张/远期预测），预测为情景非预言（给方向不给时间表 + 可证伪点），严格中立、不个股、不投资建议；落点在半导体链条劳动者的岗位与技能卡位。纯知识内容、未改引擎、不升版本。
```

- [ ] **Step 4: 检查 `strategy/README.md`** —— 先 Read；若其维护子层/专题清单，则补入本专题一行；若无此清单则跳过（不强加）。

- [ ] **Step 5: 验证**
```bash
test -f strategy/semiconductor_outlook/README.md || echo "!! 专题README缺"
ls strategy/semiconductor_outlook/*.md | wc -l   # 期望 6（README + 00..04）
ls strategy/references/huawei_tau/*.md | wc -l    # 期望 4（README + 00/01/02）
grep -q '韬（τ）定律\|韬定律.*半导体\|semiconductor_outlook\|半导体产业发展逻辑' CHANGELOG.md || echo "!! CHANGELOG未加条目"
echo "--- 确认不动引擎/不升版本 ---"
git diff --stat main..HEAD -- engine/ skills/ pyproject.toml engine/plugin.yaml api_server/server.py | grep . && echo "!! 误改引擎/版本" || echo "engine/skills/版本 未改 OK"
```
Expected: `6` 与 `4`；无 `!!`；末行 `engine/skills/版本 未改 OK`。

- [ ] **Step 6: 提交**
```bash
git add strategy/semiconductor_outlook/README.md strategy/references/huawei_tau/README.md CHANGELOG.md strategy/README.md 2>/dev/null; git add -A strategy/ CHANGELOG.md
git commit -m "docs: 半导体前瞻专题 README×2 + CHANGELOG[未发布]（韬定律半导体研究）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review（写完计划后的自检）

**Spec 覆盖：**
- spec §4.1 原料库（00/01/02）→ Task 1 ✅
- spec §4.2 提炼/预测（README + 00–04）→ Task 2–7 ✅
- spec §3 诚实三分陈述 + 情景非预言 + 中立 → 约定段 + 各任务写作要求 + 共用红线脚本 + Task4 情景纪律检查 ✅
- spec §5 与既有层分工 → Task 7 README + Task 5 挂 A 集群 ✅
- spec §6 不升版本 → 约定 + Task 7 Step 5 检查 ✅
- spec §7 验证（文件齐全/来源/三分/情景式/劳动者落点/中立/不动引擎）→ 共用脚本 + 各任务验证 + Task 7 ✅
- spec §8 非目标（不引擎接入/不吹捧/不点位时间表/不荐股）→ 约定红线 + 计划无相关内容 ✅

**Placeholder 扫描：** 无 TBD/TODO。内容任务给的是结构 + 须覆盖要点 + 搜索目标 + 验证（先搜后确认要求内容执行时检索，非占位符）。✅

**一致性：** 路径全程 `strategy/references/huawei_tau/` 与 `strategy/semiconductor_outlook/`；文件名 00-韬定律是什么 / 01-半导体产业发展逻辑 / 02-未来方向情景推演 / 03-对劳动者的含义 / 04-边界与诚实 全程一致；三分陈述/情景非预言/中立 术语一致。✅

**执行提示（给控制器）：** Task 1 与 02/03 需 WebSearch；02-未来方向情景推演 纪律最严（情景非预言 + 可证伪 + 三分），评审须重点查"无时间表/点位、可证伪点齐、三分标注、中立"。每任务走"实现 → spec 合规 → 质量（含在线 fact-check + 中立/三分专项）"两段评审；最后整支 opus 终审，再收尾。`04-边界` 虽在 Task 6 才建，02/03 可按路径前向引用。
