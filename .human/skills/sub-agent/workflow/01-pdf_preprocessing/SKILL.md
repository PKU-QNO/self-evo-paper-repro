# 01-pdf_preprocessing（子 agent 视角）

## 具体怎么干

### 工具优先级
1. **电子版 PDF**：优先用 `pymupdf`（fitz）提取文字 + 图片
2. **扫描版 PDF**：用 `ocrmypdf` 先 OCR 再提取，或 `pytesseract`
3. **公式提取**：用 `pymupdf` 提取文字流，公式用 `pix2tex` 或 `latex_ocr` 识别，识别不准的图片化保留
4. **图表分离**：`pymupdf` 的 `page.get_images()` 提取图片，按位置判断是数据图还是示意图

### 预制脚本（scripts/）
- `extract_pdf.py` — 提取文字+图片到指定目录
- `classify_figures.py` — 辅助判断数据图/示意图（看有无坐标轴）
- `extract_tables.py` — 提取表格数值

### 处理顺序
1. 跑 `extract_pdf.py` 把 PDF 拆成 text + images
2. 手动/半自动分类图（数据图/示意图）
3. 公式识别，识别不准的标注"需人工核"
4. 表格数值逐字保留
5. 输出 4 个 Markdown + figs/

## 输出约定

- 正文：`.work/<case>/paper_text.md`
- 公式：`.work/<case>/formulas.md`（编号+原文+LaTeX+来源页码）
- 图：`.work/<case>/figures.md`（编号+caption+类型[数据图/示意图]+路径）
- 表：`.work/<case>/tables.md`（编号+caption+数值逐字）
- 图文件：`.work/<case>/figs/`

## 常见坑

- pymupdf 提取公式经常乱码，复杂公式图片化比强求 LaTeX 稳
- 两栏 PDF 文字流顺序会乱，要按位置重排
- 表格数值别四舍五入，逐字保留
- caption 有时跨页，要合并

## 不确定时

停下来在报告里写 blocked，不要瞎猜。
