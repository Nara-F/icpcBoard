
# 5. 数据结构

本章代码默认使用 C++17。除特别说明外，数组下标从 1 开始；调用查询、删除操作前应保证容器非空、区间合法。字典树统一收录在第 8 章字符串中。

## 5.1 栈与队列

**问题与思路：** 栈按“后进先出”处理括号、递归展开和撤销；队列按“先进先出”处理分层扩展与任务调度。`push`、`pop`、访问栈顶或队首均为 $O(1)$，存储 $k$ 个元素需 $O(k)$ 空间。删除或读取前必须判空；需要两端操作时改用 `deque`。

**用法：**

- `stack` 只访问 `top()`；`queue` 访问 `front()`，也可查看 `back()`。
- `pop()` 不返回元素，应先读取再弹出。
- `empty()` 判空，`size()` 返回当前元素数。
- 需要从两端插入、删除时使用 `deque` 的 `push_front`、`push_back`、`pop_front`、`pop_back`。

```cpp
#include <bits/stdc++.h>
using namespace std;

void stackQueueExample(const vector<int>& a) {
    // 适配器不暴露迭代器；以下循环都先读顶端/队首，再 pop。
    stack<int> st;
    for (int x : a) st.push(x); // 入栈顺序与 a 相同，弹出顺序因此相反
    while (!st.empty()) {
        int x = st.top();
        st.pop();
        (void)x;  // 在此处理：顺序与 a 相反
    }

    queue<int> q;
    for (int x : a) q.push(x); // 队列按到达顺序服务
    while (!q.empty()) {
        int x = q.front();
        q.pop();
        (void)x;  // 在此处理：顺序与 a 相同
    }

    deque<int> dq;
    dq.push_front(1);
    dq.push_back(2);
    if (!dq.empty()) dq.pop_front();
}
```

**易错点：**

1. 对空容器调用 `top()`、`front()`、`back()` 或 `pop()` 是未定义行为。
2. `stack`、`queue` 默认不支持随机访问和遍历。
3. 深度优先搜索改写为显式栈时，入栈顺序会影响访问顺序。

**参考：**

