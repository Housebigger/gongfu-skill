"""Tool schemas — what the LLM sees."""

GONGFU_CONSULT = {
    "name": "gongfu_consult",
    "description": (
        "共富参谋——劳动者的随身参谋。适用于：想了解行业前景、考虑创业、面临职业困境、"
        "规划成长路线、寻找合作机会、想看未来趋势。直接用大白话描述你的情况就行，"
        "不用纠结分类。例如：'我30岁做嵌入式开发，同事都走了，很累' 或 '想在县城开个养老服务机构'。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "situation": {
                "type": "string",
                "description": (
                    "用你自己的话描述你的情况——你的行业、岗位、城市、困惑、想解决的问题。"
                    "越具体判断越准确。"
                ),
            }
        },
        "required": ["situation"],
    },
}
