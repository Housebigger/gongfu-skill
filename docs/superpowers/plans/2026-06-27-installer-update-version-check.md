# 安装脚本版本检查 + `--update` 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 给 `install.sh` / `install.ps1` 加版本检查（当前 vs 最新）与显式 `--update`：默认对已安装系统只读检查+非交互提示，更新需 `--update`。

**Architecture:** 两个安装脚本重构为「参数解析 → 版本助手 → 默认/更新分支」；bash 用函数 + `main()` 守卫（可 `source` 单测），ps1 镜像同逻辑（`[switch]$Update` + `[version]` 比较）。引擎/接口/版本号均不动。

**Tech Stack:** bash（兼容 macOS 自带 3.2）、PowerShell；`curl`/`Invoke-WebRequest` 抓远程版本；标准 git。

**前置说明（执行者必读）：**
- 工作目录：仓库根 `/Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill`，命令在此根下跑。
- 分支：已在 `feat/installer-update-version-check`（spec 已提交于此）。
- **不改** `engine/`、`skills/`、`mcp_server/`、`api_server/`、`pyproject.toml`、`agents/install.sh`；**不升版本号**。
- 版本来源：`engine/plugin.yaml` 的 `version:`（当前为 `1.7.0`）。远程最新从 `https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/engine/plugin.yaml` 抓。
- `set -e` 只放进 `main()`，**不要**全局——否则 `source` 脚本做单测时会被助手的非零返回打断。
- 版本比较语义：`version_gt A B` 为真 ⇔ **B 严格大于 A**。

---

## Task 1: 重写 install.sh（结构化 + 版本检查 + --update）

**Files:**
- Rewrite: `install.sh`（整文件替换为下方内容）

- [ ] **Step 1: 用以下完整内容覆盖 `install.sh`**

```bash
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
```

- [ ] **Step 2: 语法检查**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
bash -n install.sh && echo "SYNTAX OK"
```
Expected: `SYNTAX OK`

- [ ] **Step 3: 助手函数单元自测（source 不触发安装）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
bash -c '
source ./install.sh
fail=0
version_gt 1.6.0 1.7.0  && echo ok1 || { echo FAIL1; fail=1; }
version_gt 1.7.0 1.7.0  && { echo FAIL2; fail=1; } || echo ok2
version_gt 1.7.0 1.6.0  && { echo FAIL3; fail=1; } || echo ok3
version_gt 1.9.0 1.10.0 && echo ok4 || { echo FAIL4; fail=1; }
version_gt 1.7.0 1.7.1  && echo ok5 || { echo FAIL5; fail=1; }
v=$(get_yaml_version engine/plugin.yaml); [ "$v" = "1.7.0" ] && echo ok6 || { echo "FAIL6 got=$v"; fail=1; }
exit $fail
' && echo "UNIT TESTS PASS"
```
Expected: `ok1 ok2 ok3 ok4 ok5 ok6` then `UNIT TESTS PASS`. (No installer output — confirms the `BASH_SOURCE` guard works.)

- [ ] **Step 4: --help 与未知参数**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
bash install.sh --help | head -3
echo "help_exit=$?"
bash install.sh --bogus >/tmp/gf_bogus.out 2>&1; echo "bogus_exit=$?"; grep -q "未知参数" /tmp/gf_bogus.out && echo "UNKNOWN ARG HANDLED"
```
Expected: 帮助前几行打印、`help_exit=0`；`bogus_exit=2` 且 `UNKNOWN ARG HANDLED`。

- [ ] **Step 5: 默认模式对「已安装」系统只读（仓库不被改动）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
TMPH=$(mktemp -d)
mkdir -p "$TMPH/plugins"
ln -s "$(pwd)/engine" "$TMPH/plugins/gongfu-skill"   # 模拟「已安装」
before=$(git status --porcelain)
HERMES_HOME="$TMPH" GONGFU_SKILL_DIR="$(pwd)" bash install.sh >/tmp/gf_check.out 2>&1 || true
after=$(git status --porcelain)
rm -rf "$TMPH"
[ "$before" = "$after" ] && echo "READONLY OK" || { echo "READONLY FAIL"; git status --porcelain; }
grep -Eq "当前 v|已是最新|无法获取最新版本|本地 v" /tmp/gf_check.out && echo "CHECK PRINTED" || { echo "CHECK NOT PRINTED"; cat /tmp/gf_check.out; }
```
Expected: `READONLY OK` 和 `CHECK PRINTED`（在线时打印「当前 v1.7.0 ｜ 最新 v1.7.0 / ✅ 已是最新」；离线时打印「无法获取最新版本」——都算通过）。**关键：仓库 git 状态零变化**。

