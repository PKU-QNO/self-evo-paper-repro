# Mie scattering theory: A review of physical features and limitations

- **作者**：Yuriy A. Akimov（IHPC, A*STAR, Singapore）
- **来源**：arXiv 2401.04146（2024-01-10），投稿 Phys. Rev. B 模板（revtex4-2）
- **正文来源**：本文由 LaTeX 源 `Text-rev.tex` 直接转写（权威，非 OCR）；PDF 为 9 页电子版可交叉核对
- **性质**：理论综述 + 分析型论文。核心是对 Mie 解做球谐分析，揭示"源自由"(source-free) 与"电流源"(current-sourced) 两类散射场的干涉如何造成共振，并讨论经典 Mie 理论的局限

> 说明：本文档保留章节结构，公式只给引用锚点（完整 LaTeX 见 `formulas.md`），图只给锚点（完整 caption 与分类见 `figures.md`）。

---

## Abstract

Mie 理论是球形粒子光散射的经典问题。本文对其感应场的解做球谐分析，揭示散射与吸收共振行为背后的物理。作者区分出两组散射场——电流源 (current-sourced) 与源自由 (current-free/source-free)——二者干涉使得每个轨道指数下的光-物质相互作用都呈共振。作为一种模型，源自由散射场天然限制了经典解的适用性。文中讨论这些局限，并给出在激发源描述、球界面、散射体局域化三方面进一步细化理论的途径。

## 1. Introduction

- Mie 理论（Mie 1908）是球形粒子电磁波散射的经典问题，桥接了小粒子 Rayleigh 散射与较大粒子 Rayleigh-Gans-Debye 散射，可算任意尺寸粒子。
- 解释了频率选择性散射与尺寸相关变色（胶体纳米粒子溶液）。
- 后被推广到多层球 (Aden 1951)、偶极子发射的非平面入射场 (Ruppin 1982)、快电子 (de Abajo 1999)。
- 现广泛用于纳米尺度等离激元与光子结构的光学共振设计。
- 遗留基础问题：为什么散射与吸收随粒子尺寸变化不同？为什么共振散射随尺寸单调增大而共振吸收不然？Mie 系数的共振本质从何而来？深亚波长金属粒子（高阶电流可忽略）为何仍出现类似共振？Mie 理论能预测电磁能量的稳态流，却不能预测动量流，说明它对光-物质相互作用是"截断"描述。
- 本文用严格球谐分析来回答这些问题。

## 2. Mie theory（核心公式区）

描述角频率 $\omega$ 的谐波平面波入射到球形粒子的散射与吸收。

- 均匀介电常数 $\varepsilon$ 区域内的场用 TM/TE 场描述 → 公式 (H)、(E)，其中 $k_0=\omega\sqrt{\varepsilon_0\mu_0}$ 为真空波数。
- 支配 TM/TE 场按矢量球谐 $Y_{lm}$ 展开（轨道/方位指数 $l,m$）→ (H_TM_lm)、(E_TE_lm)。
- 标量球谐 $Y_{lm}(\theta,\phi)$ 定义 → 公式 (Y)。
- 径向标量函数 $H_{lm},E_{lm}$ 满足波动方程 → (WEd_H)、(WEd_E)。
- 半径 $R$ 的球，径向函数分段定义（内 $r<R$ / 外 $r>R$）。
- 入射/散射/内部场：入射用球 Bessel $j_l(k_e r)$，散射用第一类球 Hankel $h_l^{(1)}(k_e r)$，内部用 $j_l(k_i r)$ → (H_inc)–(E_int)。$k_{i,e}=k_0\varepsilon_{i,e}^{1/2}$。
- $x$-偏振、沿 $z$ 传播的 TEM 平面波的球谐展开给出入射场幅度 $\widetilde H_{lm},\widetilde E_{lm}$（仅 ${\rm Im}\,\varepsilon_e=0$ 时）。
- **Mie 系数 $a_l,b_l,c_l,d_l$**（边界条件：$r=R$ 处切向 $E^{TE},H^{TM}$ 连续）→ 公式 (S:a_l)–(S:d_l)。其中 Riccati–Bessel 函数 $\psi_l(q)=q\,j_l(q)$、$\xi_l(q)=q\,h_l^{(1)}(q)$，$q_i=k_iR$、$q_e=k_eR$。
- **散射/吸收截面**（对入射平面波积分散射与吸收功率）→ 公式 (sigma_sca)、(sigma_abs)：
  - $\sigma_{\rm sca}=\dfrac{2\pi}{k_e^2}\sum_{l=1}^\infty (2l+1)(|a_l|^2+|b_l|^2)$
  - $\sigma_{\rm abs}=\dfrac{2\pi}{k_e^2}\sum_{l=1}^\infty (2l+1)[{\rm Re}(a_l+b_l)-(|a_l|^2+|b_l|^2)]$

