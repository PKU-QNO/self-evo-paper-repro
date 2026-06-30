# 03-concurrent_skill_work（evolution-agent 视角）

## 这步干什么

并行 spawn M 个 sub-E-agent，每个负责改一个 skill 的草稿。**每个 sub-E-agent 只碰一个 skill**，不改 workflow 拓扑、蓝图结构、AGENTS.md。

## 输入

- 上一步的修改计划（`plan.md`）
- 当前 skill 的最新版本（`.claude/skills/<skill-name>/`）
- 相关 capsule 的原始工作报告和审查报告
- `.work/.todo/<paper-name>/` 下的单论文草稿（如果有）

## 输出要求

- M 份 skill 草稿（`.work/.evolution/<timestamp>/drafts/<skill-name>.skill.yaml`）：
  - 改了什么 / 为什么改 / 验证结果 / 来源 case
  - 每条候选经验/改动必须带 5 字段：`candidate_id`（唯一 ID）、`evidence_ref`（引用 capsule/verifier 结果/数值）、`decision`（Save/Improve/Absorb/Fork/Archive/Drop）、`tier`（Tier-1/2/3）、`rollback_ref`（接受后出问题回滚到哪个版本）
  - 用 skill_to_yaml.py 导出当前 skill 为 yaml 再改
  - 改完保存 yaml（不改 `.claude/skills/` 原文）
- 如果不需要改某个 skill，在计划里注明"skipped"
- 如果本步涉及 Magnus blueprint 参数扫描能力，必须补充 `sweep_manifest.yaml` 规范：记录 `sweep_id`、`blueprint_id`、扫描参数/范围/步长/总点数、每个点的结果路径和 `result_class`，并支持复跑单点和复现整图。

## 要传达给 sub-E-agent 的约定

- **只碰 skill 内容 + 提示词备注**，不碰：
  - × workflow 拓扑
  - × 蓝图结构（`.magnus/`）
  - × AGENTS.md / CLAUDE.md
  - × 自迭代系统自身
  - × 其他 skill 的文件
- 先读当前 skill 文件，理解它的结构和边界
- 用 `skill-creator/scripts/skill_to_yaml.py` 导出 yaml 草稿
- 改的时候保留原 skill 的所有字段，只增补或修改相关内容
- 每条改动边上标注来源（哪篇 capsule 的哪个发现）
- **不能因为"我觉得更好"就改——必须有 capsule 数据支撑**
- 涉及参数扫描的 skill/蓝图经验必须要求写 `sweep_manifest.yaml`，否则不能标 Absorb/active
- 改完不要恢复成 `.claude/skills/` 格式——保持 yaml 草稿形态

## 本步 sub-E-agent 必须回答的决策问题

1. 你改了什么？为什么改？哪篇 capsule 支撑的？
2. 有没有改超出 skill 范围（碰了拓扑/蓝图/AGENTS）？
3. 改动会不会导致旧 case 退化？
4. 草稿完整性——有没有遗漏原 skill 的关键部分？
5. 你觉得还需不需要额外的 case 验证？哪些？

## 人工 gate ③

**每份 skill 草稿给用户看。** 确认：
- 改动范围是否合理（有没有碰不该碰的）
- 改动了是不是 capsule 数据支撑的
- 草稿质量（有没有遗漏、有没有过度修改）

## 局部 spawn 模版（供 evolution-agent 拼接用）

```
【第 03 步：concurrent_skill_work】
【任务】并行 spawn M 个 sub-E-agent，每个负责改一个 skill 的草稿。每个 sub-E-agent 只碰一个 skill，不改 workflow 拓扑、蓝图结构、AGENTS.md。
【输入】上一步的修改计划（`plan.md`）；当前 skill 最新版本（`.claude/skills/<skill-name>/`）；相关 capsule 的原始工作报告和审查报告；`.work/.todo/<paper-name>/` 下的单论文草稿（如果有）
【输出】M 份 skill 草稿（`.work/.evolution/<timestamp>/drafts/<skill-name>.skill.yaml`），每份标明改了什么/为什么改/验证结果/来源 case；每条候选经验/改动必须带 candidate_id/evidence_ref/decision/tier/rollback_ref 五字段；不需要改的注明"skipped"；涉及 Magnus blueprint 参数扫描时补充 `sweep_manifest.yaml` 规范
【要传达的约定】只碰 skill 内容+提示词备注，不碰 workflow 拓扑、蓝图结构、AGENTS.md/CLAUDE.md、自迭代系统自身、其他 skill 的文件；先读当前 skill 文件理解结构和边界；用 `skill-creator/scripts/skill_to_yaml.py` 导出 yaml 草稿；改的时候保留原 skill 的所有字段只增补或修改相关内容；每条改动边上标注来源（哪篇 capsule 的哪个发现）；不能因为"我觉得更好"就改——必须有 capsule 数据支撑；涉及参数扫描的 skill/蓝图经验必须要求写 `sweep_manifest.yaml`，记录 `sweep_id`/`blueprint_id`/扫描参数范围步长总点数/每点结果路径+result_class，并支持复跑单点和复现整图；改完保持 yaml 草稿形态，不恢复成 `.claude/skills/` 格式
【必须回答的决策问题】1. 你改了什么？为什么改？哪篇 capsule 支撑的？2. 有没有改超出 skill 范围（碰了拓扑/蓝图/AGENTS）？3. 改动会不会导致旧 case 退化？4. 草稿完整性——有没有遗漏原 skill 的关键部分？5. 你觉得还需不需要额外的 case 验证？哪些？
【人工 gate】③ 每份 skill 草稿给用户看。确认改动范围是否合理、是否 capsule 数据支撑、草稿质量（有没有遗漏/过度修改）。
【并发说明】M 个 sub-E-agent 并行，每人改一个 skill（M = plan.md 中待改 skill 数量）。每个 sub-E-agent 只碰一个 skill，互不干扰。
【预制脚本】无（尚未建立）
```
