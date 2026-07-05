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

### 待你有空时可回看/可推翻的项（都已落，不阻塞）
- Layer3 阈值是 SEPR 自定、无文献先例 → 跑完据实调，别当权威门槛卡后续论文。
- 记忆分层扶正的子问题：main 回灌逐条照搬 vs 只提炼 case 级结论（CC 倾向后者防膨胀）→ 攒 2-3 case 看真实膨胀再定。
- C1 残留（sub→leaf 身份仍 prompt 软约束）→ 跑通后与 hooks 一起收口（审计 N4 登记）。

---

