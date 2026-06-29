# 04-theory_and_implementation（子 agent 视角）

## 具体怎么干

### 推导
1. 从 Maxwell 方程出发，写完整推导到 $a_n, b_n$
2. **核心公式 $a_n, b_n$ 必须对着教材核**（Bohren & Huffman 或 Kerker）
3. review 论文（Akimov 等）只做交叉，不当主源
4. 推导笔记标公式来源页码

### 代码
1. 特殊函数用 `scipy.special`（spherical_jn, spherical_yn, lpmv 等），不自写
2. 单位 SI
3. 级数截断 $n_{\max} \approx x + 4x^{1/3} + 2$
4. 函数签名和 verifier 脚本期望一致

### 测试（TDD）
1. 物理约束测试值先写死（能量守恒容差 1e-10 等）
2. 代码迁就测试，不是测试迁就代码
3. 每个代码文件配一个 test 文件

### 预制脚本（scripts/）
- `mie_coefficients_template.py` — Mie 系数代码骨架
- `scattering_template.py` — 截面计算骨架
- `test_template.py` — 物理约束测试骨架

## 输出约定

- 推导：`.work/<case>/derivation.md`（含公式来源页码）
- 代码：`.work/<case>/code/*.py`
- 测试：`.work/<case>/tests/test_*.py`

## 常见坑

- $a_n, b_n$ 分子分母易搞反，AI 高频错——必须教材核
- 球贝塞尔 vs 普通贝塞尔别混
- $n$ 的阶数别漏
- 单位 nm/m 必须统一
- 复数运算用 numpy，别手算

## 决策问题重点回答

- 需不需要数值脚本 / magnus？本步要定清
- 核心公式来源是哪本教材第几页？
- 哪些用 scipy.special、哪些自写？
