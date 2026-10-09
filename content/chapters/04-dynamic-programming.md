# 4. 动态规划

## 4.1 DP 入门：状态、转移与顺序

**适用范围：** 存在按依赖顺序计算的状态时适用；复杂度为状态数乘转移数。输入状态定义与初值，输出目标状态值；必须说明不可达初值及计算顺序。
**能做什么：** 计算不相邻选数的最大和并恢复一组下标。
**输入 / 输出：** 输入 value[1..n]；返回 maximumSum 与 1-based chosenIndices，允许空选，故全负答案为 0。
**复杂度：** 状态数 × 转移数.

**用途：** 动态规划适合具有最优子结构和重复子问题的计数、可行性或最优化问题。先定义状态含义，再写转移、初值和计算顺序；每个状态只算一次。若状态数为 $S$、每个状态枚举 $T$ 个转移，时间 $O(ST)$、空间 $O(S)$，可按依赖关系滚动压缩。

**思路：**

- 明确写出 `dp[i]` 表示什么，未定义状态不要参与转移。
- 初值对应最小子问题；求最小值时其余状态常设为无穷大。
- 递推顺序必须保证依赖状态已算出；不易确定时可先写记忆化搜索。
- 模板示例为线上选数：选出的下标不能相邻，允许一个都不选。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct LineDPResult {
    ll maximumSum;
    vector<int> chosenIndices; // 1-based
};

// 参数：value[1..n] 的 long long 权值。返回：最大和与一组 1-based 互不相邻下标；允许空选。效果：O(n) 时间、空间。
LineDPResult maximumNonAdjacentSum(const vector<ll>& value) {
    // value 使用 1-based；dp[i] 表示前 i 个位置允许空选时的最大和。
    int n = static_cast<int>(value.size()) - 1; // value[1..n]
    vector<ll> dp(n + 1, 0);
    if (n >= 1) dp[1] = max(0LL, value[1]);
    for (int i = 2; i <= n; ++i) {
        // 不选 i 继承 dp[i-1]；选 i 时前一个可选前缀只能到 i-2。
        dp[i] = max(dp[i - 1], dp[i - 2] + value[i]);
    }

    vector<int> chosen;
    // 从 dp[n] 逆推一组最优下标；相等时固定选择“不取 i”。
    for (int i = n; i >= 1;) {
        if (i == 1) {
            if (dp[i] > 0) chosen.push_back(1);
            break;
        }
        if (dp[i] == dp[i - 1]) {
            --i;
        } else {
            chosen.push_back(i);
            i -= 2;
        }
    }
    reverse(chosen.begin(), chosen.end());
    return {dp[n], chosen};
}
```

**易错点：**

1. 状态含义必须固定，例如“前 `i` 个”与“恰好以 `i` 结尾”不可混用。
2. 求最小值时未到达状态不能初始化为 0，否则会产生虚假转移。
3. 空间压缩后往往无法直接恢复方案，需要保留前驱或完整 DP 表。

**参考：**

- [OI Wiki：动态规划基础](https://oi-wiki.org/dp/basic/)
- [OI Wiki：记忆化搜索](https://oi-wiki.org/dp/memo/)

## 4.2 0-1 背包

**适用范围：** 每件物品最多取一次的容量优化；时间 O(nC)。输入重量/价值与容量 C，输出最大价值；非负重量且 C 可分配，压缩数组时容量倒序。
**能做什么：** 求容量不超过 C 的 0-1 背包值，或可选 exact 版本求恰好装满。
**输入 / 输出：** 输入平行的 0-based 重量/价值数组及容量；返回最大价值；exact 版无法恰好装满时返回空 optional。
**复杂度：** O(nC).

**用途：** 有 $n$ 件物品，每件至多选一次，求容量不超过 $W$ 时的最大价值。令 `dp[j]` 为容量上限为 `j` 的最大价值；处理物品时容量必须倒序，避免同一物品重复使用。时间 $O(nW)$、空间 $O(W)$，适合容量不大且重量为非负整数的题目。

**思路：**

- `weight[i]`、`value[i]` 均按 `0..n-1` 存储。
- 本模板求“总重量不超过容量”的最大价值，允许不装满。
- 若要求恰好装满，除 `dp[0]=0` 外应初始化为负无穷，并跳过不可达状态。
- 只问可行性时可用 `vector<char>`，转移为逻辑或。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：平行的重量/价值数组与容量；每件至多取一次。返回：不超过容量的最大价值。效果：O(nC)，要求容量非负。
ll zeroOneKnapsack(const vector<int>& weight,
                   const vector<ll>& value,
                   int capacity) {
    // 物品为 0-based；dp[j] 表示总重量不超过 j 的最大价值。
    vector<ll> dp(capacity + 1, 0);
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        // 容量倒序保证右侧 dp[j-weight[i]] 尚未使用当前物品。
        for (int j = capacity; j >= weight[i]; --j) {
            dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
        }
    }
    return dp[capacity];
}

// 恰好装满时的最大价值；不可达返回 nullopt。
// 参数：平行的重量/价值数组及非负容量；每件至多取一次。返回：恰好装满的最大价值，无解为空。效果：O(nC)。
optional<ll> exactZeroOneKnapsack(const vector<int>& weight,
                                  const vector<ll>& value,
                                  int capacity) {
    const ll NEG_INF = numeric_limits<ll>::lowest() / 4;
    // 除 dp[0] 外均不可达，因而该版本要求最终重量恰好为 capacity。
    vector<ll> dp(capacity + 1, NEG_INF);
    dp[0] = 0;
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        for (int j = capacity; j >= weight[i]; --j) {
            // 不可达状态不能参与加法，否则会制造不存在的方案。
            if (dp[j - weight[i]] != NEG_INF) {
                dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
            }
        }
    }
    if (dp[capacity] == NEG_INF) return nullopt;
    return dp[capacity];
}
```

