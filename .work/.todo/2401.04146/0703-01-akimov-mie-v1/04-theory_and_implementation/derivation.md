# derivation.md — step04 T1+T2 BH 式推导核对 + Akimov 等价 + verifier 结果

> case: 0703-01-akimov-mie-v1 ｜ timestamp: 20260704-01 ｜ 步骤: 04-theory_and_implementation（T1+T2）
> 公式主源: Bohren & Huffman 教材（`.paper/scattering.pdf`）§4.3/§4.4；本 case 物理 spec = `formalization.yaml` `equations.primary_BH`。
> 本文件供 **Gate3 用户对教材核对** $a_l, b_l$ 公式、记号、导数约定。原始 stdout 见同目录 `verifier_log.txt`。

---

## 一、记号与约定（Gate3 核对第一优先）

| 符号 | 定义 | 说明 |
|------|------|------|
| $x$ | $x = q_e = k_e R$ | 外部尺寸参数，实正数（verifier 传入） |
| $m$ | $m = \sqrt{\varepsilon_i/\varepsilon_e}$ | 相对折射率；$\varepsilon$ 比为负时 $m$ 纯虚，取主值 $\mathrm{Im}\,m \ge 0$ |
| $mx$ | $mx = q_i = m x$ | 内部宗量，$m$ 复时为复数 |
| $\psi_l(z)$ | $\psi_l(z) = z\, j_l(z)$ | Riccati-Bessel（第一类），$j_l$ = 球 Bessel |
| $\chi_l(z)$ | $\chi_l(z) = -z\, y_l(z)$ | $y_l$ = 球 Neumann |
| $\xi_l(z)$ | $\xi_l(z) = z\, h_l^{(1)}(z) = \psi_l(z) - i\chi_l(z)$ | $h_l^{(1)} = j_l + i y_l$ |
| $'$ | $\dfrac{d}{dz}$ | **对宗量求导**（不是对 $r$ 求导） |

**时谐约定**：$e^{-i\omega t}$。散射场用 $h_l^{(1)}$（外向辐射）。BH 教材、Akimov 论文均为 $e^{-i\omega t}$，两源约定一致，**无需符号翻转**（见 `formalization.yaml` assumptions 第 5 条）。

**导数实现**（核对要点）：代码用 `scipy.special.spherical_jn(l, z, derivative=True)` 给 $j_l'(z)$，再由链式法则组合：
$$\psi_l'(z) = \frac{d}{dz}\big[z\,j_l(z)\big] = j_l(z) + z\, j_l'(z)$$
$$\xi_l'(z) = h_l^{(1)}(z) + z\, {h_l^{(1)}}'(z),\quad h_l^{(1)} = j_l + i y_l$$
已用中心差分独立核对：$z=2.3+0.4i,\ l=2$ 时解析 $\psi_l'$ 与数值差分差 $1.4\times10^{-10}$（差分步长 $10^{-6}$，符合二阶精度），导数约定正确。

---

## 二、BH 主源 $a_l, b_l$ 公式（`scattering.mie_ab`，Gate3 对教材核对）

`formalization.yaml` `equations.primary_BH`，代码逐字实现：

$$a_l = \frac{m\,\psi_l(mx)\,\psi_l'(x) - \psi_l(x)\,\psi_l'(mx)}{m\,\psi_l(mx)\,\xi_l'(x) - \xi_l(x)\,\psi_l'(mx)}$$

$$b_l = \frac{\psi_l(mx)\,\psi_l'(x) - m\,\psi_l(x)\,\psi_l'(mx)}{\psi_l(mx)\,\xi_l'(x) - m\,\xi_l(x)\,\psi_l'(mx)}$$

对应 BH (1983) 式 (4.53)（$a_n$，TM/电多极）与 (4.54)（$b_n$，TE/磁多极），非磁性 $\mu = \mu_0$ 特例（BH 一般式中 $\mu_1/\mu = 1$）。`notation_map`：BH $a_n \leftrightarrow$ Akimov $a_l$（电），BH $b_n \leftrightarrow$ Akimov $b_l$（磁）。

**截面（光学定理，`equations.cross_sections`）**：
$$Q_{sca} = \frac{2}{x^2}\sum_l (2l+1)\big(|a_l|^2 + |b_l|^2\big),\quad Q_{ext} = \frac{2}{x^2}\sum_l (2l+1)\,\mathrm{Re}(a_l + b_l),\quad Q_{abs} = Q_{ext} - Q_{sca}$$
因 Fig3 无量纲化，$\pi R^2$ 因子约掉，代码令 $C = Q$（`compute_cross_sections` 三返回值共用同一套 $a_l, b_l$ 与同一归一，故 $C_{ext} = C_{sca} + C_{abs}$ 解析恒等）。