> 不在此测真实 `--update`（会对当前仓库 `git pull`）——列入装后实测。

- [ ] **Step 6: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add install.sh
git commit -q -m "feat(install.sh): 版本检查 + --update（默认只读检查，更新需显式 --update）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: 重写 install.ps1（镜像 bash 逻辑）

**Files:**
- Rewrite: `install.ps1`（整文件替换为下方内容）

- [ ] **Step 1: 用以下完整内容覆盖 `install.ps1`**

```powershell
# gongfu-skill 共富参谋插件安装脚本（Windows PowerShell）
# 用法：
#   安装/检查（远程）： iwr -useb https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1 | iex
#   更新（远程）：       & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1))) -Update
#   本地：              .\install.ps1   /   .\install.ps1 -Update   /   .\install.ps1 -Help
param(
    [string]$GongfuDir = "",
    [switch]$Update,
    [switch]$Help
)
$ErrorActionPreference = "Stop"

# 兼容 --update / --help / -u / -h 字面量（curl|iex 习惯）
if ($args -contains '--update' -or $args -contains '-u') { $Update = $true }
if ($args -contains '--help'   -or $args -contains '-h') { $Help   = $true }

function Write-Info($m) { Write-Host "[gongfu] $m" -ForegroundColor Cyan }
function Write-Ok($m)   { Write-Host "[gongfu] $m" -ForegroundColor Green }
function Write-Warn($m)  { Write-Host "[gongfu] $m" -ForegroundColor Yellow }

$RepoUrl        = "https://github.com/Housebigger/gongfu-skill.git"
$CloneDir       = Join-Path $HOME ".gongfu-skill"
$RawInstallUrl  = "https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1"
$RawVersionUrl  = "https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/engine/plugin.yaml"

function Get-YamlVersion($path) {
    if (-not (Test-Path $path)) { return $null }
    $line = (Get-Content $path | Where-Object { $_ -match '^version:' } | Select-Object -First 1)
    if (-not $line) { return $null }
    return ($line -replace '^version:\s*','' -replace '["'']','').Trim()
}

function Get-RemoteVersion {
    try {
        $content = (Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 -Uri $RawVersionUrl).Content
        $line = ($content -split "`n" | Where-Object { $_ -match '^version:' } | Select-Object -First 1)
        if ($line) { return ($line -replace '^version:\s*','' -replace '["'']','').Trim() }
    } catch { return $null }
    return $null
}

# 返回 $true 当且仅当 $Remote 严格大于 $Local
function Test-VersionGt($Local, $Remote) {
    try { return ([version]$Remote -gt [version]$Local) } catch { return $false }
}

function Get-PluginsDir {
    if ($env:HERMES_HOME) { return (Join-Path $env:HERMES_HOME "plugins") }
    return (Join-Path (Join-Path $HOME ".hermes") "plugins")
}

function Test-Installed {
    return (Test-Path (Join-Path (Get-PluginsDir) "gongfu-skill"))
}

function Resolve-Repo($DoPull) {
    if ($GongfuDir -ne "" -and (Test-Path (Join-Path $GongfuDir "engine\plugin.yaml"))) {
        $script:RepoDir = $GongfuDir
        if ($DoPull -and (Test-Path (Join-Path $RepoDir ".git"))) {
            Push-Location $RepoDir; try { git pull --ff-only -q } catch { Write-Warn "git pull 失败，继续用现有内容" }; Pop-Location
        }
    } elseif (Test-Path (Join-Path $PWD "engine\plugin.yaml")) {
        $script:RepoDir = $PWD
        if ($DoPull -and (Test-Path (Join-Path $RepoDir ".git"))) {
            Push-Location $RepoDir; try { git pull --ff-only -q } catch { Write-Warn "git pull 失败，继续用现有内容" }; Pop-Location
        }
    } else {
        if (Test-Path (Join-Path $CloneDir ".git")) {
            $script:RepoDir = $CloneDir
            if ($DoPull) {
                Write-Info "拉取最新版本..."
                Push-Location $CloneDir; try { git pull --ff-only -q } catch { Write-Warn "git pull 失败，继续用现有内容" }; Pop-Location
            }
        } else {
            Write-Info "克隆仓库到 $CloneDir ..."
            git clone --depth 1 -q $RepoUrl $CloneDir
            $script:RepoDir = $CloneDir
        }
    }
}

