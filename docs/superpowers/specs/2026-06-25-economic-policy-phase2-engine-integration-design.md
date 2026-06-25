# 设计文档：经济政策推演法引擎接入（战略库第三根源·方法框架）

- 日期：2026-06-25
- 状态：已通过设计评审，待落地
- 涉及层：`skills/data/`（新增数据）+ `engine/`（router + tools）+ 文档/版本。**这是引擎改动 → 按约定升版本。**

## 1. 背景与目标

经济政策追踪专栏（战略库第三条研究根源）已完成 Phase 1（台账 01 + 主线复盘 02/03 + 作用规律 04 + 边界 05）与 Phase 2 知识层（推演方法 06 + 议题推演 07/08）。Phase 2 落地时明确把"引擎接入"留作单独一轮——因为"把预测硬注入引擎"需谨慎，更可能注入**方法框架**而非**具体结论**。本设计就是这一轮。

**目标**：把 `06-推演方法与外部约束.md` 里**通用、不带时效**的方法层接进 `gongfu_consult`——当用户问"未来方向"时，给调用方 LLM 一套**怎么向前推演**的方法（六要素情景法）+**推演的诚实纪律**（情景非预言 / 给方向不给时间表 / 不投资建议 / 不政治预测）。这为战略库第三根源补上"知识根 → 引擎"闭环，方式镜像第二根源（Serenity 产业链分析法 v1.3.0）。

## 2. 已确认的设计决策

- **注入范围 = 仅方法框架（evergreen）**（用户已选）：只注入 `06 §1` 六要素推演法 + `06 §4` 推演诚实边界。**不注入** `06 §2/§3` 的国际/国情时效性宏观假设，**不注入** `07/08` 的议题三情景结论。引擎永不过时、零维护。
- **触发路由 = 趋势前瞻 OR 行业判断**（用户已选）：`route_to` 含 `opportunity-radar` 或 `industry-scan` 时注入。
- **不依赖 cluster**：方法是通用宏观推演法，与现有所有 `get_*_for_cluster` 注入不同——按意图触发即可，趋势前瞻常无明确行业时也应给方法。
- **诚实边界双重落地**：既进 `knowledge_context`（作为内容），也在 `execution_guide` 里再强调一次（作为对 LLM 的说话指令）——保持"引擎返回指令而非成品文案"的契约。

## 3. 数据层（新增 1 个 source 文件）

`skills/data/policy-deduction-tools.yaml`——从 `06` 蒸馏。结构比现有 tool 系统更简单：**无 `cluster_match`**（方法通用），仅两块。

```yaml
# 经济政策推演方法速查
# 蒸馏自 strategy/economic_policy/06-推演方法与外部约束.md（§1 六要素 + §4 诚实边界）
# 只含推演"方法"与"诚实边界"，evergreen：
#   不含国际/国情时效性宏观假设（06 §2/§3），不含 07/08 议题三情景结论。
# 与 industrial-chain-tools.yaml 互补：Serenity 卡片回答"怎么读一条产业链"，
#   本文件回答"怎么从政策作用规律向前推演未来方向"。
# 注意：只含推演方法，不含任何个股/仓位/买卖点/政治预测。

method_steps:          # 六要素推演法，有序（对应 06 §1 ①—⑥）
  - step: 现状锚点
    principle: 用可查证的官方"已发生"数据锁定起点，注明口径与时间窗口，不从假设出发
    one_liner: 先钉住"现在确实发生了什么"，再往前推
    quote_source: strategy/economic_policy/06 §1①
  - step: 规律库外推
    principle: 用已摸透的政策作用规律（时滞分层 / 传导节点 / 就业收入传导）向前延伸，并对传导节点逐项检查；只外推已有证据的机制
    one_liner: 不是凭空预测，是拿"已验证的规律"当推演引擎
    quote_source: strategy/economic_policy/06 §1② + 04
  - step: 套外部约束与国情
    principle: 任何推演都不在真空里——先检查规律外推是否被外部约束（国际博弈/外需/供应链）和国情（资产负债表/灰犀牛/人口）压制、放大或不变；只做方向定性
    one_liner: 给推演套上"现实约束框"，判断是顺风、逆风还是待观察
    quote_source: strategy/economic_policy/06 §1③
  - step: 基准上行下行三情景
    principle: 给方向谱不给单点；每个情景各带"触发条件（可观察指标）+ 关键假设 + 对劳动者方向含义"；一律"若…则…"条件式，不给时间表点位
    one_liner: 给三条路和各自的岔路口信号，不给一句"会怎样"的预言
    quote_source: strategy/economic_policy/06 §1④
  - step: 可证伪点与观察指标
    principle: 列 2—4 个官方可查指标，说明"看到什么数据说明在走哪条情景"；区分"规律前提失效信号（回去重审规律）"与"下行情景触发信号（切换路径）"
    one_liner: 让推演可被现实检验——事后怎么都能自圆其说的不是推演是诡辩
    quote_source: strategy/economic_policy/06 §1⑤
  - step: 劳动者含义
    principle: 把宏观推演翻成一线劳动者可操作的职业/行业/技能/区域方向，含基准情景方向与"下行信号出现时留意什么"；不承诺一定涨薪/一定有工作
    one_liner: 落到"岗位机会和卡位窗口"，不落到"哪个板块涨"
    quote_source: strategy/economic_policy/06 §1⑥ + 00 第三节

honest_boundaries:     # 推演诚实边界（对应 06 §4 四条）
  - 情景非预言：给方向不给点位和时间表，只用"若…则…"条件式，不预测"某年某指标到某点"
  - 规律有条件：推演建立在历史观察性规律上，规律非铁律、遇外部冲击/政策叠加/口径调整会失效
  - 不投资建议：服务对象是劳动者的职业方向判断，落点在岗位/就业/技能，不出个股、不出资产配置
  - 不政治预测：不预测政治走势、不评判政策对错、不做人事变动预测，不超出已公开官方文件推断意图
```

