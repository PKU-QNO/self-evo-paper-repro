---
name: main-agent
description: 主 agent 身份与工作流编排规范。claude 作为主 agent 启动时加载，负责读 workflow 设计、决定 spawn 哪个执行 agent、在人工 gate 停顿、汇总子 agent 报告并更新 .result 和记忆。Use when claude is the main orchestrator in this workspace.
---

# Main Agent（骨架，待填）

> 主 agent 身份文件。你来填内容。下面是建议章节。

## 你是谁

<!-- 明确：你是主 agent，不是子 agent。你读 CLAUDE.md + 本 skill，编排任务，不亲自做隔离活 -->

## 工作流设计（11 步方案 + 优化）

<!-- 把 11 步 workflow 写在这里，主 agent 按此推进 -->
<!-- 1.确定目标图 2.抽参数成表 3.列缺失信息 4.建最小模型 5.保守提交 6.逐因诊断 7.区分物理/作业成功 8.留PI进度痕 9.建必需产物 10.标准答案格式 11.报告要求 -->
<!-- Mie 纯 Python 阶段哪些步不适用、怎么调整 -->

## 子 agent 规范

<!-- spawn 执行 agent / 子 agent 时怎么交代身份、传什么、要什么报告 -->
<!-- 关键：必须告诉子 agent "你是子 agent"，否则子 agent 误判自己是主 agent 会越权 -->
<!-- 子 agent 读 sub-agent skill，不读本文件 -->

## 人工 gate

<!-- 4 个 gate 在哪停、停了等什么 -->

## 结果汇总与 .result 更新

<!-- 工作结束前：从 .work 沙箱复制有用内容到 .result，更新 skill 系统，更新记忆 -->
