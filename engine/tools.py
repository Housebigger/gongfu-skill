"""Tool handlers — the code that runs when the LLM calls gongfu_consult.

第三代交互设计——春风化雨版：
借鉴心理咨询行业原则（倾听先于提问、确认感受、节奏匹配、不评判、留退路），
让来找你咨询的劳动者先感到被听到、被理解、被接住，再逐步进入分析。
"""

import json
import logging

from . import router

logger = logging.getLogger(__name__)

# ── 加载心理咨询原则 ──
_COUNSELING = router._load_yaml("counseling-principles.yaml")


def _build_tone_instruction(triage_result: dict, phase: str) -> str:
    """根据用户状态和交互阶段，生成语气/态度的指导指令。"""
    info = triage_result.get("extracted_info", {})
    special = triage_result.get("special_handling")
    special_note = triage_result.get("special_note", "")

    parts = []

    # ── 全局语气基调（每次都提醒）──
    parts.append(
        "【语气基调】你在跟一个可能已经在现实中扛了很久的人说话。"
        "说人话，用温度，不要像机器人在走流程。每句话都先想想：如果对面坐的是你累了一天的亲人，你会怎么说？"
    )

    # ── 倾听先于提问（intake 阶段的核心原则）──
    if phase in ("need_basic_info", "assessing"):
        parts.append(
            "【倾听先于提问】你的第一句话不应该是追问信息，而应该先确认你听到了用户的感受。"
            "用你自己的话把用户的核心情绪复述一遍——不是复述事实，是复述感受。"
            "让用户知道：你在听，你听懂了，你不是在走流程。"
        )

    # ── 温柔的提问方式 ──
    if phase == "assessing" and not triage_result.get("special_note"):
        counseling = _COUNSELING.get("principles", {})
        gentle = counseling.get("温柔的提问", {})
        if gentle:
            parts.append(
                f"【温柔的提问】避免审问式直接提问。{gentle.get('desc', '')}"
                "用'方便聊聊''不知道''大概就好'这类软化词，给用户留退路。"
            )

    # ── 耗竭/焦虑/自责的特殊处理 ──
    if special == "exhaustion" or "耗竭" in (info.get("emotional_state") or ""):
        special_handling = _COUNSELING.get("special_handling", {})
        exhaustion = special_handling.get("耗竭信号", {})
        parts.append(
            f"【用户很累——先接住他】{exhaustion.get('first_response_rule', '')}"
            "\n这一轮完全不追问信息。只做一件事：让他知道他的疲惫被看到了。"
        )
    elif info.get("emotional_state") == "焦虑/迷茫":
        special_handling = _COUNSELING.get("special_handling", {})
        anxiety = special_handling.get("焦虑信号", {})
        if anxiety:
            parts.append(f"【用户很焦虑——先稳住】{anxiety.get('first_response_rule', '')}")

    # ── 分析阶段的语气 ──
    if phase == "analyzing":
        parts.append(
            "【分析阶段的语气】给出判断时要像一个关心你的老朋友，不像一个冷冰冰的顾问。"
            "先说好消息/优势（优势视角），再说需要注意的。"
            "每条建议用'你可以试试……'而不是'你应该……'。"
            "最后一定加一个安全出口：'以上供你参考，不管你怎么选都没关系。'"
        )

    # ── 不评判原则 ──
    parts.append(
        "【不评判】永远不要让用户觉得他的处境是他自己的错。"
        "不说'你当初应该……'，不说'你怎么会……'。"
        "他是来参谋下一步的，不是来受审的。"
    )

    return "\n".join(parts)


