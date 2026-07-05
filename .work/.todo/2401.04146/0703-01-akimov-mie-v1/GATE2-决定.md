# Gate2 决定记录 — 用户已裁决（2026-07-04，经 optics_agent CC 独立核对）

> 对应 main-agent 在 Gate2（formalization spec 核对）呈现的 3 个核对点 + 第 7 框架发现。
> main-agent 恢复后以本文件为准放行 step04。

## optics_agent CC 独立核对（非转述，对抗式）

- **物理核**：酉性实数化严格成立——无损球 Mie 系数落 Argand 圆 $|a_l-\tfrac12|=\tfrac12$，圆与实轴仅交于 $\{0,1\}$，故 $\mathrm{Im}\,a_l=0\Leftrightarrow a_l\in\{0,1\}$，数学严格非近似；负 ε 域（理想无损，$\mathrm{Im}\,\varepsilon_i=0$）酉性仍成立。BH 式 $a_l,b_l$、光学定理截面、$Q=2/q_e^2$ 归一全部标准无误。
- **接口契约核（实读 verifier 源码，非信 sub-agent）**：`check_energy_conservation.py`/`check_large_size_limit.py`/`check_rayleigh_limit.py` 三脚本真实存在，`from scattering import compute_cross_sections / compute_Q_ext / compute_Q_sca`，签名 `(m=..., x=...)`，`CODE_DIR=reproduction_test/mie/code`——与 spec T1 契约完全一致，sub-agent 未虚报。

## 决定 1：范围边界 ✅ 认可

只做 Fig3 六面板 loci + Lorenz-Mie 核基础设施；显式不做 Fig4/5/7/8（材料谱）、Fig6（超吸收复根）、Fig1/2（场分布）、§4 修正。Fig6/Fig5(c)(f) 留第二轮。

## 决定 2：Layer3 阈值 ✅ 认可原数 + 1 条强制附加判据

- 阈值认可不改：归一化最近距离（$q_e$/10、$\varepsilon$/25），中位 $<0.01$、95 分位 $<0.03$。
- **强制附加判据（从"附带"升为硬判据）**：**曲线支数逐面板一致**——"最近距离"对 loci 图有盲区（只罚"离点远"，不罚"多画一条论文没有的杂散支"，即 brentq 括到极点的伪根）。支数不一致 → Layer3 直接 FAIL，不靠目测。这样阈值才闭合。
- **诚实标注**：此阈值无 loci 图文献先例，是 SEPR 自定、首次使用，报告须标"SEPR 自定阈值，非社区标准"，跑完据实调；不得反过来当权威门槛卡后续论文。

## 决定 3：T1→T4 拆分 + T2 blocker 口径 ✅ 认可

- 依赖图正确（T2/T3 只依赖 T1，T2 建议先行早暴露 blocker）。
- T2 blocker 口径（两式 $<10^{-12}$ 不过即停机）符合 Gate1 决定 3；300 随机点预验证 max 差 4.7e-16 风险极低，但**正式验证必须落盘脚本固化，不得拿 step03 预验证顶 T2**。
- T3 的 Layer2 论文内自洽判据（sr 根处 $\sigma_{sca,l}/\pi R^2=2(2l+1)/q_e^2$、$\sigma_{abs,l}=0$）是 Fig3 零材料依赖能给的最干净验证，保留。

## 第 7 框架发现：重新定性（不是"矛盾"，是"设计正确、需扶正为显式规则"）

sub-agent 称"allowlist 与记忆红线内在矛盾"——**定性不准**。正解：
- 子 agent MCP 全量注入占 60k+ context，allowlist 排除 MCP 是**刻意设计**；
- 记忆红线本意是"每个 agent 搜/存"，但**执行层 sub 本就不该独立写长期记忆**（会制造 case 级半成品污染全局库）。
- 正确架构 = **编排层（main/evolution）持 memento 负责搜+代存+去污染筛选；执行层（sub/sub-E）结构性无 MCP，落 `.work/memento-cache/` JSON 由 main 审后回灌；叶子层同理**。
- main 现在"代存两条"就是正解，非 workaround——要做的是把它从"临时兜底"**扶正成写死的记忆分层规则**（改 CLAUDE.md 记忆纪律）。此项已记入 `toEflow/`，由 optics_agent CC 本轮跑完后落，**不打断 step04**。
- 待决子问题（不阻塞）：main 回灌是逐条照搬还是只提炼 case 级结论进全局？倾向后者（防膨胀），攒 2-3 case 看真实膨胀再定。

---

**放行**：Gate2 通过。main-agent 进 step04（BH 主源推导 + `code/scattering.py` 实现，遵守 verifier 接口契约，T2 先行）→ Gate3（用户对教材核公式）停机。
