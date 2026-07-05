# 08-result_analysis（子 agent 视角）

## 具体怎么干

### 量化对比（不靠肉眼）
1. 数字化论文图（如 step 07 没做）
2. 算 RMSE（曲线整体）
3. 算共振峰位误差（nm）
4. 算 Q 值相对误差
5. 算峰幅值相对误差

### 差异归因
- 参数差异（论文没给全/你猜的）
- 模型差异（你简化了什么）
- 数值精度（级数截断/网格）
- 论文图数字化误差

### 物理结论
- 基于数值，不是复述论文
- 写清楚观察到的物理现象（如三区过渡、多极出现顺序）

### 预制脚本（scripts/）
- `compute_rmse.py` — 算曲线 RMSE
- `find_peaks.py` — 找共振峰位
- `plot_comparison.py` — 三方叠加图

## 输出约定

- 分析报告：`.work/.todo/{paper}/{case}/result_analysis.md`（RMSE+峰位误差+归因+结论）
- 对比图：`.work/.todo/{paper}/{case}/figs/comparison_*.png`

## 常见坑

- 别说"基本一致"，给数字
- 差异要归因，不能只说"有差异"
- 容差是用户定的，你只报数字

## 人工 gate ④

这步末停下来，让用户看量化误差数字决定 pass/fail。你报告里把数字列清楚，别让用户自己算。
