"""yaml_to_skill.py — .skill.yaml → 文件夹形式 skill

把 skill_to_yaml.py 产生的 .skill.yaml 还原成 skill 文件夹。
用于从沙箱草稿 .skill.yaml 同步回 .claude/skills/。

用法:
  python yaml_to_skill.py <input.skill.yaml> [-o output_folder]

不指定 -o 则输出到当前目录下与 skill id 同名的文件夹。

注意:
  - 会覆盖输出目录下同名文件
  - 还原后 SKILL.md 的 frontmatter 完整保留
  - 脚本/二进制文件用 errors=replace 读取，适合文本类 skill
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path


def parse_yaml_blocks(text: str) -> dict:
    """简易解析：提取 kind/version/exported_at/payload.id/title/description/files。

    不依赖 PyYAML，用结构匹配避免安装依赖。
    """
    result = {}

    # 顶层标量
    m = re.search(r'^kind:\s*(.+)$', text, re.MULTILINE)
    result["kind"] = m.group(1).strip().strip('"') if m else ""
    m = re.search(r'^version:\s*(.+)$', text, re.MULTILINE)
    result["version"] = m.group(1).strip().strip('"') if m else ""
    m = re.search(r'^exported_at:\s*(.+)$', text, re.MULTILINE)
    result["exported_at"] = m.group(1).strip().strip('"') if m else ""

    # payload.id / title / description
    m = re.search(r'^\s+id:\s*"?(.+?)"?\s*$', text, re.MULTILINE)
    result["id"] = m.group(1).strip() if m else ""
    m = re.search(r'^\s+title:\s*"?(.+?)"?\s*$', text, re.MULTILINE)
    result["title"] = m.group(1).strip() if m else ""
    m = re.search(r'^\s+description:\s*"(.*?)"\s*$', text, re.MULTILINE | re.DOTALL)
    result["description"] = m.group(1) if m else ""

    # files: 提取每个 - path: + content: | 块
    files = []
    # 找 files: 行位置
    fm = re.search(r'^\s+files:\s*$', text, re.MULTILINE)
    if fm:
        body = text[fm.end():]
        # 每个 path 块
        pat = re.compile(
            r'^\s+-\s+path:\s*"(.+?)"\s*\n\s+content:\s*\|\n((?:        .*\n|\n)*)',
            re.MULTILINE,
        )
        for pm in pat.finditer(body):
            path = pm.group(1)
            raw = pm.group(2)
            # 去掉 8 空格缩进
            content_lines = []
            for cl in raw.splitlines(keepends=True):
                if cl.startswith("        "):
                    content_lines.append(cl[8:])
                elif cl.strip() == "":
                    content_lines.append("\n")
                else:
                    content_lines.append(cl)
            content = "".join(content_lines)
            files.append({"path": path, "content": content})
    result["files"] = files
    return result


def restore_files(parsed: dict, out_folder: Path) -> int:
    out_folder.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in parsed["files"]:
        fp = out_folder / f["path"]
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(f["content"], encoding="utf-8")
        count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description=".skill.yaml → 文件夹 skill")
    ap.add_argument("input_yaml", help="输入 .skill.yaml 路径")
    ap.add_argument("-o", "--output", help="输出文件夹路径，不指定则用 skill id 在当前目录建")
    args = ap.parse_args()

    inp = Path(args.input_yaml).resolve()
    if not inp.is_file():
        print(f"ERROR: {inp} 不是文件", file=sys.stderr)
        return 1

    text = inp.read_text(encoding="utf-8")
    parsed = parse_yaml_blocks(text)
    if not parsed["files"]:
        print("ERROR: 未解析出任何文件，检查 yaml 格式", file=sys.stderr)
        return 1

    if args.output:
        out = Path(args.output)
    else:
        out = Path.cwd() / (parsed["id"] or inp.stem.replace(".skill", ""))

    n = restore_files(parsed, out)
    print(f"OK: {inp.name} -> {out} ({n} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
