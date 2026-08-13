# 光学组组会交接稿：论文复现线

更新时间：2026-07-09

> 本稿主线是**论文复现结果和下一步需要光学组配合的内容**。SEPR/workflow/agent 框架只在解释“为什么进度慢”和“主要成果”时简要带过，会上仍建议把重点放在“目前复现了什么、没有复现什么、卡在哪里、需要什么输入”。

## 0. 开场一句话

这段时间我们跑了两条论文复现线：

1. **Akimov 2401.04146 的 Mie Fig.3**：纯 Python 解析复现，Fig.3 六面板 loci 已完成，底层物理约束和独立复算都通过；但论文图数字化长尾误差仍超出我们自定阈值，所以口径是 `partial_physical_match`，不是整篇论文完全复现成功。
2. **Degiron 2009 NJP Fig.3**：COMSOL/Magnus 链路、日志、CSV、图和诊断流程已经打通，但 full-vector Wave Optics/RF mode analysis 仍没有跑出可信 `neff`；目前不是物理复现成功，核心 blocker 是缺一个 COMSOL 6.3 GUI 导出的最小 mode-analysis 模板。

后续如果条件允许，可能需要组里协助提供一个**最小可运行的 COMSOL 2D mode-analysis `.java` 或 `.mph` 模板**，以及每篇论文的标准参数/边界/验证信息。这样可以减少继续手写猜 COMSOL Java API 的不确定性，把时间更多放在物理复现和验证上。

## 1. 当前复现状态总表

| 论文/目标图 | 方法 | 当前状态 | 能说什么 | 不能说什么 |
|---|---|---|---|---|
| Akimov 2401.04146 Fig.3 | Lorenz-Mie 解析公式 + Python 求根 | `partial_physical_match` | Fig.3 曲线数学复现正确；物理硬约束、公式交叉验证、完备性、非共振支定量对比均通过 | 不能说整篇论文已完全复现；不能说 `physical_reproduction_success` |
| Degiron 2009 NJP Fig.3 v1 | COMSOL Java + Magnus | `surrogate_fallback` | 跑通了提交、日志、stdout-to-CSV、出图流程 | 不能说是 COMSOL 物理复现，最终图是 fallback |
| Degiron 2009 NJP Fig.3 v2 | COMSOL 标量 PDE 诊断 + SU-8 mode probe | `diagnostic_only` / 物理复现未完成 | 定位到 full-vector mode-analysis 设置是 blocker；孤立 SU-8 模型能进 eigensolver 但 matrix factorization failed | 不能说恢复了反交叉，也不能说 `Im(neff)` 可信 |

## 2. 为什么进度看起来比较慢

这里建议会上主动解释，不然容易被理解成“只复现了几张图”。慢的原因主要有四类。

### 2.1 前期做 workflow / agent 框架花了很久

前期不是直接从某一篇论文开算，而是先搭了一套“论文复现 agent”框架。这个过程经历了 V1、V2、V3 三版：

- **V1：可自迭代 DSL / workflow 设想**。一开始想做更自由的 DSL 和自演化 workflow，让系统自己改拓扑、改流程、改经验层。后来通过风险审查发现自由度过高：容易 reward hacking、拓扑漂移、记忆污染、把 pipeline 成功误判成物理成功，也不适合当前“小规模、强人审、强物理验证”的科研复现项目。因此 V1 进入远期归档，不作为当前执行方案。
- **V2：固定拓扑 workflow runner 方案**。V2 把拓扑写死，agent 只在不确定断点介入，确定性检查尽量脚本化，自迭代只碰 skill / 提示词备注，所有关键改变过 human gate。这个设计解决了 V1 自由度过大的问题，但后来判断如果自己再实现一套 workflow runner，工程成本仍然高，而且真实复现还没跑通，继续加治理会偏离目标。
- **V3：当前采用的 SEPR Claude 三层子 agent 方案**。最终没有先造完整 runner，而是用 Claude Code 的 main-agent / sub-agent / leaf 三层结构跑复现；核心防线是固定 10 步复现流程、人工 gate、deterministic verifier、7 级 `result_class`、run manifest、capsule、失败记录和 skill 候选。这个方案的目标不是展示 agent 框架，而是让论文复现过程更可审计、可复查、可沉淀。

