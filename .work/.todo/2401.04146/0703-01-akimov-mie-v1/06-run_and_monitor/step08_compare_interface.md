# step08 量化对比接口说明（Akimov Fig3 Layer3）

> 来源：step06 T4（复现执行者 W-sub）| case: 0703-01-akimov-mie-v1 | timestamp: 20260705-01
> 用途：为 step08 正式 Layer3 量化对比准备指标定义、归一化、阈值、数据路径与脚本签名。
> **本步（T4）只准备，不算最终指标**。最终 Layer3 指标由 step08 执行、Gate4 人审裁决。

---

## 一、指标定义

**主指标：数字化取样点到复现曲线族的最近归一化距离。**

对每个数字化取样点 $p=(q_e^{(p)},\varepsilon^{(p)})$（来自原图 Fig3），在**同一面板、同一类型**（sr↔sr、nr↔nr）的复现曲线族点集里找最近点，取归一化欧氏距离：

$$ d(p) = \min_{c \in \text{repro}(\text{panel},\text{type})} \sqrt{\left(\frac{q_e^{(p)}-q_e^{(c)}}{10}\right)^2 + \left(\frac{\varepsilon^{(p)}-\varepsilon^{(c)}}{25}\right)^2} $$

- 归一化：$q_e$ 方向除以轴跨度 10，$\varepsilon$ 方向除以轴跨度 25（$[-10,15]$），使两轴等权、$d$ 无量纲、可跨面板聚合。
- 方向：数字化点 → 复现曲线（复现曲线是"真值"参照，密采样机器精度根；数字化点带主观误差）。
- 复现曲线族点集：直接用 T3 六 CSV 的全部 $(q_e,\varepsilon)$ 行（每面板每类型上万点，密到可当连续曲线的最近邻查询）。

**辅助判据（Gate2 强制，已在 T4 完成并 PASS）：曲线支数逐面板一致。**
切片法 vs 二维 contour 独立法逐面板支数已核对一致（TM 12/12,12/12,11/11；TE 12/12,11/11,11/11），contour 点被切片法覆盖 >99.8%，无系统性漏根。见 `completeness_check.txt`。step08 不需重算，引用即可。

---

## 二、建议阈值（SEPR 自定，非社区标准）

> **重要标注**：loci 图（曲线族位置对比）**无文献先例 RMSE/距离阈值**。以下为 SEPR 本 case 自定，量级取"数字化误差 + 轴范围百分比"，**非社区公认标准**。最终由 Gate4 用户认可后生效，不得自行放宽。

| 指标 | 建议阈值 | 依据 |
|------|---------|------|
| 归一化距离 **中位数** | $< 0.01$ | 约轴范围 1%，与数字化不确定度同量级 |
| 归一化距离 **95 分位** | $< 0.03$ | 容忍密集区/端点少量大偏差 |
| 曲线支数逐面板一致 | 已 PASS（T4） | Gate2 强制附加判据，防漏根 |

数字化不确定度量级（见 T4 报告）：$dq_e \sim 0.05$、$d\varepsilon \sim 0.15$，归一化后 $\sim 0.005$–$0.006$，与中位阈值 0.01 同量级——即阈值本质是"数字化误差 + 复现残差应共处同一量级"。

---

## 三、数据路径

| 角色 | 路径 | 格式 |
|------|------|------|
| 复现曲线族（真值参照） | `reproduction_test/mie/data/fig3_loci_{TM,TE}_l{1,2,3}.csv` | 列 `q_e,eps_ratio,branch_id,type,residual`；`type∈{sr,nr}`；`branch_id=0` 为 eps=1 平凡 nr 线 |
| 数字化取样点（待评估） | `reproduction_test/mie/data/fig3_digitized.csv` | 列 `panel,l,pol,type,q_e,eps_ratio`；`type∈{sr,nr}`，`pol∈{TM,TE}` |
| 完备性判据结果 | `.work/.todo/2401.04146/0703-01-akimov-mie-v1/06-run_and_monitor/completeness_check.txt` | 逐面板支数/覆盖，已 PASS |
| 目测叠图 | `reproduction_test/mie/figures/fig3_overlay.png` | 供人审对照 |

**面板对齐键**：数字化侧 `(pol,l)`，复现侧文件名 `fig3_loci_{pol}_l{l}.csv`，一一对应。类型键 `type`（sr/nr）两侧一致。

---

## 四、建议脚本签名（step08 可直接实现）

```python
# reproduction_test/mie/code/fig3_compare.py  (step08 新建, 非本步产物)

def load_repro_curve(pol: str, l: int, typ: str) -> np.ndarray:
    """读 fig3_loci_{pol}_l{l}.csv, 过滤 type==typ, 返回 (N,2) 数组 [q_e, eps].
    注意: nr 含 branch_id=0 平凡线, 是否纳入对比由 step08 决定
    (原图 eps=1 有该实线, 建议纳入)."""

def load_digitized(pol: str, l: int, typ: str) -> np.ndarray:
    """读 fig3_digitized.csv, 过滤 (pol,l,type), 返回 (M,2) 数组 [q_e, eps]."""

def nearest_norm_dist(dig_pts: np.ndarray, repro_pts: np.ndarray,
                      qe_span: float = 10.0, eps_span: float = 25.0) -> np.ndarray:
    """对每个 dig 点算到 repro 点集的最近归一化距离, 返回 (M,) 距离数组.
    归一化: dq/qe_span, deps/eps_span. 可用 scipy.spatial.cKDTree 加速."""

def panel_metrics(pol: str, l: int) -> dict:
    """对一个面板算 sr/nr 的 {median, p95, max, n} 归一化距离统计."""

def layer3_verdict(threshold_median=0.01, threshold_p95=0.03) -> dict:
    """聚合六面板 sr+nr, 判 median<阈值 且 p95<阈值; 结合完备性(已PASS)出 Layer3 PASS/FAIL.
    返回逐面板 + 全局统计 + verdict. 不自行声明 physical_reproduction_success
    (需 Gate4 人审)."""
```

**实现要点**：
- 用 `scipy.spatial.cKDTree`（对归一化后的 repro 点集建树，query 数字化点）避免 O(N·M) 暴力。
- 复现点集先归一化（$q/10,\varepsilon/25$）再建树，查询点同样归一化。
- nr 的 eps=1 平凡线（branch_id=0）建议纳入（原图确有该蓝实线）。
- 逐面板 + 全局两级统计；输出结构化 dict，Gate4 呈现。

---

## 五、result_class 与边界

- 本接口文件（T4）：`simulation_completed`（仿真数据 + 数字化数据备齐，未算最终 Layer3 指标）。
- step08 跑完指标后：若 Layer3 距离达标 + 完备性 PASS → 最高 `partial_physical_match`；`physical_reproduction_success` 还需 Gate4 人审。
- 阈值 SEPR 自定、无社区先例——step08 报告须显式标注，Gate4 呈现事项。
