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
    "07": ROOT / "content/chapters/07-mathematics.md",
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


def section_snippet(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise RuntimeError(f"section not found: {heading}")
    blocks = snippets_from_text(match.group(1))
    if len(blocks) != 1:
        raise RuntimeError(f"expected one C++ block in {heading}, found {len(blocks)}")
    return blocks[0]


def snippets_from_text(text: str) -> list[str]:
    return re.findall(r"```cpp\n(.*?)```", text, re.S)


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
        ("dsu_on_tree", section_snippet(CHAPTERS["05"], "## 5.14 DSU on Tree（树上启发式合并）") + r'''
int main() {
    mt19937 rng(712367);
    auto check = [&](int n, int mode) {
        vector<vector<int>> tree(n + 1);
        for (int v = 2; v <= n; ++v) {
            int p = mode == 1 ? v - 1 : (mode == 2 ? 1 : int(rng() % (v - 1)) + 1);
            tree[p].push_back(v);
            tree[v].push_back(p);
        }
        vector<int> color(n + 1);
        for (int u = 1; u <= n; ++u) {
            if (mode == 3) color[u] = 17;
            else if (mode == 4) color[u] = u * 100003 - 900000;
            else color[u] = int(rng() % 9) - 4;
        }
        int root = mode == 0 ? int(rng() % n) + 1 : 1;
        DSUOnTree solver(tree, color, root);
        vector<int> got = solver.solve();
        assert(solver.solve() == got);

        vector<int> parent(n + 1), order{root};
        parent[root] = -1;
        for (size_t i = 0; i < order.size(); ++i) {
            int u = order[i];
            for (int v : tree[u]) if (v != parent[u]) {
                parent[v] = u;
                order.push_back(v);
            }
        }
        vector<set<int>> seen(n + 1);
        vector<int> want(n + 1);
        for (int i = n - 1; i >= 0; --i) {
            int u = order[i];
            seen[u].insert(color[u]);
            for (int v : tree[u]) if (parent[v] == u)
                seen[u].insert(seen[v].begin(), seen[v].end());
            want[u] = (int)seen[u].size();
        }
        for (int u = 1; u <= n; ++u) assert(got[u] == want[u]);
    };

    check(1, 0);
    check(80, 1);
    check(80, 2);
    check(80, 3);
    check(80, 4);
    for (int test = 0; test < 300; ++test) check(1 + int(rng() % 90), 0);
}
'''),
        ("point_segment_tree_custom_merge", section_snippet(CHAPTERS["05"], "## 5.15 单点修改线段树与自定义合并 {#point-segment-tree-custom-merge}") + r'''
int main() {
    vector<Affine> two(3);
    two[1] = makeAffine(2, 1);
    two[2] = makeAffine(3, 4);
    PointSegmentTree<Affine, ComposeAffine> ordered(two, makeAffine(1, 0), ComposeAffine{});
    Affine pair = ordered.rangeQuery(1, 2);
    assert((pair.a * 5 + pair.b) % MOD == 37); // f2(f1(5)); reversed order would be 39
    assert(affineExample() == 821);

    mt19937 rng(91237);
    for (int trial = 0; trial < 100; ++trial) {
        int n = 1 + int(rng() % 30);
        vector<Affine> functions(n + 1);
        for (int i = 1; i <= n; ++i)
            functions[i] = makeAffine(rng() % MOD, rng() % MOD);
        PointSegmentTree<Affine, ComposeAffine> st(functions, makeAffine(1, 0), ComposeAffine{});
        for (int step = 0; step < 80; ++step) {
            if (rng() % 3 == 0) {
                int pos = 1 + int(rng() % n);
                Affine f = makeAffine((ll)(rng() % MOD), (ll)(rng() % MOD));
                functions[pos] = f;
                st.pointSet(pos, f);
            }
            int l = 1 + int(rng() % n), r = 1 + int(rng() % n);
            if (l > r) swap(l, r);
            Affine want = makeAffine(1, 0);
            for (int i = l; i <= r; ++i) want = ComposeAffine{}(want, functions[i]);
            Affine got = st.rangeQuery(l, r);
            assert(got.a == want.a && got.b == want.b);
            ll x = rng() % MOD;
            assert((got.a * x + got.b) % MOD == (want.a * x + want.b) % MOD);
        }
    }

    vector<ll> sums{0, 4, -2, 7, 1};
    PointSegmentTree<ll, plus<ll>> sumTree(sums, 0, plus<ll>{});
    assert(sumTree.rangeQuery(2, 4) == 6);
    sumTree.pointSet(3, 10);
    assert(sumTree.rangeQuery(1, 4) == 13);

    vector<ll> mins{0, 8, -3, 5, 2};
    auto minMerge = [](ll a, ll b) { return min(a, b); };
    PointSegmentTree<ll, decltype(minMerge)> minTree(mins, LLONG_MAX, minMerge);
    assert(minTree.rangeQuery(1, 4) == -3);
    minTree.pointSet(2, 9);
    assert(minTree.rangeQuery(2, 4) == 2);
}
'''),
        ("sieve_divisor_counts", section_snippet(CHAPTERS["07"], "## 7.3 素数筛") + r'''
int main() {
    PrimeSieve empty(0);
    assert(empty.primes.empty() && empty.minPrime.size() == 1);
    PrimeSieve one(1);
    assert(one.primes.empty() && one.divisorCount[0] == 0 && one.countDivisors(1) == 1);

    const int n = 3000;
    PrimeSieve sieve(n);
    vector<int> expectedPrimes;
    for (int x = 2; x <= n; ++x) {
        int divisorCount = 0;
        for (int d = 1; d <= x; ++d) if (x % d == 0) ++divisorCount;
        int smallest = 0, exponent = 0;
        for (int p = 2; p <= x; ++p) if (x % p == 0) {
            smallest = p;
            int value = x;
            while (value % p == 0) { ++exponent; value /= p; }
            break;
        }
        assert(sieve.countDivisors(x) == divisorCount);
        assert(sieve.minPrime[x] == smallest);
        assert(sieve.minPrimeExponent[x] == exponent);
        assert(sieve.isPrime(x) == (divisorCount == 2));
        if (divisorCount == 2) expectedPrimes.push_back(x);
    }
    assert(sieve.divisorCount[0] == 0); // sentinel only; no mathematical meaning
    assert(sieve.divisorCount[1] == 1 && sieve.countDivisors(2) == 2);
    assert(sieve.primes == expectedPrimes);
    assert(!sieve.isPrime(-1) && !sieve.isPrime(0) && !sieve.isPrime(1) && !sieve.isPrime(n + 1));
    assert(sieve.countDivisors(1024) == 11); // 2^10
    assert(sieve.countDivisors(2187) == 8);  // 3^7
    assert(sieve.countDivisors(432) == 20);  // 2^4 * 3^3
    assert(sieve.countDivisors(1225) == 9);  // 5^2 * 7^2
}
'''),
    ]
    for name, code in runtime_cases:
        compile_and_run(name, code, Path(tmpdir), run=True)
    print(f"PASS: {checked} chapter code blocks compile under C++17; {len(runtime_cases)} targeted runtime checks pass.")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="icpcboard-check-") as tmpdir:
        main()
