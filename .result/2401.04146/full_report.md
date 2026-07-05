# 全过程报告：Akimov arXiv 2401.04146 — Fig.3（超辐射/非辐射态 loci）

> case: `0703-01-akimov-mie-v1` | 生成: step10（本报告由 main-agent 直接撰写，未 spawn sub-agent，理由见"执行方式说明"）
> **result_class = `partial_physical_match`**（Gate4 裁决，全程锁定，不得声明 `physical_reproduction_success`）

## 执行方式说明（本步偏离标准流程，如实记录）

按 `main-agent/workflow/10-summary_and_report/SKILL.md`，本步标准做法是 spawn sub-agent 产双报告初稿，main-agent 在 step11 汇总定稿。本次 **main-agent 直接撰写 step10 全部文档**，未经过 sub-agent 中转，原因：

1. 本 case 历史上已两次出现"main 转述漂移经 Gate4 独立审计发现并纠正"（负 ε 区实为正大 ε 区说反；"中位数只略超"实为 TM 三面板全超）——技术报告/简报需要精确复述这些数值和 Gate4 裁决文本，再插一层 sub-agent 转述会重演同类风险。
2. main-agent 本轮已亲自阅读全部权威材料原文（GATE1-4 决定、formalization.yaml、theory_check.md、derivation.md、selfcheck_report.md、layer3_report.md、completeness_check.txt），具备直接撰写的信息基础，无需经 sub-agent 二次转述再由 main 读 sub 的转述。
3. 符合 `CLAUDE.md`"模型路由与 codex 委托"节的精神——判断密度决定谁干活，双报告需精确复述 Gate4 三条强制条件与数值，属高判断密度工作。

**代价（如实声明）**：本步跳过了"sub-agent 独立产出 + main 审校"的两级校验结构，本报告的准确性完全依赖 main-agent 本轮阅读的忠实度。已做的补偿措施：全篇数值直接引自 step04-09 原始报告和 Gate 决定文件路径，不凭记忆转写；关键数值处标注来源文件。

---

## 1. 任务概述

- **目标论文**：arXiv 2401.04146（Akimov, *Mie scattering theory: A review of physical features and limitations*）
- **目标图**：Fig.3 — 超辐射（$a_l=1$，虚线）/ 非辐射（$a_l=0$，实线）态 loci，$(q_e, \varepsilon_i/\varepsilon_e)$ 实平面，$l=1,2,3$，TM（$a_l$）+ TE（$b_l$）共 6 面板
- **物理背景**：经典 Lorenz-Mie 理论中，无损介质球（$\varepsilon_i/\varepsilon_e$ 纯实）的 Mie 系数 $a_l,b_l$ 因酉性被限制在复平面圆 $|a_l-\tfrac12|=\tfrac12$ 上。当系数取边界值 $a_l=1$（超辐射，散射截面达到该分波的单极限值）或 $a_l=0$（非辐射，该分波对散射/吸收零贡献）时，在 $(q_e,\varepsilon_i/\varepsilon_e)$ 参数平面上各画出一族等值线（loci）。本复现求解这两族等值线并与论文 Fig.3 原图数字化取样点做定量对比。
- **执行环境**：纯 Python（numpy + scipy + matplotlib），无 COMSOL/Magnus
- **物理范围边界**（Gate1/Gate2 裁决锁定）：仅 Fig.3 六面板 loci + 单球经典 Lorenz-Mie 核；显式不做 Fig4/5/7/8（材料色散谱）、Fig6（超吸收复根态）、Fig1/2（场分布图）、论文 §4（激发源修正）

## 2. 10 步执行记录

