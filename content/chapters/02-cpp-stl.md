# 2. STL 库使用

本章按竞赛中最常用的 C++17 功能组织，供选型与查错。`n` 表示元素数，区间均为左闭右开 `[first,last)`。示例统一包含 `<bits/stdc++.h>`（GNU C++17）；若使用标准库实现，应按代码补齐对应头文件。容器操作后按其失效规则重新取得迭代器。

## 2.1 顺序容器：`vector` 与 `array` {#stl-vector-array}

`vector<T>` 是连续存储的动态数组，适合默认的序列存储、随机访问和尾部增删。下标、首尾访问 O(1)，尾插均摊 O(1)，中间插删 O(n)。扩容会使所有迭代器、指针和引用失效；未扩容的尾插使 `end()` 失效。`reserve(n)` 只预留容量，`resize(n)` 才改变元素数。`array<T,N>` 是固定长度数组，元素连续，大小编译期确定，不支持增删；适合小型固定表。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<int> a{4, 1, 3};
    a.reserve(8);                 // 预留容量，不改变 size
    a.push_back(2);
    sort(a.begin(), a.end());
    array<int, 3> fixed{1, 2, 3};
    cout << a[0] + fixed[2] << '\n';
}
```

常用成员：`size()`、`empty()`、`front()`、`back()` 均为 O(1)；`pop_back()` 删除末元素 O(1)，空时不可调用；`clear()` 清空元素但容量通常保留；`erase(it)` 删除单个元素并返回新位置，后缀移动 O(n)；`swap(other)` 交换内容/容量，通常 O(1)。`erase` 会使删除点及之后的迭代器失效，扩容会使全部失效。

| 操作 | 作用与复杂度 | 常见用途/边界 |
|---|---|---|
| `vector<T> a(n)` / `a(n,x)` | 创建 n 个默认值 / x，O(n) | 创建后下标有效；空 vector 不可写 `a[0]` |
| `push_back(x)` / `emplace_back(args...)` | 末尾插入，均摊 O(1) | emplace 原位构造；扩容时全体迭代器失效 |
| `reserve(n)` | 预留容量，不改变 size | 估计规模时减少扩容；不能因此访问 `a[n]` |
| `resize(n,x)` | 调整 size，新元素填 x；最坏 O(n) | 需要真正创建可下标访问的槽位 |
| `insert(pos,x)` / `erase(pos)` | 中间修改 O(n) | pos 必须来自本 vector；返回新的迭代位置 |

避免用 `vector<bool>` 需要真实 `bool&` 或连续 `bool` 存储的场景；它是位压缩特化。二维 `vector` 常用于不规则邻接表；规则网格也可用一维下标 `r * width + c` 改善局部性。

## 2.2 `string` {#stl-string}

`string` 是可变长字符序列，提供随机访问，常用于文本、数字串和字符状态。`size`、下标访问 O(1)，查找和拼接通常与处理字符数成正比。`getline(cin,s)` 读取一整行（此前若用 `>>`，先处理残留换行）；`find(x)` 返回首匹配位置，找不到返回 `string::npos`；`substr(pos,len)` 返回新字符串，越界起点会抛出异常。`stoi`/`stoll` 将前缀转换为整数，非法输入抛异常，超范围也抛异常。修改导致扩容时指针、引用和迭代器可能失效。字符串下标是字节位置，不是 Unicode 字符位置。

| 操作 | 行为 |
|---|---|
| `s += t` / `s.append(t)` | 追加字符或字符串；总成本与追加长度相关 |
| `s.find(t,pos)` | 从 pos 起找子串；找不到是 `string::npos`，不可当作普通负数位置用 |
| `s.substr(pos,len)` | 复制子串；pos 必须不大于 size，len 可超出尾部并自动截断 |
| `stoi` / `stoll` | 将十进制前缀转 int/long long；可用位置参数确认是否消费了全部输入 |

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    string s = "contest";
    s += "!";
    auto pos = s.find("test");
    if (pos != string::npos) cout << s.substr(pos, 4) << '\n';
}
```

## 2.3 `pair`、`tuple` 与结构化绑定 {#stl-pair-tuple}

