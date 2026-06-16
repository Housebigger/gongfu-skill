"""Tool schemas — what the LLM sees."""

GONGFU_CONSULT = {
    "name": "gongfu_consult",
    "description": (
        "共富参谋——劳动者的随身参谋。适用于：想了解行业前景、考虑创业、面临职业困境、"
        "规划成长路线、寻找合作机会、想看未来趋势。\n\n"
        "有两种模式：\n"
        "- mode='intake'（默认）：初次收到用户描述时调用。分析用户情况，识别意图，"
        "提取已知信息，列出还缺什么，并给出需要追问的问题（一次只问一个）。"
        "收到返回后，你要用自然对话的方式向用户提问，不要一次性抛出所有问题。\n"
        "- mode='analyze'：信息收集充分后调用。加载知识库，产出完整判断。\n\n"
        "交互流程：intake → 追问补充 → intake（再次评估） → 信息够了 → analyze → 输出判断。\n"
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
