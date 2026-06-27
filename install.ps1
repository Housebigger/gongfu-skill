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
