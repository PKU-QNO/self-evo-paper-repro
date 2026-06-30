# 10-summary_and_report（主 agent 视角）

## 这步干什么

子 agent 做经验沉淀 + 记忆更新 + 双报告（技术报告 + 经验报告）。这是子 agent 的最后一步，主 agent 的总结是第 11 步。

## 输出要求（子 agent 产出初稿，主 agent step11 汇总定稿）

子 agent 产 4 类文档初稿，放沙箱；主 agent 定稿后投递到最终目录：

### 1. 全过程报告（最详细，给人审查留痕）
- 沙箱草稿：`.work/<case>/full_report_draft.md`
- 最终路径：`.result/<paper>/full_report.md`
- 内容：完整记录每步做了什么、用了什么参数、遇到什么问题、结果数值，并显式标注 `result_class`（CLAUDE.md 7 级枚举）

### 2. 简报（给老师/PI 的一页摘要）
- 沙箱草稿：`.work/<case>/brief_draft.md`
- 最终路径：`.result/<paper>/brief.md` + 填 `todo.md` 一段
- 内容：论文名/目标/`result_class`/关键数字/一句话结论

### 3. SKILL 更改建议
- 沙箱草稿：`.work/self-iteration/<paper>.skill-suggestion-draft.md`
- 最终路径：`toEflow/<paper>.skill-suggestion.md`
- 内容：本次复现暴露的 skill 缺陷/改进点，带 tier 标注、适用边界、来源 case。只增不删。

### 4. 蓝图建议（如需）
- 沙箱草稿：`.work/self-iteration/<paper>.blueprint-suggestion-draft.md`
- 最终路径：`toEflow/<paper>.blueprint-suggestion.md`
- 内容：如果要上 COMSOL/Magnus，蓝图怎么写/改；如果纯 Python 不上 Magnus，明确写"本次无需蓝图"

### 其他
- benchmark.yaml 条目追加
- memento 长期记忆更新
- skill 改进走沙箱（`.work/self-iteration/<skill>.skill.yaml`，如需）
- 输出约定参考 `references/main_report_template.md`

## 要传达给子 agent 的约定

- 双报告分开：技术报告给老师看，经验报告给自迭代用
- 经验要带适用边界，不写成通用规律
- skill 改进走沙箱草稿，不直接改 .claude
- 记忆写入前查重
- 所有报告、brief、memento 记忆必须标注 `result_class`；不得用旧的 level 0-5 替代 7 级枚举

## 本步子 agent 必须回答的决策问题

1. 物理复现成功了吗？`result_class` 是 7 级枚举中的哪一级？
2. 暴露了哪些 skill 缺陷？值得自迭代吗？
3. 给下一篇复现留什么接力信息？
4. 哪些内容该进 .result？哪些留沙箱？

## 人工 gate

触发关键节点"即将进 .result"+"即将自迭代"问用户。

## 下一步

→ 11-main_agent_report（主 agent 自己写）

## 本步 sub-agent spawn 局部模版

```
【第 10 步：summary_and_report】
【任务】经验沉淀 + 记忆更新 + 双报告（技术报告 + 经验报告）。这是子 agent 的最后一步。
【输入】.work/{case}/各步产出文件
【输出】.work/{case}/full_report_draft.md / brief_draft.md / .work/self-iteration/{paper}.skill-suggestion-draft.md / .work/self-iteration/{paper}.blueprint-suggestion-draft.md / benchmark.yaml 条目追加 / memento 记忆更新
【要传达的约定】双报告分开（技术报告给老师，经验报告给自迭代）；经验要带适用边界，不写成通用规律；skill 改进走沙箱草稿，不直接改 .claude；记忆写入前查重；所有报告、brief、memento 记忆必须标注 result_class，不得用旧的 level 0-5 替代 7 级枚举。
【必须回答的决策问题】1.物理复现成功了吗？result_class 是 7 级枚举中的哪一级？2.暴露了哪些 skill 缺陷？值得自迭代吗？3.给下一篇复现留什么接力信息？4.哪些内容该进 .result？哪些留沙箱？
【人工 gate】触发关键节点"即将进 .result"+"即将自迭代"问用户。
【retry_budget】本步最多重跑 5 轮，每轮必须有新证据/新假设。
【blocker_condition】技术报告、经验报告或 benchmark 条目缺关键证据；result_class 无法归类；用户未确认 `.result/` 内容或自迭代候选去向。
【预制脚本】无（参考 references/main_report_template.md）
```
