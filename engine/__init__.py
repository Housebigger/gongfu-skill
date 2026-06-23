"""gongfu-skill plugin — registration."""

import logging
from pathlib import Path

from . import schemas, tools

logger = logging.getLogger(__name__)


def _on_pre_llm_call(session_id, user_message, conversation_history, is_first_turn, model, platform, **kwargs):
    """Inject a brief announcement on first turn so the agent knows gongfu_consult exists."""
    if not is_first_turn:
        return None

    return {
        "context": (
            "【共富参谋已加载】用户如果想了解行业前景、创业评估、职业困惑、成长规划、协作建议、"
            "趋势前瞻，可以调用 gongfu_consult 工具——直接传用户的原话即可，工具会自动路由和加载知识。"
        )
    }


def register(ctx):
    """Wire schema to handler and register hook."""
    ctx.register_tool(
        name="gongfu_consult",
        toolset="gongfu",
        schema=schemas.GONGFU_CONSULT,
        handler=tools.gongfu_consult,
    )

    ctx.register_hook("pre_llm_call", _on_pre_llm_call)

    # Register bundled skills
    skills_dir = Path(__file__).parent / "skills"
    if skills_dir.exists():
        for child in sorted(skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                ctx.register_skill(child.name, skill_md)
                logger.debug("gongfu-skill: registered skill %s", child.name)

    logger.info("gongfu-skill: registered gongfu_consult tool + %d skills",
                len(list(skills_dir.iterdir())) if skills_dir.exists() else 0)
