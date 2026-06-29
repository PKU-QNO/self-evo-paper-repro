# 01-concurrent_review（sub-E-agent 视角）

## 具体怎么干

你被分配审查一篇 capsule。这篇 capsule 不是你参与复现的——如果 evolution-agent 分配错，立即报告。

### 审查步骤

1. **读 capsule**：读 `.work/.result/<case>/capsule.md` 和子 agent 原始工作报告
2. **读原始报告**：读子 agent 在 `.work/.sub-report/` 下的工作报告（特别是第 8 字段经验）
3. **对抗式审查**：假设 capsule 有遗漏，去找遗漏：
   - 执行者说"成功"——验证他的通过标准（是不是物理上成功？还是代码跑了就叫成功？）
   - 执行者说"失败"——确认他归因对了（有没有可能问题出在执行者自己的代码而不是物理？）
   - 执行者说"经验 X"——这个经验够不够具体？还是笼统废话？
4. **判断 self-bias 风险**：执行者有没有自己夸自己？归因有没有偏向自己？
5. **提取 skill 改进点**：这篇 capsule 暴露了哪个 skill 的什么问题？

### 工具

- 预制脚本（`scripts/` 目录）：
  - （暂无）后续迭代补充
- 可 spawn 子子 agent 读 capsule 中的代码/数据做辅助验证

### 输出约定

- 审查报告写到 `.work/.evolution/<timestamp>/sub-reports/review-<case>-<timestamp>.md`
- 用 8 字段模板
- 第 6 字段重点回答：成功/失败根因、skill 缺陷、self-bias 风险
- 第 8 字段标经验 type，引用 capsule 编号

## 常见坑

- **不要重做复现。** 你的任务是审查 capsule，不是重新跑一遍。发现证据不足时写"blocked"，不自己补实验
- **对抗式不是找茬。** 假设有错去找错，但找到了要归因到具体位置、给出合理怀疑理由
- **self-bias 的判断要有依据。** 不说"我觉得他不对"，要说"他在第 X 步报告里说通过了 Y 验证，但 Z 数据显示..."
- **注意胶囊是"工作报告 capsule"不是"论文 PDF"。** 审的是执行过程，不是原论文

## 决策问题重点

1. **根因**：成功/失败是真根因还是表面归因？
2. **skill 缺陷**：有没有足够证据说这个 skill 有问题？
3. **self-bias 风险**：高/中/低？依据？
4. **经验 type**：为什么归为这个 type？（因为≥2 case 才 PROCEDURE？1 次就 CAUTIONARY？）