`pair<A,B>` 表示两个关联值，常用于坐标、边 `(邻点, 权值)` 和排序键；比较按 `first` 再按 `second` 字典序进行。`tuple` 可装多个异质字段，但字段命名不直观；字段较多且语义稳定时优先自定义 `struct`。结构化绑定要求分量数量匹配。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<pair<int,int>> edges{{2, 7}, {1, 4}};
    sort(edges.begin(), edges.end()); // 先按 first，再按 second
    auto [to, weight] = edges.front();
    auto record = make_tuple(3, string("Ada"), true);
    cout << to << ' ' << weight << ' ' << get<1>(record) << '\n';
}
```

## 2.4 两端序列与适配器：`deque`、`stack`、`queue` {#stl-deque-adapters}

`deque<T>` 支持两端均摊 O(1) 插入删除及 O(1) 随机访问；适合单调队列和两端操作。它不是连续内存，不能把 `data()` 当作数组接口。两端插入通常不使已有元素引用失效，但迭代器规则较严格，结构修改后宜重取。

`stack<T>` 提供后进先出，只用 `push/pop/top`；`queue<T>` 提供先进先出，只用 `push/pop/front/back`。二者是容器适配器，`pop` 返回 `void`，应先读取元素再弹出。读取空容器的顶部或队首是错误。

| 适配器 | 读取 | 插入/删除 | 典型用途 |
|---|---|---|---|
| `stack` | `top()` | `push()` / `pop()` | 括号匹配、DFS 显式栈、单调栈 |
| `queue` | `front()`、`back()` | `push()` / `pop()` | BFS、按到达顺序处理任务 |
| `priority_queue` | `top()` | `push()` / `pop()` | 每步取当前最小/最大候选 |

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    deque<int> d{2, 3}; d.push_front(1); d.pop_back();
    stack<int> st; st.push(5); int x = st.top(); st.pop();
    queue<int> q; q.push(x); cout << q.front() << '\n';
}
```

## 2.5 堆：`priority_queue` {#stl-priority-queue}

`priority_queue<T>` 默认是最大堆：`top()` 为最大值，插入和删除堆顶 O(log n)，读取 O(1)。最小堆可用 `greater<T>`。适合反复取当前最大/最小值；若要删除任意元素或遍历有序全体，选择其他结构。自定义比较器需满足严格弱序。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    priority_queue<int> maxHeap;
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int x : {4, 1, 7}) { maxHeap.push(x); minHeap.push(x); }
    cout << maxHeap.top() << ' ' << minHeap.top() << '\n';
}
```

## 2.6 有序集合：`set`、`multiset` {#stl-set-multiset}

`set<T>` 保存互异键，`multiset<T>` 保存可重复键；二者按比较器维护有序，查找、插入 O(log n)，按键删除 multiset 的全部 k 个匹配项为 O(log n+k)。适合需要动态维护有序元素并查前驱/后继的场景。迭代器为双向迭代器，`lower_bound(x)` 返回首个不小于 `x` 的元素，`upper_bound(x)` 返回首个大于 `x` 的元素；不存在时返回 `end()`。插删通常只使被删元素迭代器失效。

`set::erase(x)` 删除键为 x 的元素，`multiset` 中会删除所有等于 x 的元素；若只删一个重复项，先 `find` 再按迭代器删除。不要对集合迭代器调用 `sort`。

| 操作 | `set` / `multiset` 行为 |
|---|---|
| `insert(x)` | O(log n) 插入；set 忽略重复键，multiset 保留 |
| `find(x)` / `count(x)` | 查键 O(log n)；multiset 统计重复数 O(log n + k)，k 为重复个数 |
| `lower_bound(x)` / `upper_bound(x)` | O(log n) 取首个 >=x / >x 的迭代器 |
| `erase(it)` / `erase(x)` | 按迭代器删一个 O(log n)；按键删除 multiset 全部匹配项 O(log n+k) |

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    multiset<int> s{2, 2, 5};
    auto it = s.find(2);
    if (it != s.end()) s.erase(it); // 只删除一个 2
    auto next = s.lower_bound(3);
    if (next != s.end()) cout << *next << '\n';
}
```

## 2.7 有序映射：`map` {#stl-map}

