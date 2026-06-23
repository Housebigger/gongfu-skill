"""gongfu-skill MCP Server

把共富参谋引擎暴露为标准 MCP tool，适配 Claude Desktop / Cursor / Cline /
Windsurf / Continue 等所有支持 MCP 的 agent 客户端。

引擎代码（router/tools/schemas）原样复用，零修改——本文件只是一个适配层。
"""

import importlib
import logging
import sys
import types
from pathlib import Path

# ── 1. 加载引擎（通过合成包，不触碰 Hermes 插件）──────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
_ENGINE_DIR = _REPO_ROOT / "engine"

if "gongfu_engine" not in sys.modules:
    # 创建合成包，让 engine 内部的 `from . import router` 相对导入能正常解析
    _pkg = types.ModuleType("gongfu_engine")
    _pkg.__path__ = [str(_ENGINE_DIR)]
    sys.modules["gongfu_engine"] = _pkg

schemas = importlib.import_module("gongfu_engine.schemas")
router = importlib.import_module("gongfu_engine.router")
tools = importlib.import_module("gongfu_engine.tools")

# ── 2. 创建 MCP Server ─────────────────────────────────────────────────
from mcp.server.fastmcp import FastMCP  # noqa: E402

logger = logging.getLogger("gongfu-mcp")

mcp = FastMCP(
    "gongfu-skill",
    instructions=(
        "共富参谋——劳动者的随身参谋。适用于：想了解行业前景、考虑创业、面临职业困境、"
        "规划成长路线、寻找合作机会、想看未来趋势。\n\n"
        "这个工具借鉴了心理咨询的原则：先倾听，再理解，最后才给建议。\n"
        "交互流程：先用 mode='intake' 分析用户情况，必要时温柔追问补充信息，"
        "信息充分后用 mode='analyze' 给出完整判断。"
    ),
)

# 从 schemas.py 取描述文本（保持单一信息源）
_TOOL_DESC = schemas.GONGFU_CONSULT["description"]


# ── 3. 注册 MCP Tool ───────────────────────────────────────────────────
@mcp.tool(name="gongfu_consult", description=_TOOL_DESC)
def gongfu_consult(situation: str, mode: str = "intake") -> str:
    """共富参谋主入口。

    Args:
        situation: 用户的原话描述。intake 模式传用户最初的说法；
                   如果已经追问过，传把用户所有回答拼在一起的完整描述。
        mode: intake=收集信息阶段（默认），analyze=分析输出阶段。
    """
    return tools.gongfu_consult({"situation": situation, "mode": mode})


# ── 4. 入口 ─────────────────────────────────────────────────────────────
def main():
    """stdio transport —— 所有 MCP 客户端的通用默认。"""
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    logger.info("gongfu-skill MCP server starting (stdio)…")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
