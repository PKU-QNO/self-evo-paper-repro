# 参数表 — Akimov 2401.04146

> 步骤：02-paper_reading（子 agent / W-sub）
> case：0703-01-akimov-mie-v1 ｜ timestamp：20260703-2236
> **状态：已备齐，待 Gate1 用户核对**（目标图未定，本步不触发 gate；main-agent 会连同"选图"一起呈现用户）
> 来源标注约定：`§X`=论文小节，`(公式名)`=formulas.md 中锚点，`Fig N`=figures.md，`tex:L`=Text-rev.tex 行号；`trust` 标注非论文原文的教材/惯例来源。
> **不下载材料数据**：第二部分材料光学常数只列推荐源并标 `pending`。

---

## 第一部分 · 通用核参数（选哪张图都要，与材料无关）

### 1.1 尺寸参数与折射率

| 符号 | 定义 / 值 | 单位 | 来源 | 备注 |
|------|-----------|------|------|------|
| $q_e$ | $q_e=k_e R$（=尺寸参数，等价常见 $x$） | 无量纲 | §2 (H_inc)–(E_int)，formulas.md 一、二节 | 论文用 $q_e$ 而非 $x$ |
| $q_i$ | $q_i=k_i R=m\,q_e$ | 无量纲 | §2，(S:a_l) 上下文 | 内部尺寸参数 |
| $k_0$ | $k_0=\omega\sqrt{\varepsilon_0\mu_0}=\omega/c=2\pi/\lambda_0$ | rad/m | §2 (H),(E)，tex:L89 段 | 真空波数 |
| $k_e$ | $k_e=k_0\,\varepsilon_e^{1/2}$ | rad/m | §2 (H_inc) 后 | 外介质波数 |
| $k_i$ | $k_i=k_0\,\varepsilon_i^{1/2}$ | rad/m | §2 (H_inc) 后 | 球内波数 |
| $m$ | $m=\sqrt{\varepsilon_i/\varepsilon_e}$（相对折射率） | 无量纲 | BH 记号，`trust`（论文用 $\varepsilon_i/\varepsilon_e$，$m$ 是 BH 等价量） | 复现时 BH 式用 $m$ |
| $\varepsilon_i$ | 球内介电常数（复，含色散） | 无量纲(相对) | §2 | 候选 A 用纯实，B/C 用材料色散 |
| $\varepsilon_e$ | 外介质介电常数（实，${\rm Im}=0$） | 无量纲(相对) | §2；入射幅度式要求 ${\rm Im}\,\varepsilon_e=0$ | SiO2；候选 A 归一为 $\varepsilon_i/\varepsilon_e$ |
| $R$ | 球半径 | nm（论文）/ m（SI 计算） | 各 Fig caption | 按候选取值，见第二部分 |
| $E_0$ | 入射平面波电场幅度 | V/m | §2 入射幅度式 | 截面/系数与 $E_0$ 无关（比值），可设 1 |

### 1.2 多极阶数截断 $n_{max}$（$l_{max}$）

| 项 | 值 | 来源 | trust |
|----|----|------|-------|
| 论文实际用到的阶 | $l=1,2,3$（Fig1/3/6 到 $l=3$；Fig4/5/7/8 到 $l=2$） | Fig caption（tex:L314/339/…） | 论文原文 |
| 数值截断经验公式 | $n_{max}\approx x+4x^{1/3}+2$（Wiscombe 截断） | **教材/scipy 惯例，非 Akimov 原文** | `trust`：BH/Wiscombe 经典，高可信 |
| 论文是否给数值 $n_{max}$ | **否**（tex 中 "truncat" 均指物理"截断描述"，非数值截断，tex:L83/L395 已核） | missing_info.md | — |

> 复现建议：候选 A/B/C 的 $q_e$ 最大约 10（Fig3）或谱扫描下 Ag R=300nm@6eV 处 $q_e$ 也在个位数量级 → $n_{max}=\lceil x+4x^{1/3}+2\rceil$ 取到约 10–15 即足够收敛，对复现 $l=1,2,3$ 贡献绰绰有余。

### 1.3 特殊函数求值方式

| 函数 | 定义 | 实现（trust=scipy 惯例） |
|------|------|------------------------|
| 球 Bessel $j_l(q)$ | 规则解 | `scipy.special.spherical_jn(l, q)` |
| 第一类球 Hankel $h_l^{(1)}$ | $=j_l+{\rm i}y_l$ | `spherical_jn + 1j*spherical_yn` |
| 第二类球 Hankel $h_l^{(2)}$ | $=j_l-{\rm i}y_l$（$\zeta_l=q h_l^{(2)}$，两类场分解用） | `spherical_jn - 1j*spherical_yn` |
| Riccati–Bessel $\psi_l(q)$ | $\psi_l(q)=q\,j_l(q)$ | §2 (S:a_l) 上下文；formulas.md 三节 |
| Riccati–Bessel $\xi_l(q)$ | $\xi_l(q)=q\,h_l^{(1)}(q)$ | 同上 |
| 导数 $\psi_l',\xi_l'$ | 对宗量求导 | **论文未给递推式**；用 `spherical_jn(l,q,derivative=True)` 或递推 $\psi_l'(q)=\psi_{l-1}(q)-\frac{l}{q}\psi_l(q)$（`trust` BH 附录），见 missing_info |

