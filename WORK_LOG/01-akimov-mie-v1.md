# 阶段十二：Mie 首次实跑（Akimov 2401.04146）+ 首跑信号驱动修复

> 详细记录 · case `0703-01-akimov-mie-v1` · 2026-07-03-至今
> 这是 WORK_LOG 文件夹化后**第一篇多阶段详细记录**（阶段十二起，每阶段单独成文，比顶层总览详细）。
> 顶层 `../WORK_LOG.md` 只保留本阶段一句话摘要 + 指针。

---

### 阶段十二：首次实跑 step01-02 + 首跑信号驱动修复（2026-07-03/04）

**首次实跑**（2026-07-03，Akimov 2401.04146，case `0703-01-akimov-mie-v1`）：W-flow step01（pdf_preprocessing）+ step02（paper_reading）完成。产物在 `.work/.todo/2401.04146/0703-01-akimov-mie-v1/`（figures.md 12 图逐图清单 + formulas.md + missing_info.md + figs/ + LaTeX 源），子报告在 `.work/.sub-report/`。

**首跑暴露的 6 条信号**（全部真跑才冒出来，静态审计 `optics_agent/v3-final/V3-AUDIT-2026-07_latest.md` 只预判到其中 3 条）：
1. **memento MCP 不可用**——后确诊为 Claude Code 全部 MCP 断联（环境故障，非"未接入"；用户排查后恢复）。
2. **路径自相矛盾**（= 审计 A2）：同一 SKILL 内 `.work/<case>/` 与 `.work/.todo/{paper}/{case}/{timestamp}/` 并存，spawn 时被迫手动消歧义。
3. **预设目标图不存在**：FINAL 计划/执行手册/papers.md 断言论文有 $Q_{sca}(x)$ 过渡曲线，step02 逐图核对证实 12 张图中没有——Phase-1 预设目标是虚构的。
4. **skill 论文描述错误**（与 3 同根）：`papers.md` 的内容断言是没读原文写的（declared-vs-actual）。
5. **sub-agent 漏交硬产物**：核心产物做了但没写 8 字段报告和 tables.md（"报告靠自觉非 100% fire"被证实；Hook #3 重启信号，已记录）。
6. **verifier 脚本 `check_*.py` 已存在**（中性）：hooks 的"verifier 产物存在"前置比预期早满足；但"脚本存在 ≠ verifier 可信"，verifier 自身仍待 MMS/同构扰动自证。

**修复批次（2026-07-04，本批全部完成，均 .claude+.human 双写）**：
- **papers.md 契约重写**：文件只留课程表层 + 学习目标层（Deliverables = 我们的交付，非论文图），**删除全部论文内容断言**；"论文有哪张图"一律由 step02 对原文提取、过 gate① 才生效；文件头写明契约与首跑教训。optics_agent 侧 FINAL 计划与执行手册的同类断言同步修正（标注论文无 $Q_{sca}(x)$ 图；目标图候选 Fig3 loci / Fig5(c)(f) $|a_1|,|b_1|$ / Fig6）。
- **A2 路径收敛**：`.work/<case>/`、`.work/{case}/`、`.work/self-iteration/`、带 `{timestamp}` 层的 `.todo` 路径 → 统一 canonical `.work/.todo/{paper}/{case}/...`（skill 草稿在其下 `self-iteration/`；case 名含日期版本，无额外 timestamp 层）。CLAUDE.md 目录约定同步；残留 grep=0。E-flow 的 `.work/.result`（A1 消费侧）本轮不动，留待 E-flow 前与 A1 生产契约一起修。
- **spawn 模板硬交付红线**（W 全局模板，三明治首尾各一遍）："8 字段报告 + required_output_paths 全部产物是硬交付，缺任一本步不算完成；不适用也要落盘说明文件（如 tables.md 写明'无表格+依据'）；预写论文描述只是未核实线索，以原文为准；结束前逐项自检"。
- **step02/03 目标图产出条款**：step02 新增"复现目标图候选"为本步权威产出（源自 step01 真实图清单、过 gate①）；step03 约定"目标图只能从 step02 候选中选定"。
- **MCP 预检第 0 步**（CLAUDE.md 记忆要求节）：agent 开工前先确认 memento 工具真实可调用；不可用 → 显式声明降级 + 落 `.work/memento-cache/` 结构化 JSON，禁静默假装搜过/存过；robust 版 = SessionStart hook 探活，随 hooks 一起硬化。
- **验证**：main-agent / sub-agent / optics-mie-reproduction / pdf 四个改动 skill quick_validate 全过。
- **对照静态审计**：A2 / 知识污染 / 漏报告三条从"文件推断"升级为"真跑观测证实"；C1 残留（sub→leaf 身份仍 prompt 软约束）已在审计 N4 登记。
- **Gate1 裁决 + A1/D 补修**（2026-07-04 追加）：用户裁决全按推荐——**目标图=Fig3 loci（候选 A）**、参数表过、**BH 教材式为公式主源**（Akimov 式交叉验证，不一致即 blocker），落盘 `GATE1-决定.md`，Gate1 放行。同批：**A1 生产侧闭合**——step11 SKILL（双写）加"写 capsule 强制节"（`.work/.result/<case>/capsule.md` 100% fire，processed/run_id/result_class/evidence_refs/provenance+断点清单+候选经验，缺则本步不算完成），CLAUDE.md 目录约定同步，E-flow 产/消路径对上；**D 骨架诚实化**——pdf/magnus SKILL 标"⚠ 预制脚本不存在不可依赖"，脚本逐条标（未实现），pdf 注明用现有工具临时实现（首跑已验证）、magnus 注明 Mie 阶段不用。quick_validate 全过。

