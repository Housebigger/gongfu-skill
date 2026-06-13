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
- `engineering_strategy/`：34 篇
  - 面向长周期工程、根据地、主战场、阶段判断、总动员，以及受创后的最坏准备、转机判断与困难阶段主动缩编
- `system_analysis_and_architecture/`：1 篇
  - 面向主次矛盾、故障排序与系统结构判断
- `team_process_and_knowledge/`：59 篇
  - 面向协作边界、知识沉淀、纪律、保护建设者、复杂协作治理
- `indexes/`
  - `indexes/embedded-engineering-thought-series-index.md`

当前合计：99 篇 article-based 笔记，对应 99 篇毛文来源。

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
- 如何在客户现场、产线、供应链和样机都不稳定的工程游击区里生产工具、证据和稳定性

### `system_analysis_and_architecture/`
适合看：
- 复杂系统里如何识别主次矛盾
- 故障排序与结构化诊断怎么做

### `team_process_and_knowledge/`
适合看：
- 嵌入式团队的协作边界、知识复盘、纪律、奖惩与协同治理
- 为什么“保护建设者 + 让破坏者承担后果”是团队长期稳定的核心
- 如何在假缓和、传话和离间中保护真正扛事的人与工程主线
- 如何识别管理层口中的“准备整顿”“以后解决”究竟是在给嵌入式项目的内耗升级、拖字维持还是真实修复打掩护
- 如何避免工程公共事务重新滑回少数核心人包办，并把真正承担者组织进形成层
- 如何整顿嵌入式团队作风里的主观主义、小圈子协作和工程八股
- 如何让平台、流程、日志和工具真正服务真实承担者，并从现场语言与交付基础往上提高
- 如何在困难阶段别只让驱动、测试、FAE 和少数骨干散着补窟窿，而要把分散承担者、半可用力量和现场经验组织成真正交付主力
- 如何在项目旧打法快见顶时，研究现实形势、复盘关键历史、放下旧包袱、训练分析机器，并提前为工厂、认证、现场与更复杂系统责任做好准备
- 如何在项目到了真正转折点时，不再拿昨天的防守地图组织今天的新阶段，而是把主任务、后方整顿与工程供给系统一起切换
- 如何别把嵌入式组织做成自保机器，而要把真正对交付、现场和系统有益的建设者放到中心，并让有根据的批评进入机制
- 如何别把现场反馈说成杂音，而要回答真实工程风险并把问题闭环到板卡、固件、测试和现场动作

## 放置原则

- 先按“工程用途”放置，再按文章顺序命名
- 同一篇毛文只要能落到嵌入式母题，就可以进入这里
- 如果内容的主要承载场景是产品软件而不是硬件耦合工程，请改放到 `../inspiration_on_software_development/`

