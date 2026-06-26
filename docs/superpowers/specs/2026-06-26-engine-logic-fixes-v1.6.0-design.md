# 设计文档：v1.6.0 引擎逻辑修复（源自 2026-06-26 全仓审计）

- 日期：2026-06-26
- 状态：已通过设计评审，待落地
- 涉及层：`engine/`（router/tools/schemas）+ `skills/situation-triage/SKILL.md` + `skills/data/methodology-tools.yaml` + 版本/文档。**这是引擎改动 → 升版本 v1.6.0。**

## 1. 背景与目标

2026-06-26 对全仓做了四路只读审计（引擎逻辑 / 数据接线 / 四壳构建 / 结构导航）。文档准确性批已合并（main `4d26290`，知识层、未升版本）。本轮把审计发现的**引擎正确性缺陷**修掉，并兑现一处"已承诺却未交付"的能力（地域分析），作为 v1.6.0 发布。

审计实跑（合成包 `gongfu_engine`）确认的问题：`analyze` 信息不足时产出空壳"假分析"；年龄正则从 3 位数截错并产生 `age=0`；`regional-matrix.yaml` 是运行时死数据而 schemas/SKILL 却承诺了"地域分析"；危机词 `了结`/`无所谓了` 子串误命中把正常咨询挡在门外；`situation-triage/SKILL.md` 缺测试用例与源文档映射；以及若干廉价 NIT。

## 2. 已确认的设计决策（用户已选）

- **范围 = CRITICAL + IMPORTANT + 廉价 NIT**（一轮把引擎严密性做透）。
- **region 注入内容 = 区域画像 + 决策建议 + 该区域机会评分列**（按区域符号 ①–⑤ 直接取 `opportunity_matrix` 列，不新建 cluster→机会 映射）。
- **危机词 = 收紧为更确定短语**（降误判，仍偏安全，保留真信号）。
- 升版本 v1.6.0；纯文档准确性已在上一轮完成，本轮是引擎发布。

## 3. 改动清单（按严重度）

### A. CRITICAL

**A1. `analyze` 短路 `need_more_info`** — `engine/tools.py` `gongfu_consult`
在危机分支之后、`mode` 分支之前插入：
```python
if triage_result.get("special_handling") == "need_more_info":
    return _handle_intake(situation, triage_result)
```
理由：`triage()` 在"无意图且无行业"时返回 `need_more_info`（无 `extracted_info`/`detected_intents` 键）。当前仅 `intake` 路径处理它；`analyze` 模式会落入 `_handle_analyze`，靠 `.get` 默认值兜住但产出 `route_to:[]`、`knowledge_context` 仅 `user_strengths` 的空壳"分析"，违反 intake→analyze 契约。改为无论 mode 一律回退到已验证的 `_handle_intake`（其 `need_basic_info` 分支温柔请用户补基本信息）。

**A2. 年龄正则** — `engine/router.py`（约 228 行 + 顶部 import）
- `re.search(r'(\d{2})\s*岁', situation_text)` → `re.search(r'(?<!\d)(\d{1,3})\s*岁', situation_text)`
- 抽到后校验：`14 <= age <= 80` 才赋值，否则 `age` 保持 `None`。
- `import re` 从函数内提到模块顶部（消除每次调用重复 import 的 NIT）。
理由：现状 `120岁→20`、`100岁→0`（`age=0` 静默污染 `_identify_strengths` 黄金期判断与 growth-planner 必填校验、全景图显示"0 岁"）。新正则用负向前瞻避免从多位数尾部截取；范围校验剔除 0 与不合理值。

**A3. region 接线注入 analyze** — `engine/router.py` + `engine/tools.py`
- 新增 `router.get_regional_context(region: str) -> dict`（镜像 `get_*_for_cluster` 风格）：
  ```python
  def get_regional_context(region: str) -> dict:
      """Get evergreen regional knowledge for analyze injection. {} if missing."""
      if not region:
          return {}
      regions = _REGIONAL.get("regions", {})
      profile = regions.get(region, {})
      if not profile:
          return {}
      region_key = region[0]  # ①②③④⑤
      matrix = _REGIONAL.get("opportunity_matrix", {})
      region_scores = {opp: scores.get(region_key)
                       for opp, scores in matrix.items()
                       if region_key in scores}
      return {
          "region_profile": profile,
          "region_scores": region_scores,
          "regional_advice": _REGIONAL.get("regional_advice", {}),
      }
  ```
