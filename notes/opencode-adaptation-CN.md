# OpenCode 适配调研与 SEPR 落地方案

日期：2026-06-30  
工作区：`C:\Users\27370\Desktop\project\self-evo-paper-repro`

## 结论摘要

- OpenCode 会从当前目录向上查找本地 `AGENTS.md` / `CLAUDE.md`，并读取第一个命中的本地规则文件；项目配置 `opencode.json` 也会从当前目录向上查到最近 Git worktree。
- 官方文档没有发现 `agentRoot` / `root` / `workspace isolation` 这类可在配置里强制截断上级规则读取的字段。隔离的可靠做法是在 SEPR 根目录放本地 `AGENTS.md`，并从 SEPR 根目录启动 OpenCode。
- OpenCode 配置是合并式，不是替换式；项目 `opencode.json` 只覆盖冲突键，不能天然清空全局配置。需要用项目级 `permission` 显式收紧工具、skill 和 task。
- OpenCode skills 是按需加载：模型先看到 `<available_skills>` 中的 name/description，再调用 `skill({ name })` 读取全文；这不同于 Claude Code 的 `skills` 字段/工具描述注入习惯。
- SEPR 的 `.claude/skills/*/SKILL.md` 可以被 OpenCode 直接发现并复用，但要通过 OpenCode prompt/agent 配置强制“先加载对应 skill”。
- 本次已落地最小适配层：`AGENTS.md`、`opencode.json`、`.opencode/prompts/*.md`、`scripts/start-opencode-sepr.ps1`。

## 资料来源

- OpenCode Rules：`https://opencode.ai/docs/rules/`
- OpenCode Config：`https://opencode.ai/docs/config/`
- OpenCode Agents：`https://opencode.ai/docs/agents/`
- OpenCode Permissions：`https://opencode.ai/docs/permissions/`
- OpenCode Tools：`https://opencode.ai/docs/tools/`
- OpenCode CLI：`https://dev.opencode.ai/docs/cli/`
- OpenCode Agent Skills：`https://frank.dev.opencode.ai/docs/skills/`
- GitHub docs source：`https://github.com/sst/opencode/blob/dev/packages/web/src/content/docs/rules.mdx`、`agents.mdx`、`config.mdx`

## 1. Workspace 配置隔离机制

### 1.1 规则文件加载

OpenCode 的 Rules 文档说明，启动时按以下顺序查找规则文件：

1. 从当前目录向上遍历本地文件：`AGENTS.md`、`CLAUDE.md`
2. 全局文件：`~/.config/opencode/AGENTS.md`
3. Claude Code fallback：`~/.claude/CLAUDE.md`，除非禁用 Claude compatibility

同一类别里“第一个匹配文件胜出”。如果同一目录同时有 `AGENTS.md` 和 `CLAUDE.md`，只用 `AGENTS.md`。OpenCode 也支持项目 `CLAUDE.md` 作为兼容 fallback，但优先建议使用 `AGENTS.md`。

### 1.2 配置文件加载

OpenCode Config 文档说明配置源按以下顺序合并，后者覆盖冲突键：remote config、global config、`OPENCODE_CONFIG`、project `opencode.json`、`.opencode` 目录、`OPENCODE_CONFIG_CONTENT`、managed config。项目配置应放在项目根目录；OpenCode 启动时会从当前目录向上查找 `opencode.json`，直到最近 Git 目录。

关键点：配置是 merge，不是 replace。因此项目 `opencode.json` 不能天然阻止全局配置中未冲突的项继续存在，只能覆盖同名项或用 permission deny/ask 收紧能力。

### 1.3 是否有 root/agentRoot 隔离字段

本次查阅官方 rules/config/agents/permissions/CLI 文档和 GitHub docs source，没有看到 `agentRoot`、`root`、`workspaceRoot` 或类似“禁止读取上级 AGENTS.md”的配置字段。OpenCode 的“外部目录”是 permission 层的 `external_directory`，用于拦截工具读写当前工作目录外的路径，不是规则文件加载边界。

### 1.4 SEPR 禁止读上级规则的做法

本次采用三层防护：

