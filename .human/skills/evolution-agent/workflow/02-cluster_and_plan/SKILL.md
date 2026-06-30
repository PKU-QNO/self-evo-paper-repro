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
  - 每条候选经验/改动必须带 5 字段：`candidate_id`（唯一 ID）、`evidence_ref`（引用 capsule/verifier 结果/数值）、`decision`（Save/Improve/Absorb/Fork/Archive/Drop）、`tier`（Tier-1/2/3）、`rollback_ref`（接受后出问题回滚到哪个版本）
- 修改计划（`.work/.evolution/<timestamp>/plan.md`）：
  - 要改哪些 skill，每项改什么
  - 需要新建哪些 skill（如果需要）
  - 哪些经验建议 absorb 到已有 skill
  - 优先级排序
  - 每项修改计划要明确：影响范围 / 验证方案 / 回滚方案 / candidate_id / evidence_ref / decision / tier / rollback_ref
- 冲突台账（`.work/.evolution/<timestamp>/conflict_ledger.yaml`）：聚类时发现冲突必须记录，不自动调和

## conflict ledger（冲突台账）

聚类时只要发现以下情况，必须写入 `conflict_ledger.yaml`：同一现象得到不同结论、同一参数出现不同值、候选经验与已有 skill 冲突。冲突不自动调和；一旦进入台账，触发 Tier-2/3 人审。

每条冲突记录必须包含字段：

```yaml
- conflict_id: <稳定编号，如 conflict-001>
  冲突项描述: <同现象不同结论/同参数不同值/经验与已有skill冲突的具体描述>
  来源A: <论文/case/已有skill + 路径或版本>
  来源B: <论文/case/已有skill + 路径或版本>
  当前采用项: <本轮暂时采用的说法/参数/经验>
  被拒项: <本轮暂不采用的说法/参数/经验>
  "裁决人/agent": <裁决人或 agent 身份>
  复查条件: <出现什么新证据时重新审>
```

写台账只代表需要审查，不代表已经证明某一方错误。若证据不足，`当前采用项` 可以写 `pending`，但不能删除冲突。

## 要传达给 sub-E-agent 的约定

- 经验分 4 type 分流，不是一锅烩：

| type | 是什么 | 存哪 | 升级门槛 |
|------|--------|------|---------|
| GUIDING | 成功根因 | 提示词备注 | 1 次就记 |
| CAUTIONARY | 失败教训 | pitfalls_log | 1 次就要记 |
| FACT | 可验证碎片 | memento fact | 1 次就记 |
| PROCEDURE | 可复用流程 | skill candidate | ≥2 case 才升 active |

- 不要把所有发现都写进 skill——要判断"值得升级"还是"记一下就行"
- 发现冲突必须写入 `.work/.evolution/<timestamp>/conflict_ledger.yaml`，冲突不自动调和，进入 Tier-2/3 人审
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

## 局部 spawn 模版（供 evolution-agent 拼接用）

```
【第 02 步：cluster_and_plan】
【任务】拿所有审查报告做跨 case 聚类，提取共性 pattern，按经验 4 类型分流，规划哪些 skill 需要改。
【输入】上一步的 N 份审查报告（`.work/.evolution/<timestamp>/sub-reports/`）；各篇 capsule 原始工作报告
【输出】聚类报告（`.work/.evolution/<timestamp>/clusters.md`）含跨 capsule 共性 pattern + 4 type 分类和 case 支撑数量；修改计划（`.work/.evolution/<timestamp>/plan.md`）含要改哪些 skill、新建/absorb 方案、优先级排序和每项的影响范围/验证方案/回滚方案；如发现冲突，写冲突台账（`.work/.evolution/<timestamp>/conflict_ledger.yaml`）
【要传达的约定】经验分 4 type 分流（GUIDING/CAUTIONARY/FACT/PROCEDURE）不是一锅烩，各有存地和升级门槛；不要把所有发现都写进 skill——要判断"值得升级"还是"记一下就行"；发现冲突（同现象不同结论/同参数不同值/经验与已有skill冲突）必须写入 conflict ledger，字段含 conflict_id、冲突项描述、来源A、来源B、当前采用项、被拒项、裁决人/agent、复查条件；冲突不自动调和，触发 Tier-2/3 人审；修改计划优先级：修复 bug（CAUTIONARY）> 补充用例（FACT）> 优化流程（PROCEDURE）> 记录成功（GUIDING）
【必须回答的决策问题】1. 哪些 pattern 是跨 case 共性、哪些是单 case 特例？2. 每条候选经验应该走 4 type 的哪一类？3. 修改计划中，改动会影响多少个现有 skill？4. 有没有"改一个 skill 导致其他 case 退化"的风险？5. 优先改哪个？为什么？
【人工 gate】② 聚类结果和修改计划给用户看。确认聚类方向对不对、有没有漏共性或过度归纳、修改计划范围合不合理、优先级是否合理。
【并发说明】不并发，evolution-agent 自己做。可 spawn 一个 sub-E-agent 协助分析，但聚类结论和修改计划由 evolution-agent 审裁。
【预制脚本】无（尚未建立）
```
