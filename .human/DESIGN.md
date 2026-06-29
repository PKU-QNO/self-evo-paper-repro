# .human/ 顶层设计文档

> 人看的中文设计稿，不是 prompt-engineered 的 agent skill。
> 后期 `.claude/skills/` 会写英文 4 身份 agent-skill，这里是设计源头。
> 读者：项目成员、PI、任何想理解系统架构的人。

---

## 1. .human/ 是什么

`.human/` 是**人看的设计稿目录**。所有架构决策、身份定义、workflow 设计、skill 蓝图，先用中文写在这里，等设计稳定后再翻译/优化成英文 prompt-engineered 版本放进 `.claude/skills/`。

**不是** agent 运行时读的文件。agent 读 `.claude/skills/`，人读 `.human/`。

目录结构：
```
.human/
├── DESIGN.md           ← 本文，顶层设计
├── CLAUDE.md           ← CLAUDE.md 镜像（设计阶段同步根目录版本）
└── skills/             ← 中文设计稿 skill
    ├── main-agent/         复现编排者（设计稿）
    ├── sub-agent/          复现执行者（设计稿）
    ├── evolution-agent/    自迭代编排者（设计稿）
    ├── sub-E-agent/        自迭代执行者（设计稿）
    ├── optics-mie-reproduction/
    ├── optics-magnus-platform/
    ├── optics-magnus-artifacts/
    ├── optics-agent-core/
    └── skill-creator/
```

---

## 2. 4 agent 架构

系统由四个 agent 身份 skill 驱动，分为两套完全对称的 workflow：

### 复现 workflow（主）

| 身份 | skill 名 | 职责 |
|------|---------|------|
| 复现编排者 | `main-agent` | 读主 agent skill，编排 10 步复现流程；spawn 子 agent、校验报告、汇总结果 |
| 复现执行者 | `sub-agent` | 读子 agent skill，执行单步任务（读图抽参、搭模型、跑代码、写报告） |
| 子子 agent | （复用 sub-agent） | 被子 agent spawn 做单点小活（数字提取、跑 verifier、查公式），第 3 层不再 spawn |

### 自迭代 workflow（积累后人工触发）

| 身份 | skill 名 | 职责 |
|------|---------|------|
| 自迭代编排者 | `evolution-agent` | 编排 5 步自迭代流程（并发审查→聚类规划→并发改 skill→验证 replay→治理报告） |
| 自迭代执行者 | `sub-E-agent` | 被 evolution-agent spawn，执行审查 capsule、改 skill 草稿、跑验证等具体任务 |

### 两套对称

```
复现 workflow               自迭代 workflow
─────────────────           ─────────────────
main-agent（编排）          evolution-agent（编排）
  └─ sub-agent（执行）        └─ sub-E-agent（执行）
      └─ sub-agent（子子）         └─ sub-E-agent（子子，复用身份）
```

**互不交叉**：
- 复现 workflow 只产 capsule（工作报告 + benchmark 条目），不自迭代
- 自迭代 workflow 拿已积累的 capsule 做批量治理，不改复现流程
- 执行者不总结自己（子 agent 只产原始报告，不自评经验）

---

## 3. 身份选择逻辑

用户在对话中表达意图后，CLAUDE.md 的路由规则决定当前 agent 以什么身份启动：

| 用户意图 | 身份选择 | 行为 |
|---------|---------|------|
| "复现这篇新论文" / "跑 Fig.3" | → `main-agent` | 加载 main-agent skill，进入 10 步复现 workflow |
| "跑自迭代" / "提炼经验" / "治理" | → `evolution-agent` | 加载 evolution-agent skill，进入 5 步自迭代 workflow |
| "帮我看这个脚本" / "调试" / "算个东西" / "问问题" | → 不进 workflow | 不加载身份 skill，直接以当前能力执行 |
| 模糊时 | → 问用户 | "这次是复现新论文、跑自迭代，还是局部任务？" |

**关键原则**：
- 复现和自迭代是互斥入口，不会同时进入
- 局部任务不进任何 workflow，避免把简单活拖长
- 身份选择的结果是加载不同的 agent-skill，不是不同模型

---

## 4. .human/ 与 .claude/ 关系

```
.human/skills/            .claude/skills/
─────────────────         ─────────────────
中文设计稿                英文 prompt-engineered 版
人是读者                  agent 实际读
先写，等设计稳定           后写
放全部 9 个 skill         只放 4 个 agent 身份 skill
                          （领域知识 skill 放法后期定）
```

