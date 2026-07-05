# 03-reproduction_design（主 agent 视角）

## 这步干什么

设计复现目标，拆分成可执行的子任务。把论文 prose 转成结构化物理 spec，代码必须消费这个 spec，不能从 prose 直接生成代码（防"正确解了错题"）。

## 输出要求

- 物理 formalization spec（`.work/.todo/{paper}/{case}/formalization.yaml`）：
  - geometry（几何）
  - materials（材料+色散）
  - equations（方程）
  - boundary_conditions（边界条件）
  - sources（源）
  - solver（求解方式）
  - observables（可观测量）
  - assumptions（假设）
  - missing_fields（缺什么）
- 复现拆分计划（`.work/.todo/{paper}/{case}/repro_plan.md`）：分几步、每步产出什么、检验什么

## 要传达给子 agent 的约定

- spec 字段必须齐全，缺失的写 missing_fields，不能空着
- observables 要对应论文图的实际物理量
- solver 要明确是解析/半解析/数值
- **目标图只能从 step02 产出的候选（源自真实图清单、过 gate①）中选定**；papers.md/计划预写目标图是未核实线索，不得直接采用（2026-07-03 首跑教训）

## 本步子 agent 必须回答的决策问题

1. 复现目标是整篇还是单图？建议从哪张图开始？
2. 拆成几个子任务？依赖关系是什么？
3. 每个子任务的检验标准是什么？
4. **需不需要数值计算脚本？还是纯解析够？**（关键，影响 step 04 和 06）
5. **需不需要 magnus 云计算？还是本地跑得动？**（关键，影响 step 06）

## 人工 gate ②

**物理 formalization 后停下来**，让用户核对 spec 是否匹配论文物理问题。

## 下一步

→ 04-theory_and_implementation

## 本步 sub-agent spawn 局部模版

```
【第 03 步：reproduction_design】
【任务】设计复现目标，拆分成可执行的子任务。论文 prose → 结构化物理 spec，代码消费 spec 而非 prose。
【输入】.work/.todo/{paper}/{case}/paper_understanding.md / parameter_table.md / missing_info.md
【输出】.work/.todo/{paper}/{case}/formalization.yaml / repro_plan.md
【要传达的约定】spec 字段必须齐全，缺失的写 missing_fields 不能空着；observables 要对应论文图的实际物理量；solver 要明确是解析/半解析/数值。
【必须回答的决策问题】1.复现目标是整篇还是单图？建议从哪张图开始？2.拆成几个子任务？依赖关系是什么？3.每个子任务的检验标准是什么？4.需不需要数值计算脚本？还是纯解析够？5.需不需要 magnus 云计算？还是本地跑得动？
【人工 gate】②——物理 formalization 后停下来，让用户核对 spec 是否匹配论文物理问题。
【retry_budget】本步最多重跑 5 轮，每轮必须有新证据/新假设。
【blocker_condition】observables/solver/geometry/materials 任一核心字段无法闭合；检验标准无法量化；用户未确认 formalization 且存在物理目标歧义。
【预制脚本】无
```
