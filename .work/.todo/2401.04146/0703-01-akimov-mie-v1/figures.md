# 图清单 — Akimov 2401.04146

- **caption 来源**：LaTeX 源 `Text-rev.tex`（逐字提取）
- **图像来源**：LaTeX 源附带的矢量图 `Fig{N}-eps-converted-to.pdf`，用 pymupdf 以 3x 渲染为 `figs/Fig{N}.png`（比 PDF 截屏清晰）
- **坐标轴信息**：由渲染图人工读取（Read 工具查看），非 OCR
- **分类口径**：`数据图`=有坐标轴/可数字化的定量曲线或色图；`理论loci图`=从解析式直接生成的曲线（无需外部材料数据）；`场分布图`=解析场的色图。本文**无纯示意图**（无结构/流程示意）。
- 共 **12 张图，全部为数据/理论/场分布图**，均由作者用理论式或含材料色散计算生成。

> **归一化说明**：Fig4/5/7/8 纵轴 $\sigma_{\rm sca}/(\pi R^2)$ 或 $\sigma_{\rm abs}/(\pi R^2)$ 即散射/吸收效率 $Q$。虚线 "limit" = $\sigma_{{\rm sca},l}^{\rm sr}/(\pi R^2)=2(2l+1)/q_e^2$（纯解析）。

---

## Fig1 — 源自由散射场分布（场分布图）
- **文件**：`figs/Fig1.png`
- **caption**（原文）：Contributions of source-free scattered fields of different orbital indices and polarizations to the governing fields $\vec H^{\rm TM}$ and $\vec E^{\rm TE}$ under $q_e=1$. The contributions are normalized by the amplitudes of the plane incident fields $E_0$ and $H_0=\sqrt{\varepsilon_0\varepsilon_e/\mu_0}E_0$.
- **内容**：6 面板 = ($l$=1,2,3) × (上排 TM: $|H_l^{\rm TM}/H_0|$，下排 TE: $|E_l^{\rm TE}/E_0|$) 的二维色图。
- **坐标轴**：横 $k_e x$ ∈ [−4,4]，纵 $k_e z$ ∈ [−4,4]；中心白色圆盘=球（$q_e=1$）。色标峰值随 $l$ 增大：TM 约 0.5 / 2.0 / 12.5；TE 约 0.5 / 2.0 / 12.5。
- **条件**：$q_e=1$，源自由场（与材料无关）。
- **可复现性**：可，纯解析（$h_l^{(1)}$ 场分布），无需材料数据。非阶段1核心。

## Fig2 — 电流源/源自由幅度比（数据图·理论）
- **文件**：`figs/Fig2.png`
- **caption**：Amplitude ratios of the current-sourced and source-free scattered fields as functions of ${\rm Im}\,\varepsilon_i/\varepsilon_e$ for different orbital indices and polarizations under $q_e=1$. The labels show the values of ${\rm Re}\,\varepsilon_i/\varepsilon_e=-5$, 1 and 5 kept fixed for the respective curves.
- **坐标轴**：横 ${\rm Im}\,\varepsilon_i/\varepsilon_e$；纵 幅度比 $|a_l^{(2)}/a_l^{(1)}|$ 等。曲线按 ${\rm Re}\,\varepsilon_i/\varepsilon_e\in\{-5,1,5\}$ 分组，$l$/偏振区分。
- **条件**：$q_e=1$。
- **可复现性**：可，纯解析（$a_l^{(1)},a_l^{(2)}$ 之比）。

## ★ Fig3 — 超辐射/非辐射态 loci（理论loci图）— **step08 首选候选 A**
- **文件**：`figs/Fig3.png`
- **caption**：Super-radiating (dashed lines) and non-radiating (solid lines) states of the TM and TE polarizations for the orbital indices $l=1,2,3$.
- **内容**：6 面板 = ($l$=1,2,3) × (上排 TM，下排 TE)。每面板在 $(q_e,\varepsilon_i/\varepsilon_e)$ 平面画出满足 $a_l=1$/$b_l=1$（超辐射，红虚线）与 $a_l=0$/$b_l=0$（非辐射，蓝实线）的等值线族。
- **坐标轴**：横 $q_e$ ∈ [0,10]；纵 $\varepsilon_i/\varepsilon_e$ ∈ [−10,15]（实值）。
- **条件**：纯实 $\varepsilon_i/\varepsilon_e$，**无需任何材料色散数据**。
- **可复现性**：★强。直接解析求根 $a_l(q_e,\varepsilon_i/\varepsilon_e)=1$ 或 $0$。最适合作 step08 定量对比（loci 位置可数字化对比）。

