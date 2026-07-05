# SEPR 项目状态总览

> 本文给用户和未来 agent 快速了解 `self-evo-paper-repro` 工作区现状。细节以 `CLAUDE.md`、`.human/DESIGN.md` 和各 skill 为准。

## 1. 工作区一句话定位

SEPR = 光学论文复现自进化 agent，`.human/` 是中文审查稿，`.claude/skills/` 是中文详细执行版（4 身份约 6465 行已完成），采用 4 agent 架构：复现 workflow 的 `main-agent` + `sub-agent`，自迭代 workflow 的 `evolution-agent` + `sub-E-agent`。英文 prompt-engineered 版是可选后期优化。

## 2. 当前阶段

当前处于设计阶段完成、准备进入首轮执行的状态：`.human/` 已经形成完整项目计划，`.claude/skills/` 中文详细执行版已完成并用于 agent 实际运行。`.human/` 与 `.claude/` 不是逐字镜像；关键协议字段（result_class、路径、报告 schema、human gate）必须双写同步。

近期启动点是 Mie 第一阶段：教材与 11 篇论文已就位，等待用户确认/发话后启动第一篇或第一组 Mie 复现。

> **近期变更（2026-07-03，见 WORK_LOG 阶段十一）**：落地 V3 加固基础版——叶子层硬化（新增 `sub-leaf`/`sub-e-leaf` agent）、4 agent `skills:` 预加载；**撤销 OpenCode**（删 `opencode.json`/`.opencode/`，`AGENTS.md` 降 stub，三文件同步约束取消，仅面向 Claude Code；Opus 不稳应急改 URL/API 指向 DeepSeek）。hooks 与 disable-model-invocation 搁置到 Mie 跑通后。

## 3. 4 agent 架构表

| workflow | 编排者 | 执行者 | 步数 |
|---|---|---|---|
| 复现 | `main-agent` | `sub-agent` | 10 步 + 第 11 步主 agent 报告 |
| 自迭代 | `evolution-agent` | `sub-E-agent` | 5 步 + 第 6 步 evolution-agent 报告 |

说明：执行者可以再 spawn 子子 agent 做单点小任务，但第 3 层不再继续 spawn。

## 4. 关键机制

