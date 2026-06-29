# 主 agent 总结报告模板（第 11 步）

> 主 agent 工作结束前必须写这份报告，写到 `.work/.sub-report/main-<case>-<timestamp>.md`。
> 这是 workflow 的第 11 步，子 agent 的 step 10 报告是经验+记忆+双报告，本报告是主 agent 的全局总结。

## 报告正文

### 1. 本次复现概况
- 目标论文：`<论文>`
- 目标图/物理量：`<图号>`
- 最终状态：`<物理复现成功 / 部分复现 / fallback / 失败>`

### 2. 10 步执行轨迹
（每步一句话：做了什么、结果、是否有问题。引用各步子 agent 报告路径。）

### 3. 关键决策点回顾
（主 agent 在哪些节点拍了板、拍了什么、依据是什么。尤其"需不需要数值脚本/需不需要 magnus"这类。）

### 4. 人工 gate 记录
（哪些节点请求了用户意见、用户说了什么。）

### 5. 最终成果
- 进入 `.result/` 的内容：`<列表>`
- benchmark 更新：`<条目>`
- skill 更新：`<哪些 skill 改了，沙箱草稿路径>`

### 6. 自迭代建议
（本次复现暴露了哪些 skill 缺陷、哪些值得自迭代。给自迭代 workflow 的输入。注意：自迭代要过 human gate。）

### 7. 给下一篇的接力
（本次学到的、下一篇复现要注意的。）

### 8. 长期记忆更新摘要
（主 agent 自己也更新 memento：本次 case 的全局结论。）

---

```yaml
---
report_meta:
  agent_role: main-agent
  case: <论文-图>
  timestamp: <ISO>
  final_status: physical_reproduction | partial | fallback | failed
steps_executed:
  - step: 01-pdf_preprocessing
    status: completed
    sub_report: <.work/.sub-report 路径>
  - step: 02-paper_reading
    status: completed
    sub_report: <路径>
  # ... 10 步
human_gates:
  - node: <请求节点>
    user_decision: <用户决定>
result_artifacts:
  - path: <.result 下路径>
    type: benchmark | skill | blueprint | report
memory_update:
  memento_id: <如有>
  summary: <一句话>
---
```