**易错点：**

1. 0-1 背包容量必须倒序；正序会把一件物品使用多次。
2. “不超过容量”与“恰好装满”的初始化不同。
3. 重量为 0 且价值为正时仍只能选一次，倒序模板可正确处理。

**参考：**

- [OI Wiki：背包 DP](https://oi-wiki.org/dp/knapsack/)

## 4.3 完全背包与多重背包

**适用范围：** 完全背包允许每件任取次数，多重背包有数量上限；前者 O(nC)，后者二进制拆分 O(CΣlog count)。输入物品与容量，输出最优值；循环方向决定取用次数语义。
**能做什么：** 求完全背包或有限数量多重背包最大价值。
**输入 / 输出：** 输入平行重量/价值/数量数组及容量；返回最大价值；完全背包每件可无限取。
**复杂度：** O(nC) 或 O(CΣlog count).

**用途：** 完全背包中每件物品可选无限次，容量正序转移；多重背包限制第 $i$ 件最多选 $c_i$ 次，可按二进制拆成 $O(\log c_i)$ 件 0-1 物品。完全背包时间 $O(nW)$；二进制多重背包时间 $O(W\sum\log c_i)$，空间均为 $O(W)$。

**思路：**

- 两个模板都求容量不超过 `capacity` 的最大价值，允许留空。
- 完全背包要求正重量；零重量正价值且可无限选会导致答案无界。
- 多重背包将数量拆为 `1,2,4,...,剩余`，再按 0-1 背包倒序。
- 容量很大而总价值较小时，可改用“价值为状态、重量为代价”的 DP。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：平行重量/价值数组与容量；每件可无限取。返回：不超过容量的最大价值。效果：O(nC)，重量须为正。
ll completeKnapsack(const vector<int>& weight,
                    const vector<ll>& value,
                    int capacity) {
    // weight 必须为正；dp[j] 表示容量上限为 j 的最大价值。
    vector<ll> dp(capacity + 1, 0);
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        // 正序使 dp[j-weight[i]] 可含当前物品，从而允许重复选择。
        for (int j = weight[i]; j <= capacity; ++j) {
            dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
        }
    }
    return dp[capacity];
}

