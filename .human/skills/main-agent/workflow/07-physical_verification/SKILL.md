# 07-physical_verification（主 agent 视角）

## 这步干什么

跑物理通用检查（能量守恒、瑞利极限、大尺寸极限等）。这是"AI 没法糊弄"的硬约束层。

## 输出要求

- 物理验证报告（`.work/<case>/physical_verification.md`）：
  - 各 verifier 脚本结果（pass/fail + 数值）
  - 两方一致性状态
- benchmark.yaml 更新草稿（`.work/self-iteration/benchmark_<case>.yaml`）

## 要传达给子 agent 的约定

- 用 `optics-mie-reproduction/scripts/` 下的预制 verifier 脚本
- 3 层检验顺序：物理硬约束→极限退化→论文图量化
- 任何一层 fail 立即停，不继续
- verifier 通过 ≠ 物理复现成功，要分开写
- Layer 1 物理硬约束任一适用项失败 → 默认 `result_class` 不得高于 `diagnostic_only`，禁止声明 `physical_reproduction_success` 或 `partial_physical_match`。必须先修代码/模型，硬约束过了才能往上走。

## 本步子 agent 必须回答的决策问题

1. 3 层检验都过了吗？哪层 fail？
2. 两方（我们/论文图）一致吗？
3. 可以进结果分析了吗，还是要回 step 04 修代码？

## 人工 gate

fail 时触发关键节点"物理验证失败/换方案"问用户。

## 下一步

→ 08-result_analysis（全过）或 回 04（fail）

## 本步 sub-agent spawn 局部模版

```
【第 07 步：physical_verification】
【任务】跑物理通用检查（能量守恒、瑞利极限、大尺寸极限等）。这是"AI 没法糊弄"的硬约束层。
【输入】.work/{case}/data/*.csv / code/*.py
【输出】.work/{case}/physical_verification.md / .work/self-iteration/benchmark_{case}.yaml（草稿）
【要传达的约定】用 optics-mie-reproduction/scripts/ 下的预制 verifier 脚本；3 层检验顺序：物理硬约束→极限退化→论文图量化；任何一层 fail 立即停不继续；verifier 通过 ≠ 物理复现成功，要分开写；Layer 1 物理硬约束任一适用项失败 → 默认 result_class 不得高于 diagnostic_only，禁止声明 physical_reproduction_success 或 partial_physical_match，必须先修代码/模型。
【必须回答的决策问题】1.3 层检验都过了吗？哪层 fail？2.两方（我们/论文图）一致吗？3.可以进结果分析了吗，还是要回 step 04 修代码？
【人工 gate】fail 时触发关键节点"物理验证失败/换方案"问用户。
【retry_budget】本步最多重跑 5 轮，每轮必须有新证据/新假设。
【blocker_condition】任一 verifier 连续 fail 且无新假设；硬约束/极限退化/论文图量化任一层无法生成证据；同一 verifier fingerprint 第二次失败。
【预制脚本】optics-mie-reproduction/scripts/ 下预制 verifier 脚本
```
