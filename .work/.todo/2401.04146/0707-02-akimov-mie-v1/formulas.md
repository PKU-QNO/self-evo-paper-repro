# 公式清单 — Akimov 2401.04146（case 0707-02，聚焦 Fig6 超吸收态）

- **来源**：LaTeX 源 `01-pdf_preprocessing/src/Text-rev.tex`（权威，非 OCR，本 case 独立逐条核对）
- **记号约定**：$q_i=k_iR$、$q_e=k_eR$（尺寸参数，等价常见 $x$）；$k_{i,e}=k_0\varepsilon_{i,e}^{1/2}$；$k_0=\omega\sqrt{\varepsilon_0\mu_0}$；下标 $i$=内部($r<R$)、$e$=外部($r>R$)；$l$=轨道指数、$m$=方位指数
- **★ 标记**：Fig6 复现最核心公式

---

## 一、基础场展开（第 2 节，tex:L92-121）

### (H),(E) — TM/TE 场组合
$$\vec H=\left(\vec H^{\rm TM}-\frac{\rm i}{k_0}\sqrt{\frac{\varepsilon_0}{\mu_0}}\nabla\times\vec E^{\rm TE}\right)e^{-{\rm i}\omega t}$$
$$\vec E=\left(\vec E^{\rm TE}+\frac{\rm i}{k_0\varepsilon}\sqrt{\frac{\mu_0}{\varepsilon_0}}\nabla\times\vec H^{\rm TM}\right)e^{-{\rm i}\omega t}$$

### (Y) — 标量球谐
$$Y_{lm}(\theta,\phi)=\sqrt{\frac{2l+1}{4\pi}\frac{(l-m)!}{(l+m)!}}\,P_l^m(\cos\theta)\,e^{{\rm i}m\phi}$$

### (WEd_H),(WEd_E) — 径向波动方程
$$\frac{{\rm d}^2 H_{lm}}{{\rm d}r^2}+\frac{2}{r}\frac{{\rm d}H_{lm}}{{\rm d}r}-\left[\frac{l(l+1)}{r^2}-k_0^2\varepsilon\right]H_{lm}=0$$
$E_{lm}$ 同型。

## 二、入射/散射/内部场（第 2 节，tex:L124-174）

### (H_inc)–(E_int)
$$H_{lm}^{\rm inc}=\widetilde H_{lm}j_l(k_e r),\quad E_{lm}^{\rm inc}=\widetilde E_{lm}j_l(k_e r)$$
$$H_{lm}^{\rm sca}=-a_l\widetilde H_{lm}h_l^{(1)}(k_e r),\quad E_{lm}^{\rm sca}=-b_l\widetilde E_{lm}h_l^{(1)}(k_e r)$$
$$H_{lm}^{\rm int}=d_l\widetilde H_{lm}j_l(k_i r),\quad E_{lm}^{\rm int}=c_l\widetilde E_{lm}j_l(k_i r)$$
$k_{i,e}=k_0\varepsilon_{i,e}^{1/2}$。

### 入射平面波球谐幅度（仅 ${\rm Im}\,\varepsilon_e=0$）
$$\widetilde H_{lm}=-{\rm i}^l\sqrt{\frac{\pi(2l+1)}{l(l+1)}}\sqrt{\frac{\varepsilon_0\varepsilon_e}{\mu_0}}\,m\,\delta_{m,\pm1}E_0$$
$$\widetilde E_{lm}=-{\rm i}^{l+1}\sqrt{\frac{\pi(2l+1)}{l(l+1)}}\,\delta_{m,\pm1}E_0$$

## 三、★★ Mie 系数（第 2 节，公式 S:a_l–S:d_l，tex:L176-194）— Fig6 上游最核心

> Riccati–Bessel 函数：$\psi_l(q)=q\,j_l(q)$，$\xi_l(q)=q\,h_l^{(1)}(q)$；$q_i=k_iR$，$q_e=k_eR$。$'$ 表示对宗量求导。