- `team_process_and_knowledge/083-embedded-cross-functional-work-needs-common-program-field-base-and-self-correction.md`
- `engineering_strategy/084-move-engineering-mountains-by-incremental-work-team-confidence-and-field-support.md`
- `engineering_strategy/085-embedded-teams-need-distributed-self-supply-and-engineering-rectification.md`
- `team_process_and_knowledge/086-dont-let-review-theater-replace-real-engineering-feedback-and-accountability.md`
- `team_process_and_knowledge/087-external-pressure-that-backs-bad-engineering-decisions-creates-field-crisis.md`
- `team_process_and_knowledge/088-embedded-teams-must-reject-surrender-thinking-that-cancels-field-facts-and-engineering-discipline.md`
- `engineering_strategy/089-embedded-teams-must-use-final-field-windows-to-concentrate-test-delivery-and-stabilization.md`
- `team_process_and_knowledge/090-after-engineering-victory-protect-field-fruits-and-keep-self-reliant-engineering-weapons.md`
- `team_process_and_knowledge/091-when-authority-calls-field-fixes-illegal-protect-engineering-facts-from-internal-war.md`
- `team_process_and_knowledge/092-field-teams-should-refuse-wrong-standby-orders-with-logs-versions-and-acceptance-rights.md`
- `team_process_and_knowledge/093-when-field-engineers-are-called-disobedient-preserve-logs-failure-history-and-self-defense-boundaries.md`
- `team_process_and_knowledge/094-field-teams-should-negotiate-acceptance-while-keeping-tests-logs-and-fallbacks.md`
- `team_process_and_knowledge/095-after-acceptance-documents-field-teams-must-convert-paper-closure-into-real-stability.md`
- `team_process_and_knowledge/096-when-vendors-say-they-are-just-restoring-operations-check-logs-access-paths-and-attack-surface.md`
- `engineering_strategy/097-embedded-teams-in-hard-times-must-protect-real-frontline-benefits-and-production-capacity.md`
- `engineering_strategy/098-embedded-teams-in-hard-years-need-main-battle-plans-local-backbone-and-long-support.md`
- `engineering_strategy/099-embedded-teams-need-stable-field-base-areas-before-central-platform-battles.md`
- `team_process_and_knowledge/100-embedded-teams-must-not-let-big-customer-or-war-panic-dissolve-field-fight.md`
- `team_process_and_knowledge/109-embedded-teams-must-not-mistake-surface-crackdowns-for-real-control-when-a-project-order-is-losing-every-front.md`
- `engineering_strategy/101-embedded-teams-under-full-scale-attack-must-preserve-core-delivery-and-field-strength.md`
- `engineering_strategy/102-embedded-teams-must-see-through-paper-tigers-and-super-weapons-to-real-strength.md`
- `engineering_strategy/103-embedded-teams-should-stop-fighting-every-bug-at-once-and-concentrate-on-one-decisive-field-breakthrough.md`
- `engineering_strategy/105-embedded-stage-reviews-must-validate-confidence-with-facts-structure-and-next-main-targets.md`
- `engineering_strategy/106-when-an-embedded-project-nears-a-new-upsurge-build-the-engineering-arms-and-supply-lines.md`
- `engineering_strategy/107-dont-tie-the-whole-embedded-delivery-system-to-one-symbolic-center-under-heavy-attack.md`
- `engineering_strategy/108-under-hard-embedded-pressure-dont-rush-into-the-vendors-scripted-route-keep-maneuvering-and-cut-dependency-lines.md`
- `engineering_strategy/113-when-an-embedded-project-reaches-a-real-turning-point-stop-running-the-new-stage-with-yesterdays-defensive-map.md`
- `engineering_strategy/117-dont-use-the-same-embedded-push-in-every-engineering-zone-classify-maturity-and-advance-by-stage.md`
- `engineering_strategy/119-dont-roll-out-new-embedded-order-everywhere-at-once-build-backbone-win-the-middle-and-expand-by-waves.md`
- `engineering_strategy/120-dont-use-one-hard-move-to-break-embedded-supply-and-production-chains.md`
- `engineering_strategy/123-correct-the-main-engineering-deviation-first-and-dont-upgrade-before-the-system-is-ready.md`
- `engineering_strategy/126-when-taking-over-an-embedded-project-first-classify-assets-keep-field-supply-running-and-plan-long.md`
- `engineering_strategy/127-dont-skip-the-necessary-transition-stage-in-a-new-engineering-zone.md`
- `team_process_and_knowledge/114-embedded-teams-need-regular-direct-problem-focused-engineering-reports.md`
- `team_process_and_knowledge/115-core-embedded-builders-must-lead-by-organizing-the-whole-delivery-main-force.md`
- `team_process_and_knowledge/121-dont-push-non-core-but-critical-middle-forces-out-of-the-embedded-delivery-system.md`
- `team_process_and_knowledge/122-after-a-critical-embedded-breakthrough-reorganize-for-sustained-delivery-not-just-another-save.md`
- `team_process_and_knowledge/124-embedded-teams-need-real-condition-based-governance-not-subjective-pushes-or-empty-process-campaigns.md`
- `team_process_and_knowledge/125-dont-keep-specs-and-decisions-inside-core-engineers.md`
- `team_process_and_knowledge/116-embedded-teams-get-stronger-when-real-burden-bearers-can-speak-help-decide-and-correct.md`
- `team_process_and_knowledge/118-dont-let-extreme-embedded-slogans-shrink-your-real-support-surface-or-hand-away-leadership.md`

## 110—112 官方缺口补写导航
- `engineering_strategy/110-when-embedded-project-enters-second-stage-move-main-force-from-lab-defense-to-field-battlefields.md`
- `team_process_and_knowledge/111-embedded-turnarounds-need-a-clear-engineering-program-and-differentiated-team-policy.md`
- `team_process_and_knowledge/112-embedded-field-work-needs-simple-discipline-that-protects-sites-tools-and-trust.md`

说明：官方 110—112 已按本主题完成补写；顺序主线推进为 001—160 连续覆盖，下一篇为 161《中国人民大团结万岁》。
