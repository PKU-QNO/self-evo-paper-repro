# 图清单 — Akimov 2401.04146（case 0707-02，聚焦 Fig6）

- **caption 来源**：LaTeX 源 `Text-rev.tex`（逐字提取，本 case 独立核对）
- **图像来源**：矢量图 `01-pdf_preprocessing/src/Fig{N}-eps-converted-to.pdf`，已由 codex exec 以 3x 渲染为 `figs/Fig{N}.png`（本 case 目录下已存在，直接引用，未重新渲染）
- **坐标轴信息**：由 Read 工具人工查看 `figs/Fig6.png` 和 `figs/Fig3.png`（交叉对照）读取
- **分类口径**：`理论loci图`=从解析式直接生成的曲线（无需外部材料数据）；`数据图`=有坐标轴/可数字化的定量曲线或色图；`场分布图`=解析场的色图

---

## Fig1 — 源自由散射场分布（场分布图）
- **caption**：Contributions of source-free scattered fields of different orbital indices and polarizations to the governing fields $\vec H^{\rm TM}$ and $\vec E^{\rm TE}$ under $q_e=1$.
- **可复现性**：可，纯解析，非本 case 核心（Fig6 不依赖 Fig1）。

## Fig2 — 电流源/源自由幅度比（数据图·理论）
- **caption**：Amplitude ratios of the current-sourced and source-free scattered fields as functions of ${\rm Im}\,\varepsilon_i/\varepsilon_e$ for different orbital indices and polarizations under $q_e=1$.
- **可复现性**：可，纯解析。与 Fig6 主题相关（都涉及 $a_l^{(2)}$ 随 $\varepsilon_i/\varepsilon_e$ 变化），但非本 case 直接目标。

## Fig3 — 超辐射/非辐射态 loci（理论loci图）— 姊妹 case 0703-01 已复现
- **caption**：Super-radiating (dashed lines) and non-radiating (solid lines) states of the TM and TE polarizations for the orbital indices $l=1,2,3$.
- **内容**：6 面板 = ($l$=1,2,3) × (上排 TM，下排 TE)。每面板在 $(q_e,\varepsilon_i/\varepsilon_e)$ **实平面**画满足 $a_l=1$/$b_l=1$（超辐射，虚线）与 $a_l=0$/$b_l=0$（非辐射，实线）的等值线族。
- **坐标轴**：横 $q_e\in[0,10]$；纵 $\varepsilon_i/\varepsilon_e\in[-10,15]$（**纯实值**）。
- **与 Fig6 的关系**：Fig3 求根问题是**实**方程 ${\rm Im}\,a_l(q_e,\varepsilon)=0$（因为超辐射/非辐射态本身要求纯实 $\varepsilon$，酉性保证 $a_l\in\{0,1\}$ 当且仅当 $a_l$ 为实数）。Fig6 的超吸收条件本质不同：$a_l=1/2$ **不**要求 $\varepsilon$ 为实数（反而通常需要复数），是真正的复数方程求根，比 Fig3 多一个自由度维度。

---

## ★★★ Fig6 — 超吸收态 loci（理论loci图）— 本 case 核心目标

- **文件**：`figs/Fig6.png`（已渲染，1716×2442 px @ 3x）
- **caption**（原文，tex:L347，逐字）：Super-absorbing states of the TM and TE polarizations for the orbital indices $l=1,2,3$.

### 内容与布局
6 面板，2 行 × 3 列：
- 列 = $l=1$、$l=2$、$l=3$（从左到右）
- 每列内又分上下两个子图（每个"面板"实际是 **2 个纵向堆叠的子图**）：
  - **上方子图**：标注 "$l$=1, TM"（或 2/3, TM/TE），纵轴 **${\rm Re}\,\varepsilon_i/\varepsilon_e$**，范围约 $[-5,15]$；横轴 $q_e\in[0,10]$。曲线为蓝色实线，从上方多条渐近曲线（标注数字 1–12，随 $q_e$ 增大单调递减趋于低值）加上一条独立的、在 $q_e\in[0,3]$ 附近有一个先降后升的"U 形"曲线（标注"1"，是与其余分支不同的另一支，在 ${\rm Re}<0$ 区域出现）。
  - **下方子图**：标注同一 $(l,$偏振$)$，纵轴 **${\rm Im}\,\varepsilon_i/\varepsilon_e$**，范围随面板不同（TM: 0–3/0–4/0–4；TE: 0–1.2/0–0.8/0–0.6，随 $l$ 增大峰值降低），横轴同 $q_e\in[0,10]$。曲线为红色实线，多条曲线呈现"先升后降"的钟形/驼峰状分布，在低 $q_e$ 附近（$q_e\approx1$–4，随 $l$ 增大峰位右移）出现尖峰（标注"1"），然后多条曲线（标注"2"到高编号如"11"/"12"）收敛聚拢并缓慢下降延伸到 $q_e=10$。
- 上下两排布局：**第一行（q_e 1-3 列）为 TM**（"$l$=1,TM" / "$l$=2,TM" / "$l$=3,TM"），**第二行为 TE**（"$l$=1,TE" / "$l$=2,TE" / "$l$=3,TE"）。