**(S:a_l) TM 散射系数：**
$$a_l=\frac{q_i\psi_l(q_i)\psi_l'(q_e)-q_e\psi_l(q_e)\psi_l'(q_i)}{q_i\psi_l(q_i)\xi_l'(q_e)-q_e\xi_l(q_e)\psi_l'(q_i)}$$

**(S:b_l) TE 散射系数：**
$$b_l=\frac{q_e\psi_l(q_i)\psi_l'(q_e)-q_i\psi_l(q_e)\psi_l'(q_i)}{q_e\psi_l(q_i)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_i)}$$

**(S:c_l),(S:d_l) 内场系数：** 略（本 case 超吸收态不直接用内场系数，需要时见 case 0703-01 formulas.md）。

> **复现注意**：本文 $a_l/b_l$ 与标准 Bohren–Huffman (BH) 记号（$m=\sqrt{\varepsilon_i/\varepsilon_e}$、$x=q_e$、$mx=q_i$）等价但代数形式不同（本文分子分母含显式 $q_i,q_e$ 因子）。**step04 建议以 BH 标准式为主实现，本文式交叉验证**——这条已在姊妹 case 0703-01 的 step03 用 300 随机点数值验证过（max 误差 4.7e-16），本 case 可直接复用该结论（同一套 Mie 系数代码，仅求解目标条件不同）。

## 四、★ 截面公式（第 2 节，公式 sigma_sca / sigma_abs，tex:L196-208）

$$\sigma_{\rm sca}=\frac{2\pi}{k_e^2}\sum_{l=1}^\infty(2l+1)\left(|a_l|^2+|b_l|^2\right)$$
$$\sigma_{\rm abs}=\frac{2\pi}{k_e^2}\sum_{l=1}^\infty(2l+1)\left[{\rm Re}(a_l+b_l)-(|a_l|^2+|b_l|^2)\right]$$

> 归一化：$\sigma/(\pi R^2)$。

## 五、两类散射场分解（第 3.1 节，tex:L212-285）★ Fig6 关键上游

### 向外/向内入射场分解
$$H_{lm}^{{\rm inc},j}=\tfrac12\widetilde H_{lm}h_l^{(j)}(k_e r),\quad E_{lm}^{{\rm inc},j}=\tfrac12\widetilde E_{lm}h_l^{(j)}(k_e r),\quad j=1,2$$

### (S:cd_l1) 向外分量 Mie 系数
$$a_l^{(1)}=b_l^{(1)}=\tfrac12,\qquad c_l^{(1)}=d_l^{(1)}=0$$

### ★★★ (S:a_l2)–(S:d_l2) 向内分量 Mie 系数 — Fig6 直接依赖公式
> $\zeta_l(q_e)=q_e h_l^{(2)}(q_e)$（球向内 Riccati-Bessel，第二类球 Hankel）。

$$a_l^{(2)}=\frac12\frac{q_i\psi_l(q_i)\zeta_l'(q_e)-q_e\zeta_l(q_e)\psi_l'(q_i)}{q_i\psi_l(q_i)\xi_l'(q_e)-q_e\xi_l(q_e)\psi_l'(q_i)}$$
$$b_l^{(2)}=\frac12\frac{q_e\psi_l(q_i)\zeta_l'(q_e)-q_i\zeta_l(q_e)\psi_l'(q_i)}{q_e\psi_l(q_i)\xi_l'(q_e)-q_i\xi_l(q_e)\psi_l'(q_i)}$$

> 关系：$a_l=a_l^{(1)}+a_l^{(2)}$，$b_l=b_l^{(1)}+b_l^{(2)}$。**因此 $a_l=1/2 \Leftrightarrow a_l^{(2)}=0$**（因为 $a_l^{(1)}\equiv1/2$ 恒成立），这是 main-agent 背景说明中给出的关键简化，tex 源第 361 行原文明确证实（"can be considered as those when the current-sourced scattered fields vanish"）。

