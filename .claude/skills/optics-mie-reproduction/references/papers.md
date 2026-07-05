# Mie Reproduction Papers（课程表 + 学习目标；不含论文内容断言）

11 papers, executed in 7 stages by increasing difficulty. Each stage has one main paper plus optional references. Non-arXiv PDFs are in `papers/mie/`; arXiv papers are accessible directly.

## ⚠ 本文件契约（2026-07-04 修订，首跑教训）

本文件只承载两类信息，**不承载第三类**：

1. **课程表层（可信）**：论文属于哪个 Stage、为什么选它、PDF 在哪、难度排序、来源可信度提醒。这是人工制定的教学计划。
2. **学习目标层（可信，但它是"我们要产出什么"）**：每条 `Deliverables` 是**我们这个 Stage 想写出的代码/曲线/验证**，**不是**"论文里有这张图"的断言。我们的交付曲线可能在论文里根本没有对应图——那不影响交付，但不能拿它当复现比对目标。
3. **论文内容断言（本文件不提供）**：论文里实际有哪些图、哪些曲线、哪些可比对的定量目标，**一律由 W-flow step02（paper_reading）对论文原文/LaTeX 源提取，产出 `figures.md`，过 gate① 人工核对后才生效**。本文件中任何看似描述论文内容的句子都只是**未核实线索（unverified hint）**，与 step02 产出冲突时**以 step02 为准**。

**为什么有这条契约**：2026-07-03 首跑 Akimov 时，本文件旧版断言该论文含 "$Q_{sca}(x)$ curve, Rayleigh→Mie→geometric transition"——step02 逐图核对证实**论文 12 张图里没有这条曲线**，整个"复现哪张图"的预设目标是虚构的（declared-vs-actual，写描述的人没读过原文）。sub-agent 盲信此类描述会跑偏。故所有内容断言已从本文件移除或降级为线索。

---

## Stage 1 — Single-sphere Mie basics

### Akimov — Mie scattering theory: a review (arXiv 2401.04146, 2024)

**选篇理由**：单球 Lorenz-Mie 的系统 review，覆盖多极展开系数的物理来源，适合作第一阶段的公式主线索引。**注意它是 review，不是有原创数据图的研究论文——可比对的目标图偏理论 loci / 系数谱类**（此点已由 2026-07-03 首跑 step02 证实）。

- **Deliverables（我们的交付，非论文图）**: `code/mie_coefficients.py`（$a_n, b_n$）、`code/scattering.py`（cross sections）、$Q_{sca}(x)$ curve for $n=1.5,2,3,4$（教学用基线曲线，**论文中无此图**）、multipole decomposition。
- **Verification**: energy conservation, Rayleigh $x^4$, large-size $Q\to2$。
- **复现目标图**：由 step02 的 `figures.md` 确定（2026-07-03 首跑已产出：`.work/.todo/2401.04146/0703-01-akimov-mie-v1/figures.md`；候选为 Fig3 超辐射/非辐射 loci、Fig5(c)(f) $|a_1|,|b_1|$ 谱、Fig6 超吸收 loci）。
- **Caveat**: Akimov is a review and may have typos; verify $a_n,b_n$ against Bohren & Huffman or Kerker, use Akimov only as cross-check。教材 `.paper/scattering.pdf` 是公式主源。

## Stage 2 — Metal sphere LSPR

### Colas des Francs — Mie plasmons: modes volumes, quality factors and coupling strengths (arXiv 1112.2814, 2011)

**选篇理由**：金属纳米球 LSPR 的 Mie 展开，含模式体积/品质因子/Purcell 因子的闭式表达，适合引入 Drude 色散。（内容细节属未核实线索，step02 核。）

- **Deliverables**: `code/drude.py`（Au/Ag Drude）、`code/lspr.py`、LSPR wavelength vs radius（$R=10,20,50,100$ nm）、Purcell factor spectrum。
- **Verification**: quasi-static LSPR $\mathrm{Re}(\varepsilon)=-2\varepsilon_d$。
- **Physics（学习点）**: quasi-static（$a_1$-dominated）与 full Mie expansion 的差异。
- **复现目标图**：step02 产出后定。

## Stage 3 — Dielectric sphere Mie modes

### Main paper: to be supplemented via Web of Science

References: García-Etxarri et al. (2011); Kuznetsov et al. "Magnetic light" (Sci. Rep. 2012); Evlyukhin et al. "Demonstration of Magnetic Dipole Resonances of Dielectric Nanospheres" (Nano Lett. 2012); Kuznetsov et al. "Optically resonant dielectric nanostructures" (Science 2016).

**选篇理由**：高折射率介质球通过内部位移电流支持更丰富的 Mie 模式（磁/电偶极、四极），损耗低于等离激元结构——与 Stage 2 形成对照。

