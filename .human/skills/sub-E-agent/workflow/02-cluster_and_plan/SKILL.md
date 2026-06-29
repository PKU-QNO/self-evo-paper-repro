# 02-cluster_and_plan（sub-E-agent 视角）

## 具体怎么干

你拿所有审查报告做跨 case 聚类，提取共性 pattern，按经验 4 类型分流，写修改计划。

### 聚类步骤

1. **读所有审查报告**：读 `.work/.evolution/<timestamp>/sub-reports/review-*.md`
2. **提取 pattern**：按 "什么问题 + 什么 capsule + 审查者意见" 的格式整理
3. **跨 case 归因**：同一个 pattern 出现在多少篇 capsule 里？是共性还是特例？
4. **4 type 分流**（核心决策）：

| type | 判断标准 | 例子 |
|------|---------|------|
| GUIDING | "这么做成功了，值得记住" | "先做网格收敛再跑全波，避免发散" |
| CAUTIONARY | "这么做失败了，别这样" | "材料虚部没确认就跑全波，结果全错" |
| FACT | 客观、可验证的碎片信息 | "Fig3 波长范围 600-800nm" |
| PROCEDURE | 可复用的流程/方法，需要 ≥2 case 才升级 | "对比论文图先 min-max 归一化" |

5. **规划修改计划**：根据聚类结果，列出要改哪些 skill、改什么、优先级

### 工具

- 预制脚本（`scripts/` 目录）：
  - （暂无）后续迭代补充
- 可 spawn 子子 agent 帮你做跨报告对比（读多份报告提取差异和共性）
- 可 spawn 子子 agent 读现有 skill 文件判断"这个发现是不是新"（有没有已在 skill 中）

### 输出约定

- 聚类报告：`.work/.evolution/<timestamp>/clusters.md`
  - 每条 pattern 写清楚：描述 / 涉及 capsule / 出现次数 / 4 type 分类
- 修改计划：`.work/.evolution/<timestamp>/plan.md`
  - 每项：目标 skill / 改什么 / 为什么 / 影响范围 / 优先级

### 常见坑

- **不要过度归纳。** 单案例的奇怪问题不要强行聚类成共性。标注"单 case，待观察"
- **不要漏掉共性。** 同一件问题在不同 capsule 里措辞不同（比如"忘了归一化"和"对比时坐标轴单位错了"可能同根因）
- **PROCEDURE 门槛记牢：≥2 case 才升。** 只有 1 个 case 的 Procedure 建议降为 GUIDING 或 FACT
- **修改计划要可操作。** 不要说"改进物理验证"，要说"在 energy_conservation.py 里加 LSPR 区域能量守恒检查"

## 决策问题重点

1. **跨 case vs 单 case**：有多少 capsule 证实了这个 pattern？
2. **4 type 分类**：分类依据是什么？PROCEDURE 是否满足 ≥2 case？
3. **影响范围**：改动影响几个 skill？有没有连锁反应？
4. **优先级**：CAUTIONARY（修 bug）> PROCEDURE（加复用）> GUIDING（记成功）> FACT（记碎片）
