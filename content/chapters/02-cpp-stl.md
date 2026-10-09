# 2. STL 库使用

本章面向 ICPC 现场速查，统一采用 C++17。每个容器先说明它的存储结构、复杂度与选择场景，再把成员方法、可直接配合的泛型算法和常见组合集中列出。复杂度中的 $n$ 表示容器或处理区间的元素数，$k$ 表示插入、删除或移动的元素数。除非题面或模板另有说明，示例默认包含 `<bits/stdc++.h>`，区间统一使用左闭右开的 `[first,last)`。

选择容器时，先判断是否需要连续内存、随机访问、两端操作、有序查找或迭代器稳定性。竞赛中一般优先使用 `vector`：它常数小、缓存友好，并能直接使用全部随机访问算法。只有需求明确匹配时，再改用 `deque` 或链表。调用任何会改变元素数量、容量或排列的操作后，都要重新确认迭代器、指针和引用是否仍然有效。

## 2.1 迭代器与半开区间

迭代器是容器与泛型算法之间的统一接口，可以把它近似理解为“带有容器规则的指针”。`begin()` 指向首元素，`end()` 指向最后一个元素之后的哨兵位置；STL 统一使用 `[first,last)`，因此空区间自然满足 `first == last`，区间长度为 `distance(first,last)`，两个相邻区间也能写成 `[l,m)` 与 `[m,r)` 而不重叠。

迭代器能力分级：输入迭代器可读，输出迭代器可写，前向迭代器可多次正向遍历，双向迭代器还可 `--`，随机访问迭代器可做 `it + k`、`it - k` 和比较大小。`vector`、`array`、`deque`、`string` 提供随机访问迭代器；`list` 提供双向迭代器；`forward_list` 只提供前向迭代器。算法能否使用取决于迭代器类别，例如 `sort` 要求随机访问迭代器，而 `find` 只要求输入迭代器。

移动随机访问迭代器通常为 $O(1)$；在链表上，`advance`、`next`、`prev`、`distance` 需要逐节点走，通常为 $O(k)$ 或 $O(n)$。迭代器只在所属容器及其有效期内有意义，不能比较来自不同容器的迭代器，也不能解引用 `end()`。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void iteratorBasics(vector<int>& a, const list<int>& linked) {
    vector<int>::iterator it = a.begin();
    vector<int>::const_iterator cit = a.cbegin();
    auto rit = a.rbegin();                 // 反向首元素，即原容器的最后一个元素
    auto sentinel = a.end();               // 尾后哨兵，只能比较，不能解引用

    if (it != sentinel) *it = 10;          // 普通迭代器可修改元素
    if (cit != a.cend()) cout << *cit;     // const_iterator 只能读取
    if (rit != a.rend()) cout << *rit;

    // list 不是随机访问容器，只能用 next 逐步移动。
    auto second = next(linked.begin(), min<size_t>(1, linked.size()));
    (void)second;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `c.begin()`、`c.end()`：返回正向区间的首迭代器和尾后迭代器，通常为 $O(1)$；`end()` 不可解引用。 |
| `c.cbegin()`、`c.cend()`：返回只读迭代器，即使 `c` 本身可修改，也不能通过该迭代器改元素，通常为 $O(1)$。 |
| `c.rbegin()`、`c.rend()`：返回反向迭代器；遍历顺序从尾到头。反向迭代器的 `base()` 指向其所指元素的后一个正向位置。 |
| `*it`：读取迭代器指向的元素；若迭代器可写，可通过它修改元素。对 `end()`、失效迭代器或空区间解引用是未定义行为。 |
| `it->member`：等价于 `(*it).member`，用于元素为结构体、`pair` 等对象时访问成员。 |
| `++it`、`it++`：移动到下一个元素；无须旧值时优先写前置自增。对所有常用容器单步移动为 $O(1)$。 |
| `--it`：移动到前一个元素，仅双向及随机访问迭代器支持；`--c.end()` 在非空容器上可得到末元素。 |
| `it + k`、`it - k`、`it[k]`：仅随机访问迭代器支持，移动或访问为 $O(1)$；链表迭代器不能这样写。 |
| `last - first`：仅随机访问迭代器支持，$O(1)$ 返回区间长度；两个迭代器必须来自同一序列且范围合法。 |
| `next(it,k)`：返回向前移动 `k` 步后的副本，不修改 `it`；随机访问迭代器为 $O(1)$，其他类别为 $O(k)$。 |
| `prev(it,k)`：返回向后移动 `k` 步后的副本，仅双向及随机访问迭代器可用；复杂度同 `next`。 |
| `advance(it,k)`：原地移动 `it`；随机访问为 $O(1)$，链表为 $O(\lvert k\rvert)$。不要越过合法范围。 |
| `distance(first,last)`：返回从 `first` 走到 `last` 的步数；随机访问为 $O(1)$，否则为 $O(n)$。对只能正向走的迭代器，`last` 必须可由 `first` 到达。 |
| `begin(a)`、`end(a)`：非成员版本，可统一处理 STL 容器和原生数组；原生数组区间为 `[a,a+N)`。 |
| `sort(first,last)`：要求随机访问迭代器，平均及最坏复杂度均为 $O(n\log n)$；会重排区间，等价元素不保证保持原顺序。 |
| `find(first,last,x)`：只需输入迭代器，线性扫描，$O(n)$；未找到返回 `last`。 |
| `lower_bound(first,last,x)`：要求区间已按同一规则有序，比较次数 $O(\log n)$；但链表移动迭代器仍可能为 $O(n)$，链表通常不应用它做二分。 |
| `reverse(first,last)`：要求双向迭代器，$O(n)$ 原地反转；会改变元素顺序，但通常不改变容器大小。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `sort(a.begin() + l, a.begin() + r)`：排序下标区间 `[l,r)`，必须保证 `0 <= l <= r <= a.size()`。 |
| `auto it = find(a.begin(), a.end(), x); if (it != a.end())`：判断是否找到，并用 `it - a.begin()` 得到 `vector` 下标。 |
| `for (auto it = c.begin(); it != c.end(); ) it = needErase(*it) ? c.erase(it) : next(it);`：对提供 `erase(iterator)` 的容器边遍历边删除，并接住其返回的新位置；不适用于没有 `erase` 的 `array`，也不适用于只提供 `erase_after` 的 `forward_list`。 |
| `for (auto it = c.rbegin(); it != c.rend(); ++it)`：从后向前遍历。 |
| `for (const auto& x : c)`：只读范围遍历且避免复制大对象；不能在循环中改变会使迭代器失效的容器结构。 |
| `auto mid = next(c.begin(), k)`：对非随机访问容器取得第 `k` 个位置；实际花费 $O(k)$。 |
| `vector<int> b(first, last)`：复制半开区间到新容器，复杂度 $O(n)$。 |
| `copy(first, last, back_inserter(ans))`：把区间追加到支持 `push_back` 的容器；目标无需预先 `resize`。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

void eraseNegative(vector<int>& a) {
    // vector::erase 会让被删位置及其后的迭代器失效，
    // 返回值正好是删除后下一元素的新迭代器。
    for (auto it = a.begin(); it != a.end();) {
        if (*it < 0) {
            it = a.erase(it);
        } else {
            ++it;
        }
    }
}
```

**易错点。**

- `end()` 是哨兵，不是最后一个元素；非空容器的末元素是 `prev(end())`。
- 来自不同容器的迭代器不能相减或作有序比较；即使元素值相同也不行。
- 容器扩容、插入、删除后要按该容器规则判断失效范围，不要继续使用旧迭代器。
- `sort`、`nth_element`、`lower_bound` 等算法对迭代器类别或区间有序性有额外要求。
- 不要在范围 `for` 中对同一 `vector` 做 `push_back` 或 `erase`；底层迭代器可能立即失效。

**参考：**

- [OI Wiki：迭代器](https://oi-wiki.org/lang/csl/iterator/)
- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)

## 2.2 `vector`

`vector<T>` 是连续内存上的动态数组，是竞赛中最常用的顺序容器。连续存储使它缓存友好，并可通过 `data()` 与需要数组指针的接口衔接。下标访问、首尾访问为 $O(1)$；尾插通常为均摊 $O(1)$；在中间插入或删除需要搬移后缀，复杂度 $O(n)$。

`vector` 同时维护元素数量 `size` 和已分配槽位数 `capacity`。当尾插超过容量时，它会申请更大的内存并搬移全部元素，所以单次扩容可能为 $O(n)$，但连续尾插的总成本仍是线性的。若能估计最终规模，先 `reserve` 可以减少扩容次数并避免不必要的迭代器失效。需要真正创建元素时使用 `resize`，不能把 `reserve` 当成 `resize`。

它提供随机访问迭代器，因此可以直接使用 `sort`、`reverse`、`lower_bound`、`unique`、`next_permutation` 等泛型算法。除非题目频繁在头部插删，或必须保持已有元素的迭代器稳定，通常优先选择 `vector`。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void vectorInitialization() {
    vector<int> a;                       // 空数组
    vector<int> b(5);                    // 5 个 0
    vector<int> c(5, -1);                // 5 个 -1
    vector<int> d{3, 1, 4, 1, 5};        // 列表初始化
    vector<int> e(d.begin() + 1, d.end()); // 复制 d 的 [1, size) 区间
    vector<vector<int>> graph(10);       // 10 个空 vector，常作邻接表
    vector<vector<int>> matrix(3, vector<int>(4, 0)); // 3 行 4 列
    (void)a; (void)b; (void)c; (void)e; (void)graph; (void)matrix;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `v.size()`：返回当前元素数，$O(1)$，类型为无符号的 `size_type`。 |
| `v.empty()`：判断是否没有元素，$O(1)$；比写 `v.size() == 0` 更直接。 |
| `v.capacity()`：返回当前无需重新分配即可容纳的元素数，$O(1)$；它可能大于 `size()`。 |
| `v.reserve(n)`：保证容量至少为 `n`，不创建元素且不改变 `size()`；若发生重分配为 $O(size)$，全部迭代器、指针和引用失效。若 `n <= capacity()`，无效果。 |
| `v.resize(n)`：把元素数改为 `n`。缩小时销毁尾部元素；扩大时值初始化新元素；复杂度与被增删元素数及可能的重分配有关。扩大且重分配时全部迭代器、指针和引用失效；不重分配时已有元素仍有效。缩小时被删元素和旧 `end()` 失效。 |
| `v.resize(n,value)`：扩大时用 `value` 初始化新元素；原有元素不变。缩小时 `value` 被忽略；失效规则同上一项。 |
| `v.shrink_to_fit()`：请求释放多余容量，但标准不保证一定执行；若重分配，全部迭代器、指针和引用失效。竞赛中通常无须调用。 |
| `v[i]`：不检查边界的 $O(1)$ 随机访问；越界是未定义行为。 |
| `v.at(i)`：检查边界的 $O(1)$ 访问；越界抛出 `out_of_range`，竞赛热路径较少使用。 |
| `v.front()`、`v.back()`：返回首元素和末元素引用，$O(1)$；空容器上调用是未定义行为。 |
| `v.data()`：返回连续内存首地址，$O(1)$；空容器时不可解引用。任何重分配都会使旧指针失效。 |
| `v.push_back(x)`：在尾部复制或移动加入 `x`，均摊 $O(1)$；若扩容则 $O(n)$，且全部迭代器、指针和引用失效。 |
| `v.emplace_back(args...)`：用参数在尾部直接构造元素，复杂度和失效规则同 `push_back`；对简单标量二者通常无区别。C++17 中返回新元素的引用。 |
| `v.pop_back()`：删除尾元素，$O(1)$ 且不返回该值；调用前必须非空。尾元素及 `end()` 失效。 |
| `v.insert(pos,x)`：在 `pos` 前插入一个元素，$O(n)$；若扩容则全部迭代器失效，否则 `pos` 及其后迭代器、指针和引用失效。返回新元素迭代器。 |
| `v.insert(pos,count,x)`：在 `pos` 前插入 `count` 个 `x`；复杂度 $O(n+count)$，失效规则同单元素插入。 |
| `v.insert(pos,first,last)`：插入迭代器区间，通常 $O(n+k)$。C++17 要求 `first`、`last` 不能是 `v` 自身的迭代器；需要自插入时先复制目标区间到临时容器。 |
| `v.emplace(pos,args...)`：在 `pos` 前原地构造一个元素；仍需搬移后缀，复杂度和失效规则同 `insert`。 |
| `v.erase(pos)`：删除 `pos` 元素并返回下一元素迭代器，$O(n)$；被删位置及其后迭代器、指针和引用失效。 |
| `v.erase(first,last)`：删除 `[first,last)` 并返回删除区间后新位置，复杂度 $O(n)$；空区间不删除。 |
| `v.clear()`：销毁全部元素、令 `size()` 为 0，$O(n)$；通常不释放 `capacity()`。所有元素迭代器、引用和指针失效。 |
| `v.assign(n,x)`：用 `n` 个 `x` 替换全部内容，$O(n)$；原有元素及其迭代器、引用失效。 |
| `v.assign(first,last)`：用指定区间替换全部内容，$O(n)$，原有迭代器、指针和引用全部失效。C++17 要求来源迭代器不能来自 `v` 自身，需要时先复制到临时容器。 |
| `v.swap(other)`、`swap(v,other)`：交换两个 `vector` 的内容，通常 $O(1)$；元素迭代器继续指向原元素，但它们所属的容器已交换，旧 `end()` 失效。 |
| `sort(v.begin(),v.end())`：按升序原地排序，$O(n\log n)$；需自定义顺序时传严格弱序比较器。 |
| `stable_sort(v.begin(),v.end())`：稳定排序，保留等价元素相对次序；有足够额外内存时为 $O(n\log n)$，否则 C++17 最坏为 $O(n\log^2 n)$。 |
| `reverse(v.begin(),v.end())`：$O(n)$ 原地翻转。 |
| `lower_bound(v.begin(),v.end(),x)`：在已升序区间中找第一个不小于 `x` 的位置，$O(\log n)$；无解返回 `end()`。 |
| `upper_bound(v.begin(),v.end(),x)`：在已升序区间中找第一个大于 `x` 的位置，$O(\log n)$。 |
| `binary_search(v.begin(),v.end(),x)`：在已升序区间判断是否存在，$O(\log n)$，只返回布尔值。 |
| `unique(v.begin(),v.end())`：把相邻重复元素移到逻辑尾部并返回新尾，$O(n)$；它不会改变 `size()`，常与 `erase` 连用。去除所有重复前通常先排序。 |
| `next_permutation(v.begin(),v.end())`：改成下一字典序排列，$O(n)$；已为最大排列时改为最小排列并返回 `false`。枚举全部排列前应先排序。 |
| `prev_permutation(v.begin(),v.end())`：改成上一字典序排列，$O(n)$，返回是否存在更小排列。 |
| `min_element`、`max_element`：线性扫描返回最值迭代器，$O(n)$；空区间返回 `end()`。 |
| `accumulate(v.begin(),v.end(),init)`：按顺序累加，$O(n)$；结果类型由 `init` 决定，求 `long long` 和必须写 `0LL`。 |
| `count(v.begin(),v.end(),x)`：统计等于 `x` 的元素数，$O(n)$。 |
| `find(v.begin(),v.end(),x)`：返回首个等于 `x` 的迭代器，$O(n)$；未找到返回 `end()`。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `v.reserve(n); for (...) v.push_back(x);`：已知规模上界时预留容量，减少扩容和元素搬移。 |
| `sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end());`：排序去重，总复杂度 $O(n\log n)$。 |
| `int p = lower_bound(v.begin(), v.end(), x) - v.begin();`：在升序数组中得到首个 `>= x` 的下标，若为 `size()` 表示不存在该位置。 |
| `int cnt = upper_bound(v.begin(), v.end(), x) - lower_bound(v.begin(), v.end(), x);`：统计升序数组中 `x` 的出现次数，$O(\log n)$。 |
| `sort(v.rbegin(), v.rend());`：降序排序；也可使用 `greater<int>()`。 |
| `reverse(v.begin() + l, v.begin() + r);`：翻转下标区间 `[l,r)`。 |
| `do { use(v); } while (next_permutation(v.begin(), v.end()));`：按字典序枚举不重排列；进入循环前先 `sort`。 |
| `v.erase(v.begin() + l, v.begin() + r);`：删除下标区间 `[l,r)`；后缀整体前移，$O(n)$。 |
| `v.insert(v.end(), b.begin(), b.end());`：把 `b` 追加到 `v`，复杂度 $O(v.size()+b.size())$ 的最坏界，预留容量可减少重分配。 |
| `long long sum = accumulate(v.begin(), v.end(), 0LL);`：用 `long long` 累加，避免 `int` 初值导致中间溢出。 |
| `vector<int>(v).swap(v);`：用副本重建并交换，常见实现通常会把容量压到接近 `size()`，但标准不保证一定收缩；$O(n)$ 且使全部旧迭代器失效。通常无须使用。 |
| `vector<vector<pair<int,int>>> g(n + 1); g[u].push_back({v,w});`：带权图邻接表。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> sortedUnique(vector<int> values) {
    sort(values.begin(), values.end());

    // unique 只把相邻重复值压到逻辑尾部，不会缩短 vector。
    // erase 才真正删除 [newEnd, end) 中的多余元素。
    auto newEnd = unique(values.begin(), values.end());
    values.erase(newEnd, values.end());
    return values;
}

pair<int, int> equalRangeIndices(const vector<int>& sorted, int x) {
    // 前提：sorted 已按升序排列。
    auto first = lower_bound(sorted.begin(), sorted.end(), x);
    auto last = upper_bound(sorted.begin(), sorted.end(), x);
    return {int(first - sorted.begin()), int(last - sorted.begin())};
}
```

