# icpcBoard

icpcBoard 是按 Markdown 章节维护的 ICPC 中文算法手册。内容放在 `content/`；HTML 模板、打印样式和构建配置彼此独立，同一份源文件可生成 Markdown、HTML 和 PDF。

## 构建

需要 Python 3.10 或更新版本、Chrome/Chromium，以及 Poppler 提供的 `pdfinfo` 和 `pdftotext`。字体建议使用 Noto Serif CJK SC（正文）、Noto Sans CJK SC（标题）和 Maple Mono NF CN（代码）。CSS 已设置通用回退字体；缺少推荐字体时仍可构建，但排版可能略有差异。

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make validate
make all
```

`make markdown`、`make html`、`make pdf` 可分别构建 Markdown、HTML 和 PDF；`make all` 一次生成三种格式：`output/markdown/icpcBoard.md`、内嵌样式的独立 HTML `output/html/icpcBoard.html` 和 A4 PDF `output/pdf/icpcBoard.pdf`。PDF 采用黑白单栏排版，含可点击目录和页码。代码使用 9 pt Maple Mono NF CN 字体，保留缩进，过长代码可以自然换页。

若浏览器程序不在 `PATH` 中，可在 `config/build.json` 设置 `chrome_bin`。版式编辑 `styles/icpcBoard.css`，文档结构编辑 `templates/document.html`，源文件顺序和输出路径编辑 `config/build.json`。

## 内容格式

章节文件放在 `content/chapters/`，使用带零填充数字前缀的文件名（如 `01-...md`、`02-...md`），构建时按文件名排序。每章必须有且仅有一个一级标题 `#`。使用 `##` 作为小节标题、`cpp` 围栏代码块、标准 Markdown 表格，以及 `$...$` / `$$...$$` TeX 数学公式。前言和关键词索引在 `config/build.json` 中单独列出，不纳入章节通配符。

`make validate` 检查章节结构、围栏代码、显式标题 ID 和配置输入，不生成交付文件。也可直接运行 `python scripts/build.py --format markdown|html|pdf|all`，按需使用各导出层。`make clean` 清除构建产物。

## 项目结构

```text
config/build.json             源文件顺序、标题与输出路径
content/frontmatter.md       前言
content/chapters/01–09        九个编号章节
content/10-keyword-index.md   题意关键词索引
scripts/build.py             Markdown、HTML、PDF 构建器
styles/icpcBoard.css          屏幕与 A4 打印样式
templates/document.html      独立 HTML 框架
tests/                        代码块检查与定向回归检查
docs/                         构建说明与内容覆盖表
output/                       本地生成结果与保留的样例
```

## 代码检查

在安装了 `g++` 的环境中运行：

```sh
python3 tests/check_foundations.py
python3 tests/check_algorithms.py
```

`check_foundations.py` 独立编译第 01–04 章的所有 C++17 围栏代码块，只做语法检查。`check_algorithms.py` 检查第 05–09 章代码块，并运行 Bellman–Ford、线段树、Dinic、最小费用流、区间赋值线段树、后缀数组和圆几何的定向回归样例。

第 01–04 章与第 05–09 章的来源和覆盖说明见 [docs/coverage-01-04.md](docs/coverage-01-04.md) 与 [docs/coverage-05-09.md](docs/coverage-05-09.md)。

## 原有样例

仓库初始样例保留在 `output/source/` 与 `output/pdf/icpc-sample.pdf`，作为参考文件，不会被新手册构建覆盖。