所以前期慢，是因为先建立了“怎么复现才不容易自欺欺人”的基础设施。现在已经开始把重心转回具体论文复现。

### 2.2 Claude / 中转站 / 工具链不稳定

实际运行中，Claude Code 和相关中转链路有过几类不稳定：

- 长上下文下偶发 tool-call 格式错误，一旦出错会污染后续对话，需要熔断开新 session。
- MCP / memento 等工具链曾出现整批断联，导致记忆检索和存储需要降级处理。
- 子 agent 在长报告阶段会出现输出截断或“自称完成但磁盘不完整”的情况，需要主 agent 再逐项核磁盘。
- 模型、启动方式和 agent frontmatter 之间也踩过坑，例如 `/skill` 不会自动切 agent model，必须明确用正确启动方式。

这些问题本身不属于光学物理，但会直接影响复现链路的可靠性，因此花了不少时间修复和加红线。

### 2.3 每篇论文都需要人工确认“是否真的复现正确”

论文复现不是代码跑通就结束。每篇论文都要区分：

- workflow / pipeline 是否完成；
- COMSOL job 或 Python 程序是否成功运行；
- 物理结果是否真的复现论文；
- 如果没复现，是参数缺失、模型简化、数值错误、读图误差，还是论文描述本身不充分。

Akimov Fig.3 的例子里，代码能画图还不够，还要做 BH 教材公式核对、Akimov 公式交叉验证、物理极限验证、曲线支数完备性、论文图数字化对比、独立重新求根。Degiron 的例子里，COMSOL job 成功也不够，因为 `.mph` 生成和平台成功不等于 mode-analysis 物理结果可信。

这类判断目前必须有人审和物理复核，不适合完全自动放行。

### 2.4 个人原因

还有一部分是个人时间和精力安排原因。这个会上口述即可，文档里不展开。

## 3. 主要成果

### 3.1 Agent 系统 skill 和复现流程

已经沉淀出一套可继续迭代的 agent 复现系统：

- **main-agent / sub-agent / leaf 三层执行结构**：main-agent 负责编排和 gate 汇总，sub-agent 执行具体步骤，leaf 做更小的局部任务，避免无限递归。
- **10 步论文复现流程**：PDF 预处理、论文阅读、复现设计、理论与实现、理论审查、运行与监控、物理验证、结果分析、可复现性自检、总结报告，另有 main-agent 最终报告。
- **4 个人工 gate**：目标图与参数确认、formalization / spec 确认、核心公式确认、最终误差与 result_class 确认。
- **7 级 `result_class`**：强制区分 `pipeline_completed`、`diagnostic_only`、`surrogate_fallback`、`partial_physical_match`、`physical_reproduction_success` 等状态，避免把流程跑通说成物理成功。
- **项目 skills**：Mie 解析复现、COMSOL batch、COMSOL Java API、Magnus 平台、论文复现报告等 skill 已经作为项目知识入口存在；后续每篇论文的经验会继续整理成可复用 skill。

一句话：目前最重要的成果不是“agent 会自动写很多字”，而是把论文复现拆成可审计的步骤、产物、验证和人工裁决。

### 3.2 已形成的论文复现报告和后续 skill

目前已有的复现产物包括：

- **Akimov 2401.04146 Fig.3**：完整复现报告、简报、代码、数据、图、benchmark、capsule，以及一份中文 LaTeX 复现论文草稿。该 case 已形成 Mie loci 复现经验，后续会整理为 Akimov / Mie 相关 skill。
- **Degiron 2009 NJP Fig.3 v1**：COMSOL/Magnus 端到端 rehearsal 报告，记录了 Java sandbox、stdout-to-CSV、surrogate fallback 的完整链路和失败原因。
- **Degiron 2009 NJP Fig.3 v2**：更诚实的 scalar diagnostic + isolated SU-8 mode-analysis probe 报告，明确把 blocker 缩小到 COMSOL full-vector mode-analysis 设置。
- **复现标准答案模板**：已经整理出希望光学组提供的 geometry、materials、physics、boundary、mesh、solver、sweep、validation、failure notes 信息格式。

后续还会把几篇论文的经验沉淀成更正式的 paper-specific / method-specific skill，例如：

- Akimov / Mie loci 复现 skill；
- Mie 材料色散谱复现 skill；
- Degiron / COMSOL mode-analysis 排障 skill；
- COMSOL GUI-export template 到自动扫参模型的转换 skill。

