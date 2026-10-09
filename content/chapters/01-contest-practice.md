# 1. 竞赛常用内容

## 1.1 通用代码骨架与多测清空

**问题：** 将单组逻辑放进 `solve()`，入口只负责读取测试组数并循环调用，便于复用和隔离状态。多测总成本是各组复杂度之和；优先使用局部容器，谨慎清空大型全局数组。

**思路：**

- 单测时保留 `int testCases = 1`，不要读取不存在的测试组数。
- 多测时取消读取 `testCases` 的注释；先确认题面是否给出 $T$。
- 优先把数组、图、DP 表定义为 `solve()` 内局部变量，每组自动重新构造。
- 大型全局数组只清空本组访问过的范围；时间戳法适合频繁清空布尔或编号状态。
- 每组输出格式统一在 `solve()` 内处理，题目要求时加 `Case #x:`。


```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve() {
    int n;
    cin >> n;

    // 状态尽量放在 solve 内：每组测试结束后自动销毁，不会串组。
    vector<ll> a(n + 1); // 本模板约定输入下标为 1..n
    for (int i = 1; i <= n; ++i) cin >> a[i];

    // 在这里编写单组答案。
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int testCases = 1;
    // cin >> testCases; // 仅当题面明确给出测试组数时启用
    while (testCases--) solve();
    return 0;
}
```

**易错点：**

1. 把样例中的多组数据误认为题目输入含 $T$，会从第一项开始读错。
2. `vector::clear()` 只把大小变为 0；重新 `resize` 后不能假设旧内存内容有意义。
3. 全局邻接表、答案、计数器、时间戳和静态局部变量都可能跨组残留。
4. 对最大数组每组完整 `memset`，可能把本可通过的算法拖成 TLE。

**参考：**

