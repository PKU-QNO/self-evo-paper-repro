---
name: pdf
description: PDF processing for SEPR — text/formula/figure/table extraction, OCR for scanned PDFs, figure digitization. Use when the task involves reading or extracting content from PDF files (papers, textbooks), classifying data figures vs schematic figures, or digitizing paper figures for quantitative comparison.
---

# PDF Skill（空白，待后期英文 prompt-engineered）

> 现阶段是占位骨架。详细中文设计稿在 `.human/skills/` 对应位置（待建）。后期翻译成英文 prompt-engineered 版。
> 这个 skill 给 sub-agent 用，处理 PDF 提取（workflow step 01 pdf_preprocessing）。

## 职责（待填）

- PDF 文字提取（电子版优先 pymupdf）
- 公式提取/识别（pix2tex 或图片化保留）
- 图表分离（数据图 vs 示意图分类）
- 表格数值逐字保留
- 扫描版 OCR（ocrmypdf / pytesseract）
- 论文图数字化（为 step08 量化对比准备）

## 预制脚本（待填）

- `scripts/extract_pdf.py` — 提取文字+图片
- `scripts/classify_figures.py` — 数据图/示意图分类
- `scripts/extract_tables.py` — 表格数值提取
- `scripts/digitize_figure.py` — 论文图数字化

## 输出约定（待填）

- 正文 → `.work/<case>/paper_text.md`
- 公式 → `.work/<case>/formulas.md`
- 图 → `.work/<case>/figures.md` + `figs/`
- 表 → `.work/<case>/tables.md`

## 常见坑（待填）

- 两栏 PDF 文字流顺序乱
- 公式 OCR 不准的图片化保留
- 表格数值别四舍五入
- caption 跨页要合并
