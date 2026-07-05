# step05 对抗式审查报告 — theory_check.md

> case: `0703-01-akimov-mie-v1` | step05 theory_check | timestamp: 20260705-01
> 被审：`reproduction_test/mie/code/scattering.py`（BH 主源核）+ `akimov_coeffs.py`（Akimov 独立实现）
> 证据源：本目录 `adversarial_probes.py` / `adversarial_probes.txt`（8 探针原始 stdout）+ `.paper/scattering.pdf`（BH 教材）+ derivation.md + formalization.yaml
> 审查立场：**默认怀疑代码有错，逐条证伪**。verifier PASS 不作为符号正确的充分证据。
>
> **落盘说明**：本审查由 sub-agent(step05) 执行探针脚本（已落盘 `adversarial_probes.{py,txt}`），文档汇总因 sub 连续两步在文档阶段截断，由 main-agent 依据探针原始 stdout 汇总（编排层汇总职责，非隔离计算活；探针数值均来自 sub 落盘的 stdout，未二次运行）。

---

## 结论速览

| 审查维度 | 结论 | 关键证据 |
|----------|------|----------|
| 1. BH 式分子/分母逐项 | ✅ 与 spec/教材一致 | 逐项比对 §1；三 verifier + T2 数值佐证 |
| 2. 符号 / 时谐约定 | ✅ $\xi_l=+iy$、$e^{-i\omega t}$ 正确 | P1（Rayleigh 对教材 Im 同号）+ P7（符号注入对照） |
| 3. 负 ε 域 m 纯虚分支 | ✅ 数值可用，且分支无关 | P2/P3/P8（偶函数，两分支等价） |
| 4. T2 独立性 | ✅ 真独立（非复制粘贴） | P5（AST 解析无 import + 三路径一致） |
| 5. 截面/守恒 | ✅ 解析恒等 | energy verifier 机器零；§5 |
| 6. 边界/极点 | ✅ graceful（无静默错值） | P4/P6 |
| **是否发现 bug** | **无实质 bug，代码未改** | git status 干净；仅 1 条非 bug 观察（§7） |
| **result_class** | `simulation_completed`（维持上游，审查加固） | — |

---

## 1. BH 式分子/分母逐项核对（维度 1）

`scattering.py::mie_ab` 实现（第 93-99 行）：
```
a_num = m * psi_mx * psip_x - psi_x * psip_mx
a_den = m * psi_mx * xip_x - xi_x * psip_mx
b_num = psi_mx * psip_x - m * psi_x * psip_mx
b_den = psi_mx * xip_x - m * xi_x * psip_mx
```
对照 formalization.yaml `equations.primary_BH` / derivation.md §2：
$$a_l = \frac{m\,\psi_l(mx)\,\psi_l'(x) - \psi_l(x)\,\psi_l'(mx)}{m\,\psi_l(mx)\,\xi_l'(x) - \xi_l(x)\,\psi_l'(mx)},\quad b_l = \frac{\psi_l(mx)\,\psi_l'(x) - m\,\psi_l(x)\,\psi_l'(mx)}{\psi_l(mx)\,\xi_l'(x) - m\,\xi_l(x)\,\psi_l'(mx)}$$

**逐项对应**（psi_mx=$\psi_l(mx)$, psip_x=$\psi_l'(x)$, xi_x=$\xi_l(x)$, xip_x=$\xi_l'(x)$）：
- a_num：$m\psi_l(mx)\psi_l'(x)-\psi_l(x)\psi_l'(mx)$ ✓（m 因子在 $\psi_l(mx)\psi_l'(x)$ 项，正确）
- a_den：$m\psi_l(mx)\xi_l'(x)-\xi_l(x)\psi_l'(mx)$ ✓
- b_num：$\psi_l(mx)\psi_l'(x)-m\psi_l(x)\psi_l'(mx)$ ✓（m 因子在第二项，与 a 互换，正确）
- b_den：$\psi_l(mx)\xi_l'(x)-m\xi_l(x)\psi_l'(mx)$ ✓

