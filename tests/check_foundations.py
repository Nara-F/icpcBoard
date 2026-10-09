#!/usr/bin/env python3
"""Compile every C++17 fenced example in chapters 01–04 independently."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    ROOT / "content/chapters/01-contest-practice.md",
    ROOT / "content/chapters/02-cpp-stl.md",
    ROOT / "content/chapters/03-basic-search.md",
    ROOT / "content/chapters/04-dynamic-programming.md",
]


def main() -> int:
    compiler = shutil.which("g++")
    if compiler is None:
        print("g++ is required for the C++17 snippet check", file=sys.stderr)
        return 2

    failures: list[str] = []
    total = 0
    with tempfile.TemporaryDirectory(prefix="icpcboard-foundations-") as temp_name:
        temp = Path(temp_name)
        for chapter in CHAPTERS:
            text = chapter.read_text(encoding="utf-8")
            blocks = re.findall(r"```cpp\s*\n(.*?)\n```", text, re.DOTALL)
            chapter_passes = 0
            for index, code in enumerate(blocks, start=1):
                source = temp / f"{chapter.stem}-{index}.cpp"
                source.write_text(code + "\n", encoding="utf-8")
                result = subprocess.run(
                    [compiler, "-std=c++17", "-fsyntax-only", str(source)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                total += 1
                if result.returncode == 0:
                    chapter_passes += 1
                else:
                    failures.append(
                        f"{chapter.relative_to(ROOT)} block {index}:\n"
                        f"{result.stderr.strip()}"
                    )
            print(f"{chapter.relative_to(ROOT)}: {chapter_passes}/{len(blocks)} passed")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"All {total} C++17 snippets passed syntax checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
