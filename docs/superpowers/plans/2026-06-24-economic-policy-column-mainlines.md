# 经济政策专栏内容扩展（六主线复盘 + 作用规律）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 填充经济政策追踪专栏 Phase 1 的深度内容——6 条政策主线的"政策↔真实结果"复盘（02/03）+ 跨主线的作用规律总结（04），把骨架变成可用的规律库。

**Architecture:** 在已建专栏 `strategy/economic_policy/`（README/00/01/05 已就位）里新增 02/03/04 三个文件，沿用 `00-方法论框架.md` 的"政策→现实四步法"（①意图→②举措→③真实结果→④观察规律）。每条主线按统一模板复盘，真实结果带国家统计局/官方数据与来源。**本轮仍不动引擎**（无 `skills/data` / `engine/` 改动）。

**Tech Stack:** Markdown；WebSearch/WebFetch 核实数据与来源；无 Python、无自动化测试，doc-based 验证（文件齐全 + 每主线五段结构 + 真实结果带数据来源 + grep 无个股 + 观察性表述无"导致/因为"式强因果）。

**设计依据：** `docs/superpowers/specs/2026-06-24-economic-policy-column-design.md`（§2 六主线、§4.2 文件 02/03/04、§5 作用规律方法）。承接 `docs/superpowers/plans/2026-06-24-economic-policy-column-scaffold.md`（骨架已合并）。

