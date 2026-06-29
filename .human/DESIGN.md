# .human/ 顶层设计文档

> 人看的中文设计稿，不是 prompt-engineered 的 agent skill。读者：项目成员、PI、任何想理解系统架构的人。
> 后期 `.claude/skills/` 会写英文 4 身份 agent-skill，这里是设计源头。
> 本文整合了 2026-06-29 会话所有决策，是完整的项目计划。

---

## 1. .human/ 定位

`.human/` 是**人话版中文审查稿**，给人看的。`.claude/` 是英文 prompt-engineered 执行版，agent 运行时读。

核心原则：
- **现阶段 `.human/` 是主**，所有设计改动先写这里，等设计稳定后再翻译/优化成英文放进 `.claude/skills/`
- **双写机制**：workflow 更新 skill 时同时写两处——`.human/skills/<skill>/`（中文设计稿）和 `.claude/skills/<skill>/`（英文版）。两版内容同义但语言不同
- **不是** agent 运行时读的文件。agent 读 `.claude/skills/`，人读 `.human/`

目录结构：
```
.human/
├── DESIGN.md           ← 本文，顶层设计
├── CLAUDE.md           ← 根 CLAUDE.md 镜像（设计阶段同步）
└── skills/             ← 中文设计稿 skill
    ├── main-agent/         复现编排者
    ├── sub-agent/          复现执行者
    ├── evolution-agent/    自迭代编排者
    ├── sub-E-agent/        自迭代执行者
    ├── optics-mie-reproduction/
    ├── optics-magnus-platform/
    ├── optics-magnus-artifacts/
    ├── optics-agent-core/
    └── skill-creator/
```

**后期稳定期**（当前不急着做）：
- `.human/skills/` 保持中文设计稿
- `.claude/skills/` 写英文 prompt-engineered 版（只放 4 个 agent 身份 skill）
- 同步时不是逐字翻译，而是把设计意图重新表达为 agent 高效阅读的英文

---

## 2. 4 Agent 架构

系统由四个 agent 身份 skill 驱动，分两套完全对称的 workflow：

### 复现 workflow

| 身份 | skill 名 | 职责 |
|------|---------|------|
| 复现编排者 | `main-agent` | 读 main-agent skill，编排 10 步复现流程；spawn 子 agent、校验报告、汇总结果 |
| 复现执行者 | `sub-agent` | 读 sub-agent skill，执行单步任务（读图抽参、搭模型、跑代码、写报告） |
| 子子 agent | 复用 sub-agent | 被子 agent spawn 做单点小活，第 3 层不再 spawn |

### 自迭代 workflow

| 身份 | skill 名 | 职责 |
|------|---------|------|
| 自迭代编排者 | `evolution-agent` | 编排 6 步自迭代流程（并发审查→聚类规划→并发改 skill→验证 replay→治理报告→全局总结） |
| 自迭代执行者 | `sub-E-agent` | 被 evolution-agent spawn，执行审查 capsule、改 skill 草稿、跑验证等具体任务 |

### 两套对称

```
复现 workflow                 自迭代 workflow
─────────────────            ─────────────────
main-agent（编排 10 步）       evolution-agent（编排 6 步）
  └─ sub-agent（执行）           └─ sub-E-agent（执行）
      └─ sub-agent（子子，第3层）    └─ sub-E-agent（子子，第3层）
```

**互不交叉**：
- 复现 workflow 只产 capsule（工作报告 + benchmark 条目 + skill 草稿），不自迭代
- 自迭代 workflow 拿已积累的 capsule + toEflow/ 草稿做批量治理，不改复现流程
- 执行者不总结自己（子 agent 只产原始报告，不自评经验）

---

## 3. 三层 Spawn 与 Subsubagent

**规则**：
- 编排者（main-agent / evolution-agent）不亲自做隔离活
- 执行者（sub-agent / sub-E-agent）做具体步骤
- 执行者可以 spawn **子子 agent** 做单点小活，**第 3 层不再 spawn**（防止 depth 爆炸）