- [OI Wiki：栈](https://oi-wiki.org/ds/stack/)
- [OI Wiki：队列](https://oi-wiki.org/ds/queue/)

## 5.2 单调栈

**问题与思路：** 求每个位置左/右侧第一个更大或更小元素时使用。扫描数组，栈内保存仍未找到答案的下标，并保持对应值单调；新元素使栈顶确定答案时不断弹出。每个下标至多进出栈一次，时间 $O(n)$、空间 $O(n)$。等号是否弹出决定“严格”还是“不严格”。

**用法：**

- 模板返回每个位置右侧第一个严格更小元素的下标，不存在为 `-1`。
- 栈保存下标，既能取值也能计算距离。
- 改求右侧第一个严格更大：把弹出条件改为 `a[i] > a[st.top()]`。
- 若求“小于等于”，相应把 `<` 改为 `<=`。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> firstSmallerOnRight(const vector<int>& a) {
    // a 与答案均为 0-based；answer[i] 是右侧首个严格更小值的下标。
    int n = (int)a.size();
    vector<int> answer(n, -1);
    stack<int> st;  // 栈中下标递增，且对应值从栈底到栈顶单调不减

    for (int i = 0; i < n; ++i) {
        // 严格更小才弹；改成 <= 即改为“右侧首个小于等于”。
        while (!st.empty() && a[i] < a[st.top()]) {
            answer[st.top()] = i;
            st.pop();
        }
        st.push(i);
    }
    return answer;
}
```

**易错点：**

1. 必须先明确答案是否允许相等，错误的等号会改变重复值的答案。
2. 求距离时使用 `answer[i] - i`，不存在的 `-1` 要单独处理。
3. 栈内通常保存下标而非数值，否则无法定位答案。

**参考：**

- [OI Wiki：单调栈](https://oi-wiki.org/ds/monotonous-stack/)

## 5.3 单调队列

**问题与思路：** 用于固定长度滑动窗口最值，也可优化形如“某段范围内取最优”的 DP。双端队列保存候选下标：队首过期就弹出，队尾不可能成为最优就弹出。每个下标至多进出一次，时间 $O(n)$、空间 $O(k)$。模板求长度为 $k$ 的窗口最小值。

**用法：**

- 返回数组长度为 `n-k+1`，第 `i` 项对应区间 `[i,i+k-1]`。
- 队列必须保存下标，才能判断元素是否离开窗口。
- 求最大值时把维护条件 `>=` 改为 `<=`。
- 本模板保留更靠右的相等元素，使其有效期更长。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> slidingWindowMinimum(const vector<int>& a, int k) {
    // a 为 0-based；每个答案对应闭区间 [i-k+1, i]。
    int n = (int)a.size();
    vector<int> answer;
    if (k <= 0 || k > n) return answer;

    // dq 保存候选下标：下标递增，对应值严格递增，队首永远是窗口最小值。
    deque<int> dq;
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();  // 移出窗口
        // 相等也弹出旧下标，保留有效期更长的新下标；求最大值时反转不等号。
        while (!dq.empty() && a[dq.back()] >= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) answer.push_back(a[dq.front()]);
    }
    return answer;
}
```

**易错点：**

1. 应先删除过期下标，再读取队首答案。
2. 队列单调的是对应值，队列中的下标始终递增。
3. 窗口长度不合法时不能直接访问队首。

**参考：**

- [OI Wiki：单调队列](https://oi-wiki.org/ds/monotonous-queue/)

## 5.4 堆与优先队列

**问题与思路：** 堆动态维护当前最大或最小元素，适合 Dijkstra、贪心调度和 Top-K。C++ `priority_queue` 默认大根堆；插入、删除堆顶为 $O(\log n)$，读取堆顶 $O(1)$，建堆 $O(n)$，空间 $O(n)$。它不能高效删除任意元素，常用“重复插入并跳过失效记录”。

**用法：**

- 大根堆：`priority_queue<int>`；小根堆见模板。
- 自定义状态常以 `pair<距离,点>` 配合 `greater`，按字典序取最小。
- `pop()` 不返回值，先用 `top()` 保存。
- 无法直接修改堆内元素；更新后重新 `push`，弹出时验证状态是否仍有效。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> heapOrder(const vector<int>& a) {
    // greater<int> 使 top() 为当前最小值；若去掉则默认是大根堆。
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int x : a) minHeap.push(x);

    vector<int> sorted;
    while (!minHeap.empty()) {
        sorted.push_back(minHeap.top());
        minHeap.pop();
    }
    return sorted;
}
```

**易错点：**

1. `priority_queue` 默认取最大值，求最小时不要忘记 `greater<T>`。
2. 自定义类型需提供比较规则，比较器含义与 `sort` 容易混淆。
3. 使用懒删除时，堆的实际大小可能远大于有效元素数。

**参考：**

- [OI Wiki：堆](https://oi-wiki.org/ds/heap/)

## 5.5 并查集

**问题与思路：** 维护元素不断合并后的连通关系，适合 Kruskal、离线连通性和等价类。每个集合用根代表；路径压缩加按大小合并，使单次查询或合并均摊 $O(\alpha(n))$，初始化和空间均为 $O(n)$。普通并查集不支持拆分，也不能直接维护集合内的路径信息。

**用法：**

- 构造 `DSU dsu(n)`，管理编号 `1..n`。
- `find(x)` 返回集合代表元，同时压缩路径。
- `unite(a,b)` 合并成功返回 `true`；已经连通返回 `false`。
- `same(a,b)` 判断连通，`size(x)` 查询所在集合大小。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    // parent[x] 指向父节点；仅根满足 parent[x]==x，且只有根的 sizeOf 有效。
    vector<int> parent, sizeOf;

    explicit DSU(int n) : parent(n + 1), sizeOf(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] == x) return x;
        // 路径压缩保持集合不变，只把查询路径上的点直接挂到根。
        return parent[x] = find(parent[x]);
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sizeOf[a] < sizeOf[b]) swap(a, b);  // 始终把小树挂到大树
        parent[b] = a;
        sizeOf[a] += sizeOf[b];
        return true;
    }

    // 所有公开查询都先压到根，避免调用方误把非根当代表。
    bool same(int a, int b) { return find(a) == find(b); }
    int size(int x) { return sizeOf[find(x)]; }
};
```

**易错点：**

1. 按大小合并时，集合大小只在根节点处有效。
2. 若题目需要撤销合并，不能使用普通路径压缩并查集。
3. 合并前必须先取根，不能直接修改 `parent[a]`。

**参考：**

- [OI Wiki：并查集](https://oi-wiki.org/ds/dsu/)

## 5.6 树状数组

**问题与思路：** 维护可加减信息的单点修改与前缀查询，常用于动态区间和、逆序对。下标 `x` 通过 `x & -x` 跳到负责区间；单点加、前缀和及区间和均为 $O(\log n)$，建表通常 $O(n\log n)$，空间 $O(n)$。基础模板不直接支持区间最值或任意区间赋值。

**用法：**

- 构造 `Fenwick fw(n)`，有效下标为 `1..n`，不能向下标 0 更新。
- `add(i,delta)` 表示第 `i` 项增加 `delta`。
- `prefixSum(i)` 查询 `[1,i]`，`rangeSum(l,r)` 查询 `[l,r]`。
- 单点赋值需先知道旧值，再增加“新值减旧值”。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Fenwick {
    int n;
    // 仅使用 1..n；tree[i] 保存 (i-lowbit(i), i] 这一段的和。
    vector<ll> tree;

    explicit Fenwick(int n) : n(n), tree(n + 1, 0) {}

    void add(int index, ll delta) {
        // index 必须 >=1；向父区间跳转，直到超过 n。
        for (int i = index; i <= n; i += i & -i) tree[i] += delta;
    }

    ll prefixSum(int index) const {
        // 查询闭区间 [1,index]；每次删掉当前下标最低位的 1。
        ll result = 0;
        for (int i = index; i > 0; i -= i & -i) result += tree[i];
        return result;
    }

    ll rangeSum(int left, int right) const {
        if (left > right) return 0;
        return prefixSum(right) - prefixSum(left - 1);
    }

    // 频次数组非负时，返回最小 i 使 prefixSum(i)>=target；无解返回 n+1。
    int lowerBound(ll target) const {
        int index = 0;
        ll accumulated = 0;
        int step = 1;
        while ((step << 1) <= n) step <<= 1;
        // 二进制提升：index 始终是“前缀和仍小于 target”的最大已知下标。
        for (; step; step >>= 1) {
            int next = index + step;
            if (next <= n && accumulated + tree[next] < target) {
                index = next;
                accumulated += tree[next];
            }
        }
        return index + 1;
    }
};
```

**易错点：**

1. 更新下标必须大于 0，否则 `i += i & -i` 会死循环。
2. 区间和是 `prefixSum(r)-prefixSum(l-1)`。
3. 值和答案可能超过 `int`，树数组优先使用 `long long`。
4. `lowerBound` 要求单点频次非负，目标大于总和时返回 `n+1`。

**参考：**

- [OI Wiki：树状数组](https://oi-wiki.org/ds/fenwick/)

## 5.7 线段树（区间加、区间和）

**问题与思路：** 维护数组的区间修改与区间查询。节点保存区间和，整段增加时记录懒标记，访问子区间前再下传。建树 $O(n)$，每次区间加或区间和查询 $O(\log n)$，空间 $O(n)$（通常开 `4n`）。模板要求修改可组合；改维护最值时需同步修改合并与标记逻辑。

**用法：**

- 输入数组 `a` 使用下标 `1..n`，构造后调用 `build(a)`。
- `rangeAdd(l,r,delta)` 令区间内每项增加 `delta`。
- `rangeSum(l,r)` 返回区间和，内部自动下传懒标记。
- 若只需单点修改，可调用 `rangeAdd(i,i,delta)`。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SegmentTree {
    int n;
    // 节点 p 管理闭区间 [left,right]。
    // sum[p] 已含本节点全部修改；lazy[p] 表示尚未下传给子节点的“每项增量”。
    vector<ll> sum, lazy;

    explicit SegmentTree(int n) : n(n), sum(4 * n + 4), lazy(4 * n + 4) {}

    void build(const vector<ll>& a, int p, int left, int right) {
        // 输入 a 使用 1-based；递归区间始终是闭区间。
        if (left == right) {
            sum[p] = a[left];
            return;
        }
        int mid = (left + right) / 2;
        build(a, p * 2, left, mid);
        build(a, p * 2 + 1, mid + 1, right);
        sum[p] = sum[p * 2] + sum[p * 2 + 1];
    }

    void build(const vector<ll>& a) { build(a, 1, 1, n); }

    void apply(int p, int left, int right, ll delta) {
        // 整段每项增加 delta，所以区间和增加 delta * 区间长度。
        sum[p] += delta * (right - left + 1);
        lazy[p] += delta;
    }

    void pushDown(int p, int left, int right) {
        if (lazy[p] == 0 || left == right) return;
        int mid = (left + right) / 2;
        // 下传必须使用子区间真实长度；完成后清空父标记，避免重复应用。
        apply(p * 2, left, mid, lazy[p]);
        apply(p * 2 + 1, mid + 1, right, lazy[p]);
        lazy[p] = 0;
    }

    void rangeAdd(int ql, int qr, ll delta, int p, int left, int right) {
        // ql,qr 是待修改闭区间；调用前保证它合法且与当前区间有交集。
        if (ql <= left && right <= qr) {
            apply(p, left, right, delta);
            return;
        }
        pushDown(p, left, right);
        int mid = (left + right) / 2;
        if (ql <= mid) rangeAdd(ql, qr, delta, p * 2, left, mid);
        if (qr > mid) rangeAdd(ql, qr, delta, p * 2 + 1, mid + 1, right);
        // 子树修改后回收信息，保持 sum[p] 等于整个 [left,right] 的和。
        sum[p] = sum[p * 2] + sum[p * 2 + 1];
    }

    void rangeAdd(int left, int right, ll delta) {
        rangeAdd(left, right, delta, 1, 1, n);
    }

    ll rangeSum(int ql, int qr, int p, int left, int right) {
        // 完全覆盖直接返回；部分覆盖前先下传，保证子节点信息最新。
        if (ql <= left && right <= qr) return sum[p];
        pushDown(p, left, right);
        int mid = (left + right) / 2;
        ll result = 0;
        if (ql <= mid) result += rangeSum(ql, qr, p * 2, left, mid);
        if (qr > mid) result += rangeSum(ql, qr, p * 2 + 1, mid + 1, right);
        return result;
    }

    ll rangeSum(int left, int right) {
        return rangeSum(left, right, 1, 1, n);
    }
};
```

**易错点：**

1. 区间和增加量是 `delta * 区间长度`，不是只加 `delta`。
2. 访问子节点前必须下传标记；下传后清空父标记。
3. `n=0` 时不能建树；调用区间必须满足 `1<=l<=r<=n`。
4. 区间赋值与区间加法的标记组合不同，不能直接混用此模板。

**参考：**

- [OI Wiki：线段树](https://oi-wiki.org/ds/seg/)

## 5.8 ST 表（静态 RMQ）

**问题与思路：** 静态数组上反复查询区间最大/最小值时使用。预处理每个起点、长度为 $2^j$ 的答案；查询 `[l,r]` 用两个可重叠的同长度区间合并。预处理 $O(n\log n)$、查询 $O(1)$、空间 $O(n\log n)$。仅适合可重复贡献的运算，如最大、最小、GCD；数组不能修改。

**用法：**

- 模板维护最大值，输入数组下标为 `1..n`。
- `query(l,r)` 要求 `1<=l<=r<=n`。
- 改最小值：将两处 `max` 改为 `min`。
- 区间和不可用重叠区间合并，应使用前缀和、树状数组或线段树。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SparseTableMax {
    int n, levels;
    vector<int> log2Floor;
    // st[j][i] 保存闭区间 [i, i+2^j-1] 的最大值；输入 a 为 1-based。
    vector<vector<int>> st;

    explicit SparseTableMax(const vector<int>& a) {
        n = (int)a.size() - 1;
        log2Floor.assign(n + 1, 0);
        // log2Floor[i] = floor(log2(i))，查询时可 O(1) 找到覆盖长度。
        for (int i = 2; i <= n; ++i) log2Floor[i] = log2Floor[i / 2] + 1;

        levels = log2Floor[n] + 1;
        st.assign(levels, vector<int>(n + 1));
        for (int i = 1; i <= n; ++i) st[0][i] = a[i];

        for (int j = 1; j < levels; ++j) {
            int length = 1 << j;
            for (int i = 1; i + length - 1 <= n; ++i) {
                // 长为 2^j 的区间由两个相邻、长为 2^(j-1) 的区间组成。
                st[j][i] = max(st[j - 1][i], st[j - 1][i + length / 2]);
            }
        }
    }

    int query(int left, int right) const {
        // max 可重复贡献：用两个可能重叠的 2^j 区间覆盖 [left,right]。
        int j = log2Floor[right - left + 1];
        return max(st[j][left], st[j][right - (1 << j) + 1]);
    }
};
```

**易错点：**

1. 构造函数要求至少有一个有效元素，且 `a[0]` 不使用。
2. 第二段起点是 `r-2^j+1`，容易漏掉 `+1`。
3. ST 表建成后不能修改原数组。

**参考：**

- [OI Wiki：ST 表](https://oi-wiki.org/ds/sparse-table/)


## 5.9 分块（区间加、区间和）

**问题与思路：** 将数组按约 $\sqrt n$ 个元素分块，整块用汇总值和懒标记处理，零散部分直接扫描。适合操作容易整块维护、又不想写线段树的题。模板区间加与区间和均为 $O(\sqrt n)$，建表与空间 $O(n)$；常数较小但渐进复杂度弱于线段树。

**用法：**

- 输入数组下标为 `1..n`，构造 `SqrtDecomposition ds(a)`。
- `rangeAdd(l,r,delta)` 对闭区间加值。
- `rangeSum(l,r)` 查询闭区间和。
- `sum[b]` 保存原始数组在整块的和，`lazy[b]` 保存整块每项额外增加量。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SqrtDecomposition {
    int n, blockSize, blockCount;
    // value[i] 与 sum[b] 均不含 lazy[b]；真实值为 value[i]+lazy[belong[i]]。
    vector<ll> value, sum, lazy;
    // belong 映射 1-based 下标到 0-based 块；块端点均为闭区间。
    vector<int> belong, leftEnd, rightEnd;

    explicit SqrtDecomposition(const vector<ll>& a) {
        // 输入 a[1..n]，a[0] 不使用；要求 n>=1。
        n = (int)a.size() - 1;
        blockSize = max(1, (int)sqrt(n));
        blockCount = (n + blockSize - 1) / blockSize;
        value = a;
        sum.assign(blockCount, 0);
        lazy.assign(blockCount, 0);
        belong.resize(n + 1);
        leftEnd.resize(blockCount);
        rightEnd.resize(blockCount);

        for (int b = 0; b < blockCount; ++b) {
            leftEnd[b] = b * blockSize + 1;
            rightEnd[b] = min(n, (b + 1) * blockSize);
            for (int i = leftEnd[b]; i <= rightEnd[b]; ++i) {
                belong[i] = b;
                sum[b] += value[i];
            }
        }
    }

    void rangeAdd(int left, int right, ll delta) {
        // 修改闭区间 [left,right]：散块写 value/sum，完整块只累加 lazy。
        int bl = belong[left], br = belong[right];
        if (bl == br) {
            for (int i = left; i <= right; ++i) value[i] += delta;
            sum[bl] += delta * (right - left + 1);
            return;
        }
        for (int i = left; i <= rightEnd[bl]; ++i) value[i] += delta;
        sum[bl] += delta * (rightEnd[bl] - left + 1);
        for (int b = bl + 1; b < br; ++b) lazy[b] += delta;  // 不改原始块和
        for (int i = leftEnd[br]; i <= right; ++i) value[i] += delta;
        sum[br] += delta * (right - leftEnd[br] + 1);
    }

    ll rangeSum(int left, int right) const {
        // 查询闭区间 [left,right]；散块逐项补 lazy，整块一次补标记贡献。
        int bl = belong[left], br = belong[right];
        ll result = 0;
        if (bl == br) {
            for (int i = left; i <= right; ++i) result += value[i] + lazy[bl];
            return result;
        }
        for (int i = left; i <= rightEnd[bl]; ++i) result += value[i] + lazy[bl];
        for (int b = bl + 1; b < br; ++b) {
            result += sum[b] + lazy[b] * (rightEnd[b] - leftEnd[b] + 1);
        }
        for (int i = leftEnd[br]; i <= right; ++i) result += value[i] + lazy[br];
        return result;
    }
};
```

**易错点：**

1. 整块懒标记没有写回 `value`，扫描零散元素时必须额外加上本块标记。
2. `sum` 只保存不含 `lazy` 的块内原值和，查询整块时再计算标记贡献。
3. 最后一块长度可能不足 `blockSize`，应使用实际左右端点。

**参考：**

- [OI Wiki：分块](https://oi-wiki.org/ds/decompose/)


## 5.10 树状数组：区间加与区间和

用两棵树维护差分：前缀和为 `x*sum(B1,x)-sum(B2,x)`；区间修改/查询均 $O(\log n)$。本代码复用 5.6 节的 `Fenwick`（`add` 与 `prefixSum`）。

```cpp
struct RangeFenwick {
    // 两棵树保存差分系数，prefix(x)=x*B1.prefix-B2.prefix。
    int n;
    Fenwick b1,b2;
    explicit RangeFenwick(int size) : n(size), b1(size), b2(size) {}
    void addPoint(int x, ll v) {
        // 差分在 l 加 v、在 r+1 减 v；n+1 的哨兵不需要写入树中。
        if (x <= n) {
            b1.add(x, v);
            b2.add(x, v * (x - 1));
        }
    }
    void addRange(int l, int r, ll v) {
        if (l > r) {
            return;
        }
        addPoint(l, v);
        addPoint(r + 1, -v);
    }
    ll prefix(int x) const {
        return b1.prefixSum(x) * x - b2.prefixSum(x);
    }
    ll query(int l, int r) const {
        return l > r ? 0 : prefix(r) - prefix(l - 1);
    }
};
```

坑：初始数组可逐点 `addRange(i,i,a[i])`；乘法必须用 `long long`；`r+1` 超界时不更新。

## 5.11 DFS 序与子树展平

**用途 / 用法：** 把有根树的子树映射为连续区间 `[tin[u],tout[u]]`，再接树状数组/线段树；预处理 $O(n)$。

```cpp
struct DfsOrder {
    vector<vector<int>> g;
    vector<int> tin,tout,order;
    int timer=0;
    explicit DfsOrder(int n)
        : g(n + 1), tin(n + 1), tout(n + 1), order(n + 1) {}
    void addEdge(int u, int v) {
        g[u].push_back(v);
        g[v].push_back(u);
    }
    void dfs(int u, int p) {
        // 进入时分配唯一时间戳，递归结束时的 timer 即子树最后一个时间戳。
        tin[u] = ++timer;
        order[timer] = u;
        for (int v : g[u]) {
            if (v != p) {
                dfs(v, u);
            }
        }
        tout[u] = timer;
    }
};
```

坑：这是每点只记录一次的 DFS 序，不是 LCA 欧拉序；换根后“子树”含义变化；深链注意栈深。

## 5.12 树链剖分

**用途 / 用法：** 把树上路径拆成 $O(\log n)$ 个连续 DFS 区间；配合线段树后路径查询通常 $O(\log^2 n)$。

```cpp
struct HLD {
    // heavy 子树最大者优先同链；任意树路径被拆成 O(log n) 个连续区间。
    int n,timer=0;
    vector<vector<int>> g;
    vector<int> parent,depth,sz,heavy,top,pos;
    explicit HLD(int nodeCount)
        : n(nodeCount), g(nodeCount + 1), parent(nodeCount + 1),
          depth(nodeCount + 1), sz(nodeCount + 1),
          heavy(nodeCount + 1, -1), top(nodeCount + 1), pos(nodeCount + 1) {}
    int dfs1(int u, int p) {
        // 后序汇总子树大小，并选出最大的孩子作为重儿子。
        parent[u] = p;
        sz[u] = 1;
        int best = 0;
        for (int v : g[u]) {
            if (v == p) {
                continue;
            }
            depth[v] = depth[u] + 1;
            int sub = dfs1(v, u);
            sz[u] += sub;
            if (sub > best) {
                best = sub;
                heavy[u] = v;
            }
        }
        return sz[u];
    }
    void dfs2(int u, int head) {
        // 重儿子先访问以保证同一重链映射为连续位置。
        top[u] = head;
        pos[u] = ++timer;
        if (heavy[u] != -1) {
            dfs2(heavy[u], head);
        }
        for (int v : g[u]) {
            if (v != parent[u] && v != heavy[u]) {
                dfs2(v, v);
            }
        }
    }
    void build(int root = 1) {
        dfs1(root, 0);
        dfs2(root, root);
    }
    template<class F>
    void forPath(int u, int v, F use) { // use(l,r): 点权区间
        while (top[u] != top[v]) {
            if (depth[top[u]] < depth[top[v]]) {
                swap(u, v);
            }
            use(pos[top[u]], pos[u]);
            u = parent[top[u]];
        }
        if (depth[u] > depth[v]) {
            swap(u, v);
        }
        use(pos[u], pos[v]);
    }
};
```

坑：边权映射到较深端点，最后同链区间应排除 LCA；非交换操作要保留路径方向；记得先向 `g` 加边再 `build`。

## 5.13 线段树：区间加、赋值与求和

**用途 / 用法：** 同时支持区间加、区间赋值与区间和，每次操作 $O(\log n)$。赋值覆盖旧加法；赋值之后的新加法累加到赋值值上。以下代码与 5.7 节的区间加树用途相近，但懒标记额外维护覆盖操作。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct AssignAddSegmentTree {
    struct Node {
        ll sum = 0;
        ll add = 0;
        ll setValue = 0;
        bool hasSet = false; // 赋值为 0 也有效，不能用 setValue==0 表示“无标记”
    };
    int n;
    vector<Node> tr;

    explicit AssignAddSegmentTree(int size) : n(size), tr(4 * size + 4) {}

    void applySet(int p, int l, int r, ll value) {
        // 覆盖整个节点：清除旧加法，并留下待下传的赋值。
        tr[p].sum = value * (r - l + 1);
        tr[p].setValue = value;
        tr[p].add = 0;
        tr[p].hasSet = true;
    }
    void applyAdd(int p, int l, int r, ll delta) {
        tr[p].sum += delta * (r - l + 1);
        // 赋值标记仍在时把增量合并到赋值值，否则累积为独立加法标记。
        if (tr[p].hasSet) tr[p].setValue += delta;
        else tr[p].add += delta;
    }
    void push(int p, int l, int r) {
        if (l == r) return;
        int m = (l + r) / 2;
        // 操作顺序必须是先赋值后加法，才能保持时间顺序。
        if (tr[p].hasSet) {
            applySet(p * 2, l, m, tr[p].setValue);
            applySet(p * 2 + 1, m + 1, r, tr[p].setValue);
            tr[p].hasSet = false;
        }
        if (tr[p].add != 0) {
            applyAdd(p * 2, l, m, tr[p].add);
            applyAdd(p * 2 + 1, m + 1, r, tr[p].add);
            tr[p].add = 0;
        }
    }
    void build(int p, int l, int r, const vector<ll>& a) {
        if (l == r) {
            tr[p].sum = a[l];
            return;
        }
        int m = (l + r) / 2;
        build(p * 2, l, m, a);
        build(p * 2 + 1, m + 1, r, a);
        tr[p].sum = tr[p * 2].sum + tr[p * 2 + 1].sum;
    }
    void build(const vector<ll>& a) { build(1, 1, n, a); }

    void update(int p, int l, int r, int ql, int qr, ll value, bool assign) {
        if (ql <= l && r <= qr) {
            if (assign) applySet(p, l, r, value);
            else applyAdd(p, l, r, value);
            return;
        }
        push(p, l, r);
        int m = (l + r) / 2;
        if (ql <= m) update(p * 2, l, m, ql, qr, value, assign);
        if (qr > m) update(p * 2 + 1, m + 1, r, ql, qr, value, assign);
        tr[p].sum = tr[p * 2].sum + tr[p * 2 + 1].sum;
    }
    void rangeAdd(int l, int r, ll value) { update(1, 1, n, l, r, value, false); }
    void rangeSet(int l, int r, ll value) { update(1, 1, n, l, r, value, true); }

    ll query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[p].sum;
        push(p, l, r);
        int m = (l + r) / 2;
        ll result = 0;
        if (ql <= m) result += query(p * 2, l, m, ql, qr);
        if (qr > m) result += query(p * 2 + 1, m + 1, r, ql, qr);
        return result;
    }
    ll rangeSum(int l, int r) { return query(1, 1, n, l, r); }
};
```

构造 `AssignAddSegmentTree st(n)` 后，用 `build(a)` 初始化 `a[1..n]`；`rangeSet(l,r,v)` 赋值，`rangeAdd(l,r,v)` 增加，`rangeSum(l,r)` 求和。要求 `n>=1`、区间合法，且乘积和节点和均能放入 `long long`。
