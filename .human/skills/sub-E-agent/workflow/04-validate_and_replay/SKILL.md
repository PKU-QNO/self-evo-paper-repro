# 04-validate_and_replay（sub-E-agent 视角）

## 具体怎么干

你拿新旧 skill 版本在旧 case 上跑对比验证。这一步不做"跑新结果"，做**对比**。

### 验证步骤

1. **读旧 skill 版本**：读 `.claude/skills/<skill-name>/SKILL.md`（当前 active）
2. **读新 skill 草稿**：读 `.work/.evolution/<timestamp>/drafts/<skill-name>.skill.yaml`
3. **确定 replay set**：从 evolution-agent 的分配中获取（至少 1-2 篇已完成复现的旧 case）
4. **如果有 transfer case**：读和本次相关的未跑论文 capsule
5. **跑对比**：
   - 对每个旧 case：用旧 skill 跑一遍、用新 skill 跑一遍
   - 对比结果：数值、pass/fail 状态、物理 verifier 通过率
   - 关键指标：旧成功 case 在新 skill 下是否保持成功
6. **判定退化和改善**：
   - 列每个旧 case 的对比结果
   - 统计退化（旧 pass→新 fail）数量
   - 统计改善（旧 fail→新 pass 或精度提升）数量

### 工具

- 预制脚本（`scripts/` 目录）：
  - （暂无）后续迭代补充。初期手动跑 case，记录对比数据
- 物理 verifier 脚本（如果已有）：如 `energy_conservation.py`
- 可 spawn 子子 agent 分别跑旧 skill 和新 skill 的验证，减轻自身负载

### 对比数据格式

每个旧 case 输出：

```
case: <case_name>
旧 skill 结果: pass/fail + 关键数值
新 skill 结果: pass/fail + 关键数值
verifier 旧: pass/fail
verifier 新: pass/fail
退化判定: 无退化 / 有退化（具体哪项）
改善判定: 有改善（具体哪项）/ 持平 / 下降
```

### 输出约定

- 验证报告：`.work/.evolution/<timestamp>/validation/replay_report.md`
  - 每个旧 case 的对比数据
  - transfer case（如有）的泛化数据
  - 退化严重程度
  - 总体判定：可进 gate / 需回滚 / 需重改

### 常见坑

- **不要只跑一次看结果就开始写报告。** 确认脚本参数、单位、环境一致
- **退化不一定是 skill 改错了，也可能是环境不一致。** 确认新旧 skill 在同一个测试环境下跑
- **精度提升 0.1% 不是改善。** 数值波动范围内的差异忽略。只有明显变化（>1% 或 pass/fail 状态变化）才记录
- **transfer case 的"改善"权重低于旧 case 的"无退化"。** 泛化好是加分项，但不抵消退化
- **物理 verifier 的通过是硬约束。** 新 skill 如果导致 verifier 从 pass 变 fail，不管数值多好都算退化

## 决策问题重点

1. **退化了没有**：逐 case 列出
2. **谁导致的**：退化可定位到具体哪个 skill 修改吗？
3. **能否进 gate**：你的建议是什么？（可进 / 回滚该项修改 / 重改）
4. **replay set 够不够**：测试覆盖是否充分？
