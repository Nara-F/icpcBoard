# 3. 基础算法与搜索

## 3.1 复杂度与枚举

**用途：** 先估算可执行次数，再选择枚举对象：约 $10^8$ 次简单操作通常已接近上限。直接枚举为 $O(n^k)$，位掩码枚举全部子集为 $O(2^n)$、空间 $O(1)$；只枚举固定大小组合可减少无效状态。适用于数据范围较小或作为对拍暴力。

**思路：**

- `mask` 的第 `i` 位表示是否选择下标 `i`，适合 `n <= 25` 左右的全子集枚举。
- 用 `mask & (1 << i)` 判断元素是否被选择；位数较多时改用 `1LL << i`。
- 枚举某个集合的非空子集时，使用 `(sub - 1) & mask`。
- 若只需固定大小的集合，可用 `__builtin_popcount(mask)` 筛选。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

// 枚举 n 个元素的全部子集，并计算每个子集的元素和。
vector<long long> enumerateSubsetSums(const vector<long long>& a) {
    int n = static_cast<int>(a.size());
    // a 使用 0-based；sums[mask] 表示恰好选择 mask 中元素的总和。
    vector<long long> sums(1ULL << n, 0);
    for (unsigned long long mask = 1; mask < (1ULL << n); ++mask) {
        // 取一个已选位，复用删去该位后的答案，避免每个子集重新扫描 a。
        int bit = __builtin_ctzll(mask);
        sums[mask] = sums[mask ^ (1ULL << bit)] + a[bit];
    }
    return sums;
}

// 枚举 mask 的所有非空子集。
vector<int> nonemptySubmasks(int mask) {
    vector<int> result;
    // 每次删去 sub 的最低位并只保留 mask 中的位；0 不在返回结果中。
    for (int sub = mask; sub; sub = (sub - 1) & mask) {
        result.push_back(sub);
    }
    return result;
}
```

**易错点：**

1. `1 << n` 在 `n >= 31` 时可能溢出，应使用 `1ULL << n`。
2. 全部 `mask` 再枚举其全部子集的总复杂度是 $O(3^n)$，不是 $O(2^n)$。
3. 不要只看大 $O$；字符串复制、哈希和递归的常数明显更大。

**参考：**

- [OI Wiki：枚举](https://oi-wiki.org/basic/enumerate/)
- [OI Wiki：复杂度](https://oi-wiki.org/basic/complexity/)

## 3.2 前缀和与差分

**用途：** 前缀和把静态区间和查询化为两个前缀之差，预处理 $O(n)$、单次查询 $O(1)$、空间 $O(n)$。差分把离线区间加转为两个端点修改，单次修改 $O(1)$，最后 $O(n)$ 还原。若修改与查询交错，应改用树状数组或线段树。

**思路：**

- 一维区间 `[l,r]` 的和为 `prefix[r] - prefix[l - 1]`。
- 对 `[l,r]` 全部加 `value`：`diff[l] += value`，`diff[r+1] -= value`。
- 二维矩形使用左上、右下坐标，容斥四个二维前缀。
- 数值总和可能超过 `int`，数组统一使用 `long long`。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct PrefixSum1D {
    // 输入与查询均为 1-based；prefix[0] 是空前缀哨兵。
    vector<ll> prefix;

    explicit PrefixSum1D(const vector<ll>& a) {
        int n = static_cast<int>(a.size()) - 1; // a[1..n]
        prefix.assign(n + 1, 0);
        for (int i = 1; i <= n; ++i) prefix[i] = prefix[i - 1] + a[i];
    }

    ll query(int left, int right) const {
        // 返回闭区间 [left, right]，调用者需保证 1 <= left <= right <= n。
        return prefix[right] - prefix[left - 1];
    }
};

struct Difference1D {
    int n;
    vector<ll> diff;

    explicit Difference1D(const vector<ll>& a)
        : n(static_cast<int>(a.size()) - 1), diff(n + 2, 0) {
        for (int i = 1; i <= n; ++i) diff[i] = a[i] - a[i - 1];
    }

    void add(int left, int right, ll value) {
        // 闭区间 [left, right] 加 value；diff[n+1] 承接右端撤销标记。
        diff[left] += value;
        diff[right + 1] -= value;
    }

    vector<ll> build() const {
        // 所有离线修改完成后再还原；result 仍为 1-based。
        vector<ll> result(n + 1, 0);
        for (int i = 1; i <= n; ++i) result[i] = result[i - 1] + diff[i];
        return result;
    }
};

struct PrefixSum2D {
    // a 的有效区域为 [1..n] x [1..m]，第 0 行和第 0 列是容斥哨兵。
    vector<vector<ll>> prefix;

    explicit PrefixSum2D(const vector<vector<ll>>& a) {
        int n = static_cast<int>(a.size()) - 1;
        int m = static_cast<int>(a[0].size()) - 1;
        prefix.assign(n + 1, vector<ll>(m + 1, 0));
        for (int i = 1; i <= n; ++i) {
            for (int j = 1; j <= m; ++j) {
                prefix[i][j] = a[i][j] + prefix[i - 1][j]
                    + prefix[i][j - 1] - prefix[i - 1][j - 1];
            }
        }
    }

    ll query(int x1, int y1, int x2, int y2) const {
        // 返回闭矩形 [x1..x2] x [y1..y2]，调用者需保证坐标顺序合法。
        return prefix[x2][y2] - prefix[x1 - 1][y2]
            - prefix[x2][y1 - 1] + prefix[x1 - 1][y1 - 1];
    }
};
```