function Invoke-BuildPacks {
    $build = Join-Path $RepoDir "scripts\build_packs.py"
    $py = Get-Command python3 -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
    if ($py -and (Test-Path $build)) {
        try {
            & $py.Source $build | Out-Null
            if ($LASTEXITCODE -eq 0) { Write-Ok "知识包已生成" } else { Write-Warn "知识包生成失败，可手动运行: python scripts\build_packs.py" }
        } catch { Write-Warn "知识包生成失败，可手动运行: python scripts\build_packs.py" }
    } else {
        Write-Warn "未找到 python，跳过知识包生成（可手动运行 python scripts\build_packs.py 补齐）"
    }
}

function Set-PluginLink {
    $pdir = Get-PluginsDir
    if (-not (Test-Path $pdir)) { New-Item -ItemType Directory -Path $pdir -Force | Out-Null }
    $target = Join-Path $pdir "gongfu-skill"
    $src = Join-Path $RepoDir "engine"
    if (Test-Path $target) { Write-Info "更新已有链接..."; Remove-Item $target -Force -Recurse }
    try {
        New-Item -ItemType SymbolicLink -Path $target -Target $src -ErrorAction Stop | Out-Null
        Write-Ok "插件已链接: $target -> $src"
    } catch {
        Write-Info "符号链接需要权限，尝试 Junction..."
        try {
            cmd /c mklink /J "$target" "$src" | Out-Null
            if (Test-Path $target) { Write-Ok "插件已链接（Junction）: $target -> $src" } else { throw "Junction 失败" }
        } catch {
            Write-Warn "自动链接失败，尝试复制文件..."
            Copy-Item -Path $src -Destination $target -Recurse -Force
            Write-Ok "插件已复制到: $target"
            Write-Warn "（注意：复制方式不支持自动更新，更新需重新运行本脚本 -Update）"
        }
    }
}

function Enable-Plugin {
    $hermes = Get-Command hermes -ErrorAction SilentlyContinue
    if ($hermes) {
        Write-Info "启用插件..."
        try { hermes plugins enable gongfu-skill 2>$null; Write-Ok "插件已启用" } catch { Write-Warn "启用失败，请手动运行: hermes plugins enable gongfu-skill" }
    } else {
        Write-Warn "未检测到 hermes 命令，请确认 Hermes Agent 已安装。"
        Write-Warn "安装后手动运行: hermes plugins enable gongfu-skill"
    }
}

function Show-Usage {
    Write-Host @"
gongfu-skill 安装脚本
用法：
  .\install.ps1            安装；若已安装则检查版本并提示
  .\install.ps1 -Update    拉取最新并更新（git pull + 重建知识包 + 重链 + 启用）
  .\install.ps1 -Help      显示本帮助

远程：
  安装/检查： iwr -useb $RawInstallUrl | iex
  更新：      & ([scriptblock]::Create((irm $RawInstallUrl))) -Update
"@
}

# ── 主流程 ──
if ($Help) { Show-Usage; return }

if ($Update) {
    Resolve-Repo $true
    $pluginYaml = Join-Path $RepoDir "engine\plugin.yaml"
    if (-not (Test-Path $pluginYaml)) { Write-Warn "找不到 $pluginYaml"; exit 1 }
    $newVer = Get-YamlVersion $pluginYaml
    Invoke-BuildPacks
    Set-PluginLink
    Enable-Plugin
    Write-Ok "✅ 已更新到 v$newVer"
    return
}

# 默认：install / check
Resolve-Repo $false
$pluginYaml = Join-Path $RepoDir "engine\plugin.yaml"
if (-not (Test-Path $pluginYaml)) { Write-Warn "找不到 $pluginYaml"; exit 1 }
$localVer  = Get-YamlVersion $pluginYaml
$remoteVer = Get-RemoteVersion

