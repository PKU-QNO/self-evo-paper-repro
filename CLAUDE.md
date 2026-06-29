# CLAUDE.md（骨架，待填）

> 这是 claude 在本工作区（self-evo-paper-repro）启动时强制读的简短路由文件。
> 设计原则：只放路由和红线，不塞具体流程。流程在各 skill 和 agent 身份文件里。
> 你来填内容。下面是建议的章节占位。

## 工作区身份

<!-- 一句话说明这是什么工作区、交付什么、不交付什么 -->

## 三层 agent 架构

<!-- 主 agent 读 main-agent skill；spawn 执行 agent 时执行 agent 读自己的身份 skill；再 spawn 子 agent 时同理 -->
<!-- 哪些 skill 主 agent 必读，哪些按任务路由加载 -->

## 目录约定

<!-- .paper 论文原文区 / .work agent 沙箱软约束 / .result 最终交付区 -->
<!-- 过程文件、SKILLNAME.yaml 自迭代草稿、结构化工作报告放哪 -->

## 安全红线

<!-- 不读 secret、不污染 papers 原文、不直接写 .result 需经主 agent 复制 -->

## skill 路由表

<!-- 哪类任务加载哪个 skill -->
