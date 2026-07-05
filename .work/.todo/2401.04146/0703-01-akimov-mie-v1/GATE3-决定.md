# Gate3 决定记录 — 用户已裁决（2026-07-05，optics_agent CC 独立复算 + 执行 verifier 修复）

> 对应 main-agent 在 Gate3（step04 T1+T2 后公式核对）呈现的 (a)(b) 两裁决点。
> main-agent 恢复后以本文件为准：重跑四个 Layer1 verifier → 进 step05。

## (a) BH 公式核对 ✅ 通过

optics_agent CC 对 `.paper/scattering.pdf`（Bohren & Huffman §4.4）逐项核 `scattering.py` + derivation.md §2：
- $a_l$（电/TM）分子 $m\psi(mx)\psi'(x)-\psi(x)\psi'(mx)$、分母 $\psi'(x)\to\xi'(x)$、$\psi(x)\to\xi(x)$ ✓ 与 BH 4.53 一致。
- $b_l$（磁/TE）$m$ 因子位置对调 ✓ 一致。
- $\xi_l=z\,h_l^{(1)}=z(j_l+iy_l)$、$e^{-i\omega t}$ 约定、散射场用 $h^{(1)}$、导数 $\psi'=j_l+zj_l'$ 链式法则 ✓ 全部自洽。
- T2 交叉验证 BH vs Akimov 3300 点 max$|\Delta|\sim$2e-15 ≪ 1e-12 = 两条独立公式路径殊途同归，实现正确性的强证据（非同一 bug 抄两遍）。
**结论：公式与教材一致，记号/导数/时谐约定无误，Gate3 公式关通过。**

## (b) 大尺寸 verifier FAIL 处理 ✅ 裁决=改 verifier（治本），已由 CC 执行

**诊断确认（CC 独立复算，非信 sub/main）**：FAIL 是 verifier 设计缺陷，非 `scattering.py` bug。三证据：能量守恒 rel err=0、Rayleigh 斜率 4.0001、T2 双路径 2e-15 一致。

**复算暴露的关键点（改变了原选项建议）**：
- $Q_{ext}\to2$ 对无损 $m=1.5$ **收敛极慢**（代数 ~$1/x$ 边缘衍射修正）：$x=200$ 偏 0.09、$x=1000$ 才 0.014、$x=2000$ 才 0.010。→ **否 A**（增大 x 到 1000 勉强过靠运气 + 算力灾难）。
- **弱阻尼压不掉主偏离**：$m=1.5+0.1i$ 在 $x=200$ 仍 0.057——虚部只衰减叠加 ripple，不改慢收敛趋势。→ **原选项 C 单独也不够**。
- → **否 B**（放宽 tol 削判别力）、**否 D**（正确实现被有 bug 的 verifier 永久扣在 diagnostic_only = 假阴性，比假阳性更坑，破坏 result_class 可信度）。

**采用方案 = 趋势判据（治本）**，CC 已改 `check_large_size_limit.py`：
- 判据从"某几点 $|Q-2|<0.05$"改为**趋势判据**：$Q_{ext}$ 随 $x$ 单调趋 2（C2 容 0.02 ripple）+ 末点 $x=800$ 达 0.05（C1）+ 首点比末点更偏（C3）。这才是"消光佯谬"物理内核，且对慢收敛/ripple 免疫。
- **双向验证（CC 实测）**：正确无损实现 → PASS（末点 0.0163）；注入 bug 漏 $b_l$ → FAIL（0.99）；注入 bug 系数×0.5 → FAIL（0.49）。判别力保住，非橡皮图章。
- **verification.md 补适用条件**（.claude+.human 双写）：1.5 判据改趋势判据，注明"无损球慢收敛需 $x\gtrsim1000$、弱阻尼压不掉主偏离、强吸收球不适用"。
- 另两 Layer1 verifier 回归 PASS（能量守恒 0.000e+00 / Rayleigh 4.0001）。

**元层面**：这是外部审查 R4/§2.10「verifier 自身有 silent failure，也要被验证」的首个实锤——本次是 verifier **太严（假阴）**。`.human` 侧 verification.md 的"Not applicable"栏其实早写了"transparent weak-contrast spheres with strong oscillatory convergence"，设计层面本就对，只是 `.claude` 脚本没落实——declared-vs-actual 的又一例。

## 放行

Gate3 通过。main-agent：**重跑四个 Layer1 verifier（新 check_large_size_limit.py 应 PASS）→ 若全 PASS，result_class 从 diagnostic_only 提升到 simulation_completed**（物理复现成功仍需 Layer3 Fig3 对比 + human gate）→ 进 step05（对抗式审查）。不进 T3（Fig3 求根是后续）。