### step03 + Gate2（2026-07-04）

**step03 一次通过**：sub-agent 产出 `formalization.yaml`（9 字段全闭合）+ `repro_plan.md`（T1→T4 拆分）。核心设计：完全无量纲化（物理只经 $q_e=k_eR$、$\varepsilon_i/\varepsilon_e$ 进入）；**酉性实数化**——无损时 $|a_l|^2=\mathrm{Re}\,a_l$（数值确认 4.4e-16）⟹ $\mathrm{Im}\,a_l=0\Leftrightarrow a_l\in\{0,1\}$，两族 loci 统一为单实方程 brentq 求根；BH 式为主源、Akimov 式交叉验证（300 随机点 max 差 4.7e-16）。sub-agent 还证伪了"分子=0 是实方程"的捷径（负 ε 域不成立）。

**Gate2 通过**（optics_agent CC 独立核对，落盘 `GATE2-决定.md`）：
- CC 独立核物理（酉性圆 $|a_l-\tfrac12|=\tfrac12$ 严格、负 ε 域成立、BH 式/光学定理无误）+ **实读 verifier 源码**确认 T1 接口契约（`from scattering import compute_cross_sections/compute_Q_ext/compute_Q_sca`，签名 (m,x)，与 spec 一致，sub 未虚报）。
- 三决定：①范围=只 Fig3 六面板 loci+Mie 核 ✅；②Layer3 阈值认可（归一距离中位<0.01/95分位<0.03）+ **加硬判据"曲线支数逐面板一致"**（最近距离对 loci 有盲区，不罚伪根杂散支）+ 标注"SEPR 自定阈值非社区标准" ✅；③T1→{T2,T3}→T4 拆分认可、T2 blocker（两式<1e-12 停机）正式脚本固化不得拿预验证顶 ✅。

**第 7 框架发现（重新定性）**：sub-agent 称"tools allowlist 排除 MCP 与'每 agent 搜/存记忆'红线内在矛盾"——**定性错，是设计正确被误读**。正解=**记忆分层**：编排层（main/evolution）持 memento 负责搜+代存+去污染筛选；执行层（sub/sub-e）结构性无 MCP（allowlist 排除 60k+ context 是刻意），落 `.work/memento-cache/` JSON 由 main 审后回灌；执行层本就不该独立写长期记忆（防 case 级半成品污染全局库）。main"代存"是设计非 workaround。扶正为显式 CLAUDE.md 规则的需求已记 `toEflow/记忆分层架构-扶正需求.md`，待本轮跑完由 optics_agent CC 落（不打断 step04）。

**当前状态**：Gate2 已放行，**下一步 main-agent 进 step04**（BH 主源推导 + `code/scattering.py`，T2 先行 → Gate3 用户核公式）。step04 放行 prompt 已落盘 `.work/.todo/.../STEP04-放行prompt.md`。剩余框架遗留：C1 残留收口 + 记忆分层扶正（均待跑通后）。

