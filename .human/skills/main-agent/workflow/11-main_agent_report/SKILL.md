# 11-main_agent_report（主 agent 自己写）

## 这步干什么

主 agent 写全局总结报告。子 agent 的 step 10 是经验+记忆+双报告，本步是主 agent 站在编排者视角的总览。

## 这是主 agent 你自己做的，不是 spawn 子 agent

读 `references/main_report_template.md`，填 8 个字段：
1. 本次复现概况
2. 10 步执行轨迹（引用各步子 agent 报告路径）
3. 关键决策点回顾（你在哪些节点拍了板）
4. 人工 gate 记录
5. 最终成果（进 .result 的、benchmark、skill 更新）
6. 自迭代建议
7. 给下一篇的接力
8. 长期记忆更新摘要

## 写完之后

1. 从 `.work` 复制有用内容到 `.result/`（问用户哪些确认）
2. 通过 gate 的 skill 草稿同步到 `.claude`（用 yaml_to_skill.py）
3. 更新 memento 长期记忆（全局结论）
4. 报告写到 `.work/.sub-report/main-<case>-<timestamp>.md`，也复制一份到 `.result/reports/`

## 人工 gate

最终确认。用户看了主 agent 报告后决定哪些进 .result、哪些 skill 草稿通过。

## workflow 结束
