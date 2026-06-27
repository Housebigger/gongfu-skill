#!/usr/bin/env bash
# gongfu-skill 共富参谋插件安装脚本
# 用法：
#   安装/检查更新（远程一键）：
#     curl -fsSL https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh | bash
#   更新（远程）：
#     curl -fsSL https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh | bash -s -- --update
#   本地（已 clone）：
#     ./install.sh            # 安装；若已安装则检查版本并提示
#     ./install.sh --update   # 拉取最新并更新

# ── 颜色 ──
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[gongfu]${NC} $1"; }
ok()    { echo -e "${GREEN}[gongfu]${NC} $1"; }
warn()  { echo -e "${YELLOW}[gongfu]${NC} $1"; }

REPO_URL="https://github.com/Housebigger/gongfu-skill.git"
CLONE_DIR="$HOME/.gongfu-skill"
RAW_INSTALL_URL="https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh"
RAW_VERSION_URL="https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/engine/plugin.yaml"

# ── 版本助手（可被 source 单测）──
# 解析 plugin.yaml 的 version:（去引号/去空白）
get_yaml_version() {
    [ -f "$1" ] || return 0
    grep -E '^version:' "$1" | head -1 | sed -E 's/^version:[[:space:]]*//; s/["'"'"']//g; s/[[:space:]]*$//'
}

# 抓远程最新版本（best-effort，5s 超时；失败/无 curl → 输出空、返回 0）
get_remote_version() {
    command -v curl >/dev/null 2>&1 || return 0
    local out
    out="$(curl -fsSL --max-time 5 "$RAW_VERSION_URL" 2>/dev/null | grep -E '^version:' | head -1 | sed -E 's/^version:[[:space:]]*//; s/["'"'"']//g; s/[[:space:]]*$//')" || true
    printf '%s' "$out"
}