### step04（T1+T2）+ Gate3（2026-07-05）

**step04 完成**：sub-agent 产 7/7 硬交付（main 独立复校）——`code/scattering.py`（BH 核 160 行）+ `akimov_coeffs.py`（67）+ `crosscheck_bh_vs_akimov.py`（148）+ derivation.md + verifier_log + 8 字段报告 + memento-cache（回灌 id 9ce51b69）。
- **Layer1 验证**：能量守恒 PASS（rel 0.000e+00）、Rayleigh PASS（斜率 4.0001）、实 m 无耗 PASS（σ_abs/σ_ext=1.29e-16）、**大尺寸 FAIL**（max$|Q_{ext}-2|$=0.171 @ x=50）。
- **T2 交叉验证 PASS**（blocker 解除）：BH vs Akimov 3300 点 max$|\Delta a|$=2.2e-15、max$|\Delta b|$=4.8e-16 ≪ 1e-12，0 极点。
- main 机械封顶 result_class=`diagnostic_only`（Layer1 一条 FAIL），不向上包装——口径正确。

**Gate3 通过**（optics_agent CC 独立复算 + 执行 verifier 修复，落盘 `GATE3-决定.md`）：
- **(a) BH 公式核对 ✅**：CC 对教材 BH §4.4 逐项核 $a_l/b_l$ + 记号/导数/时谐，全一致；T2 双路径 2e-15 是强证据。
- **(b) 大尺寸 FAIL = verifier 设计缺陷，非实现 bug**：CC 独立复算确认 $Q_{ext}\to2$ 对无损 $m=1.5$ 慢收敛（$x=1000$ 才 0.014）、**弱阻尼压不掉主偏离**（$m=1.5+0.1i$ 在 $x=200$ 仍 0.057）。→ 否 A（勉强过+算力灾难）/B（削判别力）/D（正确实现被扣 diagnostic_only=假阴性）。
- **CC 已改 verifier 为趋势判据**（治本，`check_large_size_limit.py`）：$Q_{ext}$ 单调趋 2 + 末点 x=800 达 0.05。**双向验证**：正确实现 PASS（0.0163）、漏 $b_l$ FAIL（0.99）、系数×0.5 FAIL（0.49）。verification.md 补适用条件（双写）。另两 Layer1 回归 PASS。
- **元**：外部审查 R4/§2.10「verifier 也要被验证」首个实锤——本次 verifier **太严（假阴）**。`.human` verification.md 的"Not applicable"栏本就写了此情形，`.claude` 脚本没落实=declared-vs-actual 又一例。

**当前状态**：Gate3 已放行。**下一步 main-agent 重跑四个 Layer1 verifier（新版应全 PASS）→ result_class 提升 diagnostic_only→simulation_completed（物理成功仍需 Layer3）→ 进 step05 对抗式审查**。不进 T3。放行 prompt 落盘 `.work/.todo/.../STEP05-放行prompt.md`。

### step05-09 + Gate4（2026-07-05）

**step05 对抗式审查**：8 个对抗探针（P1-P8）默认怀疑代码有错逐条证伪。核心结论：符号/时谐约定正确（对教材 Rayleigh 解析式独立核对，非靠 verifier PASS 反推）；负 ε 域 $a_l,b_l$ 是 $m$ 的偶函数（P8，机器零 1.76e-16，分支取值无关风险）；T2 真独立（AST 解析确认 `akimov_coeffs.py` 无 import `scattering`）。**未发现实质 bug，代码未改**。result_class 维持 `simulation_completed`。

**step06（T3+T4）**：`fig3_loci.py` 六面板切片法求根（q_e 800点×eps 5001点/切片）；`fig3_contour_check.py` 独立二维 contour 法核对完备性——**Gate2 强制附加判据 PASS**：切片法 vs contour 支数逐面板一致（TM 12/12,12/12,11/11；TE 12/12,11/11,11/11），覆盖 >99.8%，无系统性漏根。`fig3_digitize.py` 从论文原图数字化 1982 个取样点。

