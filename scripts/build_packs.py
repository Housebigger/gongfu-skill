#!/usr/bin/env python3
"""从单一源重新生成各派生知识包。

单一源（source of truth，唯一可手改的地方）:
  - skills/<name>/SKILL.md   每个 skill 的定义
  - skills/data/*.yaml       结构化知识库

派生目标（generated，已 gitignore，请勿手动编辑——改了会被覆盖）:
  - skills/gongfu-skill/skills/<name>/SKILL.md   Hermes 插件内嵌的 skill 副本
                                                 （不带 data/，引擎运行时读 skills/data/）
  - claude-skills/skills/<name>/SKILL.md         Claude Code 静态知识包
  - claude-skills/data/*.yaml
  - agents/zcode-skills/<name>/SKILL.md          ZCode 知识包
  - agents/zcode-skills/data/*.yaml

安装脚本（install.sh / install.ps1 / agents/install.sh）会自动调用本脚本。
也可手动运行：python scripts/build_packs.py

只用标准库，无第三方依赖，跨平台。
"""

import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC_SKILLS = REPO / "skills"
SRC_DATA = SRC_SKILLS / "data"

# (skills 目标目录, data 目标目录或 None)
TARGETS = [
    (REPO / "skills" / "gongfu-skill" / "skills", None),
    (REPO / "claude-skills" / "skills", REPO / "claude-skills" / "data"),
    (REPO / "agents" / "zcode-skills", REPO / "agents" / "zcode-skills" / "data"),
]


def source_skill_dirs():
    """skills/ 下含 SKILL.md 的目录，排除 data/ 和引擎目录 gongfu-skill/。"""
    return [
        c for c in sorted(SRC_SKILLS.iterdir())
        if c.is_dir() and c.name != "gongfu-skill" and (c / "SKILL.md").exists()
    ]


def main():
    skill_dirs = source_skill_dirs()
    if not skill_dirs:
        print("[build_packs] 未找到源 skill（skills/<name>/SKILL.md），中止", file=sys.stderr)
        return 1
    data_files = sorted(SRC_DATA.glob("*.yaml"))

    for skills_dest, data_dest in TARGETS:
        # 全量重建：先清掉旧目标，避免源里已删除的 skill 残留在副本中。
        # 对 zcode：skills_dest 是 data_dest 的父目录，整体清除即可。
        if skills_dest.exists():
            shutil.rmtree(skills_dest)
        for d in skill_dirs:
            dest = skills_dest / d.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(d / "SKILL.md", dest / "SKILL.md")

        n_data = 0
        if data_dest is not None:
            if data_dest.exists():
                shutil.rmtree(data_dest)
            data_dest.mkdir(parents=True, exist_ok=True)
            for f in data_files:
                shutil.copy2(f, data_dest / f.name)
            n_data = len(data_files)

        rel = skills_dest.relative_to(REPO)
        suffix = f" + {n_data} data" if data_dest is not None else ""
        print(f"[build_packs] {rel}: {len(skill_dirs)} skills{suffix}")

    print("[build_packs] done. 源在 skills/（SKILL.md + data/），派生包勿手改。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