## 4. 以第一篇 Akimov Fig.3 为例：我们到底在干什么

这里建议会上重点讲：我们不是让 agent “读完论文然后自动画图”，而是把一篇论文复现拆成**可审计的步骤、硬产物、验证器和人工 gate**。首篇 Akimov 2401.04146 Fig.3 的完整流程如下。

| 节点 | 做了什么 | 为什么重要 |
|---|---|---|
| Step 01 PDF 预处理 | 提取 arXiv LaTeX 源、正文、公式、12 张图和逐图清单。首跑发现预设的 $Q_{sca}(x)$ 目标图根本不存在。 | 防止框架层凭印象指定虚构目标；论文有哪些图必须先从原文落盘。 |
| Step 02 论文阅读 | 逐图列出候选复现目标、参数表、缺失信息和目标图候选：Fig.3 loci、Fig.5(c)(f) 材料谱、Fig.6 超吸收复根。 | 把“复现哪张图”变成可裁决的候选，而不是 agent 自己拍脑袋。 |
| Gate1 人工裁决 | 人选 Fig.3 loci；参数表通过；公式主源指定为 Bohren & Huffman 教材，Akimov 公式只做交叉验证。 | 防止目标漂移；同时把公式权威源提前锁住，不让后面实现时自由发挥。 |
| Step 03 复现设计 | 写 `formalization.yaml` 和 `repro_plan.md`；确定无量纲变量 $q_e=k_eR$、$\varepsilon_i/\varepsilon_e$；利用无损 Mie 系数酉性，把 $a_l=0/1$ loci 化成实方程求根。 | 把物理问题形式化为可实现、可检查的数学任务。 |
| Gate2 人工裁决 | 独立核对物理 formalization 和 verifier 接口；确认只做 Fig.3；认可 Layer3 阈值，但加硬判据“曲线支数逐面板一致”。 | 防止最近距离误差掩盖伪根/漏根；也明确阈值是 SEPR 自定，不是社区标准。 |
| Step 04 理论与实现 | 实现 `scattering.py`、`akimov_coeffs.py`、交叉验证脚本；BH vs Akimov 3300 点差异约 $10^{-15}$；初版大尺寸 verifier 报 FAIL。 | 先建立可运行的 Mie 核；同时让 verifier 自身也接受审查，而不是盲信脚本。 |
| Gate3 人工裁决 | 独立核对 BH 教材公式；判定大尺寸 FAIL 是 verifier 假阴性，不是实现 bug；把判据改成趋势收敛并做双向注错验证。 | 说明 gate 不只是“批准继续”，还会修正错误验证器，防止正确实现被误杀。 |
| Step 05 对抗式理论审查 | 8 个 probe 默认怀疑代码错，检查符号/时谐、负介电常数分支、实现独立性等，未发现实质 bug。 | 用反向审查降低“代码能跑但公式错”的风险。 |
| Step 06 运行与监控 | 切片法求六面板 loci，独立 contour 法检查支数，数字化论文 Fig.3 原图 1982 个取样点。 | 生成结果，同时留下独立完备性证据和论文图对比基准。 |
| Step 07 物理验证 | Layer1/Layer2/Layer3 分散完成：能量守恒、Rayleigh、大尺寸趋势、论文内自洽、图像定量对比。 | 把“程序运行成功”和“物理结果可信”分开验证。 |
| Step 08 结果分析 | 全局 median=0.00746 通过，p95=0.04258 超标；非共振支全通过，共振支长尾超标。 | 如实暴露边界，而不是只挑通过的指标汇报。 |
| Gate4 人工裁决 | optics_agent 独立绕开原求根脚本重新求 sr roots，和 SEPR CSV 逐点对比 $\Delta=0.0000$；接受为 `partial_physical_match`，不改阈值。 | 最终 result_class 由独立物理复算决定，防止把阈值放宽成 verifier gaming。 |
| Step 09 可复现性自检 | 扰动截断、网格密度、求根容差、随机种子，结果稳定；归因收敛为论文图数字化读点困难。 | 排除偶然数值碰巧，确认曲线本身稳健。 |
| Step 10 总结报告 | 写全过程报告、简报、skill 建议、benchmark；因 Gate4 涉及高精度复述，本次由 main-agent 直接对照原始文件撰写。 | 把 case 变成后续可复查、可沉淀的经验包。 |
| Step 11 交付封装 | 写 run manifest、capsule、`.result/2401.04146/` 自包含交付包，并额外生成中文 LaTeX 复现论文。 | 让下一次复现、自迭代和人工汇报都有统一入口，不需要翻长对话。 |

