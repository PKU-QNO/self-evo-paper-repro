# 04-validate_and_replay（evolution-agent 视角）

## 这步干什么

用新旧 skill 在旧 replay set 上跑对比验证。这是**防 self-bias 的客观闸门**——不能只靠"看起来更好"，要看量化数据。

## 输入

- 上一步的 skill 草稿（`.work/.evolution/<timestamp>/drafts/`）
- 当前 active skill（`.claude/skills/`）
- replay set：至少 1-2 篇已完成复现的旧 case（循序渐进，初期少没关系）
- 可选的 transfer case：和本次相关的未跑论文（测泛化）

## 输出要求

- replay 验证报告（`.work/.evolution/<timestamp>/validation/replay_report.md`）：
  - 每个旧 case：旧 skill 结果 vs 新 skill 结果
  - 退化检查：旧成功 case 的 pass/fail 状态不变或改善
  - transfer case：新 case 上的泛化表现
  - 物理 verifier 结果（能量守恒等客观判据）
- 如果发现退化，标注具体是哪项退化、严重程度

## 要传达给 sub-E-agent 的约定

- replay regression 不是"跑新结果"，是**对比新旧**：新旧 skill 在相同 case 上分别跑，对比输出
- 退化分级：
  - **严重**：旧 pass→新 fail（必须修或放弃这个修改）
  - **重要**：旧 0.95 精度→新 0.85（需审查）
  - **轻微**：旧 pass→新 pass 但数值有微小偏差（记录）
- 无退化 + 新 case 有改善 → 进 human gate
- 有退化 → 回滚对应修改 + 在报告中标注"此项修改需重审"
- verifier 脚本优先用已有（如 `energy_conservation.py`），不重造轮子
- 输出到 `.work/.evolution/<timestamp>/validation/`

## 本步 sub-E-agent 必须回答的决策问题

1. 新旧对比结果如何？每个旧 case 有退化吗？
2. 如果有退化，是哪个 skill 修改导致的？严重程度？
3. 物理 verifier 通过了吗？通过率？
4. 建议：这个 skill 修改可以进 gate 吗？还是需要回滚/重改？
5. replay set 够用吗？要不要补充？

## 人工 gate ④

**验证结果给用户看。** 确认：
- 退化检查数据（不要只看结论，看具体数字）
- 有退化的话，用户决定：回滚 / 重改 / 接受退化
- 无退化的话，用户决定进下一步
