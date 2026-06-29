# Evolution Agent 总结报告模板（第 6 步）

> evolution-agent 工作结束前必须写这份报告，写到 `.work/.evolution/<timestamp>/evolution_report.md`。
> 这是自迭代 workflow 的第 6 步，sub-E-agent 的各步报告是分步产出，本报告是 evolution-agent 站在编排者视角的全局总结。

## 报告正文

### 1. 本次自迭代概况
- 触发时间：`<ISO 时间>`
- 审查的 capsule 数量：`<N>`
- 涉及论文：`<列表>`
- 涉及的 skill：`<列表>`
- 最终裁决结果：`<全局状态：全部通过 / 部分通过 / 全部沙箱>`

### 2. 6 步执行轨迹
（每步一句话：做了什么、产出路径、用户 gate 结果）

### 3. 经验聚类概况
- GUIDING 经验：`<数量>`
- CAUTIONARY 经验：`<数量>`
- FACT 经验：`<数量>`
- PROCEDURE 经验：`<数量>`
- 四选一统计：Save `<N>` / Improve `<N>` / Absorb `<N>` / Drop `<N>`

### 4. 关键决策点回顾
（你在哪些节点拍了板、拍了什么、依据什么）

### 5. 人工 gate 记录
（每步用户说了什么、批了什么、否了什么）

### 6. skill 变更清单
| skill | 操作 | 沙箱草稿路径 | 状态 |
|-------|------|-------------|------|
| xxx | 新建/修改/合并/拆分 | `.work/.evolution/...` | active/sandbox |

### 7. 验证结果摘要
- replay regression 结果：`<旧 case 无退化 / 有退化已回滚>`
- 物理 verifier：`<全部通过 / 部分通过>`
- 新 case 泛化：`<有改善 / 持平 / 下降>`

### 8. 长期记忆更新
- 本次自迭代的全局经验
- 哪些记忆写入了 memento、哪些存了 pitfalls_log

---

```yaml
---
report_meta:
  agent_role: evolution-agent
  capsule_count: <N>
  timestamp: <ISO>
  final_status: all_passed | partial | all_dropped
steps_executed:
  - step: 01-concurrent_review
    status: completed
    sub_reports: <.work/.evolution/... 路径>
  - step: 02-cluster_and_plan
    status: completed
  - step: 03-concurrent_skill_work
    status: completed
  - step: 04-validate_and_replay
    status: completed
  - step: 05-generate_report
    status: completed
human_gates:
  - step: 01
    user_decision: <批准/否>
  - step: 02
    user_decision: <批准/否>
  - step: 03
    user_decision: <批准/否>
  - step: 04
    user_decision: <批准/否>
  - step: 05
    user_decision: <批准/否>
skill_changes:
  - skill: <名称>
    action: create | modify | merge | split
    draft_path: <沙箱路径>
    verdict: save | improve | absorb | drop
    final_status: active | sandbox
memory_update:
  memento_ids: <列表>
  summary: <一句话>
---
```