这一套流程的核心价值是：**每一步都有文件产物，每个不确定判断都有 gate，每个“成功”都有 result_class 边界**。所以最后的说法不是“agent 复现成功了”，而是“Akimov Fig.3 的曲线经独立求根确认正确，但仍标为 `partial_physical_match`，因为论文图数字化长尾误差未完全消除”。

## 5. Akimov Mie Fig.3：已经做到什么

### 目标

复现 Akimov 2401.04146 Fig.3：无损介质球中超辐射态 $a_l=1$ 和非辐射态 $a_l=0$ 在 $(q_e,\varepsilon_i/\varepsilon_e)$ 平面上的 loci。包括 TM/TE、$l=1,2,3$，共 6 个面板。

### 方法

- 使用 Bohren & Huffman 教材的 Lorenz-Mie 系数作为主公式源。
- 用 Akimov 论文里的等价公式做交叉验证。
- 对无损球利用酉性关系，把 $a_l=0/1$ 或 $b_l=0/1$ 的 loci 统一成实方程求根。
- 全部是 Python 解析/半解析计算，不涉及 COMSOL/Magnus。

### 关键结果

- 物理硬约束全部通过：能量守恒、Rayleigh 极限、大尺寸极限趋势。
- BH 教材公式与 Akimov 公式交叉验证通过，最大差异约 $10^{-15}$ 量级。
- 曲线完备性通过：切片求根与独立 contour 检查的支数逐面板一致，覆盖率大于 99.8%。
- 论文图定量对比：
  - 全局 median 误差通过；
  - 非共振支 6 个面板全部通过；
  - 共振支的 p95 长尾 5/6 面板超出自定阈值，TM 三个面板的中位数也略超。
- 最关键证据：用已验证的底层 Mie 核，绕开原求根脚本重新独立求根，和复现 CSV 逐点对比，差异 $\Delta=0.0000$。这说明曲线本身数学正确，长尾超标主要来自论文图人工数字化读点困难。

### 诚实边界

- 口径是 `partial_physical_match`。
- 本次只做 Fig.3，不包括材料光谱图、超吸收复根图或整篇论文所有图。
- 误差阈值 median < 0.01、p95 < 0.03 是项目自定，非领域公认标准。
- 数字化误差是否存在单侧系统偏差还没有补完；但独立求根已经足以支持“复现曲线正确”这一结论。

### 可展示产物

- 复现简报：`.result/2401.04146/brief.md`
- 全过程报告：`.result/2401.04146/full_report.md`
- 自包含交付包：`.result/2401.04146/`
- 复现图与叠图：`.result/2401.04146/figures/`
- 中文 LaTeX 复现论文：`.result/2401.04146/paper_cn/main.pdf`

## 6. Degiron 2009 NJP Fig.3：已经做到什么、卡在哪里

### 目标

复现 Degiron 2009 NJP Fig.3：在介质波导 / 长程等离激元定向耦合器中扫描 BCB 总厚度 $t$，计算两个耦合本征模式的复有效折射率：

$$
n_\mathrm{eff}=k_z/k_0
$$

论文目标现象是在 $t \approx 5.6\,\mu\mathrm{m}$ 附近出现模式反交叉 / 杂化。

### 已经打通的工程链路

- COMSOL runtime image 能在 Magnus 上运行。
- Java 模型能通过 batch 编译与提交。
- 能保存 `.mph`。
- 能从 stdout 提取 CSV。
- 能自动生成图和报告。
- 失败日志、job id、参数表、缺失信息表都能稳定落盘。

这些证明的是**执行链路可用**，不是物理复现成功。

### v1 结论

v1 最终出了类似反交叉的曲线，但标记为 `surrogate_fallback`。它证明了流程和后处理可以跑通，但不是 COMSOL full-vector mode analysis 的真实结果，不能作为论文 Fig.3 的物理复现。

### v2 结论

v2 做了两个更诚实的诊断：