### 什么时候该 spawn subsubagent

subsubagent 做不需要多步推理、不需要写代码、就干一件确定的事：

| 该 spawn | 不该 spawn |
|----------|-----------|
| 提取一张图的数值（数字化） | 需要多步推理的活（自己做） |
| 跑一个单独 verifier 脚本看结果 | 需要写代码的活（自己做） |
| 查/核一个公式 | 整个子任务（那是你自己的职责） |
| 算 RMSE 等量化对比 | 需要决策的活（报给主 agent） |
| OCR 一段公式 | 改其他子 agent 的文件 |

### subsubagent 怎么管

- 读同一个 sub-agent / sub-E-agent skill（身份一致，只是任务更小）
- 任务单要小、明确、单点
- 限定只读范围（比如只能读某个 PDF 某一页）
- 报告用简化模板（只填 3 字段：身份/做了什么/结果），不填 8 字段
- subsubagent 报告由 spawn 它的子 agent 汇总进自己的报告

---

## 4. 身份选择逻辑

用户第一句话决定身份。路由规则在根 CLAUDE.md：

| 用户意图 | 身份选择 | 行为 |
|---------|---------|------|
| "复现这篇新论文" / "跑 Fig.3" / 给一篇 PDF | → `main-agent` | 加载 main-agent skill，进入 10 步复现 workflow |
| "跑自迭代" / "把 todo 里待迭代的任务完成" / "治理" | → `evolution-agent` | 加载 evolution-agent skill，进入 6 步自迭代 workflow |
| "帮我看这个脚本" / "调试" / "算个数" / "问问题" | → 不进 workflow | 不加载身份 skill，直接以当前能力执行 |
| 模糊时 | → 问用户 | "这次是复现新论文、跑自迭代，还是局部任务？" |

**关键原则**：
- 复现和自迭代是互斥入口，不会同时进入
- 局部任务不进任何 workflow，避免把简单活拖长
- 身份选择只决定加载哪个 agent skill，不换模型

---

## 5. 完整目录结构

```
.paper/                       论文原文区（只读，不污染）
  ├── scattering.pdf           Bohren & Huffman 教材（核心公式主源）
  └── mie/                     11 篇 Mie 论文 PDF

.work/                        agent 工作沙箱（软约束）
  ├── .sub-report/             子 agent 完整报告放这里
  ├── .todo/<paper>/           单论文 workflow 过程文件 + skill 草稿缓冲
  ├── .evolution/<timestamp>/  evolution 进行中工作区
  │   ├── sub-reports/         sub-E-agent 报告
  │   ├── drafts/              skill 草稿
  │   └── validation/          replay 验证结果
  ├── memento-cache/           memento 缓存
  └── (各论文中间产物)

toEflow/                       workflow→evolution 缓冲区（只增不删）
  ├── <paper>.skill.yaml       workflow 提交的 skill 草稿
  └── <paper>.todo-entry.md    workflow 提交的迭代需求

.E-history/                    evolution 历史报告（按次数排序）
  ├── 01-evolution-report.md   开机
  ├── 02-evolution-report.md
  └── ...

.result/                       最终交付区，主 agent 工作结束前从 .work 复制内容过来

todo.md                        全局日志，每次 workflow/Eflow 结束前填一段

papers/                        -> optics_agent/papers (junction)
reproduction_test/             -> optics_agent/reproduction_test (junction)
```

**论文命名规则**：`MMDD-NN-papername-vN`，如 `0629-01-akimov-mie-v1`。

---

## 6. 记忆要求

**每个 agent（main-agent / sub-agent / evolution-agent / sub-E-agent）开始行动前必须做：**
1. 搜索 memento 记忆库（`memory_search`），找和当前任务相关的已有记忆，避免重复劳动
2. 结束前必须更新记忆（`memory_store` / `decisions_log` / `pitfalls_log`），存本次的关键事实/决策/教训

子 agent **没有自动记忆注入**，主 agent spawn 时在指令里强制要求这两步。