**step08 Layer3 量化对比**：全局 median=0.00746（**达标**）、p95=0.04258（**超标**）→ CONDITIONAL。nr（非共振支）六面板全部达标（median 0.0054-0.0074）；sr（共振支）TM 三面板 median 也略超（0.011-0.012），5/6 面板 p95 超标（0.052-0.131，仅 TE3 达标）。长尾定位：超阈点集中在**中大 $q_e$ 密集分支区**、$\varepsilon$ 常接近上边界 14.6（正大 ε 区）。main 呈现三选项交 Gate4 裁决，倾向选项1（接受）。

**Gate4 通过**（optics_agent CC 独立审计，决定性证据，落盘 `GATE4-决定.md`）：
- **独立求根 Δ=0.0000**：CC 用 Gate3 验证过的 `scattering.py` **完全绕开** `fig3_loci.py`，重新求 sr locus 根，与 SEPR CSV 逐点对比（TM l1/l2、TE l2 多切片，几十根）**全部 Δ=0.0000**——证复现曲线数学完全正确，超标非画错，归因数字化读图误差。
- **裁决**：选项1（接受）+ 3 强制条件：① result_class=`partial_physical_match`；② 诚实边界如实写明（**纠正 main 两处转述漂移**——"负ε陡共振区"实为"正大ε(≈14.6)+中大q_e密集区"说反；"中位数只略超"漏报 TM 三面板 sr 中位数也超阈）；③ 不改阈值（否决选项2=verifier gaming），benchmark.yaml 标 sr 超标为 known/accepted。否选项3（边际收益低）。

**step09 可复现性自检**：对 `fig3_loci.py` 求根做 5 类数值扰动（n_max截断/eps网格密度/q_e网格密度/brentq容差/随机种子），**全部稳定**——n_max 扰动偏移=0（结构无关，loci 单阶求根不调用截断）；Gate4 密集区（$\varepsilon>10$）在最粗测试网格下 sr 支数仍=9，无漏支无串支；brentq 容差扰动下根位置随容差单调收敛；无随机成分。**归因收敛为单因：数字化读图困难**（数据不支持"网格敏感"这一半原假设）。result_class 维持 `partial_physical_match`，排除"瞎猫碰死耗子"。

### step10-11 收尾（2026-07-05）

**step10 summary_and_report（main-agent 直接撰写，未 spawn sub-agent）**：产出 `full_report_draft.md`（192行，完整10步记录+Gate4三强制条件逐字复述+"什么没做透"+接力信息）、`brief_draft.md`（36行，PI摘要）、`self-iteration/2401.04146.skill-suggestion-draft.md`（4条建议，P0×1/P1×2/P2×1）、`self-iteration/2401.04146.blueprint-suggestion-draft.md`（本次无需蓝图）、`reproduction_test/mie/data/benchmark.yaml`（首次创建，含完整逐面板Layer3数值+独立复算验证记录+sr超标known/accepted标注）。定稿投递 `toEflow/2401.04146.skill-suggestion.md` + `toEflow/2401.04146.blueprint-suggestion.md`。

**关键执行方式变通（如实记录）**：本步 main-agent 直接撰写全部文档，未经 sub-agent 中转。理由：本 case 已两次出现 main 转述漂移被 Gate4 独立审计纠正（见上），双报告需精确复述 Gate4 裁决数值和方向性结论，属高判断密度工作，再插一层 sub-agent 转述会重演同类风险。已提交 skill-suggestion 建议1（P0，main-agent 复述纪律）作为长期解法。

**step11 main_agent_report（本次）**：写 `.work/run_manifest.yaml`（run_id/9个sub-agent spawn记录/max_depth_reached=2/未触发leaf/3条retry_fingerprint/result_class=partial_physical_match/4个human gate记录）+ `.work/.result/0703-01-akimov-mie-v1/capsule.md`（E-flow唯一输入，含六条首跑信号盘逐类核对+3条新发现信号+候选经验GUIDING×3/CAUTIONARY×3/FACT×2/PROCEDURE×1+断点清单+"什么没做透"）+ 本篇 WORK_LOG 增量更新 + 顶层 WORK_LOG.md 摘要表更新。

**当前状态**：**step11 完成，workflow 收尾**。这是本次复现最后一个 human gate——等用户确认 `.work` 沙箱中哪些产物正式进 `.result/`（顶层最终交付区，区别于 `.work/.result/` 的 capsule 沙箱）。