1. 在 SEPR 根目录新增 `AGENTS.md`，让本地规则向上查找在 SEPR 根命中，避免落到 `C:\Users\27370\Desktop\project\CLAUDE.md` 或其他上级规则。
2. 新增 `scripts/start-opencode-sepr.ps1`，启动前 `Set-Location` 到 SEPR 根目录，并设置 `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1`，避免读取全局 Claude prompt fallback。
3. 在 `opencode.json` 里设置 `instructions: ["CLAUDE.md"]`，显式把 SEPR 的 `CLAUDE.md` 作为项目说明注入。

注意：`OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1` 会禁用 Claude Code prompt fallback，但不禁用 `.claude/skills`。不要设置 `OPENCODE_DISABLE_CLAUDE_CODE=1` 或 `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1`，否则 OpenCode 不能复用 SEPR 的 `.claude/skills`。

## 2. OpenCode 子 agent 机制

### 2.1 agent 定义位置

OpenCode agents 可在两个地方定义：

- `opencode.json` 的 `agent` 字段
- Markdown agent 文件：全局 `~/.config/opencode/agents/` 或项目 `.opencode/agents/`

本次选择 `opencode.json`，因为 SEPR 需要集中声明主/子 agent、权限和 skill/task 控制。

### 2.2 primary 与 subagent

OpenCode 有两类 agent：

- `primary`：用户直接交互的主 agent，可用 Tab 切换；SEPR 对应 `sepr-main` 和 `sepr-evolution`。
- `subagent`：由 primary 通过 Task tool 自动或手动 `@mention` 调用；SEPR 对应 `sepr-sub` 和 `sepr-sub-e`。

若 subagent 未指定模型，会继承调用它的 primary agent 模型。后续如果要固定 GPT-5.5，可在项目或 agent 级加 `model` 字段。

### 2.3 tools/MCP/permission 控制

OpenCode v1.1.1 后推荐用 `permission`，legacy `tools` 已 deprecated。核心 permission key 包括：`read`、`edit`、`glob`、`grep`、`list`、`bash`、`task`、`skill`、`webfetch`、`websearch`、`external_directory` 等。

permission 可以是：

- `allow`：直接允许
- `ask`：执行前询问
- `deny`：禁止

也可以用 object pattern 做细粒度匹配，例如：

```json
{
  "permission": {
    "task": {
      "*": "deny",
      "sepr-sub": "allow"
    },
    "skill": {
      "*": "deny",
      "main-agent": "allow"
    }
  }
}
```

OpenCode 文档说明 permission key 也可匹配自定义工具和 MCP 工具名，例如 `"mymcp_*": "deny"`。因此 SEPR 可按 MCP server/tool 名前缀收紧外部工具暴露。

### 2.4 禁止子 agent 继续 spawn 子子 agent

OpenCode 用 `permission.task` 控制能否通过 Task tool 启动 subagent。设置 `task: "deny"` 后，子 agent 无法再 spawn 其他 subagent；并且 deny 的 subagent 会从 Task tool 描述中移除，模型不容易尝试调用。

本次配置里：

- `sepr-main` 只允许 task 到 `sepr-sub`
- `sepr-evolution` 只允许 task 到 `sepr-sub-e`
- `sepr-sub` 和 `sepr-sub-e` 默认 `task: "deny"`

这比当前 Claude 版“三层 spawn”更保守。若以后确实要保留第 3 层 subsubagent，可新增专用 `sepr-subsub` / `sepr-sub-e-subsub`，并只在执行 agent 的 `permission.task` 中放行这些目标。

## 3. Skill 注入机制差异

### 3.1 OpenCode skill discovery

OpenCode Agent Skills 文档说明，skills 目录包括：

- 项目 `.opencode/skills/*/SKILL.md`
- 全局 `~/.config/opencode/skills/*/SKILL.md`
- Claude-compatible 项目 `.claude/skills/*/SKILL.md`
- Claude-compatible 全局 `~/.claude/skills/*/SKILL.md`
- agent-compatible 项目 `.agents/skills/*/SKILL.md`
- agent-compatible 全局 `~/.agents/skills/*/SKILL.md`

项目路径会从当前目录向上走到 Git worktree，并收集沿途匹配的 skills。全局定义也会加载。

### 3.2 OpenCode skill loading

OpenCode skills 不会启动时预加载全文。它会在 `skill` tool 描述里列出可用 skills 的 name 和 description，agent 需要显式调用：

```text
skill({ name: "main-agent" })
```

