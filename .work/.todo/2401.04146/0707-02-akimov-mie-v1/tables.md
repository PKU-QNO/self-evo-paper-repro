# 表清单 — Akimov 2401.04146（case 0707-02）

**结论：本论文无表格。**

- **核实方式**：对 LaTeX 源 `01-pdf_preprocessing/src/Text-rev.tex` 通读全文（664 行），未见 `\begin{table}`、`\begin{tabular}` 环境。所有定量信息以公式和图（Fig1–Fig12）形式呈现。
- **交叉核对**：与姊妹 case 0703-01 的 `tables.md`（该 case 用 grep 检索确认 0 命中）结论一致，本 case 独立通读确认。
- **含义**：本步不产出表格数值。Fig6 相关的所有数值信息（坐标轴范围、$l$ 取值、TM/TE 划分）见 `figures.md`；公式见 `formulas.md`。

> 占位文件，保持 4 产物清单（paper_text.md / formulas.md / figures.md / tables.md）完整。

## provenance
- source_artifact: arXiv 2401.04146 LaTeX 源 `Text-rev.tex`（本 case 独立通读核实）
- evidence_type: 全文人工核对（非仅 grep）
- timestamp_version: 20260709
- scope_applicability: 全篇论文无表格
- confidence_result_class: 高 / pipeline_completed
