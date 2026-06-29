# CLAUDE.md — self-evo-paper-repro 工作区

> 这是 claude 在本工作区启动时强制读的简短路由文件。只放路由和红线，不塞具体流程。
> 流程在 `.claude/skills/` 下的 4 个 agent 身份 skill 里。

## 工作区身份

光学论文复现自进化 agent。交付 SKILL 蓝图（主）+ benchmark 数据（次），不交付自迭代内容本身。自迭代是手段。

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

## 目录约定

```
.paper/        论文原文区（只读，不污染）
.work/         agent 工作沙箱（软约束）
  ├── .sub-report/    子 agent 完整报告统一放这里
  ├── mie/            Mie 复现过程文件
  ├── comsol/         COMSOL 复现过程文件
  ├── self-iteration/ .skill.yaml / .blueprint.yaml 沙箱草稿（不许删）
  └── memento-cache/
.result/       最终交付区，主 agent 工作结束前从 .work 复制有用内容过来
papers/        -> optics_agent/papers (junction)
reproduction_test/ -> optics_agent/reproduction_test (junction)
```

## 沙箱草稿规则（防回滚崩溃）

**更新 `.claude/skills/` 任何 skill 前，必须先在 `.work/self-iteration/<skill-name>.skill.yaml` 写草稿，草稿不许删。**

草稿字段：改了什么 / 为什么改 / 验证结果 / 来源 case。主 agent 工作结束前把通过 gate 的草稿同步到 `.claude`，未通过的留沙箱。沙箱草稿是变更留痕，防回滚崩溃。

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
| 项目基础路由 | `optics-agent-core` |
| 创建/规范 skill | `skill-creator` |

## skill 与 blueprint 格式

skill 文件夹和 `.skill.yaml` 互转用 `skill-creator/scripts/skill_to_yaml.py` 和 `yaml_to_skill.py`。`.blueprint.yaml` 是可执行任务模板（参数+提交），`.skill.yaml` 是知识包（文件集合）。
