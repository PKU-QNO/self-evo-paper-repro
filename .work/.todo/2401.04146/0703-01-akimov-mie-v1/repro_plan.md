# repro_plan.md — Akimov 2401.04146 Fig3 复现拆分计划

> 步骤：03-reproduction_design（子 agent / W-sub）
> case：0703-01-akimov-mie-v1 ｜ timestamp：20260704-01
> 物理输入：`formalization.yaml`（本计划的唯一物理 spec，代码消费 spec 不消费论文 prose）
> 目标图：**Fig3**（用户 Gate1 裁决，`GATE1-决定.md` 决定 1，不得更换）
> 状态：**spec 已备齐，待 Gate2 用户核对**（本计划不触发 gate，由 main-agent 停机呈现）

---

## 一、复现范围边界

**做**：Fig3 六面板（$l=1,2,3$ × TM/TE）超辐射（$a_l=1$，虚线）/ 非辐射（$a_l=0$，实线）loci，$(q_e,\varepsilon_i/\varepsilon_e)\in(0,10]\times[-10,15]$ 纯实平面；附带建好标准 Lorenz-Mie 核（$a_l,b_l$ + 截面）与 3 个 Layer1 verifier + benchmark 基础设施（GATE1 决定 1 明确"照常先建"）。

**显式不做**（本次范围外，记录备查）：
- Fig4/5/7/8 材料色散谱（需 Ag/Si/SiO₂ 光学常数，**不下载**——GATE1 决定 2）
- Fig6 超吸收 loci（需复 $\varepsilon$ 平面求根，候选 D，第二轮）
- Fig1/2 场分布与幅度比（非目标）
- 论文 §4 局限性修正（激发源 $\alpha_l,\beta_l$、过渡层 ODE，Fig9–12）
- COMSOL/Magnus 任何云计算

---

## 二、子任务拆分（T1→T4，串行主线 + T2 并行支线）

```
T1 (BH 主源 Mie 核) ──┬──> T2 (Akimov 式交叉验证)   [T2 不通过 = blocker，停机]
                      └──> T3 (Fig3 求根/loci 计算) ──> T4 (出图 + 数字化对比准备)
T1 完成后即可跑 Layer1 三 verifier（不依赖 T2/T3）
```

依赖：T2、T3 都只依赖 T1；T4 依赖 T3。T2 与 T3 可并行，但**建议 T2 先行**（交叉验证是 GATE1 决定 3 的 blocker 条件，早发现早停）。

### T1 — BH 主源 Lorenz-Mie 核模块

- **产出**：`reproduction_test/mie/code/scattering.py`
- **内容**：
  - Riccati-Bessel $\psi_l,\psi_l',\xi_l,\xi_l'$（scipy.special，复宗量可用，不自实现特殊函数）
  - BH 标准式 $a_l(m,x),b_l(m,x)$（spec `equations.primary_BH`）
  - 截面求和（Wiscombe 截断 $n_{max}=\lceil x+4x^{1/3}+2\rceil$）
- **接口契约（硬约束，verifier 已定死签名）**：
  - `compute_cross_sections(m, x) -> (Cext, Csca, Cabs)`
  - `compute_Q_sca(m, x)`、`compute_Q_ext(m, x)`
  - 对应 `.claude/skills/optics-mie-reproduction/scripts/check_*.py` 的既有 import 约定（`CODE_DIR = reproduction_test/mie/code`）
  - 另暴露 `mie_ab(l, m, x) -> (a_l, b_l)` 供 T2/T3 直接调用单系数
- **检验标准（量化）**：
  - Layer1.1 能量守恒：`check_energy_conservation.py` PASS（$|\sigma_{ext}-\sigma_{sca}-\sigma_{abs}|/\sigma_{ext}<10^{-10}$，4 个内置 case）
  - Layer1.2 瑞利极限：`check_rayleigh_limit.py` PASS（小 $x$ 下 $Q_{sca}\propto x^4$ 斜率判据）
  - Layer1.3 大尺寸消光佯谬：`check_large_size_limit.py` PASS（$x\to\infty$，$Q_{ext}\to2$）
  - 附加：无耗（实 $m$）时 $\sigma_{abs}=0$（机器精度，rel $<10^{-12}$）

### T2 — Akimov 式交叉验证模块