**全局约定：**
- 中文优先；提交信息中文，结尾 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`。
- **诚实/中立**：真实结果**必须带可查数据 + 来源链接**（国家统计局/能源局/政府网/求是网等）；政策↔结果按**观察性关联**表述，禁用"由于政策X导致Y"式强因果，用"伴随""在…之后""与…同期"；不做政治评判、不宣传、不出个股/投资建议。
- **每条主线统一五段模板**：①政策意图（原文定调，注年份）→②落地举措→③真实结果（数据+来源）→④观察到的规律（时滞多长/靠什么传导/对就业收入有没有感）→⑤劳动者视角（哪些行业岗位顺风、时滞窗口、怎么卡位）。
- 数据以官方已公布口径为准，实现者须**在线核实每个数字**并附来源；拿不准的数字宁可不写，不编造。

---

## 已核实的主线锚点数据（实现者据此写作并逐条在线复核 + 补来源链接）

**主线①供给侧结构性改革（2015 起）**
- 去产能：2016 退出钢铁产能 >6500 万吨、煤炭 >2.9 亿吨（超额完成当年目标）；到 2018 年底提前两年超额完成"十三五"化解钢铁过剩产能上限目标。
- 结构优化：三次产业增加值比重调整为 7.7︰37.8︰54.5；战略性新兴产业增加值占 GDP 比重超 13%（2024）。
- 来源：国家统计局《经济结构不断优化…成就报告》https://www.stats.gov.cn/sj/sjjd/202302/t20230202_1896687.html ；发改委"十三五"供给侧改革评估 https://www.ndrc.gov.cn/wsdwhfz/202107/t20210728_1291931_ext.html

**主线②双碳（2020-09-22 联大首提）**
- 单位 GDP 能耗 2024 较 2020 下降 11.6%；非化石能源消费比重 2020 15.9%→2024 19.8%，煤炭比重 56.8%→53.2%。
- 可再生能源装机达 21.59 亿千瓦（提前 6 年实现风光承诺）；2024 年底风电 5.21 亿千瓦、光伏 8.86 亿千瓦；2024 新增可再生能源装机约占电力新增装机 86%。
- 来源：国家能源局《"双碳"目标提出 5 周年》https://www.nea.gov.cn/20250829/cc01921b69b948d6abd4e5c9206e2102/c.html ；《碳达峰碳中和的中国行动》白皮书 http://www.ncsc.org.cn/xwdt/gnxw/202511/t20251110_1132519.shtml

**主线③新质生产力（2023-09 首提）**
- 高技术制造业增加值 2024 +8.9%、占规上工业 16.3%；R&D 投入强度 2.68%、基础研究占 6.91%。
- 新能源汽车产量 1316.8 万辆 +38.7%；服务机器人 +15.6%；高技术产业投资 +8.0%。
- 来源：国家统计局《2024 国民经济和社会发展统计公报》https://www.stats.gov.cn/sj/zxfb/202502/t20250228_1958817.html ；求是网《新质生产力稳步发展》http://www.qstheory.cn/20250127/5e8518bc53e3483fa1a5135a9e7d0251/c.html

**主线④共同富裕（2021-08-17 中央财经委）**
- 居民人均可支配收入 2024 年 41314 元（实际 +5.1%）；2023 年较 2012 年实际增长 94.4%。
- 城乡收入比 2007 峰值 3.14→2024 年 2.34；基尼系数 2008 峰值 0.491→2024 年 0.465。
- 脱贫：2020 年农村贫困人口全部脱贫；中等收入群体占比 2000 年 9.78%→2021 年 38.86%。
- 来源：国家统计局《人民生活实现全面小康 稳步迈向共同富裕》https://www.stats.gov.cn/sj/sjjd/202409/t20240920_1956592.html ；《2024 年居民收入和消费支出情况》https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958325.html

**主线⑤货币政策转向"适度宽松"（2024 中央经济工作会议，14 年来首次）**
- 2024 两次降准共 1 个百分点、两次降政策利率共 0.3 个百分点；1 年期 LPR 3.45%→3.10%（-35bp）、5 年期以上 4.20%→3.60%（-60bp，历年最大）。
- 来源：新华网《货币政策开启"适度宽松"周期》http://www.news.cn/fortune/20241217/a7411923ad6044df98e5736e9d7faf11/c.html ；中国政府网《今年将实施适度宽松的货币政策》https://www.gov.cn/lianbo/bumen/202501/content_6996357.htm

**主线⑥财政政策转向"更加积极"（2024 中央经济工作会议）**
- 2025 赤字率拟按 4% 左右安排（+1 个百分点）、赤字规模 5.66 万亿（+1.6 万亿）；专项债 4.4 万亿（+5000 亿）；新增政府债务总规模 11.86 万亿（+2.9 万亿）。
- 来源：新华网/中国政府网 2025 政府工作报告报道 http://www.news.cn/fortune/20250307/2af2a33c603b45dca94d5a8ee6329127/c.html

---

## File Structure

**Create:**
- `strategy/economic_policy/02-政策主线复盘（上）-供给侧·双碳·新质生产力.md` — 主线①②③ 各按五段模板
- `strategy/economic_policy/03-政策主线复盘（下）-共同富裕·货币转向·财政转向.md` — 主线④⑤⑥ 各按五段模板
- `strategy/economic_policy/04-作用规律总结.md` — 跨 6 主线提炼可复用规律

**Modify:**
- `strategy/economic_policy/README.md` — 把 02/03/04 从"后续扩展路线"移入"当前文件"；更新 Phase 1 状态
- `strategy/references/policy_archive/00-信源清单.md` — 补充本轮用到的统计局/能源局/官方回顾来源（真实结果数据组）
- `CHANGELOG.md` — 更新 `[未发布]` 段（专栏从骨架补全到含六主线复盘 + 作用规律）

---

## Task 1: 政策主线复盘（上）`02-…供给侧·双碳·新质生产力.md`

**Files:**
- Create: `strategy/economic_policy/02-政策主线复盘（上）-供给侧·双碳·新质生产力.md`

- [ ] **Step 1: 在线核实主线①②③的数据**

用 WebSearch/WebFetch（`ToolSearch "select:WebSearch,WebFetch"`）逐条核实本 plan 顶部主线①②③的数字与来源（去产能吨数、产业结构比、单位 GDP 能耗 -11.6%、风光装机、高技术制造业 +8.9%、R&D 2.68% 等）。核不实或冲突的数字，改用能核实的口径或不写，并在文中标注口径来源。

- [ ] **Step 2: 写文件（三主线，每条五段模板）**

顶部说明：本篇承接 `00-方法论框架.md` 的四步法与 `01-政策追踪台账.md` 的时间线，对"产业供给侧"三条主线做"政策↔真实结果"复盘；真实结果均带数据来源；政策与结果是**观察性关联非严格因果**（见 `05`）。
对主线①供给侧改革、②双碳、③新质生产力各写一节，每节五段：
- ①政策意图（原文定调 + 年份，引 `01` 台账）
- ②落地举措（去产能/能耗双控/创新部署等）
- ③真实结果（本 plan 顶部数据 + 来源链接，措辞"伴随/同期/在…之后"）
- ④观察到的规律（时滞多长、靠什么传导、对就业/收入有没有感）
- ⑤劳动者视角（哪些行业岗位顺风/逆风、时滞窗口、怎么卡位——如光伏运维、新能源车、服务机器人用修调）
结尾指向 `04 作用规律总结`（"综合规律见 04"）。**无个股、无投资建议、无政治评判。**

- [ ] **Step 3: 验证**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f="strategy/economic_policy/02-政策主线复盘（上）-供给侧·双碳·新质生产力.md"
grep -q "供给侧" "$f" && grep -q "双碳\|碳达峰" "$f" && grep -q "新质生产力" "$f" && echo "OK: 三主线齐"
grep -qi "http" "$f" && echo "OK: 含来源"
grep -q "劳动者\|岗位\|就业" "$f" && echo "OK: 含劳动者视角"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
grep -nE "由于.*导致|因为.*所以.*政策" "$f" && echo "注意:疑似强因果表述" || echo "OK: 无强因果"
```
Expected: 三主线齐 / 含来源 / 含劳动者视角 / 无股票代码 / 无强因果。

