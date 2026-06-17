"""Tool handlers — the code that runs when the LLM calls gongfu_consult.

交互哲学（融合 Carl Rogers 以人为中心疗法 + Superpowers brainstorming）：

来访者来到共富参谋时，往往已经背负着很大的压力。他们不是来做问卷调查的，
是在扛不住的时候试着找一条路。所以——

1. 先接住人，再接住问题（情绪优先于信息）
2. 先倾听，再追问（积极倾听：复述+确认+共情）
3. 一次只问一个问题（不要像填表）
4. 不评判（用户已经够自责了，不要再加一层）
5. 不替用户做决定（帮他看清选项和后果，决定权永远在他手里）
6. 语气温和、循序渐进（春风化雨，不是雷厉风行）
7. 真诚（不假惺惺，不灌鸡汤，该说真话的时候温和地说真话）
"""

import json
import logging

from . import router

logger = logging.getLogger(__name__)


# ── 交互原则常量（贯穿所有模式）──
TONE_GUIDE = (
    "【交互语气·最重要】\n"
    "来找你咨询的人，大多是在生活里扛着很大压力的普通劳动者。他们鼓起勇气开口，"
    "不是来做问卷调查的，是想找一条路。请记住：\n"
    "• 先接住人，再接住问题——第一句话永远是回应 ta 的感受，不是追问信息\n"
    "• 一次只问一个问题——像朋友聊天一样，不要连珠炮\n"
    "• 用温暖但真诚的语气——不假惺惺，不灌鸡汤，该说真话的时候温和地说真话\n"
    "• 不评判——不管 ta 的处境多难，你永远不会说'你怎么不早做打算'\n"
    "• 不替 ta 做决定——你帮 ta 看清选项和后果，但'走哪条路'永远是 ta 自己说了算\n"
    "• 复述确认——用自己的话把 ta 的处境复述一遍，让 ta 知道你真的听懂了\n"
    "• 允许沉默和犹豫——如果 ta 回答得简短，不要追问，给 ta 空间"
)

EMPATHY_RESPONSES = {
    "耗竭": (
        "听起来你这段时间真的很累。不是身体累，是心累——那种扛了很久、"
        "快撑不住的感觉。你能说出来，已经很不容易了。"
    ),
    "焦虑/迷茫": (
        "听起来你现在有些焦虑，不太确定下一步怎么走。这种感觉很正常——"
        "变化太快的时候，谁都会有这种不确定感。"
    ),
    "正常": None,  # 不需要特殊共情
}


def gongfu_consult(args: dict, **kwargs) -> str:
    """共富参谋主入口——双模式：intake（倾听+收集）和 analyze（分析+输出）。"""
    situation = args.get("situation", "").strip()
    mode = args.get("mode", "intake")

    if not situation:
        return json.dumps({"error": "请描述你的情况"}, ensure_ascii=False)

    # 分诊
    triage_result = router.triage(situation)

    # 危机信号 → 安全第一
    if triage_result.get("special_handling") == "crisis":
        return json.dumps({
            "type": "special",
            "handling": "crisis",
            "message": triage_result["message"],
            "tone_guide": TONE_GUIDE,
            "instruction": (
                "用户发出了危机信号。这是最重要的时刻——不要谈职业、不要谈行业、不要追问任何信息。"
                "用最温和的语气告诉 ta：你听到了，你在乎 ta，ta 不是一个人。"
                "然后提供专业援助资源。如果 ta 愿意继续说，就倾听。"
            ),
        }, ensure_ascii=False, indent=2)

    if mode == "intake":
        return _handle_intake(situation, triage_result)

    return _handle_analyze(situation, triage_result)