- **产出**：`reproduction_test/mie/code/akimov_coeffs.py` + 验证脚本 `crosscheck_bh_vs_akimov.py` + 结果日志
- **内容**：独立实现 Akimov (S:a_l)/(S:b_l)（spec `equations.cross_check_akimov`，显式 $q_i,q_e$ 因子形式），与 T1 的 BH 式逐点比对
- **检验标准（量化）**：
  - 网格：$l\in\{1,2,3\}$ × $\varepsilon_i/\varepsilon_e\in[-10,15]$（含负值、含 $|\varepsilon|$ 小值）× $q_e\in(0,10]$，$\geq 10^3$ 个确定性网格点 + $\geq 300$ 随机点
  - 通过：$\max|a^{BH}_l-a^{Akimov}_l|<10^{-12}$ 且 $\max|b^{BH}_l-b^{Akimov}_l|<10^{-12}$
  - **不通过 = blocker（GATE1 决定 3：两式数值不一致即停机报告，不硬跑）**
- **step03 先导证据**：本步已试算 300 随机点，max 差 $4.7\times10^{-16}$（$a_l$）/ $3.5\times10^{-16}$（$b_l$）——预期 T2 顺利通过，但正式验证仍须以脚本落盘固化

### T3 — Fig3 求根 / loci 计算

- **产出**：`reproduction_test/mie/code/fig3_loci.py` + 数据 `reproduction_test/mie/data/fig3_loci_{TM,TE}_l{1,2,3}.csv`（列：$q_e$、$\varepsilon_i/\varepsilon_e$、branch_id、type∈{sr,nr}、$|a_l-\text{target}|$ 残差）
- **方法**（spec `solver.recommended_strategy`）：固定 $q_e$ 切片 → 酉性实数化（无耗时 $|a_l|^2=\mathrm{Re}\,a_l$ ⟹ $\mathrm{Im}\,a_l=0\Leftrightarrow a_l\in\{0,1\}$，单实方程）→ $\mathrm{Im}\,a_l$ 符号翻转区间 brentq 精化 → 按 $\mathrm{Re}\,a_l$ 分类 sr/nr → 串支输出
- **检验标准（量化，Layer2 论文内自洽）**：
  - 每个 sr 根：$|a_l-1|<10^{-8}$，且单通道截面 $\sigma_{sca,l}/(\pi R^2)=2(2l+1)/q_e^2$（rel err $<10^{-8}$）、$\sigma_{abs,l}=0$
  - 每个 nr 根：$|a_l|<10^{-8}$，且 $\sigma_{sca,l}/(\pi R^2)<10^{-16}$
  - 平凡线核对：$\varepsilon_i/\varepsilon_e=1$ 时 $|a_l|,|b_l|<10^{-14}$（任取 20 个 $q_e$ 抽查）
  - 完备性：备选二维 contour 图（spec `solver.fallback_strategy`）与切片法曲线族支数一致（目测 + 支数计数），防漏根
- **step03 先导证据**：$l=1$ TM、$q_e=1$ 切片试算找到 sr 根 $\varepsilon\approx-4.640$（残差 $5\times10^{-16}$），与 Fig3 面板 1 红虚线低谷位置（$\approx-5$ @ $q_e\approx1.2$）一致

### T4 — 出图 + 数字化对比准备

- **产出**：`reproduction_test/mie/figures/fig3_repro.png`（六面板，轴范围/线型/颜色约定同原图）+ 叠图 `fig3_overlay.png`（复现曲线叠在 `figs/Fig3.png` 数字化点上）+ 对比数据准备说明
- **步骤**：
  1. 用 T3 CSV 画六面板复现图（红虚=sr，蓝实=nr，横 $[0,10]$ 纵 $[-10,15]$）
  2. 数字化原图 Fig3（`pdf` skill 的图数字化流程；矢量源 `01-pdf_preprocessing/src/Fig3-eps-converted-to.pdf` 优先于 png，取样密度每条曲线 $\geq 15$ 点）——单点小活，可 spawn sub-leaf
  3. 计算对比指标（step08 正式执行，本任务准备好数据与脚本接口）
- **检验标准（量化，Layer3 建议阈值，最终待 Gate2/用户认可）**：
  - 指标：每个数字化取样点到同面板同类型（sr/nr）复现曲线族的最近距离，归一化（$q_e$ 方向 /10，$\varepsilon$ 方向 /25）
  - 建议通过阈值：中位归一化距离 $<0.01$（约轴范围 1%，数字化误差量级）且 95 分位 $<0.03$；曲线族支数逐面板一致
  - 该阈值无文献先例（loci 图对比），列入 Gate2 呈现事项

---

## 三、验证层次映射（哪个检验对应哪层）

