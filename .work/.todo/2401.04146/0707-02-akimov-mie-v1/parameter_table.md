# 参数表 — Akimov 2401.04146（case 0707-02，聚焦 Fig6）

> 步骤：02-paper_reading（子 agent / W-sub）
> case：0707-02-akimov-mie-v1 ｜ timestamp：20260709
> 来源标注约定：`§X`=论文小节，`(公式名)`=formulas.md 中锚点，`Fig N`=figures.md，`tex:L`=Text-rev.tex 行号；`trust` 标注非论文原文的教材/惯例来源。

---

## 一、通用核参数（与 case 0703-01 完全共用，Mie 系数框架不变）

| 符号 | 定义 / 值 | 单位 | 来源 | 备注 |
|------|-----------|------|------|------|
| $q_e$ | $q_e=k_e R$（尺寸参数） | 无量纲 | §2 | 与 Fig3 相同定义 |
| $q_i$ | $q_i=k_i R$ | 无量纲 | §2 | 内部尺寸参数，本 case $q_i$ 通常为**复数**（因 $\varepsilon_i$ 复） |
| $\varepsilon_e$ | 外介质介电常数（实，${\rm Im}=0$） | 无量纲(相对) | §2 | 与 Fig3 相同 |
| $\varepsilon_i$ | 球内介电常数 | 无量纲(相对) | §2 | **本 case 为复数**（Fig3 仅实数）——这是与 Case1 参数表的核心差异 |

## 二、Fig6 专属参数

| 参数 | 值/范围 | 单位 | 来源 |
|------|---------|------|------|
| $q_e$ 扫描 | $[0,\ 10]$（与 Fig3 横轴相同范围，目视核对） | 无量纲 | Fig6 横轴，figures.md |
| ${\rm Re}\,\varepsilon_i/\varepsilon_e$ 显示范围 | 目视约 $[-5,\ 15]$（各面板上方子图纵轴） | 无量纲 | figures.md，**待人工精确核实**（见 missing_info） |
| ${\rm Im}\,\varepsilon_i/\varepsilon_e$ 显示范围 | 目视随面板不同：TM 约 0–3/0–4/0–4；TE 约 0–1.2/0–0.8/0–0.6 | 无量纲 | figures.md，**待人工精确核实** |
| 轨道阶 $l$ | 1, 2, 3 | — | Fig6 caption（与 Fig3 相同） |
| 偏振 | TM（求 $a_l=1/2$）+ TE（求 $b_l=1/2$），各 3 面板 | — | Fig6 caption |
| 求根目标 | $a_l^{(2)}(q_e,\varepsilon_i/\varepsilon_e)=0$（TM）或 $b_l^{(2)}(q_e,\varepsilon_i/\varepsilon_e)=0$（TE），$\varepsilon_i/\varepsilon_e\in\mathbb C$ | — | §3.3, tex:L361 |
| 分支数量（定性） | "multiple" 态（正实部区），"only one" TM 态（负实部区），TE 负实部区零态 | — | §3.3, tex:L361（逐字引用见 formulas.md 第六节） |
| **材料数据** | **无需**（零外部依赖，与 Fig3 相同，纯理论） | — | — |

## 三、Fig6 vs Fig3 参数对比（凸显复现难度差异来源）

| 项目 | Fig3（case 0703-01） | Fig6（本 case） |
|------|----------------------|------------------|
| $\varepsilon_i/\varepsilon_e$ 定义域 | 纯实数 $\mathbb R$ | 复数 $\mathbb C$（2 个实自由度） |
| 求根未知数个数（固定 $q_e$） | 1（实数 $\varepsilon$） | 2（${\rm Re}\,\varepsilon$, ${\rm Im}\,\varepsilon$） |
| 方程个数（固定 $q_e$） | 1（实方程 ${\rm Im}\,a_l=0$，酉性化简后） | 2（${\rm Re}\,a_l^{(2)}=0$ 且 ${\rm Im}\,a_l^{(2)}=0$） |
| 求根方法（Case1 已验证 / 本 case 建议） | `scipy.optimize.brentq`（一维） | `scipy.optimize.fsolve`/`root`（二维）+ 多起点 + 延拓（建议，未验证） |