`map<K,V>` 按键有序，每个键唯一；查找、插入和删除 O(log n)。适合键域稀疏、需要有序遍历或前驱后继查询的映射。`m[key]` 不存在时会插入默认值；只读查询用 `find`，避免意外插入。迭代器按键升序，插入通常不使其失效，删除只使被删项迭代器失效。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    map<string, int> count;
    ++count["AC"];
    auto it = count.find("WA");
    if (it == count.end()) cout << "missing\n";
    for (const auto& [key, value] : count) cout << key << ':' << value << '\n';
}
```


常用成员：

| 操作 | 说明 |
|---|---|
| `find(key)` | O(log n)，缺失时返回 `end()`；只读查询优先用它 |
| `at(key)` | 查值但不插入；键不存在时抛出 `out_of_range` |
| `m[key]` | 键不存在时插入默认构造的值；适合频次累加 |
| `insert({key,value})` / `emplace(key,value)` | 插入键值；重复键不会覆盖既有值 |
| `erase(key)` / `erase(it)` | 按键删除或删除迭代器所指项；后者只删一项 |
| `lower_bound` / `upper_bound` | O(log n) 返回首个 `>= key` / `> key` 的迭代器 |

## 2.8 哈希容器：`unordered_set`、`unordered_map` {#stl-unordered}

哈希容器平均查找、插入和删除 O(1)，最坏 O(n)，不维护顺序；适合只需按键快速查找且不要求有序遍历的场景。扩容 rehash 会使所有迭代器失效（引用和指针仍有效）；插入可能触发 rehash。可用 `reserve` 预留元素数减少扩容。键类型必须可哈希且支持相等比较。

| 操作 | 说明 |
|---|---|
| `find(key)` | 返回迭代器，缺失时为 `end()`；只读检查优先用它 |
| `count(key)` / `contains(key)` | 判存在；`contains` 从 C++20 才提供，C++17 用 `find` |
| `reserve(n)` | 预计元素总量，减少 rehash；参数是元素数而非桶数 |
| `load_factor()` / `max_load_factor(x)` | 查看/调整平均装载因子；调参不能保证对抗恶意碰撞 |

自定义键需要提供哈希函数并保持“相等的键哈希值相同”。哈希不是安全性边界；攻击性输入可能退化。整数键可用随机种子的 `splitmix64` 扰动降低被构造碰撞的风险，但这不是密码学保证。

```cpp
#include <bits/stdc++.h>
using namespace std;
struct SplitMixHash {
    // 参数：64 位整数 x。返回：种子扰动后的哈希值。效果：只读进程级随机种子。
    size_t operator()(uint64_t x) const noexcept {
        static const uint64_t seed = chrono::steady_clock::now().time_since_epoch().count();
        x += seed + 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return static_cast<size_t>(x ^ (x >> 31));
    }
};
int main() {
    unordered_map<uint64_t, int, SplitMixHash> id;
    id.reserve(1000);
    id[123456789ULL] = 7;
    cout << id.at(123456789ULL) << '\n';
}
```

## 2.9 `bitset` {#stl-bitset}

`bitset<N>` 在编译期固定 N 位，适合小规模布尔状态、集合位运算和快速计数。与 `vector<bool>` 不同，长度不能运行时改变。按位与或异或、取反和移位按机器字批量处理；`count()` 返回 1 的位数。下标 0 是最低位，移位超出范围的位被丢弃。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    bitset<8> a(string("00101101"));
    bitset<8> b = a << 1;
    cout << (a & b).count() << ' ' << b << '\n';
}
```

## 2.10 排序、二分与边界 {#stl-sort-binary-search}