### 决策台账新增

### D-10 Step10 执行方式变通：main-agent 直接撰写而非 spawn sub-agent（2026-07-05）
- **背景**：本 case 已两次出现 main-agent 转述漂移被 Gate4 独立审计纠正（见 D-09）。标准流程 step10 应 spawn sub-agent 产双报告初稿。
- **main-agent 判断**：双报告（尤其 Gate4 三强制条件的完整复述）属于高判断密度工作，若再 spawn sub-agent 转写一遍、main 再读 sub 的转写汇总，等于多一层转述风险。main-agent 本轮已亲自读过全部权威原文（GATE1-4决定/formalization.yaml/theory_check/derivation/selfcheck/layer3_report），有直接撰写的信息基础。
- **执行**：main-agent 直接撰写 `full_report_draft.md`/`brief_draft.md`/skill-suggestion/blueprint-suggestion/benchmark.yaml，撰写时对照原始文件逐项核对数值（非凭记忆转写）。
- **代价声明**：跳过了"sub-agent独立产出+main审校"的两级校验结构，已在报告开头"执行方式说明"节如实记录，作为一次性变通而非常规做法。长期解法已提交 skill-suggestion 建议1。
- **落点**：`full_report_draft.md` 开头"执行方式说明"节；`toEflow/2401.04146.skill-suggestion.md` 建议1；memento pitfall `1a7973f6`。

### D-11 Step11 后最终 human gate：.result 交付范围 + 额外中文 LaTeX 论文（2026-07-05）
- **main 提议**：仅复制双报告+主报告进 `.result/2401.04146/`，代码/数据/图留在既定的 `reproduction_test/mie/` 工作区路径，不额外复制。
- **用户裁决**：① **额外要求复制代码/数据/图**，做成完整自包含交付包（超出 main 的保守提议）；② **额外要求撰写一篇中文 LaTeX arXiv 风格论文**记录本次复现全过程（不在标准 step10/11 产出范围内，用户主动加做）。
- **toEflow/ 处理时机**：用户裁决留给未来专门的 evolution-agent 批次统一处理（符合 CLAUDE.md"只增不删"缓冲区设计），不现在转发给 optics_agent；但要求在本次回复中标注路径以便随时查看。
- **执行**：
  - 代码（10个脚本）+ 数据（9个CSV+benchmark.yaml）+ 图（4张）复制进 `.result/2401.04146/{code,data,figures}/`（保留 `reproduction_test/mie/` 工作区原件不动，两处并存）。
  - 撰写 `.result/2401.04146/paper_cn/main.tex`（约 300 行，含摘要/引言/理论/数值实现与多层验证/结果/讨论-诚实边界/结论），用 `ctex` + `xelatex` 编译为 `main.pdf`（13页）。首次编译遇到 Layer1 验证表格 183pt 溢出，改用 `tabularx`+`p{}` 固定列宽修复；三次编译消除交叉引用警告，最终编译干净（0 error，仅 1 处轻微 overfull 可接受）。
- **落点**：`.result/2401.04146/`（完整交付包）、`.result/reports/main-0703-01-akimov-mie-v1-20260705-02.md`；memento session_summary `690f9a95`（pinned）。
- **当前状态**：**本次复现全流程完整闭环**，无待处理的 human gate。toEflow/ 两份建议文件路径见下方"当前 toEflow 待处理清单"。

---

## 当前 toEflow 待处理清单（用户要求标注，供随时查看）

- `toEflow/2401.04146.skill-suggestion.md`：4 条 skill 改进建议（P0×1 main-agent复述纪律缺失 / P1×2 / P2×1 记录性），留给未来 evolution-agent 批次统一处理。
- `toEflow/2401.04146.blueprint-suggestion.md`：本次无需蓝图（纯Python，记录性文件）。
- `toEflow/记忆分层架构-扶正需求.md`：Gate2 期间记录的框架规则扶正需求（早于本 case 收尾），仍待处理。

---

## 决策全账本（用户没时间盯对话 → 所有建议/裁决/落点在此，读此即可恢复，不必翻对话）

> 记法：**CC 建议** = optics_agent 侧 CC（我）给的意见；**用户裁决** = 你拍的板；**落点** = 改了哪个文件。按时间序。

