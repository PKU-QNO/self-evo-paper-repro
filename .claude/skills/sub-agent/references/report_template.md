# 子 agent 工作报告模板

> 子 agent 任务结束前必须填这份报告，写到 `.work/.sub-report/<step>-<task>-<timestamp>.md`。
> 人看 Markdown 部分，agent 读末尾 yaml 字段。报告是给主 agent 和下一个子 agent 接力的。

## 报告正文（Markdown，人看）

### 固定头（6字段，必须放在正文最前）
- role：W-sub
- task_scope：`<做哪一步、什么任务>`
- evidence_refs：`<引用了哪些 artifact/数据/报告路径>`
- confidence：低 / 中 / 高
- blocked_by：`<被什么卡住；无则写 none>`
- recommended_action：`<建议主 agent 下一步做什么>`

> 固定头是下面 8 字段报告的精简前置，内容可与第 1/3/4/6/7 字段重复，但不能省略。

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

每个决策性回答必须显式写：
- `uncertainty`：本次判断的不确定度（低/中/高 + 理由）
- `missing_evidence`：还缺什么证据才能更确定（列出要补的文件、数值、verifier、人工确认等）

不能只写"基本一致"、"看起来对"、"应该可行"；必须说明不确定度和缺证据。

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
    uncertainty: <低/中/高 + 理由>
    missing_evidence:
      - <还缺什么证据才能更确定>
    provenance:
      source_artifact: <来源 artifact，论文+图/case/skill版本>
      evidence_type: <数值/verifier结果/代码片段/人工确认>
      timestamp_version: <时间戳或版本>
      scope_applicability: <适用范围/边界>
      confidence_result_class: <置信度 + result_class>
handoff:
  next_step: 0X-xxx
  next_needs:
    - <文件/参数/注意>
memory_update:
  memento_id: <如有>
  summary: <一句话>
  provenance:
    source_artifact: <来源 artifact，论文+图/case/skill版本>
    evidence_type: <数值/verifier结果/代码片段/人工确认>
    timestamp_version: <时间戳或版本>
    scope_applicability: <适用范围/边界>
    confidence_result_class: <置信度 + result_class>
---
```

# 执行版补充：报告字段强约束

## 固定头 6 字段
- `role`: 只能写当前身份，如 sub-agent 或 sub-E-agent。
- `task_scope`: 一句话限定本次只做什么。
- `evidence_refs`: artifact 路径列表，不得只写“见上文”。
- `confidence`: low/medium/high，并说明原因。
- `blocked_by`: 无阻塞写 none；有阻塞写具体缺失物。
- `recommended_action`: 给父 agent 的下一步建议。

## 8 字段主体
1. 身份声明。
2. 做了什么，按时间顺序列动作。
3. 用了什么，列工具、脚本、文献、记忆。
4. 遇到什么问题，区分已解决和未解决。
5. 结果，列产物路径、关键数值、verifier 状态、result_class。
6. 决策性回答，逐条回答父 agent 问题。
7. 下一步需要的输入，缺失就写 exact request。
8. 长期记忆更新，列 dedup 状态、写入内容或不写原因。

## uncertainty 与 missing_evidence
- 每个判断都写 `uncertainty: low|medium|high`。
- 每个判断都写 `missing_evidence`；没有缺失写 `none`。
- 若缺失会影响 result_class，上调必须禁止，下调并解释。