// 参数：重量、价值、数量上限数组与容量。返回：不超过容量的最大价值。效果：二进制拆分，O(CΣlog count)。
ll multipleKnapsack(const vector<int>& weight,
                    const vector<ll>& value,
                    const vector<int>& count,
                    int capacity) {
    // 每个二进制组视为一件只能选择一次的 0-1 物品。
    vector<pair<int, ll>> items;
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        int remaining = count[i];
        for (int group = 1; remaining > 0; group <<= 1) {
            // 最后一组取全部 remaining，确保拆分数量之和恰为 count[i]。
            int take = min(group, remaining);
            items.push_back({weight[i] * take, value[i] * take});
            remaining -= take;
        }
    }

    vector<ll> dp(capacity + 1, 0);
    for (auto [groupWeight, groupValue] : items) {
        // 拆分后的每组只能使用一次，因此容量必须倒序。
        for (int j = capacity; j >= groupWeight; --j) {
            dp[j] = max(dp[j], dp[j - groupWeight] + groupValue);
        }
    }
    return dp[capacity];
}
```

**易错点：**

1. 完全背包正序、0-1 背包倒序；顺序写反会改变物品可用次数。
2. 二进制拆分最后一组应取剩余数量，不能遗漏非二次幂部分。
3. `weight * count` 和 `value * count` 可能溢出，价值使用 `long long`。

**参考：**

- [OI Wiki：背包 DP](https://oi-wiki.org/dp/knapsack/)

## 4.4 最长上升子序列（LIS）

**适用范围：** 求一个最长严格递增子序列及其下标；O(n log n)。输入任意可比较序列，输出 0-based 下标序列，空输入返回空序列。
**能做什么：** 恢复一个最长严格递增子序列的下标。
**输入 / 输出：** 输入可严格比较序列；返回递增的 0-based 下标向量，空输入返回空。
**复杂度：** O(n log n).

**用途：** 求序列中下标递增且值严格递增的最长子序列。维护 `tail[len]`：长度为 `len+1` 的上升子序列可取得的最小末尾值；对每个数用 `lower_bound` 替换首个不小于它的位置。时间 $O(n\log n)$、空间 $O(n)$，并可记录前驱恢复方案。

**思路：**

- 模板返回一条严格上升子序列的下标，原数组使用 `0-based`。
- 若求非下降子序列，把 `lower_bound` 改成 `upper_bound`。
- `tailValue` 只用于优化转移，它本身通常不是最终子序列。
- 最终长度为 `tailValue.size()`，根据 `previous` 逆向恢复下标。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

template <class T>
// 参数：可严格比较序列。返回：一个最长严格递增子序列的 0-based 下标。效果：无副作用，O(n log n)。
vector<int> longestIncreasingSubsequenceIndices(const vector<T>& a) {
    // a 与返回下标均为 0-based；本模板恢复严格上升子序列。
    int n = static_cast<int>(a.size());
    // tailValue[len] 是长度 len+1 的严格上升子序列的最小末值。
    vector<T> tailValue;
    // tailIndex 与 tailValue 同步，保存该末值来自的原数组下标。
    vector<int> tailIndex;
    vector<int> previous(n, -1);

    for (int i = 0; i < n; ++i) {
        // lower_bound 找首个 >= a[i] 的位置；改成 upper_bound 即求非下降。
        int position = static_cast<int>(lower_bound(tailValue.begin(),
                                                   tailValue.end(), a[i])
                                        - tailValue.begin());
        if (position == static_cast<int>(tailValue.size())) {
            tailValue.push_back(a[i]);
            tailIndex.push_back(i);
        } else {
            tailValue[position] = a[i];
            tailIndex[position] = i;
        }
        // 记录长度少一的最优末尾下标，供最终方案沿前驱恢复。
        if (position > 0) previous[i] = tailIndex[position - 1];
    }

    vector<int> indices;
    if (!tailIndex.empty()) {
        for (int i = tailIndex.back(); i != -1; i = previous[i]) {
            indices.push_back(i);
        }
        reverse(indices.begin(), indices.end());
    }
    return indices;
}
```

**易错点：**

1. 子序列不要求连续；要求连续的是子数组或子串问题。
2. 严格上升用 `lower_bound`，非下降用 `upper_bound`。
3. 不能直接输出 `tailValue` 作为方案，应通过前驱恢复。

**参考：**

