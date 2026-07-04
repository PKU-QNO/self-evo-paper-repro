# 公式清单 — Akimov 2401.04146

- **来源**：LaTeX 源 `01-pdf_preprocessing/src/Text-rev.tex`（权威，非 OCR，公式干净可提取）
- **提取方式**：逐条从 tex 源转写，保留原文上下文（前后文字）与论文内标签
- **记号约定**：$q_i=k_iR$、$q_e=k_eR$（$q_e$ 即尺寸参数，等价常见 $x$）；$k_{i,e}=k_0\varepsilon_{i,e}^{1/2}$；$k_0=\omega\sqrt{\varepsilon_0\mu_0}$；下标 $i$=内部($r<R$)、$e$=外部($r>R$)；$l$=轨道指数、$m$=方位指数
- **★ 标记**：复现阶段1单球 Mie 最核心、step04/06 必用的公式

---

## 一、基础场展开（第 2 节）

### 公式 (H),(E) — TM/TE 场组合
> 上下文：均匀 $\varepsilon$ 区域、无外部电荷电流时，电磁场可用 TM/TE 场完全描述。
$$\vec H=\left(\vec H^{\rm TM}-\frac{\rm i}{k_0}\sqrt{\frac{\varepsilon_0}{\mu_0}}\nabla\times\vec E^{\rm TE}\right)e^{-{\rm i}\omega t}$$
$$\vec E=\left(\vec E^{\rm TE}+\frac{\rm i}{k_0\varepsilon}\sqrt{\frac{\mu_0}{\varepsilon_0}}\nabla\times\vec H^{\rm TM}\right)e^{-{\rm i}\omega t}$$
其中 $\vec H^{\rm TM},\vec E^{\rm TE}$ 为 TM/TE 偏振支配场幅度，$k_0=\omega\sqrt{\varepsilon_0\mu_0}$。

### 公式 (Y) — 标量球谐
$$Y_{lm}(\theta,\phi)=\sqrt{\frac{2l+1}{4\pi}\frac{(l-m)!}{(l+m)!}}\,P_l^m(\cos\theta)\,e^{{\rm i}m\phi}$$
$P_l^m$ 为连带 Legendre 多项式。

### 公式 (WEd_H),(WEd_E) — 径向波动方程
> 上下文：径向标量函数 $H_{lm},E_{lm}$ 一般彼此独立，满足：
$$\frac{{\rm d}^2 H_{lm}}{{\rm d}r^2}+\frac{2}{r}\frac{{\rm d}H_{lm}}{{\rm d}r}-\left[\frac{l(l+1)}{r^2}-k_0^2\varepsilon\right]H_{lm}=0$$
$E_{lm}$ 同型。

## 二、入射/散射/内部场（第 2 节）★

### 公式 (H_inc)–(E_int) — 三类场
> 上下文：半径 $R$ 球，径向函数分段。散射用第一类球 Hankel $h_l^{(1)}$，内部用球 Bessel $j_l$。
$$H_{lm}^{\rm inc}=\widetilde H_{lm}j_l(k_e r),\quad E_{lm}^{\rm inc}=\widetilde E_{lm}j_l(k_e r)$$
$$H_{lm}^{\rm sca}=-a_l\widetilde H_{lm}h_l^{(1)}(k_e r),\quad E_{lm}^{\rm sca}=-b_l\widetilde E_{lm}h_l^{(1)}(k_e r)$$
$$H_{lm}^{\rm int}=d_l\widetilde H_{lm}j_l(k_i r),\quad E_{lm}^{\rm int}=c_l\widetilde E_{lm}j_l(k_i r)$$
$k_{i,e}=k_0\varepsilon_{i,e}^{1/2}$。

### 入射平面波球谐幅度（仅 ${\rm Im}\,\varepsilon_e=0$）
$$\widetilde H_{lm}=-{\rm i}^l\sqrt{\frac{\pi(2l+1)}{l(l+1)}}\sqrt{\frac{\varepsilon_0\varepsilon_e}{\mu_0}}\,m\,\delta_{m,\pm1}E_0$$
$$\widetilde E_{lm}=-{\rm i}^{l+1}\sqrt{\frac{\pi(2l+1)}{l(l+1)}}\,\delta_{m,\pm1}E_0$$
> 来自 $x$-偏振、沿 $z$ 传播 TEM 平面波 $\vec E^{\rm inc}=\vec e_x E_0 e^{{\rm i}(k_e r\cos\theta-\omega t)}$ 的分解。

## 三、★★ Mie 系数（第 2 节，公式 S:a_l–S:d_l）— 复现最核心

> 上下文：边界条件 $r=R$ 处 $\vec E^{\rm TE},\vec H^{\rm TM}$ 切向分量连续给出。Riccati–Bessel 函数：$\psi_l(q)=q\,j_l(q)$，$\xi_l(q)=q\,h_l^{(1)}(q)$；$q_i=k_iR$，$q_e=k_eR$。$'$ 表示对宗量求导。

