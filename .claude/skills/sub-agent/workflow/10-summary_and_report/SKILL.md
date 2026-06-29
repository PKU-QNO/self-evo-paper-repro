# 10-summary_and_report（子 agent 视角）

## 具体怎么干

### 双报告
**技术报告**（给老师看）：
- 推导+代码+结果+对比+结论
- 物理结论基于数值
- 标注复现 level（0-5）

**经验报告**（给自迭代用）：
- 本次学到的（物理事实、参数范围）
- 踩的坑（公式易错点、单位陷阱）
- skill 改进建议（带适用边界，不写通用规律）

### benchmark 追加
- 按 `optics-mie-reproduction/references/benchmark_format.md` 格式
- 三方一致性状态填实际值
- append-only，不覆盖

### skill 改进草稿（如需）
- 走沙箱：`.work/self-iteration/<skill>.skill.yaml`
- 用 `skill-creator/scripts/skill_to_yaml.py` 导出现有 skill 改
- 草稿不许删
- 不直接改 `.claude/skills/`（主 agent 同步）

### memento 长期记忆
- `memory_store`：本次物理事实、决策、教训
- `decisions_log store`：重要决策（如为什么选纯解析）
- `pitfalls_log store`：常见问题（如单位陷阱）
- 存前 `memory_dedup_check` 查重

### 预制脚本（scripts/）
- `build_technical_report.py` — 技术报告骨架生成
- `build_experience_report.py` — 经验报告骨架生成

## 输出约定

- 技术报告：`.work/<case>/technical_report.md`
- 经验报告：`.work/<case>/experience_report.md`
- benchmark 草稿：`.work/self-iteration/benchmark_<case>.yaml`
- skill 草稿：`.work/self-iteration/<skill>.skill.yaml`（如需）

## 常见坑

- 经验别写成通用规律，带 applies_when / does_not_apply_when
- 记忆写入前查重，别重复
- skill 改进走沙箱，别直接改 .claude

## 决策问题重点回答

- 物理复现 level 哪级？
- 哪些 skill 值得自迭代？
- 给下一篇留什么接力？
- 哪些进 .result？
