# 引擎逻辑审计方法论（engine-logic-audit）

可复用的引擎逻辑缺口排查方法 + workflow。用于系统化排查 `engine/`（`router.py` / `tools.py` / `schemas.py`）与 `skills/data/*.yaml` 的**逻辑缺口**（误匹配/漏匹配/误判/静默失败/契约破坏/数据-代码不一致），产出经对抗验证的缺口清单，供随后落地修复。

> 本仓没有 pytest，引擎正确性靠"读代码 + 合成包脚本实跑"验证。本方法把这件事**系统化、并行化、对抗化**。

## 为什么这样做

朴素地"读一遍代码找 bug"有两个老问题：① 单视角易漏（一个人很难同时盯关键词覆盖、抽取边界、危机误判、注入条件、契约一致性…）；② 易出**假阳性**——把有意设计当 bug，改了反而破坏行为（引擎是线上工具，危机检测还是安全敏感路径）。

本方法用**多 lens 并行 + 逐条对抗验证**对治：
- **7 个 lens 各管一类缺口**，并行扫，互相不漏。
- **每条候选都被独立 agent 重读代码"证伪优先"复核**：默认怀疑、确认是否有意设计、严重度是否夸大、修复是否安全。只有 `is_real=true` 才进清单。
- 综合阶段**去重、按严重度排序、切成可独立提交的修复批次、给版本号评估**。

## 7 个 lens（审计维度）

| lens | 管什么 |
|---|---|
| `intent-keyword` | 6 意图 + cluster + region 关键词覆盖；子串首匹配劫持；优先级/短路顺序 |
| `extraction` | age/cluster/region/finances/family/emotional_state 抽取的误报漏报、边界、**否定盲区** |
| `crisis` | 危机/耗竭/自责检测的误判与**漏判（含不带句尾助词的终止式）**；短路最先、优先级正确；词表与代码守卫平衡 |
| `routing-injection` | route_to 映射；各知识块注入条件是否对称、是否有分支永不/永远触发、门控过窄致知识静默丢失 |
| `contract-schema` | tools 返回 vs schemas 声明一致；intake/analyze/special 形状；`ensure_ascii=False` 全覆盖；"只给指令不写回复"契约 |
| `edge-silent` | 空/非字符串/超长输入、非法 mode、裸 except、KeyError/AttributeError、加载器缺文件、缓存正确性 |
| `data-code` | 集群 ID(A–P)/route_to↔references/字段名/稳定标识符 在代码与数据间是否漂移；死数据/死分支 |

## 怎么跑（只读，不改代码）

```js
// 按名调用（脚本在 .claude/workflows/）
Workflow({ name: "engine-logic-audit" })

// 或显式脚本路径
Workflow({ scriptPath: ".claude/workflows/engine-logic-audit.js" })

// 传 args（字符串）给所有 lens 追加本次重点关注方向
Workflow({ name: "engine-logic-audit", args: "重点查 analyze 注入条件与 region 相关分支" })
```

三阶段：**Audit**（7 lens 并行找缺口）→ **Verify**（每条对抗验证）→ **Synthesize**（去重排序 + 批次 + 版本评估）。约 15–25 分钟、后台运行、完成自动通知。

## 怎么读输出

返回 `{ report, confirmed_count, total_candidates }`，`report` 含：
- `summary`：健康度总评 + 最该先修的 3–5 条
- `inventory`：已确认缺口（按严重度），每条带 `file_line / gap / proposed_fix / fix_risk`
- `fix_batches`：可独立提交的修复批次（按风险/主题）
- `version_bump_assessment`：按本仓约定判每批是否需升版本（引擎/接口/分发结构变更才升；纯关键词/数据增补不升）
- `false_positives_dropped`：被对抗验证否决的候选（透明）

## 推荐的落地闭环（修复阶段）

审计只产清单。落地按 superpowers **subagent-driven** + **分层验证门**：

1. **开 feature 分支**，先建一个"必须保持稳定"的**回归基线脚本**（真危机短路、关键集群注入、正常咨询不崩——用合成包 `gongfu_engine` 实跑）。
2. **按批次派 implementer**（TDD：先写正反双向测试矩阵再实现），每批一次提交。
3. **每批过 controller 验证门**：亲自重跑该批断言 + 回归基线（不只信 implementer 自报）。
4. **整支终审（最强模型）** 独立复跑安全路径/契约/稳定标识符/回归。
5. 终审 `READY_TO_MERGE` 后 `merge --no-ff` 回 main + push；若动了引擎逻辑则按约定升版本（三处版本串 + CHANGELOG + README）。

## 关键原则

- **证伪优先**：候选默认有罪推定？不——默认**无效**，证不出来就丢。宁可漏报也不要假阳性改坏引擎。
- **安全路径召回优先于精度**：危机/情绪检测里，漏判真信号的代价远高于多关怀一轮的误判；删词收紧务必同时验证"真信号无一漏"。
- **稳定标识符不可动**：意图名、集群 ID（A–P）、route_to 取值、emotional_state 既有取值、MCP 工具名 `gongfu_consult`——审计可报"应改键"但落地阶段对这些**只增不改键**。
- **分层验证缺一不可**：implementer 自验 + controller 门 + 终审，三层各拦不同的错。

## 案例：v1.8.0（本方法首次实战）

- 扫描：7 lens + 对抗验证 → **28 候选 → 22 确认 / 6 否决**（否决项均为有意设计/优雅降级）。
- 落地：A–G 六批 subagent-driven，每批过 controller 验证门。
- **两处安全召回回归在门里被挡下**——这正是分层验证的价值：
  1. controller 验证门发现"删裸『不想活』"漏了 `不想活下去/活不下去了`，当场补回；
  2. 整支终审又抓出 Critical：`我不想活/我真的不想活`（不带"了"的终止式）漏判 → 改用守卫式 `_crisis_hit`（『不想活』判危机、紧随『得/在』才放行）修复，复审通过。
- 结果：v1.8.0 发布；对外接口与稳定标识符全不变。详见 `CHANGELOG.md` 的 `[1.8.0]`。

> 教训：单靠 implementer 自验会漏最危险的安全回归（"删词删过头"）。**controller 门 + 终审**把它们挡在了合并之前。