- 在 `_handle_analyze` 的 `industry_forecast` 注入块之后加：
  ```python
  if info.get("region") and (
      "industry-scan" in route_to or "opportunity-radar" in route_to
  ):
      regional = router.get_regional_context(info["region"])
      if regional:
          knowledge_context["regional"] = regional
  ```
- `get_regional_score`（单格查询，无调用点）：保留并加 docstring 注明"供未来按 cluster→机会 精确取分用；当前 analyze 走 get_regional_context 注入整列"，不删（避免删了又要加）。
理由：兑现 schemas/SKILL 已承诺的"地域分析"，消除描述↔行为不一致。注入物为慢变量（区域画像/决策建议/机会评分矩阵列），符合 evergreen 注入惯例。

### B. IMPORTANT

**B1. 危机词收紧** — `skills/data/methodology-tools.yaml` `crisis_signals.危机`
- `了结` → 拆为 `了结自己` / `了结生命`
- `无所谓了` → 删除，或改为 `活着无所谓`
- 保留：`不想活了`、`活着没意思` 等明确信号
理由：`了结`（可指了结事务/项目）、`无所谓了`（可指随便）是高频日常词，子串匹配会把"了结这个项目然后转行""无所谓了我继续干"误判自杀危机并拒服务。收紧为确定短语在"降误判"与"安全优先"间取平衡——仍保留真信号，宁可偏保守。

**B2. `situation-triage/SKILL.md` 补全** — 按 `skills/00-skill设计规范.md`
补齐缺失段：`什么时候用`（触发/反触发）、`输入规格`、`执行逻辑`（分步）、`输出规格`、**`测试用例`（≥3，含一个边界/特殊态如 need_more_info 或 crisis）**、`源文档映射`、`边界`。该 skill 是路由层，测试用例应覆盖：典型多意图路由、仅行业无意图→industry-scan、无意图无行业→need_more_info。
理由：唯一不满足"无测试用例不算完成"质量底线的 skill。

### C. 廉价 NIT

**C1. 死参数清理** — `engine/tools.py` `_build_execution_guide`
现状第 387 行 `_identify_strengths(info, triage_result.get("extracted_info", {}).get("situation", ""))` 第二参恒 `""`（`extracted_info` 无 `situation` 键）。改：`_handle_analyze` 把已算好的 `strengths` 列表传入 `_build_execution_guide(route_to, info, triage_result, strengths)`，函数内直接用，删除重算。

**C2. region/region_name 去重** — `engine/router.py`（约 220-221 行）
现状两键赋同值（均带圈号）。改：`region` 保留带圈号全名（`get_regional_score`/`get_regional_context` 用 `region[0]`）；`region_name` 改为去圈号的可读名（如 `三大动力源`），供 `_handle_intake` 全景图展示。

**C3. schemas.py 补特殊返回说明** — `engine/schemas.py`
在工具描述中补一句：intake/analyze 之外存在两种特殊短路返回——`crisis`（情绪危机，不做职业判断）与 `need_more_info`（信息过少，先请补基本信息），其键集与常规返回不同。

**C4. 裸 except 收窄** — `engine/router.py`（约 374/463/530 行启发文件读取）
`except Exception: continue` → `except (OSError, UnicodeDecodeError): continue`，避免静默吞掉非 IO 的真 bug。

**C5. route_to 优先级注释** — `engine/router.py`（约 156-176 行）
加注释固化意图：困境/耗竭优先置 `problem-diagnosis`，其余 intent 按 `intent_keywords` 出现序追加去重。不引入新优先级表（YAGNI）。

## 4. 契约守恒（不变量）

