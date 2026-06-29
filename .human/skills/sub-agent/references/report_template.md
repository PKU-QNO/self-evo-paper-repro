# 子 agent 工作报告模板

> 子 agent 任务结束前必须填这份报告，写到 `.work/.sub-report/<step>-<task>-<timestamp>.md`。
> 人看 Markdown 部分，agent 读末尾 yaml 字段。报告是给主 agent 和下一个子 agent 接力的。

## 报告正文（Markdown，人看）

### 1. 身份声明
- 我是：子 agent（被 `<父agent>` spawn）
- 做哪一步：`0X-xxx`
- 任务：`<一句话>`

### 2. 做了什么
（事实陈述，不评价）

### 3. 用了什么
- 参数：`<列出关键参数和值>`
- 工具/脚本：`<用了什么>`
- 输入文件：`<读了哪些>`

### 4. 遇到什么问题
（没有写"无"。有问题写清楚什么问题、怎么处理的；没问题写"未遇到阻碍"）

### 5. 结果
- 产物路径：`<.work 下的输出文件>`
- 关键数值：`<列表>`
- 验证状态：`<pass/fail/pending>`

### 6. 决策性回答 ★关键
（回答主 agent 在 workflow SKILL.md 里列出的"本步必须回答的决策问题"。子 agent 给建议，主 agent 拍板。）

示例（step 04 理论实现）：
- 需不需要数值计算脚本？`<需要/不需要，理由>`
- 需不需要 magnus 云计算？`<需要/不需要，理由>`
- 代码复杂度预估？`<高/中/低，哪些用 scipy.special、哪些自写>`

### 7. 下一步需要的输入
（给下一个子 agent 的接力信息：它需要什么文件、什么参数、注意什么）

### 8. 长期记忆更新
（写 memento 的内容摘要：本次沉淀了什么事实/决策/教训）

---

## yaml 字段（末尾，agent 读）

```yaml
---
report_meta:
  agent_role: sub-agent
  step: 0X-xxx
  task: <一句话>
  spawned_by: <父agent>
  timestamp: <ISO>
  status: completed | blocked | failed
artifacts:
  - path: <.work 下路径>
    type: code | data | figure | note | report
    description: <一句话>
key_values:
  - name: <物理量>
    value: <数值>
    unit: <单位>
    verifier: pass | fail | pending
decisions:
  - question: <主agent列出的决策问题>
    recommendation: <子agent建议>
    confidence: low | medium | high
handoff:
  next_step: 0X-xxx
  next_needs:
    - <文件/参数/注意>
memory_update:
  memento_id: <如有>
  summary: <一句话>
---
```