**易错点。**

- `reserve(n)` 只改变容量，之后不能直接写 `v[i]`；需要 `resize(n)` 或逐个 `push_back`。
- 任何可能扩容的操作之后，不要继续使用原来的迭代器、元素指针或引用。
- `erase` 循环必须接住返回值；删除很多满足条件的元素时，优先使用 `remove_if + erase`，避免反复搬移造成 $O(n^2)$。
- `vector<bool>` 是位压缩特化，`v[i]` 返回代理对象而非普通 `bool&`；需要正常引用语义时用 `vector<char>`。
- `size()` 为无符号类型，倒序循环不要写 `for (size_t i = v.size()-1; i >= 0; --i)`。
- `lower_bound`、`upper_bound`、`binary_search` 的区间必须按相同比较规则有序。

**参考：**

- [OI Wiki：序列式容器](https://oi-wiki.org/lang/csl/sequence-container/)
- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)

## 2.3 `array`

`array<T,N>` 是对固定长度原生数组的轻量封装，元素仍连续地直接存放在对象内部，长度 `N` 必须在编译期确定。它没有动态分配，随机访问为 $O(1)$，整体复制、赋值和交换为 $O(N)$。与原生数组相比，`array` 提供 `size()`、迭代器、边界检查访问和直接比较，能自然参与 STL 算法。

