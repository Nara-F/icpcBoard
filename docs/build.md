# 构建与导出

安装 `requirements.txt` 中的 Python 依赖，并确保 Chrome/Chromium 与 Poppler 的 `pdfinfo`、`pdftotext` 命令可用。运行 `make validate` 检查源文件。使用 `make markdown`、`make html`、`make pdf` 单独导出所需格式；`make all` 一次导出全部格式。

`config/build.json` 管理补充文件、章节输入和输出路径。章节按文件名排序，请使用数字前缀。`python scripts/build.py --validate-only` 只检查源文件；`python scripts/build.py --format markdown` 只组装 Markdown；`--format html` 生成 Markdown 和 HTML；`--format pdf` 执行完整 PDF 导出。HTML 会内嵌样式，可作为独立文件分发。PDF 从该 HTML 由无头 Chrome 导出，并检查 A4 页面尺寸、章节文本和页数。

正文使用 Noto Serif CJK SC，标题使用 Noto Sans CJK SC，代码优先 Maple Mono NF CN。缺少字体时 CSS 会回退到系统字体。数学公式由本地 `latex2mathml` 转成 MathML，不需要联网服务。
