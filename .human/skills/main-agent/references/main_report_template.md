# 主 agent 总结报告模板（第 11 步）

> 主 agent 工作结束前完成 4 类文档汇总定稿。子 agent step10 产初稿放沙箱，本步定稿投到最终目录。
> 模板中 `<>` 标记为必填。

---

## 模板 A：全过程报告 → `.result/<paper>/full_report.md`

```
# 全过程报告：<论文名> — Fig.<图号>

## 1. 任务概述
- 目标论文：<论文 DOI / arXiv ID>
- 目标图/物理量：<图号 / 物理量名>
- 物理背景：<一句话说明物理问题>

## 2. 10 步执行记录

### Step 01 — PDF 预处理
- 做了什么：<事实描述>
- 关键参数：<参数列表>
- 遇到问题：<有/无，什么>
- 结果状态：completed / blocked / failed

### Step 02 — 论文阅读
<!-- 后面每步同上格式 -->
...
### Step 10 — 总结报告
- 做了什么：产出 4 类文档初稿
- 问题：<有/无>
- 结果状态：completed

## 3. 关键决策记录
| 节点 | 决策内容 | 依据 | 谁拍的 |
|------|---------|------|--------|
| stepXX | <决策> | <依据> | main-agent / user |

## 4. 人工 gate 记录
| 节点 | 请求内容 | 用户决定 |
|------|---------|---------|
| stepXX | <gate 内容> | <用户意见> |

## 5. 最终产物清单
| 产物 | 路径 | 说明 |
|------|------|------|
| 全过程报告 | .result/<paper>/full_report.md | 本文 |
| 简报 | .result/<paper>/brief.md | 给 PI |
| SKILL 建议 | toEflow/<paper>.skill-suggestion.md | 自迭代输入 |
| 蓝图建议 | toEflow/<paper>.blueprint-suggestion.md | 自迭代输入 |
| 其他 | <列表> | |

## 6. 复现结果数值
| 物理量 | 本工作值 | 论文值 | 相对误差 | 验证状态 |
|--------|---------|--------|---------|---------|
| <量名> | <值> | <值> | <百分比> | pass/fail |

## 7. 结论
- 复现 level：<0-5>
- 一句话结论：<物理结论>

## 8. 给下一篇的接力
- <需要传递的信息>
```

---

## 模板 B：简报 → `.result/<paper>/brief.md`

```
# 简报：<论文名>

**论文**：<作者>，<期刊>，<年份>
**DOI**：<DOI>

## 目标
<一句话描述目标，如"复现 Fig.3 中 Au 纳米球散射光谱">

## 方法
<纯解析/Python 脚本/COMSOL+Magnus/混合>

## 结果
- 复现 level：<0-5>
- 关键对比：
  | 物理量 | 本工作 | 论文值 | 误差 |
  |--------|-------|--------|------|
  | <量> | <值> | <值> | <百分比> |
- 验证状态：<能量守恒/Rayleigh 极限/大尺寸极限 全部 pass / 部分 pass / fail>

## 一句话结论
<一行的物理结论，不含技术细节>

## 需要关注
<给 PI 的提醒，如"需要 COMSOL 才能推进" / "理论部分已确认，工程待实现" / "已完成">
```

复制一段更新 `todo.md`（格式随项目既有约定）：

```
- [x] <paper> Fig.<图号> — level <N>，<日期>
```

---

## 模板 C：SKILL 更改建议 → `toEflow/<paper>.skill-suggestion.md`

```
# SKILL 更改建议：<论文名> — Fig.<图号>

## 建议概览
- **来源 case**：<论文名> Fig.<图号>
- **日期**：<YYYY-MM-DD>

---

### 建议 1：<技能名> — <缺陷摘要>

**tier**：P0（必须修） / P1（值得修） / P2（建议但暂不修）
**影响 skill**：`<skill 名>/SKILL.md`
**适用边界**：
- applies_when：<什么情况下会出现这个问题>
- does_not_apply_when：<什么情况下不会>

**原文不足**：
```
<现有 SKILL 中哪段/哪条不够或缺失>
```

**改进建议**：
```
<建议怎么改或加什么>
```

**本次 case 实例**：
```
<本次复现中遇到的具体实例，方便 evolution-agent 理解>
```

---

### 建议 2：...（可多条，只增不删）

---

## 优先级排序
1. <P0 的按重要性排>
2.
3.

## 备注
<其他注意事项，如"这条与建议 1 冲突，选一个实现">
```

