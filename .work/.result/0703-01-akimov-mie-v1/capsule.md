---
processed: false
run_id: "0703-01-akimov-mie-v1-run01"
case: "0703-01-akimov-mie-v1"
timestamp: "2026-07-05"
result_class: partial_physical_match
evidence_refs:
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE4-决定.md"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE3-决定.md"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE2-决定.md"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/GATE1-决定.md"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/08-physical_verification/layer3_report.md"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/08-physical_verification/layer3_verdict.json"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/09-reproducibility_selfcheck/selfcheck_report.md"
  - "reproduction_test/mie/data/benchmark.yaml"
  - "reproduction_test/mie/data/fig3_layer3_metrics.csv"
  - ".work/.todo/2401.04146/0703-01-akimov-mie-v1/full_report_draft.md"
  - ".work/run_manifest.yaml"
provenance:
  source_artifact: "case 0703-01-akimov-mie-v1 全部 step01-11 产物，2026-07-03 至 2026-07-05"
  evidence_type: "verifier原始输出 + 独立复算(optics_agent CC) + 数值扰动测试 + 人工gate裁决"
  timestamp_version: "20260705-02"
  scope_applicability: "单球经典Lorenz-Mie，纯实ε比(无耗散)，loci类等值线图复现；不适用于含耗散/色散/多层/超吸收态"
  confidence_result_class: "高 / partial_physical_match"
---

# Capsule: Akimov arXiv 2401.04146 Fig.3 复现（SEPR 首次真实论文复现）

> E-flow（自迭代）step01 的唯一输入。`processed: false`，E-flow 消费后置 `true`。

## 一、本次复现结果一句话

Akimov Fig.3 六面板超辐射/非辐射态 loci 复现，经 optics_agent CC 独立求根验证（Δ=0.0000）证实复现曲线数学完全正确；物理硬约束、已知极限、论文内自洽、完备性判据全部通过；论文图定量对比中非共振支（nr）六面板全达标，共振支（sr）中位数部分达标、p95 长尾 5/6 面板超出 SEPR 自定阈值，经 Gate4 裁决归因为数字化读图误差，标记为 known/accepted。**result_class = `partial_physical_match`**，全程未声明 `physical_reproduction_success`。

## 二、六条首跑信号盘逐类核对（对照 memento 已存"SEPR首跑六条信号"，本阶段 step10/11 是否再次触发）

| # | 信号（首跑 step01-02 时发现） | 本阶段(step10/11)是否再触发 | 说明 |
|---|---|---|---|
| 1 | memento MCP 不可用（环境全断联） | **未触发** | 本 session 开工 MCP 预检通过，memory_search/memory_store 全程可用 |
| 2 | 路径自相矛盾（`.work/<case>/` vs `.work/.todo/{paper}/{case}/`） | **未触发** | 本阶段全程使用 canonical 路径 `.work/.todo/2401.04146/0703-01-akimov-mie-v1/`，无歧义 |
| 3 | 预设目标图虚构（论文实际无 $Q_{sca}(x)$ 图） | **未触发（已在 Gate1 前修复并锁定）** | 目标图 Fig3 已由 Gate1 裁决锁定，本阶段不涉及目标图重新判定 |
| 4 | skill 论文描述预写断言错误（papers.md 污染） | **未触发** | papers.md 已在首跑修复批次重写为课程表层，本阶段未再引用论文内容预写描述 |
| 5 | sub-agent 漏交 8 字段报告 / 文档阶段截断 | **本阶段规避，未新增实例，但历史遗留已计入** | step04/05 曾截断（已在 retry_fingerprint 记录并补齐）；step10 本身 main-agent 未 spawn sub-agent（见下"新发现"），故本阶段不存在 sub 截断风险 |
| 6 | verifier 脚本已存在（中性信号） | 不适用（本阶段非 verifier 相关步骤） | — |

## 三、本次运行新发现的信号（本 case 独有，不在原六条信号盘内）