**a 与 b 的 m 因子位置正好互换**（BH 电/磁对偶的标志），代码正确体现。无系数/符号/m 因子错位。

**Riccati-Bessel（第 41-68 行）**：$\psi_l'(z)=j_l(z)+z j_l'(z)$（链式法则，`psip = jl + z*jlp`）✓；$\xi_l=z(j_l+iy_l)$、$\xi_l'=h_1+z h_1'$ ✓。`derivative=True` 给的是 $j_l'(z)$（对宗量），代码无漏乘/多乘。

---

## 2. 符号与时谐约定（维度 2，双向归因）

**核心方法**：不靠 verifier PASS 反推符号（两式同错也会同过），而用**已知解析 Rayleigh 极限**独立对教材核。

**P1（探针）**：BH 1983 式 4.56/4.57，$e^{-i\omega t}$ 约定下 $a_1\to -i\frac{2}{3}x^3\frac{m^2-1}{m^2+2}$（纯虚，负虚部）。实测：

| m, x | code $a_1$ | 教材 $a_1$ | rel | Im 同号 |
|------|-----------|-----------|-----|---------|
| 1.5, 0.01 | 3.8e-14 − 1.9608e-7j | −1.9608e-7j | 3.5e-6 | ✓ |
| 2.0, 0.01 | 1.1e-13 − 3.3334e-7j | −3.3333e-7j | 2.0e-5 | ✓ |
| 1.2, 0.02 | 4.7e-13 − 6.8214e-7j | −6.8217e-7j | 3.9e-5 | ✓ |

rel 在 $x^2$ 高阶修正量级、**Im 同号（负）** → $\xi_l$ 用 $+iy_l$、时谐 $e^{-i\omega t}$ 正确。

**P7（符号注入对照）**：人为构造 $h=j-iy$ 错误分支，$a_1$ 的 Im 翻正号；`code == +iy 分支` 逐位一致、`code == conj(−iy 分支)`。**证明**：若代码误用 $-iy$，Rayleigh 符号会反，可鉴别；实测代码用正确分支。

**决策问题 2 答**：verifier PASS **不能**反推符号对——因 T2（BH vs Akimov）两式若同用错符号会同过，energy/rayleigh 只看模长/标度不看相位符号。必须如 P1/P7 用教材解析式独立核。结论：符号正确。

---

## 3. 负 ε 域 m 纯虚分支（维度 3，Fig3 核心域）

**P2**：ε=−10, q_e=10, l=3，$m=\sqrt{-10}$ 两分支 = ±3.1623j。主值 Im m≥0 时 $mx=+31.6j$，$\psi_3(mx)=2.23\text{e}13$（有限）。

**P8（关键发现）**：解析上 $\psi_l(-z)=(-1)^{l+1}\psi_l(z)$、$\psi_l'(-z)=(-1)^l\psi_l'(z)$，代入 $a_l$ 分子分母各出 $(-1)^l$ 公因子约掉 ⟹ **$a_l(-m)=a_l(m)$，$a_l,b_l$ 是 $m$ 的偶函数**。实测 max|系数(+m)−系数(−m)|=**1.76e-16**（机器零）。

**推论**：负 ε 域 sqrt 主值 vs 负分支**给同一系数值**，spec 顾虑的"分支取错发散"在 Fig3 域内**不成立**——真溢出仅当 $|\mathrm{Im}(mx)|>\sim700$（float64 $e^{700}$ 溢出），而 Fig3 域 $|\mathrm{Im}(mx)|<40$，远未触及。

**P3 角点**：l=3,ε=−10,q_e=10 → a=0.572+0.495j、b=0.395−0.489j，finite，|a−a_akimov|=1.1e-16；raw |$\psi_3(mx)$|=2.23e13 ≪ float64 max 1.8e308。**负 ε 域数值可用。**

**决策问题 3 答**：分支取值正确且**分支无关**（偶函数）；角点系数 O(1)、数值稳定；两 sqrt 分支均有限且给同值。