## 六、★★★ 超吸收态公式（第 3.3 节，tex:L359-380）— Fig6 直接对应

### 超吸收条件（tex:L360-361）
$$a_l=\frac12\ \text{或}\ b_l=\frac12$$
等价于（tex:L361）
$$a_l^{(2)}=0\ (\text{TM})\quad\text{或}\quad b_l^{(2)}=0\ (\text{TE})$$

> 这是复数方程：$a_l^{(2)}(q_e,\varepsilon_i/\varepsilon_e)=0$，其中 $a_l^{(2)}$ 是关于复变量 $\varepsilon_i/\varepsilon_e$（$q_e$ 固定实数扫描）的解析函数。一个复数方程 = 2 个实自由度方程（Re 和 Im 各为零），恰好对应未知数 ${\rm Re}(\varepsilon_i/\varepsilon_e)$、${\rm Im}(\varepsilon_i/\varepsilon_e)$ 两个实自由度——是适定的（非欠定/超定）求根问题，不是优化问题。

### 完备性描述（tex:L361，逐字，Fig6 核对关键线索）
> "there are multiple TM and TE super-absorbing states with ${\rm Re~}\varepsilon_i/\varepsilon_e>0$ and only one TM state with ${\rm Re~}\varepsilon_i/\varepsilon_e<0$."

即：${\rm Re}(\varepsilon_i/\varepsilon_e)>0$ 区域，TM 和 TE 各有**多个**超吸收态（对每个 $l$、随 $q_e$ 变化形成分支族，类比 Fig3 的密集渐近扇形结构）；${\rm Re}(\varepsilon_i/\varepsilon_e)<0$ 区域**只有一个 TM 态**（且明确没有 TE 态在负实部区）。

### 吸收上限（tex:L363-366）
$$\sigma_{{\rm abs},l}^{\rm sa}=\frac{\pi}{2k_e^2}(2l+1)$$

### 超吸收处等分关系（tex:L367-370）
$$\sigma_{{\rm sca},l}^{\rm sa}=\sigma_{{\rm abs},l}^{\rm sa}=\frac14\sigma_{{\rm sca},l}^{\rm sr}$$
其中 $\sigma_{{\rm sca},l}^{\rm sr}=\frac{2\pi}{k_e^2}(2l+1)$（超辐射极限，第五节公式）。

> 归一化：$\sigma_{{\rm abs},l}^{\rm sa}/(\pi R^2)=\dfrac{2l+1}{2q_e^2}$（用 $q_e=k_eR$）。

## 七、超吸收态与超辐射态的对比（tex:L378，物理背景）

> 原文（逐字）："Contrary to the super-radiating states, the super-absorbing ones are achievable for dispersive materials with finite dissipation under the proper size and material design."

即超辐射态（$a_l=1$，纯实 $\varepsilon$，Fig3）在真实有耗材料中不可达；而超吸收态（$a_l=1/2$，复 $\varepsilon$）**可以**在真实有耗色散材料（如 Ag、Si）中实现——这是 Fig6（理论 loci，纯复值扫描）和 Fig7/Fig8（真实材料吸收谱，受 $\sigma^{\rm sa}_{{\rm abs},l}$ 限制）之间的物理关联。

## 八、局限性修正公式（第 4 节，非本 case 范围）

不复现；如需完整第七节公式见 case 0703-01 的 `formulas.md` 第七节。

---

## provenance
- source_artifact: arXiv 2401.04146 LaTeX 源 `Text-rev.tex` tex:L89-380（本 case 独立提取）
- evidence_type: 逐条从 tex 源转写，公式行号已核对
- timestamp_version: 20260709
- scope_applicability: Fig6 超吸收态复现所需全部公式（第2/3.1/3.3节）；第3.2节(Fig3)/第4节公式仅引用不复述
- confidence_result_class: 高（公式转写）/ pipeline_completed
