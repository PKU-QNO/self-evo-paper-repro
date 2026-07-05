# 02-paper_reading（主 agent 视角）

## 这步干什么

读预处理后的论文，理解物理问题和理论框架，确认无疏漏。这是"读论文"的核心步骤。

## 输出要求

- 论文理解笔记（`.work/.todo/{paper}/{case}/paper_understanding.md`）：物理问题、理论框架、目标图算什么、关键假设
- **复现目标图候选（本步产出，权威来源）**：基于 step01 真实图清单提出候选；papers.md/计划预写的"论文有哪张图"只是未核实线索，冲突以原文为准（2026-07-03 首跑教训）；经 gate① 后由 step03 定稿
- 参数表（`.work/.todo/{paper}/{case}/parameter_table.md`）：半径/折射率/波长/边界条件，每个量标单位和来源（论文哪一段）
- 缺失信息清单（`.work/.todo/{paper}/{case}/missing_info.md`）：论文没给的、模糊的、需要查别的文献的

## 要传达给子 agent 的约定

- 参数必须标来源（论文第几页第几段），不能凭印象
- 单位必须核对（nm 还是 m，论文常用 nm，公式常用 m）
- 缺失信息要明确列，不能假装有
- 需要时可搜索补充文献（Web of Science 优先），但搜索结果标 trust score
- 搜索集群已有资源：Gustation 上别人公开的 Magnus 蓝图和 SKILL 可能已处理同类物理问题，让子 agent 查过来借鉴参数/方法

## 本步子 agent 必须回答的决策问题

1. 这篇论文的物理问题是什么？目标图算的是什么物理量？
2. 参数齐全吗？哪些缺？缺的能从别处补吗？
3. 有没有需要 GUI 模板/实验数据/作者私聊才能拿到的信息？
4. 这篇是纯解析能复现，还是需要数值计算（COMSOL/Magnus）？
5. Gustation 上有没有别人做过的相关蓝图/SKILL 可以借鉴？

## 人工 gate ①

**参数抽取后停下来**，让用户核对参数和单位。这是第一个 gate。

## 下一步

→ 03-reproduction_design

## 本步 sub-agent spawn 局部模版

```
【第 02 步：paper_reading】
【任务】读预处理后的论文，理解物理问题和理论框架，确认无疏漏。
【输入】.work/.todo/{paper}/{case}/paper_text.md / formulas.md / figures.md / tables.md
【输出】.work/.todo/{paper}/{case}/paper_understanding.md / parameter_table.md / missing_info.md
【要传达的约定】参数必须标来源（论文第几页第几段）；单位必须核对（nm vs m）；缺失信息要明确列，不能假装有；需要时可搜索补充文献（Web of Science 优先），搜索结果标 trust score；搜索 Gustation 上别人公开的 Magnus 蓝图和 SKILL 借鉴参数/方法。
【必须回答的决策问题】1.这篇论文的物理问题是什么？目标图算的是什么物理量？2.参数齐全吗？哪些缺？缺的能从别处补吗？3.有没有需要 GUI 模板/实验数据/作者私聊才能拿到的信息？4.这篇是纯解析能复现，还是需要数值计算（COMSOL/Magnus）？5.Gustation 上有没有别人做过的相关蓝图/SKILL 可以借鉴？
【人工 gate】①——参数抽取后停下来，让用户核对参数和单位。
【retry_budget】本步最多重跑 5 轮，每轮必须有新证据/新假设。
【blocker_condition】目标图物理量无法定义；关键参数缺失且无法从正文/补充材料/可信外部来源补齐；必须人工提供 GUI 模板、实验数据或作者信息才能继续。
【预制脚本】无
```