## ★ Fig4 — Ag/Si 大球散射谱（数据图）— **step08 候选 B（需材料数据）**
- **文件**：`figs/Fig4.png`
- **caption**：Normalized scattering cross-section with respective contributions of the TM and TE fields with $l=1,2$ for (a)–(c) a silver particle of $R=300$ nm and (d)–(f) a silicon particle of $R=200$ nm embedded in silicon dioxide. The limits in (b),(c) and (e),(f) are given by $\sigma_{{\rm sca},l}^{\rm sr}$.
- **内容/坐标轴**：6 面板。
  - (a) Ag R=300nm@SiO2：$\sigma_{\rm sca}/(\pi R^2)$（纵 线性 0–4）vs $\hbar\omega$（横 0–6 eV）。总散射。
  - (b) $l=1$ 贡献：TM(红)/TE(蓝) + "$l=1$ limit"(黑虚)；纵对数 $10^{-4}$–$10^{1}$。
  - (c) $l=2$ 贡献：同上，"$l=2$ limit"。
  - (d) Si R=200nm@SiO2：$\sigma_{\rm sca}/(\pi R^2)$（纵 0–8）vs $\hbar\omega$（0–6 eV）。
  - (e) Si $l=1$；(f) Si $l=2$，纵对数 $10^{-4}$–$10^{2}$。
- **条件**：外介质 SiO2（$\varepsilon_e$），球为 Ag / Si，谱 vs 光子能量。
- **可复现性**：中。公式全给，但**需 Ag、Si、SiO2 的 $\varepsilon(\omega)$ 色散数据（论文未提供数值）**，须用外部光学常数库（如 Ag: Johnson&Christy；Si: Green/Aspnes；SiO2: Malitson）。是否与作者所用色散源一致会影响吻合度 → missing_evidence。

## ★ Fig5 — Ag/Si 小球散射谱 + $|a_1|,|b_1|$（数据图）— **step08 候选 C（需材料数据，含 Mie 系数曲线）**
- **文件**：`figs/Fig5.png`
- **caption**：Normalized scattering cross-section with respective contributions of the TM and TE fields with $l=1,2$ for (a)–(c) a silver particle of $R=25$ nm and (d)–(f) a silicon particle of $R=40$ nm embedded in silicon dioxide. The limits in (b) and (e) are given by $\sigma_{{\rm sca},l}^{\rm sr}$.
- **内容/坐标轴**：6 面板。
  - (a) Ag R=25nm：$\sigma_{\rm sca}/(\pi R^2)$（纵 0–5）vs $\hbar\omega$（0–6 eV）；total(黑实)+$l=1$(红虚)。LSPR 峰在 $\hbar\omega\approx3$ eV，$\approx3.9$ eV 处深谷（$\varepsilon_i=\varepsilon_e$ 非辐射态）。
  - (b) $l=1$ TM/TE + limit，纵对数 $10^{-6}$–$10^{4}$。
  - **(c) $|a_1|$(红)、$|b_1|$(蓝) vs $\hbar\omega$，纵线性 0–1**。← Mie 系数模直接对比，最干净。
  - (d) Si R=40nm：$\sigma_{\rm sca}/(\pi R^2)$（纵 0–4）；total+$l=1$。
  - (e) Si $l=1$ TM/TE+limit；**(f) $|a_1|,|b_1|$ vs $\hbar\omega$（纵 0–1）**。
- **条件**：Ag R=25nm / Si R=40nm @SiO2。
- **可复现性**：中（同 Fig4，需材料数据）。**优点**：(c)(f) 直接给 $|a_1|,|b_1|$ 曲线，是验证 Mie 系数实现正确性的理想量化目标（只要材料 $\varepsilon(\omega)$ 定了）。

## ★ Fig6 — 超吸收态 loci（理论loci图）— **step08 候选 D（纯理论）**
- **文件**：`figs/Fig6.png`
- **caption**：Super-absorbing states of the TM and TE polarizations for the orbital indices $l=1,2,3$.
- **内容**：6 面板 ($l$=1,2,3)×(TM,TE)，在 $(q_e,\varepsilon_i/\varepsilon_e)$ 复平面优化下满足 $a_l=1/2$（或 $b_l=1/2$）的态。
- **坐标轴**：横 $q_e$；纵 $\varepsilon_i/\varepsilon_e$（需复值优化）。
- **可复现性**：中偏强，纯理论但需在复 $\varepsilon_i/\varepsilon_e$ 平面求 $a_l=1/2$，比 Fig3 稍复杂（复根/优化）。无需材料数据。

## Fig7 — Ag/Si 大球吸收谱（数据图）
- **文件**：`figs/Fig7.png`
- **caption**：Normalized absorption cross-section with respective contributions of the TM and TE fields with $l=1,2$ for (a)–(c) a silver particle of $R=300$ nm and (d)–(f) a silicon particle of $R=200$ nm embedded in silicon dioxide. The limits in (b),(c) and (e),(f) are given by $\sigma_{{\rm abs},l}^{\rm sa}$.
- **坐标轴**：$\sigma_{\rm abs}/(\pi R^2)$ vs $\hbar\omega$（0–6 eV）；(b,c,e,f) 含吸收上限 $\sigma_{{\rm abs},l}^{\rm sa}$。
- **可复现性**：中，需材料数据（同 Fig4）。

