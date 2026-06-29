# self-evo-paper-repro 工作区架构

> 2026-06-29 建。光学论文复现自进化 agent 的独立工作区。
> 隔离自 optics_agent 的 coding 上下文，专门跑论文复现 + skill/蓝图自进化实验。

## 设计要点

- **三层 agent**：主 agent（读 main-agent skill 编排）→ 执行 agent → 子 agent（隔离上下文），一般 3 层
- **身份隔离**：CLAUDE.md 只放路由红线；每层 agent 读自己的身份 skill（main-agent / sub-agent），不共用一份造成混淆
- **sub-agent 强制声明身份**：spawn 时必须告诉子 agent"你是子 agent"，防越权误判
- **结构化工作报告**：子 agent 结束前写固定字段报告到 .work，人看 Markdown，agent 读 yaml
- **记忆全电脑共享**：sub-agent 结束调 memento-mcp 写长期记忆
- **不交付自迭代内容**：交付的是 benchmark 数据（次要）+ SKILL 蓝图（主），自迭代是手段不是交付物
- **能力丧失不滚**：重跑对应篇章当 mini-replay + 强化，不做统一 project-flow（不同人负责不同领域）

## 目录结构

```text
self-evo-paper-repro/
├── CLAUDE.md                    # 简短路由+红线，claude 启动强制读（待填）
├── .claude/
│   ├── skills/                  # skill 系统
│   │   ├── main-agent/          # 主 agent 身份+workflow 设计（待填）
│   │   ├── sub-agent/           # 子 agent 身份+工作报告+记忆规范（待填）
│   │   ├── optics-agent-core/   # 基础路由（从 optics_agent 复制）
│   │   ├── optics-mie-reproduction/  # Mie 复现流程+4层检验+verifier（从 optics_agent 复制）
│   │   ├── optics-magnus-platform/   # Magnus 平台操作（从 optics_agent 复制）
│   │   └── optics-magnus-artifacts/  # Magnus artifact 格式（从 optics_agent 复制）
│   └── agents/                  # claude 原生 agent 定义文件（可选，按需建）
├── .paper/                      # 论文原文区（按领域分）
│   ├── mie/
│   └── comsol/
├── .work/                       # agent 工作沙箱（软约束），过程文件、SKILLNAME.yaml 自迭代草稿、工作报告
│   ├── mie/
│   ├── comsol/
│   ├── self-iteration/
│   └── memento-cache/
├── .result/                     # 最终交付区，主 agent 工作结束前从 .work 复制有用内容过来
│   ├── mie/
│   ├── comsol/
│   ├── benchmarks/              # benchmark 数据（次要交付）
│   ├── skills-blueprint/        # SKILL 蓝图（主要交付）
│   └── reports/
├── papers -> optics_agent/papers           # junction，够得着 Mie PDF
└── reproduction_test -> optics_agent/reproduction_test  # junction，够得着 mie 代码目录
```

## 待填（用户自己写初稿）

- `CLAUDE.md` — 简短路由 + 红线
- `.claude/skills/main-agent/SKILL.md` — 主 agent 身份 + 11 步 workflow + 子 agent 规范
- `.claude/skills/sub-agent/SKILL.md` — 子 agent 身份声明 + 结构化工作报告 + 更新记忆

## 从 optics_agent 复制过来的 skill

- `optics-agent-core`、`optics-mie-reproduction`、`optics-magnus-platform`、`optics-magnus-artifacts`
- 这几份是当前 optics_agent 的最新版，新工作区独立维护，后续改这里不影响 optics_agent

## 11 步 workflow 短语（main-agent 里要按 Mie 调整）

1. 确定目标图
2. 抽参数成表
3. 列缺失信息
4. 建最小可执行模型
5. 保守提交作业
6. 逐因诊断失败
7. 区分物理/作业成功
8. 留 PI 进度痕
9. 建必需产物
10. 标准答案格式
11. 报告要求

> 注：这 11 步来自 v1 COMSOL/Magnus 流程。Mie 纯 Python 阶段第 5/6 步不适用（无 job 提交），核心骨架通用：读论文→抽参数→formalization→推导→代码→检验→对比→报告。