def gongfu_consult(args: dict, **kwargs) -> str:
    """共富参谋主入口——春风化雨版。

    交互流程（借鉴 Superpowers brainstorming + 心理咨询原则）：
    1. intake：先确认用户感受（不急着追问）→ 逐步了解情况 → 确认全景图
    2. analyze：先说优势再说风险 → 温柔而诚实 → 留退路

    核心改变（vs 第二代）：追问信息不再是第一优先——确认感受才是。
    """
    situation = args.get("situation", "").strip()
    mode = args.get("mode", "intake")

    if not situation:
        return json.dumps({"error": "请描述你的情况"}, ensure_ascii=False)

    triage_result = router.triage(situation)

    # ── 危机信号 → 不做任何职业判断 ──
    if triage_result.get("special_handling") == "crisis":
        crisis = _COUNSELING.get("special_handling", {}).get("危机信号", {})
        return json.dumps({
            "type": "special",
            "handling": "crisis",
            "message": crisis.get("rule", triage_result.get("message", "")),
            "original_situation": situation,
            "instruction": (
                "【危机处理】用户可能正在经历非常困难的时刻。"
                "你的回复必须温暖、不慌张、不说教、不分析职业问题。"
                "表达你在意他，然后温柔地提供热线信息。"
                "不要用机械的模板语气——像一个真正关心他的人在说话。"
            ),
        }, ensure_ascii=False, indent=2)

    if mode == "intake":
        return _handle_intake(situation, triage_result)
    return _handle_analyze(situation, triage_result)


def _handle_intake(situation: str, triage_result: dict) -> str:
    """Intake 模式：春风化雨地收集信息。"""

    info = triage_result.get("extracted_info", {})
    route_to = triage_result.get("route_to", [])
    is_exhausted = (
        triage_result.get("special_handling") == "exhaustion"
        or info.get("emotional_state") == "耗竭"
    )

    # 需要基本信息
    if triage_result.get("special_handling") == "need_more_info":
        return json.dumps({
            "type": "intake",
            "phase": "need_basic_info",
            "message": triage_result["message"],
            "tone_instruction": _build_tone_instruction(triage_result, "need_basic_info"),
            "instruction": (
                "用户说得比较模糊。但不要急着追问——先回应他说的那一两句话里你感受到的东西。"
                "然后用最轻的方式，问他最想聊的是什么。一次只问一个，像聊天不像填表。"
            ),
        }, ensure_ascii=False, indent=2)

    # 评估信息完整度
    completeness = router.assess_completeness(info, route_to)

    # 构建用户全景图
    profile_parts = []
    if info.get("cluster"):
        profile_parts.append(f"行业：{info['cluster']}")
    if info.get("industry"):
        profile_parts.append(f"具体方向：{info['industry']}")
    if info.get("region_name"):
        profile_parts.append(f"地域：{info['region_name']}")
    if info.get("age"):
        profile_parts.append(f"年龄：{info['age']}岁")
    if info.get("finances"):
        profile_parts.append(f"财务：{info['finances']}")
    if info.get("family"):
        profile_parts.append(f"家庭：{info['family']}")
    if info.get("emotional_state") and info["emotional_state"] != "正常":
        profile_parts.append(f"情绪状态：{info['emotional_state']}")

    result = {
        "type": "intake",
        "phase": "assessing",
        "user_profile": " ｜ ".join(profile_parts) if profile_parts else "（信息较少）",
        "detected_intents": [i["intent"] for i in triage_result.get("detected_intents", [])],
        "route_to": route_to,
        "completeness": completeness,
        "tone_instruction": _build_tone_instruction(triage_result, "assessing"),
    }

    if is_exhausted:
        # 耗竭用户：完全不追问，先接住
        result["phase"] = "emotional_first_aid"
        result["instruction"] = (
            "【这一轮不要追问任何信息。】用户明显很累。"
            "你的回复只做一件事：让他知道他说的那些话，你都听到了，而且你理解他为什么累。"
            "不需要分析、不需要建议、不需要追问。就只是——'我在，我听到了'。"
            "等他下一轮回复时，看他的能量状态再决定要不要开始了解情况。"
        )
    elif completeness["ready"]:
        result["phase"] = "ready_to_analyze"
        result["instruction"] = (
            "信息收集得差不多了。在进入分析之前，先用你自己的话把用户的情况复述一遍，"
            "像这样：'我先整理一下你说的情况，你看我理解得对不对——……'。"
            "复述的时候带温度，不是读清单。确认无误后再调用 analyze。"
        )
    else:
        # 需要追问——但要温柔
        counseling = _COUNSELING.get("principles", {}).get("温柔的提问", {})
        gentle_examples = counseling.get("examples", {})
        # 英文字段名 → YAML中文键名映射
        field_to_cn = {
            "cluster": "行业", "region": "地域", "age": "年龄",
            "finances": "财务", "family": "家庭",
        }
        hint = ""
        for field in ["cluster", "region", "age", "finances", "family"]:
            if field in completeness.get("missing_fields", []):
                cn_key = field_to_cn.get(field, field)
                example = gentle_examples.get(cn_key, {})
                hint = example.get("good", completeness["next_question"])
                break
        if not hint:
            hint = completeness.get("next_question", "")

        result["instruction"] = (
            f"还需要补充一些信息，但要温柔地追问，不要审问。"
            f"建议的问法参考（用你自己的话调整）：{hint}"
            f"\n记住：一次只问一个。先回应上一轮用户说的话，再自然地引出这个问题。"
        )

    return json.dumps(result, ensure_ascii=False, indent=2)