> **复现注意**（uncertainty）：$\psi_l',\xi_l'$ 是对**各自宗量**（$q_i$ 或 $q_e$）求导，不是对 $r$。链式法则里 $\frac{d}{dr}=k\frac{d}{dq}$ 的 $k$ 因子已被本文 $a_l$ 分子分母的 $q_i,q_e$ 显式因子吸收——这正是本文式与 BH 式形式不同的来源。step06 用 BH 标准式实现、本文式交叉验证时须对齐此约定。

### 1.4 极限态 verifier 判据（纯理论，Layer 1/2，无需材料）

| 判据 | 公式 | 来源 | 用途 |
|------|------|------|------|
| 超辐射上限 | $\sigma^{\rm sr}_{{\rm sca},l}/(\pi R^2)=2(2l+1)/q_e^2$，$\sigma^{\rm sr}_{\rm abs}=0$ | §3.2，formulas.md 六节 | Fig3/4/5 limit 虚线；$a_l=1$ 时应命中 |
| 非辐射 | $\sigma^{\rm nr}_{\rm sca}=\sigma^{\rm nr}_{\rm abs}=0$ | §3.2 | $a_l=0$ anapole |
| 超吸收上限 | $\sigma^{\rm sa}_{{\rm abs},l}/(\pi R^2)=(2l+1)/(2q_e^2)=\tfrac14\sigma^{\rm sr}$ | §3.3 | Fig6/7/8 limit |
| Rayleigh | $q_e\ll1\Rightarrow|a_1|\propto q_e^3$，$Q_{\rm sca}\propto q_e^4$ | §3.2 | Layer1.4 slope=4 verifier |
| 能量守恒 | $\sigma_{\rm ext}=\sigma_{\rm sca}+\sigma_{\rm abs}$ | (sigma_*) 光学定理 | Layer1.1，rel err $<10^{-10}$ |
| 无耗零吸收 | ${\rm Im}\,\varepsilon_i=0\Rightarrow\sigma_{\rm abs}=0$ | §2 | Layer1.2 |
| 大尺寸消光佯谬 | $x\to\infty\Rightarrow Q_{\rm ext}\to2$ | verification.md Layer1.5 | `trust` 教材 |

---

## 第二部分 · 按候选分组的额外参数

### 候选 A — Fig3 超辐射/非辐射 loci（§3.2）★纯理论零材料数据

| 参数 | 值/范围 | 单位 | 来源 |
|------|---------|------|------|
| $q_e$ 扫描 | $[0,\ 10]$ | 无量纲 | Fig3 横轴，figures.md |
| $\varepsilon_i/\varepsilon_e$ 扫描 | $[-10,\ 15]$，**纯实值** | 无量纲 | Fig3 纵轴，figures.md |
| 轨道阶 $l$ | 1, 2, 3 | — | Fig3 caption |
| 偏振 | TM（$a_l$）+ TE（$b_l$），各 3 面板 | — | Fig3 caption |
| 求根目标 | 超辐射 $a_l=1$/$b_l=1$（虚线）；非辐射 $a_l=0$/$b_l=0$（实线） | — | §3.2 |
| **材料数据** | **无需**（零外部依赖） | — | — |

### 候选 C — Fig5(c,f) $|a_1|,|b_1|$ 谱（§3.2）需材料数据

| 参数 | 值/范围 | 单位 | 来源 |
|------|---------|------|------|
| Ag 球半径 (c) | $R=25$ | nm | Fig5 caption，tex:L339 |
| Si 球半径 (f) | $R=40$ | nm | Fig5 caption，tex:L339 |
| 外介质 | SiO2，$\varepsilon_e=n_{\rm SiO2}^2$ | — | Fig5 caption "embedded in silicon dioxide" |
| 光子能量 $\hbar\omega$ | $[0,\ 6]$ | eV | Fig5 横轴（图像读轴，正文未列数值） |
| 纵轴 | $|a_1|,|b_1|\in[0,1]$ | 无量纲 | Fig5(c)(f) |
| 阶 $l$ | 只需 $l=1$（$a_1,b_1$） | — | Fig5(c)(f) |
| **材料数据（pending，不下载）** | Ag / Si / SiO2 的 $\varepsilon(\omega)$ | — | 推荐源见下表 |

