# 03-reproduction_design（子 agent 视角）

## 具体怎么干

### 写 formalization spec
按 `formalization.yaml` 模板填：
- geometry：几何形状、坐标、尺寸
- materials：材料+色散模型+复折射率
- equations：Maxwell+展开方式
- boundary_conditions：切向/法向连续
- sources：入射波类型
- solver：解析/半解析/数值
- observables：对应论文图的物理量
- assumptions：假设
- missing_fields：缺什么写什么，不空着

### 拆分计划
- 从最小可执行单元开始（单球→核壳→阵列）
- 标依赖关系（哪步依赖哪步）
- 每步标检验标准

### 决策问题重点回答
- **需不需要数值计算脚本？** 纯解析能算就别上数值
- **需不需要 magnus 云计算？** 本地 Python 跑得动就本地，小时级才上 magnus

### 预制脚本（scripts/）
- `formalization_template.py` — 生成 formalization.yaml 骨架

## 输出约定

- spec：`.work/.todo/{paper}/{case}/formalization.yaml`
- 拆分计划：`.work/.todo/{paper}/{case}/repro_plan.md`

## 常见坑

- observables 要对应论文图实际物理量，别写成泛泛的"散射截面"
- solver 要具体（Mie 级数 / CDA / FEM），别写"数值方法"
- missing_fields 不丢人，空着才危险

## 人工 gate ②

这步末停下来，让用户核对 spec 是否匹配论文物理问题。