**记忆写入带 provenance 五要素**（每条记忆必须包含）：
```
source:     来自哪篇论文复现（paper_id + figure）
evidence:   支撑该记忆的具体数据/代码片段/轨迹
confidence: 0.3/0.5/0.7/0.85（按出现频次）
risk_scope: 正常使用/高风险操作/仅参考
expires_at: 可选过期时间
```

---

## 7. 子 Agent Tools 控制

子 agent 的 MCP 工具描述是**全量注入 context**（不是懒加载），会占 context window。主 agent spawn 子 agent 时必须用 `tools` 字段（allowlist 模式）控制暴露的工具：

```
tools: Read, Write, Edit, Bash, Glob, Grep, ToolSearch, Skill
```

- allowlist 模式：只列出内置工具，MCP 工具自动排除，避免 context 膨胀
- **`ToolSearch` 必须显式包含**（否则 MCP 工具注册了但无法调用）
- `Skill` 放行让子 agent 能跑 skill-print.py 获得技能列表
- 需要某个 MCP 工具时才显式列出，不要全量暴露
- `tools` 字段不支持 `mcp__*` 通配符，要限 MCP 用 `disallowedTools`

---

## 8. 自迭代触发机制

**单论文 workflow step 10 只产 capsule + skill 草稿，不跑 replay。**

```
复现 workflow step 10
  → 产 capsule 到 .work/.todo/<paper>/
  → 同时扔进 toEflow/（只增不删，作为 evolution 输入）
  → 不自行启动自迭代

用户攒够了开专门 evolution session
  → 读 toEflow/ 所有草稿
  → 批量治理（不是逐篇治理）
  → 跑 replay regression 验证
```

**toEflow/ 规则**：只增不删。所有提交保留，evolution-agent 读全部做综合。

---

## 9. Validate_and_Replay 实现

**E-flow 不调 W-flow**（自迭代 workflow 不触发复现 workflow，避免循环依赖）。

按照改动深度分三层：

| 层 | 改动范围 | 验证方式 | 谁做 |
|----|---------|---------|------|
| **层A** | 改提示词备注/注意事项 | sub-E-agent 跑旧代码 + verifier + benchmark 对比 | E-flow 自洽 |
| **层B** | 改流程步骤 | sub-E-agent 重跑 step06-08 旧代码 | E-flow 自洽 |
| **层C** | 改核心方法/公式来源 | 报告"需人工开 W-flow 重跑"，human gate 决定 | 不重跑，标"未验证风险保留" |

**局限性**：
- selective replay 只能验证"不破坏旧 case 代码/验证"，不能验证"新 skill 推导在旧 case 也适用"
- 后者需要重跑 W-flow，初期不接受这么重的代价
- 初期 replay set 小（1-2 篇），先跑通流程

---

## 10. 自迭代 6 条改动（ECC 经验整合）

### 改动1：自动留痕靠主 agent 强制
没有 hook 基础设施，用**主 agent 强制**代替。主 agent spawn 子 agent 时写死两条硬要求：
1. 任务做完必须写报告到 `.work/.sub-report/`，否则不接受返回
2. 报告必须填 8 个字段（特别是第 6 字段决策性回答），缺字段打回去重写

### 改动2：执行者不总结自己（防 self-bias）
学 EDV（arXiv 2606.24428），把自迭代拆成四个角色：
```
执行者 = 跑 workflow 的子 agent（只产 capsule，不写经验）
审查者 = 自迭代时新 spawn 的子 agent，独立审 capsule
蒸馏者 = evolution-agent 拿多份审查做跨 case 对比
裁决者 = 用户（human gate）+ 物理 verifier
```

### 改动3：经验分 4 type
学 EvolveR（arXiv 2510.16079）：

