# 论文理解笔记 — Akimov 2401.04146（case 0707-02，聚焦 Fig6）

> 步骤：02-paper_reading（子 agent / W-sub）
> case：0707-02-akimov-mie-v1 ｜ timestamp：20260709
> 论文：Yuriy A. Akimov, *Mie scattering theory: A review of physical features and limitations*, arXiv 2401.04146 (2024)
> 与姊妹 case 0703-01（Fig3）的关系：同一篇论文，同一套 Mie 系数框架（第2/3.1节公式完全复用），本 case 聚焦第 3.3 节超吸收态（Fig6），比 Fig3 多一层复杂度（复数域求根 vs 实数域求根）。

---

## 1. 物理问题：Fig6 算的是什么物理量

**一句话**：Fig6 画出的是"对每个尺寸参数 $q_e$，能让球达到最大可能吸收（超吸收态 $a_l=1/2$ 或 $b_l=1/2$）所需的复相对介电常数 $\varepsilon_i/\varepsilon_e$"，按 $l=1,2,3$、TM/TE 分类，画成 $\varepsilon_i/\varepsilon_e$ 的 Re 和 Im 两条曲线（各自 vs $q_e$）。

**物理背景（承接 Fig3 的框架）**：
- 论文第 3.1 节把散射系数分解为源自由分量 $a_l^{(1)}=1/2$（恒定）与电流源分量 $a_l^{(2)}(q_e,\varepsilon_i/\varepsilon_e)$（依赖尺寸和材料），总系数 $a_l=a_l^{(1)}+a_l^{(2)}$。
- 第 3.2 节：超辐射态（$a_l=1$，$a_l^{(2)}=a_l^{(1)}=1/2$，相长干涉）与非辐射态（$a_l=0$，$a_l^{(2)}=-a_l^{(1)}=-1/2$，相消干涉）——**都要求纯实 $\varepsilon$**（因为需要 $a_l^{(2)}$ 与实数 $a_l^{(1)}=1/2$ 完全同相或反相叠加，且酉性保证纯实 $\varepsilon$ 时 $|a_l|^2={\rm Re}\,a_l$ 强制 $a_l\in\{0,1\}$，这是 case 0703-01 已验证的关键代数事实）。
- 第 3.3 节：超吸收态（$a_l=1/2$）要求 $a_l^{(2)}=0$——即电流源散射场**完全消失**，不是"与源自由场干涉"而是"根本不存在"。这个条件**不要求** $\varepsilon$ 为实数（$a_l^{(2)}=0$ 本身是复数方程，实部虚部各自为零，两个约束对两个实自由度 ${\rm Re}\,\varepsilon,{\rm Im}\,\varepsilon$，是适定问题，解通常落在复平面而非实轴上）。

## 2. Fig6 坐标轴的复数表示方式怎么理解（main-agent 决策问题 1 的回答）

**判断（基于 figures.md 中对 Fig6.png 的目视核对）**：Fig6 **不是**单一 2D 图上画复数平面的某种投影，而是**把每条 loci 曲线的复值 $\varepsilon_i/\varepsilon_e(q_e)$ 拆分成两个独立的实值子图**：
- 每个 $(l,$偏振$)$ 组合对应**一对纵向堆叠的子图**：上方子图纵轴 ${\rm Re}\,\varepsilon_i/\varepsilon_e$，下方子图纵轴 ${\rm Im}\,\varepsilon_i/\varepsilon_e$；两者共享横轴 $q_e\in[0,10]$。
- 这本质上是**参数曲线的分量展开图**：把 $q_e\mapsto\varepsilon_i(q_e)/\varepsilon_e\in\mathbb C$ 这条"复值函数曲线"拆成 ${\rm Re}(q_e)$ 和 ${\rm Im}(q_e)$ 两条实值函数曲线分别画，而不是画在复平面 $({\rm Re}\,\varepsilon,{\rm Im}\,\varepsilon)$ 上（那样会丢失 $q_e$ 作为显式坐标轴的信息）。
- 每条曲线有一个分支编号（图上数字标签 1–12），同一编号在 Re 子图和 Im 子图中配对，代表同一条 loci 曲线的两个分量。这与 Fig3（loci 直接画在 $(q_e,\varepsilon_i/\varepsilon_e)$ 实平面上，一条曲线一张图）的表示方式不同——Fig3 因为求解域是纯实数，可以直接用一张 2D 图；Fig6 因为解是复数，需要两张子图才能完整表示同一条曲线。

**这个理解对 step03/04 的直接含义**：数值实现时，对每个固定的 $l$、偏振、分支，要在 $q_e$ 网格上求解复数 $\varepsilon_i/\varepsilon_e(q_e)$，然后把结果的 Re 部分和 Im 部分分别存成两条曲线数据，分别与 Fig6 对应面板的上/下子图比对（不是与单一复平面图比对）。

