#!/usr/bin/env python3
"""Compile chapter C++ snippets and run focused regression checks (C++17)."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = {
    "05": ROOT / "content/chapters/05-data-structures.md",
    "06": ROOT / "content/chapters/06-graph-theory.md",
    "08": ROOT / "content/chapters/08-strings.md",
    "09": ROOT / "content/chapters/09-computational-geometry.md",
}
PRELUDE = """#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;
"""


def snippets(path: Path) -> list[str]:
    return re.findall(r"```cpp\n(.*?)```", path.read_text(encoding="utf-8"), re.S)


def compile_and_run(name: str, code: str, directory: Path, run: bool = False) -> None:
    source = directory / f"{name.replace(' ', '_')}.cpp"
    binary = source.with_suffix("")
    source.write_text(PRELUDE + code, encoding="utf-8")
    subprocess.run(["g++", "-std=c++17", "-fsyntax-only" if not run else "-O2", str(source), *([] if not run else ["-o", str(binary)])], check=True)
    if run:
        subprocess.run([str(binary)], check=True)


def main() -> None:
    content = {key: snippets(path) for key, path in CHAPTERS.items()}
    # Three supplementary snippets intentionally reuse definitions in the same chapter.
    dependencies = {
        ("05", 10): content["05"][5],   # RangeFenwick uses the chapter's Fenwick.
        ("06", 14): content["06"][7],   # TwoSAT uses the chapter's TarjanSCC.
        ("09", 9): content["09"][0],    # Circle routines use the shared Point helpers.
    }
    checked = 0
    for chapter in ("05", "06", "07", "08", "09"):
        file = next((ROOT / "content/chapters").glob(f"{chapter}-*.md"))
        blocks = snippets(file)
        for index, block in enumerate(blocks, 1):
            dependency = dependencies.get((chapter, index))
            compile_and_run(f"syntax_{chapter}_{index}", (dependency + "\n" if dependency else "") + block, Path(tmpdir))
            checked += 1

    runtime_cases = [
        ("bellman_ford", content["06"][2] + r'''
int main() {
    vector<DirectedEdge> edges{{1,2,4},{2,3,-2},{1,3,5},{4,5,-1},{5,4,0}};
    auto [dist, negative] = bellmanFord(5, 1, edges);
    assert(!negative && dist[3] == 2 && dist[4] == INF);
    edges.push_back({3,2,-3});
    assert(bellmanFord(5, 1, edges).second);
}
'''),
        ("segment_tree", content["05"][6] + r'''
int main() {
    vector<ll> a{0,1,2,3,4,5}; SegmentTree tree(5); tree.build(a);
    tree.rangeAdd(2,4,10);
    assert(tree.rangeSum(1,5) == 45 && tree.rangeSum(2,4) == 39);
}
'''),
        ("dinic", content["06"][11] + r'''
int main() {
    Dinic flow(4); flow.addEdge(1,1,8); flow.addEdge(1,2,3); flow.addEdge(1,3,2);
    flow.addEdge(2,4,3); flow.addEdge(3,4,4); assert(flow.maxFlow(1,4) == 5);
}
'''),
        ("min_cost_flow", content["06"][14] + r'''
int main() {
    MinCostMaxFlow flow(4); flow.addEdge(1,1,7,2); flow.addEdge(1,2,2,1);
    flow.addEdge(1,3,2,0); flow.addEdge(2,4,2,2); flow.addEdge(3,4,2,5);
    auto [amount,cost] = flow.run(1,4,3); assert(amount == 3 && cost == 11);
}
'''),
        ("range_assign_segment_tree", content["05"][12] + r'''
int main() {
    vector<ll> a{0,1,2,3,4,5}; AssignAddSegmentTree st(5); st.build(a);
    st.rangeSet(2,4,0); st.rangeAdd(3,5,2);
    assert(st.rangeSum(1,5) == 12 && st.rangeSum(2,4) == 4);
}
'''),
        ("suffix_array", content["08"][6] + r'''
int main() {
    string s="ababa"; auto sa=suffixArray(s);
    assert((sa == vector<int>{4,2,0,3,1}));
    assert((lcpArray(s,sa) == vector<int>{1,3,0,2}));
}
'''),
        ("circle_geometry", content["09"][0] + "\n" + content["09"][8] + r'''
int main() {
    Circle c{{0,0},1};
    auto tangent=lineCircleIntersections({-2,1},{1,0},c);
    assert(tangent.size()==1 && fabsl(tangent[0].x)<1e-9L);
    assert(circleIntersections(c,Circle{{1,0},1}).size()==2);
}
'''),
    ]
    for name, code in runtime_cases:
        compile_and_run(name, code, Path(tmpdir), run=True)
    print(f"PASS: {checked} chapter code blocks compile under C++17; {len(runtime_cases)} targeted runtime checks pass.")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="icpcboard-check-") as tmpdir:
        main()