**当前阶段**：`.human/skills/` 已有 7 个中文 skill（main-agent、sub-agent + 5 个领域/工具 skill）。`.claude/skills/` 是空的目录骨架或早期版本。

**目标状态**：
- `.claude/skills/` 最终放 4 个英文 prompt-engineered 的 agent 身份 skill：
  - `main-agent/`（复现编排）
  - `sub-agent/`（复现执行）
  - `evolution-agent/`（自迭代编排）
  - `sub-E-agent/`（自迭代执行）
- 领域知识 skill（optics-mie-reproduction 等）放在哪（`.claude/skills/` 内还是通过 junction 引用）后期定

---

## 5. 双写机制

workflow 跑的过程中，如果 skill 内容需要更新：

```
1. 先在 .work/self-iteration/ 写草稿（沙箱）
2. 草稿通过 human gate + 物理 verifier
3. 同时写两处：
   ├─ .human/skills/<skill>/（中文设计稿，人看）
   └─ .claude/skills/<skill>/（英文版，agent 读）
4. 两版内容同义但语言不同
```

**现阶段**（迁移期）：
- `.human/skills/` 是主，所有设计改动先写这里
- `.claude/skills/` 同步镜像 `.human/skills/` 内容（同为中文），等后期再翻译

**后期**（稳定期）：
- `.human/skills/` 保持中文设计稿
- `.claude/skills/` 写英文 prompt-engineered 版
- 同步时不是逐字翻译，而是把设计意图重新表达为 agent 高效阅读的英文

---

## 6. .human/ 目录结构图

```
.human/
├── DESIGN.md                  ← 本文：顶层架构设计
├── CLAUDE.md                  ← 根 CLAUDE.md 镜像（设计阶段同步）
│
└── skills/                    ← 中文设计稿 skill 目录
    │
    ├── main-agent/            [复现编排者]
    │   ├── SKILL.md           ─ 身份定义、10 步 workflow 编排逻辑
    │   └── workflow/          ─ 每步的 SKILL.md
    │       ├── 01-determine-target/
    │       ├── 02-extract-parameters/
    │       ├── 03-list-missing-info/
    │       ├── 04-build-minimal-model/
    │       ├── 05-submit-job/
    │       ├── 06-diagnose-failure/
    │       ├── 07-verify-physics/
    │       ├── 08-track-progress/
    │       ├── 09-build-deliverables/
    │       └── 10-standard-answer/
    │
    ├── sub-agent/             [复现执行者]
    │   ├── SKILL.md           ─ 身份声明、报告模板、子子 agent 规范
    │   └── workflow/          ─ 每步的执行脚本/工具调用指南
    │
    ├── evolution-agent/       [自迭代编排者]
    │   ├── SKILL.md           ─ 身份定义、5 步自迭代流程编排逻辑
    │   └── workflow/          ─ 每步的 SKILL.md
    │       ├── 01-concurrent-review/
    │       ├── 02-cluster-and-plan/
    │       ├── 03-concurrent-skill-work/
    │       ├── 04-validate-and-replay/
    │       └── 05-generate-report/
    │
    ├── sub-E-agent/           [自迭代执行者]
    │   ├── SKILL.md           ─ 身份声明、审查模板、蒸馏/验证规范
    │   └── workflow/          ─ 每步的执行脚本/工具调用指南
    │
    ├── optics-mie-reproduction/   ← 从 optics_agent 复制，Mie 复现流程 + 4 层检验 + verifier
    ├── optics-magnus-platform/    ← 从 optics_agent 复制，Magnus 平台操作
    ├── optics-magnus-artifacts/   ← 从 optics_agent 复制，artifact 格式
    ├── optics-agent-core/         ← 从 optics_agent 复制，基础路由
    └── skill-creator/             ← 从 optics_agent 复制，skill 创建/转换工具
```

---

## 附录：设计依据

- 自迭代 4 角色拆分灵感：EDV (arXiv 2606.24428) — 执行者不总结自己
- 经验 4 type 分类灵感：EvolveR (arXiv 2510.16079) — GUIDING/CAUTIONARY/FACT/PROCEDURE
- 自动留痕 + 分级升级灵感：ECC (222k ⭐) — hook 强制留痕、置信度、升级门槛
- 四选一裁决灵感：ECC /learn-eval — Save/Improve/Absorb/Drop
- 双写机制：本项目特有 — 人看中文设计稿 vs agent 读英文 prompt
- 详见 `notes/self_iteration_design-CN.md`
