export const meta = {
  name: 'engine-logic-audit',
  description: 'gongfu-skill 引擎逻辑缺口全面扫描：7 lens 审计 + 逐条对抗验证（证伪优先）→ 排序缺口清单 + 修复批次 + 版本号评估（只读，不改代码）',
  whenToUse: '想系统化排查 engine/（router.py/tools.py/schemas.py）+ skills/data 的逻辑缺口时。只读不改；产出经对抗验证的缺口清单与修复批次，供随后 subagent-driven 落地。可传 args（字符串）给所有 lens 追加本次重点关注方向。',
  phases: [
    { title: 'Audit', detail: '7 个 lens 并行读引擎源码找逻辑缺口' },
    { title: 'Verify', detail: '每条缺口重读代码对抗验证（证伪优先 + 修复是否安全）' },
    { title: 'Synthesize', detail: '去重排序 → 缺口清单 + 修复批次 + 版本号评估' },
  ],
}

const FILES = 'engine/router.py、engine/tools.py、engine/schemas.py、engine/__init__.py、skills/gongfu-skill/SKILL.md、skills/00-skill设计规范.md、skills/data/*.yaml'
const EXTRA = (typeof args === 'string' && args.trim()) ? `\n\n本次额外重点关注：${args.trim()}` : ''

const LENSES = [
  { key: 'intent-keyword', name: '意图分类与关键词覆盖', focus: 'triage() 的 6 意图（困境迷茫/行业判断/创业意向/成长需求/协作需求/趋势前瞻）关键词是否覆盖一线常用说法；cluster 关键词表（一线说法是否漏识别集群，尤其不带行业总称锚词的口语）；region 关键词；意图优先级与短路顺序是否有歧义/漏匹配；子串首匹配命中即停是否被次要词劫持。' },
  { key: 'extraction', name: '抽取正确性', focus: 'age/cluster/region/finances/family/emotional_state 的误报与漏报、边界（年龄范围、负向前瞻/否定盲区、多值冲突、繁简/全角/数字中文）。验证抽取是否有静默错误。' },
  { key: 'crisis', name: '危机/耗竭/自责检测', focus: '危机/耗竭/情绪词的误判（正常咨询被判危机/耗竭）与漏判（真信号未捕获，含不带句尾助词的终止式表述）；短路是否最先执行且不被其他分支抢占；词表与代码守卫（如上下文排除）是否平衡；情绪检测优先级（危机>耗竭>自责）。' },
  { key: 'routing-injection', name: '路由与知识注入条件', focus: 'route_to 映射；analyze/intake 里每块知识（industry/forecast/policy_deduction/regional/各思想 tools+inspiration/chain_tools/opportunities/user_strengths）的注入条件——是否有分支永不触发或永远触发；各注入门是否对称（同类问题应注入的块是否一致认 industry-scan/opportunity-radar/startup-feasibility）；门控过窄导致知识静默丢失。' },
  { key: 'contract-schema', name: '契约与 schema 一致性', focus: 'tools.py 实际返回结构 vs schemas.py 声明是否一致；intake/analyze/special 三形状；route_to 在各模式下的位置；need_basic_info/crisis 返回；ensure_ascii=False 是否全覆盖 json.dumps；引擎「只给 LLM 指令、不自写用户回复」契约是否被破坏；面向展示字段是否混入给 LLM 的元指令。' },
  { key: 'edge-silent', name: '边界与静默失败', focus: '空/超短/超长/非字符串输入；mode 非法值处理；编码与全角；裸 except 吞错；KeyError/IndexError/AttributeError 风险；_load_yaml 与 inspiration 加载器缺文件/缺目录处理；module 级缓存的正确性与失效；limit/切片边界。' },
  { key: 'data-code', name: '数据↔代码一致性', focus: 'YAML 里的 cluster ID 集合（A–P）vs 代码所用集合是否完全一致；route_to 取值 vs skills/gongfu-skill/references/<能力>.md 的一一对应；各 *-tools.yaml 字段名 vs 加载器实际读取字段；稳定标识符（意图名/集群ID/7 启发主题/emotional_state 取值）是否在代码与数据间漂移；某 YAML 有字段但代码没读 / 代码读但 YAML 没有（死数据/死分支）。' },
]

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'lenskey-序号，如 intent-keyword-1' },
          title: { type: 'string', description: '一句话缺口标题' },
          file: { type: 'string' },
          line_hint: { type: 'string', description: '行号或函数名锚点' },
          gap: { type: 'string', description: '逻辑缺口具体描述（是什么、为何是问题、何种输入会触发）。中文' },
          evidence: { type: 'string', description: '关键代码/数据片段引用（让验证者能复核）。' },
          severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low', 'nit'] },
          proposed_fix: { type: 'string', description: '最小、低风险的修复方向。中文' },
          fix_risk: { type: 'string', description: '修复可能的副作用/风险。中文' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
        required: ['id', 'title', 'file', 'line_hint', 'gap', 'evidence', 'severity', 'proposed_fix', 'fix_risk', 'confidence'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    title: { type: 'string' },
    is_real: { type: 'boolean', description: '重读代码后，这是否是真实逻辑缺口（默认怀疑，证伪优先）' },
    severity_final: { type: 'string', enum: ['critical', 'high', 'medium', 'low', 'nit'] },
    fix_safe: { type: 'boolean', description: '提议的修复是否安全（不破坏契约/稳定标识符/现有行为）' },
    rationale: { type: 'string', description: '复核依据（引代码）。中文' },
    correction: { type: 'string', description: '若 is_real 但描述/修复有误，给修正。中文' },
  },
  required: ['id', 'title', 'is_real', 'severity_final', 'fix_safe', 'rationale'],
}