## Fig8 — Ag/Si 小球吸收谱（数据图）
- **文件**：`figs/Fig8.png`
- **caption**：Normalized absorption cross-section with respective contributions of the TM and TE fields with $l=1,2$ for (a)–(c) a silver particle of $R=25$ nm and (d)–(f) a silicon particle of $R=40$ nm embedded in silicon dioxide. The limits in (b) and (e) are given by $\sigma_{{\rm abs},l}^{\rm sa}$.
- **坐标轴**：$\sigma_{\rm abs}/(\pi R^2)$ vs $\hbar\omega$。
- **可复现性**：中，需材料数据。

## Fig9 — 激发源修正 $\eta_{\rm sca}$（数据图·理论，需额外参数）
- **文件**：`figs/Fig9.png`
- **caption**：Ratios $\eta_{\rm sca}$ of the modified scattering cross-section contributions given by Eq.(S_sca_source) to the classical ones for the TM and TE scattered fields with $l=1,2,3$ under $q_e=1$ and $\varepsilon_i/\varepsilon_e=5+{\rm i}\,0.1$.
- **条件**：$q_e=1$，$\varepsilon_i/\varepsilon_e=5+0.1{\rm i}$，含相互作用系数 $\alpha_l$。
- **可复现性**：低-中，需外部激发建模参数 $\alpha_l$（论文未给具体扫描范围数值）。非阶段1。

## Fig10 — 激发源修正 $\eta_{\rm abs}$（数据图·理论）
- **文件**：`figs/Fig10.png`
- **caption**：Ratios $\eta_{\rm abs}$ of the modified absorption cross-section contributions given by Eq.(S_abs_source) to the classical ones for the TM and TE scattered fields with $l=1,2,3$ under $q_e=1$ and $\varepsilon_i/\varepsilon_e=5+{\rm i}\,0.1$.
- **可复现性**：低-中（同 Fig9）。非阶段1。

## Fig11 — 过渡层修正 $\eta_{\rm sca}$（数据图·理论）
- **文件**：`figs/Fig11.png`
- **caption**：Ratios $\eta_{\rm sca}$ of the modified scattering cross-section contributions given by scattering coefficients (a_l_tra) and (b_l_tra) to the classical ones for the TM and TE scattered fields with $l=1,2,3$ under $k_0(R_i+R_e)/2=1$, $\varepsilon_e=2.25$, ${\rm Im}\,\varepsilon_i=0.1$ for linear profiles of $\varepsilon(r)$.
- **条件**：$k_0(R_i+R_e)/2=1$，$\varepsilon_e=2.25$，${\rm Im}\,\varepsilon_i=0.1$，线性 $\varepsilon(r)$。
- **可复现性**：低-中，需过渡层 ODE 积分 + 厚度 $\Delta R$ 扫描。非阶段1。

## Fig12 — 过渡层修正 $\eta_{\rm abs}$（数据图·理论）
- **文件**：`figs/Fig12.png`
- **caption**：Ratios $\eta_{\rm abs}$ of the modified absorption cross-section contributions given by scattering coefficients Eqs.(a_l_tra) and (b_l_tra) to the classical ones for the TM and TE scattered fields with $l=1,2,3$ under $k_0(R_i+R_e)/2=1$, $\varepsilon_e=2.25$, ${\rm Im}\,\varepsilon_i=0.1$ for linear profiles of $\varepsilon(r)$.
- **可复现性**：低-中（同 Fig11）。非阶段1。

---

## step08 目标图汇总建议（给 main-agent 拍板）

| 候选 | 图 | 画的量 | 自变量 | 条件 | 需外部材料数据？ | 复现难度 |
|------|----|-------|--------|------|----------------|---------|
| **A** | Fig3 | 超辐射/非辐射 loci | $(q_e,\varepsilon_i/\varepsilon_e)$ 平面 | 纯实 $\varepsilon$，$l=1,2,3$ | **否** | 低（解析求根） |
| B | Fig4 | $\sigma_{\rm sca}/\pi R^2$ | $\hbar\omega$ 0–6 eV | Ag R=300/Si R=200nm@SiO2 | **是**（Ag/Si/SiO2 色散） | 中 |
| C | Fig5(c,f) | $|a_1|,|b_1|$ | $\hbar\omega$ 0–6 eV | Ag R=25/Si R=40nm@SiO2 | **是** | 中 |
| D | Fig6 | 超吸收 loci | $(q_e,\varepsilon_i/\varepsilon_e)$ | 复 $\varepsilon$ 优化 | 否 | 中（复根） |

**关键提示**：本论文**没有**经典 $Q_{\rm ext}(x)$ vs 尺寸参数、跨 Rayleigh→Mie→几何光学过渡那张曲线。main-agent 若期望复现"经典 Mie 效率-尺寸曲线"，本文不含该图，应改用上表候选或另选论文/教材图。

**推荐**：阶段1单球 Mie 若求"零外部依赖、纯物理自洽"，选 **候选 A (Fig3)**——只依赖本文解析式，可硬约束验证（$a_l=1$ 时 $\sigma_{{\rm sca},l}=\sigma^{\rm sr}$）。若求"贴近实际光谱、可对色散"，选 **候选 C (Fig5 c/f)**——直接对比 $|a_1|,|b_1|$，但须先定 Ag/Si/SiO2 光学常数来源（缺失信息，需向用户/main-agent 确认）。
</content>
