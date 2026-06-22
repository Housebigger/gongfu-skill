# methodology/ — 思想武器库

> 全民共享，共同富裕。

这里存放共富参谋的思想根基。所有判断、建议、认知框架，最终都追溯到这些原始的思想武器。

## 架构

```
methodology/
├── cluster_frameworks/              16 集群认知框架（跨体系引用）
│                                     把思想武器跟具体行业挂钩
│
├── mao_zedong_thought/              毛泽东思想
│   ├── reference/                   原料库（230 篇原文）
│   └── inspiration/                 启发库（1547 篇当代转译 × 7 主题）
│
├── marxism/                         马克思主义
│   ├── reference/                   原料库（马恩列经典原文）
│   │   ├── marx/                    马克思著作
│   │   ├── engels/                  恩格斯著作
│   │   └── lenin/                   列宁著作
│   └── inspiration/                 启发库（当代转译，主题与毛泽东启发库对齐）
│
└── README.md                        本文件
```

## 设计原则

1. **原料库和启发库分离** — reference/ 只放原文，inspiration/ 只放当代转译，不混在一起
2. **每个思想体系独立** — mao_zedong_thought/ 和 marxism/ 平级，各自管理自己的原文和转译
3. **启发库主题对齐** — 不同思想体系的启发库共享同一套主题结构（inspiration_on_today_life / inspiration_on_making_money 等），方便交叉引用
4. **集群框架跨体系** — cluster_frameworks/ 不属于任何单一体系，它从所有体系中提取思想工具，跟 16 产业集群挂钩

## 主题对照

启发库（inspiration/）统一使用以下 7 个主题，跨思想体系对齐：

| 主题目录 | 覆盖范围 |
|---|---|
| `inspiration_on_today_life/` | 职场生存、人生判断、日常抉择 |
| `inspiration_on_making_money/` | 副业、创业、收入多元化 |
| `inspiration_on_running_a_company/` | 经营管理、组织协作 |
| `inspiration_on_software_development/` | 软件工程方法论 |
| `inspiration_on_embedded_coding/` | 嵌入式/硬件开发方法论 |
| `inspiration_on_stock_investing/` | 投资、理财、资产管理 |
| `inspiration_on_educational_undertakings/` | 学习、教育、考证成长 |

## 扩展方式

将来增加新的思想体系（如邓小平理论、习近平思想），按同样模式：

1. 在 methodology/ 下新建 `<体系名>/` 目录
2. 内含 `reference/`（原料库）和 `inspiration/`（启发库）
3. 启发库使用与现有体系对齐的 7 主题结构
4. 更新本 README 的架构图
