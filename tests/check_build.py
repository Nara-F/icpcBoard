#!/usr/bin/env python3
"""Integration checks for the independent typesetting/export pipeline."""
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import render, validate_html, validate_pdf_bounds
from typst_pdf import build_typst, compile_pdf


class CodeLines(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.current = ""
        self.lines = []

    def handle_starttag(self, tag, attrs):
        if self.depth:
            self.depth += 1
        elif dict(attrs).get("class") == "code-text":
            self.depth = 1
            self.current = ""

    def handle_data(self, data):
        if self.depth:
            self.current += data

    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1
            if not self.depth:
                self.lines.append(self.current)


class BuildChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / "tmp").mkdir(exist_ok=True)
        cls.work = tempfile.TemporaryDirectory(dir=ROOT / "tmp")
        cls.directory = Path(cls.work.name)
        cls.cfg = json.loads((ROOT / "config/build.json").read_text())
        cls.cfg["typst"] = str(cls.directory / "fixture.typ")
        cls.code = '\n'.join([
            '// 保留中文、缩进、空行和字面量，长代码需要跨页。',
            'const char* value = "$n^22^n$ & <tag> </span>";',
            '',
            '/* a multiline',
            '   comment */',
        ] + [f'    int value_{i} = {i}; // 第 {i} 行' for i in range(150)])
        cls.source = (
            '# 1. 构建检查\n\n## 1.1 锚点\n\n'
            '公式 $n^22^n$ 与行内 `x_y`。\n\n$$n^22^n$$\n\n'
            '[旧锚点](#11) / [显式锚点](#explicit-target)\n\n'
            '```cpp\n' + cls.code + '\n```\n\n'
            '## 1.2 表格 {#explicit-target}\n\n'
            '| REPEATED_HEADER | 跳转 | 公式 |\n|---|---|---|\n' +
            ''.join(f'| 第 {i} 行 | [返回](#11) | $n^22^n$ |\n' for i in range(110))
        )
        cls.typ, cls.toc, cls.ast = build_typst(ROOT, cls.cfg, cls.source)
        cls.pdf = cls.directory / "fixture.pdf"
        cls.pages = compile_pdf(ROOT, cls.cfg, cls.typ, cls.pdf, cls.toc, cls.ast)
        cls.text = subprocess.check_output(["pdftotext", "-layout", str(cls.pdf), "-"], text=True)

    @classmethod
    def tearDownClass(cls):
        cls.work.cleanup()

    def test_links_code_and_pagination(self):
        # compile_pdf already compares every rendered code block and heading ID.
        self.assertEqual(set(self.pages), {"1", "11", "explicit-target"})
        self.assertGreater(self.pages["explicit-target"], self.pages["11"])
        self.assertIn("value_149", self.text)
        self.assertIn("第 109 行", self.text)
        validate_pdf_bounds(self.pdf, len(self.text.rstrip("\n").split("\f")) - 1)

    def test_math_and_repeated_headers(self):
        generated = self.typ.read_text()
        self.assertIn("$n^2 2^n$", generated)
        self.assertNotIn("n^(22^n)", generated)
        # One source header is repeated on at least two physical pages.
        self.assertGreaterEqual(self.text.count("REPEATED_HEADER"), 2)

    def test_html_preserves_code_without_line_number_text(self):
        page = render(self.source, "fixture", "", "zh-CN", "",
                      ROOT / "templates/document.html", toc_pages=self.pages)
        validate_html(page, self.source)
        parser = CodeLines()
        parser.feed(page)
        self.assertEqual("\n".join(parser.lines), self.code)


if __name__ == "__main__":
    unittest.main()
