# 设计：安装脚本加版本检查 + `--update`

- **日期**：2026-06-27
- **类型**：分发工具（安装脚本）增强 — **不升版本**（记入 CHANGELOG `[未发布]`）
- **状态**：已通过 brainstorm 评审，待写 plan
- **范围**：`install.sh`（macOS/Linux）、`install.ps1`（Windows）+ `README.md` 文档 + `CHANGELOG.md`。**不动** `agents/install.sh`。

## 1. 背景与问题

当前安装脚本（`install.sh` / `install.ps1`）在**远程一键运行**时：若 `~/.gongfu-skill` 已存在则 `git pull --ff-only`，再 build_packs → 链接 → 启用；**本地** `./install.sh` 不 pull。问题：

- 用户无法在不改动系统的前提下**得知是否有新版本**（没有版本检查）。
- 更新动作是隐式的（重跑脚本顺带 pull），没有显式、可预测的「更新」入口。

目标：加 **版本检查**（告诉用户当前版本 vs 最新版本）+ 显式 **`--update`**（执行更新）。

## 2. 决策记录（brainstorm）

1. **默认只检查+提示，`--update` 才更新**。默认运行对**已安装**系统只读：打印版本对比 + 非交互更新提示，不改动。更新需显式 `--update`。
2. **范围 = `install.sh` + `install.ps1`**（两个 Hermes 插件安装脚本，跨平台对齐）。`agents/install.sh`（ZCode/Codex 选择器）不动。
3. **不升版本**：安装脚本是分发工具，非引擎/接口/结构变更。改动记入 CHANGELOG `[未发布]`，随下个真实版本发布。
4. **非交互**：`curl|bash` / `iwr|iex` 下 stdin 即脚本本身，无法可靠交互询问 → 「提示」一律**非交互打印**（不做 y/N）。

## 3. 行为规格

### 3.1 默认模式（无参数）— 对已安装系统只读

1. **定位仓库**（同现状）：`GONGFU_SKILL_DIR` 环境变量 → 本地（脚本在仓库根）→ 远程克隆目录 `~/.gongfu-skill`。**变化**：远程分支若 clone 已存在，**不再 `git pull`**（仅在缺失时 clone=首装）。
2. **读版本**：
   - `LOCAL_VER` = 解析 `<REPO_DIR>/engine/plugin.yaml` 的 `version:`（即当前/已装版本，因为 Hermes 链接指向该 `engine/`）。
   - `REMOTE_VER` = `curl -fsSL --max-time 5`（ps1：`iwr -TimeoutSec 5`）拉取 `https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/engine/plugin.yaml` 并解析 `version:`。**best-effort**：失败则置空。
3. **判定已安装** = Hermes 插件链接 `<PLUGINS_DIR>/gongfu-skill` 已存在（`-e` 或符号链接存在）。
   - **已安装**：
     - 打印 `当前 vLOCAL ｜ 最新 vREMOTE`。
     - 若 `REMOTE_VER` 为空 → 打印 `⚠ 无法获取最新版本（网络？），当前 vLOCAL`。
     - 否则按语义化比较：
       - `REMOTE > LOCAL` → 打印 `👉 有新版本 vREMOTE（当前 vLOCAL）。运行更新：<更新命令>`。
       - `REMOTE == LOCAL` → 打印 `✅ 已是最新 vLOCAL`。
       - `REMOTE < LOCAL` → 打印 `ℹ 本地版本 vLOCAL 领先于发布版 vREMOTE（可能是开发版）`。
     - **退出 0，不做任何改动**（不 build、不重链、不 enable）。
   - **未安装 / 链接缺失**（首装或修复）：执行现有流程 build_packs → 链接 → 启用 → 打印完成 + `已安装 vLOCAL`。

### 3.2 `--update` 模式 — 执行更新

1. **定位仓库**（缺则 clone）。
2. 记录 `OLD_VER` = `<REPO_DIR>/engine/plugin.yaml` 版本。
3. 若 `<REPO_DIR>/.git` 存在 → `git pull --ff-only`（本地/远程都 pull）。pull 失败（网络/非快进）→ 温和警告并继续用现有内容（不中断）。
4. `NEW_VER` = pull 后再次解析版本。
5. build_packs → 刷新链接 → 启用。
6. 打印：`OLD_VER != NEW_VER` → `✅ 已更新 vOLD → vNEW`；否则 `✅ 已是最新 vNEW`。

> `--update` 在**完全未安装**时等价于「安装最新版」（clone + build + link + enable），并报告 `已安装 vNEW`。

### 3.3 `--help`

打印简短用法：默认=安装/检查更新；`--update`=拉取并更新；`--help`=帮助。含远程传参示例。不实现 `--check`（默认即检查，YAGNI）。

### 3.4 参数解析与跨平台传参

- `install.sh`：解析 `$1`/`$@` 中的 `--update`、`--help`（`-h`）。未知参数 → 打印用法并退出非 0。
- `install.ps1`：`param([switch]$Update, [switch]$Help)`；**同时**扫描 `$args` 兼容 `--update`/`--help` 字面量（muscle-memory 对齐）。
- 文档化的更新命令（写入 README）：
  - macOS/Linux 远程：`curl -fsSL https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.sh | bash -s -- --update`
  - Windows 远程：`& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Housebigger/gongfu-skill/main/install.ps1))) -Update`
  - 本地：`./install.sh --update` / `.\install.ps1 -Update`