| type | 是什么 | 存哪 | 升级门槛 |
|------|--------|------|---------|
| GUIDING | 成功根因、"提前做 XXX 避免 YYY" | 提示词备注 | 1 次就能记 |
| CAUTIONARY | 失败教训、"材料虚部没确认就…" | pitfalls_log | 1 次就要记 |
| FACT | 可验证碎片、"Fig3 波长 600-800nm" | memento fact | 1 次就记 |
| PROCEDURE | 可复用流程、"对比图先归一化" | skill candidate | ≥2 case 才升 active |

### 改动4：裁决改进（四选一 → 方案 A+C）
裸四选一（Save/Improve/Absorb/Drop）适合 coding 不适合 AI4S。改进为：

**方案A（六维裁决）**：加两个新维度
- **Fork**：经验冲突不合并，创建 scope 分支（如"core-shell 和均匀球用不同收敛策略"）
- **Archive**：负面经验存档，不是 Drop。带 source/claim/evidence/why_not_skill/scope 字段，供检索避坑

**方案C（三级治理）**：给经验加 tier 字段
| tier | 条件 | 状态 |
|------|------|------|
| Tier-1 | 单 case，无 verifier | → Archive，不进 skill |
| Tier-2 | ≥2 case 或 1 case + verifier | → candidate pending |
| Tier-3 | ≥3 case + verifier + replay 无退化 | → active，升级 skill |

tier 升级脚本化（算 case count + 跑 verifier）。

**方案B（多视角评议）**：3 审稿 agent + 1 主席——作为可选后续，裁决质量成瓶颈时再加。

**Mie 例子**：
- "银纳米球 LSPR 用 Drude 模型够用" → Tier-2（1 case + 有 verifier），pending
- "Fig3 要在 600-800nm 扫描" → 纯 FACT，Tier-1，Archive
- "Mie 系数的分母用对数导数更稳" → Tier-3（3 case + verifier + replay pass），active

### 改动5：改 skill 前跑 replay regression
改 skill 前后用同一批旧 case 跑对比：
1. 冻结当前 skill 版本
2. 在旧 replay set 上跑新 skill vs 旧 skill
3. 检查旧成功 case 有没有退化（pass/fail 不变或改善）
4. 只有"无退化"才进 human gate
5. 用户确认后 candidate 升 active，旧 skill 标 deprecated

### 改动6：记忆带 provenance 五要素
见第 6 节记忆要求。每条记忆写入必须带 source/evidence/confidence/risk_scope/expires_at。

---

## 11. 裁决改进详解（AI4S 适配）

裸四选一（ECC 的 Save/Improve/Absorb/Drop）是为编程任务设计的，对 AI4S 物理复现有三个不适应：
1. 没有"暂存"状态——实操中很多经验需要等更多 case 再判断
2. 没有"分支"机制——不同物理体系的经验可能冲突但都正确
3. 没有"避坑档案"——负面经验 Drop 掉就丢失了，别人可能再踩

### 方案A（六维裁决）

| 裁决 | 什么时候用 | Mie 例子 |
|------|-----------|---------|
| **Save** | 独特、具体、scope 清楚，可直接存 candidate | "银 LSPR 峰值随 n 介质线性红移 2nm/0.1RIU" |
| **Improve** | 有价值但需打磨 | "能量守恒验证写得太宽泛，要具体数值阈值" |
| **Fork** | 经验互相冲突但都正确，建 scope 分支 | "core-shell 用递归 Mie vs 均匀球用标准 Mie 的收敛判据不同" |
| **Absorb** | 可并入已有 skill | "Rayleigh 极限检查可以并入物理 verifier skill" |
| **Archive** | 单 case 无 verifier / 纯负面 | "Drude 参数用 Palik 实验数据比文献值偏 10%，坑已避" |
| **Drop** | 琐碎/冗余/太抽象/没价值 | "Python 版本要 3.10+"（已被基础环境覆盖） |

### 方案C（三级治理）

```
Tier-1 ──→ Archive（不进 skill，可检索避坑）
  ↑ 单 case 无 verifier

Tier-2 ──→ candidate pending（进 .work/.todo/，等更多证据）
  ↑ ≥2 case 或 1 case + verifier

Tier-3 ──→ active（正式写入 skill）
  ↑ ≥3 case + verifier + replay 无退化
```