- **spawn 模版拼接**：spawn 子 agent 时由全局模板、局部任务模板和主 agent 对任务的理解拼接成完整任务单。
- **subsubagent（叶子层，2026-07-03 硬化）**：sub-agent / sub-E-agent 用 `subagent_type: sub-leaf` / `sub-e-leaf` 调第 3 层叶子——叶子定义的 `tools` 不含 `Agent`，从框架层即无法再 spawn（不再靠 prompt 软约束）。
- **六维裁决 + 三级治理**：经验裁决从 Save/Improve/Absorb/Drop 扩展为 Save/Improve/Absorb/Fork/Archive/Drop，并用 Tier-1/2/3 控制进入 skill 的证据门槛。
- **validate_and_replay**：selective replay 分层 A/B/C；E-flow 不调 W-flow，核心方法变化标注需人工开 W-flow 重跑。
- **经验 4 type**：经验分为 GUIDING、CAUTIONARY、FACT、PROCEDURE，分别进入提示词备注、pitfalls、memento fact 或 skill candidate。
- **toEflow/ 缓冲**：workflow 到 evolution 的缓冲区只增不删，单论文 workflow 只提交草稿和迭代需求，不自行启动自迭代。
- **.E-history/**：每次 evolution 结束写详细自迭代报告，按次数排序保存。
- **记忆**：每个 agent 开始前搜索 memento，结束前更新 memento / decisions / pitfalls，避免重复劳动并保留 provenance。
- **tools 控制**：子 agent 使用 allowlist 模式限制工具暴露，`ToolSearch` 必须包含，避免 MCP 描述撑爆上下文。
- **蓝图扫描泛用能力**：蓝图模板支持 Annotated 参数和 `scan_parameters` 字段，不再只绑定单篇论文或单张图。

## 5. 目录结构（精简版）

```text
self-evo-paper-repro/
├── .paper/                 # 教材 + 论文原文区，只读不污染
│   ├── scattering.pdf       # Bohren & Huffman 教材
│   └── mie/                 # 11 篇 Mie 论文
├── .work/                  # agent 工作沙箱，中间产物和报告
├── toEflow/                # workflow -> evolution 缓冲，只增不删
├── .E-history/             # evolution 历史报告，按次数排序
├── .result/                # 最终交付区，由主 agent 确认后复制
├── todo.md                 # 全局日志，每次 workflow/Eflow 结束前追加
├── .human/                 # 中文审查稿，人读
├── .claude/                # 中文详细执行版，agent 运行时读
├── papers/                 # junction 到 optics_agent/papers
└── reproduction_test/      # junction 到 optics_agent/reproduction_test
```

## 6. 已完成 vs 待完成

### 已完成

- 建立 SEPR 独立工作区定位：隔离 optics_agent 的 coding 上下文，专门跑论文复现 + skill/蓝图自进化实验。
- 完成 `.human/DESIGN.md` 顶层设计，明确 `.human/` 是中文审查稿、`.claude/skills/` 是中文详细执行版，英文版为可选后期优化。
- 确定 4 agent 架构：复现 `main-agent` / `sub-agent`，自迭代 `evolution-agent` / `sub-E-agent`。
- 确定三层 spawn 规则：编排者不做隔离活，执行者可 spawn 子子 agent，第 3 层不再 spawn。
- 确定 workflow 与 E-flow 隔离：W-flow 产 capsule 和草稿，E-flow 批量治理，不互相递归调用。
- 完成经验治理设计：4 type 经验、六维裁决、三级治理、selective replay A/B/C。
- 完成目录与留痕约定：`.work/`、`toEflow/`、`.E-history/`、`.result/`、`todo.md`。
- 完成 Mie 第一阶段基础准备：`.paper/scattering.pdf` 教材、`.paper/mie/` 11 篇论文、Mie 计划与 skill 已就位。

### 待完成

- 可选后期优化：把 `.claude/skills/` 中文详细执行版再优化为英文 prompt-engineered 版（非当前阻塞项）。
- 启动 Mie 第一阶段实际复现，跑通第一篇/第一组论文的 10 步 workflow。
- 建立初期 replay set，先用 1-2 个旧 case 跑通 validate_and_replay。
- 治理 `.claude/skills/` 旧内容，并决定领域 skill 的放置方式；关键协议字段与 `.human/skills/` 双写同步。

## 7. 如何开始 Mie 第一阶段

- 教材在 `.paper/scattering.pdf`，作为 Mie 系数和核心公式的主源。
- 11 篇 Mie 论文在 `.paper/mie/`，用于第一阶段论文复现与 benchmark 建立。
- 计划在 `.human/skills/optics-mie-reproduction/` 和 `reproduction_test/mie/mie_reproduction_plan-CN.md`。
- 用户说“复现 XXX.pdf”时，入口身份选择 `main-agent`，加载复现编排 skill 后进入 10 步 workflow。
- 复现中保留 4 个人工 gate：参数核对、formalization 核对、公式核对、误差核对。
- PyMieScatt 已弃用，Mie 结果用 3 层物理检验：物理硬约束、Rayleigh/大尺寸极限退化、论文图量化对比。
- **首跑状态（2026-07-04）**：Akimov case `0703-01-akimov-mie-v1` 已完成 step01-02，产物在 `.work/.todo/2401.04146/0703-01-akimov-mie-v1/`。首跑 6 条信号及修复批次见 `WORK_LOG.md` 阶段十二（papers.md 契约重写 / A2 路径收敛为 `.work/.todo/{paper}/{case}/` / spawn 硬交付红线 / step02-03 目标图条款 / MCP 预检）。目标图从 step02 候选（Fig3 loci / Fig5(c)(f) $|a_1|,|b_1|$ / Fig6）经 gate 选定——**不采用预写计划里的 $Q_{sca}(x)$ 图（论文中不存在）**。

## 8. 给未来 agent 的快速入口

- 先读 `CLAUDE.md`，掌握路由、红线、目录约定、记忆要求和工具控制。
- 再读 `.human/DESIGN.md`，理解完整项目计划、关键机制和设计依据。
- 根据用户意图选择身份：复现新论文选 `main-agent`，跑自迭代选 `evolution-agent`，局部调试不进 workflow。
- 子 agent 被 spawn 后，先跑 `skill-print.py` 获得技能列表，再按任务单执行。
- 每个 agent 开始前先做 MCP 预检（确认 memento 工具真实可调用；不可用则显式声明降级、落 `.work/memento-cache/`，禁静默假装搜过），再搜 memento，结束前更新记忆；子 agent 的记忆要求由 spawn 指令显式写入。
- 不污染 `.paper/`，不直接写 `.result/`，高风险操作和关键 gate 必须停下来问用户。
