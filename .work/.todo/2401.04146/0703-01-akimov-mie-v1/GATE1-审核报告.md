# Gate1 审核报告 — SEPR 首次实跑（Akimov 2401.04146）

> 写给用户审核。main-agent 于 Gate1（参数核对）停机等待，本报告汇总：已完成工作、待你决定的事项、待修复的问题、后续路线。
> case：`0703-01-akimov-mie-v1` ｜ timestamp：20260703-2236 ｜ 撰写：main-agent（step02 末 Gate1 停机点）

---

## 一、当前进度一览

| 步 | 状态 | result_class | 产物 |
|---|---|---|---|
| 开工前确认 | ✅ | — | verifier 脚本已存在；纯 Python 确认；论文+LaTeX 源+教材就位 |
| Step01 PDF 预处理 | ✅（1次退回补报告） | `pipeline_completed` | paper_text / formulas / figures / tables + 12 图 PNG |
| Step02 论文阅读+抽参 | ✅（一次通过） | `pipeline_completed` | paper_understanding / parameter_table / missing_info |
| **Gate1 参数核对** | 🛑 **停机等你** | — | 本报告 |
| Step03–11 | 未开始 | `not_run` | — |

资源消耗（case 级上限对照）：spawn 2/20；外部搜索 0/30；wall-clock 约 0.5h/4h。全部健康。

---

## 二、需要你【决定】的事项（按优先级）

### 决定 1：step08 目标图选哪张 ⭐ 最高优先级，阻塞主线

**背景**：FINAL 计划假设阶段1复现经典 $Q_{ext}(x)$ 过渡曲线，但逐图核对确认 **Akimov 论文没有这张图**。论文实际讲的是源自由/电流源散射场分解与超辐射/非辐射/超吸收态。候选：

| 候选 | 图 | 画什么 | 需材料色散？ | 难度 | main-agent 评估 |
|---|---|---|---|---|---|
| **A ⭐推荐** | Fig3 | 超辐射($a_l{=}1$)/非辐射($a_l{=}0$) loci，$(q_e,\varepsilon_i/\varepsilon_e)$ 实平面，$l=1,2,3$，TM/TE | **否** | 低 | 零外部依赖，最干净测框架本身；可用论文自带硬约束自验 |
| C | Fig5(c,f) | $\lvert a_1\rvert,\lvert b_1\rvert$ vs $\hbar\omega$ | 是（Ag/Si/SiO₂） | 中 | 最直接验证 Mie 系数实现，但引入"色散源与作者是否一致"的不确定性 |
| B | Fig4 | Ag/Si 球散射谱 | 是 | 中 | 多极叠加+峰位归因更复杂 |
| D | Fig6 | 超吸收 loci（复平面） | 否 | 中（复根） | 纯理论但需复根求解器 |
| E | 经典 $Q_{ext}(x)$ 曲线 | 改对教材 BH 图做基准 | 否 | 低 | 保留原计划教学意图，但偏离"复现 Akimov 这篇" |

无论选哪个，标准 Lorenz-Mie 核（$a_l,b_l$+截面）+ 3 个 Layer1 verifier + benchmark 基础设施都会先建——阶段1核心目标不受影响，区别只在 step08 对比哪张图。

**推荐 A**。理由：首次实跑的首要目的是测试框架，A 零外部数据依赖、不引入材料色散源不确定性、解析求根难度最低、且能用 $a_l{=}1\Rightarrow\sigma_{sca,l}=\sigma^{sr}$ 做论文内自洽验证。

### 决定 2：Gate1 参数核对（请核对以下参数表）

**通用核参数**（详表：`.work/.todo/2401.04146/0703-01-akimov-mie-v1/parameter_table.md`）：

| 量 | 值/定义 | 单位 | 来源 |
|---|---|---|---|
| 尺寸参数 | $q_e=k_eR$（等价常见 $x$）；$q_i=mq_e$ | 无量纲 | 论文 §2 |
| 相对折射率 | $m=\sqrt{\varepsilon_i/\varepsilon_e}$ | 无量纲 | BH 记号（论文用 $\varepsilon_i/\varepsilon_e$） |
| 多极截断 | 论文只用 $l=1,2,3$；数值截断取 Wiscombe $n_{max}\approx x+4x^{1/3}+2$（**非论文原文，标 trust**） | — | 教材/scipy 惯例 |
| Riccati-Bessel | $\psi_l(q)=qj_l(q)$，$\xi_l(q)=qh_l^{(1)}(q)$；导数用 scipy 或 BH 递推 | — | 论文 §2 + BH |
| 单位换算 | $\lambda_0[\mathrm{nm}]=1239.84/E[\mathrm{eV}]$；$q_e=2\pi n_e R/\lambda_0$ | — | 常数核对过（例：Ag R=25nm@3eV,$n_e{=}1.46$→$q_e\approx0.55$，与 Fig5 小球偶极主导一致） |

