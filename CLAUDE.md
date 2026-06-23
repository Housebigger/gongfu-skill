# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 全民共享，共同富裕。`gongfu` here means **共富 (common prosperity)**, not 功夫 (kung fu).

## What this repo is

Two things in one repo:

1. **A Chinese-language knowledge base** for front-line workers (行业判断 / 创业 / 成长 / 协作 / 趋势), organized as three "phases": `methodology/` (思想武器库) → `accumulation_settle/` (经验沉淀) → `strategy/` (现实建功). ~2000 markdown files.
2. **An engine** (`engine/`, Python) that distills that knowledge into one callable consulting tool — `gongfu_consult` — exposed through four interchangeable shells.

Almost all content is Chinese. Cluster IDs (`A-先进制造与硬科技` … `P-公用事业与市政服务`), intent names (`困境迷茫`/`行业判断`/`创业意向`/`成长需求`/`协作需求`/`趋势前瞻`), and the 7 inspiration themes are **stable identifiers** referenced from Python and YAML — do not rename them casually.

## Commands

There is **no build, lint, or automated test suite**. "Tests" are the Test Cases sections inside each `SKILL.md` (doc-based, run by a human/LLM). Verify code changes by running a shell and exercising `gongfu_consult` directly.

```bash
# Dev environment (Python 3.10+, project pins 3.12)
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install mcp pyyaml          # only two runtime deps; starlette/uvicorn come with mcp

# Run the MCP server (stdio) — what Claude Desktop / Cursor / Claude Code connect to
python mcp_server/server.py        # or: gongfu-mcp  (after pip install -e .)

# Run the HTTP API (Coze / Dify / FastGPT / custom agents)
python api_server/server.py                 # 127.0.0.1:8787
python api_server/server.py --host 0.0.0.0 --port 9000

# Smoke-test the engine end-to-end via HTTP
curl -X POST http://127.0.0.1:8787/consult \
  -H "Content-Type: application/json" \
  -d '{"situation":"我30岁在工厂干了10年，最近产线上了机器人，我怕被替代","mode":"intake"}'

# Smoke-test the engine directly (no server) — same synthetic-package trick the servers use
python -c "import sys,importlib,types; p=types.ModuleType('gongfu_engine'); \
p.__path__=['engine']; sys.modules['gongfu_engine']=p; \
print(importlib.import_module('gongfu_engine.tools').gongfu_consult({'situation':'我45岁钢铁厂下岗想转行','mode':'analyze'}))"

# Install as a Hermes plugin
./install.sh        # macOS/Linux   (.\install.ps1 on Windows)

# Regenerate derived skill packs after editing anything under skills/ (installers run this for you)
python scripts/build_packs.py
```

## Architecture

### One engine, four shells

The engine is `engine/` (top-level) and is the **single source of runtime logic**. The three non-Hermes shells load it verbatim through a synthetic package `gongfu_engine` (see the identical `_ENGINE_DIR = _REPO_ROOT / "engine"` / `sys.modules["gongfu_engine"]` bootstrap in `mcp_server/server.py` and `api_server/server.py`). They are pure adapters — no business logic. Change behavior in the engine once and all shells get it.

- `engine/` — Hermes plugin + the engine itself (`install.sh` symlinks this dir into `~/.hermes/plugins/gongfu-skill`)
- `mcp_server/server.py` — wraps the engine as MCP tool `gongfu_consult`
- `api_server/server.py` — wraps the engine as `POST /consult` (starlette)
- `claude-skills/` & `agents/` — static knowledge packs (LLM reads markdown; no Python runs)

### Engine internals (`engine/`)

```
schemas.py  — the tool description the LLM sees (single source for tool text)
router.py   — triage(): keyword classification of free-form Chinese text into
              intents → route_to skills, extracts cluster/region/age/finances/
              family/emotional_state, and loads knowledge. Crisis/exhaustion
              detection happens FIRST and short-circuits everything else.
tools.py    — gongfu_consult(): two modes, intake → analyze. Assembles
              knowledge_context + tone_instruction + execution_guide into JSON.
```

The tool returns **instructions for the LLM**, not finished prose — `tone_instruction` and `execution_guide` tell the calling model *how* to speak (counseling principles: listen-before-asking, strengths-first, gentle, non-judgmental, always leave an exit). Preserve this contract: the engine never writes the user-facing reply itself.