### ★ 坐标轴表示方式的判断（main-agent 背景说明要求的关键回答）
- Fig6 **没有**画单一 $(q_e,\varepsilon_i/\varepsilon_e)$ 复平面投影，而是**把复值 $\varepsilon_i/\varepsilon_e$ 拆成 ${\rm Re}$ 和 ${\rm Im}$ 两个独立的实数子图**，共用横轴 $q_e$，纵向堆叠展示。即：对每个 $(l,$偏振$)$ 面板，同一条 loci 曲线（参数化为 $q_e\mapsto\varepsilon_i(q_e)/\varepsilon_e\in\mathbb C$）被拆成两条曲线分别画在上下两个子图里——上子图是该曲线的 ${\rm Re}$ 分量 vs $q_e$，下子图是 ${\rm Im}$ 分量 vs $q_e$。
- 这与 Fig3（单一子图、纵轴直接是实数 $\varepsilon_i/\varepsilon_e$）的布局本质不同：Fig3 一个面板一条曲线一张图；Fig6 一个 $(l,$偏振$)$ 对应两个子图（Re 和 Im 分离），曲线编号（1,2,…,12）在两个子图间通过数字标签配对（同一编号在 Re 和 Im 子图中代表同一条 loci 曲线的两个分量）。
- **数字标签的含义**：图上 1–12 的数字标注是**分支编号**（branch index），对应"multiple super-absorbing states"中的第几个态（按 ${\rm Re}\,\varepsilon_i/\varepsilon_e$ 从大到小或某种自然顺序编号）。TM 面板标签到 12（$l=1,2$）或到 11/12（$l=3$）；TE 面板类似。这与原文"multiple TM and TE super-absorbing states"的定性描述吻合——每个 $(l,$偏振$)$ 有约 10+ 个分支。
- **负实部分支**：TM 各面板都能看到一条独立的"1"号曲线在 ${\rm Re}\,\varepsilon_i/\varepsilon_e<0$ 区域（约 $-2$ 到 $-5$，随 $l$ 增大更负），随后转正——这应该对应原文"only one TM state with ${\rm Re~}\varepsilon_i/\varepsilon_e<0$"。**TE 面板未观察到明显的负实部分支曲线**（TE 的所有可见分支 Re 值目测均为正），与原文"只有一个 TM 态在负实部区，无 TE 态"的表述一致。

## Fig4 — Ag/Si 大球散射谱（数据图）
- 与 Fig6 非直接相关，本 case 不复现。见 case 0703-01 `figures.md`。

## Fig5 — Ag/Si 小球散射谱 + $|a_1|,|b_1|$（数据图）
- 与 Fig6 非直接相关，本 case 不复现。

## Fig7 — Ag/Si 大球吸收谱（数据图）★与 Fig6 物理关联
- **caption**：Normalized absorption cross-section with respective contributions of the TM and TE fields with $l=1,2$ for (a)–(c) a silver particle of $R=300$ nm and (d)–(f) a silicon particle of $R=200$ nm embedded in silicon dioxide. The limits in (b), (c) and (e), (f) are given by $\sigma_{{\rm abs},l}^{\rm sa}$.
- **与 Fig6 关系**：Fig7 展示真实材料（Ag/Si）吸收谱受 Fig6 理论上限 $\sigma_{{\rm abs},l}^{\rm sa}$（第六节公式）约束，可作为 Fig6 复现后的 Layer2 交叉验证参考（若后续 main-agent 决定扩展验证范围），但不是本 case 直接目标图。

## Fig8 — Ag/Si 小球吸收谱（数据图）
- 同 Fig7，与 Fig6 有物理关联但非直接目标。

## Fig9–Fig12 — 局限性修正图
- 非本 case 范围（第4节内容），不展开。

---

## Fig6 数字化需求判断

- **是否需要数字化**：需要，供后续 step08 定量对比。方法参照姊妹 case 0703-01 的 Fig3 数字化经验（颜色像素法 @ 高分辨率矢量渲染源，非手工点选），但 Fig6 曲线密集程度和分支数（每面板约 10-12 支 × 2 个子图 Re/Im）比 Fig3（每面板 2 类曲线，虚线/实线区分）更复杂，数字化脚本需要额外处理"同一编号曲线在两个子图间配对"的逻辑（这是 Fig6 特有的、Fig3 没有的复杂度）。
- **caption 原文核对状态**：Fig6 caption 极简（只有一句话，无 (a)-(f) 子面板说明，因为 6 个面板都用同一句 caption 覆盖），与 tex 源 L345-349 逐字核对一致。

## provenance
- source_artifact: arXiv 2401.04146 LaTeX 源 `Text-rev.tex`（caption tex:L347）+ `figs/Fig6.png`（Read 工具人工查看，3x 矢量渲染）+ `figs/Fig3.png`（交叉对照）
- evidence_type: caption 逐字提取 + 图像人工目视核对（非 OCR/自动数字化）
- timestamp_version: 20260709
- scope_applicability: 本 case（0707-02）Fig6 超吸收态 loci；其余 11 图仅概述不深入
- confidence_result_class: 中高（图像目视判断存在"需人工核"项，见下）/ pipeline_completed

## 需人工核（uncertainty，未做数字化前的目视局限）
- Fig6 每面板准确的分支总数（如"TM l=1 是否恰好 12 支"）仅凭目视数字标签估计，未逐支计数验证，真实数字化后可能有 ±1-2 支的计数误差。
- 纵轴（Re/Im 子图）的精确数值范围（如 TM Re 子图上限是否恰好 15）为目视估读，未做像素级坐标换算，量化对比阶段（step08）需重新用数字化脚本精确读取坐标轴刻度。
- "TE 无负实部分支"的判断基于目视未见到明显曲线，不能 100% 排除某条曲线极短暂进入负实部但因图像分辨率或曲线极窄未被目视察觉；建议 step04 数值求根后与此目视判断交叉验证。