调用后才把 `SKILL.md` 正文返回到当前会话。因此 OpenCode 比 Claude Code 更偏 lazy loading，context 更省，但要求 prompt 明确“先加载对应 skill”。

### 3.3 与 Claude Code 的差异

SEPR 现有 Claude 机制把 `.claude/skills/` 当成核心执行知识，并通过主 agent spawn 模版要求子 agent 读对应 skill。OpenCode 兼容 `.claude/skills`，但不会自动把 6465 行全部塞进上下文；只展示 skill 元数据，按需读取全文。

因此不建议为了 OpenCode 把所有 skill 正文拼进 `prompt`，否则会失去 lazy loading 优势并造成上下文膨胀。更稳的做法是：

- 保留 `.claude/skills/` 作为共用 skill 源
- 在 `.opencode/prompts/*.md` 里强制每个 OpenCode agent 启动后先调用对应 skill
- 用 `permission.skill` 控制各 agent 能加载哪些 skill

## 4. SEPR 迁移方案

### 4.1 是否需要修改 SKILL.md

短期不需要。现有 `main-agent`、`sub-agent`、`evolution-agent`、`sub-E-agent` 的 frontmatter 已有 `name` 和 `description`。不过发现一个兼容性问题：目录名是 `sub-E-agent`，frontmatter name 是 `sub-e-agent`。OpenCode 技能规范要求 skill name 必须匹配目录名，且 name 只能小写字母数字和单 hyphen。

建议后续做一次目录兼容调整：

- 把 `.claude/skills/sub-E-agent/` 重命名为 `.claude/skills/sub-e-agent/`
- 同步修改所有文档中“路径意义的 sub-E-agent”为 `sub-e-agent`
- 人类可读身份名仍可写 `sub-E-agent`

本次未改动现有 skill 目录，避免破坏 Claude Code 当前路径引用；但 `opencode.json` 已按 OpenCode skill name 使用 `sub-e-agent`。

### 4.2 已添加的文件

- `AGENTS.md`：OpenCode 本地规则入口，用于停止上级规则 fallback，并指向 `CLAUDE.md`
- `opencode.json`：项目级 agent/permission/instructions 配置
- `.opencode/prompts/sepr-main.md`：OpenCode main-agent prompt
- `.opencode/prompts/sepr-sub.md`：OpenCode sub-agent prompt
- `.opencode/prompts/sepr-evolution.md`：OpenCode evolution-agent prompt
- `.opencode/prompts/sepr-sub-e.md`：OpenCode sub-E-agent prompt
- `scripts/start-opencode-sepr.ps1`：Windows PowerShell 启动脚本，固定 cwd 并禁用 Claude prompt fallback
- `notes/opencode-adaptation-CN.md`：本报告

### 4.3 推荐启动方式

在 PowerShell 中运行：

```powershell
C:\Users\27370\Desktop\project\self-evo-paper-repro\scripts\start-opencode-sepr.ps1 --agent sepr-main
```

自迭代时运行：

```powershell
C:\Users\27370\Desktop\project\self-evo-paper-repro\scripts\start-opencode-sepr.ps1 --agent sepr-evolution
```

如果需要一次性命令：

```powershell
$env:OPENCODE_DISABLE_CLAUDE_CODE_PROMPT="1"; $env:OPENCODE_ENABLE_EXA="1"; opencode --agent sepr-main C:\Users\27370\Desktop\project\self-evo-paper-repro
```

不要从 `C:\Users\27370\Desktop\project` 直接启动 SEPR 任务，否则本地规则和 project config 的向上查找边界更容易混入父目录内容。

## 5. 后续验证清单

1. 在 SEPR 根目录运行 `opencode debug config`，确认 resolved config 使用本项目 `opencode.json`。
2. 运行 `opencode agent list`，确认出现 `sepr-main`、`sepr-sub`、`sepr-evolution`、`sepr-sub-e`。
3. 启动 `sepr-main`，确认 `<available_skills>` 中出现 `main-agent`、`sub-agent`、`optics-mie-reproduction` 等。
4. 若 `sub-e-agent` 不出现，优先处理 `.claude/skills/sub-E-agent` 目录名大小写/匹配问题。
5. 用一个 dry-run prompt 验证：primary 能调用对应 skill，`sepr-sub` 不能继续 task spawn。
