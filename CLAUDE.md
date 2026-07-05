# CLAUDE.md — self-evo-paper-repro 工作区

> 这是 claude 在本工作区启动时强制读的简短路由文件。只放路由和红线，不塞具体流程。
> 流程在 `.claude/skills/` 下的 4 个 agent 身份 skill 里。

## 输出规范（强制）

**全程中文输出，所有文档用 Markdown 写作。** 这可能下降性能但方便用户审查，优先可读性。
- 所有 agent 的对话回复、报告、笔记、SKILL 内容一律中文
- 公式用 `$...$` / `$$...$$`（不用反引号或 `\(...\)`）
- 代码注释和标识符遵循项目既有约定（可英文）
- 给用户看的文档要结构化、用户可读，不是给机器的裸数据

## 执行系统（仅 Claude Code）

SEPR 现只面向 Claude Code 一套执行系统。OpenCode（GPT-5.5 备选）已于 2026-07-03 撤销：`opencode.json`、`.opencode/`、`scripts/start-opencode-sepr.ps1` 已删除，`AGENTS.md` 降为指向本文件的 stub。因此**不再有"三文件同步"约束**——规则主源就是本 `CLAUDE.md` 一处。

Opus 不稳定时的应急方案：改 Claude Code 的 URL/API 指向 DeepSeek（非 OpenAI-specific 的 response 接口可顶），而不是维护第二套 agent 配置。

## 模型路由与 codex 委托（强制，2026-07-05 用户拍板，省经费+省上下文）

背景：codex（GPT-5.5，经 `codex-cli` MCP）token 单价约为 Opus 4.8 的 **1/50**。原则：**判断密度决定谁干活**——机械执行发 codex，物理判断与裁决留 Claude。契约（8 字段报告、result_class、provenance、GATE 决定）**全部留在 Claude 侧**，不给 codex 重写 skill。

**默认规则：Claude 不亲自读写文件——文件读写与机械执行一律委托 codex-MCP**（读文件内容不进 Claude context = 省上下文的最大头）。**白名单豁免（仅这两类 Claude 亲自做）**：

1. **裁决必需的读**：main 在 gate 停机点亲读 GATE 决定 / verifier 输出 / 关键报告——裁决依据不得经 codex 转述（转述层会漂移，Gate4 已实证）。
2. **契约文件的写**：8 字段报告、capsule、GATE 决定、WORK_LOG、run_manifest——这些是 Claude 的裁决产出，亲写并自校；不得由 codex 代笔。

**分工表**：

| 工作 | 执行方 |
|---|---|
| PDF/文本提取、跑代码脚本、数字化、批量产物、一切机械读写、非 workflow 杂活、leaf 单点 | **codex**（调用即 leaf，物理上不能再 spawn） |
| 代码实现（step04 写码） | **codex 写，Claude 验**（verifier 是确定性裁判，质量由它兜底） |
| step05 对抗审查 | **codex + Claude 双审**（跨模型异构审查，防 self-preference bias） |
| 物理推导（derivation.md）、step02 理解、step03 spec、step07/08 物理归因 | **Claude**（Gate3 核公式的上游，verifier 验代码不验推导文本） |
| main 编排、gate 裁决、capsule/WORK_LOG/报告 | **Claude（不省这条）** |

**codex 调用安全规范（硬约束）**：每次调用显式 `sandbox: workspace-write` + `approval-policy: untrusted`，**永不** `danger-full-access`；`cwd` 限 case 文件夹；secrets（secret.json/SSH/license）在 codex 可达范围外。codex 产物一律落盘，**Claude 验收（文件存在 + verifier PASS + 抽查）后才进报告**——codex 自述不作数，与对 Claude sub 的纪律一致。codex 调用计入 case 级资源上限（与 spawn 20 同口径）。

## Malformed tool-call 熔断（强制，2026-07-05）

已知机制（官方 issue #61367/#62344/#64097 等 + 本项目实测）：Opus 4.8 长上下文偶发（~1.5%）把 tool call 格式写坏；harness 把坏文本留在 transcript，模型**自回归模仿自己上一轮的坏格式**（即使它"知道"错了，模仿的是 pattern 不是意图），一次偶发级联成连败（有 issue 记录 24 连败）；错 3 次后几乎写不出正确 tool call（用户实测）。

