# CLAUDE.md — self-evo-paper-repro 工作区

> 这是 claude 在本工作区启动时强制读的简短路由文件。只放路由和红线，不塞具体流程。
> 流程在 `.claude/skills/` 下的 4 个 agent 身份 skill 里。

## 输出规范（强制）

**全程中文输出，所有文档用 Markdown 写作。** 这可能下降性能但方便用户审查，优先可读性。
- 所有 agent 的对话回复、报告、笔记、SKILL 内容一律中文
- 公式用 `$...$` / `$$...$$`（不用反引号或 `\(...\)`）
- 代码注释和标识符遵循项目既有约定（可英文）
- 给用户看的文档要结构化、用户可读，不是给机器的裸数据

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

- `.human/skills/` = **中文设计稿**，人是读者。当前所有 9 个 skill 的中文设计存这里。
- `.claude/skills/` = **英文 prompt-engineered 版**，agent 实际运行时读。当前只有从 optics_agent 复制的领域 skill，4 个 agent 身份 skill 待后期写。
- **现阶段**：`.claude/skills/` 镜像 `.human/skills/` 内容（同为中文），等设计稳定后 `.claude/skills/` 翻译为英文。
- **双写机制**：workflow 跑时更新 skill，要同时写 `.human/`（人看的设计稿）和 `.claude/`（agent 读的执行版）。

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
  ├── .todo/<paper>/  单论文 workflow 过程文件 + skill 草稿缓冲
  ├── .evolution/<timestamp>/  evolution 进行中工作区
  └── memento-cache/
toEflow/       workflow→evolution 缓冲（只增不删）
  ├── <paper>.skill.yaml       workflow 提交的 skill 草稿
  └── <paper>.todo-entry.md    workflow 提交的迭代需求
.E-history/    evolution 历史报告（按次数排序，01 开机）
  ├── 01-evolution-report.md
  └── 02-evolution-report.md
.result/       最终交付区，主 agent 工作结束前从 .work 复制有用内容过来
todo.md        全局日志，每次 workflow/Eflow 结束前填一段
papers/        -> optics_agent/papers (junction)
reproduction_test/ -> optics_agent/reproduction_test (junction)
```

论文命名规则：`MMDD-NN-papername-vN`，如 `0629-01-akimov-mie-v1`

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
1. 搜索 memento 记忆库（`memory_search`），找和当前任务相关的已有记忆，避免重复劳动
2. 结束前必须更新记忆（`memory_store` / `decisions_log` / `pitfalls_log`），存本次的关键事实/决策/教训

子 agent 没有自动记忆注入，主 agent spawn 时在指令里强制要求这两步。

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