if (Test-Installed) {
    if (-not $remoteVer) {
        Write-Warn "无法获取最新版本（网络？），当前 v$localVer"
    } elseif (Test-VersionGt $localVer $remoteVer) {
        Write-Info "当前 v$localVer ｜ 最新 v$remoteVer"
        Write-Ok "👉 有新版本 v$remoteVer。更新： .\install.ps1 -Update   （远程： & ([scriptblock]::Create((irm $RawInstallUrl))) -Update）"
    } elseif (Test-VersionGt $remoteVer $localVer) {
        Write-Info "ℹ 本地 v$localVer 领先于发布版 v$remoteVer（可能是开发版）"
    } else {
        Write-Ok "✅ 已是最新 v$localVer"
    }
    return
}

# 未安装 / 链接缺失 → 首装或修复
Invoke-BuildPacks
Set-PluginLink
Enable-Plugin
Write-Host ""
Write-Ok "共富参谋安装完成！（v$localVer）"
Write-Host ""
Write-Host "  使用方法：" -ForegroundColor Cyan
Write-Host "    新开一个 Hermes 会话，直接用大白话描述你的情况，或： /gongfu-skill 我30岁想转行不知道行不行"
Write-Host ""
```

- [ ] **Step 2: 解析校验（有 pwsh 则解析；macOS 通常无 pwsh → 记为待 Windows 实测）**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
if command -v pwsh >/dev/null 2>&1; then
  pwsh -NoProfile -Command '$null=[System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path ./install.ps1), [ref]$null, [ref]$errs); if ($errs){ $errs; exit 1 } else { "PS PARSE OK" }'
else
  echo "pwsh 不可用——install.ps1 解析/全流程留待 Windows 实测"
fi
```
Expected: `PS PARSE OK`（有 pwsh 时）或打印「留待 Windows 实测」。

- [ ] **Step 3: 人工镜像核对**（对照 Task 1 的 bash 逻辑，确认分支语义一致：默认已安装→只读检查；`-Update`→pull+build+link+enable；`Test-VersionGt` 语义=Remote>Local）。

- [ ] **Step 4: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add install.ps1
git commit -q -m "feat(install.ps1): 版本检查 + -Update（镜像 install.sh 逻辑）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: README 更新（安装/更新说明）

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 更新「自动完成」描述行**

把：
```
脚本会自动完成克隆/更新、链接插件、启用插件。新开一个 Hermes 会话即可使用。
```
改为：
```
脚本会自动完成克隆、生成知识包、链接插件、启用插件。新开一个 Hermes 会话即可使用。若已安装，重跑脚本只做版本检查并提示（不自动改动）；更新见下方「更新与版本检查」。
```

- [ ] **Step 2: 在「从 v1.1.x 升级」提示之后插入「更新与版本检查」小节**

定位 README 现有这一行：
```
> **从 v1.1.x 升级**：引擎目录已改为 `engine/`，旧的符号链接会失效——重新运行上面的安装脚本即可重新链接。详见 [CHANGELOG.md](CHANGELOG.md)。
```
在它之后插入一个空行，再插入一个新小节，**结构如下**（你来写出正确的 Markdown 围栏，最终渲染为：一个标题 + 一段说明 + 一个 bash 代码块 + 一个 powershell 代码块）：

1) 三级标题：`### 更新与版本检查`
2) 一段说明文字（原文照写）：
   `重跑安装脚本（不加参数）对**已安装**系统是只读的：它会打印「当前版本 ｜ 最新版本」，有新版本时提示你更新，但**不会自动改动**。要真正更新，加 \`--update\`：`
3) 一个 **bash** 代码块，含这 6 行（注释行以 `#` 开头）：
   - `# macOS / Linux —— 检查版本`
   - `curl -fsSL https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh | bash`
   - `# macOS / Linux —— 执行更新（git pull + 重建知识包 + 重链 + 启用）`
   - `curl -fsSL https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh | bash -s -- --update`
   - `./install.sh            # 本地：检查`
   - `./install.sh --update   # 本地：更新`