**易错点：**

1. 预留 `0` 行、`0` 列以及 `n+1` 差分哨兵，避免边界特判。
2. 二维容斥最后要把重复减去的左上区域加回来。
3. 差分适用于“全部修改后统一还原”，不能直接回答中途查询。

**参考：**

- [OI Wiki：前缀和与差分](https://oi-wiki.org/basic/prefix-sum/)

## 3.3 二分查找与二分答案

**用途：** 在有序序列查找边界，或答案存在“左侧均可行、右侧均不可行”等单调性时使用。维护一真一假的边界，每次检查中点并舍弃一半区间。整数二分需 $O(\log R)$ 次检查、空间 $O(1)$；总复杂度还要乘 `check` 的复杂度。

**思路：**

- `firstTrue` 返回闭区间 `[left,right]` 中第一个满足 `check` 的整数。
- 调用前必须保证至少存在一个可行答案；否则自行增加无解判断。
- 求“最后一个可行值”可把判定取反，或使用对应的 `lastTrue`。
- 中点写成 `left + (right - left) / 2`，避免两端相加溢出。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

template <class Check>
ll firstTrue(ll left, ll right, Check check) {
    // 闭区间内要求答案存在，且 check 呈 false...false,true...true。
    while (left < right) {
        // 向下取整；check(mid) 为真时 mid 仍可能是首个真值，不能丢弃。
        ll mid = left + (right - left) / 2;
        if (check(mid)) right = mid;
        else left = mid + 1;
    }
    return left;
}

template <class Check>
ll lastTrue(ll left, ll right, Check check) {
    // 闭区间内要求答案存在，且 check 呈 true...true,false...false。
    while (left < right) {
        // 向上取整保证只剩两个数时 mid != left，否则真分支会死循环。
        ll mid = left + (right - left + 1) / 2;
        if (check(mid)) left = mid;
        else right = mid - 1;
    }
    return left;
}
```

**易错点：**

1. 二分答案的关键是判定函数单调，不能只因答案是数字就二分。
2. 求最后一个可行值时中点必须向上取整，否则可能死循环。
3. 浮点二分通常固定迭代次数；不要直接套整数的 `+1/-1`。

**参考：**

- [OI Wiki：二分](https://oi-wiki.org/basic/binary/)

## 3.4 双指针与滑动窗口

**用途：** 当区间随右端扩张后，合法性关于左端具有单调性时，用左右指针维护连续区间；每个元素至多进出窗口一次，时间 $O(n)$、空间由维护信息决定。常用于非负数组和、至多含若干种元素、去重窗口；有负数时“和越长越大”不成立。

**思路：**

- 右指针每次加入一个元素，再不断移动左指针直到窗口合法。
- 求最长合法区间时，在收缩完成后更新答案。
- 求最短满足区间时，应在条件成立期间更新答案并收缩。
- 计数类窗口常用 `unordered_map` 或定长频次数组维护。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

// 最长无重复连续子数组长度，元素值无需预先离散化。
int longestDistinctSubarray(const vector<int>& a) {
    // a 使用 0-based；每轮收缩后窗口 [left, right] 始终不含重复值。
    unordered_map<int, int> count;
    int answer = 0;
    for (int left = 0, right = 0; right < static_cast<int>(a.size()); ++right) {
        ++count[a[right]];
        // 新加入值重复时持续移走左端，直到窗口重新合法。
        while (count[a[right]] > 1) {
            if (--count[a[left]] == 0) count.erase(a[left]);
            ++left;
        }
        answer = max(answer, right - left + 1);
    }
    return answer;
}

// 非负数组中，和至少为 target 的最短非空连续子数组长度；不存在返回 0。
int minLengthAtLeast(const vector<long long>& a, long long target) {
    // 仅适用于非负数组；非负性保证收缩左端不会漏过更短可行窗口。
    long long sum = 0;
    int answer = static_cast<int>(a.size()) + 1;
    for (int left = 0, right = 0; right < static_cast<int>(a.size()); ++right) {
        sum += a[right];
        // 条件成立时先记录当前闭区间，再移走左端继续尝试缩短。
        while (sum >= target) {
            answer = min(answer, right - left + 1);
            sum -= a[left++];
        }
    }
    return answer == static_cast<int>(a.size()) + 1 ? 0 : answer;
}
```

**易错点：**

1. 必须证明移动某一端不会错过答案，即窗口条件具有单调性。
2. `while` 收缩和 `if` 收缩含义不同，多数窗口需要连续收缩。
3. 用哈希表计数时，计数归零后及时删除，避免种类数判断错误。

**参考：**

- [OI Wiki：双指针](https://oi-wiki.org/misc/two-pointer/)

## 3.5 离散化

**用途：** 只关心数值的大小、相等关系，而原值范围很大时，将出现过的值排序去重后映射到连续编号。建表 $O(n\log n)$，每次查询 $O(\log n)$，空间 $O(n)$。适用于树状数组、线段树和扫描线；若数值间距离有意义，不能直接用名次替代。

**思路：**

- 收集所有可能参与查询、修改的坐标，再统一排序去重。
- `lower_bound` 得到从 `0` 开始的编号；需要 1-based 时再加一。
- 可用 `values[id]` 从编号恢复原值。
- 动态出现且无法预收集的值，应考虑平衡树或动态线段树。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

template <class T>
struct Discretizer {
    // values[id] 保存第 id 小的不同原值；编号统一为 0-based。
    vector<T> values;

    explicit Discretizer(vector<T> allValues) : values(move(allValues)) {
        sort(values.begin(), values.end());
        // unique 只压缩有效前缀；erase 同步缩小编号域。
        values.erase(unique(values.begin(), values.end()), values.end());
    }

    int id(const T& value) const {
        // value 应在建表输入中出现；否则返回的只是它的插入位置。
        return static_cast<int>(lower_bound(values.begin(), values.end(), value)
                                - values.begin());
    }

    const T& value(int id) const {
        return values[id];
    }

    int size() const {
        return static_cast<int>(values.size());
    }
};
```

**易错点：**

1. 忘记 `unique` 后的 `erase` 会使重复值获得错误的空间规模。
2. 线上读到新坐标后再加入，会导致已有编号整体变化。
3. 区间长度不能用离散编号之差代替，应使用原坐标之差。

**参考：**

- [OI Wiki：离散化](https://oi-wiki.org/misc/discrete/)

## 3.6 分治与归并计数

**用途：** 分治把问题拆成互不重叠的同类子问题，递归求解后合并。典型归并排序与逆序对计数：左右两半已排序时，若右元素更小，它与左侧剩余元素都构成逆序对。时间 $O(n\log n)$，辅助空间 $O(n)$，递归栈 $O(\log n)$。

**思路：**

- 调用 `countInversions(a)` 后，数组会被排序并返回逆序对数量。
- 逆序对可能达到 $n(n-1)/2$，返回值使用 `long long`。
- 合并阶段维持左右区间已排序这一不变量。
- 其他分治题需明确“如何拆分”和“如何在线性或较低复杂度内合并”。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

ll mergeCount(vector<ll>& a, vector<ll>& temp, int left, int right) {
    // 全函数统一使用左闭右开区间 [left, right)。
    if (right - left <= 1) return 0;
    int mid = left + (right - left) / 2;
    ll answer = mergeCount(a, temp, left, mid)
              + mergeCount(a, temp, mid, right);

    int i = left, j = mid, k = left;
    // 不变量：两半已排序，temp[left..k) 已是合并后的最小前缀。
    while (i < mid && j < right) {
        if (a[i] <= a[j]) {
            temp[k++] = a[i++];
        } else {
            temp[k++] = a[j++];
            // 当前右值小于左半当前值，也小于左半剩余的全部 mid-i 个值。
            answer += mid - i;
        }
    }
    while (i < mid) temp[k++] = a[i++];
    while (j < right) temp[k++] = a[j++];
    copy(temp.begin() + left, temp.begin() + right, a.begin() + left);
    return answer;
}

ll countInversions(vector<ll>& a) {
    vector<ll> temp(a.size());
    return mergeCount(a, temp, 0, static_cast<int>(a.size()));
}
```

**易错点：**

1. 本模板采用左闭右开区间 `[left,right)`，递归和合并边界必须一致。
2. 相等元素不是逆序对，比较应写 `<=`。
3. 若每层合并都新建大数组，额外分配会增大常数。

**参考：**

- [OI Wiki：递归与分治](https://oi-wiki.org/basic/divide-and-conquer/)

## 3.7 贪心与区间调度

**用途：** 贪心每步选择当前看来最优且可证明不损失全局最优的决策。典型最多不相交区间：按右端点升序，依次选择起点不早于上个终点的区间。排序 $O(n\log n)$、扫描 $O(n)$、空间 $O(n)$。套用前需用交换论证或反证证明选择安全。

**思路：**

- 本模板把区间视为半开区间 `[left,right)`，端点相接允许同时选择。
- 返回被选区间在原输入中的下标，便于恢复方案。
- 若题意为闭区间且端点重合算相交，把条件改成 `left > lastRight`。
- 带权区间不能用此贪心，应使用按终点排序的动态规划。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Interval {
    long long left, right;
    int id;
};

vector<int> maximumNonOverlapping(vector<Interval> intervals) {
    // 输入按半开区间 [left, right)；返回原输入 id，而不是排序后位置。
    sort(intervals.begin(), intervals.end(), [](const Interval& a, const Interval& b) {
        if (a.right != b.right) return a.right < b.right;
        return a.left < b.left; // 同终点时固定次序，便于复现与检查
    });

    vector<int> chosen;
    long long lastRight = numeric_limits<long long>::lowest();
    for (const auto& interval : intervals) {
        // 选择右端最早的可行区间，为后续选择留下最大空间。
        if (interval.left >= lastRight) {
            chosen.push_back(interval.id);
            lastRight = interval.right;
        }
    }
    return chosen;
}
```

**易错点：**

1. “看起来合理”不是证明；不同目标可能需要按左端点、长度或其他关键字排序。
2. 明确区间开闭，否则端点相等时是否冲突会写反。
3. 最多数量与最大权值是不同问题，后者通常需要 DP。

**参考：**

- [OI Wiki：贪心](https://oi-wiki.org/basic/greedy/)

## 3.8 DFS 深度优先搜索

**用途：** DFS 沿一条分支走到底再回退，适合连通块、可达性、环检测及需要回溯的状态搜索。邻接表图遍历时间 $O(n+m)$、空间 $O(n+m)$，递归栈最坏 $O(n)$。一般图必须记录访问状态；深链可能爆栈，可改显式栈。

**思路：**

- `dfsFrom(start)` 返回起点所在连通块的访问顺序。
- 无向图应加入双向边；有向图只加入题目给出的方向。
- 搜整张图时，对所有未访问点分别调用 DFS，可得到连通块或 DFS 森林。
- 需要退出时刻、子树信息时，在递归调用返回后处理。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> dfsFrom(int start, const vector<vector<int>>& graph) {
    // graph 与节点均为 1-based；环、重边与边方向由建图方式决定。
    int n = static_cast<int>(graph.size()) - 1;
    vector<char> visited(n + 1, false);
    vector<int> order;

    function<void(int)> dfs = [&](int u) {
        // 必须在递归邻点前标记，防止沿环或重边再次进入 u。
        visited[u] = true;
        order.push_back(u);
        for (int v : graph[u]) {
            if (!visited[v]) dfs(v);
        }
    };

    dfs(start);
    return order;
}

vector<vector<int>> connectedComponents(const vector<vector<int>>& graph) {
    // 仅用于无向图连通分量；有向图不能据此求强连通或弱连通。
    int n = static_cast<int>(graph.size()) - 1;
    vector<char> visited(n + 1, false);
    vector<vector<int>> components;
    for (int start = 1; start <= n; ++start) {
        if (visited[start]) continue;
        components.push_back({});
        stack<int> st;
        st.push(start);
        // 显式栈同样在入栈时标记，保证每个点最多入栈一次。
        visited[start] = true;
        while (!st.empty()) {
            int u = st.top();
            st.pop();
            components.back().push_back(u);
            for (int v : graph[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    st.push(v);
                }
            }
        }
    }
    return components;
}
```

**易错点：**

1. 一般图进入节点时就要标记，返回时才标记会在环上无限递归。
2. 递归深度接近 $10^5$ 时有爆栈风险。
3. 有向图的“弱连通”不能直接用原图 DFS 得到。

**参考：**

- [OI Wiki：DFS（图论）](https://oi-wiki.org/graph/dfs/)
- [OI Wiki：DFS（搜索）](https://oi-wiki.org/search/dfs/)

## 3.9 BFS 广度优先搜索

**用途：** BFS 用队列按层扩展状态，在每条边代价相同的图中可求起点到各点的最少边数，并记录前驱还原路径。邻接表实现时间 $O(n+m)$、空间 $O(n+m)$。边权不全相等时不能直接使用；权值仅为 0/1 时可用双端队列优化。

**思路：**

- `distance[v] == -1` 表示不可达，首次入队时记录距离和前驱。
- 无向边加入两次，有向边只加入一次。
- 从多个起点求最近距离时，把所有起点以距离 0 同时入队。
- 用 `restorePath` 根据 `parent` 还原起点到终点的最短路径。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

struct BFSResult {
    vector<int> distance;
    vector<int> parent;
};

BFSResult bfs(const vector<vector<int>>& graph, const vector<int>& sources) {
    // graph 与节点为 1-based；仅保证单位边权图上的最少边数。
    int n = static_cast<int>(graph.size()) - 1;
    vector<int> distance(n + 1, -1), parent(n + 1, -1);
    queue<int> q;
    for (int source : sources) {
        if (distance[source] != -1) continue;
        // 所有源点同时处于第 0 层；重复源点只入队一次。
        distance[source] = 0;
        q.push(source);
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : graph[u]) {
            // 首次入队即得到最短距离并标记，避免同层其他点重复入队。
            if (distance[v] != -1) continue;
            distance[v] = distance[u] + 1;
            parent[v] = u;
            q.push(v);
        }
    }
    return {distance, parent};
}

vector<int> restorePath(int target, const BFSResult& result) {
    // 不可达返回空数组；否则沿 parent 回到某个源点并反转为正向路径。
    if (result.distance[target] == -1) return {};
    vector<int> path;
    for (int v = target; v != -1; v = result.parent[v]) path.push_back(v);
    reverse(path.begin(), path.end());
    return path;
}
```

**易错点：**

1. 节点应在入队时标记；出队才标记会导致重复入队。
2. 普通 BFS 只保证“边数最少”，不保证任意带权图的距离最短。
3. 多源 BFS 的所有源点都应初始化为距离 0。

**参考：**

- [OI Wiki：BFS（搜索）](https://oi-wiki.org/search/bfs/)
- [OI Wiki：BFS（图论）](https://oi-wiki.org/graph/bfs/)

## 3.10 回溯与剪枝

**用途：** 回溯按决策树枚举方案，尝试一个选择、递归、再撤销；剪枝提前排除不可能或不优的分支。最坏仍为指数或阶乘复杂度，空间通常为递归深度。适合规模小的排列、组合和约束满足；应优先安排限制强的决策并设计可证明安全的剪枝。

**思路：**

- 模板示例求所有数恰好使用一次、和为 `target` 的可行排列，找到一个即停止。
- 仅当所有数非负时，`sum > target` 和“剩余和不足”剪枝才成立。
- 先排序，使相同数字相邻，从而跳过同层重复选择。
- 若要枚举全部方案，找到答案后保存并继续搜索，不要立即返回。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

// 找到一个和恰为 target 的子集，返回其元素；要求 a 中元素非负。
vector<int> subsetSumBacktracking(vector<int> a, long long target) {
    // a 必须全为非负数；返回任意可行子集，空数组也可能是合法答案。
    sort(a.rbegin(), a.rend()); // 大数优先，通常更早触发剪枝
    int n = static_cast<int>(a.size());
    vector<long long> suffix(n + 1, 0);
    // suffix[i] 是尚未考虑的 a[i..n-1] 总和，用于剩余和不足剪枝。
    for (int i = n - 1; i >= 0; --i) suffix[i] = suffix[i + 1] + a[i];

    vector<int> path, answer;
    function<bool(int, long long)> dfs = [&](int index, long long sum) {
        if (sum == target) {
            answer = path;
            return true;
        }
        // 后两个剪枝依赖元素非负；允许负数时必须删除。
        if (index == n || sum > target || sum + suffix[index] < target) return false;

        for (int i = index; i < n; ++i) {
            // 只跳过同层重复值，不影响下一层选择另一个相同元素。
            if (i > index && a[i] == a[i - 1]) continue;
            path.push_back(a[i]);
            if (dfs(i + 1, sum + a[i])) return true;
            // 当前选择失败，必须恢复 path 后才能尝试同层下一个选择。
            path.pop_back();
        }
        return false;
    };

    dfs(0, 0);
    return answer;
}
```

**易错点：**

1. 递归返回后必须完整撤销对路径、计数器和标记数组的修改。
2. 去重条件是“同一递归层跳过相同选择”，不能误删不同位置的合法使用。
3. 不满足前提的剪枝会漏解，例如数组含负数时不能用当前和超界剪枝。

**参考：**

- [OI Wiki：回溯法](https://oi-wiki.org/search/backtracking/)
- [OI Wiki：剪枝](https://oi-wiki.org/search/optimization/)

## 3.11 折半搜索

**用途：** 折半搜索把 $n$ 个决策分成两半，各自枚举约 $2^{n/2}$ 个状态，再排序、二分或双指针合并。适合 $n\approx40$ 的子集和、计数和最优化；时间通常 $O(2^{n/2}n)$，空间 $O(2^{n/2})$。它以额外内存换取指数规模的平方根级下降。

**思路：**

- `maximumSubsetSumNotExceeding` 求不超过 `limit` 的最大子集和。
- 模板要求元素非负；若允许负数，仍可枚举，但“无可行解”的返回约定需调整。
- 两半分别生成子集和，右半排序后对每个左半和做 `upper_bound`。
- 若要求方案，子集和需同时保存对应掩码。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

vector<ll> allSubsetSums(const vector<ll>& a, int left, int right) {
    // a 使用 0-based，枚举左闭右开区间 [left, right) 的全部子集和。
    vector<ll> sums{0};
    for (int i = left; i < right; ++i) {
        int oldSize = static_cast<int>(sums.size());
        // 只遍历扩展前的旧状态，否则本轮元素会被重复选择。
        for (int j = 0; j < oldSize; ++j) sums.push_back(sums[j] + a[i]);
    }
    return sums;
}

ll maximumSubsetSumNotExceeding(const vector<ll>& a, ll limit) {
    // 元素要求非负；返回不超过 limit 的最大子集和，默认空集给出 0。
    int mid = static_cast<int>(a.size()) / 2;
    vector<ll> leftSums = allSubsetSums(a, 0, mid);
    vector<ll> rightSums = allSubsetSums(a, mid, static_cast<int>(a.size()));
    sort(rightSums.begin(), rightSums.end());

    ll answer = 0;
    for (ll sum : leftSums) {
        if (sum > limit) continue;
        // upper_bound 指向首个过大值，其前驱才是可配对的最大右半和。
        auto it = upper_bound(rightSums.begin(), rightSums.end(), limit - sum);
        if (it != rightSums.begin()) answer = max(answer, sum + *prev(it));
    }
    return answer;
}
```

**易错点：**

1. `2^(n/2)` 个和可能占用大量内存，元素和也可能溢出 `int`。
2. `upper_bound(x)` 指向第一个大于 `x` 的值，取可行值前必须先判断是否为 `begin()`。
3. 分组范围统一使用左闭右开，避免漏掉或重复中点元素。

**参考：**

- [OI Wiki：双向搜索 / Meet in the middle](https://oi-wiki.org/search/bidirectional/)

## 3.12 0-1 BFS

**用途与复杂度。** 边权只取 0 或 1 的单源最短路可用双端队列在线处理：松弛到 0 边的新点放队首，1 边放队尾。时间 $O(n+m)$，空间 $O(n)$；一般非负边权应使用 Dijkstra。

**思路与用法。** 邻接表按 1-based 点编号，权值必须是 0 或 1。队列允许同一顶点多次入队；每次弹出时用当前最短距离松弛邻边。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge01 {
    int to;
    int weight; // 必须为 0 或 1
};

vector<int> zeroOneBfs(int n, const vector<vector<Edge01>>& graph, int source) {
    const int INF = numeric_limits<int>::max() / 4;
    vector<int> dist(n + 1, INF); // 点编号 1..n；不可达保持 INF
    deque<int> work;
    dist[source] = 0;
    work.push_front(source);

    while (!work.empty()) {
        int u = work.front();
        work.pop_front();
        for (const Edge01& edge : graph[u]) {
            int candidate = dist[u] + edge.weight;
            if (candidate >= dist[edge.to]) continue;
            dist[edge.to] = candidate;
            // 0 权边不增加距起点的层数，优先处理；1 权边排在后面。
            if (edge.weight == 0) work.push_front(edge.to);
            else work.push_back(edge.to);
        }
    }
    return dist;
}
```

**易错点。** 权值出现 2 或负数时该策略不再保证最短路；只在松弛成功后入队；不要在入队时永久标记 visited，因为后续可能找到更短距离。
