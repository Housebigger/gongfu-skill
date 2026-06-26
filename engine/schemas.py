"""Tool schemas — what the LLM sees."""

GONGFU_CONSULT = {
    "name": "gongfu_consult",
    "description": (
        "共富参谋——劳动者的随身参谋。适用于：想了解行业前景、考虑创业、面临职业困境、"
        "规划成长路线、寻找合作机会、想看未来趋势。\n\n"
        "这个工具借鉴了心理咨询的原则：先倾听，再理解，最后才给建议。"
        "来找你咨询的人可能已经在现实中扛了很久了——"
        "你的第一句话应该让他感到被听到，而不是被追问。\n\n"
        "有两种模式：\n"
        "- mode='intake'（默认）：初次收到用户描述时调用。分析用户情况，识别意图，"
        "提取已知信息，评估情绪状态和信息完整度。如果用户情绪低落/疲惫，"
        "返回的指令会让你先确认感受而不是追问信息。如果信息不够，"
        "返回需要追问的问题（一次只问一个，用温柔的方式）。\n"
        "- mode='analyze'：信息收集充分后调用。加载知识库，产出完整判断。"
        "输出会先说用户的优势，再给建议，最后留退路。\n\n"
        "交互流程：intake → 确认感受 → 温柔追问 → 确认全景图 → analyze → 温暖的判断。\n"
        "两种特殊返回：信息过少时返回 need_basic_info（先请补行业/城市/诉求，不分析）；"
        "检测到情绪危机时返回 crisis（不做职业判断、提供热线）。两者结构与常规返回不同。\n"
        "直接传用户的原话就行，不用纠结分类。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "situation": {
                "type": "string",
                "description": (
                    "用户的原话描述。在 intake 模式下传用户最初的说法；"
                    "如果已经追问过，传把用户所有回答拼在一起的完整描述。"
                ),
            },
            "mode": {
                "type": "string",
                "enum": ["intake", "analyze"],
                "description": "intake=收集信息阶段（默认），analyze=分析输出阶段",
                "default": "intake",
            },
        },
        "required": ["situation"],
    },
}