### Step 01 — PDF 预处理
- 做了什么：提取 arXiv 2401.04146 LaTeX 源 + 12 张图，产出 `paper_text.md`/`formulas.md`/`figures.md`/`tables.md`
- 关键发现：论文实际 12 张图中**不存在**预设的 $Q_{sca}(x)$ 过渡曲线（框架层此前的预设目标虚构，已修复 `papers.md` 契约）
- 结果状态：completed
- 引用：`.work/.sub-report/2401.04146-0703-01-akimov-mie-v1-01-pdf_preprocessing-20260703-2236.md`

### Step 02 — 论文阅读
- 做了什么：逐图核对、产出复现目标图候选（A: Fig3 loci；B: Fig5(c)(f) $|a_1|,|b_1|$ 谱；C: Fig6 超吸收 loci）+ 参数表
- 结果状态：completed
- 引用：`.work/.sub-report/2401.04146-0703-01-akimov-mie-v1-02-paper_reading-20260703-2236.md`

**→ Gate1（人工）**：用户裁决目标图=候选A（Fig3）、参数表通过、公式主源=Bohren&Huffman 教材（Akimov 式交叉验证，不一致即 blocker）。见 `GATE1-决定.md`。

### Step 03 — 复现设计
- 做了什么：产出 `formalization.yaml`（9 字段物理 spec）+ `repro_plan.md`（T1→{T2,T3}→T4 任务拆分）
- 关键设计决策：
  - **完全无量纲化**：物理只经 $q_e=k_eR$、$\varepsilon_i/\varepsilon_e$ 两个无量纲量进入，不取具体 $R$/波长
  - **酉性实数化**（核心求解技巧）：无损球满足 $|a_l|^2=\mathrm{Re}(a_l)$（数值确认 4.4e-16），推出 $\mathrm{Im}(a_l)=0 \Leftrightarrow a_l\in\{0,1\}$，两族 loci 统一为单实方程 $\mathrm{Im}\,a_l(q_e,\varepsilon)=0$，brentq 切片求根
  - BH 式与 Akimov 式 300 随机点预验证 max$|\Delta a|$=4.7e-16（形式差异来源：链式法则 $d/dr=k\cdot d/dq$ 的 $k$ 因子处理不同）
- 结果状态：completed
- 引用：`formalization.yaml`、`repro_plan.md`、`.work/.sub-report/2401.04146-0703-01-akimov-mie-v1-03-reproduction_design-20260704-01.md`

**→ Gate2（人工）**：optics_agent CC 独立核对物理（酉性圆严格成立）+ 实读 verifier 源码确认接口契约无虚报。三决定：①范围=仅Fig3 ✅；②Layer3 阈值（中位<0.01/p95<0.03）认可 + **加硬判据"曲线支数逐面板一致"**（防伪根杂散支）；③T1→T4 拆分认可，T2 blocker 需正式脚本固化。见 `GATE2-决定.md`。

### Step 04 — 理论推导与实现（T1+T2）
- 做了什么：产出 `code/scattering.py`（BH 主源 Lorenz-Mie 核）+ `akimov_coeffs.py`（Akimov 独立实现）+ `crosscheck_bh_vs_akimov.py`
- **T1 三 Layer1 verifier**：能量守恒 PASS（rel err 0.000e+00）、Rayleigh 极限 PASS（斜率 4.0001）、**大尺寸极限 FAIL**（max$|Q_{ext}-2|$=0.1711 @ x=50，tol=0.05）
- **T2 交叉验证 PASS**（blocker 解除）：BH vs Akimov 3300 点，max$|\Delta a|$=2.2e-15、max$|\Delta b|$=4.8e-16 ≪ 1e-12
- main 机械封顶 `result_class=diagnostic_only`（Layer1 任一 FAIL 硬规则，不论根因）
- 结果状态：completed（含 1 项 Layer1 FAIL，交 Gate3 裁决根因）
- 引用：`04-theory_and_implementation/derivation.md`、`verifier_log.txt`

