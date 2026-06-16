"""Tool handlers — the code that runs when the LLM calls gongfu_consult."""

import json
import logging

from . import router

logger = logging.getLogger(__name__)


def gongfu_consult(args: dict, **kwargs) -> str:
    """共富参谋主入口。

    Receives the user's free-form situation text, runs triage routing,
    loads relevant knowledge data, and returns a structured consultation
    guide that the LLM uses to produce the final response.

    The handler does NOT produce the final user-facing text — it returns
    structured data + knowledge context that the LLM then synthesizes
    into a personalized, warm response. This is by design: the LLM is
    better at tone/empathy/language than code, and the code is better at
    data lookup/routing than the LLM.
    """
    situation = args.get("situation", "").strip()
    if not situation:
        return json.dumps({"error": "请描述你的情况"}, ensure_ascii=False)

    # Step 1: Run triage routing
    triage_result = router.triage(situation)

    # Step 2: Handle special cases (crisis, need_more_info)
    if triage_result.get("special_handling") in ("crisis", "need_more_info"):
        return json.dumps({
            "type": "special",
            "handling": triage_result["special_handling"],
            "message": triage_result["message"],
            "original_situation": situation,
        }, ensure_ascii=False, indent=2)

    # Step 3: Load relevant knowledge data for routed skills
    info = triage_result.get("extracted_info", {})
    route_to = triage_result.get("route_to", [])
    knowledge_context = {}

    # Load industry data if needed
    if "industry-scan" in route_to and info.get("cluster"):
        knowledge_context["industry"] = router.get_industry_signal(info["cluster"])

    # Load startup data if needed
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

    # Load growth data if needed
    if "growth-planner" in route_to:
        growth_data = router._load_yaml("growth-profiles.yaml")
        knowledge_context["growth"] = {
            "learning_layers": growth_data.get("learning_layers", {}),
            "profiles": {k: {"core_contradiction": v.get("core_contradiction"),
                             "main_axis": v.get("main_axis"),
                             "routes": [r.get("name", "") + ": " + r.get("desc", "") for r in v.get("routes", [])]}
                         for k, v in growth_data.get("profiles", {}).items()},
        }

    # Load collaboration data if needed
    if "collaboration-match" in route_to:
        collab_data = router._load_yaml("collaboration-forms.yaml")
        knowledge_context["collaboration"] = {
            "escalation_rule": collab_data.get("escalation_rule", ""),
            "forms": {k: {"core": v.get("core"), "fit": v.get("fit"), "tightness": v.get("tightness")}
                      for k, v in collab_data.get("forms", {}).items()},
            "red_lines": collab_data.get("red_lines", []),
        }

    # Load opportunity data if needed
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

    # Load problem-diagnosis tools if needed
    if "problem-diagnosis" in route_to:
        knowledge_context["diagnosis_tools"] = {
            "stage_judgment": router._METHODOLOGY.get("stage_judgment", {}),
            "tools_available": {k: {"principle": v.get("principle"), "one_liner": v.get("one_liner")}
                                for k, v in router._METHODOLOGY.get("tools", {}).items()},
        }

    # Step 4: Build the consultation guide for the LLM
    result = {
        "type": "consultation",
        "user_situation": situation,
        "triage": {
            "detected_intents": triage_result.get("detected_intents", []),
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

    # Handle exhaustion first
    if triage_result.get("special_handling") == "exhaustion":
        steps.append(f"第{step_num}步：先处理情绪——用户明显疲惫/耗竭，建议先休息恢复2-4周再做决策。"
                     "用problem-diagnosis的「相持阶段」框架：这不是速胜也不是亡国，是相持，需要先保存有生力量。")
        step_num += 1

    for skill in route_to:
        if skill == "problem-diagnosis":
            steps.append(f"第{step_num}步：用problem-diagnosis诊断——还原用户真正的问题，"
                         "识别主要矛盾（不是表面问题），判断当前阶段（速决/相持/反攻），推荐策略工具。")
        elif skill == "industry-scan":
            cluster = info.get("cluster", "未识别")
            steps.append(f"第{step_num}步：用industry-scan扫描——用户行业={cluster}，"
                         "给出增/转/缩信号、岗位前景、地域因素、行动建议。")
        elif skill == "startup-feasibility":
            steps.append(f"第{step_num}步：用startup-feasibility评估——"
                         "先做劝退检查（7条），再匹配四条路径，给阶段建议和合规红线。")
        elif skill == "growth-planner":
            steps.append(f"第{step_num}步：用growth-planner规划——"
                         "匹配画像，定位学习层级，生成分阶段路线和关键节点。")
        elif skill == "collaboration-match":
            steps.append(f"第{step_num}步：用collaboration-match推荐——"
                         "诊断是否到了协作阶段，匹配形态，给分配建议和合规红线。")
        elif skill == "opportunity-radar":
            steps.append(f"第{step_num}步：用opportunity-radar前瞻——"
                         "映射到前瞻主题，给5-10年趋势判断，标出被低估的变量和不确定性。")
        step_num += 1

    steps.append(f"第{step_num}步：综合所有skill的输出，用温暖、朴素、有力的语言写一份完整判断。"
                 "必须包含：主要判断 + 行动建议（可操作的） + 风险红线 + 一句话总结。"
                 "记住：你是共富参谋，你的读者是一线劳动者，说人话，不灌鸡汤，不写术语。")

    return "\n".join(steps)
