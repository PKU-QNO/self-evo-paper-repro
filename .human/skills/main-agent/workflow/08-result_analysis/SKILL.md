# 08-result_analysis（主 agent 视角）

## 这步干什么

分析结果，归因差异。把数值结果和论文图量化对比，不靠"看着像"。

## 输出要求

- 结果分析报告（`.work/<case>/result_analysis.md`）：
  - `result_class`：必须使用 CLAUDE.md 的 7 级枚举之一
  - 曲线 RMSE、共振峰位误差（nm）、Q 值相对误差
  - 差异归因（参数/模型/数值精度/论文图数字化误差）
  - 物理结论（如三区过渡、多极出现顺序）
- 对比图（`.work/<case>/figs/comparison_*.png`）：我们的+论文+PyMieScatt 三方叠加

## 要传达给子 agent 的约定

- 量化对比，不靠肉眼：RMSE、峰位误差、Q 值误差
- 差异要归因，不能只说"有差异"
- 物理结论要基于数值，不是复述论文
- 报告必须显式标注 `result_class`，不得把 `surrogate_fallback`、`diagnostic_only`、`pipeline_completed` 写成物理复现成功

## 本步子 agent 必须回答的决策问题

1. 数值在容差内吗？容差是谁定的（用户定，不是 AI）？
2. 差异主要来自哪里？
3. 物理结论是什么？符合论文吗？
4. 这次算物理复现成功、部分复现、还是 fallback？

## 人工 gate ④

**论文图对比后停下来**，让用户看量化误差数字，决定 pass/fail。不听"基本一致"。

## 下一步

→ 09-reproducibility_selfcheck

## 本步 sub-agent spawn 局部模版

```
【第 08 步：result_analysis】
【任务】分析结果，归因差异。数值结果和论文图量化对比，不靠"看着像"。
【输入】.work/{case}/data/*.csv / physical_verification.md
【输出】.work/{case}/result_analysis.md（必须含 result_class，使用 CLAUDE.md 7 级枚举）/ figs/comparison_*.png
【要传达的约定】量化对比不靠肉眼：RMSE、峰位误差、Q 值误差；差异要归因，不能只说"有差异"；物理结论要基于数值不是复述论文；报告必须显式标注 result_class，不得把 surrogate_fallback、diagnostic_only、pipeline_completed 写成物理复现成功。
【必须回答的决策问题】1.数值在容差内吗？容差是谁定的（用户定，不是 AI）？2.差异主要来自哪里？3.物理结论是什么？符合论文吗？4.这次算物理复现成功、部分复现、还是 fallback？
【人工 gate】④——论文图对比后停下来，让用户看量化误差数字，决定 pass/fail。
【retry_budget】本步最多重跑 5 轮，每轮必须有新证据/新假设。
【blocker_condition】论文图无法数字化或对齐；容差未由用户/协议确认；差异归因只剩猜测无证据；结果只能标 fallback/blocked 但不能自称成功。
【预制脚本】无
```