> 注：本文用 $q_e=k_e R$ 作"尺寸参数"（等价于常见记号 $x$），$a_l/b_l$ 对应常见 Bohren–Huffman 记号 $a_n/b_n$。截面用 $\sigma$（非效率 $Q$），归一化时图中除以几何截面 $\pi R^2$（即 $Q_{\rm sca}=\sigma_{\rm sca}/\pi R^2$）。

## 3. Features

### 3.1 Two types of scattered fields（两类散射场）

- 因 Mie 理论对场线性，可把入射场拆成两部分，各自诱导散射/内部场。
- 把入射场分解为"球向外"与"球向内"两分量：$h_l^{(j)}(k_e r)$，$j=1,2$。
- 得到新 Mie 系数 $a_l^{(j)},b_l^{(j)},c_l^{(j)},d_l^{(j)}$：
  - 向外分量 ($j=1$)：$a_l^{(1)}=b_l^{(1)}=1/2$，$c_l^{(1)}=d_l^{(1)}=0$ → 公式 (S:cd_l1)。
  - 向内分量 ($j=2$)：$a_l^{(2)},b_l^{(2)},c_l^{(2)},d_l^{(2)}$ → 公式 (S:a_l2)–(S:d_l2)，含 $\zeta_l(q_e)=q_e h_l^{(2)}(q_e)$。
- **关键物理**：向外分量的散射场完全抵消入射场，内部场为零 → 对应 Maxwell 方程的"平凡解"（球内外总场为零），散射场是**源自由 (source-free)** 的（无内部电流却有非零散射场）。向内分量的散射场伴随非零内部场，是**电流源 (current-sourced)** 的。
- 源自由散射场与球的尺寸/材料无关；散射体的效应只由电流源场决定。非吸收粒子 (${\rm Im}\,\varepsilon_i=0$) 时二者仅相位差 ($|a_l^{(2)}|=|a_l^{(1)}|$)；吸收粒子则幅度与相位都不同（见 Fig2）。
- Fig1 展示不同 $l$ 的源自由散射场分布。

### 3.2 Super-radiating and non-radiating states（超辐射与非辐射态）

- 总 Mie 系数是两类场之和：$a_l=a_l^{(1)}+a_l^{(2)}$，$b_l=b_l^{(1)}+b_l^{(2)}$。二者干涉产生超辐射态与非辐射态。
- **超辐射态**：$a_l=1$ 或 $b_l=1$（相长干涉，$a_l^{(2)}=a_l^{(1)}$）。
- **非辐射态 (anapole)**：$a_l=0$ 或 $b_l=0$（相消干涉，$a_l^{(2)}=-a_l^{(1)}$）。
- 这些态要求纯实介电常数，真实（色散+耗散）材料达不到，但定义了每个 $l$ 与偏振对总截面的贡献极限：
  - $\sigma_{{\rm sca},l}^{\rm sr}=\dfrac{2\pi}{k_e^2}(2l+1)$，$\sigma_{{\rm abs},l}^{\rm sr}=0$；$\sigma_{{\rm sca},l}^{\rm nr}=\sigma_{{\rm abs},l}^{\rm nr}=0$。
- Fig3 给出 $l=1,2,3$、TM/TE 的超辐射（虚线）/非辐射（实线）态在 $(q_e,\varepsilon_i/\varepsilon_e)$ 平面的 loci。
- Fig4（Ag R=300nm / Si R=200nm）展示散射截面干涉条纹，上限为 $\sigma_{{\rm sca},l}^{\rm sr}$。
- 条纹密度受球尺寸影响；$q_e\le 2$ 时可滤掉高阶 $l$ 贡献，Fig5（Ag R=25nm / Si R=40nm）展示以偶极 ($l=1$) 为主的情形。
- **基本非辐射态**：$q_e=0$（与偏振/$l$/材料无关，对应 **Rayleigh 散射** $q_e\ll1$，$|a_1|\gg$其余，$|a_1|\propto q_e^3$）；以及 $\varepsilon_i=\varepsilon_e$（与偏振/$l$/尺寸无关，需实 $\varepsilon_i$，Fig5(a) 中 Ag 在 $\hbar\omega\approx3.9$ eV 附近）。

### 3.3 Super-absorbing states（超吸收态）

