#!/usr/bin/env bash
# gongfu-skill 共富参谋插件安装脚本
# 用法（远程一键安装）：
#   curl -fsSL https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh | bash
# 用法（本地已 clone）：
#   ./install.sh
set -e

# ── 颜色 ──
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[gongfu]${NC} $1"; }
ok()    { echo -e "${GREEN}[gongfu]${NC} $1"; }
warn()  { echo -e "${YELLOW}[gongfu]${NC} $1"; }

# ── 定位仓库目录 ──
REPO_URL="https://github.com/Housebigger/gongfu-skill.git"
CLONE_DIR="$HOME/.gongfu-skill"

if [ -n "$GONGFU_SKILL_DIR" ]; then
    # 环境变量指定了仓库路径
    REPO_DIR="$GONGFU_SKILL_DIR"
elif [ -f "$(dirname "$0")/skills/gongfu-skill/plugin.yaml" ]; then
    # 本地运行（已 clone，脚本在仓库根目录）
    REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
else
    # 远程运行（curl | bash），需要 clone
    if [ -d "$CLONE_DIR/.git" ]; then
        info "检测到已有仓库，拉取最新版本..."
        cd "$CLONE_DIR" && git pull --ff-only -q
        REPO_DIR="$CLONE_DIR"
    else
        info "克隆仓库到 $CLONE_DIR ..."
        git clone --depth 1 -q "$REPO_URL" "$CLONE_DIR"
        REPO_DIR="$CLONE_DIR"
    fi
fi

PLUGIN_SRC="$REPO_DIR/skills/gongfu-skill"

if [ ! -f "$PLUGIN_SRC/plugin.yaml" ]; then
    warn "找不到插件文件: $PLUGIN_SRC/plugin.yaml"
    warn "请确认仓库完整或重新运行安装脚本。"
    exit 1
fi

ok "仓库就绪: $REPO_DIR"

# ── 定位 Hermes 插件目录 ──
if [ -n "$HERMES_HOME" ]; then
    PLUGINS_DIR="$HERMES_HOME/plugins"
else
    PLUGINS_DIR="$HOME/.hermes/plugins"
fi

mkdir -p "$PLUGINS_DIR"

# ── 创建符号链接 ──
LINK_TARGET="$PLUGINS_DIR/gongfu-skill"

if [ -L "$LINK_TARGET" ] || [ -d "$LINK_TARGET" ]; then
    info "更新已有链接..."
    rm -rf "$LINK_TARGET"
fi

ln -sf "$PLUGIN_SRC" "$LINK_TARGET"
ok "插件已链接: $LINK_TARGET → $PLUGIN_SRC"

# ── 启用插件 ──
if command -v hermes &>/dev/null; then
    info "启用插件..."
    hermes plugins enable gongfu-skill 2>/dev/null && ok "插件已启用" || warn "启用失败，请手动运行: hermes plugins enable gongfu-skill"
else
    warn "未检测到 hermes 命令，请确认 Hermes Agent 已安装。"
    warn "安装后手动运行: hermes plugins enable gongfu-skill"
fi

# ── 完成 ──
echo ""
ok "共富参谋安装完成！"
echo ""
echo -e "  ${CYAN}使用方法：${NC}"
echo "    新开一个 Hermes 会话（hermes 或 /reset），直接用大白话描述你的情况即可。"
echo ""
echo -e "  ${CYAN}示例：${NC}"
echo "    > 我30岁做嵌入式开发，同事都走了，很累，不知道该不该换"
echo "    > 想在县城开个养老服务机构，不知道行不行"
echo "    > 未来5年AI会不会替代我的工作"
echo ""