当长度固定且较小，例如方向数组、矩阵的一行、固定维度状态或函数返回固定数组时，`array` 比 `vector` 更准确，也避免堆分配。若长度由输入决定、需要尾插或运行时扩缩，应选择 `vector`。大尺寸 `array` 作为局部变量可能占用过多栈空间，需要改为全局、静态存储或动态容器。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void arrayInitialization() {
    array<int, 4> a{};                  // 值初始化，四个元素均为 0
    array<int, 4> dx{1, 0, -1, 0};
    array<array<int, 3>, 2> mat{};      // 2 行 3 列，全部为 0
    // C++17 没有 to_array，需显式写出类型和长度。
    array<int, 4> primes{2, 3, 5, 7};
    (void)a; (void)dx; (void)mat; (void)primes;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `array<T,N> a{};`：定义固定长度数组并值初始化；数值类型会清零。省略 `{}` 时，局部基本类型元素可能未初始化。 |
| `a.size()`、`a.max_size()`：都返回编译期固定的 `N`，$O(1)$。 |
| `a.empty()`：仅当 `N == 0` 时为真，$O(1)$。 |
| `a[i]`：不检查边界的 $O(1)$ 访问。 |
| `a.at(i)`：检查边界的 $O(1)$ 访问；越界抛出 `out_of_range`。 |
| `a.front()`、`a.back()`：访问首尾元素，$O(1)$；`array<T,0>` 上调用无效。 |
| `a.data()`：返回连续存储的首地址，$O(1)$，可传给需要 `T*` 的函数。 |
| `a.fill(value)`：把每个元素赋为 `value`，$O(N)$。它按元素赋值，不是按字节填充。 |
| `a.swap(b)`、`swap(a,b)`：逐元素交换，$O(N)$；与大多数动态容器的常数交换不同。 |
| `a.begin()`、`a.end()`：随机访问迭代器，可使用完整的随机访问算法。 |
| `sort(a.begin(),a.end())`：原地排序，$O(N\log N)$。 |
| `reverse(a.begin(),a.end())`：原地翻转，$O(N)$。 |
| `lower_bound(a.begin(),a.end(),x)`：在已有序数组上二分，$O(\log N)$。 |
| `a == b`、`a < b` 等：按元素字典序比较，最坏 $O(N)$。两者元素类型和长度必须相同。 |
| `get<I>(a)`：编译期下标访问第 `I` 个元素，$O(1)$；`I` 必须为常量且小于 `N`。 |
| `tuple_size<decltype(a)>::value`：在编译期得到长度，常用于模板元编程，普通竞赛代码很少需要。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `const array<int,4> dx{1,0,-1,0};`：保存四方向增量，长度与数据绑定，避免传参时退化为指针。 |
| `array<int,26> cnt{}; ++cnt[ch-'a'];`：固定字符集计数并自动清零。 |
| `array<long long,2> state{INF,INF};`：表示固定数量的 DP 状态。 |
| `sort(a.begin(),a.end());`：直接使用泛型排序；固定长度不妨碍重排元素。 |
| `for (int x : a)`：范围遍历，与 `vector` 写法一致。 |
| `auto [x,y] = array<int,2>{3,4};`：C++17 结构化绑定拆分固定长度数组。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<pair<int, int>> fourNeighbors(int x, int y, int n, int m) {
    static const array<int, 4> dx{1, 0, -1, 0};
    static const array<int, 4> dy{0, 1, 0, -1};
    vector<pair<int, int>> result;

    for (int dir = 0; dir < 4; ++dir) {
        int nx = x + dx[dir], ny = y + dy[dir];
        if (0 <= nx && nx < n && 0 <= ny && ny < m) {
            result.push_back({nx, ny});
        }
    }
    return result;
}
```

**易错点。**

- C++17 不提供 `std::to_array`；应直接写出 `array<T,N>{...}`。
- `array<int,N> a;` 对局部基本类型不保证清零；需要零初始化时写 `a{}`。
- `array` 长度不能由输入变量决定；运行时长度使用 `vector`。
- `array<T,0>` 合法，但不能调用 `front()`、`back()` 或解引用 `begin()`。
- 大型局部 `array` 可能导致栈溢出。

**参考：**

- [OI Wiki：序列式容器](https://oi-wiki.org/lang/csl/sequence-container/)

## 2.4 `deque`

`deque<T>` 是双端队列。它通常由多块固定大小的连续缓冲区和一层索引组成，整体内存不连续，因此没有 `data()`，但仍支持 $O(1)$ 随机访问。它能在头尾以 $O(1)$ 插入和删除单个元素；在中间插删需要移动元素，复杂度 $O(n)$。

当算法需要同时在两端增删并偶尔按下标访问时，`deque` 很合适，例如 0-1 BFS、滑动窗口的候选下标和普通双端队列模拟。只在尾部增长时仍优先 `vector`；只需要 FIFO 或 LIFO 接口时可用基于 `deque` 的 `queue`、`stack`。不要把 `deque` 误当作链表：中间插删并非 $O(1)$，其迭代器失效规则也比链表严格。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void dequeInitialization() {
    deque<int> a;
    deque<int> b(5, -1);             // 5 个 -1
    deque<int> c{2, 3, 5, 7};
    deque<int> d(c.begin() + 1, c.end());
    (void)a; (void)b; (void)d;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `dq.size()`、`dq.empty()`：返回元素数或判断为空，均为 $O(1)$。 |
| `dq[i]`、`dq.at(i)`：$O(1)$ 随机访问；前者不检查边界，后者越界抛异常。 |
| `dq.front()`、`dq.back()`：$O(1)$ 访问首尾元素；调用前必须非空。 |
| `dq.push_front(x)`、`dq.emplace_front(args...)`：在头部加入一个元素，保证 $O(1)$；全部迭代器失效，但已有元素的指针和引用仍有效。 |
| `dq.push_back(x)`、`dq.emplace_back(args...)`：在尾部加入一个元素，保证 $O(1)$；全部迭代器失效，但已有元素的指针和引用仍有效。 |
| `dq.pop_front()`、`dq.pop_back()`：删除首或尾元素，$O(1)$ 且不返回值，必须先判空。`pop_front` 只使被删元素失效；`pop_back` 还会使旧 `end()` 失效。 |
| `dq.insert(pos,x)`、`dq.emplace(pos,args...)`：在中间插入，复杂度 $O(n)$；全部迭代器、指针和引用失效。返回所插元素的迭代器。若位置恰为首尾，应按头尾插入规则判断失效。 |
| `dq.erase(pos)`、`dq.erase(first,last)`：删除元素并返回后继位置，复杂度 $O(n)$。只删开头时仅被删元素失效；只删结尾时被删元素和旧 `end()` 失效；从中间删除时全部迭代器、指针和引用失效。 |
| `dq.resize(n,value)`：从尾部增删元素，复杂度与变化量有关。扩大时全部迭代器失效、已有元素的指针和引用仍有效；缩小时被删元素和旧 `end()` 失效。 |
| `dq.clear()`：删除全部元素，$O(n)$；指向元素的迭代器、指针和引用全部失效。 |
| `dq.swap(other)`：通常 $O(1)$ 交换内容。 |
| `dq.begin()`、`dq.end()`：随机访问迭代器，因此支持 `it+k`、迭代器相减以及 `sort`。 |
| `sort(dq.begin(),dq.end())`：可用，$O(n\log n)$；但分块存储的常数通常不如 `vector`。 |
| `reverse(dq.begin(),dq.end())`：$O(n)$ 原地翻转。 |
| `lower_bound(dq.begin(),dq.end(),x)`：有序时可二分，比较和移动均为 $O(\log n)$。 |
| `dq.data()`：不存在，因为元素整体不保证连续。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `dq.push_front(v)` 与 `dq.push_back(v)`：0-1 BFS 中权值 0 的新状态放队首，权值 1 的放队尾。 |
| `while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();`：维护单调递减下标队列。 |
| `while (!dq.empty() && dq.front() < i-k+1) dq.pop_front();`：删除滑动窗口外的过期下标。 |
| `int x = dq.front(); dq.pop_front();`：先读取再弹出；`pop_front()` 本身没有返回值。 |
| `dq.emplace_front(args...)`：直接在队首构造复杂对象。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> slidingWindowMaximum(const vector<int>& a, int k) {
    // 非法窗口没有定义；用空数组显式表示参数不合法。
    if (k <= 0 || k > (int)a.size()) return {};

    deque<int> dq;  // 保存下标；对应值从队首到队尾单调不增
    vector<int> ans;

    for (int i = 0; i < (int)a.size(); ++i) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i + 1 >= k) ans.push_back(a[dq.front()]);
    }
    return ans;
}
```

**易错点。**

- `deque` 没有 `data()`，不能把整个容器当作一段连续数组传出。
- 在头尾插入不会让已有元素的指针和引用失效，但会使全部迭代器失效；不要长期保存其迭代器。
- 中间插删为 $O(n)$，且会使全部迭代器、指针和引用失效；频繁中间操作应重新评估容器选择。
- `pop_front()`、`pop_back()` 不返回元素，且空容器调用未定义。
- `deque<bool>` 没有 `vector<bool>` 的专门位压缩语义。

**参考：**

- [OI Wiki：序列式容器](https://oi-wiki.org/lang/csl/sequence-container/)

## 2.5 `list`

`list<T>` 是双向链表，每个元素单独存储并保存前驱、后继链接。已知迭代器位置时，插入和删除为 $O(1)$；首尾插删也是 $O(1)$；但查找第 $k$ 个元素必须逐节点移动，复杂度 $O(n)$，且不支持下标或随机访问。

链表的优势是节点操作和迭代器稳定性：插入不会使已有元素的迭代器、指针和引用失效；删除只使被删元素失效；`splice` 可以直接转移节点。代价是每个节点额外存指针、内存不连续、缓存局部性差，实战常数往往明显大于 `vector`。只有确实需要频繁在已知位置插删、稳定引用或 $O(1)$ 拼接节点时再使用。

`list` 的迭代器是双向迭代器，不能传给通用 `sort`。标准库为它提供了成员版 `sort`、`merge`、`unique`、`remove`、`splice` 和 `reverse`，这些操作通过重连节点工作。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void listInitialization() {
    list<int> a;
    list<int> b(4, 0);
    list<int> c{1, 2, 3};
    list<int> d(c.begin(), c.end());
    (void)a; (void)b; (void)d;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `lst.size()`、`lst.empty()`：返回元素数或判断为空，C++11 起均为 $O(1)$。 |
| `lst.front()`、`lst.back()`：$O(1)$ 访问首尾元素；空链表调用未定义。 |
| `lst.push_front(x)`、`lst.emplace_front(args...)`：头插，$O(1)$；已有迭代器和引用不失效。 |
| `lst.push_back(x)`、`lst.emplace_back(args...)`：尾插，$O(1)$；已有迭代器和引用不失效。 |
| `lst.pop_front()`、`lst.pop_back()`：删除首尾，$O(1)$ 且不返回值；只使被删元素的迭代器和引用失效。 |
| `lst.insert(pos,x)`、`lst.emplace(pos,args...)`：在 `pos` 前插入，已知位置时 $O(1)$；返回新元素迭代器。 |
| `lst.erase(pos)`：删除 `pos` 并返回下一位置，$O(1)$；只使被删元素失效。 |
| `lst.erase(first,last)`：删除区间，$O(k)$，返回 `last` 对应的新位置。 |
| `lst.clear()`：删除全部节点，$O(n)$。 |
| `lst.remove(x)`：删除所有等于 `x` 的节点，$O(n)$；容器大小直接改变，只使被删节点失效。C++17 返回 `void`，不能用返回值取得删除数量。 |
| `lst.remove_if(pred)`：删除所有满足谓词的节点，$O(n)$；与泛型 `remove_if` 不同，它会真正删除。C++17 返回 `void`。 |
| `lst.unique()`：删除连续重复节点，$O(n)$；若要全局去重通常先 `lst.sort()`。 |
| `lst.sort()`：链表成员排序，稳定，$O(n\log n)$；不能写 `sort(lst.begin(),lst.end())`。 |
| `lst.reverse()`：通过重连节点反转，$O(n)$；元素对象本身通常不搬移。 |
| `lst.merge(other)`：线性合并两个已按相同规则排序的链表，$O(n+m)$；节点移入当前链表，`other` 变空。 |
| `lst.splice(pos,other)`：把 `other` 全部节点移到 `pos` 前，通常 $O(1)$；`other` 变空，节点迭代器仍有效但所属容器改变。 |
| `lst.splice(pos,other,it)`：把 `other` 中 `it` 节点移到 `pos` 前，$O(1)$。 |
| `lst.splice(pos,other,first,last)`：转移 `[first,last)`；同一容器内为 $O(1)$，跨容器时需计算转移数量而为 $O(k)$。`pos` 不能位于被转移范围内。 |
| `find(lst.begin(),lst.end(),x)`：线性查找，$O(n)$。 |
| `distance(lst.begin(),it)`：逐节点计算位置，$O(n)$；链表不适合频繁求下标。 |
| `lower_bound(lst.begin(),lst.end(),x)`：即使已排序，迭代器移动仍使总复杂度为 $O(n)$；没有对数时间优势。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `it = lst.erase(it)`：安全删除当前节点并继续遍历。 |
| `lst.sort(); lst.unique();`：排序后删除全部重复值，$O(n\log n)$。 |
| `a.splice(a.end(), b);`：把 `b` 的全部节点接到 `a` 尾部，不复制元素，`b` 变空。 |
| `a.splice(pos, b, it);`：把 `b` 的单个节点移动到 `a` 的 `pos` 前，适合维护稳定句柄。 |
| `auto it = next(lst.begin(), k);`：取得第 `k` 个节点，耗时 $O(k)$。 |
| `lst.remove_if([](int x){ return x < 0; });`：一次遍历删除负数。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

void moveNodeToFront(list<int>& values, list<int>::iterator it) {
    // 同一链表内 splice 单节点：不复制值，it 仍指向原节点，操作为 O(1)。
    values.splice(values.begin(), values, it);
}

void eraseOdd(list<int>& values) {
    for (auto it = values.begin(); it != values.end();) {
        if (*it & 1) it = values.erase(it);
        else ++it;
    }
}
```

**易错点。**

- `list` 没有 `operator[]`，也不能做 `it + k`；定位本身是线性的。
- 排序必须用 `lst.sort()`，不能使用要求随机访问迭代器的 `std::sort`。
- `unique()` 只删除相邻重复值；无序链表先排序才能全局去重。
- `merge()` 要求两个链表已经按相同规则有序，否则结果不保证有序。
- `splice` 后节点迭代器仍指向同一节点，但该节点可能已属于另一个容器。
- 多数竞赛问题中，`vector` 的低常数会胜过链表的理论插删优势。

**参考：**

- [OI Wiki：序列式容器](https://oi-wiki.org/lang/csl/sequence-container/)

## 2.6 `forward_list`

`forward_list<T>` 是单向链表，每个节点只保存后继链接，比 `list` 少一个前驱指针。它只提供前向迭代器，不能反向遍历，也没有 `back()`、`push_back()` 和 `size()`。已知前驱节点时，在其后插入或删除为 $O(1)$；寻找前驱或第 $k$ 个节点仍需 $O(n)$。

它的接口围绕“某位置之后”设计：`before_begin()` 返回首节点之前的特殊迭代器，配合 `insert_after`、`erase_after` 可以处理头节点。`forward_list` 的内存开销比双向链表略小，但接口更不直观，竞赛中使用频率很低。只有内存敏感且明确只需单向遍历、稳定节点和已知前驱位置插删时才考虑它。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void forwardListInitialization() {
    forward_list<int> a;
    forward_list<int> b(4, -1);
    forward_list<int> c{1, 2, 3};
    forward_list<int> d(c.begin(), c.end());
    (void)a; (void)b; (void)d;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `fl.empty()`：判断是否为空，$O(1)$；`forward_list` 没有 `size()`。 |
| `fl.front()`：访问首元素，$O(1)$；空容器调用未定义。没有 `back()`。 |
| `fl.before_begin()`、`fl.cbefore_begin()`：返回首节点之前的特殊位置，不可解引用，用于头部的 after 操作。 |
| `fl.push_front(x)`、`fl.emplace_front(args...)`：头插，$O(1)$。没有 `push_back()`。 |
| `fl.pop_front()`：删除首节点，$O(1)$ 且不返回值；调用前必须非空。 |
| `fl.insert_after(pos,x)`：在 `pos` 后插入，$O(1)$，返回新节点迭代器；`pos` 必须可解引用或为 `before_begin()`。 |
| `fl.emplace_after(pos,args...)`：在 `pos` 后直接构造，$O(1)$。 |
| `fl.erase_after(pos)`：删除 `pos` 后一个节点，$O(1)$，返回被删节点之后的位置；必须保证 `pos` 后确实存在节点。 |
| `fl.erase_after(first,last)`：删除 `(first,last)`，即不删除 `first` 和 `last`；复杂度 $O(k)$。 |
| `fl.clear()`：删除全部节点，$O(n)$。 |
| `fl.remove(x)`、`fl.remove_if(pred)`：线性扫描并真正删除匹配节点，$O(n)$，只使被删节点失效；二者在 C++17 中都返回 `void`。 |
| `fl.unique()`：删除连续重复值，$O(n)$；全局去重通常先排序。 |
| `fl.sort()`：稳定成员排序，$O(n\log n)$；通用 `std::sort` 不可用。 |
| `fl.reverse()`：反转链，$O(n)$。 |
| `fl.merge(other)`：合并两个已排序单链表，$O(n+m)$；`other` 变空。 |
| `fl.splice_after(pos,other)`：把 `other` 全部节点接到 `pos` 后，通常 $O(1)$；`other` 变空。 |
| `fl.splice_after(pos,other,it)`：把 `other` 中 `it` 后面的单个节点移到 `pos` 后，$O(1)$；注意转移的不是 `it` 本身，并须保证 `next(it)` 存在。 |
| `fl.splice_after(pos,other,first,last)`：把 `other` 的开区间 `(first,last)` 移到 `pos` 后；同一容器内为 $O(1)$，跨容器为 $O(k)$。`pos` 不能位于被转移范围内。 |
| `distance(fl.begin(),fl.end())`：计算元素数，$O(n)$；频繁调用会重复遍历。 |
| `find(fl.begin(),fl.end(),x)`：线性查找，$O(n)$。 |
| `reverse(fl.begin(),fl.end())`：泛型反转不可用，因为它要求双向迭代器；应调用 `fl.reverse()`。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `fl.insert_after(fl.before_begin(), x)`：等价于头插，并返回新首节点。 |
| `fl.erase_after(fl.before_begin())`：删除首节点；调用前必须非空。 |
| `for (auto prev = fl.before_begin(); next(prev) != fl.end(); )`：保存前驱以便按条件删除后继。 |
| `fl.sort(); fl.unique();`：排序后全局去重。 |
| `int n = distance(fl.begin(), fl.end());`：必要时线性计算长度；不要放入重复循环。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

void eraseNegative(forward_list<int>& values) {
    // 单链表删除节点需要掌握其前驱，因此维护 prev，检查 next(prev)。
    auto prev = values.before_begin();
    while (next(prev) != values.end()) {
        if (*next(prev) < 0) {
            values.erase_after(prev);  // prev 不动，继续检查新的后继
        } else {
            ++prev;
        }
    }
}
```

**易错点。**

- 没有 `size()`、`back()`、`push_back()`、`pop_back()`；若频繁需要这些操作，容器选择不合适。
- `before_begin()` 不能解引用，它只是为了表示首节点之前的位置。
- `erase_after(first,last)` 删除的是 `(first,last)`，与常见 `[first,last)` 形式不同。
- 不能使用 `std::sort` 或 `std::reverse`；使用成员函数 `sort()`、`reverse()`。
- 删除只使被删节点的迭代器和引用失效，插入不会使其他节点失效。

**参考：**

- [OI Wiki：序列式容器](https://oi-wiki.org/lang/csl/sequence-container/)

## 2.7 `string`

`std::string` 是连续存储的可变字符序列，可视为针对 `char` 优化的动态数组。它支持 $O(1)$ 下标访问和均摊 $O(1)$ 尾部追加单字符；中间插删、拼接、截取通常需要复制或搬移，复杂度与结果长度相关。它还提供查找、比较、替换、数值转换和流输入输出，是竞赛处理文本的默认类型。

字符串下标从 0 开始，`size()` 是字符数，不包含 C 风格结尾空字符。`c_str()` 与 `data()` 可取得连续字符缓冲区，但修改字符串或触发重分配后旧指针可能失效。`find` 等成员查找使用 `string::npos` 表示失败；简单实现通常最坏可达 $O(nm)$，需要保证线性或处理大量模式匹配时应改用 KMP、Z 函数、AC 自动机等专门算法。

`string` 提供随机访问迭代器，因此可直接使用 `sort`、`reverse`、`next_permutation`、`lower_bound` 等算法；使用二分前仍必须保证字符区间有序。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void stringInitialization() {
    string a;
    string b = "hello";
    string c(5, 'x');                    // "xxxxx"
    string d(b.begin() + 1, b.end());    // "ello"
    string e = b.substr(1, 3);           // "ell"
    const char raw[] = {'a', '\0', 'b'};
    string f(raw, 3);                    // 可包含内部 '\0'，size() 为 3
    (void)a; (void)c; (void)d; (void)e; (void)f;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `s.size()`、`s.length()`：均返回字符数，$O(1)$，不包含结尾空字符。 |
| `s.empty()`：判断长度是否为 0，$O(1)$。 |
| `s.capacity()`、`s.reserve(n)`、`s.resize(n,ch)`：语义与 `vector` 类似；`reserve` 不增加字符，`resize` 才改变长度。重分配会使指针、引用和迭代器失效。 |
| `s[i]`：$O(1)$ 且不做抛异常式边界检查。正文字符下标为 `[0,size())`；C++17 允许读取 `s[s.size()]`，其值为结尾的 `CharT()`，但把该位置改为非零值是未定义行为；`i > size()` 违反前置条件。 |
| `s.at(i)`：检查边界的 $O(1)$ 访问；越界抛出 `out_of_range`。 |
| `s.front()`、`s.back()`：$O(1)$ 访问首尾字符；空串调用未定义。 |
| `s.data()`、`s.c_str()`：返回连续字符数据指针；C++17 中 `data()` 对非 const 字符串可返回可写指针，但不得写越界或破坏结尾约束。修改字符串后旧指针可能失效。 |
| `s.push_back(ch)`、`s += ch`：尾部追加字符，均摊 $O(1)$。 |
| `s += t`、`s.append(t)`：追加字符串，复杂度与追加长度及可能重分配有关。 |
| `s.pop_back()`：删除末字符，$O(1)$ 且不返回字符；空串调用未定义。 |
| `s.substr(pos,len)`：复制从 `pos` 开始至多 `len` 个字符，$O(len)$；省略 `len` 表示取到末尾，`pos > size()` 抛异常。 |
| `s.find(t,pos)`：从 `pos` 起找 `t` 首次出现位置；失败返回 `string::npos`，最坏可达 $O(nm)$。 |
| `s.rfind(t,pos)`：反向寻找最后一次出现，失败返回 `npos`。 |
| `s.find_first_of(chars,pos)`：找第一个属于字符集合 `chars` 的位置；不是查找整个子串。 |
| `s.find_first_not_of(chars,pos)`：找第一个不属于集合的字符位置，常用于跳过分隔符。 |
| `s.compare(t)`：按字典序比较，返回负数、0 或正数，最坏 $O(n)$。通常直接用比较运算符更简洁。 |
| `s == t`、`s < t` 等：按字符字典序比较，最坏 $O(n)$。 |
| `s.insert(pos,t)`：在下标 `pos` 插入字符串，$O(n+\lvert t\rvert)$，会改变原串并可能使迭代器失效。 |
| `s.erase(pos,len)`：删除指定片段，$O(n)$；省略 `len` 删除到末尾。 |
| `s.replace(pos,len,t)`：把片段替换为 `t`，复杂度与移动及写入字符数有关。 |
| `s.clear()`：删除全部字符，$O(n)$，容量通常保留。 |
| `sort(s.begin(),s.end())`：按字符编码升序排序，$O(n\log n)$。 |
| `reverse(s.begin(),s.end())`：原地翻转，$O(n)$。 |
| `next_permutation(s.begin(),s.end())`：生成下一字典序字符排列，$O(n)$；枚举前先排序。 |
| `stoi(s)`、`stoll(s)`、`stod(s)`：把字符串前缀转换为数值；非法或越界会抛异常，可用第二参数取得停止位置。 |
| `to_string(x)`：把常见数值转换为十进制字符串。浮点输出格式不可精细控制时使用字符串流。 |
| `getline(cin,s)`：读取一整行但丢弃行末换行；可读空格。与 `cin >>` 混用时先处理残留换行。 |
| `stringstream ss(s)`：按流规则切分、解析一行，使用方便但常数较大。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `cin >> s`：读取一个不含空白的单词；遇空格、制表符或换行停止。 |
| `cin.ignore(numeric_limits<streamsize>::max(), '\n'); getline(cin,s);`：读完整行前清掉上一轮输入残留到行末。 |
| `cin >> ws; getline(cin,s);`：跳过所有前导空白后读行；若行首空格有意义，不应这样写。 |
| `if (s.find(t) != string::npos)`：判断子串是否出现。 |
| `for (size_t pos = s.find(t); pos != string::npos; pos = s.find(t,pos+1))`：枚举允许重叠的匹配位置；`t` 不能为空。 |
| `sort(s.begin(),s.end()); do { use(s); } while (next_permutation(s.begin(),s.end()));`：枚举字符多重集合的不重排列。 |
| `s.erase(remove(s.begin(),s.end(),ch),s.end());`：删除所有等于 `ch` 的字符。 |
| `int digit = s[i]-'0';`：已确认字符为数字时转数值；可用 `isdigit((unsigned char)s[i])` 检查。 |
| `string one(1,ch);`：由单个字符构造字符串；不要把 `ch` 直接当作 C 字符串指针。 |
| `string rev = s; reverse(rev.begin(),rev.end());`：保留原串并得到反转副本。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<size_t> findAllOccurrences(const string& text, const string& pattern) {
    vector<size_t> positions;
    if (pattern.empty()) return positions; // 避免空模式导致无限枚举

    for (size_t pos = text.find(pattern); pos != string::npos;
         pos = text.find(pattern, pos + 1)) {
        positions.push_back(pos);           // pos+1 允许匹配彼此重叠
    }
    return positions;
}

vector<string> splitByWhitespace(const string& line) {
    stringstream input(line);
    vector<string> words;
    string word;
    while (input >> word) words.push_back(word);
    return words;
}
```

**易错点。**

- `string::npos` 是无符号最大值，不要存入 `int` 后依赖其变成 `-1`；直接与 `npos` 比较。
- `substr` 会创建并复制新字符串，大量大子串操作可能成为瓶颈。
- `find` 不保证线性复杂度；严格复杂度要求下使用专门字符串算法。
- `cin >> s` 不读空格；`getline` 与格式化输入混用时注意残留换行。
- 传出 `c_str()` 或 `data()` 后，任何修改字符串的操作都可能让旧指针失效。
- `tolower`、`isdigit` 等 `<cctype>` 函数应传入 `unsigned char` 转换后的值，避免负 `char` 导致未定义行为。

**参考：**

- [OI Wiki：string](https://oi-wiki.org/lang/csl/string/)
- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)

## 2.8 `pair`

`pair<T1,T2>` 把两个值组合成一个对象，常用于坐标、边、带权状态、键值对和函数返回多个结果。两个字段分别为 `first`、`second`，创建和访问都是 $O(1)$。只要字段支持比较，`pair` 就能直接比较：先比较 `first`，相等时再比较 `second`，即字典序；这使 `vector<pair<...>>`、`set<pair<...>>` 和 `priority_queue<pair<...>>` 很方便。

当两个字段含义明确且局部使用时，`pair` 简洁有效；若字段较多、容易写反，或需要自定义行为，命名 `struct` 更易读。C++17 结构化绑定可以把 `pair` 拆成局部变量，注意 `auto [x,y]` 会复制，只有 `auto& [x,y]` 才能修改原对象。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void pairInitialization() {
    pair<int, int> a;                    // 两个 int 均值初始化为 0
    pair<int, string> b{7, "node"};
    auto c = make_pair(3, 4LL);          // 推导为 pair<int,long long>
    pair<int, int> d = {1, 2};
    (void)a; (void)b; (void)c; (void)d;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `pair<T,U> p{a,b}`：直接构造两个字段，复杂度取决于字段构造，固定大小标量可视为 $O(1)$。 |
| `make_pair(a,b)`：推导字段类型并创建 `pair`；C++11 后多数场合花括号更简洁。 |
| `p.first`、`p.second`：访问两个字段，$O(1)$；若对象非常量，可直接修改。 |
| `get<0>(p)`、`get<1>(p)`：按编译期下标访问字段，$O(1)$。 |
| `auto [x,y] = p`：C++17 结构化绑定，复制两个字段；修改 `x`、`y` 不影响 `p`。 |
| `auto& [x,y] = p`：引用绑定，修改字段会作用于 `p`；容器元素失效时这些引用也失效。 |
| `tie(x,y) = p`：把字段赋给已存在变量；会发生赋值而非声明。 |
| `tie(x,ignore) = p`：只接收第一字段，忽略第二字段。 |
| `p == q`、`p != q`：按两字段比较相等性，最坏检查两个字段。 |
| `p < q`、`p > q` 等：字典序比较，先 `first` 后 `second`。复杂度由字段比较决定。 |
| `p.swap(q)`、`swap(p,q)`：分别交换两个字段，复杂度为字段交换复杂度之和。 |
| `sort(v.begin(),v.end())`：`vector<pair<...>>` 默认按 `first` 升序，再按 `second` 升序，$O(n\log n)$。 |
| `priority_queue<pair<int,int>> pq`：默认字典序最大 `pair` 在堆顶；先最大 `first`，再最大 `second`。 |
| `map<Key,Value>` 的元素类型：迭代时得到类似 `pair<const Key,Value>`，`first` 键不可通过迭代器修改。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `vector<pair<int,int>> edges; edges.push_back({u,v});`：保存边或坐标。 |
| `sort(v.begin(),v.end());`：按第一关键字升序、第二关键字升序。 |
| `sort(v.begin(),v.end(), [](const auto& a,const auto& b){ if (a.first != b.first) return a.first < b.first; return a.second > b.second; });`：第一字段升序、第二字段降序。 |
| `auto [dist,u] = pq.top(); pq.pop();`：从存储 `pair` 的优先队列拆包。 |
| `return {answer,index};`：函数返回两个结果。 |
| `set<pair<int,int>> seen;`：按字典序维护唯一二元状态。 |
| `min(p,q)`、`max(p,q)`：按 `pair` 字典序取较小或较大者。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<pair<int, int>> sortByFirstAscSecondDesc(
    vector<pair<int, int>> values
) {
    sort(values.begin(), values.end(), [](const auto& a, const auto& b) {
        if (a.first != b.first) return a.first < b.first;
        return a.second > b.second;
    });
    return values;
}

pair<long long, int> maximumWithIndex(const vector<long long>& a) {
    // 前置条件：a 非空，否则“最大值及其下标”没有定义。
    assert(!a.empty());

    long long best = numeric_limits<long long>::lowest();
    int index = -1;
    for (int i = 0; i < (int)a.size(); ++i) {
        if (a[i] > best) best = a[i], index = i;
    }
    return {best, index};
}
```

**易错点。**

- 默认比较是字典序，不是只比较 `first`。
- `auto [x,y]` 会复制；要原地修改必须使用 `auto& [x,y]`。
- 结构化绑定引用容器元素时，容器扩容或删除可能使引用失效。
- 字段语义复杂时使用命名结构体，减少把 `first`、`second` 写反的风险。
- 自定义比较器必须满足严格弱序，元素完全等价时要返回 `false`。

**参考：**

- [OI Wiki：pair](https://oi-wiki.org/lang/csl/pair/)

## 2.9 `tuple`

`tuple<Ts...>` 是 `pair` 的多字段推广，可在一个对象中保存任意固定数量、不同类型的值，适合函数返回多个结果、临时复合排序键和小型固定状态。字段数量与类型在编译期确定；`get<I>` 访问固定字段通常为 $O(1)$。默认比较按第 0、1、2……字段依次进行字典序比较。

C++17 结构化绑定使 `tuple` 的拆包很自然，但字段数量多时，`get<2>` 或 `[a,b,c,d]` 很难表达含义。若对象会跨越较大作用域、需要反复使用或携带行为，应改用具名 `struct`。`tuple` 适合“临时组合”，不应为了少写一个结构体而牺牲可读性。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;

void tupleInitialization() {
    tuple<int, int, long long> state{2, 7, 100LL};
    auto record = make_tuple(string("alice"), 95, true);
    tuple<int, int, int> zero{};          // 三个 int 均为 0
    (void)state; (void)record; (void)zero;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `tuple<Ts...> t{args...}`：构造固定字段组合；复杂度为各字段构造成本之和。 |
| `make_tuple(args...)`：推导字段类型并构造元组；通常会保存值，而非引用。 |
| `get<I>(t)`：按编译期下标访问第 `I` 个字段，$O(1)$；`I` 必须是常量且不能越界。 |
| `get<Type>(t)`：当该类型在元组中恰好出现一次时按类型访问；重复类型时编译失败。竞赛中按下标更常见。 |
| `auto [a,b,c] = t`：C++17 结构化绑定并复制字段。变量个数必须与元组字段数一致。 |
| `auto& [a,b,c] = t`：引用绑定，可修改原元组字段。 |
| `tie(a,b,c) = t`：把字段赋给已有变量；可用 `ignore` 忽略不需要的字段。 |
| `tie(a,b,c)`：创建引用元组，常用于一次比较多个现有变量或作为赋值左侧。引用对象必须保持有效。 |
| `forward_as_tuple(args...)`：创建转发引用元组，不延长临时对象生命周期；竞赛中很少需要，误用易产生悬空引用。 |
| `tuple_cat(t1,t2,...)`：连接多个元组、`pair` 或 `array`，复杂度为字段复制或移动成本之和。 |
| `t == u`：逐字段判断相等。 |
| `t < u`、`t > u` 等：从第 0 字段开始字典序比较；当前字段不等时停止。 |
| `t.swap(u)`、`swap(t,u)`：逐字段交换。 |
| `tuple_size<decltype(t)>::value`：编译期获得字段数。 |
| `tuple_element<I,decltype(t)>::type`：编译期获得第 `I` 个字段类型。 |
| `sort(v.begin(),v.end())`：`vector<tuple<...>>` 默认按字段依次升序，$O(n\log n)$。 |
| `priority_queue<tuple<...>> pq`：默认字典序最大的元组在堆顶；小根堆可配 `greater<tuple<...>>`。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `tuple<int,int,long long>{u,v,w}`：保存带两个端点和权值的记录。 |
| `auto [u,v,w] = edge;`：拆包读取三个字段；只读且字段较大时可写 `const auto& [u,v,w]`。 |
| `return {distance,parent,count};`：函数一次返回多个结果。 |
| `sort(events.begin(),events.end());`：按时间、类型、编号等字段的声明顺序做字典序排序。 |
| `tie(a,b,c) < tie(x,y,z)`：按多个现有变量生成字典序比较键，不创建具名结构体。 |
| `make_tuple(a.first,-a.second) < make_tuple(b.first,-b.second)`：用变号表达整数第二关键字降序；最小负数可能溢出时不要使用。 |
| `priority_queue<tuple<ll,int,int>, vector<tuple<ll,int,int>>, greater<tuple<ll,int,int>>> pq;`：以第一字段为首关键字的小根堆。 |
| `tie(answer,index) = solve();`：把函数返回元组写入已有变量。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

tuple<ll, int, int> summarize(const vector<int>& a) {
    // 前置条件：a 非空，否则最小值和最大值没有定义。
    assert(!a.empty());

    ll sum = 0;
    int minimum = numeric_limits<int>::max();
    int maximum = numeric_limits<int>::lowest();

    for (int x : a) {
        sum += x;
        minimum = min(minimum, x);
        maximum = max(maximum, x);
    }
    return {sum, minimum, maximum};
}

vector<tuple<int, int, int>> sortEvents(vector<tuple<int, int, int>> events) {
    // 默认顺序：先比较时间，再比较事件类型，最后比较编号。
    sort(events.begin(), events.end());
    return events;
}
```

**易错点。**

- `get<I>` 的 `I` 必须是编译期常量，不能用循环变量访问不同字段。
- 默认排序严格按字段声明顺序；关键字优先级不一致时要调整字段顺序或提供比较器。
- `auto [a,b,c]` 复制字段，`auto&` 才引用原对象。
- `make_tuple(ref(x))` 才能显式保存引用包装；普通 `make_tuple(x)` 保存值。
- `forward_as_tuple` 可能保存指向临时对象的引用，不熟悉生命周期时避免使用。
- 三个以上字段若长期存在，应优先定义带字段名的 `struct`。

**参考：**

- [OI Wiki：pair](https://oi-wiki.org/lang/csl/pair/)
- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
## 2.10 `stack`

`std::stack<T>` 是后进先出（LIFO）的容器适配器，只能操作栈顶。它常用于括号匹配、表达式求值、单调栈、撤销和显式栈 DFS。默认底层是 `deque<T>`，也可用支持 `back/push_back/pop_back` 的 `vector` 或 `list`。`top/push/emplace/pop` 通常为 $O(1)$，空间 $O(n)$。它无迭代器；需要遍历或随机访问时直接用 `vector` 更合适。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
stack<int> st;                        // 默认底层 deque<int>
stack<int, vector<int>> vectorStack;  // 改用 vector
deque<int> sourceData{1, 2, 3};
stack<int> copied(sourceData);        // 栈底到栈顶为 1、2、3
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `st.empty()`、`st.size()`：判空、取得元素数，均为 $O(1)$。 |
| `st.top()`：返回栈顶引用，$O(1)$；可读写，空栈调用未定义。 |
| `st.push(value)`、`st.emplace(args...)`：在栈顶插入，通常 $O(1)$。 |
| `st.pop()`：删除栈顶，通常 $O(1)$，没有返回值。 |
| `st.swap(other)`、`swap(st, other)`：交换两个同类型栈，通常 $O(1)$。 |
| `st = stack<T>{}`：用空栈覆盖以清空；原元素会被析构。 |
| `a == b`、`a < b` 等：C++17 按底层容器字典序比较，最坏 $O(n)$。 |
| `sort/reverse/find/next_permutation`：不能直接使用，因为没有 `begin/end`。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `int x = st.top(); st.pop();`：取得并删除栈顶，执行前必须判空。 |
| `while (!st.empty()) st.pop();`：逐个弹出清空，$O(n)$。 |
| `stack<pair<int,int>> st;`：同时保存值和下标。 |
| `while (!st.empty() && a[st.top()] <= a[i]) st.pop();`：维护严格递减单调栈。 |
| `stack<State> st; st.push(start);`：显式栈模拟递归。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
// 每个位置右侧第一个严格更大元素的下标；不存在为 -1。
vector<int> nextGreaterPosition(const vector<int>& a) {
    vector<int> ans(a.size(), -1);
    stack<int> st;  // 尚未找到答案的下标，对应值单调不增
    for (int i = 0; i < (int)a.size(); ++i) {
        while (!st.empty() && a[st.top()] < a[i]) {
            ans[st.top()] = i;  // a[i] 是首个严格更大的右侧元素
            st.pop();
        }
        st.push(i);
    }
    return ans;
}
```

**易错点。**

- `pop()` 不返回元素；弹出后先前的 `top()` 引用失效。
- 无 `clear()`、下标和迭代器；复制后逐个弹出可遍历，但顺序为栈顶到栈底。
- 单调栈中的 `<` 与 `<=` 决定相等元素如何处理，必须对应题意。
- 显式 DFS 若要保持递归访问顺序，通常要逆序压入邻点。

**参考：**

- [OI Wiki：容器适配器](https://oi-wiki.org/lang/csl/container-adapter/)
- [OI Wiki：单调栈](https://oi-wiki.org/ds/monotonous-stack/)

## 2.11 `queue`

`std::queue<T>` 是先进先出（FIFO）的容器适配器，从队尾加入、队首取出，是 BFS、拓扑排序、层序遍历和任务模拟的基础工具。默认底层为 `deque<T>`，也可用 `list<T>`；`vector` 没有 `pop_front()`，不能作为底层。基本操作通常 $O(1)$，空间 $O(n)$。按优先级取元素用 `priority_queue`；需要遍历或两端操作用 `deque`。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
queue<int> q;
queue<int, list<int>> listQ;
deque<int> sourceData{1, 2, 3};
queue<int> copied(sourceData);  // 队首 1，队尾 3
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `q.empty()`、`q.size()`：判空、取得元素数，均为 $O(1)$。 |
| `q.front()`、`q.back()`：返回队首、队尾引用，$O(1)$；空队列调用未定义。 |
| `q.push(value)`、`q.emplace(args...)`：在队尾插入，通常 $O(1)$。 |
| `q.pop()`：删除队首，通常 $O(1)$，无返回值。 |
| `q.swap(other)`、`swap(q, other)`：交换同类型队列，通常 $O(1)$。 |
| `q = queue<T>{}`：用空队列覆盖以清空。 |
| `a == b`、`a < b` 等：C++17 按底层容器比较，最坏 $O(n)$。 |
| `sort/reverse/find` 和范围 `for`：不能直接使用，因为没有迭代器。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `q.push(start); dist[start] = 0;`：BFS 起点入队并立即标记。 |
| `int u = q.front(); q.pop();`：取得并删除队首。 |
| `int levelSize = q.size();`：固定当前层节点数。 |
| `queue<pair<int,int>> q;`：网格 BFS 保存坐标。 |
| `queue<int> q;` 配合入度数组：Kahn 拓扑排序。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> bfsDistances(const vector<vector<int>>& graph, int start) {
    vector<int> dist(graph.size(), -1);
    queue<int> q;
    dist[start] = 0;  // 入队即标记，防止重复入队
    q.push(start);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : graph[u]) {
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
    return dist;
}
```

**易错点。**

- `pop()` 无返回值，先取 `front()`；空队列调用 `front/back/pop` 均未定义。
- BFS 应在入队时标记，否则同一点可能重复入队。
- 普通 BFS 只适用于无权或等权图；0/1 边权用 0-1 BFS，一般非负边权用 Dijkstra。

**参考：**

- [OI Wiki：容器适配器](https://oi-wiki.org/lang/csl/container-adapter/)
- [OI Wiki：广度优先搜索](https://oi-wiki.org/search/bfs/)

## 2.12 `priority_queue`

`std::priority_queue<T>` 基于堆，每次访问当前优先级最高的元素。默认底层为 `vector<T>`，比较器 `less<T>`，所以默认大根堆，`top()` 为最大值。常用于 Dijkstra、Prim、贪心调度、合并代价和维护前 $k$ 大/小。`top` 为 $O(1)$，插入和弹顶 $O(\log n)$，建堆通常 $O(n)$。它不能删除或修改任意元素；更新优先级常采用重新入堆、出堆时跳过旧状态。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
priority_queue<int> maxHeap;
priority_queue<int, vector<int>, greater<int>> minHeap;
vector<int> initial{3, 1, 4, 1, 5};
priority_queue<int> fromRange(initial.begin(), initial.end());  // 线性建堆
struct Node { long long distance; int vertex; };
struct GreaterDistance {
    bool operator()(const Node& a, const Node& b) const {
        return a.distance > b.distance;  // 距离更小者优先
    }
};
priority_queue<Node, vector<Node>, GreaterDistance> pq;

// lambda 比较器的类型要写入模板参数，并把比较器对象传给构造函数。
auto bySecond = [](const pair<int, int>& a, const pair<int, int>& b) {
    return a.second > b.second;  // second 较小者优先
};
priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(bySecond)> bySecondHeap(bySecond);
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `pq.empty()`、`pq.size()`：判空、取得元素数，均为 $O(1)$。 |
| `pq.top()`：返回最高优先级元素的常量引用，$O(1)$；空堆调用未定义。 |
| `pq.push(value)`、`pq.emplace(args...)`：插入，$O(\log n)$。 |
| `pq.pop()`：删除堆顶，$O(\log n)$，无返回值。 |
| `pq.swap(other)`：交换完全同类型的堆，通常 $O(1)$。 |
| `priority_queue<T,vector<T>,greater<T>>`：小根堆写法。 |
| `priority_queue<T,vector<T>,decltype(cmp)> pq(cmp)`：使用 lambda 比较器；类型和对象都不能省略。比较器返回 `true` 表示左参数应排在右参数之后。 |
| `make_heap/push_heap/pop_heap/sort_heap`：操作随机访问区间的泛型堆算法。 |
| `sort/reverse/find` 和范围 `for`：不能直接使用，因为没有迭代器。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `priority_queue<int> pq;`：动态取得最大值。 |
| `priority_queue<int,vector<int>,greater<int>> pq;`：动态取得最小值。 |
| 小根堆执行 `push(x)` 后若 `size()>k` 则 `pop()`：保留最大的 $k$ 个数。 |
| `auto [d,u]=pq.top(); pq.pop(); if (d!=dist[u]) continue;`：Dijkstra 跳过旧记录。 |
| `pq.emplace(distance, vertex);`：直接构造 `pair` 入堆。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> largestK(const vector<int>& a, int k) {
    if (k <= 0) return {};
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int x : a) {
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();  // 淘汰当前最小值
    }
    vector<int> ans;
    while (!pq.empty()) { ans.push_back(pq.top()); pq.pop(); }
    reverse(ans.begin(), ans.end());
    return ans;
}
```

**易错点。**

- 默认大根堆；最短路通常需要 `greater<...>` 小根堆。
- 比较器必须满足严格弱序，不能用 `>=` 或 `<=`；返回 `true` 表示左参数优先级更低。
- `top()` 为常量引用，不能原地修改。需要删除任意元素时考虑 `set/multiset` 或延迟删除。

**参考：**

- [OI Wiki：容器适配器](https://oi-wiki.org/lang/csl/container-adapter/)
- [OI Wiki：堆](https://oi-wiki.org/ds/binary-heap/)

## 2.13 `set`

`std::set<Key>` 是保存不重复键的有序关联容器，通常由平衡二叉搜索树实现。元素始终按比较器排序，默认升序；重复插入不会新增元素。它适合动态去重、判存在、前驱后继和需要稳定最坏 $O(\log n)$ 的查询。查找、插入、按键删除和界查询均为 $O(\log n)$，遍历 $O(n)$，空间 $O(n)$。只判存在且不关心顺序可用平均更快的 `unordered_set`；允许重复则用 `multiset`。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
set<int> s;
set<int, greater<int>> descending;
set<int> initialized{3, 1, 3, 2};  // 仅保存 1、2、3
vector<int> a{4, 1, 4, 2};
set<int> fromRange(a.begin(), a.end());
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `s.empty()/size()/clear()`：判空 $O(1)$、计数 $O(1)$、删除全部 $O(n)$。 |
| `s.insert(x)`：$O(\log n)$，返回 `pair<iterator,bool>`，布尔值表示是否真正插入。 |
| `s.emplace(args...)`：直接构造并尝试插入，$O(\log n)$。 |
| `s.erase(key)`：按键删除，返回 `0` 或 `1`，$O(\log n)$。 |
| `s.erase(it)`：删迭代器所指元素并返回下一位置，均摊 $O(1)$；只有被删元素的迭代器和引用失效。 |
| `s.erase(first,last)`：删除 `[first,last)` 并返回区间之后的新位置，复杂度 $O(\log n+k)$。 |
| `s.find(key)`、`s.count(key)`：查位置或返回 `0/1`，$O(\log n)$；C++17 无 `contains`。 |
| `s.lower_bound(x)`：首个 `>=x`；`s.upper_bound(x)`：首个 `>x`，均 $O(\log n)$。 |
| `s.equal_range(x)`：返回两个界组成的迭代器对，$O(\log n)$。 |
| `s.begin()`、`s.rbegin()`：默认比较器下分别为最小、最大元素；取迭代器 $O(1)$。 |
| `s.extract(key/it)`：C++17 取出节点，可改键后重新插入。 |
| `s.merge(other)`：C++17 转移不重复节点，冲突键留在 `other`。 |
| `set_union/intersection/difference`：对两个已排序区间做集合运算，时间与总长度线性。 |
| `sort/reverse/next_permutation`：不能直接用；树迭代器非随机访问且键只读。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `if (s.find(x) != s.end())` 或 `if (s.count(x))`：判存在。 |
| `auto [it, inserted] = s.insert(x);`：取得位置及是否首次插入。 |
| `s.lower_bound(x)`、`s.upper_bound(x)`：最小的 `>=x`、`>x`。 |
| `auto it=s.upper_bound(x); if(it!=s.begin()) --it;`：最大的 `<=x`。 |
| `auto it=s.lower_bound(x); if(it!=s.begin()) --it;`：最大的 `<x`。 |
| `*s.begin()`、`*s.rbegin()`：最小值、最大值；必须先判空。 |
| `s.erase(s.begin())`、`s.erase(prev(s.end()))`：删除最小值、最大值。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
// 集合不能为空；差相同时返回较小值。
int nearestValue(const set<int>& values, int x) {
    auto right = values.lower_bound(x);
    if (right == values.begin()) return *right;
    if (right == values.end()) return *prev(right);
    auto left = prev(right);
    long long dl = (long long)x - *left;
    long long dr = (long long)*right - x;
    return dl <= dr ? *left : *right;
}
```

**易错点。**

- 键通过迭代器是只读的；要改键可在 C++17 使用 `extract`。
- 优先调用成员 `lower_bound/upper_bound`；泛型版本对树迭代器的移动可能为线性。
- `--begin()` 和解引用 `end()` 均未定义，前驱后继必须检查边界。
- 比较器必须满足严格弱序。`set` 不支持按排名取第 $k$ 小。

**参考：**

- [OI Wiki：关联式容器](https://oi-wiki.org/lang/csl/associative-container/)

## 2.14 `multiset`

`std::multiset<Key>` 是允许重复键的有序关联容器，通常由平衡树实现。它适合动态维护可重复数据、滑动窗口中位数、反复取最小/最大值和支持删除指定一次的“可删除堆”。插入、查找和界查询为 $O(\log n)$；遍历 $O(n)$。它比 `priority_queue` 多了查找、删除任意已知值和双端取值，但节点开销与常数更高。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
multiset<int> ms;
multiset<int, greater<int>> descending;
multiset<int> initialized{3, 1, 3, 2};  // 1、2、3、3
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `ms.empty()/size()/clear()`：判空、计数、清空；清空为 $O(n)$。 |
| `ms.insert(x)`、`ms.emplace(...)`：总会插入一项，$O(\log n)$，返回迭代器。 |
| `ms.erase(key)`：删除所有等于 `key` 的元素，返回数量，$O(\log n+k)$。 |
| `ms.erase(it)`：只删除迭代器所指的一次出现并返回下一位置，均摊 $O(1)$。 |
| `ms.erase(first,last)`：删除 `[first,last)`，返回区间之后的新位置，复杂度 $O(\log n+k)$。 |
| `ms.find(key)`：找某次出现，$O(\log n)$；不存在返回 `end()`。 |
| `ms.count(key)`：出现次数，$O(\log n+k)$。 |
| `ms.lower_bound/upper_bound/equal_range`：等值范围的左右界，$O(\log n)$。 |
| `ms.begin()`、`ms.rbegin()`：默认比较器下为最小、最大元素。 |
| `ms.extract(it)`、`ms.merge(other)`：C++17 取节点或转移节点。 |
| `sort/reverse/next_permutation`：不能直接用；迭代器非随机访问且元素只读。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `ms.insert(x)`：加入一次 `x`。 |
| `auto it=ms.find(x); if(it!=ms.end()) ms.erase(it);`：只删除一次 `x`。 |
| `ms.erase(x)`：删除所有 `x`，不要误用于删除一次。 |
| `*ms.begin()`、`*ms.rbegin()`：最小值、最大值。 |
| `ms.erase(ms.begin())`、`ms.erase(prev(ms.end()))`：删除一次最小/最大值。 |
| `distance(ms.lower_bound(l), ms.upper_bound(r))`：虽能区间计数，但移动为线性，不宜频繁用。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> slidingWindowMinimum(const vector<int>& a, int k) {
    vector<int> ans;
    if (k <= 0 || k > (int)a.size()) return ans;
    multiset<int> window;
    for (int i = 0; i < (int)a.size(); ++i) {
        window.insert(a[i]);
        if (i >= k) {
            auto it = window.find(a[i - k]);
            window.erase(it);  // 只删离开窗口的这一次
        }
        if (i >= k - 1) ans.push_back(*window.begin());
    }
    return ans;
}
```

**易错点。**

- `erase(value)` 删除全部相等元素；只删一次必须 `find` 后删迭代器。
- 要区分相同键个体，可存 `{value, unique_id}`。
- `distance` 在 `multiset` 上是 $O(n)$，不能高效做排名或区间计数。
- 只需反复取最小值且不删任意值时，`priority_queue` 通常更快。

**参考：**

- [OI Wiki：关联式容器](https://oi-wiki.org/lang/csl/associative-container/)

## 2.15 `map`

`std::map<Key,T>` 是键唯一的有序映射，通常由平衡树实现。它适合动态计数、稀疏下标、按键排序输出、前驱后继，以及需要稳定最坏 $O(\log n)$ 的场景。查找、插入、更新、删除和界查询均为 $O(\log n)$，遍历 $O(n)$，空间 $O(n)$。不需要键序时可选 `unordered_map`；一个键对应多个值可用 `map<Key,vector<T>>` 或 `multimap`。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
map<string, int> frequency;
map<int, int, greater<int>> descending;
map<string, int> initialized{{"alice", 3}, {"bob", 5}};
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `mp.empty()/size()/clear()`：判空 $O(1)$、计数 $O(1)$、清空 $O(n)$。 |
| `mp[key]`：返回值引用；缺键会插入 `{key,T{}}`，$O(\log n)$，有副作用。 |
| `mp.at(key)`：不插入；缺键抛 `out_of_range`，$O(\log n)$。 |
| `mp.insert({key,value})`：缺键才插入，返回 `pair<iterator,bool>`，$O(\log n)$。 |
| `mp.emplace(...)`：原地构造；`try_emplace(key,args...)` 仅缺键时构造值（C++17）。 |
| `mp.insert_or_assign(key,value)`：C++17 不存在则插入、存在则覆盖，$O(\log n)$。 |
| `mp.find(key)`、`mp.count(key)`：返回迭代器或 `0/1`，$O(\log n)$；C++17 无 `contains`。 |
| `mp.erase(key)`：按键删除并返回 `0/1`，$O(\log n)$。 |
| `mp.erase(it)`：删除当前位置并返回下一位置，均摊 $O(1)$；只有被删元素失效。 |
| `mp.erase(first,last)`：删除 `[first,last)` 并返回区间之后的新位置，复杂度 $O(\log n+k)$。 |
| `mp.lower_bound(x)`、`upper_bound(x)`：按键找首个 `>=x`、`>x`，$O(\log n)$。 |
| `mp.begin()`、`mp.rbegin()`：默认比较器下为最小键、最大键。 |
| `mp.extract/merge`：C++17 取节点、转移不冲突节点。 |
| `sort/reverse/next_permutation`：不能直接用；迭代器非随机访问且键只读。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `++frequency[x]`：首次出现自动插入零值再加一。 |
| `if (mp.find(x) != mp.end())`：无副作用判存在。 |
| `for (auto& [key,value] : mp)`：按键顺序遍历，可改值但不能改键。 |
| `mp[key] = value`：插入或覆盖；昂贵值考虑 `insert_or_assign`。 |
| `auto [it,ok] = mp.try_emplace(key,args...);`：避免无谓构造值。 |
| `mp.lower_bound(x)`、`prev(mp.upper_bound(x))`：按键找后继、前驱；后者先查边界。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<pair<string, int>> countSorted(const vector<string>& words) {
    map<string, int> frequency;
    for (const string& word : words) ++frequency[word];
    vector<pair<string, int>> answer;
    for (const auto& [word, count] : frequency)
        answer.push_back({word, count});  // map 已按键排序
    return answer;
}
```

**易错点。**

- 只查询不要写 `mp[key]`：缺键会被插入，改变 `size()` 并可能浪费内存。
- `const map` 不能用 `operator[]`；用 `find` 或 `at`。
- 迭代器解引用得到 `pair<const Key,T>`：键不可改、值可改。
- 比较器须满足严格弱序；只比较部分字段可能把不同对象视为同键。
- `distance` 在 `map` 上是线性的，不能高效求排名。

**参考：**

- [OI Wiki：关联式容器](https://oi-wiki.org/lang/csl/associative-container/)

## 2.16 `multimap`

`std::multimap<Key,T>` 是允许重复键的有序键值容器，同一键可对应多条独立记录。适合按键排序且频繁增删单条记录的场景，例如时间到事件、分数到选手。查找、插入和界查询 $O(\log n)$，遍历一个键的全部 $k$ 项还需 $O(k)$。若主要整组处理，`map<Key,vector<T>>` 往往更直观、内存更省。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
multimap<int, string> events;
multimap<int, string> initialized{{10, "A"}, {5, "B"}, {10, "C"}};
multimap<int, string, greater<int>> descending;
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `mm.empty()/size()/clear()`：判空、计数、清空；清空 $O(n)$。 |
| `mm.insert({key,value})`、`emplace(key,value)`：总会新增，$O(\log n)$，返回迭代器。 |
| `mm.find(key)`：返回该键的某项，$O(\log n)$；不存在返回 `end()`。 |
| `mm.count(key)`：出现次数，$O(\log n+k)$。 |
| `mm.lower_bound/upper_bound/equal_range`：同键范围的左右界，$O(\log n)$。 |
| `mm.erase(key)`：删除该键全部记录并返回删除数量，$O(\log n+k)$。 |
| `mm.erase(it)`：只删迭代器所指的一条并返回下一位置，均摊 $O(1)$；区间版本删除 `[first,last)`，复杂度 $O(\log n+k)$。 |
| `mm.begin()/rbegin()`：访问比较器顺序下的首、尾记录。 |
| `mm.extract/merge`：C++17 取节点或转移节点。 |
| `operator[]`、`at`：不存在，因为一个键可能有多个值。 |
| `sort/reverse/next_permutation`：不能直接用；迭代器非随机访问且键只读。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `auto [first,last] = mm.equal_range(key);`：取得该键全部记录。 |
| `for(auto it=first; it!=last; ++it) use(it->second);`：遍历该键所有值。 |
| `mm.erase(key)`：删除该键全部记录。 |
| `auto it=mm.find(key); if(it!=mm.end()) mm.erase(it);`：只删除一条。 |
| `for (auto& [key,value] : mm)`：按键顺序遍历全部记录。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<string> valuesForKey(const multimap<int, string>& mm, int key) {
    vector<string> answer;
    auto [first, last] = mm.equal_range(key);
    for (auto it = first; it != last; ++it)
        answer.push_back(it->second);  // 只遍历该键的连续区间
    return answer;
}
```

**易错点。**

- 无 `operator[]`；用 `insert/emplace` 添加、`equal_range` 取全部值。
- `erase(key)` 会删同键全部记录；只删一条用迭代器版本。
- C++11 起等价键元素的相对顺序保持不变；若题意要求按第二关键字排序，仍应把第二关键字纳入复合键。
- 整组存取优先考虑 `map<Key,vector<T>>`；频繁删除单条时 `multimap` 更方便。

**参考：**

- [OI Wiki：关联式容器](https://oi-wiki.org/lang/csl/associative-container/)

## 2.17 `unordered_set`

`std::unordered_set<Key>` 是不重复键的哈希集合，不保持排序。平均插入、删除、查找 $O(1)$，最坏因冲突退化到 $O(n)$，空间 $O(n)$。适合只判存在或去重且不需要前驱后继的场景。相比 `set` 通常常数更小，但遍历顺序不确定、桶有额外内存；要求稳定最坏复杂度时用 `set`。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
unordered_set<int> us;
unordered_set<string> names{"alice", "bob"};
unordered_set<int> reserved;  // 填充前可调用 reserve() 与 max_load_factor()
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `us.empty()/size()/clear()`：判空、计数、清空；清空 $O(n)$。 |
| `us.insert(x)`：平均 $O(1)$、最坏 $O(n)$，返回 `pair<iterator,bool>`。 |
| `us.emplace(...)`：直接构造并尝试插入，复杂度同上。 |
| `us.find(key)`、`us.count(key)`：查位置或返回 `0/1`，平均 $O(1)$、最坏 $O(n)$；C++17 无 `contains`。 |
| `us.erase(key)`：删除该键并返回 `0/1`；`erase(it)` 删除当前位置并返回下一位置。平均 $O(1)$、最坏 $O(n)$，只使被删元素失效。 |
| `us.reserve(n)`：按当前最大负载率预留至少容纳 `n` 个元素的桶，可能重哈希；平均 $O(n)$、最坏 $O(n^2)$。 |
| `us.rehash(b)`：令桶数至少为 `b` 且满足负载率要求；平均 $O(n)$、最坏 $O(n^2)$，不删除元素。 |
| `us.load_factor()`：返回 `size()/bucket_count()`；`us.max_load_factor(z)` 读写自动扩容阈值。 |
| `bucket_count/bucket_size(i)`：桶数、第 `i` 桶大小，用于诊断哈希质量。 |
| `begin/end`：可遍历但顺序未指定；发生重哈希时全部迭代器失效，但元素引用和指针仍有效。 |
| `lower_bound/upper_bound`：不存在；`sort/reverse/next_permutation` 也不能直接用。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `if (us.insert(x).second)`：判断 `x` 是否首次出现。 |
| `if (us.find(x)!=us.end())` 或 `if (us.count(x))`：判存在。 |
| `us.max_load_factor(0.7f); us.reserve(expected);`：先设负载率再按预计元素数预留，减少扩容。 |
| `unordered_set<long long> seen; seen.insert(encode(x,y));`：编码状态后去重。 |
| `vector<int> v(us.begin(),us.end()); sort(v.begin(),v.end());`：需确定顺序时复制排序。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> uniqueInInputOrder(const vector<int>& a) {
    unordered_set<int> seen;
    seen.reserve(a.size() * 2 + 1);
    vector<int> answer;
    for (int x : a)
        if (seen.insert(x).second) answer.push_back(x);
    return answer;
}
```

### 自定义哈希模板

```cpp
#include <bits/stdc++.h>
using namespace std;

struct CustomHash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }

    size_t operator()(uint64_t x) const {
        static const uint64_t seed =
            chrono::steady_clock::now().time_since_epoch().count();
        return static_cast<size_t>(splitmix64(x + seed));
    }

    size_t operator()(const pair<int, int>& p) const {
        // 转为 uint32_t 后拼成 64 位；负数也会保留其低 32 位编码。
        uint64_t high = static_cast<uint32_t>(p.first);
        uint64_t low = static_cast<uint32_t>(p.second);
        return (*this)((high << 32) | low);
    }
};

unordered_set<long long, CustomHash> numbers;
unordered_set<pair<int, int>, CustomHash> states;
unordered_map<long long, int, CustomHash> frequency;
```

**易错点。**

- 不依赖遍历顺序；重哈希、实现或运行环境变化都可能改变顺序。
- `reserve/rehash` 只有实际重哈希时才使全部迭代器失效；插入触发自动重哈希时同理。元素引用和指针在重哈希后仍有效。
- `erase` 只使被删元素的迭代器、引用和指针失效；未发生重哈希的插入不使迭代器失效。
- 自定义键需提供相容的哈希和相等判断：相等对象必须有相同哈希。
- 对抗性输入可能制造冲突；必要时随机扰动哈希或改用 `set`。
- 需要最值、前驱后继或有序输出时使用 `set`。

**参考：**

- [OI Wiki：无序关联式容器](https://oi-wiki.org/lang/csl/unordered-container/)
- [OI Wiki：哈希表](https://oi-wiki.org/ds/hash/)

## 2.18 `unordered_map`

`std::unordered_map<Key,T>` 是键唯一的哈希映射，不保持顺序。平均查找、插入、更新和删除 $O(1)$，最坏 $O(n)$，空间 $O(n)$。它适合频率统计、状态到编号、稀疏 DP 和记忆化；若需要按键排序、范围查询或稳定最坏复杂度，用 `map`。键域小且可直接开数组时，数组通常更快。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
unordered_map<string, int> frequency;
unordered_map<int, string> initialized{{1, "one"}, {2, "two"}};
unordered_map<long long, int> memo;  // 填充前可调用 reserve() 与 max_load_factor()
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `mp.empty()/size()/clear()`：判空、计数、清空；清空 $O(n)$。 |
| `mp[key]`：缺键会插入 `{key,T{}}` 并返回值引用，有副作用；平均 $O(1)$、最坏 $O(n)$。 |
| `mp.at(key)`：不插入；缺键抛 `out_of_range`，平均 $O(1)$、最坏 $O(n)$。 |
| `mp.insert({key,value})`：仅缺键时插入，返回 `pair<iterator,bool>`；平均 $O(1)$、最坏 $O(n)$。 |
| `mp.emplace(...)`：尝试原地构造；`try_emplace(key,args...)` 仅缺键时构造值（C++17）；平均 $O(1)$、最坏 $O(n)$。 |
| `mp.insert_or_assign(key,value)`：C++17 插入或覆盖；上述操作平均 $O(1)$、最坏 $O(n)$。 |
| `mp.find(key)`、`mp.count(key)`：查位置或返回 `0/1`；平均 $O(1)$、最坏 $O(n)$，C++17 无 `contains`。 |
| `mp.erase(key)`：删除键并返回 `0/1`；`erase(it)` 删除当前位置并返回下一位置。平均 $O(1)$、最坏 $O(n)$。 |
| `mp.reserve(n)`：按当前最大负载率预留 `n` 个元素所需桶；`mp.rehash(b)` 设置最少桶数。二者可能重哈希，平均 $O(n)$、最坏 $O(n^2)$。 |
| `load_factor/max_load_factor/bucket_count`：观察当前负载率、设置自动扩容阈值或查询桶数。 |
| `begin/end`：可遍历但顺序未指定；键只读、值可修改。重哈希使迭代器失效，但元素引用和指针仍有效。 |
| `lower_bound/upper_bound`：不存在；`sort/reverse/next_permutation` 也不能直接用。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `++frequency[x]`：频率统计，缺键时先插入零值。 |
| `auto it=mp.find(x); if(it!=mp.end()) use(it->second);`：无副作用查询。 |
| `mp.max_load_factor(0.7f); mp.reserve(expected);`：先设最大负载率，再按预计元素数预留。 |
| `if (mp.emplace(key,value).second)`：判断是否首次插入。 |
| `mp.try_emplace(key, expensiveArgs...)`：键存在时不构造昂贵值。 |
| `vector<pair<K,V>> v(mp.begin(),mp.end()); sort(v.begin(),v.end());`：需有序输出时复制排序。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
// 返回第一对和为 target 的下标；不存在返回 {-1,-1}。
pair<int, int> twoSum(const vector<int>& a, int target) {
    unordered_map<int, int> firstPosition;
    firstPosition.reserve(a.size() * 2 + 1);
    for (int i = 0; i < (int)a.size(); ++i) {
        auto it = firstPosition.find(target - a[i]);
        if (it != firstPosition.end()) return {it->second, i};
        firstPosition.try_emplace(a[i], i);  // 保留首次出现位置
    }
    return {-1, -1};
}
```

**易错点。**

- 只读查询不要用 `mp[key]`，否则插入默认值并可能触发重哈希。
- 不依赖遍历顺序；自动重哈希会使全部迭代器失效，但指向元素的引用和指针仍有效。
- `erase` 只使被删元素失效；插入仅在触发重哈希时使迭代器失效。
- 自定义键必须保证：若 `a==b`，则两者哈希值相同。
- 可直接复用上一节的 `CustomHash`：如 `unordered_map<long long,int,CustomHash>`。
- 对抗性数据下可能退化；高安全性场景用 `map` 或随机哈希。
- 可直接开数组且键域不大时，数组通常更快、常数更小。

**参考：**

- [OI Wiki：无序关联式容器](https://oi-wiki.org/lang/csl/unordered-container/)
- [OI Wiki：哈希表](https://oi-wiki.org/ds/hash/)

## 2.19 `bitset`

`std::bitset<N>` 是长度在编译期确定的二进制位容器，每位只能是 `0` 或 `1`。它比 `bool` 数组节省空间，并能按机器字批量位运算，常用于集合表示、状态压缩、可达性 DP、字符集合和布尔矩阵优化。

单点操作通常 $O(1)$；整组与、或、异或、移位和计数约为 $O(N/w)$，其中 $w$ 为机器字长，空间为 $O(N/w)$ 个机器字。`N` 必须是编译期常量；长度运行时才确定时应使用整数块数组或其他动态位集。

### 定义与初始化

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1000;
bitset<N> a;                    // 全部为 0
bitset<8> b(13);                // 00001101
bitset<8> c("10110010");        // 字符串最右端对应第 0 位
bitset<4> d(string("110101"), 1, 4);  // 读取子串 "1010"
```

字符串最右边对应第 `0` 位；`bitset<4>("1010")` 从左到右的位编号为 `3,2,1,0`。

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `bitset<N> b;`：固定长度位集，默认全零；`N` 必须是编译期常量。 |
| `bitset<N> b(value)`：用整数低 `N` 位初始化；超出整数位宽的高位为零。 |
| `bitset<N> b(string)`：用 `0/1` 字符串初始化，最右字符为第 `0` 位。 |
| `b.size()`：返回位数 `N`，$O(1)$。 |
| `b[i]`：不检查越界；非常量 `bitset` 返回代理引用，可读写但不是 `bool&`，常量对象返回 `bool`。 |
| `b.test(i)`：读取第 `i` 位并检查越界；越界抛异常，$O(1)$。 |
| `b.set()`、`b.reset()`、`b.flip()`：全部置一、清零、翻转，约 $O(N/w)$。 |
| `b.set(i)`、`b.reset(i)`、`b.flip(i)`：操作单个位，$O(1)$；`set(i,value)` 可赋布尔值。 |
| `b.count()`：返回一的个数，约 $O(N/w)$。 |
| `b.any()`、`b.none()`、`b.all()`：是否有一、是否全零、是否全一，约 $O(N/w)$。 |
| `b.to_string()`：转长度 `N` 的 `01` 字符串，高位在左，$O(N)$；也可传自定义的零、壹字符。 |
| `b.to_ulong()`、`b.to_ullong()`：转无符号整数；不能容纳时抛 `overflow_error`。 |
| `a & b`：按位与；`a \| b`：按位或；`a ^ b`：异或；`~a`：翻转有效的 `N` 位。二元运算要求两者长度相同。 |
| `a &= b`、`a \|= b`、`a ^= b`：原地位运算，会修改左操作数。 |
| `a << k`、`a >> k`：整体移位，移出位丢弃、空位补零；`<<=`、`>>=` 原地修改。 |
| `a == b`、`a != b`：比较相同长度位集，约 $O(N/w)$。 |
| `a[i].flip()`、`a[i] = b[j]`：通过代理引用翻转或复制单个位。 |
| `swap(a,b)`：交换相同长度位集，约 $O(N/w)$。 |
| `cin >> b`：最多读取 `N` 个 `0/1` 字符；`cout << b`：从高到低输出完整 `N` 位。 |
| `sort/reverse/next_permutation`：不能直接用，因为没有 `begin/end` 和迭代器；需要时先 `to_string()`。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `(a & b).count()`：两个集合交集大小。 |
| `(a \| b).count()`：两个集合并集大小。 |
| `(a & b).any()`：是否存在公共元素。 |
| `(a & ~b).none()`：判断 `a` 是否为 `b` 的子集。 |
| `b.set(x)`、`b.reset(x)`、`b.test(x)`：加入、删除、查询元素 `x`。 |
| `reachable \|= reachable << weight`：0-1 背包批量更新所有可达和。 |
| `(adj[u] & adj[v]).count()`：统计两点公共邻居。 |
| `letters.set(ch-'a')`：记录出现过的英文字母。 |

### 示例模板

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int MAX_SUM = 100000;

bitset<MAX_SUM + 1> subsetSums(const vector<int>& weights) {
    bitset<MAX_SUM + 1> reachable;
    reachable.set(0);  // 空集的和为 0
    for (int weight : weights) {
        // 原第 s 位为 1，左移后第 s+weight 位为 1；
        // |= 同时保留“不选当前物品”的旧状态。
        reachable |= reachable << weight;
    }
    return reachable;
}

int main() {
    auto reachable = subsetSums({2, 3, 7});
    cout << reachable.test(5) << '\n';  // 1：2+3
    cout << reachable.test(6) << '\n';  // 0
    cout << reachable.test(9) << '\n';  // 1：2+7
}
```

**易错点。**

- 长度不能由输入决定，不能写 `bitset<n>`。
- `operator[]` 不检查越界；下标不确定时使用 `test()`。
- `~b` 只翻转声明范围内的 `N` 位；移动不少于 `N` 位时结果全零。
- `to_ullong()` 不是截取低 64 位；高位有一时可能抛异常。
- 没有迭代器，不能直接使用 `sort`、`reverse`、`next_permutation` 或范围 `for`。
- `vector<bool>` 长度可动态变化，但与 `bitset` 的接口和性能不同。
- 可达性 DP 的位数必须覆盖最大可能和；超出 `MAX_SUM` 的状态会被静默丢弃，模板中的 `weight` 必须非负。

**参考：**

- [OI Wiki：bitset](https://oi-wiki.org/lang/csl/bitset/)
## 2.20 排序与选择

`<algorithm>` 中的排序与选择算法都处理半开区间 `[first, last)`。`sort` 适合绝大多数需要整体有序的场景；若相等元素的原相对次序有意义，使用 `stable_sort`。只需要第 $k$ 小或最小的前 $k$ 项时，`nth_element`、`partial_sort` 通常比完整排序更合适。

这些算法默认使用 `operator<`，也可传入比较器 `comp(a,b)`。比较器必须满足严格弱序：`comp(x,x)` 永远为假，且顺序具有传递性；写成 `a <= b` 会破坏算法前提。`sort`、`stable_sort`、`nth_element` 和 `partial_sort` 会重排原区间；`partial_sort_copy`、`is_sorted` 与 `is_sorted_until` 不修改输入。重排通常不使 `vector` 迭代器失效，但迭代器所在位置保存的元素可能已经改变。

### 基本调用

```cpp
#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int main() {
    vector<int> a = {5, 1, 4, 1, 3};
    sort(a.begin(), a.end());                    // 升序
    sort(a.begin(), a.end(), greater<int>());    // 降序
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `sort(first, last)`：将随机访问区间按升序排序；平均及最坏复杂度均为 $O(n\log n)$，不保证相等元素的原相对次序。 |
| `sort(first, last, comp)`：按严格弱序 `comp` 排序。`vector`、`array`、原生数组可用；`list` 迭代器不是随机访问迭代器，应调用 `list::sort()`。 |
| `stable_sort(first, last)`：稳定升序排序；额外内存充足时通常为 $O(n\log n)$，内存不足时可退化到 $O(n\log^2 n)$；可能分配 $O(n)$ 辅助空间。 |
| `stable_sort(first, last, comp)`：按 `comp` 稳定排序；适合先按次关键字排序、再按主关键字稳定排序，或必须保留输入先后顺序的场景。 |
| `is_sorted(first, last)` / `is_sorted(first, last, comp)`：判断区间是否已有序，线性检查，复杂度 $O(n)$，不修改区间。 |
| `is_sorted_until(first, last)`：返回最长有序前缀的尾后迭代器；全部有序时返回 `last`，复杂度 $O(n)$。 |
| `nth_element(first, nth, last)`：重排后 `*nth` 等于完整排序后该位置的值；其左侧元素均不大于它、右侧均不小于它，但两侧内部无序。平均复杂度 $O(n)$，会修改原区间。 |
| `nth_element(first, nth, last, comp)`：按 `comp` 选择顺序统计量；`nth` 可位于 `[first,last]`。只有 `nth!=last` 时才存在可读取的第 `nth-first` 小元素；选第 $k$ 小须保证 `0<=k<n`。 |
| `partial_sort(first, middle, last)`：把最小的 `middle-first` 个元素按升序放到 `[first,middle)`；后半段顺序未指定。复杂度约 $O(n\log k)$，其中 $k=middle-first$。 |
| `partial_sort(first, middle, last, comp)`：按 `comp` 选出并排序前 $k$ 项；若 `middle==first` 不产生已排序结果，若 `middle==last` 等价于完整排序。 |
| `partial_sort_copy(first, last, outFirst, outLast)`：不修改输入，把最小的至多 $k$ 项有序复制到输出区间，返回输出尾后迭代器；复杂度约 $O(n\log k)$。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `sort(a.begin(), a.end());`：整体升序。 |
| `sort(a.rbegin(), a.rend());`：利用反向迭代器整体降序。 |
| `sort(a.begin(), a.end(), [](const auto& x, const auto& y){ return tie(x.first,x.second) < tie(y.first,y.second); });`：多关键字排序。 |
| `nth_element(a.begin(), a.begin()+k, a.end()); int kth=a[k];`：取得 0-based 第 `k` 小，平均 $O(n)$。 |
| `nth_element(a.begin(), a.begin()+n/2, a.end());`：取得中位数；偶数长度时若需两个中位数，要另行选择或排序。 |
| `partial_sort(a.begin(), a.begin()+k, a.end());`：得到升序的最小 $k$ 个元素。 |
| `stable_sort(id.begin(), id.end(), [&](int i,int j){ return score[i]>score[j]; });`：按分数降序且同分保持原顺序。 |

### 选择第 k 小示例

```cpp
#include <bits/stdc++.h>
using namespace std;

int kthSmallest(vector<int> values, int k) {
    // k 为 0-based；按值传参，避免打乱调用者的数组。
    if (k < 0 || k >= static_cast<int>(values.size())) {
        throw out_of_range("kthSmallest");
    }
    nth_element(values.begin(), values.begin() + k, values.end());
    return values[k];
}

int main() {
    cout << kthSmallest({7, 2, 5, 2, 9}, 2) << '\n'; // 5
}
```

**易错点。**

- `sort` 不稳定；不要依赖相等元素排序后的先后顺序。
- 比较器必须写“严格小于”，不能用 `<=`，也不能随调用改变结果。
- `nth_element` 只保证分区性质，不保证左右两段有序。
- `partial_sort(a.begin(), a.begin()+k, a.end())` 要保证 `0 <= k <= a.size()`。
- 结构体比较器参数优先用 `const T&`，避免排序时产生大量复制。

**参考：**

- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
- [OI Wiki：排序简介](https://oi-wiki.org/basic/sort-intro/)

## 2.21 查找、最值与二分

线性查找算法不要求区间有序，适合寻找某个值、满足谓词的首项或统计出现次数。二分查找系列通过反复折半，在已按同一规则排序的区间上以 $O(\log n)$ 次比较定位边界，是离散化、频次统计和有序容器查询的基础。

最关键的约定是返回值通常为迭代器：找不到时返回 `last`，使用 `*it` 前必须检查。`lower_bound` 找第一个“不小于目标”的位置，`upper_bound` 找第一个“大于目标”的位置；二者相减得到目标出现次数。标准的精确前置条件是区间对“元素与本次查询值的比较表达式”已经分区；把整个区间按同一比较器排序是竞赛中最常用、最容易验证的充分条件。若排序和查询使用不兼容的规则，结果不可靠。

### 基本调用

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> a = {1, 2, 2, 2, 5, 8}; // 二分前必须有序
    auto first = lower_bound(a.begin(), a.end(), 2);
    auto after = upper_bound(a.begin(), a.end(), 2);
    int frequency = static_cast<int>(after - first); // 3
    (void)frequency;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `find(first, last, value)`：线性寻找首个等于 `value` 的元素，找到则返回其迭代器，否则返回 `last`；复杂度 $O(n)$。 |
| `find_if(first, last, pred)`：返回首个使 `pred(x)` 为真的元素；`find_if_not` 返回首个为假的元素；均为 $O(n)$。 |
| `count(first, last, value)` / `count_if(first, last, pred)`：统计相等元素或满足谓词的元素数量；完整扫描，复杂度 $O(n)$。 |
| `min(a,b)` / `max(a,b)`：返回两者中较小/较大者的 `const` 引用；可传比较器。不要保存对临时对象返回值的长期引用。 |
| `min({a,b,c})` / `max({a,b,c})`：对初始化列表求最值，返回值；比较次数线性。 |
| `minmax(a,b)`：一次得到 `{min,max}`；`minmax({ ... })` 处理初始化列表。相等时具体选择规则与单独调用可能不同，不应依赖对象身份。 |
| `min_element(first,last)` / `max_element(first,last)`：返回最值迭代器；空区间返回 `last`，复杂度 $O(n)$。可传 `comp`。 |
| `minmax_element(first,last)`：一次扫描返回 `{最小值迭代器, 最大值迭代器}`，复杂度 $O(n)$；空区间二者均为 `last`。 |
| `lower_bound(first,last,value)`：在按升序分区的区间返回首个 `x >= value` 的位置；比较次数 $O(\log n)$。随机访问迭代器上移动也是 $O(\log n)$。 |
| `upper_bound(first,last,value)`：返回首个 `x > value` 的位置；复杂度与前置条件同 `lower_bound`。 |
| `binary_search(first,last,value)`：判断有序区间中是否存在目标，返回 `bool`；比较次数 $O(\log n)$，不提供位置。 |
| `equal_range(first,last,value)`：返回 `{lower_bound, upper_bound}`，即所有等于目标元素组成的半开区间；比较次数 $O(\log n)$。 |
| `lower_bound/upper_bound/equal_range(..., comp)`：支持自定义顺序；区间必须已按与查询兼容的 `comp` 分区。对结构体异构查询时要注意参数方向。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `int pos = lower_bound(a.begin(),a.end(),x)-a.begin();`：第一个 `>=x` 的 0-based 下标，若不存在则等于 `a.size()`。 |
| `int pos = upper_bound(a.begin(),a.end(),x)-a.begin();`：第一个 `>x` 的下标。 |
| `int cnt = upper_bound(a.begin(),a.end(),x)-lower_bound(a.begin(),a.end(),x);`：有序数组中 `x` 的出现次数。 |
| `auto [lo,hi] = equal_range(a.begin(),a.end(),x);`：取得所有 `x` 的迭代器区间 `[lo,hi)`。 |
| `auto it=max_element(a.begin(),a.end()); if(it!=a.end()) ...`：先判空再解引用最值。 |
| `find_if(a.begin(),a.end(),[](int x){return x<0;});`：寻找首个负数。 |
| `lower_bound(a.begin(),a.end(),x,greater<int>())`：在已经降序的数组上找第一个按降序规则不先于 `x` 的位置；不能拿升序数组直接查询。 |

**易错点。**

- 对未排序区间调用二分系列，程序通常不会报错，但返回结果不可靠。
- `set::lower_bound`、`map::lower_bound` 应调用成员函数；对树迭代器使用通用算法虽比较次数为对数，迭代器移动可能是线性的。
- 找不到目标时迭代器等于 `end()`，不可解引用。
- 浮点数含 `NaN` 时不能形成正常严格顺序，排序与二分都需谨慎。
- 二分答案使用谓词时见基础算法章节；本节函数是在已排序元素区间上查位置。

**参考：**

- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
- [OI Wiki：二分](https://oi-wiki.org/basic/binary/)

## 2.22 去重、删除与分区

标准算法不能改变 `vector`、`string` 等容器的实际长度，因此 `unique` 和 `remove` 只会把“保留的元素”移动到前部，并返回新的逻辑结尾。要真正缩短容器，必须再调用成员 `erase`，这就是 erase-remove 写法。`unique` 只消除相邻重复项；若要全局去重，通常先排序。

分区算法按照谓词把元素分成前后两组，不要求组内有序。`partition` 通常线性且不稳定，`stable_partition` 保持两组内部原相对次序但可能使用额外内存。它们都会重排原区间；若后续仍依赖原下标，应先保存索引或在副本上操作。

### 基本调用

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> a = {3, 1, 3, 2, 1};
    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end()); // {1,2,3}

    vector<int> b = {1, 2, 3, 4, 5};
    b.erase(remove_if(b.begin(), b.end(),
                      [](int x) { return x % 2 == 0; }),
            b.end());                              // {1,3,5}
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `unique(first,last)`：将相邻相等元素压缩为一个，返回新逻辑结尾；复杂度 $O(n)$。`[newEnd,last)` 中元素仍存在但值处于有效但未指定状态。 |
| `unique(first,last,pred)`：把相邻且满足 `pred(a,b)` 的元素视为等价；谓词应表达等价关系。 |
| `unique_copy(first,last,out)`：把相邻去重结果复制到输出，不修改输入，返回输出尾后迭代器；输入输出重叠限制较多，通常输出到另一容器。 |
| `remove(first,last,value)`：稳定地把不等于 `value` 的元素移动到前部，返回新逻辑结尾，复杂度 $O(n)$；不改变容器大小。 |
| `remove_if(first,last,pred)`：稳定保留使 `pred` 为假的元素；复杂度 $O(n)$，不改变容器大小。 |
| `remove_copy` / `remove_copy_if`：把保留元素复制到输出区间，不修改输入；调用者必须保证输出空间足够或使用插入迭代器，且输入与实际写入的输出区间不能重叠。 |
| `partition(first,last,pred)`：把谓词为真的元素移到前部，返回第二组起点；复杂度 $O(n)$，不保证组内相对顺序。 |
| `stable_partition(first,last,pred)`：稳定分区；额外内存足够时 $O(n)$，否则可能达到 $O(n\log n)$，可能分配 $O(n)$ 空间。 |
| `partition_copy(first,last,outTrue,outFalse,pred)`：分别复制到两个输出区间，返回两个输出尾后迭代器；不修改输入，复杂度 $O(n)$。 |
| `is_partitioned(first,last,pred)`：判断是否已按谓词分区，复杂度 $O(n)$。 |
| `partition_point(first,last,pred)`：在已经按同一谓词分区的区间中返回两组分界；谓词调用次数 $O(\log n)$，但非随机访问迭代器的移动总量可达 $O(n)$。未分区时结果不可靠。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `sort(a.begin(),a.end()); a.erase(unique(a.begin(),a.end()),a.end());`：排序后全局去重，整体 $O(n\log n)$。 |
| `a.erase(remove(a.begin(),a.end(),x),a.end());`：删除 `vector/string/deque` 中所有等于 `x` 的元素。 |
| `a.erase(remove_if(a.begin(),a.end(),pred),a.end());`：按条件删除。 |
| `auto mid=partition(a.begin(),a.end(),pred);`：`[begin,mid)` 满足谓词，`[mid,end)` 不满足。 |
| `int distinct=unique(a.begin(),a.end())-a.begin();`：只需要逻辑去重长度；只有相邻重复已聚集时才正确。 |

**易错点。**

- 不要只写 `a.erase(unique(...))`；`erase(pos)` 只删一个位置，应传 `[newEnd,a.end())`。
- `unique` 不会处理不相邻的相同值，全局去重前通常需要 `sort`。
- 算法名 `remove` 不会销毁元素，也不是 C 的文件删除函数；容器缩短由 `erase` 完成。
- 调用 `vector::erase` 后，删除位置及其后的迭代器和引用失效。
- `partition_point` 的输入必须已按同一谓词分区。

**参考：**

- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
- [OI Wiki：STL 容器](https://oi-wiki.org/lang/csl/container/)

## 2.23 排列、归并与集合运算

排列算法按当前比较顺序生成字典序相邻排列。若要枚举一个多重集合的所有不同排列，先排序，再从最小排列反复调用 `next_permutation`，直到它返回 `false`。最坏会生成 $n!$ 个排列，每次调整 $O(n)$，只适合很小的 $n$。

归并与集合算法都要求输入区间已经按同一比较器排序。`merge` 保留重复元素，是两个有序序列的归并；`set_union`、`set_intersection` 等按多重集合语义决定每个值出现次数。输出空间必须足够，最稳妥的竞赛写法是 `back_inserter(result)`。

### 基本调用

```cpp
#include <algorithm>
#include <iterator>
#include <vector>
using namespace std;

int main() {
    vector<int> a = {1, 2, 2, 4};
    vector<int> b = {2, 2, 3};
    vector<int> intersection;
    set_intersection(a.begin(), a.end(), b.begin(), b.end(),
                     back_inserter(intersection)); // {2,2}
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `next_permutation(first,last)`：把区间变为下一字典序排列并返回 `true`；当前已是最大排列时变为最小排列并返回 `false`。单次 $O(n)$。 |
| `prev_permutation(first,last)`：变为上一字典序排列；当前为最小时变为最大并返回 `false`。单次 $O(n)$。 |
| `next_permutation/prev_permutation(...,comp)`：按严格弱序 `comp` 定义排列顺序。枚举前必须按同一规则排成最小/最大排列。 |
| `is_permutation(first1,last1,first2)`：判断两段是否包含相同元素及次数；最坏复杂度 $O(n^2)$，可传等价谓词。C++14 起另有带 `last2` 重载，可同时检查长度。三迭代器版本要求第二段至少有第一段那么长。 |
| `merge(first1,last1,first2,last2,out)`：稳定归并两个已排序区间到输出，复杂度 $O(n+m)$；重复项全部保留。输出不能与输入区间不安全重叠。 |
| `inplace_merge(first,middle,last)`：原地归并相邻的两个已排序区间 `[first,middle)` 和 `[middle,last)`；额外内存足够时线性，否则可能 $O(n\log n)$。 |
| `includes(first1,last1,first2,last2)`：判断第一个有序多重集合是否包含第二个，复杂度 $O(n+m)$。 |
| `set_union(...)`：输出有序并集；某值在两边出现 $p,q$ 次时输出 $\max(p,q)$ 次，复杂度 $O(n+m)$。 |
| `set_intersection(...)`：输出有序交集；出现次数为 $\min(p,q)$。 |
| `set_difference(A,B,out)`：输出有序差集 $A-B$；出现次数为 $\max(p-q,0)$。 |
| `set_symmetric_difference(...)`：输出有序对称差；出现次数为 $\lvert p-q\rvert$。 |
| `merge`、`includes`、所有 `set_*` 均有末尾 `comp` 重载；所有输入必须已经按兼容的 `comp` 排序。输出算法返回输出尾后迭代器。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `sort(p.begin(),p.end()); do { ... } while(next_permutation(p.begin(),p.end()));`：枚举不同字典序排列；重复值不会产生重复排列。 |
| `vector<int> c; merge(a.begin(),a.end(),b.begin(),b.end(),back_inserter(c));`：归并且保留两边全部重复项。 |
| `set_union(...,back_inserter(c));`：按多重集合语义求并集。若需要普通集合语义，先分别去重。 |
| `inplace_merge(a.begin(),a.begin()+mid,a.end());`：已知前后两段各自有序时线性/近线性合并。 |
| `includes(have.begin(),have.end(),need.begin(),need.end())`：检查需求多重集合是否被库存包含。 |

**易错点。**

- 从未排序序列开始调用 `next_permutation`，只能枚举当前位置之后的排列，不能保证覆盖全部排列。
- `next_permutation` 返回 `false` 时已经把序列重置为最小排列。
- 集合算法不是给 `set` 容器专用的；它们处理任意已排序迭代器区间。
- 多重集合的并、交次数与数学普通集合不同，需要时先 `sort + unique`。
- 用普通输出迭代器时必须预留足够空间；`back_inserter` 会自动 `push_back`。
- `merge` 与 `set_*` 的输出区间不能和任一输入区间重叠；不要一边遍历某个 `vector`，一边向同一个 `vector` 做 `back_inserter`。

**参考：**

- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
- [OI Wiki：排列与组合](https://oi-wiki.org/math/combinatorics/combination/)

## 2.24 `numeric` 数值算法

`<numeric>` 提供区间累加、前缀运算、相邻差分、内积、连续编号和整数最大公约数等工具。它们通常只需一次线性扫描，适合替代容易写错的简单循环。最重要的类型规则是：累加器类型由初值决定，`accumulate(..., 0)` 会按 `int` 累加，即使容器元素是 `long long`。

C++17 的 `reduce` 与扫描算法允许改变括号结合方式，便于并行实现；`reduce` 还可重排参与运算的元素。浮点加法不满足结合律，因此结果可能与从左到右的 `accumulate` 不同。需要严格左到右顺序时使用 `accumulate` 或 `partial_sum`；使用 `reduce` 时，为得到稳定含义，二元操作通常应同时满足结合律和交换律，扫描操作至少应能安全地重新结合。

### 基本调用

```cpp
#include <numeric>
#include <vector>
using namespace std;

int main() {
    vector<long long> a = {3, 5, 7};
    long long sum = accumulate(a.begin(), a.end(), 0LL); // 初值决定累加类型

    vector<long long> prefix(a.size());
    partial_sum(a.begin(), a.end(), prefix.begin());     // {3,8,15}
    (void)sum;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `accumulate(first,last,init)`：按从左到右的顺序计算 `init + x1 + ...`，复杂度 $O(n)$；返回类型是 `init` 的类型。 |
| `accumulate(first,last,init,op)`：反复执行 `init = op(init,*it)`；`op` 可用于乘积、拼接、结构体聚合等，顺序确定。 |
| `reduce(first,last,init)`：C++17 归约，允许改变结合顺序；操作应满足结合、交换要求，复杂度 $O(n)$。无执行策略版本也不保证严格左折叠。 |
| `reduce(first,last,init,op)`：按 `op` 归约。并行执行策略重载位于 `<execution>`，竞赛环境的链接支持不一定一致，通常不用。 |
| `inner_product(first1,last1,first2,init)`：计算两区间点积，左到右执行，复杂度 $O(n)$。第二段至少要有同样长度。 |
| `inner_product(...,opAdd,opMul)`：用 `opMul` 合并对应元素，再用 `opAdd` 聚合，可实现加权转移或相似度。默认乘法先按两个元素的类型计算；即使 `init` 为 `0LL`，两个 `int` 相乘仍可能先溢出。 |
| `partial_sum(first,last,out)`：输出包含当前项的前缀和；返回输出尾后迭代器，复杂度 $O(n)$。可传二元操作。C++17 中中间累加类型来自输入元素，单纯把输出容器改成 `long long` 不能防止 `int` 溢出。 |
| `adjacent_difference(first,last,out)`：首项原样输出，之后输出 `x[i]-x[i-1]`；可传二元操作，复杂度 $O(n)$。默认减法按输入元素类型进行，输出到更宽类型也不能挽救已发生的溢出。 |
| `inclusive_scan(first,last,out)`：C++17 包含当前元素的扫描，类似前缀和；可提供 `op` 和初值，结合顺序可能不同。 |
| `exclusive_scan(first,last,out,init)`：C++17 不包含当前元素的扫描，首个输出为 `init`。 |
| `transform_inclusive_scan` / `transform_exclusive_scan`：C++17 先对每项做一元变换，再扫描；用于平方前缀和等组合操作。 |
| `iota(first,last,value)`：依次写入 `value, ++value, ...`，复杂度 $O(n)$；常用于生成索引或初始排列。 |
| `gcd(a,b)`：C++17 最大公约数，结果非负；`gcd(0,0)==0`。参数绝对值必须能由公共类型表示。 |
| `lcm(a,b)`：C++17 最小公倍数；任一参数为 0 时结果为 0。若任一参数的绝对值或真实最小公倍数不能由公共类型表示，则行为未定义；应先判断范围或使用更宽类型。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `long long sum=accumulate(a.begin(),a.end(),0LL);`：以 `long long` 类型累加；仍须确认真实总和没有超过 `long long` 范围。 |
| `long long product=accumulate(a.begin(),a.end(),1LL,multiplies<long long>());`：求乘积；仍需自行处理溢出或取模。 |
| `iota(id.begin(),id.end(),0); sort(id.begin(),id.end(),comp);`：保持原数组不动，只排序索引。 |
| `int g=accumulate(a.begin(),a.end(),0,[](int x,int y){return gcd(x,y);});`：整段 gcd。 |
| `partial_sum(a.begin(),a.end(),prefix.begin()+1);`：预先令 `prefix` 大小为 `n+1`、`prefix[0]=0`，得到常用 1-based 前缀和。 |
| `adjacent_difference(prefix.begin(),prefix.end(),diff.begin());`：从包含首项的前缀序列恢复相邻差。 |

### 前缀和示例

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<long long> a = {4, -1, 7, 2};
    vector<long long> prefix(a.size() + 1, 0);

    // 输出写到 prefix[1..n]，prefix[0] 保留为 0。
    partial_sum(a.begin(), a.end(), prefix.begin() + 1);

    int left = 1, right = 3; // 查询原数组 0-based 闭区间 [1,3]
    cout << prefix[right + 1] - prefix[left] << '\n';
}
```

**易错点。**

- `accumulate` 的初值写成 `0LL`、`0.0L` 等目标类型，避免窄类型溢出或截断。
- `inner_product` 的默认乘法、`partial_sum` 与 `adjacent_difference` 的中间运算可能仍使用输入元素类型；需要更宽中间值时，先把输入存为宽类型，或提供显式提升的运算并手写前缀循环。
- `reduce` 可能先组合两个输入元素；即使初值较宽，也不应假设所有中间运算都会自动提升。
- 输出区间必须有足够空间；也可使用 `back_inserter`，但前缀数组常直接预分配。
- `lcm(a,b)` 可能在先除后乘仍超出类型范围，不能因为参数各自不溢出就认为安全。
- 对浮点和不可结合运算，`reduce`/scan 的重排可能产生不同结果。
- `adjacent_difference` 的输入输出可以同起点原地操作，但理解覆盖次序较难，比赛中优先使用独立数组。

**参考：**

- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
- [OI Wiki：最大公约数](https://oi-wiki.org/math/number-theory/gcd/)
- [OI Wiki：前缀和与差分](https://oi-wiki.org/basic/prefix-sum/)

## 2.25 Lambda、比较器与函数对象

Lambda 是在使用位置定义的小型可调用对象，常用于排序、查找、删除和数据结构比较。基本形式为 `[捕获列表](参数) -> 返回类型 { 函数体 }`；返回类型多数可省略。`[]` 不捕获外部变量，`[&]` 按引用捕获，`[=]` 按值捕获，也可写 `[&limit,offset]` 精确指定。

比较器描述“`a` 是否严格排在 `b` 前面”，必须形成严格弱序。排序中的等价含义是 `!comp(a,b) && !comp(b,a)`，不一定等同于 `a==b`。若比较器捕获会变化的外部状态，容器或排序进行期间顺序规则可能改变，结果将失去保证；放进 `set`、`priority_queue` 的比较器还必须在对象生命周期内有效。

### 定义与初始化

```cpp
#include <algorithm>
#include <tuple>
#include <utility>
#include <vector>
using namespace std;

int main() {
    vector<pair<int,int>> jobs = {{2,5}, {1,9}, {2,3}};
    sort(jobs.begin(), jobs.end(), [](const auto& a, const auto& b) {
        // 第一关键字升序，第二关键字降序；相等对象必须返回 false。
        if (a.first != b.first) return a.first < b.first;
        return a.second > b.second;
    });
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `[](int x){ return x*x; }`：无捕获 Lambda；可隐式转换为兼容的普通函数指针。 |
| `[=](int x){...}`：按值捕获函数体中用到的自动变量；捕获发生时复制，之后外部变量改变不会同步。默认不能修改捕获副本。 |
| `[&](int x){...}`：按引用捕获；能读写外部变量，但 Lambda 不得活得比被引用对象更久。 |
| `[value,&answer](...) {...}`：显式混合捕获，通常比全捕获更易审查。 |
| `[value]() mutable {...}`：允许修改按值捕获的内部副本，不会修改外部原变量。 |
| `[factor](auto x) { return factor*x; }`：泛型 Lambda，C++14 起参数可用 `auto`。 |
| `[](auto x) noexcept -> long long {...}`：可显式写异常说明和返回类型；多个返回分支类型不一致时常需指定返回类型。 |
| `std::less<T>` / `std::greater<T>`：标准升序/降序函数对象；`greater<int>()` 常用于降序排序和小根堆。 |
| `less<>` / `greater<>`：透明函数对象，可接受不同但可比较的类型，适合异构比较。 |
| `function<R(Args...)>`：类型擦除的通用可调用包装，可保存 Lambda、函数指针或函数对象；有间接调用和可能分配的开销。递归 Lambda 常用它，但极深/极频繁递归需关注常数。 |
| `reference_wrapper<T>`、`ref(x)`、`cref(x)`：把引用包装成可复制对象；向需要复制参数的算法或函数对象传引用时使用。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `sort(a.begin(),a.end(),[](const Node& x,const Node& y){ if(x.w!=y.w)return x.w<y.w; return x.id<y.id; });`：显式多关键字比较。 |
| `priority_queue<int,vector<int>,greater<int>> pq;`：标准小根堆。 |
| `auto pred=[&](long long x){ return feasible(x,limit); };`：封装二分答案判定。 |
| `count_if(a.begin(),a.end(),[&](int x){return x>=low && x<=high;});`：按区间条件计数。 |
| `function<void(int,int)> dfs = [&](int u,int parent){ ... dfs(v,u); };`：C++17 递归 Lambda 的直观写法。 |
| `sort(id.begin(),id.end(),[&](int i,int j){return tie(a[i],i)<tie(a[j],j);});`：按外部数组排序索引。 |

**易错点。**

- 比较器返回 `a <= b`、随机结果或依赖不断变化的全局值，都会破坏严格弱序。
- `[&]` Lambda 被返回、存入长期容器或异步使用时，可能悬空引用；生命周期不清楚就按值捕获。
- 按值捕获大容器会复制整个容器；可显式按引用捕获只读数据。
- `std::function` 比模板参数或 `auto` 有额外开销，热循环中优先让编译器保留具体类型。
- 浮点比较器不宜直接引入 EPS 写成“差小于 EPS 就相等”，这可能破坏传递性；可量化键或单独分组。

**参考：**

- [OI Wiki：Lambda 表达式](https://oi-wiki.org/lang/lambda/)
- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)

## 2.26 随机数与 `shuffle`

C++ 随机库把“随机数引擎”和“分布”分开：`mt19937`/`mt19937_64` 产生可复现的伪随机比特，`uniform_int_distribution`、`uniform_real_distribution` 等把它映射到目标分布。竞赛造数与随机算法应保存种子，便于复现；需要密码学安全性的场景不属于这些引擎的用途。

`shuffle` 使用给定引擎均匀打乱随机访问区间，替代已从 C++17 移除的 `random_shuffle`。固定种子便于调试，时钟或 `random_device` 种子便于不同运行获得不同序列。随机化只能降低被特定数据卡住的概率，不能替代正确性和复杂度分析。

### 定义与初始化

```cpp
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <random>
#include <vector>
using namespace std;

int main() {
    uint64_t seed = chrono::steady_clock::now().time_since_epoch().count();
    mt19937_64 rng(seed);

    uniform_int_distribution<int> dist(1, 100); // 闭区间 [1,100]
    int x = dist(rng);

    vector<int> p = {1, 2, 3, 4, 5};
    shuffle(p.begin(), p.end(), rng);
    (void)x;
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `mt19937 rng(seed)`：32 位梅森旋转引擎，状态较大、周期长、速度快；相同实现与种子产生相同序列。调用一次近似 $O(1)$。 |
| `mt19937_64 rng(seed)`：64 位版本，直接生成 64 位结果；常用于 `long long` 范围和随机哈希盐。 |
| `rng()`：取得引擎原始结果，范围为 `[rng.min(),rng.max()]`；不要直接用 `% k` 假设严格均匀。 |
| `rng.seed(s)`：重新播种并重置引擎状态；不要在循环内反复用时钟播种，否则相近时刻可能产生相关序列。 |
| `uniform_int_distribution<T> dist(l,r)`：生成闭区间 `[l,r]` 上的均匀整数；每次调用写 `dist(rng)`。需保证 `l<=r`。 |
| `uniform_real_distribution<T> dist(l,r)`：通常生成 `[l,r)` 上的均匀实数；浮点离散表示使端点细节不宜用于严格边界逻辑。 |
| `bernoulli_distribution(p)`：以概率 `p` 返回 `true`，要求 $0\le p\le1$。 |
| `normal_distribution<T>(mean,stddev)`：均值为 `mean`、标准差为 `stddev` 的正态分布，要求 `stddev>0`；题意要求均匀数据时不要误用。 |
| `shuffle(first,last,rng)`：用随机引擎打乱随机访问区间，复杂度 $O(n)$；原区间被修改。 |
| `sample(first,last,out,k,rng)`：C++17 无放回抽样至多 `k` 项，返回输出尾后迭代器；复杂度 $O(n)$，不修改输入。输出需有空间或用插入迭代器。 |
| `random_device rd`：实现提供的非确定种子源；可能是真随机，也可能是伪随机或不可用，通常只用于播种而非大量取数。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());`：单次运行随机播种。 |
| `mt19937_64 rng(seed); cerr << "seed=" << seed << '\n';`：对拍保存可复现种子。 |
| `uniform_int_distribution<long long>(l,r)(rng)`：临时分布生成 `[l,r]` 整数。频繁调用同一区间时宜保存分布对象。 |
| `shuffle(a.begin(),a.end(),rng);`：随机排列。 |
| `vector<int> picked; sample(a.begin(),a.end(),back_inserter(picked),k,rng);`：无放回抽样。 |
| `uint64_t salt=rng();`：为自定义哈希取得每次运行不同的盐；并不提供密码学安全性。 |

**易错点。**

- 不要用 `rand()`、`random_shuffle` 或 `rng()%range` 代替现代分布类。
- 分布构造区间是闭区间还是半开区间要区分：整数通常 `[l,r]`，实数通常 `[l,r)`。
- 固定种子适合复现；时钟种子适合随机化。失败时必须把实际种子保留下来。
- `shuffle` 要求随机访问迭代器，不能直接打乱 `list`。
- 伪随机算法仍可能命中坏情况；题目要求确定最坏复杂度时不要只靠随机化兜底。

**参考：**

- [OI Wiki：随机函数](https://oi-wiki.org/misc/random/)
- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)

## 2.27 遍历、复制、变换与区间调整

这一组算法覆盖“检查每项、复制选择项、逐项映射、填充值以及调整区间顺序”等机械操作。它们大多是 $O(n)$，用半开区间表达输入，并返回输出尾后迭代器或处理后的函数对象。相比手写循环，标准算法能清晰表现意图，但调用者仍需保证输出空间和区间重叠规则正确。

`copy`、`transform` 等不会自动扩大普通 `vector`，应先 `resize`，或通过 `back_inserter` 调用 `push_back`。`reverse`、`rotate`、`replace`、`fill` 会直接修改原区间；`copy_if`、`replace_copy` 等则写到另一个输出区间。涉及对象所有权时，`move` 会把源元素置于有效但未指定状态。

### 基本调用

```cpp
#include <algorithm>
#include <iterator>
#include <vector>
using namespace std;

int main() {
    vector<int> a = {1, 2, 3, 4};
    vector<int> squares(a.size());
    transform(a.begin(), a.end(), squares.begin(),
              [](int x) { return x * x; });

    vector<int> even;
    copy_if(a.begin(), a.end(), back_inserter(even),
            [](int x) { return x % 2 == 0; });
}
```

### 方法、运算与常用函数

| 方法、常用函数与说明 |
|---|
| `for_each(first,last,f)`：按顺序对每个元素调用 `f`，复杂度 $O(n)$，返回最终函数对象；`f` 可通过引用参数修改元素。 |
| `all_of` / `any_of` / `none_of(first,last,pred)`：分别判断全部、至少一个、没有元素满足谓词；最坏 $O(n)$，满足结论后可提前停止。空区间上结果分别为 `true,false,true`。 |
| `copy(first,last,out)`：复制到输出并返回输出尾后迭代器，复杂度 $O(n)$；重叠区间通常不安全，向右重叠复制使用 `copy_backward`。 |
| `copy_n(first,count,out)`：复制恰好 `count` 项；调用者必须保证输入足够，`count<0` 的可移植语义不宜依赖。 |
| `copy_if(first,last,out,pred)`：只复制满足谓词的项；返回实际输出尾后位置，复杂度 $O(n)$。 |
| `copy_backward(first,last,outLast)`：从后向前复制到以 `outLast` 结尾的区间，适合目标区间向右重叠；返回目标起点。 |
| `move(first,last,out)` / `move_backward(...)`：逐项移动；源对象仍可析构和赋值，但值未指定。不要与 `<utility>` 的单对象 `std::move` 混淆。 |
| `transform(first,last,out,unaryOp)`：逐项映射，复杂度 $O(n)$；输出可与输入同起点实现原地变换。 |
| `transform(first1,last1,first2,out,binaryOp)`：合并两个等长输入段；第二段必须至少有第一段长度。 |
| `fill(first,last,value)` / `fill_n(first,count,value)`：向区间写入同一值，复杂度 $O(n)$；`fill_n` 返回输出尾后迭代器。 |
| `generate(first,last,g)` / `generate_n(first,count,g)`：反复调用生成器并写入结果；生成器可维护状态，复杂度 $O(n)$。 |
| `replace(first,last,old,new)` / `replace_if(first,last,pred,new)`：原地替换，复杂度 $O(n)$。 |
| `replace_copy` / `replace_copy_if`：复制时替换，不修改输入，返回输出尾后迭代器。 |
| `swap_ranges(first1,last1,first2)`：逐项交换两个等长区间，复杂度 $O(n)$；两区间重叠时不应使用。 |
| `iter_swap(i,j)`：交换两个迭代器指向的元素；`swap(a,b)` 交换对象，通常利用移动或容器常数时间成员交换。 |
| `reverse(first,last)`：原地反转区间，交换约 $n/2$ 次，复杂度 $O(n)$。 |
| `reverse_copy(first,last,out)`：反序复制到输出，不修改输入，复杂度 $O(n)$。 |
| `rotate(first,middle,last)`：把 `[first,middle)` 移到后面，原来的 `middle` 成为新首项；复杂度 $O(n)$，返回原 `first` 元素旋转后的新位置。 |
| `rotate_copy(first,middle,last,out)`：复制旋转后的顺序，不修改输入，返回输出尾后迭代器。 |
| `clamp(value,low,high)`：C++17 把值限制在闭区间 `[low,high]`，可传比较器；必须保证 `low` 不大于 `high`。返回引用，传临时对象时不要长期保存该引用。 |
| `lexicographical_compare(first1,last1,first2,last2)`：按字典序比较两个区间，最多检查到较短区间结束，复杂度 $O(\min(n,m))$；可传比较器。 |
| `equal(first1,last1,first2)`：逐项判断相等；第二段必须足够长。C++14 起可传 `last2` 的重载检查两段长度。 |
| `mismatch(first1,last1,first2)`：返回首个不同位置的一对迭代器；第二段必须足够长。C++14 起有带 `last2` 重载。 |

### 竞赛常用写法

| 常用写法 |
|---|
| `for_each(a.begin(),a.end(),[](int& x){x*=2;});`：原地逐项修改；简单循环同样清楚时不必强行使用。 |
| `bool ok=all_of(a.begin(),a.end(),[](int x){return x>=0;});`：检查所有元素。 |
| `copy_if(a.begin(),a.end(),back_inserter(b),pred);`：筛选到动态数组。 |
| `transform(a.begin(),a.end(),a.begin(),[](int x){return abs(x);});`：原地映射。 |
| `rotate(a.begin(),a.begin()+k,a.end());`：整体左循环移动 `k` 位，先令 `k%=n` 且处理空数组。 |
| `reverse(a.begin()+l,a.begin()+r+1);`：反转 0-based 闭区间 `[l,r]`。 |
| `x=clamp(x,low,high);`：把数值钳制到合法范围；`low<=high` 必须成立。 |
| `equal(a.begin(),a.end(),b.begin(),b.end())`：C++14 起直接比较两个完整区间，长度不同返回 `false`。 |

### 区间旋转示例

```cpp
#include <bits/stdc++.h>
using namespace std;

void rotateLeft(vector<int>& a, long long k) {
    if (a.empty()) return; // 防止 k % 0
    k %= static_cast<long long>(a.size());
    if (k < 0) k += static_cast<long long>(a.size()); // 允许负数表示向右旋转

    // [0,k) 移到末尾，原下标 k 成为新首项。
    rotate(a.begin(), a.begin() + k, a.end());
}

int main() {
    vector<int> a = {1, 2, 3, 4, 5};
    rotateLeft(a, 2); // {3,4,5,1,2}
    for (int x : a) cout << x << ' ';
    cout << '\n';
}
```

**易错点。**

- 输出到 `result.begin()` 前先 `resize`；只 `reserve` 不会创建可写元素，追加输出使用 `back_inserter`。
- `copy` 的目标起点落入源区间 `[first,last)` 时行为未定义；向右重叠复制使用 `copy_backward`，目标位于源区间左侧时使用 `copy`。
- 移动后的对象仍必须有效，但其具体值不能依赖。
- `rotate` 的 `middle` 必须位于 `[first,last]`；空数组取模要先特判。
- 算法会使哪些元素、迭代器或引用失效取决于容器操作；单纯重排不改变 `vector` 容量，但元素内容和位置已变。

**参考：**

- [OI Wiki：STL 算法](https://oi-wiki.org/lang/csl/algorithm/)
- [OI Wiki：迭代器](https://oi-wiki.org/lang/csl/iterator/)

## 2.28 C++17 版本边界

**用途。** 比赛机的标准版本可能固定为 C++17；确认接口是否属于 C++20，可避免本地能编译、提交环境报错。以下片段使用 `<bits/stdc++.h>`。

**用法。** 关联容器存在性用 `find` 或 `count`；批量删除用 erase-remove 惯用法；字符串前后缀自行比较。删除容器末项前先读取，因为 `pop` 系列不返回元素。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool containsValue(const set<int>& values, int x) {
    // C++17 没有 set::contains；find 不会修改容器。
    return values.find(x) != values.end();
}

void eraseNonPositive(vector<int>& values) {
    // C++17 没有 std::erase_if；remove_if 先稳定移动保留项到前部，
    // 再由 vector::erase 真正缩短容器。
    values.erase(remove_if(values.begin(), values.end(),
                           [](int x) { return x <= 0; }),
                 values.end());
}

string popLast(string& s) {
    if (s.empty()) return {}; // back/pop_back 在空串上不合法
    char last = s.back();
    s.pop_back(); // pop_back 返回 void
    return string(1, last);
}
```

**易错点。** C++17 没有 `.contains()`、`std::erase/erase_if`、`std::span`、ranges、`starts_with/ends_with` 或 `std::to_array`；`size()` 常为无符号类型，倒序和与 `int` 比较时应显式转换并先处理空容器。
