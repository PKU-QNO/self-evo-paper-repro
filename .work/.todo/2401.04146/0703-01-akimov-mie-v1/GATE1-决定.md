# Gate1 决定记录 — 用户已裁决（2026-07-04）

> 对应 `GATE1-审核报告.md` 的决定 1/2/3。main-agent 恢复后以本文件为准放行 step03。

## 决定 1：step08 目标图 = 候选 A（Fig3）✅

- **目标图**：Akimov Fig3 — 超辐射（$a_l=1$，虚线）/ 非辐射（$a_l=0$，实线）态 loci，$(q_e,\ \varepsilon_i/\varepsilon_e)$ 实平面，$l=1,2,3$，TM+TE 共 6 面板。
- **理由**：零材料色散依赖（排除"色散源与作者不一致"混杂变量），解析求根难度最低，可用论文内自洽验证（$a_l=1 \Rightarrow \sigma_{sca,l}=\sigma^{sr}_{sca,l}=2(2l+1)/q_e^2 \cdot \pi R^2$）。
- 候选 C（Fig5(c)(f) $|a_1|,|b_1|$ 谱）留作本篇加做项或第二轮，本篇不阻塞主线。
- 标准 Lorenz-Mie 核（$a_l,b_l$+截面）+ 3 个 Layer1 verifier + benchmark 基础设施照常先建。

## 决定 2：Gate1 参数核对 ✅ 通过

- 通用核参数表（`parameter_table.md`）通过：$q_e=k_eR$ 记号、$m=\sqrt{\varepsilon_i/\varepsilon_e}$、Wiscombe 截断 $n_{max}\approx x+4x^{1/3}+2$（保持 trust 标注，非论文原文）、Riccati-Bessel 定义、eV↔nm 换算（例算 $q_e\approx0.55$ 核对无误）。
- **候选 A 参数**（本篇生效）：$q_e\in[0,10]$、$\varepsilon_i/\varepsilon_e\in[-10,15]$ 纯实、$l=1,2,3$、TM+TE。
- 材料源三条（Ag=Johnson&Christy 1972 / Si=Aspnes 1983 / SiO₂=Malitson 1965）本篇选 A 用不到，**不下载**；留作候选 C/B 启用时的默认认可源。

## 决定 3：公式主源口径 ✅ 确认

- **step04 以教材 Bohren & Huffman（`.paper/scattering.pdf`）标准式为主源实现**；Akimov 论文式（带显式 $q_i,q_e$ 因子，形式不同但等价）做交叉验证。
- **两式数值必须一致，不一致即 blocker**（停机报告，不硬跑）。
- Gate3 人工核公式时的核对对象 = BH 标准式。

## 决定 4：memento ✅ 已解除（MCP 已恢复，见审核报告）

---

**放行指令**：Gate1 通过，main-agent 按 `GATE1-审核报告.md` §四路线继续 step03（formalization spec 以 Fig3 为目标图）→ Gate2 停机。
