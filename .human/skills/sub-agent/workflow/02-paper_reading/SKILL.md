# 02-paper_reading（子 agent 视角）

## 具体怎么干

### 阅读重点（按顺序）
1. abstract — 物理问题是什么
2. introduction — 背景和动机
3. modeling section — 数值/理论方法
4. target figure + caption + nearby text — 目标图算什么
5. 参数段 — 半径/折射率/波长/边界条件

### 参数抽取规范
- 每个参数标：值、单位、来源（论文第 X 页第 Y 段）
- 单位核对：论文常用 nm，公式常用 m，统一记录原文单位，换算在代码阶段做
- 缺失参数明确列进 missing_info.md，不假装有

### 搜索补充（需要时）
- 物理论文优先 `paper-search-wos` / Web of Science
- AI 相关用 `arxiv-research`
- 非论文用 `exa`
- 搜索结果标 trust score（教材>经典论文>近期 arXiv>博客）

### Gustation 集群资源搜索
- 目的：找别人公开的 Magnus 蓝图和 SKILL，看有没有同类物理问题的复现可借鉴
- 怎么查：
  1. SSH 到 Gustation：`ssh zhangyuanzheng@Gustation`
  2. 查 `/data/public/` 下各目录的 `*.magnus.blueprint.yaml` / `*.magnus.skill.yaml` 文件：
     ```bash
     find /data/public -name "*.magnus.blueprint.yaml" -o -name "*.magnus.skill.yaml" 2>/dev/null
     ```
  3. 用 Magnus CLI 查公开蓝图库（需要 magnus SDK 配置 token，`magnus address` + `magnus token` 从 secret.json 取）：
     ```python
     import magnus
     magnus.list_blueprints()
     ```
  4. 看名含关键词的，下载描述或源码判断是否相关
- trust score：
  - 同类物理问题 + 经过 COMSOL Magnns 成功运行的蓝图：高
  - 同类物理问题但仅定义未验证：中
  - 同平台（Magnus/COMSOL）但不同物理：低参考
  - 目录结构/工程组织方式：可不打分，当作模板参考
- 注意：Gustation 是校园内网集群，不能访问公网，所有搜索限在集群文件系统和 Magnus API 范围内

### 预制脚本（scripts/）
- `build_param_table.py` — 把抽取的参数格式化成 parameter_table.md

## 输出约定

- 理解笔记：`.work/.todo/{paper}/{case}/paper_understanding.md`
- 参数表：`.work/.todo/{paper}/{case}/parameter_table.md`（值+单位+来源）
- 缺失信息：`.work/.todo/{paper}/{case}/missing_info.md`

## 常见坑

- 别凭印象记参数，必须回原文核
- 单位错一个量级全错，重点核对
- 论文 sometimes 用 μm 有时用 nm，混用时要标清
- "implicit parameter"（如背景折射率默认 1）也要记

## 人工 gate ①

这步末停下来，让用户核对参数和单位。你在报告第 6 字段列出"建议用户重点核对哪些参数"。