- [OI Wiki：最长上升子序列](https://oi-wiki.org/dp/basic/#%E6%9C%80%E9%95%BF%E4%B8%8A%E5%8D%87%E5%AD%90%E5%BA%8F%E5%88%97)

## 4.5 最长公共子序列（LCS）

**适用范围：** 求两个序列的最长公共子序列；O(nm) 时间与空间。输入任意可相等比较的序列，输出一个最长公共子序列；并列答案不保证唯一。
**能做什么：** 求两个序列的一个最长公共子序列。
**输入 / 输出：** 输入支持相等比较的 a、b；返回一个最长公共子序列元素序列。
**复杂度：** O(nm).

**用途：** 求两个序列都能按原顺序取出的最长公共子序列。令 `dp[i][j]` 表示两序列前 $i,j$ 项的 LCS 长度；末项相等则从左上加一，否则取上方和左方最大值。时间 $O(nm)$、空间 $O(nm)$；只求长度可滚动为 $O(m)$ 空间。

**思路：**

- 模板输入任意可比较元素序列，返回一条 LCS。
- `dp` 多开一行一列作为空前缀，初值全为 0。
- 恢复时相等元素加入答案；否则走向 DP 值较大的一侧。
- 最长公共子串要求连续，状态和答案更新方式不同，不能套用此模板。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

template <class T>
// 参数：支持相等比较的两序列。返回：一个最长公共子序列。效果：无副作用，O(nm) 时间与空间。
vector<T> longestCommonSubsequence(const vector<T>& a, const vector<T>& b) {
    // a、b 为 0-based；dp[i][j] 表示两序列前 i、j 个元素的 LCS 长度。
    int n = static_cast<int>(a.size());
    int m = static_cast<int>(b.size());
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    // i、j 递增，保证左、上、左上三个依赖状态已经计算。
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                // 最优公共子序列可把这对相同末字符一起接到左上状态。
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                // 末字符不同时，至少舍弃一侧末字符，取两种可能的较优值。
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    vector<T> result;
    // 从右下角逆推；值相等走左上，否则走不减小 dp 的一侧。
    for (int i = n, j = m; i > 0 && j > 0;) {
        if (a[i - 1] == b[j - 1]) {
            result.push_back(a[i - 1]);
            --i;
            --j;
        } else if (dp[i - 1][j] >= dp[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }
    reverse(result.begin(), result.end());
    return result;
}
```

**易错点：**

1. 元素相等时使用左上状态加一，不是上方或左方加一。
2. LCS 可以不连续，不要与最长公共子串混淆。
3. 完整二维表占 $O(nm)$ 内存，`n,m` 很大时可能超限。

**参考：**

- [OI Wiki：动态规划基础](https://oi-wiki.org/dp/basic/)

## 4.6 区间 DP

**适用范围：** 答案由相邻子区间合并得到时适用；常见 O(n^3)，空间 O(n^2)。输入序列，输出区间最优值；按区间长度递增，需定义单元素初值。
**能做什么：** 最小化相邻石子反复合并的总代价。
**输入 / 输出：** 输入石子权值；返回每次合并成本为区间和时的最小总费用，少于两项返回 0。
**复杂度：** 通常 O(n^3).

**用途：** 当答案由连续区间的子区间合并而来时，令 `dp[l][r]` 表示区间 `[l,r]` 的最优值，按区间长度递增，枚举分割点 `k` 合并左右答案。典型石子合并时间 $O(n^3)$、空间 $O(n^2)$；环形问题常复制一倍转成链。

**思路：**

- 模板求链式相邻石子合并的最小总代价，`stones` 使用 `0-based`。
- `dp[i][i]=0`，因为一堆石子无需合并。
- 前缀和在 $O(1)$ 时间得到当前区间总重量。
- 若求最大值，修改初值和 `min`；代价公式需按具体题意替换。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

// 参数：相邻合并权值序列。返回：每次合并相邻段、代价为段和时的最小总费用。效果：O(n^3)，空/单元素费用为 0。
ll minimumMergeCost(const vector<ll>& stones) {
    // stones 使用 0-based；dp[left][right] 表示闭区间合成一堆的最小代价。
    int n = static_cast<int>(stones.size());
    if (n == 0) return 0;
    vector<ll> prefix(n + 1, 0);
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + stones[i];

    // dp[i][i]=0；按长度递增保证转移所需的两个子区间已经算完。
    vector<vector<ll>> dp(n, vector<ll>(n, 0));
    for (int length = 2; length <= n; ++length) {
        // 所有长度更短的区间都已完成，当前转移可直接读取子区间。
        for (int left = 0; left + length <= n; ++left) {
            int right = left + length - 1;
            dp[left][right] = INF;
            ll intervalSum = prefix[right + 1] - prefix[left];
            // split 将 [left,right] 分成 [left,split] 与 [split+1,right]。
            for (int split = left; split < right; ++split) {
                dp[left][right] = min(dp[left][right],
                    dp[left][split] + dp[split + 1][right] + intervalSum);
            }
        }
    }
    return dp[0][n - 1];
}
```

**易错点：**

1. 必须按区间长度从小到大计算，确保子区间已经完成。
2. 分割点范围为 `left <= split < right`。
3. 环形区间复制后通常只枚举长度不超过原长度的区间。

**参考：**

- [OI Wiki：区间 DP](https://oi-wiki.org/dp/interval/)

## 4.7 树形 DP

**适用范围：** 父子依赖可分解的树上最优值；O(n) 状态/边处理。输入以 1..n 编号的树，输出根状态或全点结果；递归深度可能达 n。
**能做什么：** 求树上最大权独立集。
**输入 / 输出：** 输入 1..n 无向树与节点权值；返回不选相邻点的最大权和，允许空集。
**复杂度：** O(n).

**用途：** 树形 DP 先选根，用 DFS 汇总子树信息；状态通常描述节点选或不选、子树内代价等。树上最大权独立集令 `dp[u][1]` 为选 $u$，则孩子不能选；`dp[u][0]` 为不选，可取孩子两状态较大者。时间 $O(n)$、空间 $O(n)$。

**思路：**

- 模板输入无根树邻接表和 `weight[1..n]`，返回最大权值，允许空集。
- `parent` 用于阻止 DFS 沿无向边返回父节点。
- 选中节点后，与它直接相邻的节点均不能选。
- 若需恢复方案，保存每个状态对孩子所选状态并再次遍历。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：1..n 编号无向树。返回：不选相邻点时的最大权值和。效果：O(n)，权值按本函数参数约定给出。
ll maximumWeightIndependentSet(const vector<vector<int>>& tree,
                               const vector<ll>& weight,
                               int root = 1) {
    // tree 与 weight 均为 1-based；输入应为一棵连通无向树。
    int n = static_cast<int>(tree.size()) - 1;
    vector<array<ll, 2>> dp(n + 1, {0, 0});

    // 参数：当前点与父点。返回：无。效果：递归聚合子树状态到 dp[u]。
    function<void(int, int)> dfs = [&](int u, int parent) {
        // dp[u][0/1]：u 不选/选时，其整棵子树内可取得的最大权值。
        dp[u][0] = 0;
        dp[u][1] = weight[u];
        for (int v : tree[u]) {
            if (v == parent) continue;
            dfs(v, u); // 后序处理保证子树状态先于父状态完成
            // 不选 u 可自由选孩子最优状态；选 u 时所有孩子都必须不选。
            dp[u][0] += max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };

    dfs(root, 0);
    return max(dp[root][0], dp[root][1]);
}
```

**易错点：**

1. 无向树必须跳过父节点，否则递归会来回循环。
2. 合并孩子前先写清各维状态含义，不能在同一轮覆盖仍需使用的旧值。
3. 输入若不是连通树，需要对每个连通块分别计算并合并答案。

**参考：**

- [OI Wiki：树形 DP](https://oi-wiki.org/dp/tree/)

## 4.8 状态压缩 DP

**适用范围：** n 较小且状态由元素子集决定；常见 O(2^n n^2) 时间、O(2^n n) 空间。输入 n 个点及代价矩阵，输出最优闭合路线代价；要求 n 能安全位移且内存可承受。
**能做什么：** 求访问所有点并回到起点的最小旅行商回路。
**输入 / 输出：** 输入 n×n cost 方阵及 0-based 起点；返回最小回路费用，无解为 INF。
**复杂度：** O(2^n n^2).

**用途：** 当元素数较小且状态仅表示“哪些元素已选”时，用二进制掩码压缩集合。旅行商路径令 `dp[mask][u]` 为从起点出发、访问集合 `mask` 且停在 $u$ 的最小代价，枚举新节点转移。时间 $O(n^2 2^n)$、空间 $O(n2^n)$，通常适合 $n\le20$。

**思路：**

- 模板求从 `start` 出发、访问全部节点并回到起点的最短回路。
- `cost[u][v]` 为边权；无边设为 `INF`，允许有向图。
- `mask` 必须包含 `start` 和当前终点 `u`。
- 只求访问全部点的最短路径时，最后取各终点最小值，不再加回起点的边。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

// 参数：方阵 cost 与起点下标。返回：从起点出发访问每点一次并回起点的最小费用；无可行环返回 INF。效果：O(2^n n^2)，n 须较小。
ll travelingSalesmanCycle(const vector<vector<ll>>& cost, int start = 0) {
    // 节点为 0-based；cost[u][v] 可表示有向边，无边必须设为 INF。
    int n = static_cast<int>(cost.size());
    int all = 1 << n;
    // dp[mask][u]：从 start 出发，恰好访问 mask 中节点并停在 u 的最小代价。
    vector<vector<ll>> dp(all, vector<ll>(n, INF));
    dp[1 << start][start] = 0;

    for (int mask = 0; mask < all; ++mask) {
        if (!(mask & (1 << start))) continue;
        for (int u = 0; u < n; ++u) {
            // u 必须已访问且状态可达；INF 状态不能参与加法。
            if (!(mask & (1 << u)) || dp[mask][u] == INF) continue;
            for (int v = 0; v < n; ++v) {
                if (mask & (1 << v)) continue;
                if (cost[u][v] == INF) continue;
                // 只向未访问 v 扩展，因此每个节点在路径中恰好出现一次。
                int nextMask = mask | (1 << v);
                dp[nextMask][v] = min(dp[nextMask][v],
                                      dp[mask][u] + cost[u][v]);
            }
        }
    }

    ll answer = INF;
    // 最后补上 u -> start；若仍为 INF，表示不存在哈密顿回路。
    for (int u = 0; u < n; ++u) {
        if (dp[all - 1][u] != INF && cost[u][start] != INF) {
            answer = min(answer, dp[all - 1][u] + cost[u][start]);
        }
    }
    return answer;
}
```

**易错点：**

1. `1 << n` 要求 `n` 较小；位数超过 `int` 时应改用 64 位掩码，但状态数通常早已不可承受。
2. 无穷大状态不能直接参与加法，避免溢出形成伪最短路。
3. 估算内存：`2^20 * 20 * 8` 字节约为 160 MiB。

**参考：**

- [OI Wiki：状压 DP](https://oi-wiki.org/dp/state/)

## 4.9 数位 DP

**适用范围：** 按数字位逐位构造且约束可由有限状态描述；复杂度 O(L·S)，S 为状态数。输入十进制上界与目标和，输出 [0,N] 中符合条件数量；前导零语义由实现固定。
**能做什么：** 统计数位和等于目标的非负整数个数。
**输入 / 输出：** 输入非负上界与目标数位和；返回 [0,n] 内符合条件个数，前导零不计数。
**复杂度：** O(L·S).

**用途：** 数位 DP 统计巨大整数区间内满足数位约束的数。按高位到低位搜索，状态记录位置、已用信息及是否受上界限制；不受限状态可记忆化。模板统计数位和等于目标值的非负整数个数，时间 $O(D\cdot S\cdot10)$、空间 $O(D\cdot S)$。

**思路：**

- `countDigitSumUpTo(n,s)` 统计 `[0,n]` 中数位和为 `s` 的数，`n<0` 返回 0。
- 区间 `[left,right]` 的答案为两个前缀计数之差。
- 前导零在本题不改变数位和；涉及“数字长度、相邻位”时需增加 `started` 状态。
- 计数可能超过 `long long`，题目要求取模时应在转移中取模。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：非负上界 n 与目标数位和。返回：[0,n] 中数位和等于目标的整数个数。效果：O(位数×targetSum)。
ll countDigitSumUpTo(ll n, int targetSum) {
    // 统计闭区间 [0,n]；n<0 或目标和为负时统一返回 0。
    if (n < 0 || targetSum < 0) return 0;
    string digits = to_string(n);
    int length = static_cast<int>(digits.size());
    vector<vector<ll>> memo(length, vector<ll>(targetSum + 1, -1));

    // position 从最高位向低位；tight 表示当前前缀是否仍贴住 n 的上界。
    // 参数：当前数位位置、已用数位和及是否受上界限制。返回：满足目标数位和的补全数。效果：写入 memo，避免重复状态计算。
    function<ll(int, int, bool)> dfs = [&](int position, int sum, bool tight) -> ll {
        if (sum > targetSum) return 0;
        if (position == length) return sum == targetSum;
        // 仅非受限状态与更高位选择无关，可以跨路径复用记忆化值。
        if (!tight && memo[position][sum] != -1) return memo[position][sum];

        int upper = tight ? digits[position] - '0' : 9;
        ll answer = 0;
        for (int digit = 0; digit <= upper; ++digit) {
            // 只有原状态受限且本位取到当前上界，下一位才继续受限。
            answer += dfs(position + 1, sum + digit,
                          tight && digit == upper);
        }
        if (!tight) memo[position][sum] = answer;
        return answer;
    };

    return dfs(0, 0, true);
}

// 参数：非负闭区间 [left,right] 与目标数位和。返回：区间内符合条件的整数个数。效果：调用两次 countDigitSumUpTo。
ll countDigitSumInRange(ll left, ll right, int targetSum) {
    // 用前缀计数相减得到闭区间 [left,right]；left-1 由前缀函数处理负数。
    return countDigitSumUpTo(right, targetSum)
         - countDigitSumUpTo(left - 1, targetSum);
}
```

**易错点：**

1. `tight` 的下一状态应为“原来受限且当前位取到上界”。
2. 只有不受上界限制的状态才能直接复用记忆化结果。
3. 数字 0 是否计入、前导零是否影响约束，必须按题意单独处理。

**参考：**

- [OI Wiki：数位 DP](https://oi-wiki.org/dp/digit/)

## 4.10 DAG 上的 DP

**适用范围：** 依赖图为 DAG 且转移沿边传播；O(V+E)。输入邻接表与源点，输出最长路值；不可达节点用 NEG_INF 标记。
**能做什么：** 计算 DAG 中从源点出发的最长路。
**输入 / 输出：** 输入 1..n DAG 邻接表及源点；返回各点最长路，不可达为 NEG_INF。
**复杂度：** O(V+E).

**用途：** 有向无环图天然给出状态依赖：按拓扑序处理节点，使所有前驱先于后继完成。模板求指定源点到各点的最长路，可有负边；拓扑排序与松弛总时间 $O(n+m)$、空间 $O(n+m)$。若图存在环则拓扑序不完整，不能直接使用 DAG DP。

**思路：**

- 图使用 `graph[u] = {v,w}`，点编号为 `1..n`。
- `distance[v] == NEG_INF` 表示从源点不可达。
- 求路径条数、最短路等，只需替换状态初值与松弛公式。
- 若拓扑序长度小于 `n`，函数返回空数组表示输入不是 DAG。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG_INF = numeric_limits<ll>::lowest() / 4;

struct Edge {
    int to;
    ll weight;
};

// 参数：1..n 编号 DAG 邻接表与源点。返回：各点最长路权值；不可达为 NEG_INF。效果：O(V+E)，图必须无环。
vector<ll> longestPathInDAG(const vector<vector<Edge>>& graph, int source) {
    // graph 与节点为 1-based、有向、可含重边和负权，但必须无环。
    int n = static_cast<int>(graph.size()) - 1;
    vector<int> indegree(n + 1, 0);
    for (int u = 1; u <= n; ++u) {
        for (const auto& edge : graph[u]) ++indegree[edge.to];
    }

    queue<int> q;
    // 所有入度为 0 的点同时入队，保证断开的 DAG 也能完成拓扑排序。
    for (int u = 1; u <= n; ++u) {
        if (indegree[u] == 0) q.push(u);
    }
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (const auto& edge : graph[u]) {
            if (--indegree[edge.to] == 0) q.push(edge.to);
        }
    }
    // 拓扑序不含全部节点说明存在有向环；用空数组作为失败状态。
    if (static_cast<int>(order.size()) != n) return {};

    // distance[u] 为 source 到 u 的最长距离；NEG_INF 表示不可达。
    vector<ll> distance(n + 1, NEG_INF);
    distance[source] = 0;
    for (int u : order) {
        // 不可达点不能松弛出边，否则负无穷参与加法会产生伪状态。
        if (distance[u] == NEG_INF) continue;
        for (const auto& edge : graph[u]) {
            distance[edge.to] = max(distance[edge.to],
                                    distance[u] + edge.weight);
        }
    }
    return distance;
}
```

**易错点：**

1. 必须按拓扑序转移，按节点编号遍历通常不满足依赖关系。
2. 负权边存在时，不可达状态必须设为负无穷而非 0。
3. 有环图没有完整拓扑序；若需要处理环，应先缩点或改建模。

**参考：**

- [OI Wiki：DAG 上的 DP](https://oi-wiki.org/dp/dag/)

## 4.11 编辑距离

**适用范围：** 插入、删除、替换的单位代价字符串编辑距离；O(nm) 时间、O(m) 空间。输入两字符串，输出最少操作数。
**能做什么：** 计算单位编辑代价下的字符串编辑距离。
**输入 / 输出：** 输入字符串 a、b；返回插入/删除/替换代价均为 1 时的最少操作数。
**复杂度：** O(nm).

**用途与复杂度。** 求两个字符串通过插入、删除、替换变成相同字符串的最少操作数。状态转移枚举最后一步，时间 $O(nm)$；滚动一行后空间为 $O(m)$。

**思路与用法。** `dp[j]` 表示已处理的 `a` 前缀与 `b[0..j)` 的编辑距离。每行开始时保存左上旧值；相等字符沿用左上，不等时在删除、插入、替换三者中取最小。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数：两字符串。返回：插入、删除、替换代价均为 1 的最小编辑次数。效果：O(|a||b|) 时间、O(|b|) 空间。
int editDistance(const string& a, const string& b) {
    // dp[j] 表示当前 a 前缀与 b 的前 j 个字符之间的编辑距离。
    vector<int> dp(b.size() + 1);
    iota(dp.begin(), dp.end(), 0); // 空串变成 b 前 j 字符需要 j 次插入

    for (int i = 1; i <= static_cast<int>(a.size()); ++i) {
        int diagonal = dp[0]; // 覆盖前保存左上角的旧状态
        dp[0] = i; // b 为空时只能删除 a 的 i 个字符
        for (int j = 1; j <= static_cast<int>(b.size()); ++j) {
            int oldAbove = dp[j];
            if (a[i - 1] == b[j - 1]) {
                dp[j] = diagonal;
            } else {
                dp[j] = 1 + min({oldAbove, dp[j - 1], diagonal});
            }
            diagonal = oldAbove;
        }
    }
    return dp[b.size()];
}
```

**易错点。** `dp[j]` 在更新前是上方旧值，`dp[j-1]` 是本行左侧新值，`diagonal` 才是左上旧值；字符串很长时 `O(nm)` 仍可能超时。

## 4.12 树形 DP 与换根

**适用范围：** 树上需要求每个点作根的答案且可从父答案增量转移；O(n)。输入树，输出每个根的答案；边权和/节点编号需符合代码约定。
**能做什么：** 计算树上每个点作为根时的距离和。
**输入 / 输出：** 输入 n 和 1-based 无向树边；solve 返回 n+1 向量，1..n 槽为各根答案；同一对象仅调用一次，重复调用会重复累加。
**复杂度：** O(n).

**用途与复杂度。** 子树信息可合并成父节点状态；换根 DP 复用相邻根之间的答案，避免每个根重新遍历整棵树。示例要求 $n\ge1$，求无权树每个点到所有点的距离和，时间 $O(n)$、空间 $O(n)$。

**思路与用法。** 先以 1 为根求子树大小和根 1 的距离总和；第二遍从父点 `u` 移到子点 `v` 时，`v` 子树内的 `sz[v]` 个点距离减 1，其余 `n-sz[v]` 个距离加 1，因此 `ans[v]=ans[u]+n-2*sz[v]`。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct RerootDistanceSum {
    int n;
    vector<vector<int>> graph;
    vector<int> subtreeSize;
    vector<ll> answer;

    // 参数：树的顶点数 n>=1。返回：清零的换根 DP 对象。效果：分配 1..n 邻接表及状态数组。
    explicit RerootDistanceSum(int n)
        : n(n), graph(n + 1), subtreeSize(n + 1), answer(n + 1, 0) {}

    // 参数：树中相邻顶点 u、v。返回：无。效果：向无向邻接表加入一条边。
    void addEdge(int u, int v) {
        graph[u].push_back(v);
        graph[v].push_back(u); // 无向树
    }

    // 参数：当前点、父点和深度。返回：无。效果：计算子树大小与初始根答案。
    void firstDfs(int u, int parent, int depth) {
        subtreeSize[u] = 1;
        answer[1] += depth; // 第一遍累加以 1 为根的距离和
        for (int v : graph[u]) {
            if (v == parent) continue;
            firstDfs(v, u, depth + 1);
            subtreeSize[u] += subtreeSize[v];
        }
    }

    // 参数：当前根及其父点。返回：无。效果：将父点答案转移到子点并遍历整棵树。
    void rerootDfs(int u, int parent) {
        for (int v : graph[u]) {
            if (v == parent) continue;
            answer[v] = answer[u] + n - 2LL * subtreeSize[v];
            rerootDfs(v, u);
        }
    }

    // 参数：无；构造器须已给出 n 与全部树边。返回：answer[1..n] 的各根距离和。效果：O(n)，写入并返回内部答案。
    vector<ll> solve() {
        firstDfs(1, 0, 0);
        rerootDfs(1, 0);
        return answer; // answer[1..n] 有效
    }
};
```

**易错点。** 公式依赖树和单位边长；加权树需改用子树权重和总边权推导。递归链可能达到 $n$ 层，超大树应改迭代 DFS；每个测试用例都要重建或清空结构。

## 4.13 概率与期望 DP

**适用范围：** 等概率、独立抽取不同种类卡片直到集齐；本例不覆盖一般状态图。复杂度 O(n)。
**能做什么：** 计算 n 种卡片等概率独立抽取直至集齐的期望次数。
**输入 / 输出：** 输入种类数 n>0；返回期望抽取次数。
**复杂度：** O(n) 时间与空间。

**用途与复杂度。** 已收集 $i$ 种时，以 $(n-i)/n$ 概率抽到新种类，否则仍在状态 $i$。移项可得 `E[i]=(1 + pNew * E[i+1])/pNew`，总计 O(n) 时间与空间。

**思路与用法。** 收集 `n` 种等概率卡片，已有 `i` 种时下一步以 `(n-i)/n` 概率获得新种类，否则回到同一状态。把留在原状态的项移到等式左边，得到 `E[i]=(1 + pNew * E[i+1])/pNew`。

**代码：**

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数：不同卡片种类数 n>0。返回：等概率独立抽取直到集齐的期望次数。效果：O(n) 时间、空间。
double couponCollectorExpectation(int n) {
    // e[i] 是已收集 i 种时还需抽取次数的期望，边界 e[n]=0。
    vector<double> e(n + 1, 0.0);
    for (int i = n - 1; i >= 0; --i) {
        double pNew = static_cast<double>(n - i) / n;
        // 一步必然消耗，再以 pNew 前进；重复抽到旧种的概率已移项。
        e[i] = (1.0 + pNew * e[i + 1]) / pNew;
    }
    return e[0];
}
```

**易错点。** 期望的线性性允许对和取期望，但一般不能把“最优”随机决策直接替换为期望最大或最小；检查分母非零，输出精度按题目要求设置。
