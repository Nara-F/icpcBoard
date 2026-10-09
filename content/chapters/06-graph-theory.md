
# 6. 图论

本章默认点编号为 `1..n`。无向边必须加入两个方向；权值和距离使用 `long long`。若题目允许重边，应保留全部边，或在矩阵建图时取最小权值。DFS 与 BFS 基础统一见第 3.8、3.9 节。


## 6.1 拓扑排序

**问题与思路：** 把有向无环图排成每条边都从前指向后的序列，适合先修关系、任务依赖与 DAG DP。统计入度，将所有入度为 0 的点入队，取出后删除其出边。邻接表实现时间 $O(n+m)$、空间 $O(n+m)$。结果不足 $n$ 个点说明存在有向环，因而没有拓扑序。

**用法：**

- 建有向边 `u -> v`，并令 `indegree[v]++`。
- `topologicalSort` 返回任意一个拓扑序；有环返回空数组。
- 若需要字典序最小序列，把普通队列换成小根堆。
- 函数按值接收入度，不会破坏调用者保存的原入度。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> topologicalSort(
    const vector<vector<int>>& graph,
    vector<int> indegree
) {
    // graph[u] 只保存有向出边 u->v；indegree 必须逐条统计所有入边（含重边）。
    int n = (int)graph.size() - 1;
    queue<int> q;
    for (int u = 1; u <= n; ++u) {
        if (indegree[u] == 0) q.push(u);
    }

    // 不变量：队列中的点在“删去已输出点及其出边后”入度为 0。
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : graph[u]) {
            if (--indegree[v] == 0) q.push(v);
        }
    }

    if ((int)order.size() != n) return {};  // 有向环导致剩余点无法降至入度 0
    return order;
}
```

**易错点：**

1. 计算的是入度而不是出度。
2. 重边需逐条计入入度，也会在遍历时逐条减少。
3. 返回空数组既可能表示有环，也可能是 `n=0`；本章默认 `n>=1`。

**参考：**

- [OI Wiki：拓扑排序](https://oi-wiki.org/graph/topo/)

## 6.2 Dijkstra 单源最短路

**问题与思路：** 求一个起点到所有点的最短距离，适用于有向或无向图，但边权必须非负。用小根堆反复取当前距离最小的点并松弛出边，旧堆记录直接跳过。复杂度 $O((n+m)\log n)$，空间 $O(n+m)$。负边会破坏正确性；不可达点保持 `INF`。

**用法：**

- 有向边只加入 `graph[u]`；无向边同时加入 `u->v` 与 `v->u`。
- 保留重边没有问题，算法会自动选更优边。
- `dist[v]==INF` 表示不可达；`previous` 可还原路径。
- 所有权值必须 `>=0`，距离与权值使用 `long long`；有限最短距离须小于 `INF` 且加法不越界。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

struct Edge {
    // 邻接表中的一项表示有向边“当前点 -> to”；无向边需手动加入反向项。
    int to;
    ll weight;
};

struct DijkstraResult {
    vector<ll> distance;  // INF 表示从 start 不可达
    vector<int> previous; // 最短路树中的前驱；start 和不可达点均为 -1
};

DijkstraResult dijkstra(
    const vector<vector<Edge>>& graph,
    int start
) {
    // 仅适用于所有边权 >=0；允许重边。点编号为 1..n。
    int n = (int)graph.size() - 1;
    vector<ll> distance(n + 1, INF);
    vector<int> previous(n + 1, -1);
    // 小根堆保存“入堆时距离,点”；同一点可能有多条新旧记录。
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;

    distance[start] = 0;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [currentDistance, u] = pq.top();
        pq.pop();
        if (currentDistance != distance[u]) continue;  // 跳过已经失效的旧记录

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            // u 被取出时 distance[u] 已是当前最优；这里松弛一条出边 u->v。
            if (distance[v] > distance[u] + edge.weight) {
                distance[v] = distance[u] + edge.weight;
                previous[v] = u;
                pq.push({distance[v], v});
            }
        }
    }
    return {distance, previous};
}

vector<int> restorePath(int start, int target, const vector<int>& previous) {
    // 返回 start 到 target 的点序列；前驱链无法到 start 时返回空数组。
    vector<int> path;
    for (int v = target; v != -1; v = previous[v]) {
        path.push_back(v);
        if (v == start) break;
    }
    if (path.empty() || path.back() != start) return {};
    reverse(path.begin(), path.end());
    return path;
}
```

**易错点：**

1. 存在负权边时不能使用 Dijkstra，即使负边不从起点直接发出。
2. 无向边必须加入两个方向；重边不应错误覆盖成较大权值。
3. 必须跳过小根堆中的旧距离记录。
4. 不可达时不能直接拿 `INF` 参与后续加法或输出为普通距离。

**参考：**

