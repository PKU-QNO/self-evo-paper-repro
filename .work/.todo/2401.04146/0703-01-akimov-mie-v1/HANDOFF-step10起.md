# 交接 prompt — Akimov Fig3 复现，从 step10 起（新对话用）

> 生成日期：2026-07-05 | 上一对话上下文已满，此为交接。
> 用途：把这份内容整段发给同一工作区的新对话，即可无缝续接。

---

## 你是谁 / 现在到哪了

你是 SEPR 的 **main-agent**（复现编排者）。正在跑 SEPR 首次真实论文复现：**Akimov arXiv 2401.04146，Fig3**（超辐射 $a_l=1$ / 非辐射 $a_l=0$ 态 loci，六面板 TM/TE × l=1,2,3，$(q_e, \varepsilon_i/\varepsilon_e)$ 实平面）。

- case 名：`0703-01-akimov-mie-v1`
- 纯 Python 阶段（**无 COMSOL/Magnus**；任何步骤想要远程作业就停下问用户）。
- **10 步 W-flow 已跑到 step09 完成，Gate1/2/3/4 全过。剩 step10（总结+双报告+benchmark+skill草稿）、step11（run_manifest+capsule+WORK_LOG）。**
- **result_class 全程锁定 `partial_physical_match`**（Gate4 裁决，CLAUDE.md 红线封顶，**绝不**声明 physical_reproduction_success）。

## 开工必做（按 CLAUDE.md）

1. **读 CLAUDE.md**（工作区根，强制路由 + 红线）。
2. **MCP 预检**：确认 `memory_search` 等 memento 工具可调用。可用则搜记忆；不可用则降级落 `.work/memento-cache/` 并声明。
3. **搜 memento**：`memory_search("akimov 2401.04146 step")` 恢复全链决策。已存关键记忆 id：step04=9ce51b69、step05=b1c06162、step06=96e14ad5、step06T4=0209f838、step08=91a349cd、step09=d1cf5e45（还有 step01/02/03、Gate 系列）。
4. **读顶层 `WORK_LOG.md`** + 本篇 **`WORK_LOG/01-akimov-mie-v1.md`**（恢复大框架，optics_agent CC 已帮补到 Gate3；step10/11 你要按新规范增量续写）。
5. 读身份 skill：`.claude/skills/main-agent/SKILL.md` + workflow/10、11。

## 必读的权威文件（决策口径，以这些为准，别靠转述）

| 文件 | 内容 |
|------|------|
| `.work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE4-决定.md` | **最重要**。选项1接受+3强制条件。独立求根 Δ=0 证复现正确 |
| `GATE1-决定.md` / `GATE2-决定.md` / `GATE3-决定.md` | 早前 gate 裁决（目标图=Fig3、spec、公式对教材核） |
| `formalization.yaml` | 物理 spec（BH主源式+Akimov交叉式+solver求根策略+observables六面板） |
| `repro_plan.md` | T1→T4 拆分 + Layer1/2/3 判据 + 阈值 |
| `09-reproducibility_selfcheck/selfcheck_report.md` | step09 自检结论 + 对 Gate4 归因的单因校正 |
| `08-physical_verification/layer3_report.md` + `layer3_verdict.json` | Layer3 量化对比结果 |

## Gate4 裁决的 3 条强制条件（step10/11 报告必须如实体现，不得只写"长尾读图误差"）

1. **接受依据** = optics_agent CC 用 Gate3 验证过的 scattering.py **完全独立重新求 sr locus 根**，与 SEPR fig3_loci.py CSV 逐点对比 **Δ=0.0000**（TM l1/l2、TE l2 多切片）→ 证复现曲线数学正确、无画错；超标归因数字化读图（nr 六面板全达标佐证无整体偏移）。
2. **诚实边界**（关键，别写反）：
   - **TM 三面板 sr 的中位数也略超阈**（0.011–0.012 > 0.01），**非仅 p95 长尾**；TE 三面板才是"中位达标、仅长尾超"。
   - 超阈点集中在 **正大 ε（≈上边界 14.6）+ 中大 q_e 密集分支区** —— **不是"负 ε 区"**（早先 main 转述说反了，Gate4 已更正）。
   - step09 进一步把 Gate4 原"双因假设"收敛为**单因：数字化读图困难**（该区网格鲁棒、不漏支）。
3. **方向性检验（数字化偏差单/双侧分布）未完成** → 记入 capsule 的"什么没做透"。

## 不改阈值（Gate4 否决选项2）

loci 图无社区先例，SEPR 自定 `median<0.01 / p95<0.03` **保持不动**。benchmark.yaml 标 sr 阈值超标为 **known/accepted**，带 GATE4-决定.md 依据链接。这次"未达标但经独立复算接受"的记录留作后续论文校准基线。

## 待办（step10 → step11，全程 result_class=partial_physical_match）

### step10 summary_and_report
- 双报告（复现结果报告 + skill 蓝图草稿）。
- `benchmark.yaml`：Fig3 loci 复现的 benchmark 数据，sr 阈值超标标 known/accepted + 链 GATE4-决定.md。
- skill 草稿 → 写 `.work/.todo/2401.04146/0703-01-akimov-mie-v1/self-iteration/`，**结束前把 skill 草稿 + 迭代需求扔进 `toEflow/`**（只增不删；toEflow 已有一个 `记忆分层架构-扶正需求.md`）。
- **不跑 replay**（单论文做不到）。