**熔断规则**：同一 session 累计 **2 次** malformed tool call（"Your tool call was malformed"、裸 `<invoke>` 文本、`antml:` 前缀丢失、invoke 前杂 token）→ **立即熔断**：① 停止当前工作，不再尝试第 3 次工具调用；② 把当前状态写入 handoff（WORK_LOG 增量 + case 文件夹 HANDOFF 文件，纯文本输出不需要 tool call 也要尽量写——若写文件本身也失败，直接在对话里输出 handoff 全文让用户复制）；③ 告知用户开新对话接手；④ **绝不** `--resume` 本 session。缓解：每 gate 停机点默认断 session 换新对话（同时也是省钱正解——391k 旧上下文的缓存在 gate 等待期早已过期）。

## v3-final 设计归档（在 optics_agent 侧）

SEPR 的设计 / 风险审计 / 演进文档（V1→V2→V3）的 **canonical 版本**汇总在元工作区 `optics_agent/v3-final/`（本工作区通过 junction 到不了，需去 optics_agent 侧看），索引 `optics_agent/v3-final/README.md`。原散落在 `optics_agent/papers/SEPR/` 等处的文件已改名带 `_moved` 后缀并冻结（顶部有面包屑）。

**文件名后缀约定（两工作区通用）**：`_latest`=正在更新的最新版 / `_archive`=废案或完结但有价值 / `_deprecated`=无价值易误导（当前无）/ `_moved`=别处有 canonical、此处不更新 / `_V1_finished`=历史完结（预留）。本工作区的 `WORK_LOG.md` 是 living 日志，不移动。

## 子 Agent 深度与工具限制（Claude Code）

SEPR 明确只允许三层委派：`main/evolution -> sub/sub-E -> leaf`。第 3 层叶子不得继续 spawn。全部由 `.claude/agents/*.md` 定义：

| 层 | agent 定义 | maxTurns | 工具 | spawn 规则 |
|----|-----------|----------|------|-----------|
| 编排层 | `main-agent` / `evolution-agent` | 50 | 含 `Agent` | 只派对应执行者 |
| 执行层 | `sub-agent` / `sub-e-agent` | 15 | 含 `Agent` | 只派对应叶子身份 |
| 叶子层 | `sub-leaf` / `sub-e-leaf` | 15 | **不含 `Agent`** | 无法再 spawn（框架层硬约束） |

**叶子层硬化（2026-07-03，堵审计 C1）**：第 3 层不再"复用执行者身份 + prompt 提醒省略 Agent"（软约束），改为独立的 `sub-leaf` / `sub-e-leaf` agent 定义——其 `tools` 不含 `Agent`，从框架层即无法继续 spawn。执行者 spawn 叶子时用 `subagent_type: sub-leaf`（或 `sub-e-leaf`）。四个非叶子 agent 均 `disallowedTools: mcp__*, NotebookEdit`；工具 allowlist 统一 `Read, Write, Edit, Bash, Glob, Grep, ToolSearch, Skill`（编排/执行层另含 `Agent`）。四个非叶子 agent 另用 `skills:` frontmatter 预加载各自身份 skill（`skill-print.py` 仍作兜底）。

## 工作区身份

光学论文复现自进化 agent。交付 SKILL 蓝图（主）+ benchmark 数据（次），不交付自迭代内容本身。自迭代是手段。

## result_class 状态枚举（强制）

所有报告、brief、handoff、memento 记忆和自迭代 capsule 必须用以下 7 级枚举标注结果状态：

| result_class | 含义 |
|--------------|------|
| `not_run` | 未跑 |
| `pipeline_completed` | 流程跑完，无物理判断 |
| `simulation_completed` | 仿真跑完，数值出结果，无物理判断 |
| `diagnostic_only` | 只做诊断，无复现声明 |
| `surrogate_fallback` | 用代理/简化方案，不是物理复现 |
| `partial_physical_match` | 部分物理量匹配，未全通过 |
| `physical_reproduction_success` | 物理复现成功（硬约束 + 极限 + 论文图量化全过 + human gate） |

