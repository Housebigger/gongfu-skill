# skills/ —— 第三阶段核心产出：可调用的专业判断 skill + 共富参谋插件

日期：2026-06-15（初版）/ 2026-06-15（插件版更新）

本目录是 gongfu-skill 第三阶段「技能上架、才华流通、智慧共富」的核心产出。它把前两阶段 1800+ 文件里的知识，蒸馏成 AI agent 可以调用的 skill——让普通劳动者不用自己读完这些文件，而是通过 agent 调用 skill，直接获得专业判断服务。

---

## 一个入口技能 + 六类内部能力

对外只有一个技能 `gongfu-skill/`（前门：意图识别 + 信息提取 + 路由 + 情绪优先）。原先环环相扣的 6 类判断能力已下沉为 `gongfu-skill/references/` 内部参考，由引擎 `route_to` 调度：

| 内部能力（references/<能力>.md） | 回答的问题 | 知识来源 |
|---|---|---|
| `problem-diagnosis` | 我这个处境的主要矛盾是什么 | methodology 毛泽东战略思维工具箱 |
| `industry-scan` | 我这个行业在我这个地方行不行 | worker_guidance 16 集群 + regional 五大区域 |
| `startup-feasibility` | 我该不该创业、创什么、怎么起步 | entrepreneurship 四条路径 + 诚实劝退 |
| `growth-planner` | 我该怎么一步步成长 | growth_path 四种画像 + 学习地图 |
| `collaboration-match` | 我该找什么合作、怎么分钱 | collaboration 五种形态 + 信任分配 |
| `opportunity-radar` | 未来 5—10 年机会在哪 | perspective 六大前瞻 + new_value 十大增量 |

---

## 共富参谋插件 / 引擎（已移至仓库顶层 `engine/`）

> 引擎/插件代码原先在 `skills/gongfu-skill/`，现已上移到仓库顶层 `engine/`，让"知识源 `skills/`"与"引擎 `engine/`"一眼分清。本目录 `skills/` 现在只放知识源（1 个前门 `SKILL.md` + `references/` 6 能力 + `data/` + 设计规范）。

这一个技能封装成一个 Hermes 插件，对外只有一个简约接口，采用多轮对话交互（借鉴 Superpowers brainstorming 模式）：

**`gongfu_consult(situation="用大白话描述你的情况")`** —— 双模式：
- `mode="intake"`（默认）：分析用户情况，识别意图和信息缺口，返回需要追问的问题（一次一个）
- `mode="analyze"`：信息充分后，加载知识库，产出完整判断

交互流程：intake → 自然追问（一次一个问题） → 确认全景图 → analyze → 输出判断

### 插件结构

```
engine/                  # 仓库顶层
├── plugin.yaml          # 插件清单
├── __init__.py          # 注册（工具+hook+skills）
├── schemas.py           # gongfu_consult 工具 schema
├── tools.py             # 工具 handler
├── router.py            # 路由逻辑（前门分诊的代码版）
└── skills/              # ⚙生成：内嵌 gongfu-skill（含 references/，由 scripts/build_packs.py 生成，gitignore）
    └── gongfu-skill/SKILL.md + references/

# 数据不在 engine/ 内，引擎运行时读取 skills/data/ 的 14 个 YAML 知识库
```

### 安装

```bash
# 符号链接到 Hermes plugins 目录（或直接运行 ./install.sh）
ln -sf /path/to/gongfu-skill/engine ~/.hermes/plugins/gongfu-skill

# 启用
hermes plugins enable gongfu-skill

# 新开一个 session 即可用（/reset 或新 hermes）
```

---

## skill 组合示例

```
用户：「我30岁做嵌入式开发，同事都走了，很累」
  → 前门分诊路由：检测到耗竭→特殊处理 + problem-diagnosis
  → problem-diagnosis（诊断主要矛盾=精力耗竭vs判断力，阶段=相持）
  → industry-scan（嵌入式/机器人=A集群，增★★★★★）

用户：「想在县城开个养老服务机构」
  → 前门分诊路由：创业意向→startup-feasibility + 行业=E民生
  → startup-feasibility（先劝退检查→匹配路径→红线）
```

---

## 如何制作新 skill

1. 读 `00-skill设计规范.md` 了解标准结构和五项质量标准
2. 参考已有 skill 的 SKILL.md 格式
3. 按「先干再总结」原则：先做出能跑的 skill，再从实践中提炼规范更新
4. 每个 skill 必须有至少 3 个测试用例（含一个边界/劝退用例）
5. 如果 skill 需要数据，蒸馏到 `data/*.yaml`

---

## 诚实的边界

1. 所有 skill 产出的是**方向参考**，不是就业承诺/投资建议/医疗诊断/法律意见。
2. skill 的判断基于 2025—2026 年形势，需要持续校准。
3. 插件的路由逻辑不可能 100% 准确——自然语言意图识别有误差，允许路由到多个 skill。
4. **情绪危机处理优先于职业建议**——检测到耗竭/危机信号时，先处理人再处理事。
