# Mie scattering theory: A review of physical features and limitations

- **作者**：Yuriy A. Akimov（IHPC, A*STAR, Singapore）
- **来源**：arXiv 2401.04146（2024-01-10），投稿 Phys. Rev. B 模板（revtex4-2）
- **正文来源**：本文档由 LaTeX 源 `01-pdf_preprocessing/src/Text-rev.tex`（664 行）直接转写（权威，非 OCR）
- **性质**：理论综述 + 分析型论文。核心是对 Mie 解做球谐分析，揭示"源自由"(source-free) 与"电流源"(current-sourced) 两类散射场的干涉如何造成共振，并讨论经典 Mie 理论的局限
- **本 case（0707-02）聚焦目标**：第 3.3 节 "Super-absorbing states"（超吸收态，Fig6），其上游依赖第 2 节（Mie 系数）、第 3.1 节（两类场分解）、第 3.2 节（超辐射/非辐射态，Fig3——已由 case 0703-01 复现）

> 说明：本文档结构与 case 0703-01 的 `paper_text.md` 一致（同一篇论文），公式只给引用锚点（完整 LaTeX 见 `formulas.md`），图只给锚点（完整 caption 与分类见 `figures.md`）。本次独立重新核对 tex 源逐条转写，未直接照抄 0703-01 版本。

---

## Abstract

Mie 理论是球形粒子光散射的经典问题。本文对其感应场的解做球谐分析，揭示散射与吸收共振行为背后的物理。作者区分出两组散射场——电流源 (current-sourced) 与源自由 (source-free)——二者干涉使得每个轨道指数下的光-物质相互作用都呈共振。作为一种模型，源自由散射场天然限制了经典解的适用性。文中讨论这些局限，并给出在激发源描述、球界面、散射体局域化三方面进一步细化理论的途径。

## 1. Introduction（tex:L62-86）

- Mie 理论（Mie 1908）是球形粒子电磁波散射的经典问题，桥接了小粒子 Rayleigh 散射与较大粒子 Rayleigh-Gans-Debye 散射。
- 遗留基础问题：为什么散射与吸收随粒子尺寸变化不同？为什么共振散射随尺寸单调增大而共振吸收不然？Mie 系数共振的本质从何而来？深亚波长金属粒子（高阶电流可忽略）为何仍出现共振？
- Mie 理论能预测电磁能量的稳态流，却不能预测动量流，说明它是对光-物质相互作用的"截断"描述。
- 本文用严格球谐分析回答这些问题。

## 2. Mie theory（tex:L89-208，核心公式区）

描述角频率 $\omega$ 的谐波平面波入射到球形粒子的散射与吸收。

- 均匀介电常数 $\varepsilon$ 区域内的场用 TM/TE 场描述 → 公式 (H)、(E)，$k_0=\omega\sqrt{\varepsilon_0\mu_0}$ 为真空波数。
- 支配 TM/TE 场按矢量球谐 $Y_{lm}$ 展开（轨道/方位指数 $l,m$）→ (H_TM_lm)、(E_TE_lm)；标量球谐定义 → 公式 (Y)。
- 径向标量函数 $H_{lm},E_{lm}$ 满足波动方程 → (WEd_H)、(WEd_E)。
- 半径 $R$ 的球，径向函数分段定义（内 $r<R$ / 外 $r>R$）；入射用 $j_l(k_e r)$，散射用 $h_l^{(1)}(k_e r)$，内部用 $j_l(k_i r)$ → (H_inc)–(E_int)。$k_{i,e}=k_0\varepsilon_{i,e}^{1/2}$。
- $x$-偏振、沿 $z$ 传播的 TEM 平面波的球谐展开给出入射场幅度 $\widetilde H_{lm},\widetilde E_{lm}$（仅 ${\rm Im}\,\varepsilon_e=0$ 时）。
- **Mie 系数 $a_l,b_l,c_l,d_l$**（边界条件：$r=R$ 处切向 $E^{TE},H^{TM}$ 连续）→ 公式 (S:a_l)–(S:d_l)。Riccati–Bessel 函数 $\psi_l(q)=q\,j_l(q)$、$\xi_l(q)=q\,h_l^{(1)}(q)$，$q_i=k_iR$、$q_e=k_eR$。
- **散射/吸收截面** → 公式 (sigma_sca)、(sigma_abs)。

## 3. Features（tex:L210-380）

### 3.1 Two types of scattered fields（两类散射场，tex:L212-301）

- Mie 理论对场线性，可把入射场拆成"球向外"($h_l^{(1)}$, $j=1$) 与"球向内"($h_l^{(2)}$, $j=2$) 两分量，各自诱导散射/内部场。
- 向外分量 ($j=1$)：$a_l^{(1)}=b_l^{(1)}=1/2$，$c_l^{(1)}=d_l^{(1)}=0$ → 公式 (S:cd_l1)。散射场恰好完全抵消入射场，内部场为零 → Maxwell 方程的"平凡解"，散射场是**源自由 (source-free)**（无内部电流却有非零散射场），与球尺寸/材料无关。
- 向内分量 ($j=2$)：$a_l^{(2)},b_l^{(2)},c_l^{(2)},d_l^{(2)}$ → 公式 (S:a_l2)–(S:d_l2)，含 $\zeta_l(q_e)=q_e h_l^{(2)}(q_e)$（第二类球 Hankel）。伴随非零内部场，是**电流源 (current-sourced)** 场，散射体的全部物理效应由它决定。
- 无耗材料 (${\rm Im}\,\varepsilon_i=0$) 时 $|a_l^{(2)}|=|a_l^{(1)}|$（仅相位差）；有耗材料幅度、相位都不同（Fig2）。Fig1 展示源自由场分布（$q_e=1$，场分布图）。

