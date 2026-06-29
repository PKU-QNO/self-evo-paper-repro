"""skill-print.py — 扫描 .claude/skills/ 打印所有 skill 的 name + description。

sub-agent 启动时强制运行此脚本，获得当前工作区可用 skill 列表和描述。
因为子 agent 不自动注入 SKILL 描述，主 agent spawn 时让它先跑这个脚本。

用法:
  python .claude/skill-print.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def extract_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {"name": "", "description": ""}
    fm = m.group(1)
    name = ""
    desc = ""
    in_desc = False
    desc_lines = []
    for line in fm.splitlines():
        if in_desc:
            # 多行 description 续行（缩进或无 key）
            if re.match(r"^\s", line) or ":" not in line:
                desc_lines.append(line.strip())
            else:
                in_desc = False
        if not in_desc and line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif not in_desc and line.startswith("description:"):
            desc = line.split(":", 1)[1].strip()
            if not desc:
                in_desc = True
    if desc_lines:
        desc = " ".join([desc] + desc_lines).strip()
    return {"name": name, "description": desc}


def main() -> int:
    skills_dir = Path(__file__).resolve().parent / "skills"
    if not skills_dir.exists():
        print("ERROR: .claude/skills/ 不存在", file=sys.stderr)
        return 1

    skills = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = extract_frontmatter(text)
        name = fm["name"] or skill_md.parent.name
        desc = fm["description"]
        folder = skill_md.parent.name
        skills.append({"name": name, "desc": desc, "folder": folder})

    print(f"# 可用 skill 列表（{len(skills)} 个）")
    print(f"# 工作区: {Path(__file__).resolve().parent.parent}")
    print()
    for s in skills:
        print(f"## {s['name']}")
        print(f"   目录: .claude/skills/{s['folder']}/")
        print(f"   描述: {s['desc']}")
        print()
    print(f"# 共 {len(skills)} 个 skill")
    print("# 如需加载某 skill 完整内容: Read .claude/skills/<folder>/SKILL.md")
    print("# 如需加载某 skill 的 references/scripts: 查看 .claude/skills/<folder>/ 下结构")
    return 0


if __name__ == "__main__":
    sys.exit(main())