**截断**：Wiscombe $n_{max} = \lceil x + 4x^{1/3} + 2\rceil$（trust 来源：Wiscombe 1980 教材/库惯例，**非论文原文**，代码注释已标）。

---

## 三、Akimov 式独立实现与等价（T2）

`akimov_coeffs.akimov_ab`，`formalization.yaml` `equations.cross_check_akimov`（显式 $q_i, q_e$ 因子）：

$$a_l = \frac{q_i\,\psi_l(q_i)\,\psi_l'(q_e) - q_e\,\psi_l(q_e)\,\psi_l'(q_i)}{q_i\,\psi_l(q_i)\,\xi_l'(q_e) - q_e\,\xi_l(q_e)\,\psi_l'(q_i)}$$

$$b_l = \frac{q_e\,\psi_l(q_i)\,\psi_l'(q_e) - q_i\,\psi_l(q_e)\,\psi_l'(q_i)}{q_e\,\psi_l(q_i)\,\xi_l'(q_e) - q_i\,\xi_l(q_e)\,\psi_l'(q_i)}$$

其中 $q_e = x$，$q_i = mx$。

**等价性（解析）**：$a_l$ 分子分母同提公因子 $q_e$，并用 $q_i = m q_e$：分子 $= q_e[m\,\psi_l(q_i)\psi_l'(q_e) - \psi_l(q_e)\psi_l'(q_i)]$，分母 $= q_e[m\,\psi_l(q_i)\xi_l'(q_e) - \xi_l(q_e)\psi_l'(q_i)]$，$q_e$ 约去即得 BH $a_l$。$b_l$ 同理。**形式差异来源**：链式法则 $d/dr = k\cdot d/dq$ 的 $k$ 因子被 Akimov 式显式保留、BH 式吸收进 $m$。

**独立性保证**：`akimov_coeffs.py` 有自己的 `_psi/_xi` 求值路径，**不 import** `scattering.mie_ab`（否则交叉验证失去意义）。两模块只共用 scipy 底层特殊函数（合理的共同信赖基）。

**T2 逐点比对结果**（`crosscheck_bh_vs_akimov.py`，原始 stdout 见 verifier_log.txt）：

| 网格 | 点数（要求） | max$|\Delta a|$ | max$|\Delta b|$ | 极点跳过 |
|------|------|------|------|------|
| 确定性 | 3000（≥1000） | $2.221\times10^{-15}$ | $4.408\times10^{-16}$ | 0 |
| 随机（seed=20260704） | 300（≥300） | $4.775\times10^{-16}$ | $4.775\times10^{-16}$ | 0 |
| **合计** | 3300 | $\mathbf{2.221\times10^{-15}}$ | $\mathbf{4.775\times10^{-16}}$ | **0** |

判据 $<10^{-12}$，实测 $\le 2.2\times10^{-15}$（机器精度量级），**PASS**。0 个极点跳过（`|den| < 10^{-9}` 阈值下确定性/随机网格均未命中 loci 分母零点）。**T2 blocker 解除**（与 step03 预验证 $4.7\times10^{-16}$ 量级一致，本步脚本已正式固化落盘，未拿预验证顶）。

---

## 四、Layer1 三 verifier 结果（原始 stdout 见 verifier_log.txt）

| verifier | 判据 | 实测 | 结果 |
|----------|------|------|------|
| `check_energy_conservation.py`（1.1） | $|C_{ext}-C_{sca}-C_{abs}|/C_{ext} < 10^{-10}$，4 case | max rel err $= 0.000\times10^{0}$ | **PASS** |
| `check_rayleigh_limit.py`（1.2） | $Q_{sca}\propto x^4$，斜率 $=4.0\pm0.01$ | 拟合斜率 $= 4.0001$ | **PASS** |
| `check_large_size_limit.py`（1.3） | $|Q_{ext}-2| < 0.05$，$x\in\{50,80,120,200\}$ | max $|Q_{ext}-2| = 0.1711$ @ $x=50$ | **FAIL** |

**附加自测**：实 $m=1.5+0i$、$x=1$ 时 $C_{abs} = -2.78\times10^{-17}$，$|C_{abs}|/C_{ext} = 1.29\times10^{-16}$（机器精度），无耗吸收为 0 —— 符合 spec `lossless_unitarity`。

**能量守恒 max rel err = 0（严格）** 是对 $a_l, b_l$ 酉性的强验证：$Q_{abs} = Q_{ext} - Q_{sca}$ 定义式恒等在数值上完全成立。

---

## 五、大尺寸 verifier FAIL 根因诊断（重点，供 Gate3 裁决）

**结论：非 `scattering.py` 实现错误，疑似 verifier 阈值/采样点设计不当。** 三条证据（本步独立复跑确认）：

