# 设计文档：逐集群行业前景接入引擎（evergreen 卡片）

- 日期：2026-06-26
- 状态：已通过设计评审，待落地
- 涉及层：`skills/data/`（新增数据）+ `engine/`（router + tools）+ 文档/版本。**这是引擎改动 → 按约定升版本 v1.5.0。**

## 1. 背景与目标

`strategy/economic_policy/09-行业前景推演/` 已完成 16 个产业集群（A–P）的"政策机制驱动·三情景"行业前景推演（知识层，分两批已合并）。本轮把这套逐集群前景**按 cluster 接入** `gongfu_consult`：当引擎识别出用户所在产业集群时，注入该集群的前景方向骨架，让调用方 LLM 在"行业判断 / 趋势前瞻"类咨询中，除了已有的静态信号、产业链卡点、推演方法之外，还能拿到**这个集群专属的"政策→前景"方向**。

**核心难点 = evergreen**：09 各集群文件含大量时效性结论（三情景数据、阈值、带年份统计、待核实项）。引擎若直接搬运会迅速过时。延续 v1.4.0 `policy_deduction` 的先例——**只注入慢变量蒸馏物，时效内容留在知识层**。

## 2. 已确认的设计决策

- **注入内容 = 精简 evergreen 卡片**（用户已选）：每集群一张卡，字段全为慢变量；不含三情景数据/阈值/带年份统计/待核实项。
- **不进引擎**：三情景的具体数据与阈值、所有带年份的统计数字、待核实项——留在 `09-行业前景推演/<cluster>.md` 知识层文件。
- **复用既有 cluster-keyed 注入模式**：镜像 `chain-tools.yaml` / `industry-signals.yaml` 的 `cluster_match` + `get_*_for_cluster` + 在 `_handle_analyze` 按 route_to + cluster 注入。

## 3. 注入内容：每集群 evergreen 卡片字段

从每个 `09-行业前景推演/<cluster>.md` 蒸馏，全部慢变量：

| 字段 | 含义 | evergreen 理由 |
|------|------|--------------|
| `main_issue` | 主驱动议题（如"双碳+新动能·`08` 议题④"）| 议题归属稳定 |
| `tone` | 基调（顺风/逆风/分化/托底/转型，与 industry-signals 的 signal 对齐）| 基调以年计慢变 |
| `positioning` | 卡位方向（growth / 转岗 方向，来自各篇"六·劳动者含义"）| 方向稳定，不含具体数据 |
| `watch_indicators` | 观察指标**名**（如"风光新增装机、新能源发电占比"）| 只给指标名，不给阈值/数值 |
| `one_liner` | 一句话方向 | 概括，慢变 |
| `source` | 指向 `strategy/economic_policy/09-行业前景推演/<cluster>.md` | 让 LLM 知道详版在哪、可引导用户查阅 |

**显式排除（留在知识层）**：三情景具体数据/阈值、带年份统计数字、待核实项、情景触发条件的数值。

## 4. 数据层（新增 1 个 source 文件）

`skills/data/industry-forecast-tools.yaml`，结构镜像 `industrial-chain-tools.yaml`：
- `forecasts:` —— 16 张集群卡，键为集群 ID（A-先进制造与硬科技 … P-公用事业与市政服务），每张卡含上述 6 字段。
- `cluster_match:` —— A–P 各映射到自己那张卡（1:1）。
- 头部注释写清：本文件只含 evergreen 蒸馏物，时效数据见 `09-行业前景推演/<cluster>.md`；**集群基调翻转时同步更新本卡**；不含个股、不含时效数据。

## 5. 引擎层（改 2 个文件）

### 5.1 `engine/router.py`
- 模块级加载（与 `_CHAIN`/`_DEDUCTION` 并列）：
  ```python
  # 逐集群行业前景卡片（战略库第三根源·09 行业前景推演蒸馏·evergreen）
  _FORECAST = _load_yaml("industry-forecast-tools.yaml")
  ```
- 新函数（镜像 `get_chain_tools_for_cluster`）：
  ```python
  def get_industry_forecast_for_cluster(cluster: str) -> dict:
      """Get the evergreen per-cluster industry-forecast card. Returns {} if missing."""
      if not cluster:
          return {}
      forecasts = _FORECAST.get("forecasts", {})
      card = forecasts.get(cluster, {})
      if not card:
          return {}
      return {
          "main_issue": card.get("main_issue", ""),
          "tone": card.get("tone", ""),
          "positioning": card.get("positioning", ""),
          "watch_indicators": card.get("watch_indicators", ""),
          "one_liner": card.get("one_liner", ""),
          "source": card.get("source", ""),
      }
  ```
  （`cluster_match` 是 1:1，可直接用 cluster 键取卡；保留 `cluster_match` 段以与同目录其它工具文件结构一致、并备未来一卡多集群之需。）

