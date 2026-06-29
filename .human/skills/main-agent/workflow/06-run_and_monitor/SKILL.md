# 06-run_and_monitor（主 agent 视角）

## 这步干什么

运行代码，监视执行。本地跑或 magnus 云跑（step 04 决定的）。

## 输出要求

- 运行日志（`.work/<case>/run_log.md`）：命令、耗时、输出
- 结果数据（`.work/<case>/data/*.csv`）
- 初步图（`.work/<case>/figs/*.png`）
- 异常记录（如有）

## 要传达给子 agent 的约定

- 先跑最小 smoke case 确认能跑，再跑完整扫描
- 本地跑得动就本地，magnus 云跑要保守提交（查现有 job、资源不过半）
- 监视输出，数值异常（NaN/Inf/负值）立即停
- 保留日志，不要覆盖

## 本步子 agent 必须回答的决策问题

1. 跑成功了吗？有没有 NaN/Inf/异常值？
2. 初步结果形状对吗（峰在该出现的位置吗）？
3. 耗时和资源多少？要不要换 magnus？
4. 可以进物理验证了吗？

## 人工 gate

无（这步是执行，异常时触发关键节点"物理验证失败/换方案"问用户）

## 下一步

→ 07-physical_verification
