---
name: situation-triage
description: "Use as the router/intake layer when a worker describes their situation — FIRST collect information through multi-turn dialogue (one question at a time), THEN route to analysis. This skill embodies the Superpowers-style interaction: understand before advise, confirm before conclude."
version: 2.0.0
author: gongfu-skill
license: MIT
metadata:
  gongfu_skill:
    phase: 3
    source_layers: [全局]
    methodology: [矛盾论-018, 改造我们的学习-060, 关心群众生活-011]
---

# 情况分诊 skill（路由层 · 多轮对话版）

## 概述

这个 skill 是共富参谋插件的**路由层 + 交互层**。第二代引入了 Superpowers 式的多轮对话模式：不是用户说一句就立刻给判断，而是先通过自然对话逐步把用户的情况了解清楚，确认无误后再动手分析。

核心原则（借鉴 Superpowers brainstorming）：
1. **先理解，再建议** — 不要跳过了解阶段直接给答案
2. **一次只问一个问题** — 不要一次性抛出一堆问题把用户压垮
3. **先确认，再结论** — 用自己的话复述用户情况，确认理解无误后再分析
4. **自然对话，不填表** — 用人话聊，不要搞得像问卷调查

## 交互流程

```
用户说出情况
    │
    ▼
gongfu_consult(mode="intake")  ← 第一轮
    │
    ├── 返回：已知信息 + 意图 + 信息完整度 + 下一个该问的问题
    │
    ▼
LLM 用自然语气追问（一次一个问题）
    │
    ▼
用户回答 → LLM 拼接全部信息
    │
    ▼
gongfu_consult(mode="intake")  ← 再次评估
    │
    ├── 信息不够 → 继续追问（重复上一步）
    │
    └── 信息够了 → phase="ready_to_analyze"
         │
         ▼
    LLM 复述用户全景图，请用户确认
         │
         ▼
    用户确认 → gongfu_consult(mode="analyze")
         │
         ▼
    输出完整判断
```

## 什么时候用

**总是先用这个 skill 的 intake 模式。** 它是共富参谋的总入口。

**特殊处理**：
- 如果用户情绪明显耗竭/低落 → 第一个回复先关心人，不要急着追问信息
- 如果检测到危机信号 → 不做任何职业判断，建议寻求专业帮助
- 如果用户只想要简单信息（如「光伏行业怎么样」）→ 可以快速走完，不必过度追问

## 执行逻辑

### Intake 模式

1. **分诊**：意图识别 + 信息提取 + 情绪检测（同第一代）
2. **信息完整度评估**：检查 cluster/region/age/finances/family 是否足够
3. **决策**：
   - 信息不够 → 返回 next_question，LLM 继续对话
   - 信息够了 → 返回 ready_to_analyze，LLM 复述确认
4. **全景图**：把已知信息拼成一句话画像，供 LLM 复述给用户

### Analyze 模式

1. 加载对应 skill 的知识数据（YAML）
2. 按路由顺序组装执行指南
3. LLM 综合知识 + 用户全景图，输出完整判断

## 关键设计决策

### 为什么不一次性问所有问题？

因为用户是普通劳动者，不是填表机器。一次性看到 5 个问题会让人压力很大，甚至放弃。一次只问一个，用聊天的节奏，让用户感觉是在跟一个关心他的人对话，而不是在填问卷。

### 什么时候可以跳过追问？

- 用户描述已经足够详细（如「我35岁在深圳做嵌入式开发，干了10年，有房贷，妻子支持我转行」）→ 直接确认后分析
- 用户的问题不依赖这些信息（如纯趋势前瞻「AI会不会替代嵌入式开发」）→ 直接分析
- 用户情绪耗竭 → 先关心人，信息收集放到后面

### 情绪优先原则

如果检测到耗竭信号，**第一个回复不追问信息**，而是先表达理解。等用户感觉被听到了，再慢慢了解情况。人是第一位的，信息是第二位的。

## 诚实的边界

1. 路由不可能 100% 准确——允许路由到多个 skill。
2. **情绪危机处理优先于一切**——检测到危机信号时不做职业判断。
3. 信息提取不到时宁可追问，不要瞎猜。
4. 多轮对话不是目的——目的是让用户感觉被认真对待，判断更准确。如果用户不耐烦，应加快节奏。