1. 标量 TM-like PDE sweep 可以跑完整，但 `Re(neff)` 偏低，`Im(neff)` 基本为 0，没有恢复论文的小 $t$ 损耗趋势和反交叉。
2. 单独做孤立 SU-8 Wave Optics/RF mode-analysis probe：模型能编译、显式 mesh 能过、能进入 eigensolver、能保存 `.mph`，但输出 0 行 `neff`，原因是 eigensolver matrix factorization failed。

因此 v2 的最好表述是：

> v2 复现了工作链路并把 blocker 缩小到 COMSOL mode-analysis 设置，但没有物理复现 Fig.3。

### 当前 blocker

当前卡点不是 Magnus、license、镜像，也不是 CSV 后处理，而是 COMSOL 6.3 Wave Optics/RF 里 2D mode-analysis 的正确设置。手写 Java API 可以造出物理接口和 study，但 solver sequence、边界/PML、传播方向、mode search shift、结果表达式等很可能不完整或不正确。

继续靠手写猜 API 已经不合算。最有效的输入是一个 GUI 里搭好的最小可运行模型，然后导出 `.java` 或直接给 `.mph`。

## 7. 后续可能需要的协助

### A. 最小 COMSOL mode-analysis 模板

如果组里同学方便，后续希望能参考一个在 COMSOL 6.3 GUI 里搭好的最小模型，并导出 `.java` 或 `.mph`：

- 2D 横截面 mode analysis。
- 传播方向明确为 $z$。
- 波长 $1.55\,\mu\mathrm{m}$。
- 结构可以先用矩形 dielectric waveguide，不需要一上来做 Degiron 全结构。
- 能输出一个可信的 $n_\mathrm{eff}$ 或 $\beta$。
- 模型中包含 physics interface、study、solver sequence、search shift、mode count、边界/PML、mesh、result expression。

这个模板的作用不是直接复现 Degiron，而是作为“已知可运行的 COMSOL mode-analysis 语法样板”。后续 agent 可以基于模板改几何、材料和 sweep。

### B. Degiron Fig.3 的领域确认

需要组里确认这些信息：

- BCB 总厚度 $t$ 的定义和坐标原点。
- Au stripe、SU-8 waveguide、gap、垂直位置的几何解释是否正确。
- SU-8 是否可用矩形近似，还是必须按论文/实验真实截面。
- BCB、SiO2、SU-8、Au 在 $1.55\,\mu\mathrm{m}$ 的材料参数来源。
- 外部区域用 PML、scattering boundary 还是 finite window；域尺寸推荐多少。
- mesh 在 Au 薄层、gap、界面附近的推荐尺度。
- mode search shift 该用 $n_\mathrm{eff}$ 还是 $\beta$；shift 大概给多少。
- symmetric/anti-symmetric 两支应该用什么 field profile 或能量积分规则分类。
- 孤立 SU-8 和孤立 Au LR-SPP 各自大概的 $n_\mathrm{eff}$ 和损耗范围。

### C. 后续 Mie 复现优先级

Akimov Fig.3 已做完第一轮。下一步可以二选一：

- Fig.5(c)(f)：材料色散下的 $|a_1|, |b_1|$ 谱。需要 Ag、Si、SiO2 等材料色散数据源。
- Fig.6：超吸收态复根。物理更有意思，但酉性简化不再适用，需要另立复数求根方程。

这里也希望听取组里的判断：哪一个更适合作为下一轮复现目标。

## 8. 希望以后每篇复现任务给的“标准答案”格式

为了避免 agent 猜参数，建议每篇论文复现前让熟悉方向的同学按下面模板给一页信息：

```text
figure_id:
physical_goal:
geometry:
  coordinate_system:
  layer_stack:
  object_coordinates:
  uncertain_dimensions:
materials:
  wavelength:
  complex_indices_or_permittivities:
physics:
  interface_or_equation:
  dependent_fields:
  propagation_direction:
  eigenvalue_or_observable:
boundaries:
  exterior_domain_size:
  PML_or_scattering_boundary:
  substrate_truncation:
mesh:
  metal_max_element:
  gap_max_element:
  bulk_max_element:
solver:
  study_type:
  mode_count_or_time_steps:
  search_shift_or_frequency:
  tolerances:
sweep:
  parameter:
  points:
validation:
  expected_numeric_range:
  expected_trend:
  target_plot:
failure_notes:
  common_solver_errors:
  acceptable_simplifications:
```

