# Structure and Writing Conventions

This repository now uses a theme-first structure for methodology notes.

## Core principle

Do not default to date-only folders for methodology writing.
Choose the practical application first, then place the file under the appropriate theme and subtheme.

## Current root

- `methodology/great_man_inspiration/`
  - `inspiration_on_embedded_coding/`
  - `inspiration_on_software_development/`
  - `inspiration_on_today_life/`
  - `inspiration_on_making_money/`
  - `inspiration_on_stock_investing/`
  - `inspiration_on_running_a_company/`
  - `inspiration_on_educational_undertakings/`

## Placement rules

### If the note is mainly about embedded engineering method
Place it under:
`methodology/great_man_inspiration/inspiration_on_embedded_coding/`

Then choose one:
- `engineering_strategy/`
- `debugging_and_fieldwork/`
- `system_analysis_and_architecture/`
- `team_process_and_knowledge/`
- `indexes/`

Use this only for embedded software, firmware, drivers, hardware-coupled debugging, board bring-up, field constraints, and related engineering work.

### If the note is mainly about general software development
Place it under:
`methodology/great_man_inspiration/inspiration_on_software_development/`

Then choose one:
- `product_strategy/`
- `user_research_and_requirements/`
- `architecture_and_engineering/`
- `iteration_and_delivery/`
- `team_process_and_quality/`
- `indexes/`

Use this for mobile apps, WeChat mini programs, frontend and backend products, web systems, product software teams, and general software engineering methodology.

### If the note is mainly about ordinary life in the present era
Place it under:
`methodology/great_man_inspiration/inspiration_on_today_life/`

Then choose one:
- `survival_strategy/`
- `judgement_and_decision/`
- `long_term_growth/`
- `cooperation_and_organization/`
- `indexes/`

### If the note is mainly about side-income, stock investing, business, or company building
Prefer these reserved themes:
- `inspiration_on_making_money/`
- `inspiration_on_stock_investing/`
- `inspiration_on_running_a_company/`

### If the note is mainly about education practice
Place it under:
`methodology/great_man_inspiration/inspiration_on_educational_undertakings/`

Then choose one:
- `student_understanding_and_guidance/`
- `classroom_and_teaching_design/`
- `teacher_growth_and_backbone/`
- `school_governance_and_crisis_response/`
- `school_coordination_and_organization/`

Use this for teaching design, classroom management, student guidance, teacher development, school governance, and related education work. Target audience: 体制内 educators (e.g. 初中政治老师).

Use them with this distinction:
- `inspiration_on_making_money/` -> side-income, monetization, freelance/service offers, content/IP commercialization, and副业赚钱 systems
- `inspiration_on_stock_investing/` -> stock-market investing, market observation, research discipline, position sizing, and risk control in二级市场
- `inspiration_on_running_a_company/` -> company operation, leadership, organization design, and strategic execution
- `inspiration_on_educational_undertakings/` -> education practice, school management, teaching design, teacher growth, and classroom governance for 体制内 educators

## Filename rules

- Use lowercase kebab-case English filenames
- Prefer sequence-first naming for article series
- Use `000-` for overviews and corpus summaries
- Avoid date prefixes unless chronology itself is the main organizing principle

Examples:
- `001-on-protracted-war-long-cycle-embedded-software.md`
- `003-red-political-power-foothold-thinking.md`
- `000-mao-anthology-sequential-reading-overview.md`

## Sequential Mao article note style

For article-by-article inspiration notes in the Mao anthology sequence, prefer a unified long-form transfer style rather than brief card notes or YAML-only summaries.

Recommended skeleton:
- `# 从《原文》看……`
- `日期：YYYY-MM-DD`
- `原文对应：`
- `《原文标题》`
- `写作背景：`
- `说明：`
- `核心思想的当代转译：`
- numbered body sections such as `## 一、……` through `## 八、……`
- closing section such as `## 九、给今天……的一句落地建议`

Practical expectations:
- Do not stop at a short摘录 or a few bullets if the surrounding sequence uses fuller long-form transfer notes.
- Explain why the historical text mattered in its own moment, then translate it into today's practical scene.
- Keep one clear modern mainline per note; do not stack many weak mini-insights into one shallow page.
- Theme-specific notes may keep extra sections like self-check questions or related links, but those should be additions, not replacements for the core long-form structure.
- Prefer consistent human-readable prose over frontmatter-heavy templates when the surrounding sequence is prose-first.

## Index maintenance

Whenever a new note is added:
1. update the local theme `index.md`
2. update any series index that links to the note
3. if the note changes the overall structure, update `methodology/great_man_inspiration/index.md`