### 信号 7：main-agent 向用户汇报时发生转述漂移（**新增，重要**）

本 case 在 step08→Gate4 期间，main-agent 至少两次向用户呈现 Gate 相关结论时发生转述漂移：
- 把"超标点集中在正大 ε(≈14.6)+中大 q_e 密集区"误转述为"负 ε 陡共振区"（方向说反）；
- 把"TM 三面板 sr 中位数也超阈"漏报，只转述"中位数基本达标只有 p95 长尾超标"（遗漏一半事实）。

两次均由 optics_agent CC 独立审计发现并在 `GATE4-决定.md` 中显式纠正（"纠正 main 转述"字样）。这是 SEPR 框架**编排层自身的转述可靠性问题**，与"子 agent 转述漂移"（已有硬交付红线防护）不同维度——当前框架没有防护"main 向用户汇报时凭记忆转写导致漂移"这一环节。

**处理**：本次 step10 采用一次性变通（main-agent 直接撰写双报告，不经 sub-agent 二次转述，撰写前重新核对全部原始文件）规避第三次漂移；已提交 skill-suggestion 建议1（P0）供 evolution-agent 固化为流程规则。

### 信号 8：Layer3 CONDITIONAL 结果的独立复算验证技巧被临场发明，未固化为标准步骤

Gate4 的决定性证据（独立求根 Δ=0.0000）是 optics_agent CC 临场想到并执行的方法——用已验证的底层核绕开被测上层脚本重新计算，与被测产物逐点比对。这个方法论对本 case 至关重要，但目前不在任何 workflow SKILL 的标准步骤里。已提交 skill-suggestion 建议3。

### 信号 9：loci/等值线类图的 Layer3 度量存在几何放大盲区

归一化最近距离度量在曲线陡峭区域会放大数字化误差的影响（非复现偏差）。本 case 的 sr 长尾即此效应。已提交 skill-suggestion 建议2。

## 四、候选经验（GUIDING / CAUTIONARY / FACT / PROCEDURE）

### GUIDING（成功根因）

1. **酉性实数化技巧**：无损球满足 $|a_l|^2=\mathrm{Re}(a_l)$，推出 $\mathrm{Im}(a_l)=0 \Leftrightarrow a_l\in\{0,1\}$，把两族 loci 等值线统一为单个实方程求根。这是本 case 求解 Fig3 的核心设计决策，把二维 contour 问题降为一维 brentq 切片求根问题，精度和效率都远高于直接二维等值线提取。
   - 适用边界：仅适用于纯实 $\varepsilon$ 比（无耗散）的无损球；含耗散/复 $\varepsilon$（如同论文 Fig6 超吸收态）酉性不成立，需另立方程。
   - provenance: source_artifact=formalization.yaml equations.lossless_unitarity; evidence_type=数值验证(300随机点4.4e-16); timestamp_version=20260704-01; scope_applicability=无损球loci复现; confidence_result_class=高/pipeline_completed(设计阶段)

2. **独立复算验证是打破"数字化误差 vs 代码错误"二义性的最强证据**：当 Layer3 出现部分超标的 CONDITIONAL 结果时，用另一条已验证的独立路径（不同脚本、同一已验证底层核）重新计算被测结果，逐点比对。若 Δ≈0，可决定性证明"复现代码正确，误差在别处"，比单纯的误差机理定性论证强得多。
   - 适用边界：需要已有一个通过 Gate 验证的独立底层核可复用；不适用于没有独立实现路径的情况。
   - provenance: source_artifact=GATE4-决定.md; evidence_type=独立求根Δ=0.0000; timestamp_version=20260705-01; scope_applicability=Layer3 CONDITIONAL裁决场景; confidence_result_class=高/partial_physical_match

