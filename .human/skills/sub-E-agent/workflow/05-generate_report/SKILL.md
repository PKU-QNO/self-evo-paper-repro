# 05-generate_report（sub-E-agent 视角）

## 具体怎么干

你写治理报告初稿，对每条候选经验做六维裁决 + 三级治理建议。evolution-agent 读后做最终裁决。

### 报告步骤

1. **读所有材料**：
   - 审查报告（01 产出）
   - 聚类报告（02 产出）
   - skill 草稿（03 产出）
   - 验证报告（04 产出）
2. **整理候选经验清单**：从 clusters.md 提取每条候选经验
3. **六维裁决 + 三级治理建议**（核心工作）：

   对每条候选经验，先按六维裁决，再定 tier：

   | 裁决 | 判断依据 |
   |------|---------|
   | **Save** | 独特的、具体的、scope 清楚、有 ≥1 case 支撑、不重复现有 skill |
   | **Improve then Save** | 有价值但不完整：缺适用边界 / 缺具体步骤 / 缺验证方式 → 列出改进点 + 修订版 |
   | **Absorb (Merge)** | 经验与已有 skill 兼容 → 展示 diff + 建议合并位置 + 合并理由 |
   | **Fork** | 经验与已有 skill 冲突/不兼容 → 在 skill 内创建 scope 分支，带冲突标注（不强行合并） |
   | **Archive** | 有价值但不足以进 skill → 存负面知识库，带 source/claim/evidence/why_not_skill/scope 字段 |
   | **Drop** | 琐碎（"记得调参数"）/ 冗余（skill 已覆盖）/ 太抽象（"提高精度"）→ 说明原因。Drop 不是消失，可能记 memento |

   同时给每条经验定 tier：
   - **Tier-1**：单 case 无 verifier → Archive，不进 skill
   - **Tier-2**：≥2 case 或 1 case + verifier 通过 → candidate pending
   - **Tier-3**：≥3 case + verifier + replay 无退化 → active 升级

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
- 建议裁决：Save / Improve / Absorb / Fork / Archive / Drop
- Tier：Tier-1 / Tier-2 / Tier-3（附 case count + verifier 结果）
- 置信度：0.3 / 0.5 / 0.7 / 0.85
- scope 边界：<此经验适用/不适用的范围>
- 冲突清单：<如有冲突经验，列出冲突方向>
- 理由：<基于验证数据的解释>
- 如 Improve：改进点列表
- 如 Absorb：目标 skill + 合并方式 + diff
- 如 Fork：冲突边界 + 分支方案
- 如 Archive：source / claim / evidence / why_not_skill / scope
- 如 Drop：原因（琐碎/冗余/抽象/噪声）
```

### 常见坑

- **Absorb 和 Improve 是高质量路径，不是"偷懒"。** 该合并的合并，不要图省事全 Save
- **Improve 要有具体改进点。** "改一下就行"不够，要列"具体改什么、怎么改"
- **Fork 不是推卸。** 冲突经验各自正确就要明确分支 scope，不要强行合并
- **Archive 不是 Drop。** 五个字段必须完整，否则以后检索不了
- **Drop 不是说这经验没用。** 是说"不值得升级为 skill"——可能记到 memento 就行
- **六维建议 + tier 都要有验证数据支撑。** 不凭感觉。"因为 replay 显示旧 case 无退化"、"因为仅 1 个 case 支撑不符合 PROCEDURE 门槛"
- **注意裁决倾向：** Save 门槛高（独特+完整+scope 清），Improve+Absorb 是主路径，Fork 和 Archive 是创新点

## 决策问题重点

1. **每条经验的六维建议是什么？tier 几级？**
2. **Save 的够不够格？**（scope 清不清晰？）
3. **Absorb 的合不合理？**（合并后 skill 会不会太臃肿？）
4. **Fork 的冲突边界清不清楚？**（不强行合并的理由是否充分？）
5. **Archive 的五个字段全不全？**（缺了以后检索不了）
6. **Drop 的理由站得住脚吗？**
7. **总体建议**：用户如果问"值不值得这次自迭代"，你怎么回答？