### 候选 B — Fig4 Ag/Si 大球散射谱（§3.2）需材料数据

| 参数 | 值/范围 | 单位 | 来源 |
|------|---------|------|------|
| Ag 球半径 (a–c) | $R=300$ | nm | Fig4 caption，tex:L314 |
| Si 球半径 (d–f) | $R=200$ | nm | Fig4 caption，tex:L314 |
| 外介质 | SiO2 | — | Fig4 caption |
| 光子能量 $\hbar\omega$ | $[0,\ 6]$ | eV | Fig4 横轴（图像读轴） |
| 纵轴 | $\sigma_{\rm sca}/(\pi R^2)$：总(线性 0–4 Ag / 0–8 Si)，分量(对数) | 无量纲 | Fig4 |
| 阶 $l$ | $l=1,2$（大球高阶显著） | — | Fig4 caption |
| **材料数据（pending，不下载）** | Ag / Si / SiO2 的 $\varepsilon(\omega)$ | — | 推荐源见下表 |

### 材料光学常数推荐数据源（候选 B/C 共用，全部 `pending`，本步不下载）

| 材料 | 推荐源 | 说明 | 状态 |
|------|--------|------|------|
| Ag（银） | Johnson & Christy, *Phys. Rev. B* 6, 4370 (1972) | 等离激元标准源；覆盖 0.5–6.5 eV | `pending`（待用户选定候选后搜） |
| Si（硅） | Aspnes & Studna, *Phys. Rev. B* 27, 985 (1983)；或 Green 2008 | 介电常数标准源；可见近红外 | `pending` |
| SiO2（二氧化硅） | Malitson, *J. Opt. Soc. Am.* 55, 1205 (1965)（Sellmeier） | 透明基底，${\rm Im}\,\varepsilon_e\approx0$，满足外介质无吸收假设 | `pending` |
| 通用获取 | refractiveindex.info 数据库（汇编上述源） | 便捷但须核对到原始文献 | `pending` |

> **uncertainty（候选 B/C）**：论文未注明用哪套色散数据源。若复现选用的 $\varepsilon(\omega)$ 与作者不同，LSPR/Mie 峰位可能偏移几十 meV → 影响 Layer3 定量吻合。missing_evidence：作者所用材料色散来源（论文未给，需选定候选后从图峰位反推或按标准源试）。候选 A 无此问题（零材料依赖）。

---

## 单位换算核对（论文 nm/eV → SI）

| 换算 | 关系 | 数值常数 |
|------|------|---------|
| 长度 nm↔m | $1\ {\rm nm}=10^{-9}\ {\rm m}$ | — |
| 光子能量↔角频率 | $\omega=E/\hbar$ | $\hbar=6.582\times10^{-16}$ eV·s ⟹ $\omega[{\rm rad/s}]=1.519\times10^{15}\times E[{\rm eV}]$ |
| 光子能量↔真空波长 | $\lambda_0=hc/E$ | $\lambda_0[{\rm nm}]=1239.84/E[{\rm eV}]$（$hc=1239.84$ eV·nm） |
| 真空波数 | $k_0=2\pi/\lambda_0=\omega/c$ | $c=2.998\times10^{8}$ m/s |
| 外介质波数 | $k_e=k_0\sqrt{\varepsilon_e}=k_0\,n_{\rm SiO2}$ | SiO2 $n\approx1.46$（$\varepsilon_e\approx2.13$）@可见 |
| 尺寸参数 | $q_e=k_e R=\dfrac{2\pi n_e R}{\lambda_0}=\dfrac{2\pi n_e R[{\rm nm}]\,E[{\rm eV}]}{1239.84}$ | 例：Ag R=25nm@3eV, $n_e$=1.46 ⟹ $q_e\approx0.55$（偶极主导，与 Fig5 小球一致） |

> 单位坑（step01 记忆 & SKILL 常见坑）：论文半径用 **nm**，光子能量用 **eV**（不是波长 nm，也不是角频率）；公式全 SI。$q_e$ 计算要 $\lambda_0$ 换到 SI 或统一用 eV·nm 常数 1239.84。截面/系数都是无量纲比值，与 $E_0$ 无关，代码里可令 $E_0=1$。

---

## provenance（本参数表）
- source_artifact：arXiv 2401.04146（Text-rev.tex，caption tex:L314/L339，§2/§3.2/§3.3）+ step01 formulas.md/figures.md
- evidence_type：论文原文数值 + caption 逐字 + 教材惯例（trust 标注）
- timestamp_version：20260703-2236
- scope_applicability：阶段1单球经典 Mie；材料色散数据为 pending 占位，未下载未验证
- confidence_result_class：高（参数抽取，非物理复现）/ pipeline_completed