---

## 4. T2 独立性判定（维度 4，防"同一 bug 复制两份"）

**P5（AST 解析，非读 docstring）**：对 `akimov_coeffs.py` 做 AST 解析真实 import 语句：
```
[('from','__future__',['annotations']), ('from','scipy.special',['spherical_jn','spherical_yn'])]
真实 import 依赖 scattering? False    真实代码调用 mie_ab? False
```
+ 三条独立路径交叉：BH（scattering）/ Akimov 显式 q_i,q_e 因子 / 第三形式 $\xi=\psi-i\chi$，三者两两一致（|BH−Ak|≤5.6e-17、|BH−3rd|=0）。

**决策问题 4 答**：**T2 是有效独立验证，非伪独立**。akimov_coeffs 用自己的 `_psi/_xi`，不 import 也不调 scattering 的函数，只共用 scipy 底层特殊函数（合理共同信赖基）。第三条路径进一步加固。T2 的 max|Δa|=2.2e-15 是真独立公式等价，非同 bug 复制。

---

## 5. 截面与守恒（维度 5）

`_qsca_qext`（第 114-131 行）：$Q_{sca}=\frac{2}{x^2}\sum(2l+1)(|a_l|^2+|b_l|^2)$、$Q_{ext}=\frac{2}{x^2}\sum(2l+1)\mathrm{Re}(a_l+b_l)$，共用同套 a_l,b_l + 同一归一 $2/x^2$。`compute_cross_sections` 令 $Q_{abs}=Q_{ext}-Q_{sca}$ **解析恒等**（同一组求和相减），故 energy verifier 得 max rel err 0.000e+00（机器零），非数值巧合。Wiscombe $n_{max}=\lceil x+4x^{1/3}+2\rceil$：x=800 给 nmax≈840，大尺寸趋势 verifier 末点已收敛（|Q−2|=0.0163）。

---

## 6. 边界/极点行为（维度 6）

**P4**：极点扫描 l=1 TM，最小 |a_den|=1.87e-3 @ ε=−2.025,q_e=0.094，该点 a_1=0.186−0.389j（|a|=0.43，O(1) 正常）——**未出现"异常小分母配异常大 |a|"的静默错值**。真退化输入 m=0j → nan（graceful，可接受；开头两行 RuntimeWarning 即此探针触发，非代码 bug）。

**P6**：大 l（远超 Wiscombe nmax）：x=5,nmax=14，l=14→a~1e-11、l=54→a~1e-100、l=94→a→0（underflow），**全程 finite，收敛区内无 inf/nan**。高阶 evanescent 正确趋零。

---

## 7. 唯一观察（非 bug）

`_refractive_index(m)` 只做 `complex(m)` 收敛，不做 sqrt——即代码**直接消费上游传入的 m**，sqrt 分支选择留给上游（crosscheck/step06 solver）。由 P8 偶函数结论，此设计**无风险**（分支无关）。但需给 step06 的提醒：Fig3 求根从 ε 比算 m 时，用 `np.sqrt`（返回主值 Im≥0）即可，无需特意处理分支——已由偶函数保证等价。此为**注意事项非缺陷**，记入 memento 供 step06 用。

---

## 8. result_class 与遗留

- **未发现实质 bug**，`scattering.py`/`akimov_coeffs.py` 功能**未改**（git status 干净）。
- 尝试的证伪路径（全部未推翻代码）：Rayleigh 符号对教材核（P1）、符号翻转注入（P7）、负 ε 双分支（P2）、偶函数对称（P8）、角点溢出（P3）、极点静默错值（P4）、大 l 发散（P6）、AST 伪独立（P5）。
- **result_class = `simulation_completed`**：审查步不产新物理声明，维持 step04 经 Gate3 升级的上游结论；审查加固了对负 ε 域与 T2 独立性的信心。物理复现成功仍需 Layer3（step08 论文图量化 + Gate4）。
- 无 blocker。下一步 step06（Fig3 求根 T3）可进行。
