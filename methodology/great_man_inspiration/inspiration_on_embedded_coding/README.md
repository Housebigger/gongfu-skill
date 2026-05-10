# inspiration_on_embedded_coding

这个主题把毛主席相关文章转译成面向嵌入式软件、固件、驱动、板级联调、量产收敛与现场维护的方法论。

## 主题边界

这里专门处理：
- firmware / driver / BSP / board bring-up
- 硬件强耦合的软件问题
- 真机调试、量产、现场问题闭环
- 长周期、资源受限、硬约束明显的工程场景

不处理：
- 通用 App / Web / 小程序产品开发
- 纯产品侧需求管理
- 一般性的互联网协作方法

这些内容应放到 `../inspiration_on_software_development/`。

## 当前实际结构

- `debugging_and_fieldwork/`：3 篇
  - 面向调试闭环、真机调查、反资料主义，以及一线调查方法
- `engineering_strategy/`：12 篇
  - 面向长周期工程、根据地、主战场、阶段判断、总动员，以及受创后的最坏准备、转机判断与困难阶段主动缩编
- `system_analysis_and_architecture/`：1 篇
  - 面向主次矛盾、故障排序与系统结构判断
- `team_process_and_knowledge/`：27 篇
  - 面向协作边界、知识沉淀、纪律、保护建设者、复杂协作治理
- `indexes/`
  - `indexes/embedded-engineering-thought-series-index.md`

当前合计：43 篇 article-based 笔记，对应 43 篇毛文来源。

## 推荐入口

- 总入口：`index.md`
- 系列索引：`indexes/embedded-engineering-thought-series-index.md`

## 子目录速览

### `debugging_and_fieldwork/`
适合看：
- 如何用实践闭环取代纸面判断
- 如何把“没有调查就没有发言权”落到驱动与现场问题上
- 如何把“眼睛向下、开调查会”翻译成嵌入式一线取材方法

### `engineering_strategy/`
适合看：
- 长周期工程如何判断阶段
- 如何建工程根据地
- 如何识别主战场、组织主力、避免误把暂稳当休息
- 如何在重创之后既做最坏准备又不提前判死项目
- 如何在困难阶段主动收小工程机器、保住主版本主板型和主交付主力
- 如何在项目曙光可见时继续把固件、硬件、测试与现场火力压向主交付战场，避免最后阶段分兵

### `system_analysis_and_architecture/`
适合看：
- 复杂系统里如何识别主次矛盾
- 故障排序与结构化诊断怎么做

### `team_process_and_knowledge/`
适合看：
- 嵌入式团队的协作边界、知识复盘、纪律、奖惩与协同治理
- 为什么“保护建设者 + 让破坏者承担后果”是团队长期稳定的核心
- 如何在假缓和、传话和离间中保护真正扛事的人与工程主线
- 如何避免工程公共事务重新滑回少数核心人包办，并把真正承担者组织进形成层
- 如何整顿嵌入式团队作风里的主观主义、小圈子协作和工程八股
- 如何让平台、流程、日志和工具真正服务真实承担者，并从现场语言与交付基础往上提高

## 放置原则

- 先按“工程用途”放置，再按文章顺序命名
- 同一篇毛文只要能落到嵌入式母题，就可以进入这里
- 如果内容的主要承载场景是产品软件而不是硬件耦合工程，请改放到 `../inspiration_on_software_development/`