### 3.2 Super-radiating and non-radiating states（超辐射/非辐射态，tex:L304-357）

- 总系数是两类场之和：$a_l=a_l^{(1)}+a_l^{(2)}$，$b_l=b_l^{(1)}+b_l^{(2)}$。
- **超辐射态**：$a_l=1$ 或 $b_l=1$（相长干涉，$a_l^{(2)}=a_l^{(1)}$）；**非辐射态 (anapole)**：$a_l=0$ 或 $b_l=0$（相消干涉，$a_l^{(2)}=-a_l^{(1)}$）。
- 二者均需纯实介电常数（真实材料达不到，是理论上限）：$\sigma_{{\rm sca},l}^{\rm sr}=\frac{2\pi}{k_e^2}(2l+1)$，$\sigma_{{\rm abs},l}^{\rm sr}=0$；$\sigma_{{\rm sca},l}^{\rm nr}=\sigma_{{\rm abs},l}^{\rm nr}=0$。
- Fig3 给出 $l=1,2,3$、TM/TE 的超辐射（虚线）/非辐射（实线）态在 $(q_e,\varepsilon_i/\varepsilon_e)$ **实平面**的 loci（本 case 的姊妹 case 0703-01 已复现）。
- Fig4 展示 Ag/Si 散射截面干涉条纹，上限 $\sigma^{\rm sr}_{{\rm sca},l}$；Fig5 是 $q_e\le2$ 小球偶极主导情形。
- 两类基本非辐射态：$q_e=0$（Rayleigh 极限）；$\varepsilon_i=\varepsilon_e$（阻抗匹配，需实 $\varepsilon_i$）。

### 3.3 Super-absorbing states（超吸收态，tex:L359-380）★★本 case 核心

> 原文（tex:L359-361，逐字）：
> "Another limiting case important for understanding of Mie theory is the maximum achievable absorption. Following Eq.~(\ref{sigma_abs}), the {\it super-absorbing states} must exhibit either $a_{l}=1/2$ or $b_{l}=1/2$. These states require the complex values of $\varepsilon_i/\varepsilon_e$ optimized for every size parameter $q_e$, as shown in Fig.~\ref{Fig6}. The above conditions also can be considered as those when the current-sourced scattered fields vanish: $a_{l}^{(2)}=0$ for the TM polarization or $b_{l}^{(2)}=0$ for the TE one. In other words, the super-absorbing states appear exactly the {\it source-free scattering states}. Contrary to the super-scattering states, there are multiple TM and TE super-absorbing states with ${\rm Re~}\varepsilon_i/\varepsilon_e>0$ and only one TM state with ${\rm Re~}\varepsilon_i/\varepsilon_e<0$."

- **超吸收条件**：$a_l=1/2$ 或 $b_l=1/2$。要求对每个尺寸参数 $q_e$ **优化复值** $\varepsilon_i/\varepsilon_e$（见 Fig6）。
- **等价条件（关键简化）**：电流源散射场消失，$a_l^{(2)}=0$（TM）或 $b_l^{(2)}=0$（TE）——超吸收态恰好是**源自由散射态**。
- **完备性线索（原文明示，可用于核对复现结果）**：与超辐射态不同，存在**多个** ${\rm Re}\,\varepsilon_i/\varepsilon_e>0$ 的 TM/TE 超吸收态，但**只有一个** ${\rm Re}\,\varepsilon_i/\varepsilon_e<0$ 的 TM 态（无 TE 态在 ${\rm Re}<0$ 区）。
- 吸收上限：$\sigma_{{\rm abs},l}^{\rm sa}=\frac{\pi}{2k_e^2}(2l+1)$（tex:L363-366）。超吸收处等分：$\sigma_{{\rm sca},l}^{\rm sa}=\sigma_{{\rm abs},l}^{\rm sa}=\frac14\sigma_{{\rm sca},l}^{\rm sr}$（tex:L368-370）。
- 超吸收态**可以**在色散有耗材料中实现（与超辐射态相反，tex:L378），Fig7/Fig8 展示实际 Ag/Si 粒子的吸收条纹（受 $\sigma^{\rm sa}_{{\rm abs},l}$ 限制）。
- 图 Fig6 说明（tex:L380）：吸收上限处对应的散射场恰为纯源自由（"the corresponding scattered fields are purely source-free"）。

## 4. Limitations（tex:L382-563，非本 case 范围）

阶段1单球复现不涉及；参见 case 0703-01 的 `paper_text.md` 第 4 节摘要（激发源修正 §4.1、球界面过渡层 §4.2、散射体局域化 §4.3）。

## 5. Conclusion（tex:L564-570）

球谐分析揭示 Mie 理论处理源自由 + 电流源两组场，二者干涉造成散射/吸收共振与全部谱特征；讨论了源自由场带来的局限，及三方面细化理论的途径。

## 参考文献要点（与本 case 相关）

- [Bohren:1998] Bohren & Huffman, *Absorption and Scattering of Light by Small Particles*（本工作区 `.paper/scattering.pdf`，Mie 系数公式主源，用于 step04 交叉验证）
- [Stratton:2007]、[Jackson:1999]：经典电磁场理论教材，边界条件推导引用
- [Li:2014]：本文场分解公式主引
- [Mie:1908] G. Mie, Ann. Phys. 330, 377 (1908)

## provenance
- source_artifact: arXiv 2401.04146 LaTeX 源 `Text-rev.tex`（本 case 独立读取，tex:L1-664 全文核对）
- evidence_type: 逐字文本提取
- timestamp_version: 20260709
- scope_applicability: 本 case（0707-02）聚焦 Fig6（超吸收态），上游依赖第2/3.1/3.2节
- confidence_result_class: 高（文本转写）/ pipeline_completed
