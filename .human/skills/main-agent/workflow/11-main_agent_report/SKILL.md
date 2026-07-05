# 11-main_agent_report（主 agent 自己写）

## 这步干什么

主 agent 写全局总结报告。子 agent 的 step 10 是经验+记忆+双报告，本步是主 agent 站在编排者视角的总览。

## 这是主 agent 你自己做的，不是 spawn 子 agent

### 4 类文档汇总定稿

子 agent step10 产出 4 类文档初稿放沙箱，本步你来做汇总定稿：

**1. 全过程报告**（`.result/<paper>/full_report.md`）
- 基于子 agent 草稿 `.work/.todo/{paper}/{case}/full_report_draft.md`
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

### 写 capsule（E-flow 输入契约，强制，100% fire——2026-07-04 补 A1 生产侧）

复现 workflow 结束前，主 agent **必须**产出 `.work/.result/<case>/capsule.md`（E-flow step01 唯一输入；不靠自觉，本步验收含"capsule 存在且字段齐全"）。字段：`processed: false` / `run_id` / `case` / `timestamp` / `result_class`（7 级）/ `evidence_refs` / provenance 五要素；正文含"什么真的断了/什么有效"清单 + 候选经验（4 type）。

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
6. **写 `.work/.result/<case>/capsule.md`（强制，见上节）**——缺则本步不算完成
7. **增量更新 WORK_LOG（强制，见 `CLAUDE.md`「WORK_LOG 维护规范」）**——向该篇 `WORK_LOG/<NN>-<papername>-v<N>.md` 追加本 run 带日期条目（做了什么/关键决策+为什么/引用产物路径/下一步）+ 更新决策台账（CC 建议→用户裁决→落点+memento id）+ 顶层 `WORK_LOG.md` 摘要表更新一行。只增不改历史；与 todo 分工（todo 记待办、WORK_LOG 记叙事+决策，数据只引用不重抄）。分文件按论文，多次复现分 `-v1/-v2`（version 由用户第一句话给）。缺则本步不算完成。

## 人工 gate

最终确认。用户看了主 agent 报告后决定哪些进 .result、哪些 skill 草稿通过。

## 本步 sub-agent spawn 局部模版

本步由主 agent 自己执行，不 spawn sub-agent。

## workflow 结束