最高优先级风险规则：LLM/agent 不得把 `surrogate_fallback`、`diagnostic_only`、`pipeline_completed` 当成 `physical_reproduction_success`。除非 Layer 1 物理硬约束、Layer 2 已知极限/退化、Layer 3 论文图量化和 human gate 全部通过，否则禁止标 `physical_reproduction_success`。

## 进入 workflow 的判定（重要）

**并非所有任务都要遵循完整 workflow。** 判定规则：

- 用户明确要复现一份**新论文**（或新一篇/新一张图）→ 进入 10 步复现 workflow
- 用户说"跑自迭代"（攒够后人工触发）→ 进入 5 步自迭代 workflow
- 用户在调试某个步骤、改某个 skill、问问题、跑单独脚本、看已有结果 → **不进入任何 workflow**，直接做
- 模糊时，问用户一句："这次是复现新论文、跑自迭代，还是局部任务？"

不要把每个请求都套进 workflow，那样简单活也被拖长。

## 身份选择逻辑

当前系统有 4 个 agent 身份 skill，分两套 workflow。用户表达意图后选择身份：

| 用户意图 | 选择身份 | 加载 skill | 行为 |
|---------|---------|-----------|------|
| "复现这篇新论文" | → `main-agent` | 读 main-agent skill | 进入 10 步复现编排 |
| "跑自迭代"、"提炼经验" | → `evolution-agent` | 读 evolution-agent skill | 进入 5 步自迭代编排 |
| "帮我调试/算个数/看结果" | → 不进 workflow | 不加载身份 skill | 直接做 |

身份选择只决定加载哪个 agent skill，不换模型。两套 workflow 互不交叉。

## 4 agent 身份 skill

| 身份 | skill 名 | 所属 workflow | 职责 |
|------|---------|-------------|------|
| 复现编排者 | `main-agent` | 复现 | 编排 10 步复现流程，spawn 子 agent、校验报告、汇总结果 |
| 复现执行者 | `sub-agent` | 复现 | 执行单步任务（读图抽参、搭模型、跑代码、写工作报告） |
| 自迭代编排者 | `evolution-agent` | 自迭代 | 编排 5 步自迭代流程（审查→聚类→改 skill→验证→报告） |
| 自迭代执行者 | `sub-E-agent` | 自迭代 | 执行审查 capsule、改 skill 草稿、跑验证等具体任务 |

**三层 spawn 规则**（复现和自迭代共用）：
- 编排者（main-agent / evolution-agent）不亲自做隔离活
- 执行者（sub-agent / sub-E-agent）做具体步骤
- 执行者可以 spawn 子子 agent 做单点小活（提取数值、跑 verifier、查公式），**第 3 层不再 spawn**

## .human/ 与 .claude/ 双目录

- `.human/skills/` = **中文审查稿**，人是读者，用于审阅设计意图和流程口径。
- `.claude/skills/` = **中文详细执行版**，agent 实际运行时读；4 个 agent 身份详细版已完成（约 6465 行）。
- 英文 prompt-engineered 版是可选后期优化，不是当前阻塞项。
- `.human/` 与 `.claude/` 不是逐字镜像；`.claude/` 可比 `.human/` 更详细、更适合执行。
- **双写同步机制**：凡更新 skill 正文，关键协议字段必须两侧同步，包括 `result_class`、路径约定、报告 schema、human gate、权限/安全红线。

## 关键节点必须请求用户意见（重要）

**除非用户明确说"全自动"，否则在以下节点停下来问用户：**

1. **执行完即将进 `.result` 时**——把哪些沙箱内容确认为最终成果，问用户
2. **即将自迭代（改 skill/蓝图）时**——改什么、为什么改，问用户批准
3. **物理验证失败、要重跑或换方案时**——问用户怎么办
4. **遇到缺失信息（论文没给参数、需要 GUI 模板等）时**——问用户要，不要瞎猜硬跑

中间步骤 agent 自由跑，这 4 类节点必须停。