重点不是写长理论解释，而是给 agent 能直接生成模型、发现错误、迭代修正的约束。

## 9. 组会上建议这样讲

### 2 分钟版

> 我这次不先讲 workflow，只讲论文复现进展。现在有两条线：第一条是 Mie/Akimov，纯 Python 解析复现已经把 Fig.3 六面板 loci 跑通，底层物理硬约束、公式交叉验证、曲线完备性和独立复算都通过；但因为论文图数字化长尾误差超出我们自定阈值，所以诚实口径是 partial physical match，不说整篇成功。第二条是 Degiron COMSOL，Magnus/COMSOL 执行链路已经打通，但 full-vector mode analysis 没有成功，v1 是 surrogate fallback，v2 是 scalar diagnostic。现在真正缺的是 COMSOL 6.3 GUI 导出的最小 mode-analysis 模板。希望组里能给一个 2D dielectric waveguide 在 1.55 微米下能输出 neff 的 `.java` 或 `.mph`，后面 agent 再基于它改几何和扫参。

### 如果老师问“为什么进展这么慢”

回答：

> 前面慢主要不是在单篇论文上卡住，而是先把复现系统的红线搭起来了。V1 过于自由，容易变成自演化 workflow；V2 固定拓扑但自己实现 runner 成本偏高；现在 V3 收敛成 Claude 三层子 agent 加人工 gate 和 deterministic verifier。再加上 Claude 中转链路和工具调用不稳定，以及每篇论文都必须人工判断“物理上是不是真的复现”，所以进度慢一些。个人时间原因我也单独口头说明。

### 如果老师问“主要产出是什么”

回答：

> 主要产出有两类。第一类是 agent 复现系统本身，包括 main/sub/leaf 的 skill、10 步复现流程、4 个 gate、result_class 和报告模板。第二类是具体论文复现产物：Akimov Fig.3 的完整报告、代码、数据和图；Degiron v1/v2 的 COMSOL 诊断报告和失败链路。后续我会把这些经验继续整理成 paper-specific 和 method-specific skill。

### 如果老师问“现在到底成功了吗”

回答：

> Akimov Fig.3 这张图可以说已经做到部分物理匹配，曲线本身经独立复算确认正确；但不是整篇论文全成功。Degiron 还没有物理复现成功，只是把工程链路和失败位置打通了。我们现在非常清楚卡在 COMSOL mode-analysis 设置，而不是平台或后处理。

### 如果老师问“为什么需要组里协助”

回答：

> 因为 COMSOL GUI 里正确的 Wave Optics/RF mode-analysis 设置有很多隐式 solver sequence 和 feature tag，单靠手写 Java 去猜这些设置不太稳。一个最小 GUI 导出的可运行模板，能帮助我们对齐正确的 physics/study/solver/result 写法，后续自动化和扫参才更有依据。

## 10. 下一步建议

1. **短期优先**：拿到 COMSOL 6.3 最小 mode-analysis 模板。
2. **Degiron 复现顺序**：孤立 SU-8 waveguide 先出可信 `neff`；再做孤立 Au LR-SPP；再做 Au+SU8 两点 smoke；最后做完整 $t$ sweep 和 branch classification。
3. **Mie 第二轮**：由组里选 Fig.5(c)(f) 或 Fig.6；如果做材料谱，先固定材料色散数据源。
4. **报告口径保持三态分开**：流程跑通、COMSOL job 跑通、物理复现成功必须分开说。

## 11. 内部证据路径

- Akimov 最终交付：`.result/2401.04146/`
- Akimov 详细记录：`WORK_LOG/01-akimov-mie-v1.md`
- Akimov 全过程报告：`.result/2401.04146/full_report.md`
- Degiron v1 报告：`../optics_agent/reproduction_test/private/Degiron_2009_NJP_Fig3/final_report.md`
- Degiron v2 报告：`../optics_agent/reproduction_test/private/Degiron_2009_NJP_Fig3_v2/final_report.md`
- Degiron 给 PI 的短汇报：`../optics_agent/reproduction_test/private/Degiron_2009_NJP_Fig3_v2/pi_wechat_update.md`

> 对外转发前建议删掉或改写内部相对路径，保留结论和请求即可。