---

## 模板 D：蓝图建议 → `toEflow/<paper>.blueprint-suggestion.md`

```
# 蓝图建议：<论文名> — Fig.<图号>

## 本次是否需要蓝图
<需要 / 不需要 — 本次纯 Python 无需上 Magnus>

## 如需蓝图

### 蓝图目标
<蓝图要复现什么物理问题>

### 参数声明（必须用 Annotated，支持单值和扫描列表）

```python
from typing import Annotated, Union, List

# 单值参数
wavelength: Annotated[float, "Wavelength in nm", lambda: 500.0]
radius: Annotated[float, "Particle radius in nm", lambda: 50.0]
n_medium: Annotated[float, "Refractive index of medium", lambda: 1.33]

# 扫描参数
wavelength_scan: Annotated[List[float], "Wavelength scan range in nm", lambda: [400, 800, 1.0]]
radius_scan: Annotated[List[float], "Radius scan range in nm", lambda: [10, 100, 5.0]]
```

### scan_parameters 字段

```
scan_parameters:
  - parameter: wavelength
    label: "波长"
    range: [400, 800]       # [min, max]
    step: 1.0               # 步长（nm）
    default: 500.0
    type: float
  - parameter: radius
    label: "粒子半径"
    range: [10, 100]
    step: 5.0
    default: 50.0
    type: float
  - parameter: n_medium
    label: "介质折射率"
    range: [1.0, 2.0]
    step: 0.1
    default: 1.33
    type: float
```

### 泛化能力验证

| 验证项 | 是否满足 | 说明 |
|-------|---------|------|
| 支持参数扫描（非单点） | 是/否 | |
| 扫描参数可配范围+步长 | 是/否 | |
| 支持混合扫（多参同时） | 是/否 | |
| 参数有物理类型和默认值 | 是/否 | |
| 可泛化到同类物理问题 | 是/否 | <如从本 paper 半径扫泛化到一般 Mie 散射半径扫> |

### 同类问题参数空间映射

```
本 paper 参数：
  wavelength: 400-700 nm（可见光范围）
  radius: 20-80 nm

同物理问题泛化参数空间（Mie 散射）：
  wavelength: 200-2000 nm（UV-VIS-NIR）
  radius: 1-500 nm
  n_core: 1.0-4.0（介质到金属有效折射率）
  n_shell: 1.0-2.5（包层）
```

### evolution-agent 检查清单

当 evolution-agent step03 迭代此蓝图时，必须检查：

- [ ] 蓝图参数是否用 Annotated 声明了类型+范围+默认值？
- [ ] 是否支持单值和扫描列表两种模式？
- [ ] 是否有 scan_parameters 字段？
- [ ] 蓝图能否从本篇论文的参数泛化到同物理问题的完整参数空间？
- [ ] 如果不能扫参，为什么？（合理理由才接受）

### 参考蓝图路径
<如已有关联的 .magnus.blueprint.yaml，注明路径>

## 如无需蓝图

```
本次复现基于纯 Python 解析计算，未使用 COMSOL/Magnus。
无需创建蓝图。后续如有 COMSOL 扩展需求再议。
```

---

## 附录：复现流程全景图

```
<paper> Fig.<图号>
  ├─ step01-03: PDF 阅读 & 参数提取（纯人工/agent）
  ├─ step04-06: 理论实现 & 数值验证（Python 脚本）
  ├─ step07-08: （可选）COMSOL 验证 / Magnus 提交
  ├─ step09:    physical verifier 检验
  └─ step10-11: 4 类文档产出
       ├─ .result/<paper>/full_report.md
       ├─ .result/<paper>/brief.md
       ├─ toEflow/<paper>.skill-suggestion.md
       └─ toEflow/<paper>.blueprint-suggestion.md
```
