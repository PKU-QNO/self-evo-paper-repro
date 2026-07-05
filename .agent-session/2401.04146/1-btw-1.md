# Session: self-evo-paper-repro

- **Date**: 2026-07-04 ~ 09:17:07
- **Messages**: 2 user / 2 assistant

---

**User** 09:16:44

到现在为止你遇到了哪些之前没发现的问题

---

**Assistant** 09:16:44 (<synthetic>)

到现在为止，首次实跑暴露的**之前设计阶段没发现的问题**（都是真跑才冒出来的）：

## 框架级缺口

1. **memento 记忆 MCP 根本没接入**。CLAUDE.md 把"每个 agent 开始前搜记忆、结束前存记忆"当强制红线，但本 session 里 `ToolSearch` 和 `memory_search`/`memory_store` 工具**不存在**。这不是"忘了搜"，是整套记忆纪律的底座缺失。现在靠文件系统 `.work/memento-cache/` 兜底，但那没有去重、检索、provenance 校验，等于强制规范空转。这是最该你侧决策的一条。

2. **框架内部路径约定自相矛盾**。同一个 workflow SKILL 里，"输出要求"写 `.work/<case>/paper_text.md`，"执行版-输出路径"又写 `.work/.todo/{paper}/{case}/{timestamp}/01-.../`。两套不一致，我 spawn 时得手动指定一套消歧义，否则子 agent 会两处乱放。

## 计划/知识与论文实际不符

3. **计划预期的目标图在论文里不存在**。FINAL 计划和执行手册都假设 Akimov 有经典 $Q_{ext}(x)$ 过渡曲线，逐图核对后发现**没有**。整个阶段1的"复现哪张图"是空的，得临时重定。

4. **skill 里的论文描述是错的**。`optics-mie-reproduction/references/papers.md` 白纸黑字写着本文有 "$Q_{sca}(x)$ curve, Rayleigh→Mie→geometric transition"，与论文实际内容冲突。如果 sub-agent 盲信 skill 去搭模型就会跑偏——这正好命中你们设计时担心的"记忆/知识污染"风险，只是这次污染源是 skill 参考文件本身。

## 执行层行为偏差

5. **sub-agent 会漏交规范硬要求的产物**。第一个 sub-agent 把高质量核心产物（公式、图）都做了，却**没写 8 字段工作报告，也没写 tables.md**，只在最后口头说"论文无表格"。报告是编排层拍板和审计的唯一依据，漏了就等于断链。退回补了，但说明 spawn 指令里"报告是硬交付"的约束力不够。

## 一个中性观察（不算问题，但和手册预期相反）

6. **verifier 脚本其实已经存在**。执行手册诚实标注"`check_*.py` 被引用为已存在，实际可能没落地"，但真去看，3 个脚本都在，还定义好了接口契约 `compute_cross_sections/compute_Q_sca/compute_Q_ext(m,x)`——这是好消息，比预期乐观，反而给了 step04 一个明确的实现靶子。

**共性**：1、3、4 都是"文档/配置写着有，真跑发现没有或是错的"，属于设计期没有真数据校验时留下的乐观假设；2、5 是规范内部不自洽和执行层遵从度不足。这些正是"人工预训练第一份真数据"要交给 optics_agent 侧的核心反馈。

*Tokens: in: 0 / out: 0*

---

**User** 09:16:44

<fork-boilerplate>
You are a worker fork. The transcript above is the parent's history — inherited reference, not your situation. You are NOT a continuation of that agent. Execute ONE directive, then stop.

Hard rules:
- Do NOT spawn subagents with the Agent tool. The "default to forking" guidance is for the parent; you ARE the fork, execute directly.
- One shot: report once and stop. No follow-up questions, no proposed next steps, no waiting for the user.

Guidelines (your directive may override any of these):
- Stay in scope. Other forks may be handling adjacent work; if you spot something outside your directive, note it in a sentence and move on.
- Open with one line restating your task, so the parent can spot scope drift at a glance.
- Be concise — as short as the answer allows, no shorter. Plain text, no preamble, no meta-commentary.
- If you committed changes, list the paths and commit hashes in your report.
</fork-boilerplate>

Your directive: 到现在为止你遇到了哪些之前没发现的问题

---

**Assistant** 09:17:07 (claude-opus-4-8)

任务：汇总首次实跑到目前为止暴露的、设计阶段未发现的问题。

**框架级缺口**
1. **memento 记忆 MCP 未接入**。CLAUDE.md 把"每个 agent 开始前搜、结束前存记忆"定为强制红线，但本 session `ToolSearch`、`memory_search`、`memory_store` 工具都不存在。整套记忆纪律的底座缺失，只能用文件系统 `.work/memento-cache/` 兜底（无去重/检索/provenance 校验），强制规范空转。
2. **框架内部路径约定自相矛盾**。同一 workflow SKILL 里"输出要求"写 `.work/<case>/paper_text.md`，"执行版-输出路径"写 `.work/.todo/{paper}/{case}/{timestamp}/01-.../`，两套不一致，需手动指定一套消歧义。

**计划/知识与论文实际不符**
3. **计划预期的目标图在论文里不存在**。FINAL 计划与执行手册假设 Akimov 有经典 $Q_{ext}(x)$ 过渡曲线，逐图核对后发现没有，阶段1"复现哪张图"落空、需临时重定。
4. **skill 参考文件的论文描述是错的**。`optics-mie-reproduction/references/papers.md` 写着本文有 "$Q_{sca}(x)$ curve, Rayleigh→Mie→geometric transition"，与论文实际冲突。盲信会跑偏——命中设计期担心的"知识污染"风险，且污染源是 skill 自身。

**执行层行为偏差**
5. **sub-agent 漏交规范硬要求的产物**。首个 sub-agent 核心产物（公式、图）质量高，却没写 8 字段工作报告、也没写 tables.md，只口头说"无表格"。报告是编排层拍板/审计的唯一依据，漏了即断链，已退回补齐（计1次 retry）。

**中性观察（与手册预期相反，非问题）**
6. **verifier 脚本其实已存在**。手册诚实标注"`check_*.py` 可能未落地"，实际 3 个脚本都在且定义好接口契约 `compute_cross_sections/compute_Q_sca/compute_Q_ext(m,x)`——比预期乐观，给了 step04 明确实现靶子。

共性：1、3、4 是"文档/配置写着有，真跑发现没有或是错的"（设计期乐观假设）；2、5 是规范内部不自洽与执行层遵从度不足。

*Tokens: in: 2 / out: 889*

---