## workflow 失败定义与防空跑（重要）

**workflow 怎么算失败：**
1. 物理 verifier 连续不通过且无新假设
2. 同一步重跑达到上限（5 轮）
3. 子 agent 报告 blocked 且无法自行解决
4. case 级 wall-clock / spawn 数 / 搜索数超限
5. evolution 级 replay 大面积退化或 human gate 拒绝

**防空跑硬性规则（写进 spawn 模版和各 SKILL.md）：**
- **节点级**：同一步检查不通过**最多重跑 5 轮**。每轮必须有新证据或新假设，无新信息的重跑直接 Drop/Archive 转 blocked，不再硬跑
- **retry fingerprint**：每次重跑记录改了什么/为什么重跑，相同 fingerprint 第二次失败即 blocker
- **case 级**：单篇论文复现 max wall-clock 4 小时、max spawned agents 20、max external searches 30
- **evolution 级**：单次 evolution max 处理 capsule 15、max skill 改动 8，超限分批
- 主 agent 每走一步前检查：这步重跑几次了？fingerprint 变了吗？还有新假设吗？达 5 轮仍不通过就停

**失败不是终止：** 失败时 step10 照样写报告（标失败原因 + 走到哪步 + 下次怎么改），扔 toEflow/，进 .E-history 当 Archive 负面知识。失败经验有价值。

## 目录约定

```
.paper/        论文原文区（只读，不污染）
  ├── scattering.pdf   Bohren & Huffman 教材（核心公式主源）
  └── mie/             11 篇 Mie 论文 PDF
.work/         agent 工作沙箱（软约束）
  ├── .sub-report/    子 agent 完整报告统一放这里
  ├── .todo/{paper}/{case}/  单论文 workflow 过程文件 + skill 草稿缓冲（canonical，2026-07-04 收敛；case 名含日期版本如 0703-01-akimov-mie-v1，无额外 timestamp 层；skill 草稿在其下 self-iteration/）
  ├── .result/<case>/capsule.md  W-flow step11 强制产出（100% fire），E-flow step01 唯一输入（2026-07-04 补 A1 生产侧，产/消契约闭合）
  ├── .evolution/<timestamp>/  evolution 进行中工作区
  └── memento-cache/
toEflow/       workflow→evolution 缓冲（只增不删）
  ├── <paper>.skill.yaml       workflow 提交的 skill 草稿
  └── <paper>.todo-entry.md    workflow 提交的迭代需求
.E-history/    evolution 历史报告（按次数排序，01 开机）
  ├── 01-evolution-report.md
  └── 02-evolution-report.md
.result/       最终交付区，主 agent 工作结束前从 .work 复制有用内容过来
todo.md        全局日志（临时缓冲：每次 run 填一段，进自迭代 → 迭代后归档/删减）
WORK_LOG.md    整体大框架总览（永不归档、永不删减；只增不改历史）
WORK_LOG/      多篇复现的分文件详细日志
  ├── README.md          文件夹索引 + 命名/维护约定
  ├── _TEMPLATE.md       每篇复现日志的空模板
  ├── 00-历史存档-*.md    文件夹化前全文快照（底本）
  └── <NN>-<papername>-v<N>.md   一篇复现一文件（多次复现 → 多文件，version 由用户第一句话给）
papers/        -> optics_agent/papers (junction)
reproduction_test/ -> optics_agent/reproduction_test (junction)
```

论文命名规则：`MMDD-NN-papername-vN`，如 `0629-01-akimov-mie-v1`

## WORK_LOG 维护规范（强制，main-agent 负责）

**定位（与 todo 分工，不重叠不互抄）**：
- `todo.md` = **临时缓冲**：待进自迭代的需求，迭代后归档/删减。机器索引口径，一行一 run。
- `WORK_LOG` = **整体大框架历史**：**永不归档、永不删减、只增不改历史**。人看的叙事层。
- 两者分工写死：todo 记"待办/状态"，WORK_LOG 记"发生了什么+为什么这么决定"。数据/报告不重抄，WORK_LOG **只引用** capsule / run_manifest / `.result` / gate 决定文件的路径。

