# 缺失信息清单 — Akimov 2401.04146

> 步骤：02-paper_reading（子 agent / W-sub）
> case：0703-01-akimov-mie-v1 ｜ timestamp：20260703-2236
> 原则：缺失明确列，不假装有；本步**不下载材料数据**，只标 pending。

---

## 1. 已确认缺失 / 与原计划不符

| # | 缺失项 | 影响 | 能否补 / 怎么补 | 阻塞级别 |
|---|--------|------|----------------|---------|
| 1 | **本论文无经典 $Q_{\rm ext}(x)$ vs 尺寸参数曲线**（Rayleigh→Mie→几何光学过渡那张） | 原计划 step08 目标图不存在；main-agent 已把选图上抛用户 | 改用候选 A/B/C/D（本论文实有的图），或若坚持要经典过渡曲线则另选论文/教材（BH 图）。**这不是数据缺失，是计划与论文不符** | 非阻塞（已上抛用户，等选定路线） |
| 2 | skill `optics-mie-reproduction/references/papers.md` 对本文的描述**过时**：写着 "observe smooth transition across Rayleigh/Mie/geometric-optics"、输出 "$Q_{sca}(x)$ curve for n=1.5,2,3,4"——本文并无此内容 | 若后续 step 照 papers.md 预期搭模型会跑偏 | 建议 evolution 阶段修正 papers.md Stage1 描述（本步只记录，不改 skill） | 非阻塞（提示 main-agent，记入 toEflow 候选） |

## 2. 材料数据缺失（候选 B/C，pending，本步不下载）

| # | 缺失项 | 影响 | 能否补 | 阻塞级别 |
|---|--------|------|--------|---------|
| 3 | Ag、Si、SiO2 的 $\varepsilon(\omega)$ 数值论文未提供 | 候选 B(Fig4)/C(Fig5) 谱计算所需 | 能补：Ag=Johnson&Christy 1972 / Si=Aspnes 1983 或 Green / SiO2=Malitson 1965；或 refractiveindex.info。**待用户选定候选后由后续 step 搜，避免白干** | 非阻塞（候选 A 不需要；B/C 选定后再搜） |
| 4 | **作者所用色散数据源**未注明 | 候选 B/C 的 Layer3 定量吻合度可能受色散源差异影响（峰位偏几十 meV） | 部分可补：选定候选后，用标准源试算并对峰位；若系统偏移可反推作者源。属 uncertainty 非硬缺失 | 非阻塞 |

## 3. 公式/实现细节缺失（可从教材/库补，非阻塞）

| # | 缺失项 | 影响 | 能否补 | 阻塞级别 |
|---|--------|------|--------|---------|
| 5 | 论文未显式给 $\psi_l',\xi_l'$ 的递推式 | step06 实现 Mie 系数需导数 | 能补：`scipy.special.spherical_jn(l,q,derivative=True)`，或 BH 附录递推 $\psi_l'(q)=\psi_{l-1}(q)-\frac{l}{q}\psi_l(q)$（`trust` 教材惯例） | 非阻塞 |
| 6 | 论文未给数值多极截断 $n_{max}$ | 谱求和收敛判据 | 能补：Wiscombe $n_{max}\approx x+4x^{1/3}+2$（`trust` scipy/BH 惯例）；论文实际只用到 $l=1,2,3$ | 非阻塞 |
| 7 | 本文 $a_l/b_l$ 代数形式与 BH 不同（分子分母带显式 $q_i,q_e$ 因子），$\psi_l',\xi_l'$ 对宗量求导约定需对齐 | step06 交叉验证时若约定不齐会数值不符 | 能补：以 BH 标准式为主、本文式交叉验证（papers.md Caveat 已提醒 Akimov 综述可能有 typo，须对 BH/Kerker 核） | 非阻塞（step06 重点核对项） |

## 4. 阶段1范围外（论文有但阶段1不复现，记录备查）

| # | 项 | 说明 |
|---|----|------|
| 8 | §4.1 激发源修正参数 $\alpha_l,\beta_l$（Fig9/10） | 论文未给具体扫描数值；需外部激发建模。非阶段1 |
| 9 | §4.2 过渡层 $\varepsilon(r)$ 分布、$\Delta R$、$\tilde Z_l/\tilde Y_l$ ODE（Fig11/12） | 需过渡层 ODE 积分 + 厚度扫描。非阶段1 |
| 10 | Fig6 超吸收态需复 $\varepsilon_i/\varepsilon_e$ 平面优化（复根） | 候选 D 若选中需复根求解器，比 Fig3 稍难。记录备查 |

## 5. 需人工/外部才能拿的信息

| # | 项 | 判断 |
|---|----|------|
| 11 | GUI 模板 / COMSOL image | **不需要**。阶段1纯解析，不涉及 COMSOL/Magnus |
| 12 | 实验数据 | **不需要**。本文为纯理论/分析论文，无实验 |
| 13 | 作者私聊（材料色散源） | 非必需。标准光学常数库可替代，仅影响吻合度精度（见 #4） |

---

## 总结判断

- **无硬阻塞**：通用核参数（尺寸参数、Mie 系数公式、截面公式、极限态判据）齐全，公式来源明确（§2–§3 + BH 补递推）。
- **唯一"缺"是材料色散数据**（候选 B/C），且明确可从标准源补，本步按指令**不下载**，标 pending 等用户选定候选。
- **候选 A(Fig3) 零缺失**：可立即进入后续 step 而无需任何外部数据。
- 计划层面的偏差（无 $Q_{\rm ext}(x)$ 曲线、papers.md 描述过时）已上抛，等 main-agent + 用户拍板选图。

## provenance
- source_artifact：arXiv 2401.04146（Text-rev.tex tex:L83/L314/L339/L395）+ step01 产物 + optics-mie-reproduction/references/papers.md（发现过时描述）
- evidence_type：论文原文核对 + skill 文件比对
- timestamp_version：20260703-2236
- scope_applicability：阶段1单球经典 Mie 复现的输入完备性判断
- confidence_result_class：高 / pipeline_completed
