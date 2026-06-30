# 05-generate_report（evolution-agent 视角）

## 这步干什么

生成治理报告，对每条候选经验做六维裁决 + 三级治理定级，进最终 human gate。这是自迭代的核心裁决环节。

## 输入

- 所有 01-04 步的产出
- skill 草稿 + 验证结果

## 输出要求

- 治理报告（`.work/.evolution/<timestamp>/report.md`）：
  - 每条候选经验的分类和来源
  - 六维裁决 + 三级定级建议
  - 每条候选经验/改动必须带 5 字段：`candidate_id`（唯一 ID）、`evidence_ref`（引用 capsule/verifier 结果/数值）、`decision`（Save/Improve/Absorb/Fork/Archive/Drop）、`tier`（Tier-1/2/3）、`rollback_ref`（接受后出问题回滚到哪个版本）
  - 每个 skill 变更的最终状态
  - 风险说明

## 这步是 spawn sub-E-agent，但最后你来拍板

spawn sub-E-agent 做治理报告的初稿，你读后做最终六维裁决和三级定级。

## 六维裁决规则

每条候选经验走六个去向之一：

| 裁决 | 含义 | 条件 | Mie 例子 |
|------|------|------|---------|
| **Save** | 直接存 | 独特、具体、scope 清楚 | "银 LSPR 峰值随 n 介质线性红移 2nm/0.1RIU" |
| **Improve then Save** | 打磨再存 | 有价值需改进 | "能量守恒验证写得太宽泛，要具体数值阈值" |
| **Absorb (Merge)** | 并入已有 skill | 经验与已有 skill 兼容 | "Rayleigh 极限检查可并入物理 verifier skill" |
| **Fork** | 创建 scope 分支 | 经验与已有 skill 冲突不兼容 | "core-shell 用递归 Mie vs 均匀球用标准 Mie 的收敛判据不同" |
| **Archive** | 存负面知识库 | 有价值但不足以进 skill | "Drude 参数用 Palik 实验数据比文献值偏 10%，坑已避" |
| **Drop** | 丢弃 | 琐碎/冗余/噪声 | "Python 版本要 3.10+"（已被基础环境覆盖） |

- Save、Improve、Absorb 是高质量经验处理的主路径
- Fork 用于物理体系冲突但都正确的场景，不强行合并
- Archive 不是 Drop——带 provenance 五要素、why_not_skill 和结论摘要，供检索避坑
- Drop 不是说这经验没用，是说"不值得升级为 skill"
- **prompt 类经验限制**：凡是改 `SKILL.md`、spawn 模版、`CLAUDE.md` 的提示词/流程措辞，必须先走 Save / Improve / Fork 候选分支，经 replay 验证后才允许 Absorb；禁止直接 Absorb 进已有 prompt。prompt 优化只看自评分会优化成"更会过 judge"，必须用回放证据约束。

## 三级治理规则：case count × 决策级别

每条经验附带 tier 定级。Tier 不只看 case count 和 verifier，也看决策级别；必须同时满足 case count/verifier 条件和决策级别允许范围，才能升到对应 tier。

| Tier | case count / verifier 条件 | 决策级别允许范围 | 状态 |
|------|-------------------------|------------------|------|
| **Tier-1** | 单 case 或证据未充分闭环 | 只处理低风险：文档、摘要、备注类经验；agent 可较多自主 | → Archive 或低风险备注，不进 active skill |
| **Tier-2** | ≥2 case 或 1 case + verifier 通过 | 处理 skill/记忆更新；必须人审 | → candidate pending，经 human gate 后才可同步 |
| **Tier-3** | ≥3 case + verifier + replay 无退化 | 处理物理成功声明、workflow 结构、蓝图执行口径；必须人审 + verifier + replay | → active 候选，最终 human gate 后升级 |

tier 升级脚本化只能自动建议：先算 case count + 跑 verifier/replay，再检查决策级别是否允许。case count 够但决策级别不允许时，不能升 tier；决策级别高但证据不足时，也不能升 tier。

**Mie 贯穿例子：**
- "银纳米球 LSPR 用 Drude 模型够用" → Tier-2（1 case + 有 verifier，属于 skill/记忆更新），pending，必须人审
- "Fig3 要在 600-800nm 扫描" → 纯 FACT，Tier-1（低风险文档/备注类经验），Archive
- "Mie 系数的分母用对数导数更稳" → Tier-3（3 case + verifier + replay pass，影响核心方法口径），active 候选，必须 human gate
- "某次结果可宣称物理复现成功" → 即使 case count 够，也只能走 Tier-3，必须人审 + verifier + replay

## 要传达给 sub-E-agent 的约定