**(S:a_l) TM 散射系数：**
$$a_l=\frac{q_i\psi_l(q_i)\psi_l'(q_e)-q_e\psi_l(q_e)\psi_l'(q_i)}{q_i\psi_l(q_i)\xi_l'(q_e)-q_e\xi_l(q_e)\psi_l'(q_i)}$$

**(S:b_l) TE 散射系数：**
$$b_l=\frac{q_e\psi_l(q_i)\psi_l'(q_e)-q_i\psi_l(q_e)\psi_l'(q_i)}{q_e\psi_l(q_i)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_i)}$$

**(S:c_l) 内场 TE 系数：**
$$c_l=\frac{q_i\psi_l(q_e)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_e)}{q_e\psi_l(q_i)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_i)}$$

**(S:d_l) 内场 TM 系数：**
$$d_l=\frac{q_i\psi_l(q_e)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_e)}{q_i\psi_l(q_i)\xi_l'(q_e)-q_e\xi_l(q_e)\psi_l'(q_i)}$$

> **复现注意**（uncertainty）：本文 $a_l/b_l$ 分子分母含 $q_i,q_e$ 显式因子，形式与标准 Bohren–Huffman (BH) 记号不同但等价。BH 记号用 $m=\sqrt{\varepsilon_i/\varepsilon_e}$（相对折射率）、$x=q_e$，$mx=q_i$。**step06 建议以 BH 标准式为准并用本式交叉验证**，注意 $\psi_l',\xi_l'$ 是对各自宗量 $q_i$ 或 $q_e$ 的导数。missing_evidence：本文未显式给 $\psi_l'$ 递推式，需从 BH/scipy 特殊函数补。

## 四、★ 截面公式（第 2 节，公式 sigma_sca / sigma_abs）

**(sigma_sca) 散射截面：**
$$\sigma_{\rm sca}=\frac{2\pi}{k_e^2}\sum_{l=1}^\infty(2l+1)\left(|a_l|^2+|b_l|^2\right)$$

**(sigma_abs) 吸收截面：**
$$\sigma_{\rm abs}=\frac{2\pi}{k_e^2}\sum_{l=1}^\infty(2l+1)\left[{\rm Re}(a_l+b_l)-(|a_l|^2+|b_l|^2)\right]$$

> 消光 $\sigma_{\rm ext}=\sigma_{\rm sca}+\sigma_{\rm abs}=\dfrac{2\pi}{k_e^2}\sum(2l+1){\rm Re}(a_l+b_l)$（光学定理，本文未单列但可推出）。
> 图中归一化：$\sigma/(\pi R^2)$，即效率 $Q=\sigma/\pi R^2$。用 $q_e=k_e R$ 有 $\dfrac{2\pi}{k_e^2\pi R^2}=\dfrac{2}{q_e^2}$。

## 五、两类散射场分解（第 3.1 节）★（本文核心创新）

### 向外/向内入射场分解
$$H_{lm}^{{\rm inc},j}=\tfrac12\widetilde H_{lm}h_l^{(j)}(k_e r),\quad E_{lm}^{{\rm inc},j}=\tfrac12\widetilde E_{lm}h_l^{(j)}(k_e r),\quad j=1,2$$

### (S:cd_l1) 向外分量 Mie 系数
$$a_l^{(1)}=b_l^{(1)}=\tfrac12,\qquad c_l^{(1)}=d_l^{(1)}=0$$

### (S:a_l2)–(S:d_l2) 向内分量 Mie 系数
> $\zeta_l(q_e)=q_e h_l^{(2)}(q_e)$（球向内 Riccati-Bessel）。
$$a_l^{(2)}=\frac12\frac{q_i\psi_l(q_i)\zeta_l'(q_e)-q_e\zeta_l(q_e)\psi_l'(q_i)}{q_i\psi_l(q_i)\xi_l'(q_e)-q_e\xi_l(q_e)\psi_l'(q_i)}$$
$$b_l^{(2)}=\frac12\frac{q_e\psi_l(q_i)\zeta_l'(q_e)-q_i\zeta_l(q_e)\psi_l'(q_i)}{q_e\psi_l(q_i)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_i)}$$
$$c_l^{(2)}=\frac12\frac{q_i\psi_l(q_e)\zeta_l'(q_e)-q_i\zeta_l(q_e)\psi_l'(q_e)}{q_e\psi_l(q_i)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_i)}$$
$$d_l^{(2)}=\frac12\frac{q_i\zeta_l(q_e)\xi_l'(q_e)-q_i\xi_l(q_e)\zeta_l'(q_e)}{q_i\psi_l(q_i)\xi_l'(q_e)-q_e\xi_l(q_e)\psi_l'(q_i)}$$
> 关系：$a_l=a_l^{(1)}+a_l^{(2)}$，$b_l=b_l^{(1)}+b_l^{(2)}$。

