# Step05 放行 prompt — main-agent 恢复执行

> Gate3 已通过（`GATE3-决定.md`）。verifier 已由 optics_agent CC 修好。把下面整段发给停在 Gate3 的 main-agent。

---

```
Gate3 通过（2026-07-05）。见 .work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE3-决定.md，以它为准。

(a) BH 公式核对：通过。a_l/b_l 与教材 BH §4.4 一致，T2 双路径 2e-15 为强证据。
(b) 大尺寸 verifier FAIL：确认是 verifier 设计缺陷（假阴性），非 scattering.py bug。optics_agent CC 已把 check_large_size_limit.py 改为趋势判据（Q_ext 单调趋 2 + 末点 x=800 达 0.05），并双向验证（正确实现 PASS / 注 bug FAIL），verification.md 1.5 适用条件已补（.claude+.human 双写）。你不用改 scattering.py。

【先做：重跑四个 Layer1 verifier 确认全 PASS】
PYTHONUTF8=1 python .claude/skills/optics-mie-reproduction/scripts/check_energy_conservation.py
PYTHONUTF8=1 python .claude/skills/optics-mie-reproduction/scripts/check_rayleigh_limit.py
PYTHONUTF8=1 python .claude/skills/optics-mie-reproduction/scripts/check_large_size_limit.py
（大尺寸新版应 PASS，末点 x=800 |Q-2|≈0.016。实 m 无耗 σ_abs=0 已在 step04 确认。）
- 若四个全 PASS → result_class 从 diagnostic_only 提升到 simulation_completed（Layer1 全过；物理复现成功仍需 Layer3 Fig3 定量对比 + human gate，本步无权声明 physical_reproduction_success）。
- 若大尺寸仍 FAIL → 停机报我（说明新 verifier 与预期不符），不硬跑。

【然后进 step05 theory_check（对抗式审查）】
spawn sub-agent 对 scattering.py + akimov_coeffs.py 做对抗式审查（不是复述，是找错）：
- a_l/b_l 分子分母逐项、阶数、符号、Riccati-Bessel 导数链式法则、切/法向 BC 双向归因核对；
- 重点查负 ε 域（m 纯虚）分支：ψ_l(mx) 复宗量、主值平方根 Im m≥0、指数增长是否溢出（step03 已核 l=3,ε=-10,q_e=10 角点 |N|~5e14 float64 安全，审查复核）；
- 截断 Wiscombe n_max 在 x=800 大尺寸下是否够（大尺寸 verifier 已间接压过，但审查明确写结论）；
- 交叉验证 T2 已 PASS，审查确认"两式等价"不是"两处同一 bug"（T2 是独立公式路径，非同实现复制）。
- 产出 theory_check.md（问题清单 + 修正建议），过程走硬交付红线（8 字段报告 + 全部产物落盘）。

【Gate3 已是本轮最后一个公式关；step05 后按 workflow】step05 完 → 若审查发现需改公式则回 step04；否则继续。注意：Fig3 求根（T3）+ 出图（T4）是 step06+ 的事，step05 只审查现有 T1/T2 代码，不进 T3。

【执行纪律】记忆分层：sub 无 MCP 属正常设计，落 memento-cache 由你代回灌。路径 .work/.todo/2401.04146/0703-01-akimov-mie-v1/...。result_class 红线不变。全程中文+Markdown，公式 $...$。step11 时记得按新规范增量更新 WORK_LOG/01-akimov-mie-v1.md（本轮我已替你补到 Gate3，step05 起你自己续）。
```