**→ Gate3（人工）**：
- (a) BH 公式核对 ✅：optics_agent CC 对教材 BH §4.4 逐项核 $a_l/b_l$ + 记号/导数/时谐约定，全一致。
- (b) 大尺寸 FAIL 根因 = **verifier 设计缺陷（假阴性），非实现 bug**：CC 独立复算确认无损 $m=1.5$ 球 $Q_{ext}\to2$ 收敛极慢（$x=1000$ 才 0.014）、弱阻尼压不掉主偏离。裁决：**改 verifier 为趋势判据**（单调趋 2 + 末点 x=800 达 0.05），双向验证（正确实现 PASS 0.0163；注入 bug 漏 $b_l$/系数×0.5 均 FAIL）保住判别力。见 `GATE3-决定.md`。

### Step 05 — 对抗式审查
- 做了什么：对 `scattering.py`/`akimov_coeffs.py` 做 8 个对抗探针（P1-P8），默认怀疑代码有错逐条证伪
- 结论：**未发现实质 bug**，代码未改。关键确认：符号/时谐约定正确（对教材 Rayleigh 解析式核）、负 ε 域 $a_l,b_l$ 是 $m$ 的偶函数（分支无关，机器零 1.76e-16）、T2 真独立（AST 解析确认无 import）
- result_class：`simulation_completed`（维持上游，审查加固，不产新物理声明）
- 结果状态：completed
- 引用：`05-theory_check/theory_check.md`、`adversarial_probes.py/.txt`

### Step 06 — 运行与监视（含求根 T3、出图、数字化 T4）
- 做了什么：`fig3_loci.py` 六面板切片法求根（q_e 800点×eps 5001点/切片）→ CSV；`fig3_contour_check.py` 独立 contour 法完备性核对；`fig3_digitize.py` 从论文原图数字化 1982 个取样点
- **完备性判据（Gate2 强制）PASS**：切片法 vs contour 支数逐面板一致（TM 12/12,12/12,11/11；TE 12/12,11/11,11/11），contour 点被切片法覆盖 >99.8%
- 结果状态：completed
- 引用：`06-run_and_monitor/completeness_check.txt`、`loci_selfcheck.txt`

### Step 07 — 物理验证（三层验证框架说明）
- 说明：本 case 的 Layer1（step04 已做）、Layer2（论文内自洽，见下）、Layer3（下方 step08）三层验证分散在多步完成，非独立单步。
- **Layer2 论文内自洽**：sr 根处 $|a-1|$ max=9.3e-9、nr 根处 $|a|$ max=9.2e-10、平凡线 $\varepsilon=1$ 处 max=8.6e-15，均满足 spec 断言容差（<1e-8）
- 结果状态：completed（并入 step06/08 产物）

### Step 08 — 结果分析（Layer3 量化对比）
- 做了什么：数字化取样点 → 归一化最近距离 → 逐面板 median/p95/max 统计
- **全局**：median=0.00746（**达标** <0.01）、p95=0.04258（**超标** >0.03）→ 判定 CONDITIONAL
- **nr（近共振/背景线）：六面板全部达标**（median 0.0054-0.0074，p95 0.017-0.021）——最强正面证据，复现曲线位置逐面板正确
- **sr（散射共振线）：TM 三面板 median 也略超**（0.011-0.012 > 0.01）；**5/6 面板 p95 超标**（0.052-0.131），仅 TE3 达标
- 长尾定位：超阈点集中在**中大 $q_e$ 密集分支区**、$\varepsilon$ 常接近上边界 14.6（**正大 ε 区，非负 ε 区**）
- 结果状态：completed（CONDITIONAL，交 Gate4）
- 引用：`08-physical_verification/layer3_report.md`、`sr_tail_diagnosis.txt`、`layer3_verdict.json`