- **Deliverables**: dielectric sphere extinction spectrum、multipole decomposition、magnetic dipole mode visualization。
- **Physics（学习点）**: 内部环流位移电流产生磁偶极；共振由 size parameter 和折射率决定；电/磁偶极比决定 Kerker 条件。
- **复现目标图**：主论文定稿后由 step02 产出。

## Stage 4 — Core-shell Mie

### Tam — Mesoscopic nanoshells (JCP 127, 2007) — `papers/mie/204703_1_online.pdf`

**选篇理由**：两层 Lorenz-Mie 的 core-shell 消光计算；引入两层边界条件的递推。（"quasi-static 在厚/薄壳都失效、需全级数"属未核实线索，step02 核。）

- **Deliverables**: `code/core_shell_mie.py`、extinction spectra vs shell thickness、shell-thickness–resonance-wavelength map、quasi-static vs full Mie comparison。
- **Verification**: shell-thickness→∞ collapses to single sphere (core material); core→0 collapses to single sphere (shell material)。
- **Reference**: Arruda, "Toroidal dipole in core-shell spheres" (arXiv 2406.06800)。
- **复现目标图**：step02 产出后定。

## Stage 5 — Periodic array collective resonance (SLR)

### Auguie & Barnes — Collective Resonances in Gold Nanoparticle Arrays (PRL 101, 2008) — `papers/mie/PhysRevLett.101.143902.pdf`

**选篇理由**：周期阵列中 Rayleigh anomaly 与 LSPR 耦合产生高 Q 表面晶格共振（SLR），是从单球到周期系统的过渡。（线宽由周期决定等细节属未核实线索。）

- **Deliverables**: `code/coupled_dipole.py`（CDA）、extinction spectra vs period（标注 Rayleigh anomaly 与 SLR）、linewidth-vs-period curve。
- **Verification**: Rayleigh anomaly $\lambda=P\cdot n_{\text{eff}}$; large period collapses to single sphere。
- **Reference**: Gerasimov, "Plasmonic lattice Kerker effect" (arXiv 2007.13317)。
- **复现目标图**：step02 产出后定。

## Stage 6 — Binary array geometric resonance

### Li J et al. — Tuning of narrow geometric resonances in Ag/Au binary nanoparticle arrays (Opt. Express 18, 2010) — `papers/mie/Li_J_OE2010.pdf` or `papers/mie/oe-18-17-17684.pdf`

**选篇理由**：两种材料/尺寸的二元阵列，通过尺寸比独立调谐几何共振位置与线宽——CDA 引入两种单粒子极化率。（细节属未核实线索。）

- **Deliverables**: `code/binary_cda.py`、extinction spectra vs size ratio、linewidth-vs-size-ratio curve。
- **Verification**: large period collapses to single-particle result。
- **复现目标图**：step02 产出后定。

## Stage 7 — Effective refractive index and phase diagram

### Rybin — Phase diagram for the transition from photonic crystals to dielectric metamaterials (Nat. Commun. 6, 2015) — `papers/mie/Rybin_NatComm2015.pdf`

**选篇理由**：比较 Mie 共振波长与 Bragg 共振波长，在介电常数–填充率平面构建光子晶体/超材料相图——把阵列散射响应浓缩为有效光学参数。（细节属未核实线索。）

- **Deliverables**: `code/effective_medium.py`（S-parameter retrieval of $\varepsilon_{\text{eff}}, \mu_{\text{eff}}$）、`code/phase_diagram.py`、$n_{\text{eff}}$ dispersion、$(\varepsilon, P/\lambda)$ phase diagram。
- **Verification**: low filling fraction → Maxwell-Garnett。
- **复现目标图**：step02 产出后定。

## Optional Papers (clear attachment points)

| Paper | arXiv | 选篇理由（线索级） | Attachment |
|---|---|---|---|
| Tagviashvili | 0910.3305 | ENZ-limit Mie scattering | effective medium $n_{\text{eff}}\to0$ |
| Shamkhi | 1808.10708 | generalized Kerker transverse scattering | array angular scattering |
| Arruda | 2406.06800 | core-shell toroidal dipole | core-shell extension |
| Nieto-Vesperinas | 1201.6146 | Si sphere Kerker condition | single-sphere directional scattering |

## Execution Order Summary

Stage 1 (single sphere) → Stage 2 (metal LSPR) → Stage 3 (dielectric modes) → Stage 4 (core-shell) → Stage 5 (SLR) → Stage 6 (binary array) → Stage 7 (effective medium). Optional papers attach to their stated stages. Do not skip ahead — each stage's verifier depends on the previous stage's implementation being correct.

**每个 Stage 开跑时的第一步都是 step01/02 对论文原文提取图清单并过 gate①，本文件不预设任何一张目标图。**
