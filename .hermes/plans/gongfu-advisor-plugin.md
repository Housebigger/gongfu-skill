# 共富参谋插件计划书

日期：2026-06-15
性质：实施计划。定义「共富参谋」插件的完整架构、skill 体系、实现步骤。

---

## 一、要做什么

把 strategy 层的知识 + skills/ 的判断能力，封装成一个 Hermes 插件，对外暴露一个极简接口：用户用自己的话描述处境，插件自动路由到合适的 skill 组合，产出专业判断。

插件名：`gongfu-advisor`（共富参谋）
一句话定位：**劳动者的随身参谋——说出你的情况，给你看得懂、用得上的判断。**

---

## 二、为什么是一个插件而不是一堆独立 skill

现有 3 个 skill 已经能跑，但有个问题：**用户需要知道「该调用哪个 skill」。** 这对普通劳动者不友好——一个护士不会知道「我要用 industry-scan 还是 startup-feasibility」。

插件解决的核心问题是**「简约接口」**：用户不需要知道背后有几个 skill，只需要说出自己的情况，插件自动判断该用哪个/哪几个 skill，组合出一份完整判断。

```
用户：「我30岁做嵌入式开发，同事都走了，很累，不知道该不该换」
         │
    共富参谋（唯一接口）
         │
    ┌────┴─────────────────┐
    │ 内部路由：这是一个     │
    │ 「困境+行业」复合问题  │
    └────┬─────────────────┘
         │
    problem-diagnosis → industry-scan → (可选) startup-feasibility
         │
    合并输出：一份完整的判断报告
```

---

## 三、skill 体系：从 3 个到 7 个（环环相扣）

现有 3 个 skill 覆盖了「诊断/行业/创业」。要形成环环相扣的体系，需要补齐对应 strategy 层的其余维度：

### 完整 skill 体系（7 个）

| skill | 状态 | 蒸馏自 | 解决的问题 |
|---|---|---|---|
| `problem-diagnosis` | ✅ 已有 | methodology | 我这个处境的主要矛盾是什么 |
| `industry-scan` | ✅ 已有 | worker_guidance + regional | 我这个行业行不行 |
| `startup-feasibility` | ✅ 已有 | entrepreneurship | 我该不该创业、怎么起步 |
| `growth-planner` | 🔨 待建 | growth_path | 我该怎么一步步成长 |
| `collaboration-match` | 🔨 待建 | collaboration | 我该找什么样的合作、怎么分钱 |
| `opportunity-radar` | 🔨 待建 | new_value + perspective | 未来 5—10 年机会在哪 |
| `situation-triage` | 🔨 待建 | 全局 | **路由层**——用户说了情况，该用上面哪几个 skill |

### 7 个 skill 的环扣关系

```
                    situation-triage（路由）
                   ╱        │        ╲
                  ╱          │          ╲
    problem-diagnosis   industry-scan   opportunity-radar
         │                  │                  │
         ▼                  ▼                  ▼
    growth-planner    startup-feasibility  
         │                  │
         ╲                  ╱
          ╲                ╱
       collaboration-match
```

- `situation-triage` 是总入口：接收用户的自由描述，判断该路由到哪些 skill
- 三个「诊断层」skill（problem-diagnosis / industry-scan / opportunity-radar）各自独立判断
- 两个「行动层」skill（growth-planner / startup-feasibility）给出具体路线
- `collaboration-match` 在行动层之后，解决「一个人做不了怎么办」

**每个 skill 的输出可以成为另一个 skill 的输入**——这就是「环环相扣」。

---

## 四、插件架构（Hermes 插件规范）

### 目录结构

```
gongfu-advisor/
├── plugin.yaml              # 插件清单
├── __init__.py              # 注册入口
├── schemas.py               # 工具 schema（LLM 看到的）
├── tools.py                 # 工具 handler（实际执行的代码）
├── router.py                # 路由逻辑（situation-triage 的代码版）
├── skills/                  # 内嵌的 7 个 SKILL.md
│   ├── situation-triage/SKILL.md
│   ├── problem-diagnosis/SKILL.md
│   ├── industry-scan/SKILL.md
│   ├── startup-feasibility/SKILL.md
│   ├── growth-planner/SKILL.md
│   ├── collaboration-match/SKILL.md
│   └── opportunity-radar/SKILL.md
└── data/                    # 知识数据（从 strategy 层蒸馏的结构化数据）
    ├── industry-signals.yaml    # 16 集群增/转/缩信号表
    ├── regional-matrix.yaml     # 地域×机会矩阵
    ├── startup-paths.yaml       # 四条创业路径+劝退条件
    ├── growth-profiles.yaml     # 四种画像成长路线
    ├── collaboration-forms.yaml # 五种协作形态
    ├── opportunities.yaml       # 十大新蛋糕+评分
    └── methodology-tools.yaml   # 方法论工具速查
```

### plugin.yaml

```yaml
name: gongfu-advisor
version: 1.0.0
description: "共富参谋——劳动者的随身参谋。说出你的情况，获得行业判断、创业评估、成长规划、协作建议和趋势前瞻。"
provides_tools:
  - gongfu_consult
provides_hooks:
  - pre_llm_call
```