# version_gt A B : 返回 0(true) 当且仅当 B 严格大于 A（语义化 X.Y.Z）
version_gt() {
    if [ "$1" = "$2" ]; then return 1; fi
    local a1 a2 a3 b1 b2 b3 rest
    IFS=. read -r a1 a2 a3 rest <<< "$1"
    IFS=. read -r b1 b2 b3 rest <<< "$2"
    a1=${a1//[!0-9]/}; a2=${a2//[!0-9]/}; a3=${a3//[!0-9]/}
    b1=${b1//[!0-9]/}; b2=${b2//[!0-9]/}; b3=${b3//[!0-9]/}
    a1=${a1:-0}; a2=${a2:-0}; a3=${a3:-0}
    b1=${b1:-0}; b2=${b2:-0}; b3=${b3:-0}
    if [ "$b1" -ne "$a1" ]; then if [ "$b1" -gt "$a1" ]; then return 0; else return 1; fi; fi
    if [ "$b2" -ne "$a2" ]; then if [ "$b2" -gt "$a2" ]; then return 0; else return 1; fi; fi
    if [ "$b3" -ne "$a3" ]; then if [ "$b3" -gt "$a3" ]; then return 0; else return 1; fi; fi
    return 1
}

# ── 流程函数 ──
plugins_dir() {
    if [ -n "$HERMES_HOME" ]; then echo "$HERMES_HOME/plugins"; else echo "$HOME/.hermes/plugins"; fi
}

is_installed() {
    local t; t="$(plugins_dir)/gongfu-skill"
    [ -e "$t" ] || [ -L "$t" ]
}

# 定位仓库到 REPO_DIR；参数 "pull"=允许对已有 clone 拉取，"nopull"=不拉取
resolve_repo() {
    local do_pull="$1"
    if [ -n "$GONGFU_SKILL_DIR" ]; then
        REPO_DIR="$GONGFU_SKILL_DIR"
        if [ "$do_pull" = "pull" ] && [ -d "$REPO_DIR/.git" ]; then
            ( cd "$REPO_DIR" && git pull --ff-only -q ) || warn "git pull 失败（网络或非快进），继续用现有内容"
        fi
    elif [ -f "$(dirname "$0")/engine/plugin.yaml" ]; then
        REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
        if [ "$do_pull" = "pull" ] && [ -d "$REPO_DIR/.git" ]; then
            ( cd "$REPO_DIR" && git pull --ff-only -q ) || warn "git pull 失败（网络或非快进），继续用现有内容"
        fi
    else
        if [ -d "$CLONE_DIR/.git" ]; then
            REPO_DIR="$CLONE_DIR"
            if [ "$do_pull" = "pull" ]; then
                info "拉取最新版本..."
                ( cd "$CLONE_DIR" && git pull --ff-only -q ) || warn "git pull 失败（网络或非快进），继续用现有内容"
            fi
        else
            info "克隆仓库到 $CLONE_DIR ..."
            git clone --depth 1 -q "$REPO_URL" "$CLONE_DIR"
            REPO_DIR="$CLONE_DIR"
        fi
    fi
}

build_packs() {
    local py=""
    if command -v python3 >/dev/null 2>&1; then py=python3
    elif command -v python >/dev/null 2>&1; then py=python; fi
    if [ -n "$py" ]; then
        "$py" "$REPO_DIR/scripts/build_packs.py" >/dev/null 2>&1 \
            && ok "知识包已生成" \
            || warn "知识包生成失败，可手动运行: python scripts/build_packs.py"
    else
        warn "未找到 python，跳过知识包生成（可手动运行 python scripts/build_packs.py 补齐）"
    fi
}

link_plugin() {
    local pdir target
    pdir="$(plugins_dir)"
    mkdir -p "$pdir"
    target="$pdir/gongfu-skill"
    if [ -L "$target" ] || [ -d "$target" ]; then
        info "更新已有链接..."
        rm -rf "$target"
    fi
    ln -sf "$REPO_DIR/engine" "$target"
    ok "插件已链接: $target → $REPO_DIR/engine"
}

enable_plugin() {
    if command -v hermes >/dev/null 2>&1; then
        info "启用插件..."
        hermes plugins enable gongfu-skill 2>/dev/null && ok "插件已启用" || warn "启用失败，请手动运行: hermes plugins enable gongfu-skill"
    else
        warn "未检测到 hermes 命令，请确认 Hermes Agent 已安装。"
        warn "安装后手动运行: hermes plugins enable gongfu-skill"
    fi
}

usage() {
    cat <<USAGE
gongfu-skill 安装脚本
用法：
  ./install.sh            安装；若已安装则检查版本并提示
  ./install.sh --update   拉取最新并更新（git pull + 重建知识包 + 重链 + 启用）
  ./install.sh --help     显示本帮助

远程：
  安装/检查： curl -fsSL $RAW_INSTALL_URL | bash
  更新：      curl -fsSL $RAW_INSTALL_URL | bash -s -- --update
USAGE
}

main() {
    set -e
    case "${1:-}" in
        --update|-u) MODE=update ;;
        --help|-h)   usage; return 0 ;;
        "")          MODE=install ;;
        *)           warn "未知参数: $1"; usage; return 2 ;;
    esac

    if [ "$MODE" = "update" ]; then
        resolve_repo pull
        if [ ! -f "$REPO_DIR/engine/plugin.yaml" ]; then
            warn "找不到 $REPO_DIR/engine/plugin.yaml，请检查仓库完整性。"; return 1
        fi
        local new_ver; new_ver="$(get_yaml_version "$REPO_DIR/engine/plugin.yaml" || true)"
        build_packs
        link_plugin
        enable_plugin
        ok "✅ 已更新到 v${new_ver:-未知}"
        return 0
    fi

    # 默认：install / check
    resolve_repo nopull
    if [ ! -f "$REPO_DIR/engine/plugin.yaml" ]; then
        warn "找不到 $REPO_DIR/engine/plugin.yaml，请检查仓库完整性。"; return 1
    fi
    local local_ver remote_ver
    local_ver="$(get_yaml_version "$REPO_DIR/engine/plugin.yaml" || true)"
    remote_ver="$(get_remote_version || true)"

    if is_installed; then
        if [ -z "$remote_ver" ]; then
            warn "无法获取最新版本（网络？），当前 v${local_ver:-未知}"
        elif version_gt "$local_ver" "$remote_ver"; then
            info "当前 v$local_ver ｜ 最新 v$remote_ver"
            ok "👉 有新版本 v$remote_ver。更新： ./install.sh --update   （远程： curl -fsSL $RAW_INSTALL_URL | bash -s -- --update）"
        elif version_gt "$remote_ver" "$local_ver"; then
            info "ℹ 本地 v$local_ver 领先于发布版 v$remote_ver（可能是开发版）"
        else
            ok "✅ 已是最新 v$local_ver"
        fi
        return 0
    fi

    # 未安装 / 链接缺失 → 首装或修复
    build_packs
    link_plugin
    enable_plugin
    echo ""
    ok "共富参谋安装完成！（v${local_ver:-未知}）"
    echo ""
    echo -e "  ${CYAN}使用方法：${NC}"
    echo "    新开一个 Hermes 会话，直接用大白话描述你的情况，或： /gongfu-skill 我30岁想转行不知道行不行"
    echo ""
}

# 仅当被直接执行时运行 main；被 source（如单测）时只定义函数
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
