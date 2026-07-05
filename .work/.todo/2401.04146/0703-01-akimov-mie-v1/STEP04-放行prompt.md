# Step04 放行 prompt — main-agent 恢复执行

> Gate2 已通过（`GATE2-决定.md`）。把下面整段发给停在 Gate2 的 SEPR main-agent 即可放行 step04。
> 内联了 Fig3 目标 / BH 主源 / T1 接口契约 / T2 blocker 等关键约束（cold-start brief 原则：恢复指令不依赖 agent 记得去读对文件，但 GATE2-决定.md 仍是权威落盘）。

---

```
Gate2 通过（2026-07-04，optics_agent CC 已独立核对物理与 verifier 接口契约）。三决定见 .work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE2-决定.md，以它为准。进 step04。

【本步任务：step04 theory_and_implementation】
按 formalization.yaml + repro_plan.md 的 T1→T2→T3→T4 拆分实现代码。本步先做 T1 + T2（T3/T4 可下一轮）。目标图 Fig3（超辐射 a_l=1 / 非辐射 a_l=0 loci），公式主源 = Bohren & Huffman 教材式（.paper/scattering.pdf），Akimov 论文式仅作交叉验证。

【T1 — BH 主源 Mie 核（硬接口契约，不可改签名）】
产出 reproduction_test/mie/code/scattering.py，必须暴露且签名精确匹配现有 verifier 的 import：
- compute_cross_sections(m, x) -> (Cext, Csca, Cabs)
- compute_Q_sca(m, x)
- compute_Q_ext(m, x)
- mie_ab(l, m, x) -> (a_l, b_l)   # 供 T2/T3 取单系数
（verifier 从 CODE_DIR=reproduction_test/mie/code 下 `from scattering import ...`，已实读确认，别动这些名字和 (m=,x=) 关键字调用方式。）
实现要点：Riccati-Bessel ψ_l=q·j_l(q)、ξ_l=q·h_l^(1)(q)，用 scipy.special.spherical_jn/spherical_yn(derivative=True)，复宗量直接可用，不自写特殊函数；BH 标准式 a_l,b_l（spec equations.primary_BH）；截面用光学定理式，Wiscombe 截断 n_max=ceil(x+4x^{1/3}+2)。

【T1 验收（必须全过才进 T2）】
跑三个既有 verifier（.claude/skills/optics-mie-reproduction/scripts/）：
- check_energy_conservation.py PASS（|σ_ext−σ_sca−σ_abs|/σ_ext < 1e-10）
- check_rayleigh_limit.py PASS（Q_sca ∝ x^4）
- check_large_size_limit.py PASS（Q_ext → 2）
附加：实 m（无耗）时 σ_abs=0，rel < 1e-12。

【T2 — Akimov 式交叉验证（blocker）】
产出 code/akimov_coeffs.py + crosscheck_bh_vs_akimov.py + 结果日志。独立实现 Akimov 式（spec equations.cross_check_akimov，显式 q_i,q_e 因子），与 T1 的 BH 式逐点比对：
- 网格 l∈{1,2,3} × ε_i/ε_e∈[-10,15]（含负值/含小|ε|）× q_e∈(0,10]，≥1e3 确定性点 + ≥300 随机点
- 通过判据：max|a_BH−a_Akimov| < 1e-12 且 max|b_BH−b_Akimov| < 1e-12
- 【blocker】不通过即停机报告，不硬跑（Gate1 决定3）。step03 预验证 300 点 max 差 4.7e-16 提示会过，但必须以脚本落盘固化，不得拿预验证顶 T2。

【执行纪律】
- spawn sub-agent 时用更新后的全局模板：8 字段报告 + 全部规定产物是硬交付，缺任一本步不算完成；回收报告先校验存在性和 8 字段再看内容。
- 记忆分层（本次已定，见 GATE2-决定.md 第7发现）：sub-agent 无 MCP 属正常设计，它落 .work/memento-cache/ JSON，由你（main，有 MCP）审后代回灌，别再把"sub 无法搜记忆"当 bug 报。
- 路径用 .work/.todo/2401.04146/0703-01-akimov-mie-v1/...；代码落 reproduction_test/mie/code/。
- result_class 红线：Layer1 任一硬约束 FAIL → ≤ diagnostic_only；跑通/无报错 ≠ 物理复现成功。本步（实现+单元验证）最高到 simulation_completed，物理复现成功要 Layer3 + human gate。
- 失败防护：同一步重跑 ≤5 轮且每轮新证据；触发 blocker 停机报告。全程中文 + Markdown，公式 $...$。

【完成后】T1+T2 都过 → 停在 Gate3（theory_check 后你对教材核 a_l,b_l 公式，最关键 10 分钟）。T2 若 blocker → 停机报告，不进 T3。
```