### D-01 papers.md 是否该含论文内容描述（2026-07-04）
- **背景**：首跑发现 papers.md 断言 Akimov 有 $Q_{sca}(x)$ 图，实际没有。
- **CC 建议**：不止改错字，应**契约级收缩**——框架层（papers.md/计划）不得断言论文内容，论文有什么图由 step02 从原文提取过 gate① 才算数。
- **用户裁决**：✅ 同意（"框架不应该包括论文描述，论文粗读是 workflow 第一阶段的事"）。
- **落点**：`optics-mie-reproduction/references/papers.md`（.claude+.human 双写，只留课程表+学习目标层）；step02 加"目标图候选"权威产出；step03 加"只能从候选选"；FINAL 计划+执行手册同步改。memento 决策 `a3038b08`（已 pin）。

### D-02 memento MCP 断联怎么处理（2026-07-04）
- **背景**：首跑期 memento 全断（后确诊 = 全部 MCP 断联，环境故障）。
- **CC 建议**：不接 memento（验证价值前不补基础设施）；改为**开工前 MCP 预检 + 掉线大声降级**（不可用则显式声明+文件兜底，禁静默假装搜过）。
- **用户裁决**：✅ 采纳（要求"加一条 agent 开始前确认 MCP 全部可用"）。
- **落点**：SEPR `CLAUDE.md` 记忆要求节第 0 步 + optics_agent `CLAUDE.md`（hardlink 重建 inode 34902897112198507）。

### D-03 Gate1 三决定（2026-07-04）
- **决定 1 目标图**：CC 建议候选 A（Fig3 loci，零材料依赖最干净测框架）。**用户裁决 ✅ A**。
- **决定 2 参数核对**：CC 核过参数表无误（$q_e=k_eR$、Wiscombe 截断标 trust、eV→nm 换算例算对）。**用户裁决 ✅ 通过**；材料源三条选 A 不下载。
- **决定 3 公式主源**：CC 建议 BH 教材式为主源、Akimov 式交叉验证、不一致即 blocker。**用户裁决 ✅ 确认**。
- **落点**：`GATE1-决定.md`；memento 决策 `85fd5b92`。

### D-04 A1/D 框架修复（随 Gate1 一起，2026-07-04）
- **CC 建议**：趁本篇没跑到 step11，先补 A1 生产侧（step11 必产 capsule.md）+ D 骨架诚实化（pdf/magnus 标"脚本不存在"）。
- **用户裁决**：✅（"自己生查风险 无需批准"授权范围内）。
- **落点**：step11 SKILL 双写加"写 capsule 强制节"；`CLAUDE.md` 目录约定加 capsule 行；pdf/magnus SKILL 标注。

### D-05 Gate2 三核对点 + 第 7 发现（2026-07-04）
- **核对点 1 范围边界**：CC 认可只做 Fig3 六面板。**用户裁决 ✅**。
- **核对点 2 Layer3 阈值**：CC 认可原数（中位<0.01/95分位<0.03）**但加硬判据"曲线支数逐面板一致"**（最近距离对 loci 有盲区，不罚伪根杂散支）+ 标注"SEPR 自定阈值非社区标准"。**用户裁决 ✅**（"自己生查风险无需批准"）。
- **核对点 3 T1-T4 拆分 + T2 blocker**：CC 认可（实读 verifier 源码确认接口契约，sub 未虚报；T2 两式<1e-12 不过即停机，正式脚本固化）。**用户裁决 ✅**。
- **第 7 发现（记忆分层）**：sub-agent 称"allowlist 排除 MCP 与记忆红线矛盾"。**CC 重新定性**：不是矛盾，是"编排层持 memento / 执行层落 cache 由 main 代理回灌"的正确分层设计，main"代存"是设计非 workaround；扶正为显式 CLAUDE.md 规则的需求已记 `toEflow/记忆分层架构-扶正需求.md`，待本轮跑完落，不打断 step04。
- **落点**：`GATE2-决定.md`；`toEflow/记忆分层架构-扶正需求.md`；memento 决策 `afca68ed`。