## 4. 版本比较

`X.Y.Z` 语义化比较，只有远程**严格大于**本地才报「有新版本」。

- **bash**：自写 `version_gt A B`（true ⇔ B>A），按 `.` 分三段数值比较，**不依赖** `sort -V`（BSD/macOS 可移植性不确定）。非数字段按缺省 0 处理。
- **ps1**：用原生 `[version]` 类型：`[version]$REMOTE -gt [version]$LOCAL`。

边界：任一版本为空 → 跳过比较，走「无法获取/未知」分支。

## 5. 涉及文件

| 文件 | 改动 |
|---|---|
| `install.sh` | 重构为「参数解析 → 版本助手（`get_yaml_version`/`get_remote_version`/`version_gt`）→ 默认/更新分支」。复用现有 build/link/enable 代码块。**结构化为函数 + `main()`，文件底部用 `[ "${BASH_SOURCE[0]}" = "${0}" ] && main "$@"` 守卫**——使助手函数可被 `source` 进测试而不触发安装主流程。 |
| `install.ps1` | 同上镜像（PowerShell：`param([switch]$Update,[switch]$Help)` + `[version]` 比较 + `iwr` 抓远程）。 |
| `README.md` | 更新安装/使用段：说明默认=检查、`--update`=更新、版本检查行为，加上面三种平台的更新命令。 |
| `CHANGELOG.md` | `[未发布]` 段新增「安装脚本：版本检查 + `--update`」。 |

**不改**：`engine/`、`skills/`、`mcp_server/`、`api_server/`、`pyproject.toml`、`agents/install.sh`。不升版本号。

## 6. 验证计划（shell 工具，无 pytest）

本质是 shell/PowerShell 脚本，完整安装行为依赖 Hermes 环境 + 网络，**部分只能装后人工实测**。本环境可做的自动验证：

1. **语法检查**：`bash -n install.sh`（必过）。ps1：若有 `pwsh` 则 `pwsh -NoProfile -Command "[ScriptBlock]::Create((Get-Content -Raw install.ps1)) | Out-Null"` 解析校验；无 `pwsh`（macOS 常见）→ 跳过并记为「需 Windows 实测」。
2. **助手函数单元自测**（`source install.sh` 后直接调用——靠 `main` 守卫使 source 不触发安装）：
   - `version_gt 1.6.0 1.7.0` → true（exit 0）
   - `version_gt 1.7.0 1.7.0` → false
   - `version_gt 1.7.0 1.6.0` → false
   - `version_gt 1.9.0 1.10.0` → true（多位数段）
   - `version_gt 1.7.0 1.7.1` → true
   - `get_yaml_version engine/plugin.yaml` → `1.7.0`（解析+去引号正确）
3. **`--help`**：`bash install.sh --help` 打印用法且退出 0；未知参数退出非 0。
4. **默认检查（本地仓库 + 真实远程）**：`GONGFU_SKILL_DIR=<repo> bash install.sh`（在已 clone 的本仓库上）应：读到本地版本、尝试抓远程、打印版本对比行；**不得** `git pull`、**不得**改动 `git status`。注意此仓库当前 `engine/plugin.yaml` = 1.7.0，远程 main 也应为 1.7.0 → 期望打印「✅ 已是最新 v1.7.0」（或网络失败时的降级提示）。验证「只读」：跑前后 `git status --porcelain` 不变。
   - ⚠ 注意：若测试机已通过 `~/.hermes/plugins/gongfu-skill` 链接安装过，默认模式会判定「已安装」并走只读分支；用 `GONGFU_SKILL_DIR` 指向本仓库可稳定复现版本检查打印。
5. **不可在此验证**：真实 `--update` 的 git pull + Hermes enable、ps1 全流程、`curl|bash -s -- --update` 端到端 → 列入「装后实测」交付项。

## 7. 风险与缓解

- **R1 行为变更**（默认不再自动 pull）→ 旧肌肉记忆用户重跑一键命令不再更新。缓解：默认分支明确打印「运行 … --update 更新」，README 同步；CHANGELOG 写明。
- **R2 远程版本抓取失败**（离线/限流）→ 缓解：best-effort + 超时 + 降级提示，绝不让脚本失败。
- **R3 `curl|bash` 传参**用户不熟 → 缓解：README 给出 `bash -s -- --update` 与 ps1 scriptblock 形式的确切命令。
- **R4 ps1 在本环境无法验证** → 缓解：与 bash 严格镜像逻辑 + 标注装后 Windows 实测。
- **R5 `git pull --ff-only` 在本地脏工作区/非快进失败** → 缓解：捕获失败、温和警告、继续用现有内容，不中断安装。

## 8. 不在范围（YAGNI）

- 不做交互式 y/N 确认（curl|bash 限制）。
- 不做 `--check` 独立子命令（默认即检查）。
- 不做自动后台更新检查 / 定时提醒。
- 不动 `agents/install.sh`、不改引擎/接口、不升版本号。