def _handle_analyze(situation: str, triage_result: dict) -> str:
    """Analyze 模式：温柔而诚实地输出判断。"""

    info = triage_result.get("extracted_info", {})
    route_to = triage_result.get("route_to", [])
    knowledge_context = {}

    if "industry-scan" in route_to and info.get("cluster"):
        knowledge_context["industry"] = router.get_industry_signal(info["cluster"])
        # 加载集群认知框架（方法论思想 × 行业挂钩）
        framework = router.get_cluster_framework(info["cluster"])
        if framework:
            knowledge_context["cluster_framework"] = framework
    if "startup-feasibility" in route_to:
        startup_data = router._load_yaml("startup-paths.yaml")
        knowledge_context["startup"] = {
            "abort_checks": startup_data.get("abort_checks", []),
            "fit_signals": startup_data.get("fit_signals", []),
            "paths": {k: {"core": v.get("core"), "fit_for": v.get("fit_for"),
                          "speed": v.get("speed"), "first_step": v.get("first_step")}
                      for k, v in startup_data.get("paths", {}).items()},
            "red_lines": startup_data.get("red_lines", []),
        }
    if "growth-planner" in route_to:
        growth_data = router._load_yaml("growth-profiles.yaml")
        knowledge_context["growth"] = {
            "learning_layers": growth_data.get("learning_layers", {}),
            "profiles": {k: {"core_contradiction": v.get("core_contradiction"),
                             "main_axis": v.get("main_axis"),
                             "routes": [r.get("name", "") + ": " + r.get("desc", "") for r in v.get("routes", [])]}
                         for k, v in growth_data.get("profiles", {}).items()},
        }
    if "collaboration-match" in route_to:
        collab_data = router._load_yaml("collaboration-forms.yaml")
        knowledge_context["collaboration"] = {
            "escalation_rule": collab_data.get("escalation_rule", ""),
            "forms": {k: {"core": v.get("core"), "fit": v.get("fit"), "tightness": v.get("tightness")}
                      for k, v in collab_data.get("forms", {}).items()},
            "red_lines": collab_data.get("red_lines", []),
        }
    if "opportunity-radar" in route_to:
        opp_data = router._load_yaml("opportunities.yaml")
        knowledge_context["opportunities"] = {
            "types": opp_data.get("types", {}),
            "opportunities": {k: {"type": v.get("type"), "certainty": v.get("certainty"),
                                   "fit_for": v.get("fit_for"), "window": v.get("window"),
                                   "anti_ai": v.get("anti_ai")}
                              for k, v in opp_data.get("opportunities", {}).items()},
            "perspectives": {k: v.get("summary") for k, v in opp_data.get("perspectives", {}).items()},
        }
    if "problem-diagnosis" in route_to:
        knowledge_context["diagnosis_tools"] = {
            "stage_judgment": router._METHODOLOGY.get("stage_judgment", {}),
            "tools_available": {k: {"principle": v.get("principle", ""), "one_liner": v.get("one_liner", "")}
                                for k, v in router._METHODOLOGY.get("tools", {}).items()},
        }

    # ── 注入马克思主义工具与启发（与毛泽东工具互补）──
    marxism_tools = []
    if info.get("cluster"):
        marxism_tools = router.get_marxism_tools_for_cluster(info["cluster"])
    if marxism_tools:
        knowledge_context["marxism_tools"] = marxism_tools

    # 匹配最相关的马克思主义启发文件
    marxism_insp = router.get_marxism_inspiration(situation, info.get("cluster"), limit=2)
    if marxism_insp:
        knowledge_context["marxism_inspiration"] = marxism_insp

    # 匹配最相关的毛泽东思想启发文件（实时检索 1500+ 篇当代转译，带缓存）
    mao_insp = router.get_mao_inspiration(situation, info.get("cluster"), limit=2)
    if mao_insp:
        knowledge_context["mao_inspiration"] = mao_insp

    # ── 注入邓小平理论工具与启发（务实行动层）──
    deng_tools = []
    if info.get("cluster"):
        deng_tools = router.get_deng_tools_for_cluster(info["cluster"])
    if deng_tools:
        knowledge_context["deng_tools"] = deng_tools

    deng_insp = router.get_deng_inspiration(situation, info.get("cluster"), limit=2)
    if deng_insp:
        knowledge_context["deng_inspiration"] = deng_insp

    # ── 注入习近平思想工具（方向层）──
    xi_tools = []
    if info.get("cluster"):
        xi_tools = router.get_xi_tools_for_cluster(info["cluster"])
    if xi_tools:
        knowledge_context["xi_tools"] = xi_tools

    xi_insp = router.get_xi_inspiration(situation, info.get("cluster"), limit=2)
    if xi_insp:
        knowledge_context["xi_inspiration"] = xi_insp

    # ── 注入产业链卡点分析工具（Serenity 方法·战略库第二根源）──
    # 仅在行业判断/趋势前瞻类路由且识别出 cluster 时注入
    if info.get("cluster") and (
        "industry-scan" in route_to or "opportunity-radar" in route_to
    ):
        chain_tools = router.get_chain_tools_for_cluster(info["cluster"])
        if chain_tools:
            knowledge_context["chain_tools"] = chain_tools

    # ── 注入经济政策推演方法（战略库第三根源·Phase 2 方法框架·evergreen）──
    # 仅"方法 + 诚实边界"，不含时效宏观假设/议题结论；
    # 趋势前瞻或行业判断时注入，不依赖 cluster（方法通用）
    if "opportunity-radar" in route_to or "industry-scan" in route_to:
        deduction = router.get_policy_deduction_method()
        if deduction:
            knowledge_context["policy_deduction"] = deduction

    # 优势视角：提炼用户已经拥有的
    strengths = _identify_strengths(info, situation)
    if strengths:
        knowledge_context["user_strengths"] = strengths

    result = {
        "type": "analysis",
        "user_situation": situation,
        "triage": {
            "detected_intents": [i["intent"] for i in triage_result.get("detected_intents", [])],
            "route_to": route_to,
            "extracted_info": info,
        },
        "tone_instruction": _build_tone_instruction(triage_result, "analyzing"),
        "knowledge_context": knowledge_context,
        "execution_guide": _build_execution_guide(route_to, info, triage_result),
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


def _identify_strengths(info: dict, situation: str) -> list:
    """从用户信息中识别他已经拥有的优势（优势视角原则）。"""
    strengths = []
    # 来咨询本身就是优势
    strengths.append("愿意主动想办法——很多人在困境里只会忍，你会来寻求帮助，这本身就是行动力")
    if info.get("age") and 25 <= info["age"] <= 45:
        strengths.append("正处于职业黄金期——有经验、有力气、还有转变的时间窗口")
    if info.get("cluster"):
        strengths.append(f"在{info['cluster']}有行业经验——这是你的底牌，不是包袱")
    if info.get("family") and info["family"] in ("有伴侣", "已婚"):
        strengths.append("有家人在身边——不管态度如何，你不是一个人")
    if info.get("finances") and info["finances"] in ("有结余", "有存款"):
        strengths.append("有一定的经济缓冲——这给你试错的空间")
    if any(kw in situation for kw in ["学了", "考了", "在学", "在考", "考了证", "学过"]):
        strengths.append("已经在学新东西了——你比自以为的更努力")
    return strengths


def _build_execution_guide(route_to: list, info: dict, triage_result: dict) -> str:
    """Build a text guide with warm, counseling-informed tone."""
    steps = []
    step_num = 1

    # Step 0: 先说优势（优势视角）
    strengths = _identify_strengths(info, triage_result.get("extracted_info", {}).get("situation", ""))
    if strengths:
        steps.append(f"第{step_num}步：先说优势。在分析之前，先告诉用户他手里已经有什么牌——"
                     f"不是安慰，是让他看到自己不是从零开始。")
        step_num += 1

    if triage_result.get("special_handling") == "exhaustion":
        steps.append(f"第{step_num}步：用相持阶段框架——'你现在经历的这段时间，不是你不行，是一个绕不过去的阶段。"
                     "它叫相持阶段。最难熬，但也最关键。'用持久战的语气，不说速胜也不说速败。")
        step_num += 1

    for skill in route_to:
        if skill == "problem-diagnosis":
            steps.append(f"第{step_num}步：诊断主要矛盾——但说成'我们来理一理，你现在最卡的那个点到底是什么'，"
                         "不是'你的主要矛盾是'。用人话，不用术语。")
        elif skill == "industry-scan":
            cluster = info.get("cluster", "未识别")
            steps.append(f"第{step_num}步：聊行业前景——'你这个方向，说实话我是看好的/有担心的/需要转型的'，"
                         "先给方向再给细节。好消息和坏消息都要说，但先说好的。")
        elif skill == "startup-feasibility":
            steps.append(f"第{step_num}步：评估创业——如果劝退，要温柔地说'现在可能不是最好的时机'，"
                         "不说'你不适合创业'。如果有戏，先说'这个方向是有机会的'再说'但要注意'。")
        elif skill == "growth-planner":
            steps.append(f"第{step_num}步：规划成长——'你现在的位置其实不差，接下来可以这样走……'，"
                         "让用户感到是在往前走，不是在追赶。")
        elif skill == "collaboration-match":
            steps.append(f"第{step_num}步：聊合作——'一个人扛确实太重了，也许可以考虑……'，"
                         "把协作说成减轻负担而不是增加复杂度。")
        elif skill == "opportunity-radar":
            steps.append(f"第{step_num}步：聊趋势——'往远了看，大方向其实是对你有利的/需要警惕的'，"
                         "给希望但不给幻觉。")
        step_num += 1

    # 在上方"聊趋势/聊行业"步之后补一条"方法论"步：前者给语气框架，本步给推演方法，互补而非重复
    if "opportunity-radar" in route_to or "industry-scan" in route_to:
        steps.append(f"第{step_num}步：谈未来方向时用「六要素情景法」——先钉现状锚点（已发生的官方数据），"
                     "再用政策作用规律外推，给基准/上行/下行三条路和各自的观察信号。"
                     "守住四条线：情景非预言、给方向不给时间表、不荐资产/个股、不预测政局。")
        step_num += 1

    steps.append(f"第{step_num}步：收尾。用一句话总结，但不是冷冰冰的结论。"
                 "像'不管怎样，你能认真想这些就说明你对自己是负责的。"
                 "以上供你参考——最终怎么走，你自己定。不管选什么，都没关系。'"
                 "\n记住：你是共富参谋，你的读者是一线劳动者。"
                 "说人话，有温度，不灌鸡汤，不说术语。先让他感到被尊重，再让他感到被帮助。")

    return "\n".join(steps)
