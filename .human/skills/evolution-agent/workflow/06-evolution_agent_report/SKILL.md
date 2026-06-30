# 06-evolution_agent_report（evolution-agent 自己写）

## 这步干什么

evolution-agent 写全局总结报告。sub-E-agent 的各步是分步报告，本步是 evolution-agent 站在编排者视角的总览。

## 这是你（evolution-agent）自己做的，不是 spawn sub-E-agent

报告模板见 `references/evolution_history_template.md`，写到 `.E-history/NN-evolution-report.md`。

读 `references/main_report_template.md`，填 8 个字段：
1. 本次自迭代概况
2. 6 步执行轨迹（引用各步 sub-E-agent 报告路径）
3. 经验聚类概况（4 type 统计）
4. 关键决策点回顾（你在哪些节点拍了板）
5. 人工 gate 记录（每步用户确认结果）
6. skill 变更清单（改了哪些，最终状态）
7. 验证结果摘要（replay + verifier）
8. 长期记忆更新摘要

## 写 run manifest

自迭代 workflow 结束前，evolution-agent 必须在 `.work/run_manifest.yaml` 写审计索引：
- `run_id`、`timestamp`、`batch`
- `spawned_agents`：数量、各 agent 角色、负责节点、depth
- `fan_out`：哪个节点并发了几个 sub-E-agent
- `max_depth_reached`
- `result_class`：使用 CLAUDE.md 的 7 级枚举之一
- `retry_fingerprints`：每步重跑 fingerprint、修改点、新证据/新假设、结果

`run_manifest.yaml` 只做索引，证据仍引用各步 sub-E-agent 报告、validation 和治理报告。

## 写完之后

1. 将 human gate ⑤ 通过的 skill 草稿同步到 `.claude/skills/`（用 yaml_to_skill.py）
2. 更新 memento 长期记忆
3. 更新 pitfalls_log 和 decisions_log
4. 报告写到 `.work/.evolution/<timestamp>/evolution_report.md`
5. 复制一份到 `.work/.evolution/reports/` 存档
6. 写 `.work/run_manifest.yaml`，记录 fan-out/depth/result_class/retry_fingerprints；`result_class` 使用 CLAUDE.md 的 7 级枚举之一

## 人工 gate ⑥

最终确认。用户看了 evolution-agent 总结报告后决定：
- 哪些 candidate 正式 active
- 哪些记录到长期记忆
- 自迭代流程本身有没有可以改进的地方（流程自迭代—注意：不自迭代自迭代系统自身，只迭代经验层）

## 局部 spawn 模版（供 evolution-agent 拼接用）

```
【第 06 步：evolution_agent_report】
【任务】evolution-agent 写全局总结报告。sub-E-agent 的各步是分步报告，本步是 evolution-agent 站在编排者视角的总览。
【输入】各步 sub-E-agent 报告路径；所有 01-05 步产出
【输出】evolution_report.md 写到 `.work/.evolution/<timestamp>/evolution_report.md`（8 字段：概况/6 步轨迹/4 type 统计/关键决策点/gate 记录/skill 变更清单/验证摘要/长期记忆摘要）；复制一份到 `.work/.evolution/reports/` 存档；写 `.work/run_manifest.yaml` 记录 run_id/timestamp/batch/spawned_agents/fan_out/max_depth_reached/result_class/retry_fingerprints
【要传达的约定】本步由 evolution-agent **自己执行，不 spawn sub-E-agent**；写完之后：human gate ⑤ 通过的 skill 草稿同步到 `.claude/skills/`（用 yaml_to_skill.py）；更新 memento 长期记忆；更新 pitfalls_log 和 decisions_log
【必须回答的决策问题】无——本条不是 sub-E-agent 步骤，而是 evolution-agent 总结。但需要 self-reflection：本次自迭代 overall 是否有价值？流程本身有没有可改进之处？
【人工 gate】⑥ 最终确认。用户看总结报告后决定：哪些 candidate 正式 active、哪些记录到长期记忆、自迭代流程本身有没有可以改进的地方（流程自迭代—不自迭代系统自身，只迭代经验层）
【并发说明】不并发，evolution-agent 自己执行
【预制脚本】无（尚未建立）
```
