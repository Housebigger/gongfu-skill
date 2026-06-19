#!/bin/bash
# gongfu-skill 各平台一键安装脚本
# 用法：bash agents/install.sh
# 根据你的 agent 工具，选择安装方式。

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"

echo "共富参谋（gongfu-skill）平台适配安装"
echo "=========================================="
echo "仓库路径：$REPO"
echo ""
echo "请选择你要适配的平台："
echo "  1) Claude Code（MCP Server）"
echo "  2) Claude Code（静态知识包 → 放入项目）"
echo "  3) Codex CLI（AGENTS.md 指令 + MCP）"
echo "  4) ZCode（Skill 文件）"
echo "  5) 全部安装"
echo ""
read -p "输入序号 [1-5]: " choice

install_claude_mcp() {
    echo ""
    echo "--- Claude Code MCP Server ---"
    if command -v claude &>/dev/null; then
        claude mcp add gongfu-skill -- "$REPO/.venv/bin/python" "$REPO/mcp_server/server.py" 2>/dev/null && \
            echo "✓ 已通过 claude mcp add 注册" || \
            echo "（如已存在会跳过）"
    else
        echo "未检测到 claude CLI，请手动配置："
        echo "  claude mcp add gongfu-skill -- $REPO/.venv/bin/python $REPO/mcp_server/server.py"
    fi
    echo "  或用 JSON 配置文件：$REPO/agents/mcp-claude-code.json"
}

install_claude_static() {
    echo ""
    echo "--- Claude Code 静态知识包 ---"
    echo "把 claude-skills/ 目录放入你的项目根目录即可："
    echo "  cp -r $REPO/claude-skills /你的项目/"
    echo "Claude Code 会自动读取 CLAUDE.md。"
}

install_codex() {
    echo ""
    echo "--- Codex CLI ---"
    echo "方式一（AGENTS.md 指令）："
    echo "  cp $REPO/agents/AGENTS.md /你的项目/AGENTS.md"
    echo "  或放到全局：cp $REPO/agents/AGENTS.md ~/.codex/AGENTS.md"
    echo ""
    echo "方式二（MCP Server）："
    echo "  把以下内容追加到 ~/.codex/config.toml："
    echo "  [mcp_servers.gongfu_skill]"
    echo "  command = \"$REPO/.venv/bin/python\""
    echo "  args = [\"$REPO/mcp_server/server.py\"]"
    echo "  完整模板见：$REPO/agents/mcp-codex.toml"
}

install_zcode() {
    echo ""
    echo "--- ZCode Skills ---"
    local TARGET="$HOME/.zcode/skills"
    mkdir -p "$TARGET"
    for skill_dir in "$REPO"/agents/zcode-skills/*/; do
        skill_name=$(basename "$skill_dir")
        if [ -f "$skill_dir/SKILL.md" ]; then
            mkdir -p "$TARGET/$skill_name"
            cp "$skill_dir/SKILL.md" "$TARGET/$skill_name/SKILL.md"
            echo "  ✓ $skill_name"
        fi
    done
    echo ""
    echo "已安装到 $TARGET"
    echo "在 ZCode 中：Settings → Skills → Refresh，然后用 \$skill-name 调用。"
}

case $choice in
    1) install_claude_mcp ;;
    2) install_claude_static ;;
    3) install_codex ;;
    4) install_zcode ;;
    5) install_claude_mcp; install_claude_static; install_codex; install_zcode ;;
    *) echo "无效选择"; exit 1 ;;
esac

echo ""
echo "完成！"
