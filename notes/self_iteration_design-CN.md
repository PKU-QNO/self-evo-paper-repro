# 自迭代怎么改框架 — 用 ECC 经验的人话版

> 2026-06-29。给用户审的方案，不是最终稿。看完批注我再改。
> 配合 subsubagent 和 workflow 结束自迭代工作一起看。

---

## 一、ECC 是怎么做的（人话版）

ECC（222k 星）核心就一句话：**agent 每次干活时自动留痕，攒够痕迹就自动总结成经验，攒够经验就自动升级成技能**。

它具体这么转：

```
agent 每次调工具
  → hook 自动记一条 observation（不靠 agent 自觉）
  → 后台有个小模型（Haiku）定时翻最近 500 条痕迹
  → 发现重复模式就写成一条 instinct（原子经验，带置信度 0.3-0.9）
  → instinct 攒够 2 条相似的就 /evolve 聚成 skill
  → skill 在多个项目都用上就 /promote 升成全局
```

**它做得好的**：
- 留痕是 hook 强制的，不靠 agent 自己记得写
- 经验带置信度，按出现次数给分（1-2 次=0.3，6-10 次=0.7）
- 升级有门槛（聚类≥2 才成 skill，跨项目≥2 才升全局）
- 有个 /learn-eval 四裁决：每条经验要么 Save、要么 Improve 再存、要么 Absorb 进已有的、要么 Drop

**它没有的（正好是我们的壁垒）**：
- 没有 replay（改完不验证旧任务有没有跑坏）
- 没有 human gate（自动升级，人不看）
- 没有 sandbox（直接改正式文件）
- 没有物理 verifier（它搞的是编程，没有客观物理对错）

**结论**：ECC 的"自动留痕 + 分级升级"值得抄，但它的"自动拍板"不能抄——我们要在人这一层加 gate。

---

## 二、我们框架具体怎么改（说人话）

### 改动 1：workflow 跑的时候自动留痕，不靠子 agent 自觉

**现在的问题**：sub-agent SKILL.md 写了"结束前写工作报告"，但靠 agent 自觉。agent 忙起来可能糊弄。

**怎么改**：学 ECC 的 hook 思路，但咱们没有 hook 基础设施，用**主 agent 强制**代替。主 agent spawn 子 agent 时，spawn 指令里写死两条硬要求：
1. 任务做完必须写报告到 `.work/.sub-report/`，否则主 agent 不接受返回
2. 报告必须填 8 个字段（特别是第 6 字段决策性回答），缺字段主 agent 打回去重写

**落地**：改 main-agent SKILL.md 的"走每步固定动作"，把"读报告"改成"校验报告字段齐全再读"。不需要真 hook，用主 agent 当质检员。

### 改动 2：自迭代时分四个角色，禁止执行者自己总结

**现在的问题**：现在 step 10 让跑复现的子 agent 自己写经验报告——这就是 self-bias 源头（自己干自己夸）。

**怎么改**：学 EDV（arXiv 2606.24428），把自迭代拆成四个角色，执行者只干活不总结：

```
执行者 = 跑 10 步 workflow 的那些子 agent（只产出 capsule 工作报告，不写经验）
审查者 = 自迭代时新 spawn 的几个子 agent，各自独立审同一批 capsule
蒸馏者 = 主 agent 拿多份审查报告做对比，提取跨 case 的共性
裁决者 = 用户（human gate）+ 物理 verifier（客观判）
```

**关键**：执行者只产原始工作报告（capsule），不产经验总结。经验是审查者+蒸馏者事后提炼的。这样执行者没法自己夸自己。

**落地**：自迭代 workflow 单独 5 步（见下面第四节），和复现 workflow 分开。复现 workflow 的 step 10 只产 capsule，不自迭代；自迭代 workflow 积累 10 篇后单独跑。

### 改动 3：经验分四种，不是一锅烩

**现在的问题**：现在"经验报告"是笼统的，什么都往里塞。

**怎么改**：学 EvolveR（arXiv 2510.16079），经验分四种 type，存储和升级门槛不同：

| type | 是什么 | 例子 | 存哪 | 升级门槛 |
|------|--------|------|------|---------|
| GUIDING | 成功根因 | "提前做网格收敛验证避免发散" | 提示词备注 | 1 次就能记 |
| CAUTIONARY | 失败教训 | "材料虚部没确认就跑全波会错" | pitfalls_log | 1 次就要记 |
| FACT | 可验证碎片 | "Fig3 波长扫描 600-800nm" | memento fact | 1 次就记 |
| PROCEDURE | 可复用流程 | "对比论文图先 min-max 归一化" | skill candidate | ≥2 case 才升 active |

