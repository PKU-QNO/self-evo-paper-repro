# 10-summary_and_report（主 agent 视角）

## 这步干什么

子 agent 做经验沉淀 + 记忆更新 + 双报告（技术报告 + 经验报告）。这是子 agent 的最后一步，主 agent 的总结是第 11 步。

## 输出要求（子 agent 产出）

- 技术报告（`.work/<case>/technical_report.md`）：推导+代码+结果+对比+结论
- 经验报告（`.work/<case>/experience_report.md`）：本次学到的、踩的坑、skill 改进建议
- benchmark.yaml 条目追加
- memento 长期记忆更新
- skill 改进草稿（`.work/self-iteration/<skill>.skill.yaml`，如需）

## 要传达给子 agent 的约定

- 双报告分开：技术报告给老师看，经验报告给自迭代用
- 经验要带适用边界，不写成通用规律
- skill 改进走沙箱草稿，不直接改 .claude
- 记忆写入前查重

## 本步子 agent 必须回答的决策问题

1. 物理复现成功了吗？level 0-5 哪级？
2. 暴露了哪些 skill 缺陷？值得自迭代吗？
3. 给下一篇复现留什么接力信息？
4. 哪些内容该进 .result？哪些留沙箱？

## 人工 gate

触发关键节点"即将进 .result"+"即将自迭代"问用户。

## 下一步

→ 11-main_agent_report（主 agent 自己写）