## 3. Fig6 相比 Fig3 在数值方法上难在哪（main-agent 决策问题 2 的回答）

**核心难点对比**：

| 维度 | Fig3（case 0703-01，已完成） | Fig6（本 case） |
|------|------------------------------|------------------|
| 未知数 | 1 个实数 $\varepsilon_i/\varepsilon_e\in\mathbb R$（固定 $q_e$） | 1 个复数 $\varepsilon_i/\varepsilon_e\in\mathbb C$，即 2 个实自由度（固定 $q_e$） |
| 方程 | $a_l(q_e,\varepsilon)=1$ 或 $0$，用酉性化简为单实方程 ${\rm Im}\,a_l=0$（case 0703-01 已证严格） | $a_l^{(2)}(q_e,\varepsilon_i/\varepsilon_e)=0$，是 1 个复数方程 = 2 个实方程（${\rm Re}\,a_l^{(2)}=0$ 且 ${\rm Im}\,a_l^{(2)}=0$ 同时成立） |
| 求根策略 | 一维切片扫描 + brentq（一维实数求根，符号翻转区间可靠定位） | 二维（复平面）求根：一维 brentq 不再直接适用，需要二维 Newton/割线法，或把 2 个实方程联立解 2×2 非线性方程组 |
| 初值/分支追踪 | 固定 $q_e$ 切片扫描 $\varepsilon$ 网格找符号翻转，天然覆盖所有分支 | 需要在复平面上先定位候选解（如用 $|a_l^{(2)}|$ 的等值线图/梯度下降找极小值候选点），再用 Newton 法精修；分支连续性（沿 $q_e$ 变化时同一分支应平滑演化）需要额外的分支追踪逻辑（continuation method），比一维切片扫描更容易漏根或串错支 |
| 已验证的简化 | 酉性 $\Rightarrow$ 实数化，无耗散无关 | **不能**用酉性化简（因为 $\varepsilon$ 本身是复数，酉性关系 $|a_l|^2={\rm Re}\,a_l$ 仅在纯实 $\varepsilon$ 时严格成立，case 0703-01 memory 已明确"含耗散/复 ε（如 Fig6 超吸收）不适用"） |

**结论**：Fig6 比 Fig3 难在"从一维实数求根问题升级为二维复数求根问题"，且不能复用 Fig3 已验证的酉性实数化捷径。这是本质性的方法论跃升，不是简单的参数扩展。

### 对求根策略的初步建议（main-agent 决策问题 2 的具体建议，供 step03/04 参考）

1. **复数方程转实数方程组**：把 $a_l^{(2)}(q_e,z)=0$（$z=\varepsilon_i/\varepsilon_e\in\mathbb C$，固定 $q_e$）拆成 $F_1(x,y)={\rm Re}\,a_l^{(2)}(q_e,x+{\rm i}y)=0$，$F_2(x,y)={\rm Im}\,a_l^{(2)}(q_e,x+{\rm i}y)=0$（$x={\rm Re}\,z,y={\rm Im}\,z$），用 `scipy.optimize.fsolve` 或 `scipy.optimize.root`（二维非线性方程组求根）逐点求解，比直接在复数域上手写 Newton 迭代更稳妥（scipy 有成熟的雅可比数值近似和收敛判据）。
2. **多起点覆盖多分支**：由于原文明确"multiple TM and TE super-absorbing states"，必须在合理的 $(x,y)$ 初值网格（如 $x\in[-10,20]$、$y\in[0,10]$，参考 Fig3 的 $\varepsilon$ 范围 $[-10,15]$ 外扩）上撒多个起点跑 `fsolve`，去重后按 $q_e$ 连续性归并到分支（类似图像上的编号 1-12）。
3. **沿 $q_e$ 做延拓（continuation）**：对固定的初始 $q_e_0$ 先撒点求出所有根，再沿 $q_e$ 增加/减少的方向，把上一步的解作为下一步的初值（预测-校正），可高效且保分支连续地扫出整条曲线，比每个 $q_e$ 独立撒点更省算力也更不容易断支/串支。
4. **验证判据**：解出来后代回 $a_l=a_l^{(1)}+a_l^{(2)}=1/2+0=1/2$ 断言 $|a_l-1/2|<{\rm tol}$（如 1e-8），以及吸收上限 $\sigma_{{\rm abs},l}=\sigma^{\rm sa}_{{\rm abs},l}$ 交叉验证（这两条都是 Layer1/Layer2 硬约束，可直接复用 formulas.md 第六节公式）。
5. **完备性核对（对应原文线索）**：求出全部分支后，统计 ${\rm Re}(\varepsilon_i/\varepsilon_e)>0$ 与 $<0$ 的分支数，应满足"TM 和 TE 在正实部区都有多个态"且"仅 TM 在负实部区恰好一个态、TE 在负实部区零个态"——这是可以直接拿论文原文当 verifier 判据的定量线索（不需要数字化图就能用于自查）。

