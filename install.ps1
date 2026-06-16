# gongfu-skill 共富参谋插件安装脚本（Windows PowerShell）
# 用法（远程一键安装）：
#   iwr -useb https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1 | iex
# 用法（本地已 clone）：
#   .\install.ps1
param(
    [string]$GongfuDir = ""
)

$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "[gongfu] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[gongfu] $msg" -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host "[gongfu] $msg" -ForegroundColor Yellow }

# ── 定位仓库目录 ──
$RepoUrl = "https://github.com/Housebigger/gongfu-skill.git"
$CloneDir = Join-Path $HOME ".gongfu-skill"

if ($GongfuDir -ne "" -and (Test-Path (Join-Path $GongfuDir "skills\gongfu-consultant\plugin.yaml"))) {
    $RepoDir = $GongfuDir
} elseif (Test-Path (Join-Path $PWD "skills\gongfu-consultant\plugin.yaml")) {
    # 本地运行（已 clone，脚本在仓库根目录）
    $RepoDir = $PWD
} else {
    # 远程运行，需要 clone
    if (Test-Path (Join-Path $CloneDir ".git")) {
        Write-Info "检测到已有仓库，拉取最新版本..."
        Push-Location $CloneDir
        git pull --ff-only -q
        Pop-Location
        $RepoDir = $CloneDir
    } else {
        Write-Info "克隆仓库到 $CloneDir ..."
        git clone --depth 1 -q $RepoUrl $CloneDir
        $RepoDir = $CloneDir
    }
}

$PluginSrc = Join-Path $RepoDir "skills\gongfu-consultant"
$PluginYaml = Join-Path $PluginSrc "plugin.yaml"

if (-not (Test-Path $PluginYaml)) {
    Write-Warn "找不到插件文件: $PluginYaml"
    Write-Warn "请确认仓库完整或重新运行安装脚本。"
    exit 1
}

Write-Ok "仓库就绪: $RepoDir"

# ── 定位 Hermes 插件目录 ──
$HermesHome = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path $HOME ".hermes" }
$PluginsDir = Join-Path $HermesHome "plugins"

if (-not (Test-Path $PluginsDir)) {
    New-Item -ItemType Directory -Path $PluginsDir -Force | Out-Null
}

# ── 创建符号链接（Windows 需要开发者模式或管理员权限） ──
$LinkTarget = Join-Path $PluginsDir "gongfu-consultant"

# 先清理已有链接
if (Test-Path $LinkTarget) {
    Write-Info "更新已有链接..."
    Remove-Item $LinkTarget -Force -Recurse
}

# Windows 符号链接需要权限，用 Junction（目录连接）作为 fallback
try {
    New-Item -ItemType SymbolicLink -Path $LinkTarget -Target $PluginSrc -ErrorAction Stop | Out-Null
    Write-Ok "插件已链接: $LinkTarget -> $PluginSrc"
} catch {
    Write-Info "符号链接需要权限，尝试 Junction..."
    try {
        cmd /c mklink /J "$LinkTarget" "$PluginSrc" | Out-Null
        if (Test-Path $LinkTarget) {
            Write-Ok "插件已链接（Junction）: $LinkTarget -> $PluginSrc"
        } else {
            throw "Junction 创建失败"
        }
    } catch {
        Write-Warn "自动链接失败，尝试复制文件..."
        Copy-Item -Path $PluginSrc -Destination $LinkTarget -Recurse -Force
        Write-Ok "插件已复制到: $LinkTarget"
        Write-Warn "（注意：复制方式不支持 git pull 自动更新，更新需重新运行本脚本）"
    }
}

# ── 启用插件 ──
$hermesCmd = Get-Command hermes -ErrorAction SilentlyContinue
if ($hermesCmd) {
    Write-Info "启用插件..."
    try {
        hermes plugins enable gongfu-consultant 2>$null
        Write-Ok "插件已启用"
    } catch {
        Write-Warn "启用失败，请手动运行: hermes plugins enable gongfu-consultant"
    }
} else {
    Write-Warn "未检测到 hermes 命令，请确认 Hermes Agent 已安装。"
    Write-Warn "安装后手动运行: hermes plugins enable gongfu-consultant"
}

# ── 完成 ──
Write-Host ""
Write-Ok "共富参谋安装完成！"
Write-Host ""
Write-Host "  使用方法：" -ForegroundColor Cyan
Write-Host "    新开一个 Hermes 会话（hermes 或 /reset），直接用大白话描述你的情况即可。"
Write-Host ""
Write-Host "  示例：" -ForegroundColor Cyan
Write-Host "    > 我30岁做嵌入式开发，同事都走了，很累，不知道该不该换"
Write-Host "    > 想在县城开个养老服务机构，不知道行不行"
Write-Host "    > 未来5年AI会不会替代我的工作"
Write-Host ""