4) 一个 **powershell** 代码块，含这 4 行：
   - `# Windows —— 检查版本`
   - `iwr -useb https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1 | iex`
   - `# Windows —— 执行更新`
   - `& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1))) -Update`

写完后用编辑器/预览确认两个代码块的 ```` ``` ```` 围栏成对闭合、互不嵌套。

- [ ] **Step 3: 核对并提交**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
grep -nF "更新与版本检查" README.md
grep -nF "bash -s -- --update" README.md
grep -nF "scriptblock]::Create" README.md
```
Expected: 三个 grep 各命中。
```bash
git add README.md
git commit -q -m "docs(readme): 安装/更新说明——版本检查 + --update 用法

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: CHANGELOG `[未发布]` 记录

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: 在 `## [未发布]` 段下记录本次改动**

读 `CHANGELOG.md`。若存在 `## [未发布]` 段（在 `## [1.7.0]` 之上），在其下加入下方条目；若 `[未发布]` 段不存在，则在 `## [1.7.0] - 2026-06-27` 之上新建 `## [未发布]` 段再加入：
```markdown
### Added
- **安装脚本版本检查 + `--update`**（`install.sh` / `install.ps1`）：默认运行对已安装系统只读——打印「当前版本 ｜ 最新版本」并在有新版本时提示；更新需显式 `--update`（远程 `curl … | bash -s -- --update` / `… -Update`）。远程版本抓取 best-effort + 超时降级。引擎/接口/版本号不变。
```
（这是知识/工具增量，按惯例不升版本号，随下个真实版本发布。）

- [ ] **Step 2: 提交**

```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git add CHANGELOG.md
git commit -q -m "docs(changelog): 记录安装脚本版本检查 + --update（未发布）

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: 最终验收扫描（控制器）

**Files:** 无改动（只读校验）。

- [ ] **Step 1: 两脚本语法 + 助手单测 + 范围确认**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
bash -n install.sh && echo "SH SYNTAX OK"
bash -c 'source ./install.sh; version_gt 1.6.0 1.7.0 && version_gt 1.7.0 1.7.1 && ! version_gt 1.7.0 1.7.0 && [ "$(get_yaml_version engine/plugin.yaml)" = "1.7.0" ] && echo "HELPERS OK"'
echo "--- 确认未触碰引擎/接口/版本号 ---"
git diff main...HEAD --name-only | sort
echo "--- 版本号仍 1.7.0、未被改动 ---"
grep -nF '1.7.0' pyproject.toml engine/plugin.yaml | head
```
Expected: `SH SYNTAX OK`、`HELPERS OK`；改动文件清单只含 `install.sh`、`install.ps1`、`README.md`、`CHANGELOG.md`、`docs/superpowers/...`（spec/plan）；版本号仍 1.7.0。

- [ ] **Step 2: git 干净 + 提交历史**

Run:
```bash
cd /Users/housebigger/Documents/01_work/playground_hermes/gongfu-skill
git status --porcelain && echo "[clean]"
git log --oneline main..HEAD
```
Expected: 工作树干净；分支含 spec + 4 个实现提交。

---

## 验收标准（全绿即完成）

1. `install.sh`：`bash -n` 过；`source` 后 `version_gt` / `get_yaml_version` 单测全过；`--help` 退出 0、未知参数退出 2；默认模式对「已安装」系统只读（仓库 git 状态零变化）并打印版本检查。
2. `install.ps1`：结构与 bash 镜像；有 pwsh 则解析通过（无则记装后实测）。
3. README 有「更新与版本检查」小节，含 bash/ps1 更新命令。
4. CHANGELOG `[未发布]` 记录本次改动；**版本号未升**（仍 1.7.0）。
5. `git diff main...HEAD` 只触及 install.sh / install.ps1 / README.md / CHANGELOG.md / docs。

## 装后实测（交付项，本环境无法验证）

- Windows 上 `install.ps1` 全流程（解析、符号链接/Junction/复制 fallback、`-Update`、`--update` 字面量兼容、`iex` + scriptblock 传参）。
- 真实 `--update`：`git pull` + Hermes `enable` + `vOld → vNew` 报告。
- `curl -fsSL … | bash -s -- --update` 端到端。
- 离线/限流时的版本抓取降级提示。