def _handle_intake(situation: str, triage_result: dict) -> str:
    """Intake 模式：倾听→共情→了解→确认。不是信息采集，是对话。"""

    info = triage_result.get("extracted_info", {})
    route_to = triage_result.get("route_to", [])
    emotion = info.get("emotional_state", "正常")

    # 用户的描述太模糊——但不要直接说"你说不清楚"
    if triage_result.get("special_handling") == "need_more_info":
        return json.dumps({
            "type": "intake",
            "phase": "need_basic_info",
            "tone_guide": TONE_GUIDE,
            "instruction": (
                "用户的描述比较简短，你还不太清楚 ta 想聊什么。"
                "不要说'你的描述不够清楚'——那是填表思维。"
                "用一个温和的开放式问题开场，比如：\n"
                "  '谢谢你愿意跟我说。能多聊一点你现在的情况吗？比如你目前在做什么，"
                "或者最让你烦心的是哪件事？'\n"
                "让 ta 自己决定从哪里开始讲。"
            ),
        }, ensure_ascii=False, indent=2)

    # 评估信息完整度
    completeness = router.assess_completeness(info, route_to)

    # 构建用户全景图
    profile_parts = []
    if info.get("cluster"):
        profile_parts.append(f"行业：{info['cluster']}")
    if info.get("industry"):
        profile_parts.append(f"方向：{info['industry']}")
    if info.get("region_name"):
        profile_parts.append(f"地域：{info['region_name']}")
    if info.get("age"):
        profile_parts.append(f"年龄：{info['age']}岁")
    if info.get("finances"):
        profile_parts.append(f"财务：{info['finances']}")
    if info.get("family"):
        profile_parts.append(f"家庭：{info['family']}")
    if emotion != "正常":
        profile_parts.append(f"情绪：{emotion}")

    # 共情回应
    empathy = EMPATHY_RESPONSES.get(emotion)

    result = {
        "type": "intake",
        "phase": "assessing",
        "tone_guide": TONE_GUIDE,
        "user_profile": " ｜ ".join(profile_parts) if profile_parts else "（信息较少）",
        "detected_intents": [i["intent"] for i in triage_result.get("detected_intents", [])],
        "route_to": route_to,
        "completeness": completeness,
        "empathy_suggestion": empathy,
    }

    # 根据情况给出不同的交互指令
    if emotion in ("耗竭",) :
        # 情绪优先：第一轮绝不追问信息
        result["phase"] = "emotional_first_aid"
        result["instruction"] = (
            "这是最重要的时刻。用户现在很累——不是身体的累，是心里的累。"
            "你的第一个回复要做三件事，而且只做这三件事：\n"
            "1. 让 ta 知道你听到了——用你自己的话复述 ta 的处境（'听起来你最近……'）\n"
            "2. 正常化 ta 的感受——'扛了这么久，换谁都会累的'\n"
            "3. 不追问任何信息——如果 ta 想继续说，你就听；如果 ta 只是想找人说说话，那就陪着\n"
            "不要在这一轮提行业、提建议、提任何'你应该'。人在耗竭状态下听不进去道理，"
            "ta 只需要知道：有人听到了，有人在乎。"
        )
    elif emotion in ("焦虑/迷茫",):
        result["instruction"] = (
            "用户现在有些焦虑和迷茫。先回应 ta 的感受（'听起来你现在不太确定……'），"
            "然后温和地问一个问题开始了解。不要一次问太多——"
            "ta 需要感觉这是一个安全的、不会被评判的对话。"
        )
    elif completeness["ready"]:
        result["phase"] = "ready_to_analyze"
        result["instruction"] = (
            "你已经了解了足够的信息。在给出分析之前，先做一件事：\n"
            "用你自己的话，温和地复述 ta 的完整情况——就像在说'我先确认一下，我理解得对不对'。\n"
            "比如：'我先梳理一下你说的——你现在……，最让你头疼的是……，是这样吗？'\n"
            "等 ta 说'对'或者补充修正后，再调用 mode='analyze'。\n"
            "这一步看起来多余，但很重要——它让用户感觉被认真对待，也能避免你理解偏差。"
        )
    else:
        result["instruction"] = (
            f"还需要再了解一些情况，但不要让用户感觉在被审问。\n"
            f"建议的方向是了解「{completeness['next_question']}」，但你要用聊天的方式问。\n"
            f"比如不要问'你在哪个城市'，而是说'你目前在哪个地方发展？不同地方情况差别挺大的。'\n"
            f"先回应 ta 已经说过的内容（哪怕一句'听起来确实不容易'），再自然地引出问题。\n"
            f"用户回答后，把所有信息拼在一起，再次调用 gongfu_consult(mode='intake')。"
        )

    if triage_result.get("special_note"):
        result["special_note"] = triage_result["special_note"]

    return json.dumps(result, ensure_ascii=False, indent=2)