### Runtime data is read live (no rebuild step)

`router.py` reads knowledge from disk at runtime, so **adding content takes effect immediately**:

- `skills/data/*.yaml` — the structured knowledge the engine loads (`_DATA_DIR = <repo>/skills/data`, resolved from `engine/router.py`). 11 files: `industry-signals`, `startup-paths`, `growth-profiles`, `collaboration-forms`, `opportunities`, `methodology-tools`, `regional-matrix`, `counseling-principles`, plus `marxism-tools` / `deng-tools` / `xi-tools`.
- `methodology/cluster_frameworks/<cluster>.md` — loaded whole by `get_cluster_framework()`.
- `methodology/{marxism,deng_xiaoping_theory,mao_zedong_thought,xi_jinping_thought}/inspiration/*.md` — keyword-scored and excerpted at request time by `get_{marxism,deng,mao,xi}_inspiration()`. Mao's library is ~1547 files, so the Mao/Xi loaders go through a module-level cache (`_load_inspiration_dir`): each dir is read from disk **once** (first request that touches it), then scored in memory. marxism/deng (30 / 4 files) still scan per call.

Note: each system's `reference/` (原文) is source material humans distill *from*; what reaches the model is the distilled `*-tools.yaml` tool cards **plus** the live inspiration scan above. The multi-thought-system layering (马/毛/邓/习): 马克思主义=理论根基, 毛泽东思想=方法工具, 邓小平理论=务实行动, 习近平思想=方向 — all injected together in `_handle_analyze`.

### Single source + generated packs (read before editing skills or data)

`SKILL.md` and `data/*.yaml` feed four consumers (Hermes plugin, MCP/API runtime, Claude Code pack, ZCode/Codex pack). There is **exactly one source of truth** — everything else is generated.

| Path | Role |
|------|------|
| **`skills/<name>/SKILL.md` + `skills/data/*.yaml`** | **SOURCE — the only place you edit.** The running engine reads `skills/data/` directly. |
| `engine/skills/` | generated (Hermes plugin's bundled skills) — gitignored |
| `claude-skills/skills/` + `claude-skills/data/` | generated (Claude Code static pack) — gitignored |
| `agents/zcode-skills/` (skills + `data/`) | generated (ZCode pack) — gitignored |

**`scripts/build_packs.py`** regenerates all three derived locations from the source (stdlib-only, cross-platform, byte-identical copy). The three installers (`install.sh`, `install.ps1`, `agents/install.sh`) call it automatically; run it by hand after editing source:

```bash
python scripts/build_packs.py
```

Rules:
- **Never edit the generated copies** — your change will be overwritten on the next build.
- Edit a `SKILL.md` or YAML under `skills/`, then run `build_packs.py` (or any installer).
- A fresh `git clone` has no generated packs; MCP/API work anyway (they read `skills/data/` source). The Hermes plugin and the static packs need a build first — the installers handle it.
- `claude-skills/CLAUDE.md` and `agents/AGENTS.md`/`mcp-*.{json,toml}` are **hand-written**, not generated.

The `skills/00-skill设计规范.md` defines the required `SKILL.md` structure (frontmatter → overview → when-to-use → input → processing → output → **test cases** → source mapping → boundaries) and the five quality bars (可调用/可验证/可组合/可追溯/诚实).

## Conventions

- **Chinese first.** Prose, commit messages, and user-facing strings are Chinese. Keep `ensure_ascii=False` on every `json.dumps` (the API has a dedicated `ChineseJSONResponse` for this).
- **Per-directory READMEs are the navigation source of truth** — each layer (`methodology/`, `strategy/`, `accumulation_settle/`, and sub-layers) has its own `README.md`. Update it when you add files. READMEs must describe only what actually exists in the tree.
- Adding a new thought system → mirror the `reference/` + `inspiration/` (7-theme) structure under `methodology/<name>/`, add a `<name>-tools.yaml`, and wire `get_<name>_tools_for_cluster` / inspiration loaders into `router.py` + `_handle_analyze`.
- Place content by 用途/母题 (purpose/topic), not by date.
