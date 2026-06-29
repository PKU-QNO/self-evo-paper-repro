# 05-generate_report（sub-E-agent 视角）

## 具体怎么干

你写治理报告初稿，对每条候选经验做四选一裁决建议。evolution-agent 读后做最终裁决。

### 报告步骤

1. **读所有材料**：
   - 审查报告（01 产出）
   - 聚类报告（02 产出）
   - skill 草稿（03 产出）
   - 验证报告（04 产出）
2. **整理候选经验清单**：从 clusters.md 提取每条候选经验
3. **四选一裁决建议**（核心工作）：

   对每条候选经验，按以下规则裁决：

   | 裁决 | 判断依据 |
   |------|---------|
   | **Save** | 独特的、具体的、scope 清楚、有 ≥1 case 支撑、不重复现有 skill |
   | **Improve** | 有价值但不完整：缺适用边界 / 缺具体步骤 / 缺验证方式 → 列出改进点 |
   | **Absorb** | 现有 skill 已有类似内容 → 展示 diff + 建议合并位置 + 合并理由 |
   | **Drop** | 琐碎（"记得调参数"）/ 冗余（skill 已覆盖）/ 太抽象（"提高精度"）→ 说明原因。Drop 不是消失，可能记 memento |

4. **写治理报告**

### 工具

- 预制脚本（`scripts/` 目录）：
  - （暂无）后续迭代补充
- 可 spawn 子子 agent 做 diff 对比：草稿 vs 原 skill

### 输出约定

- 治理报告：`.work/.evolution/<timestamp>/report.md`
- 每条候选经验的格式：

```markdown
## 候选经验 <编号>
- 来源 capsule：<列表>
- 类型：GUIDING / CAUTIONARY / FACT / PROCEDURE
- 建议裁决：Save / Improve / Absorb / Drop
- 理由：<基于验证数据的解释>
- 如 Improve：改进点列表
- 如 Absorb：目标 skill + 合并方式 + diff
- 如 Drop：原因（琐碎/冗余/抽象）
```

### 常见坑

- **Absorb 是高质量路径，不是"偷懒"。** 该合并的合并，不要图省事全 Save
- **Improve 要有具体改进点。** "改一下就行"不够，要列"具体改什么、怎么改"
- **Drop 不是说这经验没用。** 是说"不值得升级为 skill"——可能记到 memento 就行
- **四选一建议要有验证数据支撑。** 不凭感觉。"因为 replay 显示旧 case 无退化"、"因为仅 1 个 case 支撑不符合 PROCEDURE 门槛"
- **注意裁决倾向：** Save 门槛高（独特+完整+scope 清），Improve+Absorb 是主路径，Drop 正常

## 决策问题重点

1. **每条经验的四选一建议是什么？**
2. **Save 的够不够格？**（scope 清不清晰？）
3. **Absorb 的合不合理？**（合并后 skill 会不会太臃肿？）
4. **Drop 的理由站得住脚吗？**
5. **总体建议**：用户如果问"值不值得这次自迭代"，你怎么回答？
