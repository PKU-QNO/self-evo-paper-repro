# 03-concurrent_skill_work（sub-E-agent 视角）

## 具体怎么干

你被分配改**一个** skill 的草稿。只碰 skill 内容 + 提示词备注，不碰其他。

### 修改步骤

1. **读当前 skill**：读 `.claude/skills/<skill-name>/SKILL.md`（如果是多文件 skill，全部读）
2. **读修改计划**：读 `.work/.evolution/<timestamp>/plan.md` 中你对这个 skill 的修改项
3. **读相关 capsule**：读修改计划引用的 capsule 工作报告 + 审查报告
4. **读 .todo 草稿**：读 `.work/.todo/` 下该 skill 相关的单论文草稿（如果有）
5. **导出 yaml 草稿**：
   ```
   python C:\Users\27370\.codex\skills\.system\skill-creator\scripts\skill_to_yaml.py \
       .claude/skills/<skill-name> \
       --output .work/.evolution/<timestamp>/drafts/<skill-name>.skill.yaml
   ```
6. **修改 yaml 草稿**：在 yaml 上做改动，每条改动边标注来源 case
7. **保存草稿**：不改 `.claude/skills/` 原文

### 工具

- `skill-creator/scripts/skill_to_yaml.py` — 导出 skill 为 yaml 草稿
- `skill-creator/scripts/yaml_to_skill.py` — 草稿恢复为 skill（别用，gate 通过了再用）
- 可 spawn 子子 agent 帮你做 diff 对比（改前改后）

### 修改范围（允许）

- ✅ skill/SKILL.md 内容增补、修改、删除
- ✅ 提示词备注（如 SKILL.md 第 1 行的 description）
- ✅ 引用错误修复
- ✅ 补充用例/公式/参数范围

### 修改范围（禁止）

- ❌ workflow 拓扑（workflow/ 下其他 SKILL.md）
- ❌ 蓝图结构（`.magnus/`）
- ❌ AGENTS.md / CLAUDE.md
- ❌ 自迭代系统自自身（evolution-agent / sub-E-agent skill）
- ❌ 其他 skill 的文件
- ❌ `.claude/skills/` 原文直接修改

### 输出约定

- 草稿：`.work/.evolution/<timestamp>/drafts/<skill-name>.skill.yaml`
- 每条改动要有标注：`# 来源：<capsule_id> - <审查报告建议>`
- 如果 evolution-agent 分配错了（这 skill 不需要改），在报告里注明 "skipped：理由"

### 常见坑

- **不要过度修改。** capsule 数据支撑什么就改什么，不额外发挥
- **不要漏掉原 skill 的关键部分。** 导出 yaml 后确认没有遗漏字段
- **保留原 skill 的结构。** 不重新组织、不重新分类、不加无关内容
- **改动标注要具体。** 不仅写"来源：Mie case"，要写"来源：Mie-case-3 - 审查者发现步骤 2 遗漏了散射角范围检查"
- **如果 capsule 支撑不足，写"blocked"不要蒙**

## 决策问题重点

1. **改了什么**：逐项列出，每项标注来源
2. **有没有超范围**：确认没有碰禁止区域
3. **旧 case 风险**：这个改动你觉得会导致旧 case 结果变化吗？
4. **完整性**：有没有遗漏原 skill 的关键内容？