## 4. 与 Fig3（Case1）的联系与区别

**联系（复用部分）**：
- 完全复用同一套 Mie 系数框架：$a_l,a_l^{(1)},a_l^{(2)}$ 及球 Bessel/Hankel 函数实现（`scipy.special.spherical_jn`/`spherical_yn`），第2节和第3.1节公式无需重新推导或验证——case 0703-01 已完成 BH/Akimov 记号等价性数值验证（300 点，误差 4.7e-16），本 case 直接继承。
- 同样的坐标轴自变量 $q_e$、同样的 $l=1,2,3$、TM/TE 两偏振维度、同样的 6 面板布局逻辑。
- 同样需要数字化图上曲线做 Layer3 定量对比（沿用 Fig3 数字化方法论，但需处理 Fig6 特有的"Re/Im 分离子图"结构）。

**区别（核心差异，决定复现难度差）**：
- 极限态条件不同：Fig3 是 $a_l\in\{0,1\}$（相长/相消干涉），Fig6 是 $a_l=1/2$（电流源场消失）。
- 定义域不同：Fig3 定义在实数 $\varepsilon_i/\varepsilon_e$ 轴上，Fig6 定义在复数 $\varepsilon_i/\varepsilon_e$ 平面上。
- 数值方法不同：Fig3 用一维 brentq 切片扫描，Fig6 需要二维非线性方程组求根 + 分支延拓（详见第3节）。
- 物理可实现性不同：原文明确超辐射/非辐射态（Fig3）在真实有耗材料中不可达（只是理论上限），而超吸收态（Fig6）**可以**在真实色散有耗材料（如 Ag、Si）中实现——这也是为什么 Fig7/Fig8（真实材料吸收谱）用 $\sigma^{\rm sa}_{{\rm abs},l}$ 做上限对比，而 Fig4/Fig5（真实材料散射谱）用 $\sigma^{\rm sr}_{{\rm sca},l}$ 做上限对比。

## 5. 关键假设（复现边界，与 Case1 相同基础假设）

1. **球对称**：单个均匀介质球，半径 $R$，无涂层（本 case 与 Fig3 相同，第4节局限性修正不涉及）。
2. **线性、各向同性、均匀介质**：球内 $\varepsilon_i$（本 case 允许**复数**，与 Fig3 仅实数不同）、球外 $\varepsilon_e$（实数，无吸收）。
3. **平面波入射**：$x$-偏振、沿 $z$ 传播的 TEM 单色平面波，时谐 $e^{-{\rm i}\omega t}$。
4. **外介质无吸收**：入射球谐幅度公式仅在 ${\rm Im}\,\varepsilon_e=0$ 成立（本 case 只对 $\varepsilon_i$ 复数化，$\varepsilon_e$ 仍保持实数，与论文一致）。
5. **多极求和到收敛**：本 case 只需 $l=1,2,3$ 单阶（不涉及跨阶求和，因为是逐 $l$ 逐偏振单独求 $a_l^{(2)}=0$，不像截面公式需要 $\sum_l$）。
6. **不涉及第4节局限性修正**：$\alpha_l,\beta_l$ 修正、过渡层修正均不在本 case 范围。

## 6. 与 optics-mie-reproduction skill 的关系

- 沿用 case 0703-01 已发现的记忆事实：论文 $a_l/b_l$ 与 BH 记号数值等价（4.7e-16 误差），复现以 BH 式为主、Akimov 式交叉验证。
- 沿用求根实数化经验：**明确不适用于本 case**（case 0703-01 memory 已标注"酉性实数化仅无耗介质适用，含耗散/复 ε（如 Fig6 超吸收）不适用"）——这是本 case 必须避免踩的坑，即不能照搬 Fig3 的 brentq 一维切片代码,必须重新设计二维复数求根流程。

---

## provenance
- source_artifact: arXiv 2401.04146（Text-rev.tex §3.3 tex:L359-380）+ 本 case step01 产物（paper_text.md/formulas.md/figures.md）+ case 0703-01 已有产物（paper_understanding.md/formulas.md，交叉参考但独立核对）+ memento 记忆（decision ce6e78e3, fact 96e14ad5, decision 750b5372）
- evidence_type: 逐字文本提取 + 图像目视核对 + 跨 case 记忆交叉引用
- timestamp_version: 20260709
- scope_applicability: 本 case（0707-02）Fig6 超吸收态复现的理论理解层；不含数值验证（数值验证是 step04+ 的事）
- confidence_result_class: 高（物理框架理解，非物理复现）/ pipeline_completed
