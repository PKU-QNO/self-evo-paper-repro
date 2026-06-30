# AGENTS.md - self-evo-paper-repro OpenCode Router

This file is the project-local OpenCode rule file for the SEPR workspace.
It intentionally exists so OpenCode stops at this workspace's nearest local rule
instead of falling back to parent workspace rules.

## Mandatory First Step

Read `CLAUDE.md` in this directory before doing any project work. Treat it as the
authoritative workspace router and safety policy for both Claude Code and
OpenCode sessions.

## OpenCode Adaptation

- Keep OpenCode launched from this directory, not from `C:\Users\27370\Desktop\project`.
- Prefer `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1` when launching OpenCode in this workspace.
- Do not disable Claude-compatible skills unless intentionally testing pure `.opencode/skills`; SEPR reuses `.claude/skills/*/SKILL.md`.
- OpenCode skills are loaded lazily by the `skill` tool. When acting as `main-agent`, `sub-agent`, `evolution-agent`, or `sub-e-agent`, explicitly load the matching skill before executing workflow logic.
- Follow `CLAUDE.md` result_class, workspace boundaries, safety red lines, and human-gate rules.

## Tool And Spawn Policy

- Use OpenCode `permission.task` to control which subagents can be launched.
- Use `permission.skill` to control which skills can be loaded.
- Deny `task` inside execution subagents unless the parent explicitly needs third-layer subsubagents.
- Deny edits outside this worktree unless a task explicitly requests an external path.

## 三文件同步规则（强制）

改 `CLAUDE.md` / `AGENTS.md` / `opencode.json` 任何一个，必须同步审改其它两个。详见 `CLAUDE.md` 的"三文件同步规则"节。Claude Code 和 OpenCode 共用 `.claude/skills/` 的 SKILL.md 正文，但根配置不同步会导致两系统行为分叉。