| 层 | 检验 | 所在任务 | 判据 |
|----|------|---------|------|
| Layer1.1 能量守恒 | `check_energy_conservation.py` | T1 | rel err $<10^{-10}$，PASS/FAIL 脚本判 |
| Layer1.2 瑞利极限 | `check_rayleigh_limit.py` | T1 | $Q_{sca}\propto x^4$ 斜率 |
| Layer1.3 大尺寸极限 | `check_large_size_limit.py` | T1 | $Q_{ext}\to2$ |
| Layer2 自洽 A | sr 根处 $\sigma_{sca,l}/(\pi R^2)=2(2l+1)/q_e^2$、$\sigma_{abs,l}=0$ | T3 | rel err $<10^{-8}$ |
| Layer2 自洽 B | nr 根处 $\sigma_{sca,l}=0$ | T3 | $<10^{-16}$（归一化） |
| Layer2 自洽 C | 两式交叉一致（BH vs Akimov） | T2 | $<10^{-12}$，**失败即 blocker** |
| Layer3 图对比 | Fig3 数字化 loci 位置 vs 复现曲线族 | T4→step08 | 归一化距离中位 $<0.01$（建议值，待用户认可） |

**result_class 路径**：T1–T4 全跑完且 Layer1/2 过 = `simulation_completed`→物理判断后最高 `partial_physical_match`；`physical_reproduction_success` 还需 Layer3 量化过 + human gate，本计划任何任务无权自行声明。

---

## 四、决策问题回答（供 main-agent 拍板）

1. **整篇还是单图？** 单图 Fig3 + Lorenz-Mie 核基础设施（用户 Gate1 已裁决）。范围边界见本文第一节"显式不做"清单：材料色散谱（Fig4/5/7/8）、超吸收（Fig6）、§4 修正（Fig9–12）、场分布（Fig1/2）均不在本次范围。
2. **拆几个子任务？** 4 个：T1 BH 核 → {T2 交叉验证, T3 求根} → T4 出图对比。T2/T3 均只依赖 T1；建议 T2 先于 T3 完成（blocker 早发现）。
3. **检验标准？** 全部量化，见第二、三节：Layer1 三脚本 PASS（阈值内置）；T2 两式 $<10^{-12}$；T3 根残差 $<10^{-8}$ + 超辐射截面恒等式 rel $<10^{-8}$；Layer3 归一化距离中位 $<0.01$（建议，待认可）。
4. **需不需要数值计算脚本？** 需要——"解析求根"的准确含义：$a_l$ 有解析闭式（不解 PDE、不用 FEM），但 $a_l=1/0$ 的 loci 是超越方程的根，无闭式解，须数值求根（brentq 一维括号法）。即"解析公式 + 数值求根脚本"，Python 本地。
5. **需不需要 Magnus 云计算？** 不需要。全部计算为标量特殊函数求值 + 一维求根，估算 $800\times4000$ 网格 × 6 面板在本地单核秒级~分钟级。零 COMSOL、零 HPC。

---

## 五、风险与 uncertainty

| 风险 | 等级 | 缓解 |
|------|------|------|
| 负 $\varepsilon$ 域 $\psi_l(q_i)$ 指数增长溢出 | 低 | step03 已核角点 $l=3,\varepsilon=-10,q_e=10$：$|N|\sim5\times10^{14}$，float64 安全；若扩域需重标度 |
| 曲线密集区（$q_e\to10$、$\varepsilon\to1^+$）漏根 | 中 | 密网格 + 备选 contour 完备性核对（T3 判据）；$\varepsilon$ 网格在 $[0,3]$ 加密 |
| brentq 括到极点（$D=0$ 的伪翻转） | 中 | 根处断言 $|a_l-\text{target}|<10^{-8}$，失败即丢弃并记日志（spec solver 第 4 条） |
| Layer3 阈值无先例 | 中 | 建议值列 Gate2 呈现，用户认可后生效；不自行放宽 |
| 数字化误差 | 低 | 用矢量 PDF 源数字化优先于 png |

---

## provenance

- source_artifact：`formalization.yaml`（本步）+ GATE1-决定.md + step01/02 产物 + `.claude/skills/optics-mie-reproduction/scripts/check_*.py`（接口契约实读核对）+ step03 数值预验证
- evidence_type：spec 设计 + verifier 源码核对 + 300 随机点等价性试算 + 单切片求根试算
- timestamp_version：20260704-01
- scope_applicability：仅本 case Fig3 复现的任务拆分；T1 核模块与 Layer1 verifier 可复用于后续 Mie 论文
- confidence_result_class：高（设计与先导验证）/ pipeline_completed
