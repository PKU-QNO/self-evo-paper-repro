# .codex/agents/ — codex 预制 sub-agent 定义

**定位**：这里是 **codex（GPT-5.5）执行层/叶子层**的预制 agent 定义，供 Claude main-agent 通过 `codex exec` 委托机械/确定性活时使用。

**与 `.claude/agents/*.md` 的关系（两套并存，各管各的）**：

| 目录 | 定义谁 | 通道 | 管什么步 |
|---|---|---|---|
| `.claude/agents/*.md` | Claude 三层（main/sub/leaf，全 sonnet-5） | Claude Agent-tool spawn | 编排 + **判断层**（11 步 B 档 + C 档判断层） |
| `.codex/agents/*.toml` | codex 执行层/叶子层（gpt-5.5 / mini） | bash `codex exec` + codex 原生 subagent | **机械层**（11 步 A 档 + C 档机械层） |

**加载方式**：codex 从项目 `.codex/agents/*.toml`（从 cwd walk up 到 SEPR 根）或 `~/.codex/agents/`（用户级）加载。codex exec **顶层无 `--agent` flag**（memento `ec9c0a97` 核实）——靠 exec 的 prompt 显式指示用哪个 agent，以及作为 sub-sub 层的身份来源。

**格式**（TOML，每文件一个 agent）：`name` / `description` / `developer_instructions` 必需；`model` / `model_reasoning_effort` / `sandbox_mode` / `mcp_servers` / `skills.config` 可选。

**现有原型**：
- `codex-exec-worker.toml` — 执行层（A 档整步 + C 档机械层），pin gpt-5.5-high。
- `codex-leaf-mechanical.toml` — 叶子层（sub-sub 机械活），pin gpt-5.4-mini 省钱。

**状态**：原型（一期写死规则用）。二期在真实 case 试点后按实测调整 `developer_instructions`。完整方案见 `optics_agent/notes/codex_exec_delegation_plan-CN.md` 与 SEPR `CLAUDE.md`「模型路由与 codex 委托」节。

**注意**：`.codex/skills/` 是另一回事（skill 库，Claude/codex 都可读）；`.codex/agents/` 才是 codex 预制 agent。别混。