## 六、★ 极限态与截面上限（第 3.2、3.3 节）— 纯理论，可直接复现，无需材料数据

- **超辐射态**：$a_l=1$ 或 $b_l=1$（$a_l^{(2)}=a_l^{(1)}=\tfrac12$，相长）
- **非辐射态 (anapole)**：$a_l=0$ 或 $b_l=0$（$a_l^{(2)}=-a_l^{(1)}$，相消）
- **散射上限（超辐射）**：$\;\sigma_{{\rm sca},l}^{\rm sr}=\dfrac{2\pi}{k_e^2}(2l+1),\quad \sigma_{{\rm abs},l}^{\rm sr}=0$
  - 归一化：$\sigma_{{\rm sca},l}^{\rm sr}/(\pi R^2)=\dfrac{2(2l+1)}{q_e^2}$ ← Fig4/5/7/8 中 "limit" 虚线
- **非辐射**：$\sigma_{{\rm sca},l}^{\rm nr}=\sigma_{{\rm abs},l}^{\rm nr}=0$
- **超吸收态**：$a_l=1/2$ 或 $b_l=1/2$（即 $a_l^{(2)}=0$，源自由散射态）
- **吸收上限（超吸收）**：$\;\sigma_{{\rm abs},l}^{\rm sa}=\dfrac{\pi}{2k_e^2}(2l+1)$
- **超吸收处等分**：$\sigma_{{\rm sca},l}^{\rm sa}=\sigma_{{\rm abs},l}^{\rm sa}=\dfrac14\sigma_{{\rm sca},l}^{\rm sr}$
- **Rayleigh 极限**：$q_e\ll1$，$|a_1|\gg|b_1|,|a_2|,\dots$，$|a_1|\propto q_e^3$（可作 step07 Rayleigh verifier 判据）

## 七、局限性修正公式（第 4 节，非核心，阶段1可暂不复现）

### 4.1 激发源修正（含 $\alpha_l,\beta_l$）
- (a_l_ext)/(b_l_ext)：分母 $\psi_l',\xi_l'$ 换为 $A_l',B_l'$，$A_l(q_e)=\xi_l(q_e)+\alpha_l\zeta_l(q_e)$，$B_l(q_e)=\xi_l(q_e)+\beta_l\zeta_l(q_e)$。
- (S_sca_source)：$\sigma_{\rm sca}=\dfrac{2\pi}{k_e^2}\sum(2l+1)[|a_l|^2(1-|\alpha_l|^2)+|b_l|^2(1-|\beta_l|^2)]$
- (S_abs_source)：$\sigma_{\rm abs}=\dfrac{2\pi}{k_e^2}\sum(2l+1){\rm Re}[a_l(1-\alpha_l)+b_l(1-\beta_l)-|a_l|^2(1-|\alpha_l|^2)-|b_l|^2(1-|\beta_l|^2)]$

### 4.2 球界面/过渡层修正
- 光学力 (F_opt)：$\vec F^{\rm opt}=\tfrac12{\rm Re}\int(\rho^*\vec E^{\rm inc}+\mu_0\vec J^*\times\vec H^{\rm inc}){\rm d}V$，$\vec J=-{\rm i}\omega\varepsilon_0(\varepsilon-1)\vec E$。
- 非均匀径向方程 (WEd_H_inh)、(WEd_E_inh)；波阻抗/导纳 $\tilde Z_l,\tilde Y_l$ 的 Riccati 方程 (Z_H)、(Y_E)。
- 过渡层修正 Mie 系数 (a_l_tra)、(b_l_tra)，含 $\tilde R_i=2R_i/(R_i+R_e)$、$\tilde R_e=2R_e/(R_i+R_e)$、$F_l,G_l$（依赖 $\Delta\tilde Z_l,\Delta\tilde Y_l$）。
- 共振点 ${\rm Re}\,\varepsilon(r_0)=0$：$\Delta\tilde Z_l^{\rm res}=-{\rm i}\int_{r_0-0}^{r_0+0}\dfrac{l(l+1)}{k_0r^2\varepsilon(r)}{\rm d}r$，${\rm Re}\,\Delta\tilde Z_l^{\rm res}\approx\pi\dfrac{l(l+1)}{k_0r_0^2}\left(\dfrac{{\rm d\,Re}\,\varepsilon}{{\rm d}r}\right)^{-1}_{r=r_0}$。

> 阶段1单球复现建议只用第二~六节公式；第七节属"局限性/细化"是论文后半理论延伸，需额外建模参数（$\alpha_l,\beta_l,\Delta R,\varepsilon(r)$ 分布），不建议阶段1纳入。
</content>