const REPORT = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: '引擎逻辑健康度总评 + 最该修的 3-5 条。中文' },
    inventory: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, dimension: { type: 'string' }, title: { type: 'string' }, file_line: { type: 'string' },
      severity: { type: 'string' }, gap: { type: 'string' }, proposed_fix: { type: 'string' }, fix_risk: { type: 'string' },
    }, required: ['id', 'dimension', 'title', 'file_line', 'severity', 'gap', 'proposed_fix', 'fix_risk'] }, description: '已确认（is_real）缺口，按严重度排序' },
    fix_batches: { type: 'array', items: { type: 'object', properties: { batch: { type: 'string' }, items: { type: 'array', items: { type: 'string' } }, rationale: { type: 'string' } }, required: ['batch', 'items', 'rationale'] }, description: '把缺口分成可独立提交的修复批次（按风险/主题）' },
    version_bump_assessment: { type: 'string', description: '按本仓约定（引擎/接口/分发结构变更才升版本，纯知识/关键词增补不升）评估各批是否需要升版本号。中文' },
    false_positives_dropped: { type: 'array', items: { type: 'string' }, description: '被对抗验证否决的候选缺口（is_real=false）及一句话原因' },
  },
  required: ['summary', 'inventory', 'fix_batches', 'version_bump_assessment', 'false_positives_dropped'],
}

const finderPrompt = (l) => `你是 gongfu-skill 引擎代码审计员。用 Read/Grep/Bash 阅读引擎源码与数据，从【${l.name}】这个角度找**真实逻辑缺口**（不是代码风格、不是文档措辞）。

必读：${FILES}

审计焦点：${l.focus}${EXTRA}

要求：
- 只报**真实逻辑缺口**：会导致错误输出、漏匹配、误判、静默失败、契约破坏、数据-代码不一致的问题。不报风格/命名/注释类。
- 每条必须给 file + 行号/函数锚点 + 关键代码片段 evidence（让验证者能复核）。
- proposed_fix 要最小、低风险；fix_risk 要诚实写出副作用（尤其**勿动稳定标识符**：意图名/集群 ID A–P/7 启发主题/route_to 取值/emotional_state 既有取值/MCP 工具名 gongfu_consult）。
- 重要背景：引擎契约是「返回给 LLM 的指令，不自己写用户回复」；危机/情绪检测应最先短路；安全路径上**召回优先于精度**（漏判真危机的代价远高于误判）。
- 没有把握的、可能是有意设计的，标 confidence=low 并说明。
找不到就返回空 findings。中文填写。`

const verifyPrompt = (f) => `对抗验证以下引擎逻辑缺口候选。**默认怀疑**：用 Read/Grep 重读相关代码，确认它是否真实、是否可能是有意设计、严重度是否被夸大、提议的修复是否安全（不破坏契约与稳定标识符）。安全敏感路径（危机/情绪检测）尤其要验证修复不引入漏判。

候选：${JSON.stringify(f)}

判定 is_real（真实缺口才 true）、severity_final、fix_safe、rationale（引代码）、correction（如需）。中文。`

log(`引擎逻辑审计：${LENSES.length} lens 并行 → 对抗验证 → 排序清单${EXTRA ? '（含额外关注点）' : ''}`)

const perLens = await pipeline(
  LENSES,
  (l) => agent(finderPrompt(l), { label: `audit:${l.key}`, phase: 'Audit', schema: FINDINGS }),
  (res, l) => {
    const fs = (res && res.findings) ? res.findings : []
    if (!fs.length) return []
    return parallel(fs.map((f) => () =>
      agent(verifyPrompt(f), { label: `verify:${f.id || l.key}`, phase: 'Verify', schema: VERDICT })
        .then((v) => ({ finding: f, verdict: v }))
        .catch(() => null)
    )).then((arr) => arr.filter(Boolean))
  }
)

const verified = perLens.flat().filter(Boolean)
const confirmed = verified.filter((x) => x.verdict && x.verdict.is_real)
log(`审计完成：候选 ${verified.length} 条 → 确认 ${confirmed.length} 条，进入综合`)

phase('Synthesize')
const report = await agent(
  `下面是 gongfu-skill 引擎逻辑审计的全部候选缺口及其对抗验证结论（verdict.is_real / severity_final / fix_safe / correction）。请综合成一份系统化缺口清单。

${JSON.stringify(verified)}

要求：
- summary：引擎逻辑健康度总评 + 最该优先修的 3-5 条。
- inventory：只收 verdict.is_real=true 的缺口，按 severity_final 排序；用 correction 修正过的描述；去重（同一问题多 lens 命中只留一条）。
- fix_batches：把缺口分成可独立提交的修复批次（按风险/主题，如"关键词补全"="纯数据增补低风险"、"注入条件修正"="引擎逻辑需测试"），每批列 inventory 里的 id。
- version_bump_assessment：按本仓约定（引擎/接口/分发结构变更才升版本，纯知识/关键词增补不升）评估各批是否需要升版本号。
- false_positives_dropped：列出被否决（is_real=false）的候选 + 一句话原因。
中文输出。`,
  { label: 'synthesize', phase: 'Synthesize', schema: REPORT }
)

return { report, confirmed_count: confirmed.length, total_candidates: verified.length }