## 四、特殊函数求值方式（与 Fig3 相同，直接复用）

| 函数 | 定义 | 实现 |
|------|------|------|
| 球 Bessel $j_l(q)$ | 规则解 | `scipy.special.spherical_jn(l, q)` |
| 第一类球 Hankel $h_l^{(1)}$ | $=j_l+{\rm i}y_l$ | `spherical_jn + 1j*spherical_yn` |
| 第二类球 Hankel $h_l^{(2)}$ | $=j_l-{\rm i}y_l$（$\zeta_l=q h_l^{(2)}$，本 case 直接用于 $a_l^{(2)}$） | `spherical_jn - 1j*spherical_yn` |
| 导数 $\psi_l',\xi_l',\zeta_l'$ | 对宗量求导 | `spherical_jn/yn(l,q,derivative=True)`，本 case 需注意 $q$ 或宗量本身可能为**复数**（$q_i$ 复），scipy 的 spherical_jn/yn 对复数宗量支持需要额外核实（见 missing_info） |

> **uncertainty**：`scipy.special.spherical_jn`/`spherical_yn` 官方文档主要面向实数输入；本 case $q_i=k_iR$ 因 $\varepsilon_i$ 复数而为复数，需要在 step04 明确核实 scipy 版本是否支持复数宗量，若不支持需改用 `scipy.special.spherical_jn` 的递推公式手动复数化，或改用其他复数 Bessel 实现（如通过半整数阶 `scipy.special.jv(l+0.5, z)` 复数版配合 $j_l(z)=\sqrt{\pi/(2z)}J_{l+1/2}(z)$）。这是本 case 相比 Fig3 新增的潜在实现风险点，Fig3 全程 $q_i$ 实数未遇到此问题。

## 五、极限态 verifier 判据（Fig6 专属 + 复用）

| 判据 | 公式 | 来源 | 用途 |
|------|------|------|------|
| 超吸收上限 | $\sigma^{\rm sa}_{{\rm abs},l}/(\pi R^2)=(2l+1)/(2q_e^2)$ | §3.3 | 求出根后代回验证 $\sigma_{\rm abs}$ 应等于此值 |
| 超吸收处散射=吸收 | $\sigma^{\rm sa}_{{\rm sca},l}=\sigma^{\rm sa}_{{\rm abs},l}$ | §3.3, tex:L367-370 | 硬约束，可作为 Layer1 判据 |
| 等分关系 | $\sigma^{\rm sa}_{{\rm sca},l}=\frac14\sigma^{\rm sr}_{{\rm sca},l}$ | §3.3 | 与 Fig3 超辐射极限的定量关联，可交叉验证 |
| 完备性判据 | 每 $(l,$偏振$)$ 正实部区多分支 + TM 负实部区恰 1 支 + TE 负实部区 0 支 | §3.3, tex:L361 逐字 | 求根完成后的分支计数自查（非数字化图也可用） |
| $a_l=1/2$ 直接断言 | $|a_l-1/2|<{\rm tol}$，其中 $a_l=1/2+a_l^{(2)}$ | §3.1+§3.3 | 求根后立即验证（Fig3 类比：case 0703-01 用 $|a_l-1|<1e-8$ 断言 sr） |

## 六、单位换算（与 Fig3 完全相同，直接复用）

- 论文本 case 涉及范围（$q_e\in[0,10]$）不含 nm/eV 实际材料参数（纯理论 loci），单位换算表见 case 0703-01 `parameter_table.md` 末尾"单位换算核对"节，此处不重复。

---

## provenance
- source_artifact: arXiv 2401.04146（Text-rev.tex §3.3 tex:L359-370）+ 本 case figures.md（Fig6 坐标轴目视核对）+ case 0703-01 parameter_table.md（交叉参考特殊函数实现约定）
- evidence_type: 论文原文数值 + caption 逐字 + 图像目视核对（部分待精确化，见 missing_info）+ 教材惯例（trust 标注）
- timestamp_version: 20260709
- scope_applicability: 本 case（0707-02）Fig6 超吸收态复现参数；不含材料色散（零外部依赖）
- confidence_result_class: 中高（核心参数齐全，坐标轴精确数值和 scipy 复数支持待核实）/ pipeline_completed