**候选 A 参数**：$q_e\in[0,10]$、$\varepsilon_i/\varepsilon_e\in[-10,15]$ 纯实、$l=1,2,3$、TM+TE。
**候选 B/C 参数**（若选）：Ag R=25/300nm、Si R=40/200nm @SiO₂、$\hbar\omega\in[0,6]$ eV；材料源 pending：Ag=Johnson&Christy 1972 / Si=Aspnes 1983 / SiO₂=Malitson 1965（未下载，等你选定再搜）。

**请核**：范围/量级/单位有无错；候选 B/C 的推荐材料源是否认可。

### 决定 3：公式主源口径

论文的 $a_l,b_l$ 写法带显式 $q_i,q_e$ 因子，与教材 Bohren&Huffman **形式不同但等价**。拟定口径：**step04 以教材 BH 标准式为主源实现，用 Akimov 式做交叉验证**（两式数值必须一致，不一致即 blocker）。这也是 Gate3 你对教材核公式时的核对对象。请确认或否决。

### 决定 4：~~memento 是否先修~~ ✅ 已解除

你重连后 memento MCP **已恢复**（memory_search/memory_store 实测成功）。我已把 step01/02 关键事实回灌记忆库（ID: e786ffac）。后续 spawn 的 sub-agent 将恢复正常记忆纪律；前半段的文件系统兜底记录（`.work/memento-cache/2401.04146-02-paper_reading.md`）保留作审计痕迹。

---

## 三、需要【修复】的问题（按谁修分类）

### 建议本轮跑完由 evolution / optics_agent 侧修（不阻塞主线，我会记入 toEflow/）

| # | 问题 | 证据 | 修复建议 |
|---|---|---|---|
| F1 | **skill 知识污染**：`optics-mie-reproduction/references/papers.md` Stage1 写着本文有 "$Q_{sca}(x)$ curve / Rayleigh→Mie→geometric transition"，实际没有 | step01 逐图核对 figures.md | evolution 修正 papers.md；这是设计期担心的"知识污染"首个实锤，且污染源是 skill 自身 |
| F2 | **workflow SKILL 路径约定不一致**：同一文件里"输出要求"写 `.work/<case>/...`，"执行版"写 `.work/.todo/{paper}/{case}/{timestamp}/...` | main-agent workflow/01、02 SKILL.md | 统一为一套（本次实跑用了 `.work/.todo/{paper}/{case}/` 并在 spawn 指令显式消歧义） |
| F3 | **spawn 模版对"报告是硬交付"强调不足**：step01 sub-agent 产物质量高但漏写 8 字段报告+tables.md，退回一次才补 | `.work/.sub-report/` 曾为空 | spawn 模版把"先写报告再结束"列为结束条件而非输出项之一；或 main-agent 校验清单加"报告文件存在性"前置检查 |
| F4 | **memento MCP 会话级断联**：本 session 前半段 ToolSearch/memory_* 全部不可用，强制记忆纪律空转（现已恢复，但暴露了"红线静默失效"风险） | step01/02 报告 memory_search_summary | 按 CLAUDE.md 预检条款已"大声降级"；根治靠 SessionStart hook 探活（已列 hooks 家族，Mie 跑通后硬化） |

### 不用修（澄清）

- verifier 脚本：手册标注"可能未落地"，实际已存在且接口契约明确——是好消息，step04 按 `compute_cross_sections/compute_Q_sca/compute_Q_ext(m,x)` 实现即可。
- `Li_J_OE2010.pdf` 坏文件：阶段6才用，已有替代 `oe-18-17-17684.pdf`，现在不用处理。
- 阶段3缺 PDF：阶段3才阻塞，现在不用处理。

---

## 四、你决策后的路线（预告）

1. **Step03 复现设计**：按你选的目标图写 formalization spec（geometry/materials/equations/BC + 复现目标量化定义）→ **Gate2 spec 核对（停）**
2. **Step04 理论+实现**：BH 主源推导 $a_n,b_n$ → `code/mie_coefficients.py` + `scattering.py`（遵守 verifier 接口契约）+ tests/
3. **Step05 对抗审查**：分子分母/阶数/符号/BC 双向归因 → **Gate3 你对教材核公式（最关键 10 分钟，停）**
4. **Step06 本地跑** → **Step07 跑 3 个 Layer1 verifier + Layer2 极限**（fail 即停问你）
5. **Step08 数字化目标图+量化对比**（RMSE/峰位误差）→ **Gate4 误差核对（停）**
6. **Step09 自检 → Step10 双报告+benchmark+skill草稿→toEflow/ → Step11 run_manifest + 问你哪些进 .result/**

---

## 五、审计线索（供 optics_agent 侧）

- 子报告：`.work/.sub-report/`（step01/02 各一份，8字段+固定头6字段齐全）
- 过程产物：`.work/.todo/2401.04146/0703-01-akimov-mie-v1/`
- 记忆：memento ID e786ffac（恢复后回灌）+ `.work/memento-cache/`（断联期兜底）
- spawn 统计：2 个 sub-agent（step01、step02 各1），depth=2（main→sub），无 fan-out，无 leaf spawn；step01 计 1 次 retry（补报告，非重跑提取）