- [ ] **Step 4: Commit**
```bash
git add "strategy/economic_policy/02-政策主线复盘（上）-供给侧·双碳·新质生产力.md"
git commit -m "feat: 经济政策专栏——政策主线复盘（上）供给侧·双碳·新质生产力

三主线按政策→真实结果五段复盘，数据带统计局/能源局来源，观察性关联非因果。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: 政策主线复盘（下）`03-…共同富裕·货币转向·财政转向.md`

**Files:**
- Create: `strategy/economic_policy/03-政策主线复盘（下）-共同富裕·货币转向·财政转向.md`

- [ ] **Step 1: 在线核实主线④⑤⑥的数据**

核实本 plan 顶部主线④⑤⑥数字与来源（居民收入 41314 元、城乡比 3.14→2.34、基尼 0.491→0.465、中等收入群体 9.78%→38.86%、2024 LPR -35bp/-60bp、2025 赤字率 4%、专项债 4.4 万亿 等）。核不实的改用可核实口径或不写。

- [ ] **Step 2: 写文件（三主线，每条五段模板）**

同 Task 1 的五段模板与顶部说明（措辞改为"分配与宏观调控"三条主线）。
- 主线④共同富裕：意图(2021 中央财经委)→举措(三次分配/扩中等收入/乡村振兴)→结果(收入、城乡比、基尼、脱贫、中等收入群体数据+来源)→规律(长周期、结构性)→劳动者视角(技能升级进中等收入群体、县域/乡村机会)
- 主线⑤货币转向：意图(2024 CEWC"适度宽松")→举措(降准降息/LPR/结构性工具)→结果(2024 降准降息与 LPR 降幅+来源)→规律(传导时滞、对房贷/小微的影响)→劳动者视角(房贷成本、创业融资环境)
- 主线⑥财政转向：意图(2024 CEWC"更加积极")→举措(赤字率/专项债/提振消费/两重两新)→结果(2025 赤字率4%、专项债4.4万亿等+来源)→规律(财政直达就业/项目的传导)→劳动者视角(以旧换新、基建/项目用工、消费券)
结尾指向 `04`。**无个股、无投资建议、无政治评判。**

- [ ] **Step 3: 验证**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f="strategy/economic_policy/03-政策主线复盘（下）-共同富裕·货币转向·财政转向.md"
grep -q "共同富裕" "$f" && grep -q "货币\|降准\|LPR" "$f" && grep -q "财政\|赤字\|专项债" "$f" && echo "OK: 三主线齐"
grep -qi "http" "$f" && echo "OK: 含来源"
grep -q "劳动者\|岗位\|就业\|收入" "$f" && echo "OK: 含劳动者视角"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
grep -nE "由于.*导致|因为.*所以.*政策" "$f" && echo "注意:疑似强因果" || echo "OK: 无强因果"
```
Expected: 三主线齐 / 含来源 / 含劳动者视角 / 无股票代码 / 无强因果。

- [ ] **Step 4: Commit**
```bash
git add "strategy/economic_policy/03-政策主线复盘（下）-共同富裕·货币转向·财政转向.md"
git commit -m "feat: 经济政策专栏——政策主线复盘（下）共同富裕·货币·财政

三主线按政策→真实结果五段复盘，数据带统计局/央行/政府工作报告来源。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: 作用规律总结 `04-作用规律总结.md`

**Files:**
- Create: `strategy/economic_policy/04-作用规律总结.md`

- [ ] **Step 1: 写文件（跨 6 主线提炼可复用规律）**

先通读 `02`、`03`、`00`、`01`。本篇是专栏的"摸透作用规律"核心交付，从六条主线复盘里抽取**可复用的"读政策"规律**，不再堆数据。必含小节：
1. **政策时滞规律**：不同政策见效快慢分层（去产能/财政项目较快 1–2 年；双碳/共同富裕/新质生产力为长周期），各举主线证据。
2. **传导机制规律**：政策→真实结果靠什么传导（配套财政/信贷是否落地、是否有部门分工与考核、是否落到价格/产能/岗位）；呼应 `00` 的"已落地配套→传导概率高"。
3. **见效快慢与"口号vs落地"分类**：哪些主线雷声大雨点也大、哪些是长期慢变量。
4. **对劳动者就业/收入的传导规律**：哪些政策直接创造/消灭岗位（去产能消、双碳/新质创）、哪些影响收入/成本（共同富裕、货币房贷、财政消费）。
5. **劳动者"读政策"五条可复用心法**：从大趋势看主线、看配套不看口号、算时滞提前卡位、跟主线不追噪声、先证伪再相信（呼应方法论库实事求是/抓主要矛盾）。
6. **诚实小结**：这些是观察性规律、非铁律，会随条件变化；详见 `05`。
**无个股、无投资建议、无政治评判**；引用 02/03 的结论时标"见 02/03"。

- [ ] **Step 2: 验证**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
f="strategy/economic_policy/04-作用规律总结.md"
grep -q "时滞" "$f" && grep -q "传导" "$f" && grep -q "劳动者" "$f" && echo "OK: 含规律要素"
grep -q "观察性\|非铁律\|非严格因果\|会随" "$f" && echo "OK: 含诚实小结"
grep -rEn '\$[A-Z]{2,5}\b' "$f" || echo "OK: 无股票代码"
```
Expected: 含规律要素 / 含诚实小结 / 无股票代码。