- [OI Wiki：C++ 语法基础](https://oi-wiki.org/lang/basic/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)

## 1.2 数据范围与复杂度速判

**问题：** 依据 $n,m,W,T$ 和总和约束估算时间与峰值内存，再选择算法。清空、建图、排序、递归栈和多测开销都要计算；常数和评测机差异使经验表只能初筛。

**思路：**

- 多测必须估算 $\sum n$、$\sum m$，不能只看单组上限。
- 图算法用 $n+m$ 估算；背包看 $nW$；状压看 $n2^n$ 或 $n^22^n$。
- 内存按“元素个数 × 单元素字节数”计算，并加上容器、递归栈和多份数组。
- 约 $10^8$ 次简单整数操作已可能接近常见时限；哈希、字符串复制、堆操作常数更大。
- 用最坏数据本地计时只能辅助判断，不能替代理论复杂度。

**公式与速查：**

```text
常见候选（只作一秒级 C++ 的粗略起点）：
n <= 20          O(2^n)、O(n * 2^n)
n <= 40          O(2^(n/2)) 折半搜索
n <= 500         O(n^3) 需关注常数
n <= 5,000       O(n^2) 需关注常数和内存
n <= 200,000     O(n log n)、O(n sqrt(n)) 视常数而定
n,m <= 1,000,000 O(n)、O(n+m)

内存 MiB = 元素个数 * sizeof(元素) / 1024 / 1024
例如：2^20 * 20 个 long long 约为 160 MiB。
```

**易错点：**

1. $O(n^2)$ 的二维 `long long` 数组常先 MLE，再谈不上 TLE。
2. 把取模、平衡树、哈希或大整数运算都当成一个同常数的“基本操作”。
3. 忽略清空数组、建图、排序或输入输出，它们也计入总复杂度。
4. 只根据样例规模选算法；评测按题目给出的最大范围构造数据。

**参考：**

- [OI Wiki：复杂度简介](https://oi-wiki.org/basic/complexity/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)

## 1.3 快速输入输出

**问题：** 非交互题在首次 IO 前关闭同步并解绑 `cin`，统一使用 C++ 流、以 `\n` 换行。交互题要及时刷新；`getline` 与格式化读取混用时需处理残留换行。

**思路：**

- 在任何 IO 前调用 `ios::sync_with_stdio(false); cin.tie(nullptr);`。
- 关闭同步后统一使用 `cin/cout`，不要混用 `scanf/printf`。
- 普通换行用 `'\n'`；`endl` 会额外刷新缓冲区。
- 交互题必须在每次询问后 `cout << flush`，不能照搬非交互写法。
- 输出大量元素时先拼接或顺序写入，不要在循环中无必要地刷新。


```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false); // 必须在第一次 cin/cout 操作前调用
    cin.tie(nullptr);            // 非交互题解除 cin 对 cout 的自动刷新

    int n;
    cin >> n;
    vector<long long> a(n);
    for (long long& value : a) cin >> value;

    for (int i = 0; i < n; ++i) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n'; // 不需要立即显示时，用换行而不是 endl
    return 0;
}
```

**易错点：**

1. 关闭同步后混用 C 与 C++ 输入或混用两套输出，顺序可能异常。
2. 交互题忘记刷新会等待超时；普通题频繁 `endl` 又可能拖慢输出。
3. `cin >> s` 跳过空白；要读取含空格整行时使用 `getline`，并处理残留换行。
4. 输入失败后变量不会得到有效新值；读到 EOF 的题应以 `while (cin >> x)` 控制。

**参考：**

- [OI Wiki：读入、输出优化](https://oi-wiki.org/contest/io/)
- [OI Wiki：C++ 输入输出](https://oi-wiki.org/lang/io/)

## 1.4 编译、运行与 Sanitizer

**问题：** 用 `-O2` 版模拟提交，用带警告和 Sanitizer 的调试版查越界与未定义行为。先修警告，再测样例、边界和随机数据；检查版较慢，不用于时限评估。

**思路：**

- 普通版开启 C++17、优化和警告；让本地标准尽量接近评测机。
- 调试版加入 `-g`、`-DDEBUG`、`-fsanitize=address,undefined` 和栈帧选项。
- 用输入重定向复现测试，必要时用 `time` 粗测最坏数据。
- 先修编译警告，再运行样例、边界数据和随机对拍。
- Sanitizer 报告从第一处错误和调用栈开始看；后续错误可能只是连锁反应。

**命令：**

```bash
# 接近提交环境的优化版
g++ main.cpp -std=c++17 -O2 -Wall -Wextra -Wshadow -o main

# 本地查越界和未定义行为；不要用它测正式时限
g++ main.cpp -std=c++17 -O1 -g -DDEBUG \
  -fsanitize=address,undefined -fno-omit-frame-pointer -o main_dbg

./main < sample.in > sample.out
./main_dbg < fail.in
time ./main < maximal.in > /dev/null
```

**易错点：**

1. 只在 `-O0` 下测试；未定义行为可能在 `-O2` 下表现不同。
2. 把 Sanitizer 的额外时间、内存开销当成正式程序复杂度。
3. 忽略警告中的窄化、符号比较、变量遮蔽和未初始化使用。
4. 本地编译器版本、标准或整数宽度与评测机不同，造成“本地过、提交错”。

**参考：**

- [OI Wiki：命令行编译与调试](https://oi-wiki.org/tools/compile-debug/)
- [OI Wiki：编译优化](https://oi-wiki.org/lang/optimizations/)

## 1.5 调试宏与断言

**问题：** 把日志集中写到 `cerr`，用 `DEBUG` 控制是否编译；用 `assert` 检查下标、区间和内部不变量。断言不能代替合法输入分支，也不要把必要操作写进断言。

**思路：**

- 本地用 `-DDEBUG` 开启日志，提交代码不定义 `DEBUG`。
- 在二分边界、图下标、DP 状态范围和数据结构不变量处放断言。
- 错误诊断信息写 `cerr`；正式答案只写 `cout`。
- 先打印最小必要状态：位置、关键变量、容器大小，不要倾倒全部大数组。
- `assert` 失败表示实现或推理错误；若条件来自不可信输入，应正常分支处理。


```cpp
#include <bits/stdc++.h>
using namespace std;

#ifdef DEBUG
template <class... Args>
void debugLog(Args&&... args) {
    // 折叠表达式按参数顺序输出，调试格式集中在一个入口维护。
    ((cerr << forward<Args>(args) << ' '), ...);
    cerr << '\n';
}
#define DBG(...) debugLog("[", #__VA_ARGS__, "] =", __VA_ARGS__)
#else
#define DBG(...) ((void)0)
#endif

long long rangeSum(const vector<long long>& prefix, int left, int right) {
    // 调用约定：prefix[0..n]，查询原数组闭区间 [left, right]。
    assert(1 <= left && left <= right);
    assert(right < static_cast<int>(prefix.size()));
    DBG(left, right, prefix[right], prefix[left - 1]);
    return prefix[right] - prefix[left - 1];
}
```

**易错点：**

1. 调试输出写入 `cout` 会造成 WA；提交前也不要靠手工搜索删除日志。
2. 宏参数含逗号表达式或副作用时容易产生意外；`DBG(++x)` 会真的修改 `x`。
3. 定义 `NDEBUG` 后标准 `assert` 会被移除，不能把必要计算写进断言表达式。
4. 日志本身可能使 TLE 或改变时序，只保留能缩小错误范围的信息。

**参考：**

- [OI Wiki：常见技巧](https://oi-wiki.org/contest/common-tricks/)
- [OI Wiki：命令行编译与调试](https://oi-wiki.org/tools/compile-debug/)

## 1.6 随机数与数据生成

**问题：** 用 `<random>` 的引擎和分布生成可控测试，并保存种子以复现失败。均匀整数范围应由分布指定；随机化不能替代正确性证明或复杂度分析。

**思路：**

- 从命令行读取固定种子；未提供时才使用时钟种子，并把种子输出到 `cerr`。
- 用 `uniform_int_distribution<ll>(left,right)`，不要用 `rng() % range` 追求严格均匀。
- 随机排列使用 `shuffle`；C++17 已移除 `random_shuffle`。
- 生成图时明确是否允许自环、重边、断开；树可令每个 `v` 随机连接 `[1,v-1]`。
- 纯随机以外，固定加入最小值、最大值、全相等、单调、星形和链形等结构。


```cpp
#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;

int main(int argc, char** argv) {
    // 对拍时由脚本传入 seed；同一 seed 必须生成同一测试。
    ull seed = argc >= 2 ? stoull(argv[1])
                         : chrono::steady_clock::now().time_since_epoch().count();
    mt19937_64 rng(seed);
    cerr << "seed = " << seed << '\n';

    auto randomInt = [&](long long left, long long right) {
        return uniform_int_distribution<long long>(left, right)(rng);
    };

    int n = static_cast<int>(randomInt(1, 12)); // 小规模便于暴力校验
    vector<int> permutation(n);
    iota(permutation.begin(), permutation.end(), 1);
    shuffle(permutation.begin(), permutation.end(), rng); // 原地打乱，元素仍是 1..n

    cout << n << '\n';
    for (int i = 0; i < n; ++i) {
        if (i) cout << ' ';
        cout << permutation[i];
    }
    cout << '\n';
    return 0;
}
```

**易错点：**

1. 失败后不记录种子，导致错误数据无法再次生成。
2. `rand() * rand()` 可能溢出且分布差；`rng() % k` 也可能有模偏差。
3. 只造平均随机数据，覆盖不到空集、重复值、极值和退化结构。
4. 生成器自身不满足题面约束，会让对拍结论失去意义。

**参考：**

- [OI Wiki：随机函数](https://oi-wiki.org/misc/random/)
- [OI Wiki：出题·造数据](https://oi-wiki.org/contest/problemsetting/)

## 1.7 暴力程序与正确性基准

**问题：** 对小规模输入编写结构简单、容易确认的暴力解，作为优化算法的差分基准。暴力可指数级，但必须覆盖合法边界并与被测程序使用相同输入定义。

**思路：**

- 先写数学定义最直接对应的判定，再写优化程序；两者避免复用核心函数。
- 暴力只需支持生成器的小范围，不必支持题面最大数据。
- 返回完整答案；多解或浮点题需写等价比较器，不能简单文本 `diff`。
- 对优化程序的每个可疑性质，增加能打破该性质的构造数据。
- 发现差异后先保存输入，再分别检查暴力与正解，不能默认暴力必对。


```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 示例基准：枚举所有子集，求不超过 capacity 的最大价值。
// 仅用于 n 很小的对拍；下标统一为 0..n-1。
ll bruteKnapsack(const vector<int>& weight,
                 const vector<ll>& value,
                 int capacity) {
    int n = static_cast<int>(weight.size());
    assert(n <= 24); // 防止误拿暴力跑正式上限
    ll answer = 0;
    for (unsigned long long mask = 0; mask < (1ULL << n); ++mask) {
        // 每个二进制位独立表示一件物品是否选中。
        int totalWeight = 0;
        ll totalValue = 0;
        for (int i = 0; i < n; ++i) {
            if (mask & (1ULL << i)) {
                totalWeight += weight[i];
                totalValue += value[i];
            }
        }
        if (totalWeight <= capacity) answer = max(answer, totalValue);
    }
    return answer;
}
```

**易错点：**

1. 暴力与正解复制了同一个转移或辅助函数，二者可能稳定地产生同一错误。
2. 暴力数组越界、溢出或误解题意，会把正确程序判成错误。
3. 枚举上界用 `1 << n` 可能溢出，应使用 `1ULL << n` 并限制 $n$。
4. 只比较答案值而忽略无解、多解、顺序无关或误差判定规则。

**参考：**

- [OI Wiki：枚举](https://oi-wiki.org/basic/enumerate/)
- [OI Wiki：常见技巧·对拍](https://oi-wiki.org/contest/common-tricks/)

## 1.8 自动对拍与失败保留

**问题：** 生成器、暴力程序和正式解在同一输入上运行并比较输出，可快速发现反例。对拍成本取决于单轮三程序耗时；保存种子和失败输入，先缩小反例再定位。

**思路：**

- 先分别编译 `gen.cpp`、`brute.cpp`、`main.cpp`，保证三者无编译警告。
- 脚本给生成器传递递增种子，任一步骤非零退出都视为失败。
- 用 `diff -Z -B` 只在题目允许忽略空白差异时比较；严格格式题直接用 `diff`。
- 失败时保留 `fail.in`、双方输出和 seed，再用 Sanitizer 单独复现。
- 多解、集合输出、浮点误差题应改写 checker，把两个输出都按题意验证。

**命令：**

```bash
#!/usr/bin/env bash
set -u

# 用法：先编译出 ./gen ./brute ./main，再执行 bash stress.sh。
for seed in $(seq 1 100000); do
  ./gen "$seed" > stress.in || exit 1
  ./brute < stress.in > brute.out || exit 1
  ./main < stress.in > main.out || exit 1

  if ! diff -Z -B brute.out main.out > /dev/null; then
    cp stress.in fail.in
    echo "Wrong answer, seed = $seed"
    diff -u brute.out main.out
    exit 1
  fi
done

echo "Accepted all generated tests"
```

**易错点：**

1. 程序 RE 后仍比较旧输出文件，可能误报一致；脚本必须检查退出码。
2. `diff` 不理解“任意合法方案”；此类题必须按题意写 checker。
3. 对拍全是同一种随机分布，跑再多轮也未必覆盖退化边界。
4. 并行对拍共用同名临时文件会互相覆盖；每个进程需独立目录或文件名。

**参考：**

- [OI Wiki：常见技巧·对拍](https://oi-wiki.org/contest/common-tricks/)
- [OI Wiki：出题·造数据](https://oi-wiki.org/contest/problemsetting/)

## 1.9 文件与标准流切换

**问题：** 本地可在宏控制下重定向输入输出文件，提交时仍使用标准流。检查运行目录和文件名；重定向应发生在任何 IO 之前，避免评测机找不到文件。

**思路：**

- 本地首选 `./main < sample.in > sample.out`，源码无需修改。
- 比赛明确要求文件 IO 时，严格使用题面给出的文件名和大小写。
- 若使用条件编译，只把本地文件切换放在 `#ifndef ONLINE_JUDGE` 中。
- 检查 `freopen` 返回值；本地文件不存在时立即报错。
- 调试信息仍写 `cerr`，它不会进入重定向到答案文件的 `stdout`。


```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
#ifndef ONLINE_JUDGE
    // 本地可用；若评测平台不定义 ONLINE_JUDGE，提交前应删除这段。
    if (freopen("input.txt", "r", stdin) == nullptr) return 1;
    if (freopen("output.txt", "w", stdout) == nullptr) return 1;
#endif

    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long value;
    while (cin >> value) cout << value << '\n';
    return 0;
}
```

**易错点：**

1. 假设所有 OJ 都定义 `ONLINE_JUDGE`；不确定时不要把 `freopen` 留在提交代码里。
2. 文件名大小写、扩展名或相对路径错误，导致读不到输入。
3. 把输入输出文件写反，或用写模式打开输入文件造成数据被截断。
4. 使用 shell 重定向时把 `2>` 与 `>` 混淆，调试信息进入答案文件。

**参考：**

- [OI Wiki：常见技巧](https://oi-wiki.org/contest/common-tricks/)
- [OI Wiki：C++ 输入输出](https://oi-wiki.org/lang/io/)

## 1.10 WA、RE、TLE、MLE 与 UB 排查

**问题：** 按现象分别检查建模/边界、非法访问、渐进复杂度/常数、峰值内存和未定义行为。先用最小失败输入复现，再结合编译警告、Sanitizer 与计时定位。

**思路：**

- CE：在与评测相同标准下编译，查看第一条错误，确认提交语言和入口函数。
- WA：手算最小反例，核对输入含义、开闭区间、无解输出、取模与浮点格式。
- RE：用失败输入跑 Sanitizer，检查数组下标、递归深度、迭代器和除数。
- TLE/OLE：确认循环会推进、输出量有限，再重新计算最坏复杂度和总测试规模。
- MLE：计算峰值而非单数组大小，关注 `vector<vector<...>>`、DP 多份表和按值传参。

**排查命令。**

```bash
# 1. 带警告编译；2. 用检查版复现；3. 查看峰值时间和内存（GNU/Linux）。
g++ main.cpp -std=c++17 -O2 -Wall -Wextra -Wshadow -o main
g++ main.cpp -std=c++17 -O1 -g \
  -fsanitize=address,undefined -fno-omit-frame-pointer -o main_dbg
./main_dbg < fail.in
/usr/bin/time -v ./main < maximal.in > /dev/null
```

**易错点：**

1. 看到 RE 就盲目加大数组；根因也可能是负下标、栈溢出或除零。
2. 随机修改代码后失败样例消失，就误以为问题已修复；UB 可能只改变表现。
3. 只测样例，未覆盖最大规模、不可达、重复边、负数和空答案。
4. 诊断 TLE 时只看主算法，忽略重复清空、容器复制和调试输出。

**参考：**

- [OI Wiki：题型概述·评测结果](https://oi-wiki.org/contest/problems/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)
- [OI Wiki：编译优化·未定义行为](https://oi-wiki.org/lang/optimizations/)

## 1.11 边界数据检查清单

**问题：** 根据约束逐项构造最小、最大、重复、单调、全相等、不可达和答案极值等输入。边界测试用于验证实现假设，复杂度仍需单独证明。

**思路：**

- 规模：$n=0$（若允许）、$n=1$、最小合法值、最大 $n,m,T$、总规模上限。
- 数值：全 0、全负、全相等、最小/最大值、答案刚好越过 `int`、乘法溢出。
- 序列：递增、递减、回文、重复集中、答案在首尾、空答案和唯一答案。
- 图树：孤点、断开、重边、自环（若允许）、链、星、完全图、源点即终点。
- 区间：单点、全区间、端点相接、左右边界、开闭含义；多测检查上一组残留。

**检查清单。**

```text
[ ] 手算并通过最小合法输入
[ ] 测试空答案、无解、唯一解、多解
[ ] 测试全相等、严格递增、严格递减
[ ] 测试 0、负数、最大值与 long long 溢出边缘
[ ] 测试下标 0/1、n-1/n、区间端点和源点等于终点
[ ] 测试断开图、重边、自环、链、星（按题面允许范围）
[ ] 测试两组连续输入，第二组比第一组小
[ ] 最大数据下检查时间、内存和递归深度
[ ] 核对输出大小写、空格、换行、精度和 Case 编号
```

**易错点：**

1. 构造了题面不允许的数据并据此“修复”，反而破坏正确逻辑。
2. 只测 $n=1$，未测答案在最后一个元素或最后一条边的情形。
3. 多测只用相同大小，未发现第二组变小时的残留数组内容。
4. 随机数据代替结构数据；链、星、全相等等退化形状出现概率极低。

**参考：**

- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)
- [OI Wiki：出题·数据与样例](https://oi-wiki.org/contest/problemsetting/)

## 1.12 整数溢出与浮点精度

**问题：** 根据最大中间结果选择整数类型，并在乘法前提升类型；累加、平方和及哨兵运算都要检查范围。浮点比较按误差模型选绝对/相对误差，避免随意固定 epsilon。

**思路：**

- 和、距离、计数优先用 `long long`；乘法写 `1LL * a * b`。
- 可能超过约 $9\times10^{18}$ 的整数中间值用 `__int128`，输出需自行转换。
- 无穷大取 `numeric_limits<ll>::max()/4`，加法前先排除不可达状态。
- 浮点比较用 `abs(a-b) <= eps * max(1,abs(a),abs(b))` 的混合误差。
- 输出按题意使用 `fixed << setprecision(k)`；几何 EPS 应结合坐标范围调整。


```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using i128 = __int128_t;
using u128 = __uint128_t;

bool almostEqual(long double a, long double b,
                 long double eps = 1e-12L) {
    // 同时照顾接近 0 的绝对误差和大数的相对误差。
    return fabsl(a - b) <= eps * max({1.0L, fabsl(a), fabsl(b)});
}

string toString(i128 value) {
    if (value == 0) return "0";
    bool negative = value < 0;
    // 先加一再取负，避免直接对 i128 最小值取负导致溢出。
    u128 magnitude = negative ? static_cast<u128>(-(value + 1)) + 1
                              : static_cast<u128>(value);
    string result;
    while (magnitude > 0) {
        result.push_back(static_cast<char>('0' + magnitude % 10));
        magnitude /= 10;
    }
    if (negative) result.push_back('-');
    reverse(result.begin(), result.end());
    return result;
}

i128 safeProduct(ll a, ll b) {
    return static_cast<i128>(a) * b; // 转换必须发生在乘法之前
}
```

**易错点：**

1. `long long product = a * b;` 中 `a,b` 为 `int` 时，乘法可能已溢出。
2. 有符号整数溢出是 UB，不能依赖“自然回绕”。
3. 用 `a == b` 判断计算所得浮点数，或所有问题固定使用同一个 EPS。
4. `NaN` 与任何数（包括自身）比较都不相等；异常值应用 `isfinite` 检查。

**参考：**

- [OI Wiki：变量·整数与浮点类型](https://oi-wiki.org/lang/var/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)
- [OI Wiki：编译优化·未定义行为](https://oi-wiki.org/lang/optimizations/)

## 1.13 赛中提交与三人协作流程

**问题：** 三人协作时约定接口、变量/编号口径和提交负责人，避免多人同时改同一文件。提交前确认编译标准、样例、边界、多测清理与输出格式，并保留可回滚版本。

**思路：**

- 开场快速读题，记录题意确定度、预估难度、算法、实现者和卡点；优先稳题。
- 维护纸面或离线状态表：未读、在读、待证明、编码、测试、已交、待修。
- 上机前写清状态、关键公式和边界；机器优先给已证明、可快速 AC 的实现。
- 提交前由另一人核对题号、语言、复杂度、清空、整数范围、样例和文件内容。
- 收到 WA/RE/TLE 后先保留版本与失败假设，再决定调试、重写或暂时换题。
- 封榜期按“通过概率 × 题目收益 ÷ 预计时间”排序，不因 sunk cost 长时间单点卡题。

**提交前检查。**

```text
[ ] 提交的是正确题号、正确文件、正确语言标准
[ ] 已删除本地 freopen，或确认评测定义 ONLINE_JUDGE
[ ] 调试信息不进入 stdout，交互题每次询问都 flush
[ ] 复杂度覆盖最大 n、m、T 和所有测试总规模
[ ] long long / __int128、INF 加法、取模和浮点精度正确
[ ] 多测状态已清空；数组、字符串、图的下标边界正确
[ ] 样例、最小数据、无解数据、手造边界均通过
[ ] 队友复述了算法并审过最危险的三处代码
```

**易错点：**

1. 三人同时围着一份代码调试，导致无人继续读题或准备下一题。
2. 未证明就抢机器编码，写完才发现模型或复杂度不成立。
3. WA 后立即重复提交同一份代码，产生无信息增益的罚时。
4. 只口头同步进度；长时间后队友不知道谁在做什么、哪题可接手。
5. 提交窗口选错题号、语言或旧文件，这是最不值得的罚时。

**参考：**

- [OI Wiki：ICPC/CCPC 赛事与赛制](https://oi-wiki.org/contest/icpc/)
- [OI Wiki：题型概述](https://oi-wiki.org/contest/problems/)