- [OI Wiki：最短路](https://oi-wiki.org/graph/shortest-path/)

## 6.3 Bellman–Ford 与负环判断

**问题与思路：** 单源最短路含负权边时使用。连续扫描所有边并松弛，最多做 $n-1$ 轮；第 $n$ 轮仍可松弛说明存在“起点可达”的负环，最短路无定义。时间 $O(nm)$、空间 $O(n)$，适合规模较小或用于差分约束。不可达点不能参与松弛。

**用法：**

- 边表 `DirectedEdge{from,to,weight}` 表示一条有向边；无向负边会立即构成往返负环。
- 返回值中的布尔量只判断从 `start` 可达的负环。
- 无负环时，`distance[v]==INF` 表示不可达。
- 若某轮没有更新，可提前结束。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

struct DirectedEdge {
    // 边方向固定为 from -> to；无向边若需要须显式加入两个方向。
    int from, to;
    ll weight;
};

pair<vector<ll>, bool> bellmanFord(
    int n,
    int start,
    const vector<DirectedEdge>& edges
) {
    // 用更宽的中间值避免 long long 松弛溢出；有限答案须能放入 ll 且小于 INF。
    const __int128_t BIG = (__int128_t)1 << 120;
    vector<__int128_t> work(n + 1, BIG);
    work[start] = 0;

    // 每轮扫描所有边；原地松弛可一次推进多条边，但 n 轮判环结论仍成立。
    for (int round = 1; round <= n; ++round) {
        bool changed = false;
        for (const auto& edge : edges) {
            if (work[edge.from] == BIG) continue; // 不可达点不能参与松弛
            __int128_t candidate = work[edge.from] + edge.weight;
            if (candidate < work[edge.to]) {
                work[edge.to] = candidate;
                changed = true;
                if (round == n) return {vector<ll>(n + 1, INF), true};
            }
        }
        if (!changed) break;
    }

    vector<ll> distance(n + 1, INF);
    for (int v = 1; v <= n; ++v) {
        if (work[v] != BIG) {
            // 调用方需保证所有可达最短距离均在 ll 范围内且严格小于 INF。
            distance[v] = (ll)work[v];
        }
    }
    return {distance, false};
}
```

**易错点：**

1. 不跳过不可达起点会发生 `INF + 负数` 的伪松弛。
2. 第 $n$ 轮更新只说明存在起点可达负环；图中其他负环不一定被发现。
3. 有可达负环时，受其影响的点不存在有限最短距离；此实现只返回负环标志，不提供部分距离。
4. 所有有限距离必须能表示为 `long long` 且严格小于 `INF`；中间松弛用 `__int128` 避免常见边权累加溢出。

**参考：**

- [OI Wiki：Bellman–Ford 算法](https://oi-wiki.org/graph/shortest-path/#bellmanford-%E7%AE%97%E6%B3%95)

## 6.4 Floyd 全源最短路

**问题与思路：** 求任意两点间最短路，适合点数较小的稠密图，并允许负边。依次允许编号 `1..k` 的点作为中转，更新 `dist[i][j]`。时间 $O(n^3)$、空间 $O(n^2)$。不能存在负环；完成后若 `dist[i][i]<0`，说明存在负环。不可达状态必须先判断再相加。

**用法：**

- 先构造 `(n+1)×(n+1)` 矩阵：对角线为 0，其余为 `INF`。
- 加边时用 `min(dist[u][v],w)` 处理重边；无向边同时更新两个方向。
- 调用后 `dist[u][v]==INF` 表示不可达。
- 模板原地修改距离矩阵。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

vector<vector<ll>> makeDistanceMatrix(int n) {
    // 矩阵使用 1..n；distance[u][v] 表示有向距离，初始仅自身到自身为 0。
    vector<vector<ll>> distance(n + 1, vector<ll>(n + 1, INF));
    for (int i = 1; i <= n; ++i) distance[i][i] = 0;
    return distance;
}

void addDirectedEdge(vector<vector<ll>>& distance, int u, int v, ll weight) {
    // 保留同方向重边中的最小值；无向边需再调用一次 (v,u,weight)。
    distance[u][v] = min(distance[u][v], weight);
}

void floydWarshall(vector<vector<ll>>& distance) {
    int n = (int)distance.size() - 1;
    // k 必须最外层：完成第 k 轮后，只允许 1..k 作为内部中转点。
    for (int k = 1; k <= n; ++k) {
        for (int i = 1; i <= n; ++i) {
            if (distance[i][k] == INF) continue;
            for (int j = 1; j <= n; ++j) {
                if (distance[k][j] == INF) continue;
                // 两段都可达才相加，避免 INF 参与运算产生伪路径。
                distance[i][j] = min(
                    distance[i][j],
                    distance[i][k] + distance[k][j]
                );
            }
        }
    }
}
```

**易错点：**

1. 循环顺序必须让中转点 `k` 在最外层。
2. 加边时需要对重边取最小值，不能直接覆盖。
3. 负边可以使用，但存在负环时普通最短距离无定义。
4. 矩阵空间为 $O(n^2)$，点数大时不可用。

**参考：**

- [OI Wiki：Floyd 算法](https://oi-wiki.org/graph/shortest-path/#floyd-%E7%AE%97%E6%B3%95)

## 6.5 Kruskal 最小生成树

**问题与思路：** 在连通无向带权图中选 $n-1$ 条边，使总权最小。按边权升序扫描，用并查集加入连接两个不同连通块的边。排序主导时间 $O(m\log m)$，空间 $O(n+m)$；允许负权和重边。若最终不足 $n-1$ 条边，原图不连通，只得到最小生成森林。

**用法：**

- 每条无向边在边表中只放一次，不需要存两个方向。
- `kruskal(n,edges)` 返回是否连通、总权和、所选边。
- 重边、自环可保留；自环会因端点已连通而被忽略。
- 只求总权时可以删除 `chosen` 以节省少量空间。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct DSU {
    // 只有根的 sizeOf 有效；路径压缩和按大小合并保证近常数均摊复杂度。
    vector<int> parent, sizeOf;
    explicit DSU(int n) : parent(n + 1), sizeOf(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sizeOf[a] < sizeOf[b]) swap(a, b);
        parent[b] = a;
        sizeOf[a] += sizeOf[b];
        return true;
    }
};

struct WeightedEdge {
    // 无向边在边表中只保存一次；允许负权、重边和自环。
    int u, v;
    ll weight;
};

struct KruskalResult {
    bool connected;
    ll totalWeight;
    vector<WeightedEdge> chosen;
};

KruskalResult kruskal(int n, vector<WeightedEdge> edges) {
    // 按权从小到大扫描；不成环的最轻边一定可安全加入当前生成森林。
    sort(edges.begin(), edges.end(), [](const auto& a, const auto& b) {
        return a.weight < b.weight;
    });

    DSU dsu(n);
    ll totalWeight = 0;
    vector<WeightedEdge> chosen;
    for (const auto& edge : edges) {
        if (!dsu.unite(edge.u, edge.v)) continue;  // 同一连通块：加入会成环
        totalWeight += edge.weight;
        chosen.push_back(edge);
        if ((int)chosen.size() == n - 1) break;
    }
    return {(int)chosen.size() == n - 1, totalWeight, chosen};
}
```

**易错点：**

1. 最小生成树只定义在无向连通图上。
2. 图不连通时 `totalWeight` 是生成森林权值，不能当作生成树答案。
3. 总权可能超过 `int`；负边应照常参与排序。

**参考：**

- [OI Wiki：最小生成树](https://oi-wiki.org/graph/mst/)

## 6.6 二分图判定

**问题与思路：** 判断无向图能否把点分成两组，使每条边跨组；等价于图中没有奇环。对每个未染色点 BFS，令相邻点颜色相反，若相邻点同色则失败。时间 $O(n+m)$、空间 $O(n+m)$。非连通图必须逐个连通块染色；自环必然使图不是二分图。

**用法：**

- 无向边必须双向加入邻接表。
- 返回 `true` 时，`color[u]` 为 0 或 1，给出一组合法划分。
- `color[u]==-1` 表示尚未访问。
- 重边不影响结论；自环会被正确判为冲突。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool colorBipartite(const vector<vector<int>>& graph, vector<int>& color) {
    // graph 必须是无向图的双向邻接表；-1 未访问，0/1 表示两侧颜色。
    int n = (int)graph.size() - 1;
    color.assign(n + 1, -1);

    // 必须枚举所有起点，才能覆盖非连通图中的每个连通块。
    for (int start = 1; start <= n; ++start) {
        if (color[start] != -1) continue;
        queue<int> q;
        color[start] = 0;
        q.push(start);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : graph[u]) {
                if (color[v] == -1) {
                    // 每条无向边两端必须异色；异或 1 得到另一种颜色。
                    color[v] = color[u] ^ 1;
                    q.push(v);
                } else if (color[v] == color[u]) {
                    return false;
                }
            }
        }
    }
    return true;
}
```

**易错点：**

1. 只从点 1 开始会漏掉其他连通块中的奇环。
2. 判定模板针对无向图；有向边通常先忽略方向讨论底图。
3. `color` 的 0 是一种颜色，不等于“未访问”。

**参考：**

- [OI Wiki：二分图](https://oi-wiki.org/graph/bi-graph/)

## 6.7 二分图最大匹配（增广路）

**问题与思路：** 在二分图中选最多条互不共享端点的边，适合任务分配和配对。逐个左部点 DFS 寻找增广路；遇到已匹配右点时，尝试为其原搭档改配。朴素复杂度 $O(VE)$、空间 $O(V+E)$，适合中等规模；更大规模可用 Hopcroft–Karp。

**用法：**

- 左部点编号 `1..leftCount`，右部点编号 `1..rightCount`。
- `graphLeft[u]` 只保存左点 `u` 能连接的右点。
- 返回最大匹配数；`matchRight[v]` 是右点 `v` 匹配的左点，0 表示未匹配。
- 每轮 DFS 必须使用新的右部访问标记。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct BipartiteMatcher {
    int leftCount, rightCount;
    // graphLeft[u] 只存“左部 u -> 右部 v”，左右编号属于两个独立空间。
    vector<vector<int>> graphLeft;
    vector<int> matchRight; // matchRight[v]=u；0 表示右点 v 当前未匹配
    vector<int> seen;       // 时间戳：本轮增广中右点是否已尝试
    int visitToken = 0;

    BipartiteMatcher(int leftCount, int rightCount)
        : leftCount(leftCount), rightCount(rightCount),
          graphLeft(leftCount + 1), matchRight(rightCount + 1, 0),
          seen(rightCount + 1, 0) {}

    void addEdge(int left, int right) {
        graphLeft[left].push_back(right);
    }

    bool augment(int u) {
        // 不变量：尝试为左点 u 找交错路；成功时沿递归链整体改配。
        for (int v : graphLeft[u]) {
            if (seen[v] == visitToken) continue;
            seen[v] = visitToken;
            // v 空闲，或能把 v 的旧搭档改配到别处，就可令 u 占用 v。
            if (matchRight[v] == 0 || augment(matchRight[v])) {
                matchRight[v] = u;
                return true;
            }
        }
        return false;
    }

    int maximumMatching() {
        int matching = 0;
        for (int u = 1; u <= leftCount; ++u) {
            ++visitToken; // 每个左点必须拥有独立访问轮次，不能共用 seen 状态
            if (augment(u)) ++matching;
        }
        return matching;
    }
};
```

**易错点：**

1. 输入必须明确哪边是左部、哪边是右部，编号空间不要混淆。
2. 每次尝试新的左点时都要清空访问状态或增加时间戳。
3. 再次调用 `maximumMatching()` 会在已有匹配上继续运行，不是从空匹配重算。

**参考：**

- [OI Wiki：二分图最大匹配](https://oi-wiki.org/graph/graph-matching/bigraph-match/)

## 6.8 强连通分量（Tarjan）

**问题与思路：** 把有向图分成最大强连通块，块内任意两点互相可达，常用于缩点成 DAG。DFS 记录访问次序 `dfn` 与能回到的最早次序 `low`；当 `low[u]==dfn[u]` 时弹栈得到一个分量。时间 $O(n+m)$、空间 $O(n+m)$。递归深度可达 $n$。

**用法：**

- 建有向图，只加入题目给出的方向。
- 构造 `TarjanSCC solver(graph)` 后调用 `run()`。
- `component[u]` 为点所属分量编号，范围 `0..componentCount-1`。
- 缩点时遍历原边；若两端分量不同，则加入分量间边并按需去重。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TarjanSCC {
    // graph 是 1-based 有向邻接表；只按题目方向加边，重边不影响正确性。
    const vector<vector<int>>& graph;
    int n, timer = 0, componentCount = 0;
    // dfn：首次访问序；low：经 DFS 树边和栈内返边能到达的最小 dfn。
    vector<int> dfn, low, component, st;
    vector<char> inStack;

    explicit TarjanSCC(const vector<vector<int>>& graph)
        : graph(graph), n((int)graph.size() - 1),
          dfn(n + 1, 0), low(n + 1, 0), component(n + 1, -1),
          inStack(n + 1, false) {}

    void dfs(int u) {
        // st 只保存尚未归入任何 SCC 的活跃点，inStack 与之同步。
        dfn[u] = low[u] = ++timer;
        st.push_back(u);
        inStack[u] = true;

        for (int v : graph[u]) {
            if (dfn[v] == 0) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (inStack[v]) {
                // 已访问且仍在栈中才可能属于当前 SCC；此处必须使用 dfn[v]。
                low[u] = min(low[u], dfn[v]);
            }
        }

        if (low[u] == dfn[u]) {
            // u 是一个 SCC 的 DFS 根，弹到 u 为止的点恰属于同一分量。
            while (true) {
                int v = st.back();
                st.pop_back();
                inStack[v] = false;
                component[v] = componentCount;
                if (v == u) break;
            }
            ++componentCount;
        }
    }

    void run() {
        for (int u = 1; u <= n; ++u) {
            if (dfn[u] == 0) dfs(u);
        }
    }
};
```

**易错点：**

1. 遇到仍在栈中的已访问点时，用 `dfn[v]` 更新，而不是无条件用 `low[v]`。
2. 已弹出栈的点不能再更新当前点的 `low`。
3. 大图递归可能栈溢出，需要增大栈限制或改迭代实现。

**参考：**

- [OI Wiki：强连通分量](https://oi-wiki.org/graph/scc/)

## 6.9 割点与桥（Tarjan）

**问题与思路：** 无向图中，删去某点使连通块增加则它是割点；删去某边使连通块增加则它是桥。DFS 计算 `dfn`、`low`：树边 `(u,v)` 满足 `low[v]>dfn[u]` 是桥；非根点存在 `low[v]>=dfn[u]` 则为割点，根需至少两个 DFS 子树。时间 $O(n+m)$。

**用法：**

- 用 `addEdge(u,v)` 添加一条无向边，内部共享同一边编号。
- 调用 `run()` 后，`isCutVertex[u]` 表示割点，`bridges` 保存桥的端点。
- 模板可正确处理重边：DFS 只跳过原树边的编号，不跳过所有父节点边。
- 非连通图会从每个未访问点重新 DFS。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct UndirectedLowlink {
    // 同一条无向边的两个邻接项共享 id；这是正确处理父子重边的关键。
    struct Edge { int to, id; };

    int n, timer = 0, edgeCount = 0;
    vector<vector<Edge>> graph;
    vector<int> dfn, low;
    vector<char> isCutVertex;
    vector<pair<int, int>> bridges;

    explicit UndirectedLowlink(int n)
        : n(n), graph(n + 1), dfn(n + 1), low(n + 1),
          isCutVertex(n + 1, false) {}

    void addEdge(int u, int v) {
        // 每条无向边只调用一次，内部自动加入 u->v 与 v->u 两个方向。
        graph[u].push_back({v, edgeCount});
        graph[v].push_back({u, edgeCount});
        ++edgeCount;
    }

    void dfs(int u, int parentEdge) {
        // low[u]：从 u 的 DFS 子树经至多一条非树边能到达的最小 dfn。
        dfn[u] = low[u] = ++timer;
        int childCount = 0;

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            if (edge.id == parentEdge) continue; // 只跳过来时那一条边，不跳所有父点边
            if (dfn[v] == 0) {
                ++childCount;
                dfs(v, edge.id);
                low[u] = min(low[u], low[v]);
                if (low[v] > dfn[u]) bridges.push_back({u, v}); // 子树无法绕回 u 或更高
                // 非根 u：v 子树无法越过 u 时，删除 u 会把 v 子树分离。
                if (parentEdge != -1 && low[v] >= dfn[u]) isCutVertex[u] = true;
            } else {
                low[u] = min(low[u], dfn[v]);
            }
        }

        // DFS 根没有父侧，只有至少两个独立 DFS 子树时才是割点。
        if (parentEdge == -1 && childCount >= 2) isCutVertex[u] = true;
    }

    void run() {
        for (int u = 1; u <= n; ++u) {
            if (dfn[u] == 0) dfs(u, -1);
        }
    }
};
```

**易错点：**

1. 割点条件是 `>=`，桥条件是严格 `>`。
2. DFS 根的割点条件特殊，需至少两个 DFS 子树。
3. 有重边时不能只用 `v==parent` 跳边，必须记录边编号。
4. 该算法针对无向图；有向图应使用强连通分量等概念。

**参考：**

- [OI Wiki：割点和桥](https://oi-wiki.org/graph/cut/)

## 6.10 最近公共祖先（倍增 LCA）

**问题与思路：** 在树上反复查询两点最深的公共祖先，也可据此求路径长度。预处理每个点的深度与第 $2^j$ 个祖先；查询时先把深点提升，再同步提升两点。预处理 $O(n\log n)$，单次查询 $O(\log n)$，空间 $O(n\log n)$。模板要求输入为一棵树。

**用法：**

- 无向树边需双向加入，构造 `BinaryLiftingLCA(graph,root)`。
- `lca(u,v)` 返回最近公共祖先。
- 无权路径边数为 `depth[u]+depth[v]-2*depth[lca(u,v)]`。
- 根可任意选择；不同根会改变祖先关系，但不会改变无权路径长度。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct BinaryLiftingLCA {
    int n, levels;
    vector<int> depth;       // depth[root]=0；模板只接受一棵连通树
    // up[j][u] 是 u 的第 2^j 个祖先；越过根后统一落到虚拟点 0。
    vector<vector<int>> up;

    BinaryLiftingLCA(const vector<vector<int>>& tree, int root) {
        // tree 是 1-based 无向树，必须双向加边且不能含环、重边或自环。
        n = (int)tree.size() - 1;
        levels = 1;
        while ((1 << levels) <= n) ++levels;
        depth.assign(n + 1, -1);
        up.assign(levels, vector<int>(n + 1, 0));

        queue<int> q;
        depth[root] = 0;
        q.push(root);
        // BFS 定根：up[0][v] 是父节点，同时也充当“已访问”的判断依据。
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : tree[u]) {
                if (v == up[0][u]) continue; // 仅跳父边；因此输入必须真的是树
                up[0][v] = u;
                depth[v] = depth[u] + 1;
                q.push(v);
            }
        }

        for (int j = 1; j < levels; ++j) {
            for (int u = 1; u <= n; ++u) {
                // 先跳 2^(j-1)，再从中间祖先跳同样距离。
                up[j][u] = up[j - 1][up[j - 1][u]];
            }
        }
    }

    int lift(int u, int steps) const {
        // 按 steps 的二进制位拆分向上跳；调用者应保证 steps<=depth[u]。
        for (int j = 0; j < levels; ++j) {
            if ((steps >> j) & 1) u = up[j][u];
        }
        return u;
    }

    int lca(int u, int v) const {
        // 先对齐深度，再从最高位向下保持“两点祖先仍不同”。
        if (depth[u] < depth[v]) swap(u, v);
        u = lift(u, depth[u] - depth[v]);
        if (u == v) return u;
        for (int j = levels - 1; j >= 0; --j) {
            if (up[j][u] != up[j][v]) {
                u = up[j][u];
                v = up[j][v];
            }
        }
        // 此时 u、v 不同但父节点相同，该父节点就是最近公共祖先。
        return up[0][u];
    }
};
```

**易错点：**

1. 输入若有环，模板只跳过父边，会重复访问；必须保证它是一棵树。
2. `up` 的 0 号虚拟点各级祖先应保持为 0。
3. 查询点必须和根处于同一棵树，本模板不处理森林跨树查询。
4. `1 << levels` 在极大 `n` 时应改用 `1LL << levels`。

**参考：**

- [OI Wiki：最近公共祖先](https://oi-wiki.org/graph/lca/)

## 6.11 树的直径

**问题与思路：** 树的直径是任意两点间最长简单路径。任选点出发找距离最远点 `a`，再从 `a` 找最远点 `b`，`dist[b]` 即直径；树上路径唯一，所以一次遍历即可算距离。时间 $O(n)$、空间 $O(n)$。两次遍历法适用于无负权树；无权树令边权为 1。

**用法：**

- `tree[u]` 保存 `{v,w}`，无向边加入两个方向。
- `treeDiameter(tree)` 返回直径长度及两个端点。
- 要还原直径路径，可在第二次遍历中额外记录父节点。
- 模板默认 `n>=1`，且所有边权非负、图连通并有 `n-1` 条边。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct TreeEdge {
    // 无向树边需在两端邻接表各存一份；两次最远点法要求 weight>=0。
    int to;
    ll weight;
};

pair<int, ll> farthestVertex(
    const vector<vector<TreeEdge>>& tree,
    int start
) {
    // 点编号为 1..n；distance=-1 同时作为未访问标记，因此边权必须非负。
    int n = (int)tree.size() - 1;
    vector<ll> distance(n + 1, -1);
    stack<int> st; // 树上起点到每点路径唯一，无需 Dijkstra 即可累计带权距离
    st.push(start);
    distance[start] = 0;

    while (!st.empty()) {
        int u = st.top();
        st.pop();
        for (const auto& edge : tree[u]) {
            if (distance[edge.to] != -1) continue; // 跳过父节点，避免沿无向边返回
            distance[edge.to] = distance[u] + edge.weight;
            st.push(edge.to);
        }
    }

    int vertex = start;
    for (int u = 1; u <= n; ++u) {
        if (distance[u] > distance[vertex]) vertex = u;
    }
    return {vertex, distance[vertex]};
}

tuple<ll, int, int> treeDiameter(const vector<vector<TreeEdge>>& tree) {
    // 第一次找直径某端点 a，第二次从 a 找另一端 b；返回 {长度,a,b}。
    auto [a, ignored] = farthestVertex(tree, 1);
    auto [b, diameter] = farthestVertex(tree, a);
    return {diameter, a, b};
}
```

**易错点：**

1. 该模板依赖树上路径唯一，不能直接用于一般带权图。
2. 有负边时“两次找最远点”结论不再可靠。
3. 距离可能超过 `int`，应使用 `long long`。

**参考：**

- [OI Wiki：树的直径](https://oi-wiki.org/graph/tree-diameter/)

## 6.12 最大流（Dinic）

**问题与思路：** 求有向容量网络从源点到汇点的最大可发送流量。残量网络中先 BFS 建分层图，再 DFS 沿层次递增边反复增广；当前弧避免重复扫描。一般复杂度 $O(V^2E)$，空间 $O(V+E)$，竞赛中常用于二分图匹配、资源分配和割模型。容量必须非负。

**用法：**

- 构造 `Dinic flow(n)`，点编号 `1..n`。
- `addEdge(u,v,cap)` 加一条有向容量边，并自动加容量 0 的反向残量边。
- 无向容量边通常要分别调用两次 `addEdge`，含义需按题目确认。
- `maxFlow(source,sink)` 返回最大流；若只需不超过某上限，可传 `limit`。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

struct Dinic {
    struct Edge {
        int to, reverseIndex;
        ll capacity; // 当前残量，不是原始容量；必须始终非负
    };

    int n;
    vector<vector<Edge>> graph; // graph[u][i] 与其 reverseIndex 指向的残量边互为反边
    vector<int> level;          // 残量网络中从 source 出发的 BFS 层号，-1 为不可达
    vector<int> current;        // 当前弧：本轮分层图中每点尚未尝试的首条边

    explicit Dinic(int n)
        : n(n), graph(n + 1), level(n + 1), current(n + 1) {}

    void addEdge(int from, int to, ll capacity) {
        // 加有向容量边 from->to；反向边初始容量为 0，只用于撤回已经发送的流。
        // 自环的两条边都进入同一 vector，正向边的反向下标要跳过自身。
        Edge forward{to, (int)graph[to].size() + (from == to), capacity};
        Edge backward{from, (int)graph[from].size(), 0};
        graph[from].push_back(forward);
        graph[to].push_back(backward);
    }

    bool buildLevelGraph(int source, int sink) {
        // 只沿正残量边 BFS；后续 DFS 只能走 level 恰好增加 1 的边。
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[source] = 0;
        q.push(source);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (const Edge& edge : graph[u]) {
                if (edge.capacity <= 0 || level[edge.to] != -1) continue;
                level[edge.to] = level[u] + 1;
                q.push(edge.to);
            }
        }
        return level[sink] != -1;
    }

    ll sendFlow(int u, int sink, ll pushed) {
        // 返回本次从 u 实际送到 sink 的流量；pushed 是上游允许的上限。
        if (u == sink || pushed == 0) return pushed;
        // i 使用引用：失败边以后无需重扫，这就是当前弧优化的不变量。
        for (int& i = current[u]; i < (int)graph[u].size(); ++i) {
            Edge& edge = graph[u][i];
            if (edge.capacity <= 0 || level[edge.to] != level[u] + 1) continue;
            ll sent = sendFlow(edge.to, sink, min(pushed, edge.capacity));
            if (sent == 0) continue;
            // 正向残量减少、反向残量增加，保证之后可以撤销/改道这部分流。
            edge.capacity -= sent;
            graph[edge.to][edge.reverseIndex].capacity += sent;
            return sent;
        }
        return 0;
    }

    ll maxFlow(int source, int sink, ll limit = INF) {
        // 要求 source!=sink、点编号 1..n；返回不超过 limit 的最大增广量。
        assert(source != sink);
        ll flow = 0;
        while (flow < limit && buildLevelGraph(source, sink)) {
            fill(current.begin(), current.end(), 0); // 新分层图必须重置当前弧
            while (flow < limit) {
                ll sent = sendFlow(source, sink, limit - flow);
                if (sent == 0) break;
                flow += sent;
            }
        }
        return flow;
    }
};
```

最大流可建模二分图匹配：源点连左部、右部连汇点的容量设为 1，左右兼容边也设为 1。若要取最小割，必须让 `maxFlow` 跑到无增广路为止；随后调用 `buildLevelGraph(source,sink)`，它返回 `false`，此时 `level[v]>=0` 的点构成残量可达侧。用原始输入边表累加从可达侧指向不可达侧的容量；不要把反向残量边当作原边计入。若有限 `limit` 提前截断，不能据此读取最小割。

**易错点：**

1. 反向边是残量边，不是把原边简单复制一份；其初始容量为 0。
2. 修改正向残量后必须同步增加对应反向残量。
3. `source==sink` 时最大流没有通常意义，调用前应保证两者不同。
4. 多次调用 `maxFlow` 会在当前残量网络上继续增广；重算需重新建图。

**参考：**

- [OI Wiki：最大流](https://oi-wiki.org/graph/flow/max-flow/)


## 6.13 欧拉路径与回路

**用途 / 用法：** 每条边恰走一次。下例 Hierholzer 求无向图边序对应的点序，$O(n+m)$；平行边靠边编号区分。

```cpp
vector<int> eulerTrailUndirected(
    int n, const vector<pair<int, int>>& edges) {
    // Hierholzer 回溯入答案，末尾需 reverse；每条边只消费一次。
    vector<vector<pair<int, int>>> g(n + 1);
    vector<int> deg(n + 1), it(n + 1);
    vector<char>used(edges.size());
    for (int id = 0; id < (int)edges.size(); ++id) {
        auto [u, v] = edges[id];
        g[u].push_back({v,id});
        g[v].push_back({u,id});
        ++deg[u];
        ++deg[v];
    }
    int start = 0, odd = 0;
    for (int u = 1; u <= n; ++u) {
        if (deg[u] == 0) {
            continue;
        }
        if (!start) {
            start = u;
        }
        if (deg[u] & 1) {
            ++odd;
            start = u;
        }
    }
    if (!start || (odd != 0 && odd != 2)) {
        return {};
    }
    vector<int> st{start}, path;
    while (!st.empty()) {
        int u = st.back();
        while (it[u] < (int)g[u].size()
               && used[g[u][it[u]].second]) {
            ++it[u];
        }
        if (it[u] == (int)g[u].size()) {
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = g[u][it[u]++];
            if (!used[id]) {
                used[id] = true;
                st.push_back(v);
            }
        }
    }
    if (path.size() != edges.size() + 1) {
        return {};
    }
    reverse(path.begin(), path.end());
    return path;
}
```

条件：忽略孤立点后连通；无向回路奇度点为 0，路径为 2。有向图需入出度平衡，并按有向边只加入一次。

坑：结果是逆序回退所得，最后反转；必须检查使用了全部边；无边图的返回约定按题意调整。

## 6.14 2-SAT

**用途 / 用法：** 每个布尔变量二选一、约束是两个文字的析取。建蕴含图后 SCC，$O(n+m)$。

```cpp
struct TwoSAT {
    // 每个变量 x 有 false/true 两个文字节点；蕴含边记在 g 中。
    int vars;
    vector<vector<int>> g;
    TarjanSCC scc; // 复用 6.8 节实现；它保存 g 的引用，故 g 必须先声明

    explicit TwoSAT(int n) : vars(n), g(2 * n + 1), scc(g) {}

    int node(int x, bool value) const {
        return 2 * (x - 1) + (value ? 1 : 0) + 1;
    }
    void imply(int a, int b) {
        g[a].push_back(b);
    }
    void addOr(int x, bool xv, int y, bool yv) {
        // (x==xv) OR (y==yv) 等价于 ¬x->y 与 ¬y->x。
        int a = node(x, xv), b = node(y, yv);
        imply(node(x, !xv), b);
        imply(node(y, !yv), a);
    }
    optional<vector<char>> solve() {
        scc.run();
        vector<char> answer(vars + 1);
        for (int x = 1; x <= vars; ++x) {
            int f = node(x, false), t = node(x, true);
            if (scc.component[f] == scc.component[t]) return nullopt;
            // TarjanSCC 按弹栈顺序编号，较小分量先赋值为 true。
            answer[x] = scc.component[t] < scc.component[f];
        }
        return answer;
    }
};
```

坑：复用 6.8 节的 `TarjanSCC`；节点编号及分量编号方向必须一致；若更换 SCC 实现，需重新核对赋值比较方向。

## 6.15 最小费用最大流

**用途 / 用法：** 在最大流量前提下最小化费用；逐次找残量网络最短增广路。此 SPFA 版最坏复杂度高，适合中小网络；要求 `s!=t`、费用与总代价可由 `long long` 表示，且增广过程中不存在可达负费用环。

```cpp
struct MinCostMaxFlow {
    // 残量网络逐次找最短路，parent 回溯增广；反向边费用为负。
    struct E {
        int to, rev;
        ll cap, cost;
    };
    int n;
    vector<vector<E>> g;
    explicit MinCostMaxFlow(int nodeCount)
        : n(nodeCount), g(nodeCount + 1) {
    }
    void addEdge(int u, int v, ll cap, ll cost) {
        E a{v, (int)g[v].size() + (u == v), cap, cost};
        E b{u, (int)g[u].size(), 0, -cost};
        g[u].push_back(a);
        g[v].push_back(b);
    }
    pair<ll, ll> run(int s, int t, ll limit = LLONG_MAX / 4) {
        assert(s != t);
        ll flow = 0;
        ll cost = 0;
        const ll INF = numeric_limits<ll>::max() / 4;
        while (flow < limit) {
            vector<ll> d(n + 1, INF);
            vector<int> pv(n + 1), pe(n + 1);
            vector<char> in(n + 1);
            queue<int> q;
            d[s]=0;
            q.push(s);
            in[s]=1;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                in[u]=0;
                for (int i = 0; i < (int)g[u].size(); ++i) {
                    auto& e = g[u][i];
                    if (e.cap && d[e.to] > d[u] + e.cost) {
                        d[e.to] = d[u] + e.cost;
                        pv[e.to] = u;
                        pe[e.to] = i;
                        if (!in[e.to]) {
                            in[e.to] = 1;
                            q.push(e.to);
                        }
                    }
                }
            }
            if (d[t] == INF) break;
            ll add = limit - flow;
            for (int v = t; v != s; v = pv[v]) add = min(add, g[pv[v]][pe[v]].cap);
            flow += add;
            cost += add * d[t];
            for (int v = t; v != s; v = pv[v]) {
                auto& e = g[pv[v]][pe[v]];
                e.cap -= add;
                g[v][e.rev].cap += add;
            }
        }
        return {flow,cost};
    }
};
```


要求点编号 `1..n`、容量非负、`s!=t`；可达距离和 `add * d[t]` 的费用累计必须处于 `long long` 安全范围，有限距离需小于 `INF`。SPFA 逐次最短增广适用于残量网络无可达负费用环的情况；存在此类环时，最短增广路过程可能无法收敛。`run(s,t,limit)` 最多发送 `limit` 单位并返回实际 `{flow,cost}`；重复调用会在已有残量上继续运行。

坑：反向边费用必须取负；若只需指定流量，应达到后提前停止并检查是否足量；大网络用势能+Dijkstra 版本。