### 对外接口（极简——只有一个工具）

**`gongfu_consult`** —— 这是用户唯一需要知道的接口。

```python
{
    "name": "gongfu_consult",
    "description": "共富参谋——说出你的情况，获得专业判断。适用于：想了解行业前景、考虑创业、面临职业困境、规划成长路线、寻找合作机会。直接用大白话描述你的情况就行，不用纠结分类。",
    "parameters": {
        "type": "object",
        "properties": {
            "situation": {
                "type": "string",
                "description": "用你自己的话描述你的情况——你的行业、岗位、城市、困惑、想解决的问题。越具体越准确。"
            }
        },
        "required": ["situation"]
    }
}
```

**这就是「简约接口」的全部——一个参数 `situation`，一个字符串，大白话。**

### 内部路由逻辑（router.py）

`gongfu_consult` 被调用后，`router.py` 做三件事：

**第 1 步 · 意图识别**

从用户的 `situation` 文本中识别意图类型：

| 意图 | 关键词特征 | 路由到 |
|---|---|---|
| 行业判断 | 行业名+岗位+「行不行/前景/方向」 | industry-scan |
| 创业评估 | 「创业/副业/自己做/开店」 | startup-feasibility |
| 困境诊断 | 「纠结/迷茫/累/不知道/该怎么办」 | problem-diagnosis |
| 成长规划 | 「学习/转行/考证/规划/提升」 | growth-planner |
| 协作需求 | 「合伙/合作/找人/团队」 | collaboration-match |
| 趋势前瞻 | 「未来/趋势/5年后/前景」 | opportunity-radar |
| 复合问题 | 多个关键词叠加 | 多 skill 组合 |

**第 2 步 · 信息提取**

从自由文本中提取结构化信息：
- 行业（映射到 A—P 集群）
- 岗位
- 地域（映射到五大区域）
- 年龄段
- 财务状况
- 家庭状况

**第 3 步 · 加载知识 + 组装判断**

从 `data/*.yaml` 加载对应的结构化知识，按路由到的 skill 的执行逻辑组装判断。

### slash 命令

注册一个 `/gongfu` 命令，让用户在对话中快速触发：

```
/gongfu 我30岁做嵌入式开发，同事都走了，很累
```

等效于调用 `gongfu_consult(situation="我30岁做嵌入式开发，同事都走了，很累")`。

### pre_llm_call hook

在对话开始时，注入一段简介，让 agent 知道有这个工具可用：

```
【共富参谋】已加载。用户如果想了解行业前景、创业评估、职业困惑、成长规划，
可以调用 gongfu_consult 工具，直接传用户的原话即可。
```

---

## 五、data/ 层：从文档到结构化数据

skill 的执行逻辑需要结构化数据，不能每次都读 1800 篇文档。data/ 层是把 strategy 层的关键判断**蒸馏成机器可读的 YAML 表**。

例如 `industry-signals.yaml`：

```yaml
A-先进制造与硬科技:
  signal: 增
  certainty: 5
  methodology: 丢掉幻想-155
  growth_roles: [半导体工艺工程师, 工业软件工程师, 数控技师]
  shrink_roles: [低端组装, 人工目检]
  transition_from: [传统制造业产线操作工]
  key_skills: [PLC, 嵌入式, 精密加工]
  ...
```

这样 `industry-scan` skill 执行时，不需要读整个 worker_guidance/A 文件，直接查 YAML 表即可。

**data/ 层是 skill 体系的「数据库」——skill 是「逻辑」，data 是「知识」。**

---

## 六、实施步骤

| 步骤 | 内容 | 产出 |
|---|---|---|
| 1 | 补建 4 个新 skill 的 SKILL.md | growth-planner / collaboration-match / opportunity-radar / situation-triage |
| 2 | 从 strategy 层蒸馏 7 个 data/*.yaml | 结构化知识库 |
| 3 | 编写插件代码 | plugin.yaml / __init__.py / schemas.py / tools.py / router.py |
| 4 | 把 7 个 SKILL.md 内嵌进插件 | skills/ 目录 |
| 5 | 本地测试 | 安装插件、跑测试用例、验证路由+判断 |
| 6 | 修正+迭代 | 根据测试结果调整 |

每一步完成后停下来确认，不一口气全做完。

---

## 七、诚实的边界

1. 插件的判断质量取决于 data/ 层的蒸馏质量——如果 YAML 表不够准，判断就会跑偏。第一步必须把数据蒸馏做扎实。
2. 路由逻辑（router.py）不可能 100% 准确——自然语言意图识别有误差。设计时允许「路由到多个 skill」而非强行只选一个。
3. 本插件不提供投资/医疗/法律建议，不替代专业咨询。
4. 插件的第一个版本优先保证「能跑通+判断方向对」，不追求「完美路由」。先跑起来再迭代。
5. 方法论根基：《星星之火，可以燎原》（006）——先做出能跑的版本，再逐步迭代。
