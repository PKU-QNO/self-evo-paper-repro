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

## 写完之后

1. 将 human gate ⑤ 通过的 skill 草稿同步到 `.claude/skills/`（用 yaml_to_skill.py）
2. 更新 memento 长期记忆
3. 更新 pitfalls_log 和 decisions_log
4. 报告写到 `.work/.evolution/<timestamp>/evolution_report.md`
5. 复制一份到 `.work/.evolution/reports/` 存档

## 人工 gate ⑥

最终确认。用户看了 evolution-agent 总结报告后决定：
- 哪些 candidate 正式 active
- 哪些记录到长期记忆
- 自迭代流程本身有没有可以改进的地方（流程自迭代—注意：不自迭代自迭代系统自身，只迭代经验层）
