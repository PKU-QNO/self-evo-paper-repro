# 06-run_and_monitor（子 agent 视角）

## 具体怎么干

### 本地跑
1. 先跑最小 smoke case（1-2 个参数值）确认能跑
2. 再跑完整扫描
3. 记录命令、耗时、输出

### magnus 云跑（step 04 决定要才走）
1. 查现有 job（`run_id`），有 active/success 就复用
2. 查集群资源，CPU/内存不过半
3. 保守提交（gpu_type=cpu, gpu_count=0 除非明确要 GPU）
4. 短轮询 smoke，长轮询真实 sweep

### 监视
- 数值异常（NaN/Inf/负截面）立即停
- 保留日志，不覆盖
- 初步看形状对不对（峰在该出现的位置吗）

### 预制脚本（scripts/）
- `run_smoke.py` — 跑最小 case 的 wrapper
- `run_sweep.py` — 跑参数扫描的 wrapper
- `submit_magnus.py` — magnus 提交模板（参考 optics-magnus-platform）

## 输出约定

- 日志：`.work/<case>/run_log.md`
- 数据：`.work/<case>/data/*.csv`
- 初步图：`.work/<case>/figs/*.png`

## 常见坑

- 别上来就跑完整扫描，先 smoke
- NaN 经常是级数截断不够或除零
- magnus job 别重复提交，先查
- 日志别覆盖，追加或加时间戳

## 决策问题重点回答

- 跑成功了吗？有无异常值？
- 初步形状对吗？
- 要不要换 magnus？