**结构**：
- 顶层 `WORK_LOG.md` = 总览（一句话定位/路径/当前状态/文件结构/核心设计速查/文档索引）+ **阶段/run 摘要表**（每 run 一行 + 指向详情文件的指针）。
- `WORK_LOG/<NN>-<papername>-v<N>.md` = **一篇复现一文件**，按论文分。同一篇复现多次 → 分多文件（`-v1`/`-v2`…），**version 号由用户在第一句话给定，agent 不猜、不自造命名**。
- 文件内部按"日期 + 会话/step 批次"**追加条目**（形如 `### step0X + GateN（YYYY-MM-DD）`），累积不覆盖。模板见 `WORK_LOG/_TEMPLATE.md`。

**谁写、何时写（main-agent 固定动作）**：
1. **每次新上下文开工时**：先读顶层 `WORK_LOG.md`（恢复大框架）；若继续某篇复现，再读该篇 `WORK_LOG/<...>.md`。此为身份恢复的一部分。
2. **每个会话结束前 / 每个报告点（step11、以及每个 human gate 停机前）**：向该篇 `WORK_LOG/<...>.md` **增量追加**一段带日期的条目（做了什么、关键决策+为什么、引用产物路径、下一步/停机点），并在顶层摘要表更新该 run 的行。**只增不改已有历史**。
3. **决策台账**：凡有 CC 建议 / 用户裁决 / gate 结论，追加到该篇的"决策台账"节（记：建议→裁决→落点文件+memento id），使"只读 WORK_LOG 即可恢复全部决策，不必翻对话"。
4. step11 验收清单含"WORK_LOG 已增量更新"，缺则本步不算完成（同 capsule/run_manifest 口径，不靠自觉）。

## run manifest（强制）

每次 workflow run / evolution run 结束前，必须在 `.work/` 下写一份 `run_manifest.yaml`，用于记录本轮编排的 fan-out、depth、重跑和结果分类。复现 workflow 由 main-agent 第 11 步负责写；自迭代 workflow 由 evolution-agent 第 6 步负责写。

`run_manifest.yaml` 至少包含：
- `run_id`、`timestamp`、`case`/`batch`：标识本轮复现 case 或 evolution 批次
- `spawned_agents`：数量、每个 agent 角色、负责节点、depth
- `fan_out`：哪个节点并发了几个子 agent
- `max_depth_reached`：本轮达到的最大 spawn 深度
- `result_class`：必须使用上文“result_class 状态枚举（强制）”的 7 级枚举之一，不得写 success / partial / fallback / blocked / failed / archived 等旧口径
- `retry_fingerprints`：每步重跑记录，写明 fingerprint、修改点、新证据/新假设、结果

`run_manifest.yaml` 是审计索引，不替代完整报告；完整证据仍放各 step 报告和 artifact。

## 记忆要求（每个 agent 都遵守）

**每个 agent（main-agent / sub-agent / evolution-agent / sub-E-agent）开始行动前必须做：**

0. **MCP 预检（第一步，先于一切）**：确认本 session 的 MCP 工具（尤其 `memory_search` / `memory_store` 等 memento 工具，以及 `ToolSearch`）**真实可调用**，不要假设它们在。
   - **可用** → 照第 1/2 步执行记忆纪律。
   - **不可用**（工具不存在 / 调用报错 / 全部 MCP 断联）→ **不得静默跳过还假装搜过/存过记忆**。必须：① 在报告里显式写明「本 session memento 不可用，记忆纪律降级」；② 降级落 `.work/memento-cache/` 下结构化 JSON（带 provenance 五要素），供 MCP 恢复后回灌；③ 记忆污染是第 2-3 个 case 才炸的信号，首篇复现库空，降级非阻塞——但必须**声明**，不得静默。
   - 说明：memento 断联属环境性故障（如全部 MCP 断联），不是「未接入」；预检的价值是把「红线静默失效」变成「大声降级」。robust 版是 SessionStart hook 探活，属 hooks 家族，跑通 Mie 后随 hooks 一起硬化。
