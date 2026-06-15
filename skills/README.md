# skills/ —— 第三阶段核心产出：可调用的专业判断 skill

日期：2026-06-15

本目录是 gongfu-skill 第三阶段「技能上架、才华流通、智慧共富」的核心产出。它把前两阶段 1800+ 文件里的知识，蒸馏成 AI agent 可以调用的 skill——让普通劳动者不用自己读完这些文件，而是通过 agent 调用 skill，直接获得专业判断服务。

---

## 已有 skill

| skill | 解决的问题 | 蒸馏自 |
|---|---|---|
| `industry-scan/` | 我这个行业在我这个地方未来行不行 | worker_guidance 16 集群 + regional 五大区域 |
| `startup-feasibility/` | 我该不该创业、创什么、怎么起步 | entrepreneurship 四条路径 + 诚实劝退 |
| `problem-diagnosis/` | 我现在面临一个复杂局面想不清楚怎么办 | methodology 毛泽东战略思维工具箱 |

---

## skill 组合示例

```
用户：「我30岁做Web开发，被AI威胁想转行，又怕」
  → problem-diagnosis（诊断主要矛盾=技能贬值vs收入需求）
  → industry-scan（扫描AI/数字产业前景+程序员转型路线）
  → startup-feasibility（如果还想创业，评估可行性）
```

---

## 如何制作新 skill

1. 读 `00-skill设计规范.md` 了解标准结构和五项质量标准
2. 参考已有 skill 的 SKILL.md 格式
3. 按「先干再总结」原则：先做出能跑的 skill，再从实践中提炼规范更新
4. 每个 skill 必须有至少 3 个测试用例（含一个边界/劝退用例）

---

## 诚实的边界

1. 所有 skill 产出的是**方向参考**，不是就业承诺/投资建议/医疗诊断/法律意见。
2. skill 的判断基于 2025—2026 年形势，需要持续校准。
3. 第三阶段的核心假设（文档能蒸馏成可调用的 skill）正在通过这批 skill 验证中。
