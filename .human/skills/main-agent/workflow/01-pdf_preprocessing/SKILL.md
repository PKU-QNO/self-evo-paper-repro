# 01-pdf_preprocessing（主 agent 视角）

## 这步干什么

把论文 PDF 转成 agent 能用的结构化文本：正文 Markdown、公式、图、表分离。是后续所有步骤的输入。

## 输出要求

- 正文 Markdown（`.work/<case>/paper_text.md`）
- 公式清单（`.work/<case>/formulas.md`，编号+原文+LaTeX）
- 图清单（`.work/<case>/figures.md`，编号+caption+是数据图还是示意图）
- 表清单（`.work/<case>/tables.md`，编号+caption+数值）
- 图片单独导出到 `.work/<case>/figs/`

## 要传达给子 agent 的约定

- 数据图（有坐标轴/数值）和示意图（结构/流程）要分开标记，数据图后面要数字化
- 公式必须保留原文上下文，不能只抄公式本身
- 表格数值必须逐字保留，不能四舍五入
- 图的 caption 要完整提取

## 本步子 agent 必须回答的决策问题

1. PDF 是扫描版还是电子版？需不需要 OCR？
2. 公式能不能干净提取，还是需要图片化处理？
3. 有没有数据图需要数字化（为后面 step 08 量化对比准备）？

## 人工 gate

无（这步是机械处理，不涉及物理判断）

## 下一步

→ 02-paper_reading

## 本步 sub-agent spawn 局部模版

```
【第 01 步：pdf_preprocessing】
【任务】把论文 PDF 转成 agent 能用的结构化文本：正文 Markdown、公式、图、表分离。
【输入】.paper/{paper}.pdf
【输出】.work/{case}/paper_text.md / formulas.md / figures.md / tables.md / figs/
【要传达的约定】数据图和示意图分开标记，数据图后面要数字化；公式必须保留原文上下文；表格数值逐字保留不四舍五入；图的 caption 完整提取。
【必须回答的决策问题】1.PDF 是扫描版还是电子版？需不需要 OCR？2.公式能不能干净提取，还是需要图片化处理？3.有没有数据图需要数字化？
【人工 gate】无（机械处理，不涉及物理判断）
【retry_budget】本步最多重跑 5 轮，每轮必须有新证据/新假设。
【blocker_condition】PDF 损坏/加密无法读取；OCR 后关键公式或数据图仍不可辨认；缺少原始 PDF 或图片页导致后续参数无法追溯。
【预制脚本】无
```