### 5.2 `engine/tools.py` `_handle_analyze`
在 `chain_tools` 注入块之后、`policy_deduction` 注入块附近加：
```python
# ── 注入逐集群行业前景卡片（09 行业前景推演蒸馏·evergreen）──
# 仅 evergreen 方向骨架（主驱动/基调/卡位/观察指标名/详版指引），不含时效数据；
# 行业判断/趋势前瞻类路由且识别出 cluster 时注入
if info.get("cluster") and (
    "industry-scan" in route_to or "opportunity-radar" in route_to
):
    forecast = router.get_industry_forecast_for_cluster(info["cluster"])
    if forecast:
        knowledge_context["industry_forecast"] = forecast
```
`schemas.py` 不改。

## 6. evergreen / 防过时机制

- 卡片只放慢变量；时效内容明确留在知识层，卡片 `source` 指过去。
- `industry-forecast-tools.yaml` 头部注释 + `09-行业前景推演/00-方法与边界.md` 复盘机制补一句：**集群基调翻转时同步更新该卡**（卡片是知识层的"指针 + 方向骨架"，不是数据副本）。
- 与 v1.4.0 `policy_deduction`（注入通用"方法"）互补：方法 + 逐集群方向骨架，均不含时效结论。

## 7. 与既有注入的分工（不重复）

| 注入键 | 内容 | 触发 |
|--------|------|------|
| `industry`（industry-signals）| 静态信号 增/缩/转 + growth/shrink roles | industry-scan + cluster |
| `chain_tools`（Serenity）| 产业链卡点定位方法 | industry-scan/opportunity-radar + cluster |
| `policy_deduction`（v1.4.0）| 通用推演**方法** + 诚实边界 | industry-scan/opportunity-radar |
| **`industry_forecast`（本轮新增）**| 该集群"政策→前景"**方向骨架 + 卡位 + 观察指标 + 详版指引** | industry-scan/opportunity-radar + cluster |

四者互补、同在行业判断/趋势前瞻路由注入；`industry_forecast` 提供"这个集群往哪走"的政策驱动方向，与静态信号、产业链方法、通用推演法不重叠。

## 8. 诚实纪律（卡片层）

卡片继承 09 层全部边界：不含个股/证券代码、不给点位时间表、不投资建议、不政治预测；基调/方向为定性慢变判断；观察指标只给名不给阈值。卡片不重复知识层的时效结论，需要细节时由 `source` 指引到 09 文件。

## 9. 版本与文档

- **升版本（引擎改动）= v1.5.0**：同步 `pyproject.toml` / `api_server/server.py` / `engine/plugin.yaml`；`CHANGELOG.md` 新开 `[1.5.0]`，把 `[未发布]` 累计的两批"逐集群行业前景推演"知识条目一并转入本版（随引擎接入一起发布），并加本轮引擎接入条目；`README.md` 版本行；`CLAUDE.md` 数据清单 13→14（加 `industry-forecast-tools`）。
- 跑 `build_packs.py` 重建派生包。
- 版本号最终在 merge/收尾阶段与用户确认。

## 10. 验证方式（无自动化测试，doc-based + 合成包）

1. **单元**：`router.get_industry_forecast_for_cluster(c)` 对 16 个集群 ID 各返回非空卡，6 字段齐全；未知 cluster / 空 → `{}`。
2. **注入**（合成包直跑）：analyze + 各 cluster 的行业判断/趋势前瞻情境 → `knowledge_context` 含 `industry_forecast`；无 cluster 或纯创业/纯困境路由 → **不含**。
3. **内容红线**：`grep` `industry-forecast-tools.yaml` 无个股代码、无 `必将/一定会/建议买入/包涨/稳赚`、无 6 位数字（防时效数据混入卡）、无政治预测式断言；含 16 集群、各带 `source` 指向 09。
4. **四壳一致**：`build_packs.py` 后源与生成副本字节一致。
5. **版本同步**：三处版本 = 1.5.0；CHANGELOG/README 同步。

## 11. 非目标（YAGNI）

- 不把三情景数据/阈值/带年份统计搬进引擎。
- 不改 `schemas.py` 工具参数。
- 不动 `industry-signals.yaml`（互补，不合并）。
- 不做"前景随政策自动更新 / 到期提醒"等机制（靠 09 复盘机制人工更新卡）。
- 不在卡片里复制知识层的完整推演（只给方向骨架 + 指引）。

## 12. 风险

- **卡片与知识层 drift**：知识层 09 文件更新后卡片未同步——靠 §6 复盘机制（基调翻转时更新卡）+ 卡片只放慢变量（drift 概率低）缓解。
- **时效数据混入卡**：靠 §10 验证的"无 6 位数字 / 无年份统计"grep 红线把关。
- **与既有注入冗余**：§7 明确四者分工；execution_guide 不重复堆砌。
- **越界**：卡片继承 09 诚实边界，定性方向、不给点位/时间表/个股/政治预测。
