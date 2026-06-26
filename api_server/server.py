"""gongfu-skill HTTP API Server

把共富参谋暴露为 HTTP API，适配 Coze / Dify / FastGPT / 自定义 agent 等
任何能发 HTTP 请求的平台。

基于 starlette + uvicorn（MCP SDK 已自带，零额外依赖）。

用法：
    python api_server/server.py                      # 默认 127.0.0.1:8787
    python api_server/server.py --host 0.0.0.0 --port 9000

接口：
    POST /consult    主接口，JSON body: {"situation": "...", "mode": "intake|analyze"}
    GET  /health     健康检查
    GET  /           API 信息
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# ── 加载引擎（同 MCP server，合成包方式）──────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
_ENGINE_DIR = _REPO_ROOT / "engine"

import importlib
import types

if "gongfu_engine" not in sys.modules:
    _pkg = types.ModuleType("gongfu_engine")
    _pkg.__path__ = [str(_ENGINE_DIR)]
    sys.modules["gongfu_engine"] = _pkg

schemas = importlib.import_module("gongfu_engine.schemas")
router = importlib.import_module("gongfu_engine.router")
tools = importlib.import_module("gongfu_engine.tools")

# ── HTTP 服务 ─────────────────────────────────────────────────────────
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger("gongfu-api")


class ChineseJSONResponse(Response):
    """JSONResponse with ensure_ascii=False — Chinese characters stay readable."""

    media_type = "application/json"

    def __init__(self, content, status_code: int = 200):
        super().__init__(
            content=json.dumps(content, ensure_ascii=False, indent=2),
            media_type=self.media_type,
            status_code=status_code,
        )


async def consult(request):
    """POST /consult — 共富参谋主接口

    Body: {"situation": "用户原话", "mode": "intake" | "analyze"}
    返回: engine 产出的 JSON（直接透传）
    """
    try:
        body = await request.json()
    except Exception:
        return ChineseJSONResponse({"error": "请求体必须是 JSON"}, status_code=400)

    situation = (body.get("situation") or "").strip()
    mode = body.get("mode", "intake")

    if not situation:
        return ChineseJSONResponse({"error": "请描述你的情况（situation 不能为空）"}, status_code=400)

    if mode not in ("intake", "analyze"):
        return ChineseJSONResponse({"error": "mode 只能是 intake 或 analyze"}, status_code=400)

    # 调用引擎
    raw = tools.gongfu_consult({"situation": situation, "mode": mode})
    result = json.loads(raw)

    status_code = 422 if "error" in result else 200
    return ChineseJSONResponse(result, status_code=status_code)


async def health(request):
    """GET /health — 健康检查"""
    return ChineseJSONResponse({"status": "ok", "engine": "gongfu-skill"})


async def index(request):
    """GET / — API 信息"""
    return ChineseJSONResponse({
        "name": "gongfu-skill 共富参谋 API",
        "version": "1.6.0",
        "endpoints": {
            "POST /consult": "主接口——传入用户情况，返回判断",
            "GET /health": "健康检查",
        },
        "usage": {
            "url": "/consult",
            "method": "POST",
            "body_example": {
                "situation": "我30岁在工厂干了10年，最近产线上了机器人，我怕被替代",
                "mode": "intake",
            },
        },
    })


def create_app() -> Starlette:
    middleware = [
        Middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["GET", "POST"],
                   allow_headers=["*"]),
    ]
    routes = [
        Route("/", index),
        Route("/health", health),
        Route("/consult", consult, methods=["POST"]),
    ]
    return Starlette(routes=routes, middleware=middleware)


def main():
    parser = argparse.ArgumentParser(description="gongfu-skill HTTP API")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址（默认 127.0.0.1）")
    parser.add_argument("--port", type=int, default=8787, help="监听端口（默认 8787）")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(message)s",
        stream=sys.stderr,
    )
    logger.info("gongfu-skill API starting on http://%s:%d", args.host, args.port)

    import uvicorn
    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