### step11 main_agent_report（收尾）
- `.work/run_manifest.yaml`：run_id/timestamp/case/spawned_agents/fan_out/max_depth_reached/**result_class=partial_physical_match**/retry_fingerprints。
- `.result/<case>/capsule.md`：**强制 100% 产出**（E-flow step01 唯一输入）。含 `processed:false` + 断点清单 + **"什么没做透"（把方向性检验未做透写进去）**。
- 按新规范**增量追加** `WORK_LOG/01-akimov-mie-v1.md`（step05-09 + Gate4 的条目 + 决策台账；只增不改历史）。
- 更新顶层 `WORK_LOG.md` 摘要表该 run 行。
- step11 验收清单含"WORK_LOG 已增量更新"。

## 关键红线（CLAUDE.md）

- **【2026-07-05 新规，先读 CLAUDE.md「模型路由与 codex 委托」节】**：默认 Claude 不亲自读写文件——机械读写/执行委托 codex-MCP（`codex-cli`，sandbox: workspace-write + approval-policy: untrusted，cwd 限 case 文件夹）。**豁免仅两类**：① 你在裁决点亲读 GATE 决定/verifier 输出（不经转述）；② 契约文件（step10 双报告、step11 capsule/run_manifest/WORK_LOG）由你亲写自校。step10 的 benchmark.yaml 条目、产物复校（批量 ls/读）之类机械活发 codex。
- **【malformed 熔断】**：同 session 累计 2 次 tool call 格式错（裸 `<invoke>`/丢前缀/杂 token）→ 立即停、写 handoff、让用户开新对话，绝不硬试第 3 次（自回归级联，见 CLAUDE.md 熔断节）。
- **停 gate 问用户**：即将进 `.result` 时（step11 后停机，等用户确认哪些产物入库）。
- 子 agent spawn 用 allowlist：`Read, Write, Edit, Bash, Glob, Grep, ToolSearch, Skill`（排除 MCP）。执行层无 MCP 是**正常设计**（非 bug），落 `.work/memento-cache/` JSON 由 main 代回灌。
- **硬交付红线**：8 字段报告 + 全部 required_output_paths 产物落盘缺一不算完成。spawn 后 main **独立复校磁盘存在性**（不信 sub 自述——本次 sub 多次自述"全落"与磁盘不符，均因文档阶段截断）。
- **防截断纪律**：sub 单步产物多易触 max_turns=15，spawn 时要求**分批落盘**（每完成一个产物即落，别攒最后）。
- 全程中文 + Markdown，公式 `$...$`。

## 已完成产物清单（复校用）

- **代码** `reproduction_test/mie/code/`：scattering.py(BH核)、akimov_coeffs.py(交叉验证)、crosscheck_bh_vs_akimov.py、fig3_loci.py(求根)、fig3_plot.py、fig3_contour_check.py、fig3_digitize.py、fig3_compare.py(Layer3)、fig3_dist_plot.py、fig3_selfcheck.py
- **数据** `reproduction_test/mie/data/`：fig3_loci_{TM,TE}_l{1,2,3}.csv(六面板 loci,%.17g全精度)、fig3_digitized.csv(1982点)、fig3_layer3_metrics.csv、fig3_selfcheck_perturbation.csv
- **图** `reproduction_test/mie/figures/`：fig3_repro.png、fig3_overlay.png、fig3_contour_check.png、fig3_dist_hist.png（_fig3_src_render.png 是数字化中间物非正式产物）
- **子报告** `.work/.sub-report/`：01/02/03/04/05/06/06T4/08/09 各一份
- **memento-cache** `.work/memento-cache/`：step03/04/05/06/06T4/08/09 JSON（均待/已回灌）
- **step 中间产物**：`.work/.todo/2401.04146/0703-01-akimov-mie-v1/0X-*/` 各步目录

## 核心物理结论速查（写报告用）

- 三 Layer1 verifier 全 PASS：能量守恒 0.0e+00、Rayleigh 斜率4.0001、大尺寸趋势判据末点x=800 |Q-2|=0.0163（CC 改过 verifier 为趋势判据）。
- T2 交叉验证 BH vs Akimov：max|Δa|=2.2e-15 ≪ 1e-12。step05 对抗审查确认 T2 真独立（AST）、符号对教材核正确、a_l/b_l 是 m 偶函数（负ε分支无关）。
- Layer2 论文内自洽：sr max|a-1|=9.3e-9、nr max|a|=9.2e-10、平凡线 eps=1 max|a|=8.6e-15、step03锚点 l=1 TM q_e=1 → eps=-4.640 命中。
- 完备性(Gate2强制)：切片法 vs contour 支数逐面板一致(TM12/12,12/12,11/11;TE12/12,11/11,11/11)，覆盖>99.8%。
- Layer3：全局 median=0.00746(达标)、p95=0.04258(超标) → CONDITIONAL → Gate4 独立求根Δ=0 接受为 partial_physical_match。
- step09：loci 对 5 类数值扰动稳定。