1. 搜索 memento 记忆库（`memory_search`），找和当前任务相关的已有记忆，避免重复劳动
2. 结束前必须更新记忆（`memory_store` / `decisions_log` / `pitfalls_log`），存本次的关键事实/决策/教训

子 agent 没有自动记忆注入，主 agent spawn 时在指令里强制要求这三步（含第 0 步 MCP 预检）。

所有记忆写入和报告中的 provenance 必须统一使用以下五个字段名，不混用 source、claim、evidence、scope、confidence 等别名：

```yaml
provenance:
  source_artifact: <来源 artifact，论文+图/case/skill版本>
  evidence_type: <数值/verifier结果/代码片段/人工确认>
  timestamp_version: <时间戳或版本>
  scope_applicability: <适用范围/边界>
  confidence_result_class: <置信度 + result_class>
```

如果某条记忆暂时缺字段，必须显式写 `unknown` 或 `pending`，不能省略字段。

## 子 agent tools 控制（重要）

子 agent 的 MCP 工具描述是**全量注入** context（不是懒加载），会占 context window。主 agent spawn 子 agent 时必须用 `tools` 字段（allowlist 模式）控制暴露的工具：

```
tools: Read, Write, Edit, Bash, Glob, Grep, ToolSearch, Skill
```

- allowlist 模式：只列出内置工具，MCP 工具自动排除，避免 context 膨胀
- `ToolSearch` 必须显式包含（否则 MCP 工具注册了但无法调用）
- `Skill` 放行让子 agent 能跑 skill-print.py 获得技能列表
- 需要某个 MCP 工具时才显式列出，不要全量暴露
- `tools` 字段不支持 `mcp__*` 通配符，要限 MCP 用 `disallowedTools`

## 沙箱草稿规则（防回滚崩溃）

**单论文 workflow 的 step 10**：把 skill 草稿写到 `.work/.todo/<paper-name>/`，不提交 `.claude/`。workflow 结束前把要给 evolution 用的 skill 草稿 + 迭代需求扔进 `toEflow/`（只增不删）。不跑 replay（单论文做不到）。

**evolution-agent**：读 `toEflow/` 所有草稿做批量治理。改 skill 前先在 `.work/.evolution/<timestamp>/` 写草稿，通过 human gate 的才同步到 `.claude/` + `.human/`。草稿不许删。

**validate_and_replay 实现**（E-flow 不调 W-flow）：
- 层 A（改提示词备注/注意事项）：sub-E-agent 跑旧代码 + verifier + benchmark 对比，E-flow 自洽
- 层 B（改流程步骤）：sub-E-agent 重跑 step 06-08 旧代码，E-flow 自洽
- 层 C（改核心方法/公式来源）：报告"需人工开 W-flow 重跑"，human gate 决定，不重跑标"未验证风险保留"

## 安全红线

- 不读 `secret.json`、SSH key、license 内容
- 不污染 `.paper/` 原文
- 不直接写 `.result/`，需主 agent 复制
- 子 agent 不动其他子 agent 的文件，除非任务就是修改/debug 那个文件
- 高风险操作（改 active COMSOL image、删目录、提交 Magnus job）必须问用户

## skill 路由表

| 任务 | skill |
|------|-------|
| 复现编排 | `main-agent` |
| 复现执行 | `sub-agent` |
| 自迭代编排 | `evolution-agent` |
| 自迭代执行 | `sub-E-agent` |
| Mie 理论复现 | `optics-mie-reproduction` |
| Magnus 平台操作 | `optics-magnus-platform` |
| Magnus artifact 格式 | `optics-magnus-artifacts` |
| PDF 处理（提取/OCR/数字化） | `pdf` |
| Magnus HPC 执行（蓝图提交/作业监控，SLURM/973G/128核） | `magnus` |
| 项目基础路由 | `optics-agent-core` |
| 创建/规范 skill | `skill-creator` |

## skill 与 blueprint 格式

skill 文件夹和 `.skill.yaml` 互转用 `skill-creator/scripts/skill_to_yaml.py` 和 `yaml_to_skill.py`。`.blueprint.yaml` 是可执行任务模板（参数+提交），`.skill.yaml` 是知识包（文件集合）。