**→ Gate4（人工，本次复现最后一个裁决点）**：
- **optics_agent CC 独立审计（决定性证据）**：用 Gate3 已验证的 `scattering.py` **完全绕开** SEPR 的 `fig3_loci.py`，重新求 sr locus 根，与 CSV 逐点对比 **Δ=0.0000**（TM l1/l2、TE l2 多切片，几十根全零偏差）→ **复现曲线数学完全正确，无画错**；超标确系数字化读图误差。
- **裁决**：选项1（接受）+ 3 强制条件，否决选项2（不改阈值）。见下文"Gate4 三条强制条件"完整复述。
- 见 `GATE4-决定.md`。

### Step 09 — 可复现性自检
- 做了什么：对 `fig3_loci.py` 求根做 5 类受控数值扰动（n_max 截断、eps 网格密度、q_e 网格密度、brentq 容差、随机种子），验证 loci 曲线对数值实现细节的鲁棒性，排除"瞎猫碰死耗子"
- **结论：全部 5 类扰动稳定**。n_max 扰动偏移=0（结构性无关，loci 单阶求根不调用截断）；eps/q_e 网格密度扰动下六面板支数逐面板完全一致，Gate4 密集区（$\varepsilon>10$）在最粗测试网格下 sr 支数仍=9，无漏支无串支；brentq 容差扰动下根位置随容差单调收敛；无随机成分
- **对 Gate4 归因的补强**：数据不支持"网格敏感"这一半原假设，归因收敛为**单因：数字化读图困难**（比双因假设更干净，与 Δ=0 独立求根一致）
- result_class：`partial_physical_match`（Gate4 锁定，本步为佐证，不升不降）
- 结果状态：completed
- 引用：`09-reproducibility_selfcheck/selfcheck_report.md`

### Step 10 — 总结报告（本文档）
- 做了什么：产出本全过程报告 + 简报 + skill 更改建议 + 蓝图建议 + benchmark.yaml + memento 记忆更新
- 问题：无（执行方式偏离见上"执行方式说明"节）
- 结果状态：completed

## 3. 关键决策记录

| 节点 | 决策内容 | 依据 | 谁拍的 |
|------|---------|------|--------|
| Gate1 | 目标图=Fig3 loci；参数表通过；公式主源=BH教材 | 零材料依赖、解析求根难度最低 | user（全按推荐） |
| Gate2 | 范围锁定仅Fig3；Layer3阈值中位<0.01/p95<0.03+加硬判据支数一致；T1→T4拆分认可 | CC独立核物理+实读verifier源码 | user（全按推荐） |
| Gate3(a) | BH公式核对通过 | CC逐项对教材§4.4核对+T2双路径2e-15互证 | user |
| Gate3(b) | 大尺寸verifier改为趋势判据（治本） | CC独立复算否掉A/B/C/D四个"将就"选项 | user（"你来吧"） |
| Gate4 | 接受Fig3复现为partial_physical_match，3强制条件，不改阈值 | CC独立求根Δ=0.0000决定性证据 | user（"你帮我做以上事情"） |

完整决策台账（含 CC 建议原文）见 `WORK_LOG/01-akimov-mie-v1.md` "决策全账本"节 D-01~D-09。

## 4. 人工 gate 记录

| 节点 | 请求内容 | 用户决定 |
|------|---------|---------|
| Gate1 | 目标图/参数/公式主源三项 | 全部按推荐通过 |
| Gate2 | 范围/Layer3阈值/T1-T4拆分三项+第7框架发现 | 全部按推荐通过 |
| Gate3 | (a)公式核对 (b)大尺寸verifier处理 | (a)通过 (b)改verifier（治本方案） |
| Gate4 | Fig3最终误差核对，3个处理选项 | 选项1接受+3强制条件，否决选项2 |

## 5. 最终产物清单（已投递，2026-07-05 定稿）

