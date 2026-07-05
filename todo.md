# todo.md — SEPR 全局日志

> 每次 workflow 或 Eflow 结束前必须填一段。
> 论文命名规则: MMDD-NN-papername-vN（如 0629-01-akimov-mie-v1）

## 日志格式

每段格式：

```
## MMDD-NN-papername-vN (YYYY-MM-DD)
- 类型: workflow / Eflow
- 论文/批次: <名字>
- 摘要: <一句话>
- result_class: not_run / pipeline_completed / simulation_completed / diagnostic_only / surrogate_fallback / partial_physical_match / physical_reproduction_success（Eflow 无物理复现结果时写 not_run 或 N/A）
- 自迭代产出: 提交 X 个 skill 草稿到 toEflow/（或: 本次无）
- 待迭代需求: <需求或无>
```

---

（日志从这里开始追加）

## 0703-01-akimov-mie-v1 (2026-07-05)
- 类型: workflow
- 论文/批次: Akimov arXiv 2401.04146, Fig.3（超辐射/非辐射态 loci）
- 摘要: SEPR 首次真实论文复现，10步W-flow全部跑完，Gate1-4全过。CC独立求根Δ=0.0000证复现曲线数学正确，sr长尾归因数字化读图误差（known/accepted，不改阈值）。
- result_class: partial_physical_match
- 自迭代产出: 提交 2 个文件到 toEflow/（2401.04146.skill-suggestion.md 4条建议 + 2401.04146.blueprint-suggestion.md 无需蓝图）
- 待迭代需求: skill-suggestion建议1(P0)——main-agent复述纪律缺失，已发生两次真实转述漂移事故，需固化进main-agent SKILL防止后续case重演
