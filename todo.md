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