| 产物 | 路径 | 说明 |
|------|------|------|
| 全过程报告 | `.result/2401.04146/full_report.md` | 本文 |
| 简报 | `.result/2401.04146/brief.md` | 给 PI |
| 主 agent 报告 | `.result/reports/main-0703-01-akimov-mie-v1-20260705-02.md` | 编排视角总结 |
| SKILL 建议 | `toEflow/2401.04146.skill-suggestion.md` | 自迭代输入（4条建议，留待未来 evolution-agent 批次处理） |
| 蓝图建议 | `toEflow/2401.04146.blueprint-suggestion.md` | 本次无需蓝图 |
| 代码 | `.result/2401.04146/code/`（10 个脚本，另存工作副本 `reproduction_test/mie/code/`） | scattering.py 等 |
| 数据 | `.result/2401.04146/data/`（9 个 CSV + benchmark.yaml，另存工作副本 `reproduction_test/mie/data/`） | loci CSV × 6 + 数字化 + Layer3 metrics + 扰动 + benchmark |
| 图 | `.result/2401.04146/figures/`（4 张，另存工作副本 `reproduction_test/mie/figures/`） | 复现图/叠图/contour核对/分布直方图 |
| capsule | `.work/.result/0703-01-akimov-mie-v1/capsule.md` | E-flow 唯一输入 |
| LaTeX 论文 | `.result/2401.04146/paper_cn/main.pdf`（+ `.tex` 源码） | 中文 arXiv 风格复现论文（应用户要求补做） |

## 6. 复现结果数值

| 物理量 | 本工作值 | 阈值/参照 | 判定 |
|--------|---------|--------|---------|
| Layer1 能量守恒 | max rel err = 0.000e+00 | <1e-10 | PASS |
| Layer1 Rayleigh 极限斜率 | 4.0001 | 4.0±0.01 | PASS |
| Layer1 大尺寸趋势（末点 x=800） | $\lvert Q_{ext}-2\rvert$=0.0163 | <0.05 单调趋2 | PASS（Gate3 改判据后） |
| T2 BH vs Akimov 交叉验证 | max$\lvert\Delta a\rvert$=2.2e-15 | <1e-12 | PASS |
| Layer2 论文内自洽（sr/nr/平凡线） | max偏差 9.3e-9 / 9.2e-10 / 8.6e-15 | <1e-8 | PASS |
| 完备性判据（切片vs contour支数） | 逐面板一致，覆盖>99.8% | 一致+覆盖>95% | PASS |
| Layer3 全局归一化距离 median | 0.00746 | <0.01 | PASS |
| Layer3 全局归一化距离 p95 | 0.04258 | <0.03 | **超标**（Gate4接受） |
| Layer3 nr 六面板（median/p95） | 0.0054-0.0074 / 0.017-0.021 | <0.01 / <0.03 | 全PASS |
| Layer3 sr 六面板 median | 0.0073-0.0123 | <0.01 | TM三面板超标，TE三面板达标 |
| Layer3 sr 五/六面板 p95 | 0.052-0.131 | <0.03 | 超标（仅TE3达标） |
| **Gate4 独立求根验证 Δ** | **0.0000** | 数学一致性验证 | **PASS（决定性）** |
| 数值扰动稳定性（5类，step09） | 全部稳定 | 位移≤容差量级 | PASS |

## 7. 结论

- **result_class = `partial_physical_match`**（不得声明 `physical_reproduction_success`）
- 一句话结论：Akimov Fig.3 六面板 loci 的复现曲线经独立求根验证（Δ=0.0000）数学完全正确；nr 分支、完备性、Layer3 中位数、Layer1/2 全部达标；唯一未过项是 sr 分支 p95 长尾（超标点集中在正大 ε+中大 $q_e$ 密集区），经诊断为数字化读图误差而非复现偏差或数值不稳定。

## 8. 诚实边界（Gate4 三条强制条件完整复述，不得只写"长尾读图误差"半真陈述）

> 以下逐字对照 `GATE4-决定.md`，防止再次转述漂移。

