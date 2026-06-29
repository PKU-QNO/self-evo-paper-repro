# Sub-E Agent 工作报告模板

> sub-E-agent 任务结束前必须填这份报告，写到 `.work/.evolution/<timestamp>/sub-reports/<step>-<task>-<timestamp>.md`。
> 人看 Markdown 部分，agent 读末尾 yaml 字段。报告是给 evolution-agent 和下一步接力的。

## 报告正文（Markdown，人看）

### 1. 身份声明
- 我是：sub-E-agent（被 `<evolution-agent>` spawn）
- 做哪一步：`0X-xxx`
- 任务：`<一句话>`
- 是否涉及 capsule：`<涉及的 capsule 列表>`

### 2. 做了什么
（事实陈述，不评价。如："读了 3 篇 capsule 报告，提取了 5 个共性 pattern"）

### 3. 用了什么
- 工具/脚本：`<用了什么>`
- 输入文件：`<读了哪些>`
- 参考的 skill：`<读了哪些 skill 文件>`

### 4. 遇到什么问题
（没有写"无"。有问题写清楚什么问题、怎么处理的；没问题写"未遇到阻碍"）

### 5. 结果
- 产物路径：`<.work/.evolution/ 下的输出文件>`
- 关键发现：`<列表>`
- 验证状态：`<pass/fail/pending>`

### 6. 决策性回答 ★关键
（回答 evolution-agent 在 workflow SKILL.md 里列出的"本步必须回答的决策问题"。你给建议，evolution-agent 拍板。）

### 7. 下一步需要的输入
（给下一步或 evolution-agent 的接力信息：它需要什么文件、什么参数、注意什么）

### 8. 长期记忆更新
（写 memento 的内容摘要：本次沉淀了什么经验教训。每条要标 type：GUIDING/CAUTIONARY/FACT/PROCEDURE，并引用来 capsule 编号。）

---

## yaml 字段（末尾，agent 读）

```yaml
---
report_meta:
  agent_role: sub-E-agent
  step: 0X-xxx
  task: <一句话>
  capsule_ids:
    - <capsule_1>
    - <capsule_2>
  spawned_by: evolution-agent
  timestamp: <ISO>
  status: completed | blocked | failed
artifacts:
  - path: <.work/.evolution 下路径>
    type: review | cluster | draft | validation | report
    description: <一句话>
key_decisions:
  - question: <evolution-agent列出的决策问题>
    recommendation: <你的建议>
    confidence: low | medium | high
    supporting_evidence: <哪篇 capsule/验证数据>
handoff:
  next_step: 0X-xxx
  next_needs:
    - <文件/参数/注意>
experience_updates:
  - type: GUIDING | CAUTIONARY | FACT | PROCEDURE
    capsule_source: <来源 capsule 编号>
    summary: <一句话>
    memory_action: store | pitfalls_log | decisions_log
---
```