- 引擎仍只返回"给 LLM 的指令"，不写用户可见成品（危机/need_more_info 的 `message` 是既有的、刻意的安全例外，本轮不扩大该例外）。
- 危机检测仍在 `triage` 最前、`gongfu_consult` 第一分支，不可绕过。A1 的 need_more_info 短路放在危机分支**之后**，不影响危机优先级。
- 集群 ID / intent 名 / 区域符号 / 7 主题等稳定标识符不改名。
- region 注入为慢变量（evergreen），不引入时效数据。

## 5. 验证方式（无 pytest，合成包 + doc-based）

合成包脚本（`.venv/bin/python` + `gongfu_engine` 引导）逐项：
1. **A1**：`{"situation":"你好啊","mode":"analyze"}` → 返回 `type:"intake"`、`phase:"need_basic_info"`（非 `type:"analysis"` 空壳）。
2. **A2**：`120岁`→`age` 非 20（未抽取或合理）、`100岁`→`age` 非 0、`45岁`→45、`2岁半`→不崩。
3. **A3**：`{"situation":"我在成都做新能源，想看看前景","mode":"analyze"}` → `knowledge_context` 含 `regional`（含 region_profile + region_scores + regional_advice）；无 region 的句子 → 不含 `regional`；纯创业/纯困境路由 → 不含。
4. **B1**：`"我想了结这个项目然后转行"` → 非 crisis（正常路由）；`"我不想活了"` → 仍 crisis。
5. **B2**：`grep` `situation-triage/SKILL.md` 含"测试用例"/"源文档映射"段。
6. **C1**：execution_guide 第 1 步仍在（strengths 恒非空），且不再依赖空串重算。
7. **回归**：既有 analyze（如 `"我45岁钢铁厂下岗想转行"`）的 industry/cluster_framework/各思想体系/chain/policy_deduction/industry_forecast 注入不破。
8. **四壳一致**：`build_packs.py` 后源与生成副本字节一致。
9. **版本同步**：三处 = 1.6.0；README/CHANGELOG 同步。

## 6. 版本与文档

- 升 v1.6.0：`pyproject.toml`、`api_server/server.py`（`/` index version）、`engine/plugin.yaml` 三处同步；`README.md` 顶部"当前版本"行。
- `CHANGELOG.md` 新开 `[1.6.0]`：把 `[未发布]` 累计的"华为韬定律半导体研究专题（知识层）"条目转入本版随引擎发布，并加本轮引擎修复条目（地域分析接线 + analyze 短路 + 年龄抽取 + 危机词 + situation-triage SKILL + NIT 清理）。
- `CLAUDE.md` 数据清单仍 14 个 yaml（regional-matrix 早在 14 内，本轮只是接线，不新增文件）；可补一句"regional-matrix 现经 get_regional_context 在 analyze 注入"。
- 跑 `python scripts/build_packs.py` 重建派生包。

## 7. 非目标（YAGNI）

- 不建 cluster→机会类型 映射（区域注入按符号取整列即可）。
- 不删 `get_regional_score`、不删 regional-matrix.yaml（接线而非删）。
- 不扩大"引擎直出成品话术"的例外范围。
- 不补 deng/xi inspiration 语料、不建 mao-tools.yaml（属内容路线图，已在 methodology/README 诚实声明的渐进策略，非本轮）。
- 不引入 route_to 显式优先级表（仅加注释）。
- 不改 schemas 的工具参数（仅补描述文字）。

## 8. 风险

- **危机词收紧→漏判**：靠"仍保留真信号 + 收紧而非删全部 + 偏保守"缓解；验证用例双向覆盖（误命中句转正常、真危机句仍触发）。
- **region 注入 drift**：注入物为慢变量，regional-matrix 更新时同源；与既有 cluster-keyed 注入分工（地域 vs 行业）不重叠。
- **A1 回退改变调用方预期**：analyze 信息不足时返回 intake 形态——这是更正确的语义；schemas（C3）会说明特殊返回，调用方可感知。
- **回归**：第 5 节第 7 项专门回归既有注入。