3. **数值扰动稳定性自检可有效排除"瞎猫碰死耗子"**：对求根流程的 5 类数值旋钮（截断阶数、网格密度×2、求根容差、随机种子）做受控扰动，验证结果的鲁棒性，是独立于"结果对不对"的"结果是不是巧合"的正交检验。
   - 适用边界：适用于任何数值求根/迭代类复现；对纯解析闭式无迭代过程的计算意义较小。
   - provenance: source_artifact=selfcheck_report.md; evidence_type=5类扰动实测; timestamp_version=20260705-01; scope_applicability=数值求根类复现; confidence_result_class=高/partial_physical_match

### CAUTIONARY（失败教训）

1. **main-agent 向用户汇报会发生转述漂移，需要"复述前重新核对原文"的纪律**：本 case 两次被独立审计发现方向说反/遗漏一半事实。不能假设 main-agent 对早前步骤的记忆转述是准确的，尤其是"哪个方向/哪个子集"这类需要精确指向的判断。
   - 适用边界：所有涉及方向性/范围性数值判断的汇报场景；纯路径引用无此风险。
   - provenance: source_artifact=GATE4-决定.md两处"纠正main转述"标注; evidence_type=人工确认; timestamp_version=20260705-02; scope_applicability=所有SEPR case; confidence_result_class=高/partial_physical_match

2. **verifier 阈值可能对特定物理场景（慢收敛+振荡）设计不当，产生假阴性**：step04 大尺寸极限 verifier 最初用定点阈值判据，对无损球（$m=1.5$）在 Wiscombe/Mie ripple 振荡区产生假阴性 FAIL，被 Gate3 诊断为 verifier 设计缺陷而非实现错误，改为趋势判据后问题解决。教训：verifier 本身需要被验证（双向注入 bug 测试判别力），不能假设"verifier FAIL=实现错"。
   - 适用边界：无损/弱阻尼介质、大尺寸/大阶数收敛较慢的物理量；已在 `verification.md` 标注 Not applicable 边界（强吸收球）。
   - provenance: source_artifact=GATE3-决定.md; evidence_type=CC独立复算+双向注入bug验证; timestamp_version=20260705-01; scope_applicability=大尺寸极限类verifier设计; confidence_result_class=高/simulation_completed

3. **sub-agent 在 max_turns=15 限制下易在"文档写作阶段"截断，代码/数据已落盘但报告文本不全**：本 case step04/05 均出现此模式（自述"全落"与磁盘实际不符）。main-agent 独立复校磁盘是唯一有效拦截手段，不能信 sub 自述。
   - 适用边界：产物数量多、报告篇幅长的 step（如 T1+T2 合并步骤）风险更高。
   - provenance: source_artifact=memento记忆9ce51b69等; evidence_type=磁盘复校对比; timestamp_version=20260704-01至20260705-01; scope_applicability=sub-agent执行步骤; confidence_result_class=高

### FACT（可验证的碎片知识）

1. 无损球 Mie 系数 $a_l, b_l$ 是相对折射率 $m$ 的偶函数：$a_l(-m)=a_l(m)$（负 $\varepsilon$ 比域两个 sqrt 分支给同一系数值，机器精度验证 max 差 1.76e-16）。分支选择在 Fig3 定义域内无风险。
   - provenance: source_artifact=theory_check.md P8; evidence_type=8个对抗探针数值实测; timestamp_version=20260705-01; scope_applicability=负ε比域m纯虚情形; confidence_result_class=高

2. BH 教材式与 Akimov 论文式的形式差异来源：链式法则 $d/dr=k\cdot d/dq$ 的 $k$ 因子处理方式不同（Akimov 显式保留、BH 吸收进 $m$），两式数值等价（3300点 max 差 2.2e-15）。
   - provenance: source_artifact=derivation.md §3; evidence_type=T2交叉验证脚本; timestamp_version=20260704-01; scope_applicability=Lorenz-Mie系数两种等价记号; confidence_result_class=高

### PROCEDURE（可复用执行流程，本 case 仅 1 次，暂不满足 ≥2 case 升 active 的条件）