- 最大可达吸收：**超吸收态** $a_l=1/2$ 或 $b_l=1/2$，需为每个 $q_e$ 优化复 $\varepsilon_i/\varepsilon_e$（Fig6）。等价于电流源散射场消失 ($a_l^{(2)}=0$)，即"源自由散射态"。
- 上限贡献：$\sigma_{{\rm abs},l}^{\rm sa}=\dfrac{\pi}{2k_e^2}(2l+1)$；且此时散射=吸收=超辐射极限的 1/4：$\sigma_{{\rm sca},l}^{\rm sa}=\sigma_{{\rm abs},l}^{\rm sa}=\tfrac14\sigma_{{\rm sca},l}^{\rm sr}$。
- 与超辐射态不同，超吸收态在色散有耗材料中可实现。Fig7（大粒子）、Fig8（小粒子，偶极主导）展示吸收条纹，上限 $\sigma_{{\rm abs},l}^{\rm sa}$。

## 4. Limitations

### 4.1 Excitation source（激发源）

- 用外部入射场建模激发源会使电磁相互作用描述不完整。要计入外部激发电流，散射场须为 $h^{(1)}$ 与 $h^{(2)}$ 的线性组合（含复相互作用系数 $\alpha_l,\beta_l$）→ 修改后的 $a_l,b_l$ 公式 (a_l_ext)、(b_l_ext)，及 $A_l,B_l$ 定义。
- 修改后的截面 → (S_sca_source)、(S_abs_source)，含 $(1-|\alpha_l|^2)$ 等因子。影响低阶 $l$ 尤甚（Fig9 $\eta_{\rm sca}$、Fig10 $\eta_{\rm abs}$）。

### 4.2 Sphere interface（球界面）

- Mie 解的电场在 $r=R$ 处不连续，导致无法算总力 $F^{\rm tot}$、压缩力 $F^{\rm com}$（光学力 $F^{\rm opt}$ 可算 → 公式 (F_opt)）。
- 解决：引入 $\varepsilon(r)$ 径向渐变的连续过渡层。此时径向方程改为 (WEd_H_inh)、(WEd_E_inh)；引入相对 TM 波阻抗 $\tilde Z_l$、TE 波导纳 $\tilde Y_l$ → Riccati 型方程 (Z_H)、(Y_E)。
- 过渡层给出修改的 Mie 系数 (a_l_tra)、(b_l_tra)，含 $\tilde R_i,\tilde R_e$ 与因子 $F_l,G_l$（依赖过渡层阻抗差 $\Delta\tilde Z_l$、导纳差 $\Delta\tilde Y_l$）。
- 薄层时 $\Delta\tilde Z_l,\Delta\tilde Y_l \propto \Delta R$；当过渡层存在 ${\rm Re}\,\varepsilon(r_0)=0$ 的点时 $\Delta\tilde Z_l$ 共振（TM，高 $l$ 增强超表面吸收，需 ${\rm Re}\,\varepsilon_i/\varepsilon_e<0$）。Fig11/Fig12 展示线性 $\varepsilon(r)$ 分布下 $\eta_{\rm sca}/\eta_{\rm abs}$。

### 4.3 Scatterer localization（散射体局域化）

- 源自由散射场的根源是散射体在 $r<R$ 的有限局域化：入射与散射场在 $r>R$ 满足同一方程、可完全抵消。
- 要避免须让散射体延展到全空间、仅在 $r\to\infty$ 消失（无界散射体）。但径向非均匀球的散射解与经典 Mie 显著不同，经典散射系数无法修改来描述无限延展散射体。

## 5. Conclusion

- 球谐分析揭示 Mie 理论处理两组场（源自由 + 电流源），二者干涉造成散射/吸收共振与全部谱特征。
- 讨论了源自由场带来的局限，及在激发源、球界面、散射体局域化三方面细化经典理论的途径。这些局限与解法对多数散射问题通用，也适用于非球形散射体。

## 参考文献要点（与复现相关）

- [Bohren:1998] Bohren & Huffman, *Absorption and Scattering of Light by Small Particles*（本工作区 `.paper/scattering.pdf`，公式主源）
- [Stratton:2007] Stratton, *Electromagnetic Theory*
- [Jackson:1999] Jackson, *Classical Electrodynamics*
- [Li:2014] *Plasmonic Nanoelectronics and Sensing*（本文场分解公式主引）
- [Mie:1908] G. Mie, Ann. Phys. 330, 377 (1908)
- 其余 Akimov/Grahn/Miroshnichenko/Luk'yanchuk 等见源 bibliography（`formulas.md` 末不复列）
</content>
</invoke>