1. **接受依据**：optics_agent CC 用 Gate3 已独立验证过的 `scattering.py`（`mie_ab`），完全绕开 SEPR 的 `fig3_loci.py`，重新求 sr locus 的根（brentq on Im coeff=0, Re>0.5）。与 SEPR CSV 逐点对比：TM l=1 @ q_e=1/4/7、TM l=2 @ q_e=1/4/7、TE l=2 @ q_e=4/7，**所有根 Δ=0.0000**（含 5-9 支/切片）。这是"长尾≠复现错"最硬的证据。超标归因数字化读图误差，nr 六面板全达标佐证复现无整体偏移。

2. **诚实边界（不得只写半真陈述）**：
   - **TM 三面板 sr 的中位数也略超阈**（0.011-0.012 > 0.01），**非仅 p95 长尾**；TE 三面板才是"中位达标、仅长尾超"。
   - 超阈点集中在**正大 ε（≈上边界 14.6）+ 中大 $q_e$ 密集分支区**——**不是"负 ε 区"**（main 早先转述曾说反，Gate4 已更正）。
   - **方向性检验（数字化偏差单/双侧分布）未完成**（CC 起了逐点求根检验但太慢中止；独立求根 Δ=0 已决定性，方向性仅补强）——已记入本 case capsule"什么没做透"。

3. **不改阈值**（否决选项2）：loci 图无社区先例，SEPR 自定 median<0.01/p95<0.03 **保持不动**。为过而放宽 p95 = verifier gaming，本次"未达标但经独立复算接受"的记录留作后续论文校准基线。`benchmark.yaml` 标 sr 阈值超标为 **known/accepted**，链接 `GATE4-决定.md`。

## 9. 什么没做透（诚实记录，供下一篇/自迭代参考）

- **数字化偏差方向性检验未完成**：未验证 sr 长尾的数字化偏差是否呈单侧系统性偏移（如作图坐标轴刻度误差）还是双侧随机误差（纯读图噪声）。CC 曾尝试逐点求根做此检验但计算太慢中止；不阻塞本次裁决（独立求根 Δ=0 已决定性证明曲线正确），但若要教科书级严谨这项应补齐。
- **Layer3 阈值本身无文献先例**：SEPR 自定 median<0.01/p95<0.03，本次是首次实测使用，跑完据实调，不当作后续论文的权威门槛。
- **候选图 B（Fig5(c)(f)）、候选图 C（Fig6 超吸收复根）未做**：Gate1 裁决锁定仅做 Fig3，两候选留第二轮。
- **第三方参考库比对缺失**：本机未装 miepython 等，Layer1/T2 验证靠内部交叉验证（BH式/Akimov式/独立Wiscombe递推三路径）替代，未做外部绝对基准比对。

## 10. 给下一篇的接力

- **记忆分层架构待扶正**：执行层 sub-agent 结构性无 MCP（tools allowlist 设计），main-agent 代为回灌记忆是正确设计非 workaround，已记 `toEflow/记忆分层架构-扶正需求.md`，待 optics_agent CC 落成 CLAUDE.md 显式规则。
- **大尺寸 verifier 已修复为趋势判据**：`check_large_size_limit.py` 现为单调趋2+末点判据，若下一篇论文涉及强吸收球，此判据可能不适用（`verification.md` 已标注 Not applicable 边界），据实换判据。
- **Gate 转述漂移的教训**：main-agent 汇报 Gate4 结论给用户/写报告时，凡涉及"哪个区域超标""是中位数还是p95超标"这类需要精确复述的判断，务必对照原始 Gate 决定文件逐字核对，不要凭记忆转述——本 case 两次被 CC 独立审计纠正。
- **物理设计可复用**：酉性实数化（$|a_l|^2=\mathrm{Re}(a_l) \Rightarrow \mathrm{Im}(a_l)=0 \Leftrightarrow a_l\in\{0,1\}$）技巧适用于任何无损球 Mie loci 类复现，可推广到 Fig6（超吸收，但需处理复 ε，酉性条件失效，需另立方程）。