**tier 升级脚本化**：写一个简单的脚本，遍历经验库，算每条的 case count（来源去重）+ 检查 verifier 结果，自动建议哪些可以升级。

**方案B（多视角评议）**：3 个审稿 agent 各自独立审经验 + 1 个主席 agent 综合——当前不做，等裁决质量成瓶颈再加。

---

## 12. 教材与论文

### 教材
`.paper/scattering.pdf` = **Bohren & Huffman《Absorption and Scattering of Light by Small Particles》**。核心公式 an, bn（Mie 系数）的权威来源。

### 论文
`.paper/mie/` 下有 11 篇 Mie 相关论文 PDF。论文命名 `MMDD-NN-papername-vN`。

### PyMieScatt
**已弃用**。不依赖第三方 Mie 计算库。取而代之的是**3 层物理检验**：

| 层 | 检验内容 | 描述 |
|----|---------|------|
| 1 | 物理硬约束 | 能量守恒（Q_sca + Q_abs = Q_ext）、光学定理 |
| 2 | 极限退化 | Rayleigh 极限（x→0 时 Q_sca ∝ x⁴）、大尺寸消光悖论（x→∞ 时 Q_ext → 2） |
| 3 | 论文图量化对比 | 两方一致性（数值对齐论文数据，不做统计显著性检验） |

---

## 13. todo.md + .E-history/

### todo.md
全局日志文件，在仓库根目录。每次 workflow/Eflow **结束前**填一段，格式：

```
## YYYY-MM-DD: 论文名 / 工作类型

- 论文/摘要：什么论文
- 复现结果：成功/部分/失败
- 自迭代产出：改了什么 skill，tier 变化
- 待迭代需求：哪些经验在 pending / archive
```

每次追加在文件末尾，不覆盖历史。

### .E-history/
每次 evolution 结束前写详细自迭代报告，按次数排序：

```
.E-history/
  ├── 01-evolution-report.md   第一次 evolution
  ├── 02-evolution-report.md   第二次
  └── ...
```

内容包含：本次治理范围、改了什么 skill、每条的裁决/tier/验证结果、风险记录。

---

## 14. 待解决问题

1. **四选一改进方案 A+C**：要写进 evolution-agent / sub-E-agent 的 step05 SKILL.md，尚未落地
2. **`.claude/skills/` 英文 4 身份 agent-skill**：待后期写，当前 `.human/skills/` 是主
3. **subsubagent 规范**：用户待细看批注（sub-agent SKILL.md 的"子子 agent 规范"节）
4. **Mie 第一阶段**：待用户确认教材后开始（教材已在 `.paper/scattering.pdf`）
5. **replay set**：初期小（1-2 篇），先跑通流程
6. **evolution-agent / sub-E-agent 的 `.human/skills/`**：已建，待用户批注
7. **`toEflow/` 和 `.E-history/` 目录**：尚未创建，根 CLAUDE.md 已约定，等实际运行时建
8. **tier 升级脚本**：方案 C 的脚本化需要写，当前未实现

---

## 附录：设计依据

- 自迭代 4 角色拆分灵感：EDV (arXiv 2606.24428) — 执行者不总结自己
- 经验 4 type 分类灵感：EvolveR (arXiv 2510.16079) — GUIDING/CAUTIONARY/FACT/PROCEDURE
- 自动留痕 + 分级升级灵感：ECC (222k ⭐) — hook 强制留痕、置信度、升级门槛
- 四选一裁决灵感：ECC /learn-eval — Save/Improve/Absorb/Drop，本项目扩展为方案 A+C
- 三级治理灵感：ECC 置信度门槛 + 本项目 AI4S 适配
- 双写机制：本项目特有 — 人看中文设计稿 vs agent 读英文 prompt
- validate_and_replay 分层验证：本项目的 E-flow 不调 W-flow 原则
- 详见 `notes/self_iteration_design-CN.md`