- [ ] **Step 3: Commit**
```bash
git add "strategy/economic_policy/04-作用规律总结.md"
git commit -m "feat: 经济政策专栏——作用规律总结（六主线提炼）

政策时滞/传导机制/对就业收入传导 + 劳动者读政策五条心法；观察性规律非铁律。

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: 文档同步 + 整体复核

**Files:**
- Modify: `strategy/economic_policy/README.md`
- Modify: `strategy/references/policy_archive/00-信源清单.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: `economic_policy/README.md` —— 02/03/04 转正**

读 README，把 `02/03/04` 从"后续扩展路线"小节移到"当前文件"表格（加内容提要：02=供给侧·双碳·新质生产力复盘；03=共同富裕·货币·财政复盘；04=作用规律总结）。"后续扩展路线"小节改为只剩"Phase 2 推演（另开 spec）"，或注明"主线复盘可持续增补新政策"。更新 Phase 1 状态描述（骨架→内容基本齐备）。**不要在当前文件清单里留下不存在的文件。**

- [ ] **Step 2: `policy_archive/00-信源清单.md` —— 补真实结果数据源**

在"真实结果数据"组补充本轮实际引用的来源（去重，保持现有条目格式）：国家统计局年度统计公报与"人民生活/经济结构"成就报告、国家能源局"双碳"成效、求是网"新质生产力"等。每条 名称—URL—（✅可抓/⚠仅登记）—提要。

- [ ] **Step 3: `CHANGELOG.md [未发布]` —— 更新条目**

把现有"经济政策追踪专栏（骨架）"条目更新为：专栏 Phase 1 内容补全——新增六条政策主线"政策↔真实结果"复盘（02/03）与作用规律总结（04）；仍为纯知识内容、未改引擎、不升版本；Phase 2 推演另开 spec。

- [ ] **Step 4: 验证 + 整体复核**
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
echo "=== 专栏文件 ===" && ls strategy/economic_policy/
echo "=== README 不留幽灵文件：当前文件应含00-05全部且都真实存在 ==="
for n in 00 01 02 03 04 05; do ls strategy/economic_policy/ | grep -q "^$n-" && echo "$n 存在" || echo "缺 $n"; done
echo "=== 无引擎/数据改动 ===" && git diff --stat main..HEAD -- engine/ skills/ && echo "(应为空)"
echo "=== 全专栏无个股 ===" && grep -rEn '\$[A-Z]{2,5}\b' strategy/economic_policy/ || echo "OK: 无股票代码"
grep -q "作用规律" strategy/economic_policy/README.md && grep -q "六" CHANGELOG.md && echo "OK: 文档同步"
```
Expected: 00–05 全部存在；engine/skills diff 为空；无股票代码；README/CHANGELOG 同步。

- [ ] **Step 5: Commit**
```bash
git add strategy/economic_policy/README.md "strategy/references/policy_archive/00-信源清单.md" CHANGELOG.md
git commit -m "docs: 专栏内容扩展收尾——README 02/03/04 转正 + 信源补真实结果源 + CHANGELOG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review（写完即查）

**1. Spec coverage（对照 spec §2/§4.2/§5）：**
- 02 主线复盘上（供给侧/双碳/新质生产力）→ Task 1 ✅
- 03 主线复盘下（共同富裕/货币/财政）→ Task 2 ✅
- 04 作用规律总结 → Task 3 ✅
- 五段模板 = spec §5 的政策→现实四步 + 劳动者视角 ✅
- README/信源/CHANGELOG 同步 → Task 4 ✅
- 不动引擎、Phase 2 推演仍另开 → 全程约束 + Task 4 复核 ✅
- 诚实/中立/无个股/观察性非因果 → 各任务验证 ✅

**2. Placeholder scan：** 每主线给了已核实锚点数据 + 来源，并要求在线复核；无 TBD/TODO。六主线模板统一、非"同上"占位。✅

**3. 一致性：** 文件名 02/03/04 与 spec 一致；五段模板各任务一致；主线①—⑥ 与 spec §2 六主线一一对应；真实结果一律带来源。✅