**落地**：sub-agent 工作报告第 8 字段"长期记忆更新"要标 type。自迭代时蒸馏者按 type 分流到不同存储。

### 改动 4：经验裁决用四选一，不是二选一

**现在的问题**：现在经验要么采纳要么扔，太粗。

**怎么改**：学 ECC 的 /learn-eval，每条候选经验四选一：

- **Save**：独特、具体、scope 清楚 → 直接存 candidate
- **Improve then Save**：有价值但要打磨 → 列出改进点 + 修订版再存
- **Absorb into [已有skill]**：该并入已有 skill → 展示 diff + 合并建议
- **Drop**：琐碎/冗余/太抽象 → 说明为什么扔

**关键**：Absorb 和 Improve 是高质量经验处理的主路径，二选一会把该合并的强行新建、该打磨的硬采纳。

**落地**：自迭代 workflow 的 quality_gate 步骤用这个四选一。

### 改动 5：改 skill 前必须跑回归，不能只看"好像更好"

**现在的问题**：现在沙箱草稿规则写了"过 gate 才同步"，但没说怎么验证"过"。

**怎么改**：学 PACE（arXiv 2606.08106）+ SEAGym（arXiv 2606.17546），改 skill 前后用同一批旧 case 跑对比：

```
改 skill 前：
1. 冻结当前 skill 版本
2. 在旧 replay set（至少 3 篇已完成的复现）上跑新 skill vs 旧 skill
3. 检查旧成功 case 有没有退化（pass/fail 不变或改善）
4. 在新 transfer case（和本次相关的未跑论文）上测泛化
5. 只有"无退化 + 新 case 有改善"才进 human gate
6. 用户确认后 candidate 升 active，旧 skill 标 deprecated
```

**落地**：自迭代 workflow 的 validate_and_replay 步骤。这需要有个 replay set——就是之前完成的那些 Mie case。初期 replay set 小（就 1-2 篇），先跑通流程，后面攒。

### 改动 6：记忆写入带来源证据，不是裸存

**现在的问题**：现在 memento 写记忆没强制带来源。

**怎么改**：每条记忆写入必须带五要素（学 SkillEvolBench + safety risk 教训）：

```
source: 来自哪篇论文复现（paper_id + figure）
evidence: 支撑该记忆的具体数据/代码片段/轨迹
confidence: 0.3/0.5/0.7/0.85（按 ECC 频次规则）
risk_scope: 正常使用/高风险操作/仅参考
expires_at: 可选过期时间
```

**落地**：sub-agent 工作报告第 8 字段、自迭代蒸馏者写记忆时，都带这五要素。memento 的 memory_store 本身支持 tags，用 tags 装这些。

---

## 三、subsubagent 怎么落到框架（你说重点看这个）

你之前说"sub-agent 积极调 subsubagent 解决小问题，但没想好怎么写"。我起草进 sub-agent SKILL.md 了，这里说人话讲清楚逻辑。

### 什么时候该 spawn subsubagent

subsubagent 是**第 3 层，不再往下 spawn**（防 depth 爆）。它适合"单点小活"——不需要多步推理、不需要写代码、就干一件确定的事：

| 该 spawn | 不该 spawn |
|----------|-----------|
| 提取一张图的数值（数字化） | 需要多步推理的活（自己做） |
| 跑一个单独 verifier 脚本看结果 | 需要写代码的活（自己做） |
| 查/核一个公式 | 整个子任务（那是你自己的职责） |
| 算 RMSE 等量化对比 | 需要决策的活（报给主 agent） |
| OCR 一段公式 | 改其他子 agent 的文件（除非任务就是 debug） |

### subsubagent 怎么管

- 读同一个 `sub-agent` skill（身份一致，它也是"子 agent"，只是任务更小）
- 任务单要小、明确、单点
- 限定只读范围（比如只能读某个 PDF 某一页）
- 报告用**简化模板**（只填 3 字段：身份/做了什么/结果），不填 8 字段——它是来干小活的，不写长报告
- subsubagent 报告由 spawn 它的子 agent 汇总进自己的报告

### 落地

sub-agent SKILL.md 已经有这节了。你要看的是：举例合不合你的想法、要不要加/删 subsubagent 的使用场景。批注时重点看 sub-agent SKILL.md 的"子子 agent 规范"那节。

