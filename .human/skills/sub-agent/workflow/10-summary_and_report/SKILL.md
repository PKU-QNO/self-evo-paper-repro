# 10-summary_and_report（子 agent 视角）

## 具体怎么干

### 4 类文档产出（初稿，主 agent step11 定稿）

子 agent 产 4 类文档初稿放沙箱，主 agent 汇总定稿后投到最终目录。

**① 全过程报告**（最详细，给人审查留痕）
- 草稿：`.work/.todo/{paper}/{case}/full_report_draft.md`
- 完整记录每步操作、参数、问题、数值

**② 简报**（给老师/PI 一页摘要）
- 草稿：`.work/.todo/{paper}/{case}/brief_draft.md`
- 论文名/目标/复现 level/关键数字/一句话结论

**③ SKILL 更改建议**
- 草稿：`.work/.todo/{paper}/{case}/self-iteration/<paper>.skill-suggestion-draft.md`
- 技能缺陷/改进点，带 tier、适用边界、来源 case
- 只增不删

**④ 蓝图建议**
- 草稿：`.work/.todo/{paper}/{case}/self-iteration/<paper>.blueprint-suggestion-draft.md`
- 上 Magnus 的蓝图设计方案，纯 Python 则注明"本次无需蓝图"

### benchmark 追加
- 按 `optics-mie-reproduction/references/benchmark_format.md` 格式
- 三方一致性状态填实际值
- append-only，不覆盖

### skill 改进草稿（如需）
- 走沙箱：`.work/.todo/{paper}/{case}/self-iteration/<skill>.skill.yaml`
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

- 全过程报告草稿：`.work/.todo/{paper}/{case}/full_report_draft.md`
- 简报草稿：`.work/.todo/{paper}/{case}/brief_draft.md`
- SKILL 更改建议草稿：`.work/.todo/{paper}/{case}/self-iteration/<paper>.skill-suggestion-draft.md`
- 蓝图建议草稿：`.work/.todo/{paper}/{case}/self-iteration/<paper>.blueprint-suggestion-draft.md`
- benchmark 草稿：`.work/.todo/{paper}/{case}/self-iteration/benchmark_<case>.yaml`
- skill 改进草稿：`.work/.todo/{paper}/{case}/self-iteration/<skill>.skill.yaml`（如需）
- 模板参考：`main-agent/references/main_report_template.md`

## 常见坑

- 经验别写成通用规律，带 applies_when / does_not_apply_when
- 记忆写入前查重，别重复
- skill 改进走沙箱，别直接改 .claude

## 决策问题重点回答

- 物理复现 level 哪级？
- 哪些 skill 值得自迭代？
- 给下一篇留什么接力？
- 哪些进 .result？
