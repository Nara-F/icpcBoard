#!/usr/bin/env python3
"""Compile every C++17 fenced example in chapters 01–04 independently."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import contextlib
import io
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    ROOT / "content/chapters/01-contest-practice.md",
    ROOT / "content/chapters/02-cpp-stl.md",
    ROOT / "content/chapters/03-basic-search.md",
    ROOT / "content/chapters/04-dynamic-programming.md",
]


def compile_cpp(compiler: str, source_text: str, directory: Path, name: str) -> Path:
    source = directory / f"{name}.cpp"
    executable = directory / name
    source.write_text(source_text + "\n", encoding="utf-8")
    result = subprocess.run(
        [compiler, "-std=c++17", "-O0", str(source), "-o", str(executable)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"could not compile smoke fixture {name}:\n{result.stderr}")
    return executable


def smoke_python_harness(compiler: str, temp: Path) -> None:
    """Exercise the documented stress script on pass, WA, exit, and timeout paths."""
    chapter = (ROOT / "content/chapters/01-contest-practice.md").read_text(encoding="utf-8")
    section = chapter.split("## 1.14 Python 调试与随机对拍", 1)[1]
    blocks = re.findall(r"```python\s*\n(.*?)\n```", section, re.DOTALL)
    if not blocks:
        raise RuntimeError("chapter 1.14 has no runnable Python stress example")
    namespace: dict[str, object] = {"__name__": "foundation_smoke"}
    exec(compile(blocks[0], "chapter-01-14-stress.py", "exec"), namespace)
    stress = namespace["stress"]

    fixture = r'''#include <bits/stdc++.h>
using namespace std;
int main(int argc, char** argv) {
    string mode = argv[0];
    if (mode.find("nonzero") != string::npos) return 7;
    if (mode.find("slow") != string::npos) this_thread::sleep_for(chrono::milliseconds(1500));
    int n; if (!(cin >> n)) return 2;
    if (mode.find("wrong") != string::npos) { cout << 999999; return 0; }
    long long best = LLONG_MIN, current = 0;
    for (int i = 0; i < n; ++i) {
        long long x; cin >> x;
        current = max(x, current + x);
        best = max(best, current);
    }
    cout << best << '\n';
}'''
    binary = compile_cpp(compiler, fixture, temp, "stress-fixture")
    programs = {}
    for mode in ("correct", "wrong", "nonzero", "slow"):
        path = temp / mode
        shutil.copy2(binary, path)
        programs[mode] = str(path)

    correct_dir = temp / "case-correct"
    correct_dir.mkdir()
    original_cwd = Path.cwd()
    try:
        os.chdir(correct_dir)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            ok = stress(programs["correct"], seed=20261009, rounds=20)
    finally:
        os.chdir(original_cwd)
    if not ok or "PASS" not in output.getvalue():
        raise RuntimeError(f"stress success path failed: {output.getvalue()}")

    # Isolate the harness' documented failed.in/failed.txt outputs by case.
    for mode, needle in (("wrong", "actual="), ("nonzero", "return code 7"), ("slow", "timeout")):
        case_dir = temp / f"case-{mode}"
        case_dir.mkdir()
        original_cwd = Path.cwd()
        try:
            os.chdir(case_dir)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                ok = stress(programs[mode], seed=20261009, rounds=1)
        finally:
            os.chdir(original_cwd)
        record = case_dir / "failed.txt"
        input_file = case_dir / "failed.in"
        if ok or not record.is_file() or not input_file.is_file():
            raise RuntimeError(f"stress {mode} failure artifacts were not saved")
        if needle not in record.read_text(encoding="utf-8"):
            raise RuntimeError(f"stress {mode} failure reason was not preserved")
        if mode == "wrong" and input_file.read_text(encoding="utf-8").splitlines()[0] != "1":
            raise RuntimeError("wrong-answer path did not shrink the failing input")
    print("Python stress harness smoke: correct, WA shrink/save, nonzero exit, and timeout passed.")


def smoke_constructive_example(compiler: str, temp: Path) -> None:
    chapter = (ROOT / "content/chapters/03-basic-search.md").read_text(encoding="utf-8")
    section = chapter.split("## 3.13 常用构造题思路", 1)[1]
    blocks = re.findall(r"```cpp\s*\n(.*?)\n```", section, re.DOTALL)
    if not blocks:
        raise RuntimeError("chapter 3.13 has no runnable construction example")
    executable = compile_cpp(compiler, blocks[0], temp, "constructive-example")
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5)
    if result.returncode != 0:
        raise RuntimeError(f"constructive example assertions failed: {result.stderr}")
    print("Construction example exhaustive assertions passed.")


def smoke_sliding_window_edges(compiler: str, temp: Path) -> None:
    chapter = (ROOT / "content/chapters/03-basic-search.md").read_text(encoding="utf-8")
    section = chapter.split("## 3.4 双指针与滑动窗口", 1)[1].split("## 3.5", 1)[0]
    blocks = re.findall(r"```cpp\s*\n(.*?)\n```", section, re.DOTALL)
    if not blocks:
        raise RuntimeError("chapter 3.4 has no runnable sliding-window example")
    checks = r'''
int main() {
    assert(minLengthAtLeast({}, 0) == 0);
    assert(minLengthAtLeast({1, 2}, 0) == 1);
    assert(minLengthAtLeast({1, 2, 3}, 4) == 2);
    assert(minLengthAtLeast({1, 2}, 5) == 0);
}
'''
    executable = compile_cpp(compiler, blocks[0] + checks, temp, "sliding-window-edges")
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5)
    if result.returncode != 0:
        raise RuntimeError(f"sliding-window edge assertions failed: {result.stderr}")
    print("Sliding-window edge assertions passed.")


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
    try:
        with tempfile.TemporaryDirectory(prefix="icpcboard-smoke-") as smoke_name:
            smoke_temp = Path(smoke_name)
            smoke_python_harness(compiler, smoke_temp)
            smoke_constructive_example(compiler, smoke_temp)
            smoke_sliding_window_edges(compiler, smoke_temp)
    except Exception as error:
        print(f"Foundation smoke check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
