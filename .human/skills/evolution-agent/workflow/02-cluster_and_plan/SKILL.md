# 02-cluster_and_plan（evolution-agent 视角）

## 这步干什么

拿所有审查报告做跨 case 聚类，提取共性 pattern，按经验 4 类型分流，规划哪些 skill 需要改。

## 输入

- 上一步的 N 份审查报告（`.work/.evolution/<timestamp>/sub-reports/`）
- 各篇 capsule 原始工作报告

## 输出要求

- 聚类报告（`.work/.evolution/<timestamp>/clusters.md`）：
  - 跨 capsule 的共性 pattern（哪些坑反复出现、哪些技巧反复有效）
  - 每类 pattern 的 case 支撑数量
  - 经验 4 type 分类结果
- 修改计划（`.work/.evolution/<timestamp>/plan.md`）：
  - 要改哪些 skill，每项改什么
  - 需要新建哪些 skill（如果需要）
  - 哪些经验建议 absorb 到已有 skill
  - 优先级排序
- 每项修改计划要明确：影响范围 / 验证方案 / 回滚方案

## 要传达给 sub-E-agent 的约定

- 经验分 4 type 分流，不是一锅烩：

| type | 是什么 | 存哪 | 升级门槛 |
|------|--------|------|---------|
| GUIDING | 成功根因 | 提示词备注 | 1 次就记 |
| CAUTIONARY | 失败教训 | pitfalls_log | 1 次就要记 |
| FACT | 可验证碎片 | memento fact | 1 次就记 |
| PROCEDURE | 可复用流程 | skill candidate | ≥2 case 才升 active |

- 不要把所有发现都写进 skill——要判断"值得升级"还是"记一下就行"
- 修改计划优先级：修复 bug（CAUTIONARY）> 补充用例（FACT）> 优化流程（PROCEDURE）> 记录成功（GUIDING）
- 输出 `.work/.evolution/<timestamp>/clusters.md` 和 `plan.md`

## 本步 sub-E-agent 必须回答的决策问题

1. 哪些 pattern 是跨 case 共性、哪些是单 case 特例？
2. 每条候选经验应该走 4 type 的哪一类？
3. 修改计划中，改动会影响多少个现有 skill？
4. 有没有"改一个 skill 导致其他 case 退化"的风险？
5. 优先改哪个？为什么？

## 人工 gate ②

**聚类结果和修改计划给用户看。** 确认：
- 聚类方向对不对（有没有漏共性、有没有过度归纳）
- 修改计划的范围合不合理
- 优先级是否合理