- 每条候选经验写清楚十一项：来源 / 类型 / 六维建议 / 三级 tier / 理由 / scope 边界 / `candidate_id` / `evidence_ref` / `decision` / `tier` / `rollback_ref`
- 如果有冲突经验，列出冲突清单（说明冲突双方和裁决思路）
- 六维建议要有数据支撑（来自 replay 验证和 capsule 证据）
- tier 定级基于 case count × 决策级别：case count/verifier 达标且决策级别允许，才可升 tier
- 如果建议 Absorb，写清楚合并到哪个 skill、怎么合
- 如果建议 Improve，写清楚改进点列表
- 如果建议 Fork，写清楚冲突边界和分支方案
- 如果建议 Archive，必须补全 provenance 五要素（source_artifact/evidence_type/timestamp_version/scope_applicability/confidence_result_class）和 why_not_skill
- 如果建议 Drop，写清楚为什么不够格
- prompt 类经验（改 `SKILL.md` / spawn 模版 / `CLAUDE.md` 提示词）必须标出是否已 replay；未 replay 只能 Save/Improve/Fork，不能 Absorb

## 本步 sub-E-agent 必须回答的决策问题

1. 每条候选经验的六维裁决建议是什么？数据支撑在哪里？tier 几级？
2. 哪些经验可以进 active（Tier-3）了？哪些还要沉淀？
3. 有没有冲突经验需要 Fork 分支？冲突边界是否清楚？
4. 如果有 Archive，五个字段是否完整？
5. 如果用户否决了所有修改，有没有 fallback 方案？
6. 本次自迭代的整体质量如何？值得这次投入吗？

## 人工 gate ⑤

**最终的 human gate。** 用户审每一条经验的六维裁决 + tier 定级：
- 逐条确认 Save/Improve/Absorb/Fork/Archive/Drop
- 逐条确认 Tier-1/2/3 定级
- 用户可能推翻建议，按用户决定执行
- 通过的 candidate→active（用 yaml_to_skill.py 同步到 `.claude/skills/`）
- 未通过的留沙箱 `.work/.evolution/<timestamp>/drafts/`（不删）
- 用户可能要求部分通过、部分回滚

## 局部 spawn 模版（供 evolution-agent 拼接用）

```
【第 05 步：generate_report】
【任务】生成治理报告，对每条候选经验做六维裁决 + 三级治理定级，进最终 human gate。这是自迭代的核心裁决环节。
【输入】所有 01-04 步的产出；skill 草稿 + 验证结果
【输出】治理报告（`.work/.evolution/<timestamp>/report.md`）：每条候选经验的分类和来源；六维裁决+三级定级建议；每条候选经验/改动必须带 candidate_id/evidence_ref/decision/tier/rollback_ref 五字段；每个 skill 变更的最终状态；风险说明
【要传达的约定】每条候选经验写清楚十一项：来源/类型/六维建议/三级 tier/理由/scope 边界/candidate_id/evidence_ref/decision/tier/rollback_ref；如果有冲突经验列出冲突清单和裁决思路；六维建议要有数据支撑（来自 replay 验证和 capsule 证据）；tier 定级基于 case count × 决策级别，case count/verifier 达标且决策级别允许才可升 tier；prompt 类经验（改 SKILL.md/spawn 模版/CLAUDE.md 提示词）必须先走 Save/Improve/Fork 候选分支，经 replay 验证后才允许 Absorb，禁止直接 Absorb 进已有 prompt；六维裁决六去向——Save（直接存）/Improve then Save（打磨再存）/Absorb Merge（并入已有 skill）/Fork（scope 分支）/Archive（存负面知识库，必须含 provenance 五要素 source_artifact/evidence_type/timestamp_version/scope_applicability/confidence_result_class 和 why_not_skill）/Drop（丢弃须说明理由）；三级治理——Tier-1（低风险文档/摘要/备注类经验，agent 可较多自主）/Tier-2（skill/记忆更新，必须人审）/Tier-3（物理成功声明、workflow结构、蓝图执行口径，必须人审+verifier+replay）
【必须回答的决策问题】1. 每条候选经验的六维裁决建议是什么？数据支撑在哪里？tier 几级？2. 哪些经验可以进 active（Tier-3）了？哪些还要沉淀？3. 有没有冲突经验需要 Fork 分支？冲突边界是否清楚？4. 如果有 Archive，五个字段是否完整？5. 如果用户否决了所有修改，有没有 fallback 方案？6. 本次自迭代的整体质量如何？值得这次投入吗？
【人工 gate】⑤ 最终的 human gate。用户逐条审六维裁决+tier 定级；通过的 candidate→active（用 yaml_to_skill.py 同步到 `.claude/skills/`）；未通过的留沙箱（`.work/.evolution/<timestamp>/drafts/`）不删；用户可能要求部分通过/部分回滚。
【并发说明】spawn 一个 sub-E-agent 做治理报告初稿，evolution-agent 读后做最终六维裁决和三级定级。不并发。
【预制脚本】无（尚未建立）
```
