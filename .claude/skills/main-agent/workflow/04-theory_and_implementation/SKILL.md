# 04-theory_and_implementation（主 agent 视角）

## 这步干什么

理论推导 + 代码实现。从 Maxwell 方程到最终表达式的完整推导，然后用 Python 实现。核心公式 $a_n, b_n$ 必须以教材为主源，review 论文做交叉。

## 输出要求

- 推导笔记（`.work/<case>/derivation.md`）：完整推导，核心公式标来源页码（教材或论文）
- 代码（`.work/<case>/code/*.py`）：用 scipy.special，不自写特殊函数
- 测试（`.work/<case>/tests/test_*.py`）：和代码同步写，物理约束硬编码

## 要传达给子 agent 的约定

- **核心公式 $a_n, b_n$ 必须对着教材核**，不能只靠 review 论文
- 特殊函数用 `scipy.special`，不自己实现
- 单位 SI
- 代码和测试同步写（TDD：物理约束测试值先写死，代码迁就测试）
- 不自己宣布成功

## 本步子 agent 必须回答的决策问题

1. **需不需要数值计算脚本？还是纯解析够？**（如果 step 03 没定清，这里定）
2. **需不需要 magnus 云计算？本地跑得动吗？**（同上）
3. 代码复杂度预估？哪些用 scipy.special、哪些要自写？
4. 核心公式来源是哪本教材第几页？review 论文有没有冲突？
5. 级数截断 $n_{\max}$ 怎么定？

## 人工 gate ③ 前置

这步产出核心公式后，准备进 step 05 对抗式审查。用户在 step 04/05 末核对公式。

## 下一步

→ 05-theory_check
