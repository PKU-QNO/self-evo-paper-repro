# 11-main_agent_report（主 agent 自己写）

## 这步干什么

主 agent 写全局总结报告。子 agent 的 step 10 是经验+记忆+双报告，本步是主 agent 站在编排者视角的总览。

## 这是主 agent 你自己做的，不是 spawn 子 agent

### 4 类文档汇总定稿

子 agent step10 产出 4 类文档初稿放沙箱，本步你来做汇总定稿：

**1. 全过程报告**（`.result/<paper>/full_report.md`）
- 基于子 agent 草稿 `.work/<case>/full_report_draft.md`
- 补充主 agent 编排视角的全局判断
- 每步引用于 agent 报告的路径
- 保留决策过程和问题记录

**2. 简报**（`.result/<paper>/brief.md` + 更新 `todo.md`）
- ★ 主 agent 把关：精简到一页，突出 PI 关心的结论
- 不要技术细节堆积，要结果 level + 关键数值 + 一句话结论
- 同时更新 `todo.md` 中本 case 的状态

**3. SKILL 更改建议**（`toEflow/<paper>.skill-suggestion.md`）
- 基于子 agent 草稿，主 agent 确认 tier 级别和适用边界
- 只增不删原则
- 如果子 agent 建议多个，主 agent 排序优先级

**4. 蓝图建议**（`toEflow/<paper>.blueprint-suggestion.md`）
- ★ 主 agent 把关：确认是否需要上 Magnus
- 如果需要：检查蓝图是否有扫描参数泛化能力（见 template）
- 如果纯 Python：明确写"本次无需蓝图"

### 填写主 agent 报告

读 `references/main_report_template.md`，填 8 个字段：
1. 本次复现概况
2. 10 步执行轨迹（引用各步子 agent 报告路径）
3. 关键决策点回顾（你在哪些节点拍了板）
4. 人工 gate 记录
5. 最终成果（进 .result 的、benchmark、skill 更新）
6. 自迭代建议
7. 给下一篇的接力
8. 长期记忆更新摘要

### 写 run manifest

复现 workflow 结束前，主 agent 必须在 `.work/run_manifest.yaml` 写审计索引：
- `run_id`、`timestamp`、`case`
- `spawned_agents`：数量、各 agent 角色、负责节点、depth
- `fan_out`：哪个节点并发了几个子 agent
- `max_depth_reached`
- `result_class`：使用 CLAUDE.md 的 7 级枚举之一
- `retry_fingerprints`：每步重跑 fingerprint、修改点、新证据/新假设、结果

`run_manifest.yaml` 只做索引，证据仍引用各步报告和 artifact。

## 写完之后

1. 从 `.work` 复制有用内容到 `.result/`（问用户哪些确认）
2. 通过 gate 的 skill 草稿同步到 `.claude`（用 yaml_to_skill.py）
3. 更新 memento 长期记忆（全局结论）
4. 报告写到 `.work/.sub-report/main-<case>-<timestamp>.md`，也复制一份到 `.result/reports/`
5. 写 `.work/run_manifest.yaml`，记录 fan-out/depth/result_class/retry_fingerprints；`result_class` 使用 CLAUDE.md 的 7 级枚举之一

## 人工 gate

最终确认。用户看了主 agent 报告后决定哪些进 .result、哪些 skill 草稿通过。

## 本步 sub-agent spawn 局部模版

本步由主 agent 自己执行，不 spawn sub-agent。

## workflow 结束
