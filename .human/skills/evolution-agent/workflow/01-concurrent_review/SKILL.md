# 01-concurrent_review（evolution-agent 视角）

## 这步干什么

并行 spawn N 个 sub-E-agent，每个独立审查一篇已完成复现的 capsule。**执行者不审自己**（没参与某篇 capsule 的 sub-E-agent 去审它）。

## 输入

- `.work/.result/` 下的已完成复现的 capsule 列表（通常 3-5 篇）
- 每篇的 `capsule.md` 和子 agent 原始工作报告

## 输出要求

- N 份审查报告（`sub-E-agent` 写），每份包含：
  - 这篇 capsule 的成功/失败/关键发现
  - 对 skill 的改进建议（如果有）
  - 经验分类建议（GUIDING/CAUTIONARY/FACT/PROCEDURE）
- 你汇总后的审查概况

## 要传达给 sub-E-agent 的约定

- **执行者不审自己**——确保分配时排除参与了该 capsule 的原有子 agent
- 审查要**对抗式**，不是确认式。假设有遗漏，去找遗漏
- 审查重点是"这篇 capsule 暴露了什么 skill 缺陷"，不是重做复现
- 审完后写 8 字段报告到 `.work/.evolution/<timestamp>/sub-reports/`
- sub-E-agent 报告第 6 字段必须回答决策问题
- 可以 spawn 子子 agent 读 capsule 原始报告中的代码/数据

## 本步 sub-E-agent 必须回答的决策问题

1. 这篇 capsule 的成功/失败根因是什么？
2. 它暴露了哪个（些）skill 的什么问题？
3. 你建议的改进是哪种类型（GUIDING/CAUTIONARY/FACT/PROCEDURE）？
4. 有没有跨 capsule 的共性 pattern 值得注意？
5. 这篇 capsule 的复现有 self-bias 风险吗？（执行者的自我评价可靠吗？）

## 人工 gate ①

**每份审查报告给用户看。** 确认：
- 审查质量够不够深（不是表面总结）
- 分配对了吗（执行者没审自己）
- 有没有漏掉重要的跨 capsule pattern