`sort(first,last)` 要求随机访问迭代器，原地升序排序 O(n log n)，不稳定；降序可传 `greater<>`，自定义记录用严格弱序比较器。`stable_sort` 保留等价元素原相对顺序，通常使用 O(n) 额外空间。`lower_bound`/`upper_bound` 要求区间按相同比较规则有序，返回迭代器，比较次数 O(log n)；对 `vector` 总体 O(log n)，对 `set` 应调用成员 `lower_bound` 才能得到 O(log n)。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<int> a{4, 1, 2, 2};
    sort(a.begin(), a.end());
    auto lo = lower_bound(a.begin(), a.end(), 2);
    auto hi = upper_bound(a.begin(), a.end(), 2);
    cout << (lo - a.begin()) << ' ' << (hi - a.begin()) << '\n';
}
```

常用补充：`nth_element(first,nth,last)` 平均 O(n)，把第 `nth` 元素放在排序后应处的位置，两侧各自满足分界但内部无序；`min_element`/`max_element` 返回极值迭代器，空区间返回 `last`；`binary_search` 只返回是否存在，`equal_range` 返回 `[lower_bound,upper_bound)`。`set`/`map` 需要二分时调用成员 `lower_bound`/`upper_bound`，复杂度 O(log n)；对其迭代器使用泛型二分会因逐步移动而退化。

常用算法速查（`n` 为区间长度）：

| 算法 | 前提与结果 | 复杂度 / 副作用 |
|---|---|---|
| `sort` / `stable_sort` | 随机访问区间；稳定版保留等价项相对次序 | O(n log n)，原地重排 / 稳定排序有足够内存时 O(n log n)，内存不足时最坏 O(n log² n) |
| `nth_element(first,nth,last)` | `nth` 处成为全序第 `nth` 个元素，两边只保证分界 | 平均 O(n)，重排；若 `nth==last`，不解引用该迭代器 |
| `lower_bound` / `upper_bound` | 已按同一比较器排序；分别给出 `>=x` / `>x` 的首位置 | O(log n) 比较；vector 随机访问总体 O(log n) |
| `binary_search` / `equal_range` | 有序区间；前者测存在，后者给出等值段 | O(log n) 比较 |
| `min_element` / `max_element` | 返回极值迭代器，空区间返回 `last` | O(n)，不修改区间 |
| `reverse` / `fill` | 分别反转、写入同一个值 | O(n)，原地修改 |
| `count` / `count_if` | 统计等值项 / 满足谓词项 | O(n)，不修改区间 |
| `copy` / `transform` | 输出区须足够大；`back_inserter(out)` 可追加 | O(n)，写目标区间 |
| `unique` | 只压缩相邻重复项，返回新逻辑末尾 | O(n)，重排但不改变容器 size；常与 `erase` 配合 |

`sort` 自定义比较器必须满足严格弱序，例如按键排序时比较 `a.key < b.key`，不能用 `<=`。对于 `set/map`，泛型 `lower_bound` 迭代器移动可能为 O(n)，应使用容器成员的 O(log n) 查找。

## 2.11 去重、排列与区间算法 {#stl-unique-permutation}

`unique(first,last)` 把相邻重复元素压到前部并返回新逻辑末尾，不会缩短容器；先排序才能全局去重，再用 `erase` 真正缩短。`next_permutation` 把序列改成字典序下一个排列；到最大排列时会重置为最小排列并返回 `false`，故从排序序列开始可枚举所有不同排列。`reverse` 原地反转双向迭代器范围 O(n)；`fill(first,last,value)` 用同一值覆盖范围 O(n)；`count`/`count_if` 分别统计等值项/谓词为真的项，均 O(n)。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<int> a{3, 1, 1, 2};
    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());
    do { for (int x : a) cout << x; cout << '\n'; }
    while (next_permutation(a.begin(), a.end()));
}
```

## 2.12 数值算法与 Lambda {#stl-numeric-lambda}

`accumulate(first,last,init)` 左折叠区间，结果类型由 `init` 决定；求 `long long` 和应写 `0LL`。`iota` 用递增值填充区间。

| 函数 | 结果 | 提醒 |
|---|---|---|
| `accumulate(first,last,init)` | 左折叠 / 累加 | 返回类型由 init 决定；求 long long 和用 `0LL` |
| `partial_sum(first,last,out)` | 输出每个前缀累计值 | 输出空间须足够；可用 `back_inserter` 追加 |
| `iota(first,last,start)` | 依次填 start、start+1... | 需 `<numeric>`；常用于生成下标序列 |
| `gcd(a,b)` / `lcm(a,b)` | C++17 求最大公约数 / 最小公倍数 | lcm 乘法仍可能溢出 |

`gcd(a,b)` 求最大公约数，`lcm(a,b)` 求最小公倍数（C++17 `<numeric>`）；结果类型取决于参数类型，乘法中间值仍可能溢出。Lambda 可捕获局部变量并作为比较器或局部逻辑；按值捕获复制，按引用捕获会修改原变量且不可超出其生命周期。`[&]` 捕获所有使用到的局部变量引用，需确认调用期间对象仍存活。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<int> a(5); iota(a.begin(), a.end(), 1);
    long long sum = accumulate(a.begin(), a.end(), 0LL);
    int limit = 3;
    int count = count_if(a.begin(), a.end(), [limit](int x) { return x <= limit; });
    cout << sum << ' ' << count << '\n';
}
```

## 2.13 迭代器与半开区间 {#stl-iterators}

迭代器连接容器和泛型算法，范围统一写 `[first,last)`；`end()` 是尾后哨兵，不可解引用。`begin()`/`end()` 获取边界通常 O(1)，空范围满足 `begin()==end()`。`vector`、`array`、`deque`、`string` 迭代器支持随机访问；`set/map` 为双向迭代器。`sort`、`nth_element` 要求随机访问；`reverse` 要求双向；`find`、`count` 可用于前向区间。

`it + k`、`last-first` 只适用于随机访问迭代器且区间须来自同一容器。`next(it,k)` 返回移动后的副本，`advance(it,k)` 原地移动；随机访问容器 O(1)，双向/前向容器按步数 O(k)。不要保存跨越容器结构修改仍未确认有效性的迭代器。

常见边界：所有标准算法按半开区间操作；`end()` 不可解引用；`erase`、扩容和 rehash 后检查迭代器有效性；`lower_bound` 前先确认排序规则一致；注意整数累加类型是否足够。