1. **CONDITIONAL Layer3 结果的独立复算验证流程**：① 识别怀疑对象（复现代码 or 数字化取点）；② 找一个已通过 Gate 验证的独立底层核；③ 用该核走一条完全不经过被测上层脚本的独立路径重新计算目标量；④ 与被测产物逐点比对；⑤ Δ≈0 则决定性排除代码错误，锁定归因为数字化/其他误差源。
   - 使用次数：1（本 case）。按默认流转顺序，暂时 Save，不直接 Absorb 进正式 skill（需 ≥2 case + replay 验证）。
   - provenance: source_artifact=GATE4-决定.md; evidence_type=实操流程; timestamp_version=20260705-01; scope_applicability=Layer3量化对比出现CONDITIONAL结果; confidence_result_class=中(单case)/partial_physical_match

## 五、什么真的断了 / 什么有效（对照信号盘的补充叙述）

**真的断了**：
- main-agent 的转述可靠性（信号7，两次真实事故，非假设）
- sub-agent 在文档写作阶段的产物完整性（信号5的具体表现，已有硬交付红线兜底但仍发生两次，红线是"事后拦截"而非"事前预防"）

**有效的（没断，按预期工作）**：
- 4 个人工 gate 全部按预期停机并获得用户裁决，无一被跳过
- result_class 7级枚举机制全程严格遵守（diagnostic_only→simulation_completed→partial_physical_match 演进逻辑清晰，未出现向上包装）
- 硬交付红线+main独立复校磁盘的"事后拦截"机制本身有效（两次截断均被发现并补齐，未遗漏到最终报告）
- T2 交叉验证/对抗式审查/数值扰动自检等多层独立验证机制协同工作，共同支撑了 Gate4 的高置信裁决
- Layer1/2/3 三层验证框架 + Gate2 强制附加判据（曲线支数一致性）设计合理，成功捕获了"完备性"这一 median/p95 距离度量本身无法覆盖的盲区

## 六、断点清单（如需继续本 case 的后续工作）

- Fig5(c)(f)（$|a_1|,|b_1|$ 材料光谱，需 Ag/Si/SiO2 色散数据）未做，留第二轮
- Fig6（超吸收态复根，酉性条件不成立，需另立方程）未做，留后续
- 数字化偏差方向性检验（单侧系统性 vs 双侧随机）未完成，不阻塞本次裁决但建议后续补齐
- Layer3 阈值（median<0.01/p95<0.03）本身是 SEPR 自定，无社区先例，本 case 记录可作校准基线

## 七、什么没做透（Gate4 强制记入项）

**方向性检验（数字化偏差单/双侧分布）未完成**：optics_agent CC 曾起了逐点求根检验但计算太慢中止；因独立求根 Δ=0.0000 已是决定性证据（证明复现曲线本身完全正确），方向性检验只是补强而非必需，故未阻塞 Gate4 裁决。若后续要做"教科书级严谨"的复现记录，此项应补齐：逐个数字化超阈点求出对应的真实 loci 根位置，计算带符号偏差（而非绝对距离），判断偏差方向是否呈现系统性单侧模式（如作图/印刷/扫描引入的坐标轴系统误差）还是双侧对称的纯读图噪声。

## 八、E-flow 消费提示

- 本 capsule 对应的 skill 草稿见 `toEflow/2401.04146.skill-suggestion.md`（4条建议，P0×1/P1×2/P2×1）+ `toEflow/2401.04146.blueprint-suggestion.md`（无需蓝图）。
- 三级治理归类：本 case 单次 + 有 verifier/独立复算支撑 = **Tier-2**（candidate pending，需人审），不满足 Tier-3 Absorb 条件（需 ≥3 case + replay）。
- 本 case 是 SEPR 框架的**首次真实论文复现**，多条经验缺少跨 case 验证，evolution-agent 处理时应偏保守（Save/Improve 为主，避免单 case 就 Absorb 进正式 skill）。