字段沿用现有 tool 卡片风格（`principle` / `one_liner` / `quote_source`），便于 LLM 与其它思想工具一致消费；六要素用**有序列表**保留步骤顺序（pyyaml `safe_load` 在 Py3.7+ 保序）。

## 4. 引擎层（改 2 个文件）

### 4.1 `engine/router.py`

- 模块级加载（与现有 `_CHAIN` 等并列）：
  ```python
  # 经济政策推演方法（战略库第三根源·Phase 2 方法框架·evergreen）
  _DEDUCTION = _load_yaml("policy-deduction-tools.yaml")
  ```
- 新函数（放在 `get_chain_tools_for_cluster` 之后；**无 cluster 参数**）：
  ```python
  def get_policy_deduction_method() -> dict:
      """Get the evergreen economic-policy deduction method (six steps + honest boundaries).

      Universal macro-forecasting method — not cluster-specific. Returns {} if data missing.
      """
      if not _DEDUCTION:
          return {}
      steps = _DEDUCTION.get("method_steps", [])
      boundaries = _DEDUCTION.get("honest_boundaries", [])
      if not steps and not boundaries:
          return {}
      return {"method_steps": steps, "honest_boundaries": boundaries}
  ```

### 4.2 `engine/tools.py` `_handle_analyze`

在产业链 chain_tools 注入块之后加（**不要求 cluster**）：
```python
# ── 注入经济政策推演方法（战略库第三根源·Phase 2 方法框架·evergreen）──
# 仅"方法 + 诚实边界"，不含时效宏观假设/议题结论；趋势前瞻或行业判断时注入
if "opportunity-radar" in route_to or "industry-scan" in route_to:
    deduction = router.get_policy_deduction_method()
    if deduction:
        knowledge_context["policy_deduction"] = deduction
```

### 4.3 `_build_execution_guide` 轻触

`opportunity-radar` / `industry-scan` 对应步骤补一句方法引导（让注入的方法真被用上，且再强调一次诚实纪律）：
> 聊趋势/行业未来时，可用"六要素情景法"——先钉现状锚点、再用政策作用规律外推、给基准/上行/下行三条路和各自的观察信号。**只给方向不给时间表、不荐资产、不预测政局。**

`schemas.py` 不改——描述里"想看未来趋势"已覆盖触发，方法属内部知识无需写进工具签名。

## 5. 数据流

用户原话 → `triage` → `route_to` 含 趋势前瞻/行业判断 → `_handle_analyze` 注入 `knowledge_context.policy_deduction`（六步 + 四边界）→ LLM 拿方法向前推演、按边界说话 → 用户读到"情景化方向判断 + 诚实免责"。

## 6. 验证方式（无自动化测试，doc-based）

1. **单元级**：`router.get_policy_deduction_method()` 返回 `method_steps` 长度 6、`honest_boundaries` 长度 4，非空。
2. **注入级**（直跑引擎合成包）：
   - analyze + 趋势前瞻情境（如"我30岁想看看未来几年哪些方向有机会"）→ `knowledge_context` 含 `policy_deduction`；
   - analyze + 行业判断情境（如"我在光伏厂，想知道这行以后怎样"）→ 同样含；
   - analyze + 纯创业/纯困境（不含趋势/行业判断路由）→ **不含** `policy_deduction`。
3. **内容红线**：`grep` `policy-deduction-tools.yaml` 无个股代码（`[A-Z]{2,5}` 形态）、无 `必将/一定会/建议买入/包涨`；四条诚实边界文本齐全。
4. **四壳一致**：`build_packs.py` 后 `skills/data/policy-deduction-tools.yaml` 与三处生成副本字节一致。
5. **版本同步**：`pyproject.toml` / `api_server/server.py` / `engine/plugin.yaml` 三处版本一致；CHANGELOG 有对应条目；README 版本行同步。

## 7. 版本与文档

- **升版本（引擎改动）**：建议 `v1.4.0`（minor，新增引擎能力）。同步三处版本字符串、`CHANGELOG.md`（`[未发布]` 的相关条目转入 `[1.4.0]`，注明引擎接入）、`README.md` 顶部当前版本行、`CLAUDE.md` 数据清单 12→13（加 `policy-deduction-tools`）并补一句 `get_policy_deduction_method` 接入说明。
- 版本号最终在 merge / 收尾阶段与用户确认。

## 8. 非目标（YAGNI）

- 不注入国际/国情时效性宏观假设（`06 §2/§3`）。
- 不注入 `07/08` 议题三情景结论。
- 不加 `cluster_match`（方法通用）。
- 不改 `schemas.py` 工具参数。
- 不碰 `strategy/perspective/` 行业前瞻线（与本方法互补、视角不同）。
- 不做"自动复盘 / 假设到期提醒"等机制（复盘留在知识层 `06 §5` 由人驱动）。

## 9. 风险

- **方法被注入但未被用上**：靠 `execution_guide` 轻触引导 + knowledge_context 双落地缓解。
- **诚实边界稀释**：边界既进内容又进 guide，且在 YAML 注释和卡片里反复强调"不投资建议/不政治预测"。
- **过度注入**：限定 `opportunity-radar`/`industry-scan` 两个路由，纯困境/纯创业不触发。
- **与 chain_tools 叠加冗余**：两者互补（产业链定位 vs 政策推演方向），且都受同一红线约束；execution_guide 不重复堆砌，只各引一句。
