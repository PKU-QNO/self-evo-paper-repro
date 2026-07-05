# Gate4 决定记录 — 用户已裁决（2026-07-05，optics_agent CC 独立审计）

> 对应 main-agent step08 末 Gate4（Fig3 复现最终误差核对）。裁决 = **选项 1 接受判通过，附强制条件**。
> main-agent 恢复后以本文件为准：result_class=partial_physical_match，进 step09-11 收尾。

## 裁决：选项 1（接受），附 3 强制条件；否决选项 2，不选选项 3

## optics_agent CC 独立审计（决定性证据，非信 main/sub 转述）

**独立求根 Δ=0.0000（本裁决的硬依据）**：CC 用 Gate3 已独立验证过的 `scattering.py`（`mie_ab`），**完全绕开 SEPR 的 `fig3_loci.py`**，重新求 sr locus 的根（brentq on Im coeff=0, Re>0.5）。与 SEPR CSV 逐点对比：
- TM l=1 @ q_e=1/4/7：所有根 Δ=0.0000（含 5-9 支/切片）
- TM l=2 @ q_e=1/4/7：所有根 Δ=0.0000
- TE l=2 @ q_e=4/7：所有根 Δ=0.0000
→ **SEPR 求根与复现曲线数学上完全正确，无画错位。** 这是"长尾≠复现错"最硬的证据，比 main 的自洽性论证更强（main 未做此独立交叉检验）。

**归因证实**：既然复现曲线经独立求根证实正确，数字化点偏离它就只能是读图误差。nr 六面板全达标（median 0.005-0.007）佐证复现无整体偏移。

## 3 条强制条件（报告/capsule/benchmark 必须体现）

1. **result_class = `partial_physical_match`**（CLAUDE.md 红线封顶，本次不声明 physical_reproduction_success——需所有量化无条件全过）。
2. **诚实边界如实写明**（不得只写"长尾读图误差"这种半真陈述）：
   - 接受依据 = 独立求根 Δ=0 证实复现曲线正确 + 超标归因数字化读图。
   - **TM 三面板 sr 中位数也略超阈**（0.011-0.012 > 0.01），非仅 p95 长尾；TE 三面板才是"中位达标、仅长尾超"。
   - 超阈点集中在**正大 ε（≈上边界 14.6）+ 中大 q_e 密集分支区**——**纠正 main 转述**：main 曾说"负 ε 陡共振区"，与实际诊断数据（sr_tail_diagnosis.txt: eps 常接近上边界 14.6）**说反了**。
   - **方向性检验（数字化偏差单/双侧分布）未完成**（CC 起了逐点求根检验但太慢中止；独立求根 Δ=0 已决定性，方向性仅补强）——记入 capsule"什么没做透"。
3. **不改阈值（否决选项 2）**：loci 图无社区先例，SEPR 自定 median<0.01/p95<0.03 保持不动。为过而放宽 p95 = 外部审查警告的 verifier gaming；这次"未达标但经独立复算接受"的记录比放宽阈值诚实，留作后续论文校准基线。benchmark.yaml 标 sr 阈值超标为 known/accepted（带本 Gate4 依据链接）。

## 为什么不选 3（sr 陡区加密重测）
独立求根已证复现对，再加密取点只是把读图误差摊薄、大概率同结论；多花一轮边际收益低。首篇目的（跑通框架+暴露问题）已达成。若用户要"教科书级干净首篇"或补方向性检验可选 3，CC 判断不值。

## 放行
result_class=partial_physical_match，进 step09（可复现性自检）→ step10（双报告+benchmark+skill 草稿→toEflow）→ step11（run_manifest + capsule + 按新规范增量更新 `WORK_LOG/01-akimov-mie-v1.md`）。全程 result_class 用 partial_physical_match。**这是本次复现最后一个 human gate**（step11 后进 .result 前会再确认一次哪些产物入库）。
