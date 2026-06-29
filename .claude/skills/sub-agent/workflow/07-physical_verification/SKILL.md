# 07-physical_verification（子 agent 视角）

## 具体怎么干

### 3 层检验顺序（必须按顺序，任一 fail 立即停）

**层 1 物理硬约束**（用预制 verifier）：
- 能量守恒 $C_{ext}=C_{sca}+C_{abs}$（容差 1e-10）
- 无吸收时 $C_{abs}=0$
- 光学定理
- 瑞利极限 $Q_{sca}\propto x^4$
- 大尺寸极限 $Q_{ext}\to2$
- 球对称性

**层 2 极限/退化**：
- 金属球 LSPR 准静态 $\mathrm{Re}(\varepsilon)=-2\varepsilon_d$
- 核壳壳厚→∞ 退化为单球
- 阵列周期→∞ 退化为单球
- 低填充率→Maxwell-Garnett

**层 3 论文图量化**：
- 数字化论文图，算 RMSE/峰位误差/Q 值误差
- 容差用户定，不是你定

### 预制脚本（scripts/）
- `digitize_paper_figure.py` — 数字化论文图

> 也可直接用 `optics-mie-reproduction/scripts/` 下已写好的 verifier

## 输出约定

- 验证报告：`.work/<case>/physical_verification.md`
- benchmark 草稿：`.work/self-iteration/benchmark_<case>.yaml`

## 常见坑

- verifier 通过 ≠ 物理复现成功，要分开写
- 论文图数字化误差本身就有，容差要留

## 决策问题重点回答

- 3 层都过吗？哪层 fail？
- 两方一致吗？
- 进 step 08 还是回 step 04？