---

## 四、自迭代 workflow 5 步（workflow 结束后的单独流程）

这和你之前 HANDOFF 文档里写的自迭代 workflow 一致，我用 ECC 经验细化了。**这个流程不在 10 步复现 workflow 里，是攒够 10 篇后单独触发的**。

```
自迭代 workflow（5 步，积累 10 篇后触发，全 human gate）

1. concurrent_review    [并发×10]  审查 + 质询
   - 10 个子 agent 各自独立审一篇的 capsule（执行者不参与审自己）
   - 每个审查者输出：这篇 capsule 的成功/失败/关键发现
   - 学 EDV：执行者不总结自己，审查者是事后第三方

2. cluster_and_plan     [agent]  聚类 + 规划 skill 修改
   - 主 agent 拿 10 份审查报告做跨 case 对比
   - 提取共性 pattern（哪些坑反复出现、哪些技巧反复有效）
   - 按 4 type 分流：GUIDING/CAUTIONARY/FACT/PROCEDURE
   - 规划要改哪些 skill，每个改写草稿到 .work/self-iteration/

3. concurrent_skill_work [并发×M]  每个 skill 一个子 agent
   - M 个子 agent 各改一个 skill 的草稿
   - 只碰 skill 内容 + 提示词备注，不碰 workflow 拓扑/蓝图/AGENTS
   - 改完用 skill_to_yaml.py 导出草稿

4. validate_and_replay   [agent→script]  验证 + replay regression
   - 新旧 skill 在旧 replay set 上跑对比
   - 检查旧 case 无退化 + 新 case 有改善
   - 跑物理 verifier（能量守恒等客观判据）
   - 这步是防 self-bias 的客观闸门

5. generate_report       [agent]  治理报告 + human gate
   - 生成治理报告：改了什么/为什么/验证结果/风险
   - 每条候选经验四选一裁决（Save/Improve/Absorb/Drop）
   - 用户审，通过的 candidate→active，旧标 deprecated
   - 未通过的留沙箱草稿（不许删）
```

### 和复现 workflow 的关系

```
复现 workflow（10 步 + 主 agent 第 11 步）
  → 每篇论文产 capsule（工作报告 + benchmark 条目）
  → step 10 只产 capsule，不自迭代
  → 攒 10 篇

自迭代 workflow（上面 5 步）
  → 拿 10 篇的 capsule 做批量治理
  → 全 human gate
  → 产出升级后的 skill
```

**关键**：复现和自迭代是两个独立 workflow，不混在一起。复现时只管复现+留痕，自迭代时才批量提炼经验。这样执行者不会在复现中分心去"总结自己"。

---

## 五、不照搬 ECC 什么（差异化壁垒）

ECC 能自动升级，我们要人工 gate。这是劣势也是壁垒：

| ECC | 我们 |
|-----|------|
| 自动升级，快 | 人工 gate，慢 |
| 编程任务，对错看测试 | 物理复现，对错看物理 verifier + 量纲 + 误差 |
| 没有客观物理判据 | 有能量守恒/光学定理/瑞利极限等硬约束 |
| 改完不验证旧任务 | 改完必须跑 replay regression |
| 经验可带毒（Zombie 攻击命中过） | 记忆写入带 provenance + trust_level |

**我们的卖点不是"自动"，是"垂域可验证"**——ECC 那套自动化我们抄留痕和分级，但不抄自动拍板。物理正确性靠客观 verifier，不靠 agent 自评。

---

## 六、要你拍板的 6 个问题

1. **自迭代触发条件**：攒 10 篇触发，还是你想改成 5 篇/3 篇就触发？
2. **执行者不总结自己**：这个能接受吗？（这是防 self-bias 的核心，但意味着 step 10 子 agent 不写经验，只产 capsule）
3. **经验 4 type 分类**：GUIDING/CAUTIONARY/FACT/PROCEDURE 这四类够吗？要加/删？
4. **四选一裁决**：Save/Improve/Absorb/Drop，能接受吗？
5. **replay regression 强度**：初期 replay set 小（1-2 篇），先跑通流程后面加，OK 吗？还是要等攒够才开自迭代？
6. **自迭代 workflow 要不要现在就建 skill 文件**（main-agent/self-iteration/ + sub-agent/self-iteration/ 目录已建好），还是等复现 workflow 跑通再建？

批注完这 6 个，我就把自迭代 workflow 5 步的 SKILL.md 写出来，和复现 10 步对称。
