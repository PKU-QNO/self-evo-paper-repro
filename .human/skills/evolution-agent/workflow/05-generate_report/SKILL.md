# 05-generate_report（evolution-agent 视角）

## 这步干什么

生成治理报告，对每条候选经验做四选一裁决，进最终 human gate。这是自迭代的核心裁决环节。

## 输入

- 所有 01-04 步的产出
- skill 草稿 + 验证结果

## 输出要求

- 治理报告（`.work/.evolution/<timestamp>/report.md`）：
  - 每条候选经验的分类和来源
  - 四选一裁决建议
  - 每个 skill 变更的最终状态
  - 风险说明

## 这步是 spawn sub-E-agent，但最后你来拍板

spawn sub-E-agent 做治理报告的初稿，你读后做最终裁决。

## 四选一裁决规则

每条候选经验（clusters.md 里提取的）走四个去向之一：

| 裁决 | 含义 | 条件 | 后续操作 |
|------|------|------|---------|
| **Save** | 直接存 | 独特、具体、scope 清楚 | candidate→active，更新 skill |
| **Improve** | 打磨再存 | 有价值但不完整 | 列出改进点，修订后再审 |
| **Absorb** | 并入已有 | 重复/可合并 | 展示 diff，合并建议 |
| **Drop** | 丢弃 | 琐碎/冗余/太抽象 | 说明为什么扔，留沙箱 |

- Absorb 和 Improve 是高质量经验处理的主路径
- Save 只用于确实独特且完整的经验
- Drop 不是"没用"，是"不值得升级为 skill"——可能记到 memento 就够

## 要传达给 sub-E-agent 的约定

- 每条候选经验写清楚四项：来源 / 类型 / 四选一建议 / 理由
- 四选一建议要有数据支撑（来自 replay 验证和 capsule 证据）
- 如果建议 Absorb，写清楚合并到哪个 skill、怎么合
- 如果建议 Improve，写清楚改进点列表
- 如果建议 Drop，写清楚为什么不够格

## 本步 sub-E-agent 必须回答的决策问题

1. 每条候选经验的四选一建议是什么？数据支撑在哪里？
2. 哪些经验可以进 active 了？哪些还要沉淀？
3. 如果用户否决了所有修改，有没有 fallback 方案？
4. 本次自迭代的整体质量如何？值得这次投入吗？

## 人工 gate ⑤

**最终的 human gate。** 用户审每一条经验的四选一裁决：
- 逐条确认 Save/Improve/Absorb/Drop
- 用户可能推翻建议，按用户决定执行
- 通过的 candidate→active（用 yaml_to_skill.py 同步到 `.claude/skills/`）
- 未通过的留沙箱 `.work/.evolution/<timestamp>/drafts/`（不删）
- 用户可能要求部分通过、部分回滚