### 证据 1 — 谱求和已收敛（截断充分，非截断不足）
$x=50$ 处把 $n_{max}$ 从 Wiscombe 值 67 强行加到 97、147，$Q_{ext}$ 恒为 $2.171073$ 不变：

| $x=50$，$n_{max}$ | 67（Wiscombe） | 97 | 147 |
|------|------|------|------|
| $Q_{ext}$ | 2.171073 | 2.171073 | 2.171073 |

→ 加 80 阶高阶项 $Q_{ext}$ 不动，求和完全收敛，$2.171$ 是真实物理值，不是漏项。

### 证据 2 — 独立算法交叉验证（排除 scipy 路径 bug）
用完全独立的 Wiscombe 对数导数下行递推 $D_n$（不经 scipy `spherical_jn`，自算 $\psi/\chi$ 上行递推）复算：$x=50$ 两法 $Q_{ext}$ 均 $= 2.17107$（逐系数 max$|\Delta a|\sim6\times10^{-7}$，随 $x$ 增大略升属大宗量特殊函数常态，不影响 $Q_{ext}$ 到 5 位一致）。→ 系数正确。

### 证据 3 — $Q_{ext}$ 随 $x$ 单调整体趋 2，但收敛慢（消光佯谬渐近极限 + Mie ripple）

| $x$ | 50 | 80 | 120 | 200 | 500 | 1000 | 2000 |
|-----|----|----|----|-----|-----|------|------|
| $Q_{ext}$ | 2.1711 | 2.1617 | 2.0447 | 2.0921 | 2.0426 | 2.0139 | 2.0099 |
| $|Q_{ext}-2|$ | 0.1711 | 0.1617 | 0.0447 | 0.0921 | 0.0426 | 0.0139 | 0.0099 |

物理解释：大尺寸消光佯谬 $Q_{ext}\to2$ 是 $x\to\infty$ **渐近极限**；无损介质球（实 $m=1.5$，无吸收）收敛慢，且叠加真实 Mie 干涉振荡（extinction ripple / 边缘波 + 内部干涉）。要 $x\gtrsim1000$ 才稳定 $<0.05$。verifier 采样点 $\{50,80,120,200\}$ 恰落在 ripple 未衰减区（$0.04\sim0.17$），$tol=0.05$ 卡在振荡幅度内 → FAIL 属采样/阈值与被测物理量特性不匹配，非实现错。

**注意非单调**：$x=120$（0.0447）比 $x=80$（0.1617）小、又比 $x=200$（0.0921）小，正是 ripple 振荡的特征（不是单调衰减），进一步印证是干涉振荡而非收敛残差。

**我无权改 verifier**（`check_large_size_limit.py` 在 `.claude/skills/` 下，改阈值/采样点是 human gate 决定）。仅诊断如实报告，交 Gate3。可选处理（供用户裁决）：(a) 放宽 tol 到覆盖 ripple；(b) 采样点移到 $x\gtrsim1000$；(c) 改用带小吸收的阻尼介质（ripple 被 damping 压平，$Q_{ext}\to2$ 快）；(d) 接受 FAIL 记为已知 verifier 局限。

---

## 六、result_class 与不确定性

- **本步 result_class = `diagnostic_only`**（机械规则：Layer1 任一 FAIL → $\le$ `diagnostic_only`，不论根因）。不向上包装为 `simulation_completed`。
- **uncertainty**：大尺寸 FAIL 根因诊断置信度高（三条独立证据），但"verifier 设计不当"的最终定性是 human gate 权限，非本 agent 定论。
- **missing_evidence**：无第三方参考库（miepython 本机未装）做绝对基准比对；已用「独立 Wiscombe 递推 + 解析 Rayleigh 振幅（$x=0.01$ 相对差 $7\times10^{-6}$）+ 能量守恒严格 0」三重内证替代，足以支撑"系数正确"。

## provenance
```yaml
provenance:
  source_artifact: "formalization.yaml equations.primary_BH/cross_check_akimov + BH 教材 §4.3 + scattering.py/akimov_coeffs.py/crosscheck_bh_vs_akimov.py (step04, timestamp 20260704-01)"
  evidence_type: "verifier 原始 stdout（3 Layer1 + T2 crosscheck）+ 独立 Wiscombe 递推交叉验证 + 解析 Rayleigh 振幅核对 + 导数中心差分核对"
  timestamp_version: "20260704-01"
  scope_applicability: "单球经典 Lorenz-Mie 核（纯实或复 m，含负 eps 比纯虚 m）；大尺寸诊断限无损介质 m=1.5；不适用含强色散/多层/超吸收"
  confidence_result_class: "高（数值证据充分）/ diagnostic_only（Layer1 大尺寸 FAIL 封顶）"
```