def _handle_analyze(situation: str, triage_result: dict) -> str:
    """Analyze 模式：加载知识库，组装判断指南。"""

    info = triage_result.get("extracted_info", {})
    route_to = triage_result.get("route_to", [])
    knowledge_context = {}

    if "industry-scan" in route_to and info.get("cluster"):
        knowledge_context["industry"] = router.get_industry_signal(info["cluster"])

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
            "tools_available": {k: {"principle": v.get("principle"), "one_liner": v.get("one_liner")}
                                for k, v in router._METHODOLOGY.get("tools", {}).items()},
        }

    result = {
        "type": "analysis",
        "tone_guide": TONE_GUIDE,
        "user_situation": situation,
        "triage": {
            "detected_intents": [i["intent"] for i in triage_result.get("detected_intents", [])],
            "route_to": route_to,
            "extracted_info": info,
        },
        "special_note": triage_result.get("special_note"),
        "knowledge_context": knowledge_context,
        "execution_guide": _build_execution_guide(route_to, info, triage_result),
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


def _build_execution_guide(route_to: list, info: dict, triage_result: dict) -> str:
    """Build a text guide telling the LLM how to sequence the skills."""
    steps = []
    step_num = 1
    emotion = info.get("emotional_state", "正常")

    # 开场：先回到这个人
    steps.append(
        f"开场（比所有分析都重要）：用一两句话让用户感到被理解。"
        "不是客套的'我理解你'，是具体地复述 ta 的处境——"
        "'你扛了这么久，真的很不容易。现在咱们一起来看看，有哪些路可以走。'"
    )
    step_num += 1

    # 如果情绪耗竭，在分析前先给 ta 喘息
    if emotion == "耗竭":
        steps.append(
            f"第{step_num}步：温柔地提醒——在开始分析之前，ta 需要知道一件事："
            "在很累的状态下做的决定，往往不是最好的决定。"
            "不是劝 ta 不要想这些事，是让 ta 知道'不急着现在就做决定'。"
            "用相持阶段的逻辑：这不是要速胜也不是要认输，是先歇一歇、攒点力气再走。"
        )
        step_num += 1

    for skill in route_to:
        if skill == "problem-diagnosis":
            steps.append(f"第{step_num}步：帮 ta 看清——ta 真正的问题是什么？"
                         "不是表面的'要不要换工作'，是更深的那一层。"
                         "用矛盾分析：什么是主要矛盾？ta 现在处于哪个阶段（速决/相持/反攻）？"
                         "但说的时候不要用术语——用人话，像朋友帮 ta 梳理一样。")
        elif skill == "industry-scan":
            cluster = info.get("cluster", "未识别")
            steps.append(f"第{step_num}步：说说 ta 的行业——行业={cluster}。"
                         "告诉 ta 大方向（增/转/缩），但不要只给冰冷的数据。"
                         "要说清楚：'这个行业整体在往上走/在转型/在收缩'，然后说'这意味着对你来说……'")
        elif skill == "startup-feasibility":
            steps.append(f"第{step_num}步：如果 ta 想创业——先做劝退检查。"
                         "如果命中劝退条件，温和但明确地说：'现在可能不是最好的时机'，"
                         "并告诉 ta 先做什么（比如先稳定财务/先和家人聊聊/先学一门技能）。"
                         "如果没命中，给 ta 一条最适合的路和第一步该做什么。"
                         "红线一定要说，但用'提醒'的语气而不是'警告'。")
        elif skill == "growth-planner":
            steps.append(f"第{step_num}步：给 ta 一条成长路线——"
                         "不用太长，抓重点：ta 现在在哪一层，下一步该往哪走，第一步做什么。"
                         "给 ta 希望但不夸大——'这条路需要时间，但走得通'。")
        elif skill == "collaboration-match":
            steps.append(f"第{step_num}步：如果 ta 需要找人合作——"
                         "告诉 ta 适合哪种协作方式，第一次合作从最松的开始。"
                         "分钱的事要说清楚——'先小人后君子，反而能走得更远'。")
        elif skill == "opportunity-radar":
            steps.append(f"第{step_num}步：说说 ta 关心的方向未来会怎样——"
                         "给方向不预测时间。指出被低估的机会，也诚实说不确定性。")
        step_num += 1

    steps.append(
        f"第{step_num}步（收尾·同样重要）：结尾不是总结，是送 ta 一句话。"
        "不是'祝你好运'，是一个具体的、有力量的、属于 ta 这个人的收尾。"
        "让 ta 知道：不管选择走哪条路，这条路都有人在走，而且走得通。\n\n"
        "格式要求：必须包含主要判断+行动建议+风险红线+一句话收尾。"
        "说人话，不说术语。温暖但不虚假，真诚但不冷漠。"
    )

    return "\n".join(steps)
