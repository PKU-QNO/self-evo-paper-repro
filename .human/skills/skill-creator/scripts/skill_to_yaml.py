"""skill_to_yaml.py — 文件夹形式 skill → .skill.yaml

把一个 skill 文件夹（含 SKILL.md + references/ + scripts/ + assets/ 等）
打包成单个 .skill.yaml 文件，格式参考 Magnus skill yaml 并精简。

用法:
  python skill_to_yaml.py <skill_folder> [-o output.yaml]

不指定 -o 则输出到当前目录，文件名为 <skill_name>.skill.yaml。

yaml 格式:
  kind: optics/skill
  version: "1.0"
  exported_at: <ISO 时间>
  payload:
    id: <skill 名>
    title: <人类可读名>
    description: <从 SKILL.md frontmatter 提取>
    files:
      - path: SKILL.md
        content: |
          <完整文件内容>
      - path: references/xxx.md
        content: |
          ...
"""
from __future__ import annotations
import argparse
import datetime
import os
import sys
import re
from pathlib import Path


def read_frontmatter(skill_md: Path) -> dict:
    """从 SKILL.md 的 YAML frontmatter 提取 name 和 description。"""
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {"name": skill_md.parent.name, "description": ""}
    fm = m.group(1)
    name = ""
    desc = ""
    for line in fm.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            desc = line.split(":", 1)[1].strip()
    return {"name": name or skill_md.parent.name, "description": desc}


def collect_files(skill_folder: Path) -> list[dict]:
    """收集 skill 文件夹下所有文件，返回 [{path, content}]。"""
    files = []
    for root, _, names in os.walk(skill_folder):
        for n in names:
            fp = Path(root) / n
            rel = fp.relative_to(skill_folder).as_posix()
            # 跳过 __pycache__、.pyc
            if "__pycache__" in rel or rel.endswith(".pyc"):
                continue
            content = fp.read_text(encoding="utf-8", errors="replace")
            files.append({"path": rel, "content": content})
    return files


def yaml_escape(text: str) -> str:
    """用 YAML 字面量块标量 | 方式转义，保证多行内容安全。"""
    # 检测内容里是否有特殊结尾，用 |+ 保留所有换行
    if not text.endswith("\n"):
        text = text + "\n"
    return text


def build_yaml(skill_folder: Path) -> str:
    skill_md = skill_folder / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_folder}")
    fm = read_frontmatter(skill_md)
    files = collect_files(skill_folder)
    now = datetime.datetime.now().isoformat(timespec="seconds")

    lines = []
    lines.append('kind: optics/skill')
    lines.append(f'version: "1.0"')
    lines.append(f'exported_at: "{now}"')
    lines.append('payload:')
    lines.append(f'  id: "{fm["name"]}"')
    # title 用 name 转 title case 简化
    lines.append(f'  title: "{fm["name"].replace("-", " ").title()}"')
    # description 可能含特殊字符，用双引号包，转义内部双引号
    desc = fm["description"].replace('"', '\\"')
    lines.append(f'  description: "{desc}"')
    lines.append(f'  files:')
    for f in files:
        lines.append(f'    - path: "{f["path"]}"')
        lines.append('      content: |')
        for cl in f["content"].splitlines(keepends=True):
            lines.append(f"        {cl}" if cl != "\n" else "        ")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="文件夹 skill → .skill.yaml")
    ap.add_argument("skill_folder", help="skill 文件夹路径（含 SKILL.md）")
    ap.add_argument("-o", "--output", help="输出 yaml 路径，不指定则输出到当前目录")
    args = ap.parse_args()

    skill_folder = Path(args.skill_folder).resolve()
    if not skill_folder.is_dir():
        print(f"ERROR: {skill_folder} 不是目录", file=sys.stderr)
        return 1

    yaml_text = build_yaml(skill_folder)
    if args.output:
        out = Path(args.output)
    else:
        out = Path.cwd() / f"{skill_folder.name}.skill.yaml"
    out.write_text(yaml_text, encoding="utf-8")
    print(f"OK: {skill_folder.name} -> {out} ({len(yaml_text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