### D-06 WORK_LOG 文件夹化（2026-07-04）
- **用户要求**：WORK_LOG 变文件夹 = 目录总览（原风格）+ 多阶段详细记录（从阶段十二起）+ 引用文件。
- **落点**：顶层 `WORK_LOG.md` 保留为总览+阶段摘要表+指针（旧引用不断）；`WORK_LOG/00-历史存档...`（全文快照）+ `WORK_LOG/12-...`（本文件）+ `WORK_LOG/README.md`。

### D-07 Gate3 (a) BH 公式核对（2026-07-05）
- **CC 建议/核对**：对教材 BH §4.4 逐项核 $a_l/b_l$ + 记号/导数/时谐，全一致；T2 双路径 2e-15 是实现正确的强证据。
- **用户裁决**：✅ 通过（你委托 CC 核，"你来吧"）。
- **落点**：`GATE3-决定.md` (a)。

### D-08 Gate3 (b) 大尺寸 verifier FAIL 处理（2026-07-05）
- **背景**：Layer1 大尺寸 verifier FAIL（$|Q_{ext}-2|$=0.171@x=50），main 诊断为 verifier 设计缺陷非实现 bug，给 A/B/C/D 四选项。
- **CC 建议**：独立复算否掉全部四选项——A 勉强过靠运气+算力灾难、B 削判别力、C 弱阻尼压不掉慢收敛主偏离、D 假阴性扣正确实现。改为**趋势判据**（$Q_{ext}$ 单调趋 2 + 末点达标），双向验证保判别力。
- **用户裁决**：✅ "你来吧"（授权 CC 直接改 `.claude/skills` verifier）。
- **落点**：`check_large_size_limit.py`（趋势判据，.claude）+ `verification.md` 1.5 适用条件（.claude+.human 双写）+ `GATE3-决定.md` (b)。CC 已实测双向验证 PASS/FAIL。

### D-09 Gate4 Fig3 复现最终误差核对（2026-07-05）
- **背景**：step05-08 一路自动跑完（对抗审查/求根/出图/数字化/Layer3 对比）。Layer3 卡边界：全局 median 0.00746✅/p95 0.04258❌；nr 六面板全达标，sr 5/6 面板 p95 超标（0.05-0.13）。main 给选项 1（接受，倾向）/2（放宽阈值）/3（加密重测）。
- **CC 独立审计**：用 Gate3 验证过的 `scattering.py` **完全绕开 SEPR `fig3_loci.py`** 独立重新求 sr 根，与 CSV 逐点对比 **Δ=0.0000**（TM l1/l2、TE l2 多切片，几十根全 0）→ 复现曲线数学正确、无画错，超标确系数字化读图误差。**纠正 main 两处转述漂移**：①"负 ε 陡区"实为正大 ε(≈14.6)；②"中位只略超"只对一半（TM 三面板 sr 中位也超）。
- **CC 建议**：选项 1 接受 + 3 强制条件（result_class=partial_physical_match；报告如实写诚实边界含 TM 中位也超+方向性检验未完成；**不改阈值**否决选项2=verifier gaming）。否选项3（边际收益低）。
- **用户裁决**：✅ 采纳（"你帮我做以上事情"）。
- **落点**：`GATE4-决定.md`；memento `750b5372`；benchmark.yaml 待 step10 标 sr 超标 known/accepted。
- **未做透**：数字化偏差单/双侧方向性检验（CC 逐点求根太慢中止，独立求根 Δ=0 已决定性故不阻塞）。

### 待你有空时可回看/可推翻的项（都已落，不阻塞）
- Layer3 阈值是 SEPR 自定、无文献先例 → 跑完据实调，别当权威门槛卡后续论文。
- 记忆分层扶正的子问题：main 回灌逐条照搬 vs 只提炼 case 级结论（CC 倾向后者防膨胀）→ 攒 2-3 case 看真实膨胀再定。
- C1 残留（sub→leaf 身份仍 prompt 软约束）→ 跑通后与 hooks 一起收口（审计 N4 登记）。
- 大尺寸 verifier 趋势判据的末点 x=800/tol 0.05 是 CC 复算定的 → 若后续某论文用强吸收球，此判据不适用（已在 verification.md 标 Not applicable），据实换。
- Gate4 sr 长尾方向性检验未跑完 → 若要教科书级严谨可补（逐点求根算带符号偏差，判单/双侧）；复现正确性已由 Δ=0 独立证实，非必须。

---

