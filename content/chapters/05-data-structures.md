
# 5. 数据结构

本章代码默认使用 C++17。除特别说明外，数组下标从 1 开始；调用查询、删除操作前应保证容器非空、区间合法。字典树统一收录在第 8 章字符串中。

## 5.1 栈与队列

**1. 它是做什么的**

栈、队列和双端队列是按位置约束插入、删除顺序的序列容器：栈后进先出，队列先进先出，双端队列允许在两端操作。括号匹配、撤销操作常用栈；广度优先搜索和按到达顺序处理任务常用队列；需要两端进出时用 `deque`。

本例接收整数序列 `a`，分别将其压入局部栈和队列，再逐个读取并弹出；它还演示向双端队列两端插入和从前端删除。函数返回 `void`，不修改 `a`，也不输出数据；读取出的值目前被丢弃，实际题目要在取值处加入处理逻辑。三种容器在本例中均不要求元素有序或互异。

复杂度：构造容器并处理长度为 `k` 的序列，整体时间 $O(k)$；一次 `push`、`pop`、`top`、`front`、`back` 或 `empty` 均为 $O(1)$。`deque` 两端插入和删除为 $O(1)$。存放 `k` 个元素需要 $O(k)$ 空间；这里统计额外空间的渐进量级。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 只读输入序列；按从前到后的顺序依次入栈、入队。 |
| `st` | `stack<int>` 栈适配器；只能查看和删除栈顶，先入的元素后取出。 |
| `q` | `queue<int>` 队列适配器；从队首查看和删除，先入的元素先取出。 |
| `dq` | `deque<int>` 双端队列；示例先在前端放 `1`、再在后端放 `2`，随后从前端删除 `1`。 |
| `x` | 每轮取出的元素；必须在 `pop()` 前读取，当前示例没有保留或输出它。 |

这些容器按元素顺序工作，没有节点编号或自定义下标。`stack` 和 `queue` 不提供迭代器，也不支持随机访问；若需要遍历全部元素，应逐次读取并弹出，或选择适合的其他容器。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `stackQueueExample(const vector<int>& a)` | 接收整数向量常量引用；返回 `void`。 | 创建三个局部容器并演示入栈、入队和双端队列操作；不改变 `a`，函数结束时容器销毁。当前取出的值被丢弃，没有可见输出。 |
| `push` | 插入一个元素；返回 `void`。 | 栈和队列从各自的后端加入；`deque` 可用 `push_front` 或 `push_back` 指定一端。 |
| `top` / `front` / `back` | 无参数；返回相应端元素的引用。 | 只能在容器非空时读取；示例将元素复制到 `x` 后再弹出。 |
| `pop` / `pop_front` / `pop_back` | 无参数；返回 `void`。 | 删除指定端元素，不返回被删值；调用前必须确认非空。 |
| `empty` / `size` | 无参数；分别返回是否为空、元素个数。 | 可用于安全循环和检查容器状态。 |

题目通常不需要调用演示函数；直接在自己的逻辑中声明并使用相应容器即可。若调用本例函数，`a` 中的元素只会被消费演示，不会产生答案。

**4. 怎么调用**

先选符合处理顺序的容器；插入元素；每轮先判断非空，再读取对应端并处理元素，最后调用 `pop` 删除。若要两端操作，使用 `deque`。本例完整模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 是待演示的整数序列；返回 void，局部容器消费并展示栈/队列/双端队列顺序，不改 a。
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

下面的片段可放在业务函数内。对序列 `4 7 9`，栈依次取出 `9 7 4`，队列依次取出 `4 7 9`；两端队列操作后剩余 `[2]`：

```text
vector<int> a = {4, 7, 9};
stack<int> st;
for (int x : a) st.push(x);
while (!st.empty()) {
    int x = st.top();
    // 处理 x
    st.pop();
}

queue<int> q;
for (int x : a) q.push(x);
while (!q.empty()) {
    int x = q.front();
    // 处理 x
    q.pop();
}

deque<int> dq;
dq.push_front(1);
dq.push_back(2);
dq.pop_front();
// 结果：dq 中只剩 2
```

**5. 要改哪里**

- 需要后进先出时保留 `stack`，处理逻辑放在读取 `top()` 之后、`pop()` 之前；例如括号匹配时在这里检查并配对。
- 需要先进先出时保留 `queue`，在读取 `front()` 后处理；广度优先搜索通常在入队时标记节点已发现，避免重复入队。
- 需要从两端插入或删除时改用 `deque` 的 `push_front`、`push_back`、`pop_front`、`pop_back`。栈和队列适配器不提供另一端接口。
- 若需要按下标读取、排序或遍历而不消费元素，换用 `vector` 或 `deque` 等支持相应操作的容器；`stack` / `queue` 不适合这些需求。
- 多组数据时，局部容器在函数结束时自动销毁；若容器定义在外层并跨组复用，每组开始前需清空，避免残留元素。

**6. 自检**

取 `a = [4, 7, 9]`：逐个压入栈后，弹出顺序应为 `9, 7, 4`；逐个入队后，出队顺序应为 `4, 7, 9`。对双端队列先执行 `push_front(1)`、`push_back(2)`，再执行 `pop_front()`，应只剩 `2`。单元素序列压入任一容器后只读取一次；空序列则两个处理循环都不进入。重复值（如 `[5, 5]`）仍按位置入出，结果仍各有两个 `5`，容器不会自动去重。

**7. 坑**

1. 空容器调用 `top()`、`front()`、`back()` 或 `pop()` 会导致未定义行为；先用 `empty()` 检查，或在 `while (!empty())` 中操作。
2. 先 `pop()` 再读取会丢失待处理元素；先复制/处理 `top()` 或 `front()`，再删除。
3. 误以为 `pop()` 会返回元素；它只负责删除，需先用 `top()`、`front()` 或 `back()` 取值。
4. 需要遍历或随机访问时使用 `stack` / `queue`；它们是适配器，只暴露受限接口，应改选支持目标操作的容器。
5. 显式栈模拟 DFS 时，子节点的入栈次序会影响弹出访问次序；若要维持递归 DFS 的访问顺序，通常按期望访问顺序的反向压入。

**8. 一句话原理**

栈、队列和双端队列通过限制允许操作的端点，分别实现后进先出、先进先出和两端进出。

**参考：**

- [OI Wiki：栈](https://oi-wiki.org/ds/stack/)
- [OI Wiki：队列](https://oi-wiki.org/ds/queue/)

## 5.2 单调栈

**1. 它是做什么的**

给定一个静态整数数组，若要对每个位置找右侧第一个严格更小的元素，可以从左向右扫描并用单调栈在线性时间内完成。模板返回的是元素的下标；找不到时为 `-1`。它不修改输入数组，也不处理动态插入、删除或区间更新。

预处理：无。单次调用时间：$O(n)$，其中 $n$ 是数组长度；每个下标只入栈、出栈各至多一次。额外空间：$O(n)$，用于答案和栈。每次入栈、出栈本身为 $O(1)$。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `a` | 只读输入数组，位置从 `0` 到 `n-1`。 |
| `n` | `a.size()` 转成的整数，表示元素个数。 |
| `answer` | 与 `a` 等长；`answer[j]` 存位置 `j` 右侧首个严格更小元素的位置，暂时未找到或最终不存在时为 `-1`。 |
| `st` | 保存尚未找到答案的位置下标。栈中下标从底到顶递增，对应的数组值单调不减。 |
| `i` | 当前扫描到的下标；`st.top()` 是当前正在等待答案的位置。 |

例如 `a = [3, 1, 2, 1, 4]`。扫描到位置 `1` 的值 `1` 时，位置 `0` 的值 `3` 被弹出并得到答案 `1`。值相等时不弹出，所以位置 `1` 不会把位置 `3` 当作“严格更小”；结束后 `answer = [1, -1, 3, -1, -1]`。

**3. 函数在做什么**

| 函数 | 参数与返回 | 作用和前提 |
|---|---|---|
| `firstSmallerOnRight(const vector<int>& a)` | 参数是任意长度的只读整数数组；返回等长 `vector<int>`。 | 从左向右扫描。每当 `a[i] < a[st.top()]`，位置 `i` 就是栈顶下标右侧第一个严格更小的位置，记录后弹栈；最后仍在栈中的下标没有答案，保留 `-1`。可直接处理空数组。 |

没有需要调用者自行实现的辅助函数；通常只需调用公开函数并读取返回数组。函数不保留跨调用状态，同一输入可重复调用。

**4. 怎么调用**

先准备数组，再调用函数；返回数组与输入逐项对应。下例可放在业务函数中：

```text
vector<int> a = {3, 1, 2, 1, 4};
vector<int> next = firstSmallerOnRight(a);
// next 为 {1, -1, 3, -1, -1}
```

模板代码如下，代码片段本身不含 `main`，需要在调用处提供数组：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 为 0-based 数组；返回每项右侧首个严格更小位置的下标，不存在为 -1；不改 a。
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

**5. 要改哪里**

- 求右侧首个严格更大位置：把弹栈条件改为 `a[i] > a[st.top()]`。
- 求右侧首个小于或等于的位置：把条件改为 `a[i] <= a[st.top()]`。相等值会在此时被弹出，因此较早位置会把当前相等位置记为答案。
- 求左侧最近元素：反向扫描，并相应调整栈中下标顺序与答案定义；不能只改一个比较符号。
- 需要返回元素值而不是位置时，可在确定答案处使用 `a[i]`；若要计算距离，则用 `i - j`（当前下标减去被弹出下标 `j`），并先判断答案是否为 `-1`。

**6. 自检**

对 `a = [2, 2, 1]`，结果应为 `[2, 2, -1]`：相等的 `2` 不算严格更小，而 `1` 是前两个位置的答案。对单元素 `[7]`，结果为 `[-1]`；空数组返回空数组。扫描结束时栈中每个下标右侧都没有更小值，这些位置的答案应继续为 `-1`。

**7. 坑**

- 重复值答案不对：严格与非严格条件混淆。严格更小用 `<`，小于等于用 `<=`。
- 得到的是值却拿来当位置：栈中保存的是下标，确定答案时记录的也是下标。
- `-1` 被用于计算距离或访问数组：先判断该位置是否存在答案，再计算 `answer[j] - j`。
- 误以为栈里最终只剩最小值：栈保存的是尚未找到右侧更小值的候选位置，多个位置可以同时留在栈中。

**8. 一句话原理**

从左向右扫描时，新位置一旦比栈顶位置的值小，就成为该栈顶位置等待已久的第一个严格更小元素。

**参考：**

- [OI Wiki：单调栈](https://oi-wiki.org/ds/monotonous-stack/)

## 5.3 单调队列

**1. 它是做什么的**

给定长度为 `n` 的整数数组 `a` 和窗口长度 `k`，本模板返回每个连续长度为 `k` 的闭区间最小值。仅当 `1 <= k <= n` 时有答案，结果长度为 `n-k+1`；否则返回空数组。对固定窗口，时间复杂度为 $O(n)$，队列辅助空间为 $O(k)$，另需 $O(n-k+1)$ 保存返回结果。初始化没有独立预处理阶段，单次调用处理每个元素一次；每个下标最多入队、出队各一次，所以摊还总操作数为 $O(n)$，单次循环可能弹出多个元素。

它也可用于某些 DP：当每个状态只需查询一段随状态移动的候选区间最优值，且候选值能按下标顺序维护时，可用单调队列代替逐项扫描。若候选区间不单调移动，或候选优劣不能由队尾淘汰规则保证，则不能直接套用。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `a` | 输入数组，0-based；函数不会修改它。 |
| `k` | 窗口长度，合法范围是 `1..n`。 |
| `i` | 当前扫描到的数组下标，也是当前窗口的右端点。 |
| `dq` | 候选下标的双端队列；下标递增，对应值严格递增。队首是当前窗口最小值候选。 |
| `answer` | 按窗口右端点递增收集的结果；`answer[j]` 对应闭区间 `[j, j+k-1]`。 |

处理到 `i` 时，当前窗口是 `[i-k+1, i]`。队首下标不大于 `i-k` 就已过期；从队尾删除值大于或等于 `a[i]` 的下标，因为新元素更靠右且不大于旧元素，旧元素之后不可能再成为最小值。相等时保留较新的下标，它能留在窗口更久。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `slidingWindowMinimum(a, k)` | 参数为 0-based 整数数组和窗口长度；返回各合法窗口的最小值，不修改 `a`。`k <= 0` 或 `k > a.size()` 时返回空数组。队列在调用内创建，不保留跨调用状态。 |

**4. 怎么调用**

调用时传入数组和窗口长度，直接使用返回数组；数组为空或窗口不合法时，结果为空。下面片段可放在业务函数内：

```text
vector<int> a = {4, 2, 2, 5, 1};
vector<int> ans = slidingWindowMinimum(a, 3);
// ans 为 {2, 2, 1}，依次对应 [4,2,2]、[2,2,5]、[2,5,1]
```

模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 为 0-based 数组、k 为窗口长度；返回各窗口最小值，k<=0 或 k>n 时返回空表；不改 a。
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

**5. 要改哪里**

- 求窗口最大值：队列对应值改为严格递减，把队尾条件 `a[dq.back()] >= a[i]` 改为 `a[dq.back()] <= a[i]`，队首读取方式不变。
- 若要保留相等值中较早的下标，可将最小值的队尾条件改成 `>`；此时队列值非递减，答案仍正确，但可能多保留候选。
- 变长窗口或其他 DP 候选区间，需要按题目定义修改过期条件和队尾淘汰条件；只有当淘汰后旧候选永远不可能胜出时，才能删除它。若需要同时查询多个不同窗口且窗口端点不按顺序前进，应换用适合的数据结构。

**6. 自检**

对 `a = {4,2,2,5,1}`、`k = 3`，答案应为 `{2,2,1}`；第二个窗口出现重复最小值，队列会舍弃较早的 `2`，但最小值仍为 `2`。`k=1` 时结果应逐项等于原数组；`k=n` 时只返回全数组最小值；空数组、`k=0` 或 `k>n` 均返回空数组。扫描过程中可检查队列下标递增、所有下标均在当前窗口内、对应值严格递增。

**7. 坑**

- 结果少一个或区间错位：窗口是闭区间，只有 `i >= k-1` 才产生答案；第 `j` 项对应 `[j,j+k-1]`。
- 最小值偶尔错误：队尾条件方向写反，导致队首不再是窗口最小值候选；最小值应弹出所有值大于或等于当前值的候选。
- 旧元素影响当前答案：先移除所有过期下标，再读取队首。
- 用值而非下标入队：无法判断候选何时离开窗口；队列应保存数组下标，取值时再访问 `a[dq.front()]`。

**8. 一句话原理**

每个新元素淘汰它之后永远不可能更优的旧候选，队首因此始终给出当前窗口最小值。

**参考：**

- [OI Wiki：单调队列](https://oi-wiki.org/ds/monotonous-queue/)

## 5.4 堆与优先队列

**1. 它是做什么的**

堆适合在一批候选元素中反复取得当前优先级最高或最低者，同时允许新元素加入。C++ `priority_queue` 默认是大根堆，`top()` 返回最大值；指定 `greater<T>` 后成为小根堆。常用于贪心选择、Dijkstra 和 Top-K。它支持查看堆顶、插入和删除堆顶，不支持高效删除任意元素或直接修改堆中元素。

本模板把输入向量中的整数依次放入小根堆，再按从小到大顺序取出，返回一个新向量，不修改输入。初始化采用逐个 `push`，因此处理 `n` 个元素整体为 $O(n\log n)$；不能把此实现的建堆成本写成线性。单次 `top()` 为 $O(1)$，`push` / `pop` 为 $O(\log n)$，空间为 $O(n)$。若使用支持范围建堆的接口，复杂度会不同，但本模板没有这样做。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 输入整数序列，以常量引用传入，函数不改它。 |
| `minHeap` | 小根优先队列；每次 `top()` 是尚未取出的最小值。 |
| `sorted` | 新建的结果向量，按弹出次序收集所有元素。 |
| `x` | 当前从 `a` 读入并加入堆的整数。 |

堆不暴露元素下标，也不保证除堆顶外的元素有序。相同值可以重复存在；弹出的值按非降序排列，但相等元素之间没有可观察的先后差异。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `heapOrder(const vector<int>& a)` | 接收只读整数向量；返回 `vector<int>`。 | 将所有值压入局部小根堆，逐个弹出并返回升序副本；空输入返回空向量。 |
| `push(x)` | 插入一个元素，返回 `void`。 | 堆调整后仍保持比较器定义的优先级关系。 |
| `top()` | 无参数；返回堆顶元素的常量引用。 | 仅堆非空时可调用。 |
| `pop()` | 无参数；返回 `void`。 | 删除堆顶，不返回其值；需要该值时先保存 `top()`。 |
| `empty()` / `size()` | 无参数；分别返回空状态和元素数量。 | 可用于安全取堆顶的循环条件。 |

**4. 怎么调用**

需要最小值优先时声明 `priority_queue<T, vector<T>, greater<T>>`；最大值优先可用默认 `priority_queue<T>`。循环中先保存 `top()`，再 `pop()`。本模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 为待排序整数序列；返回按升序弹出的副本，不改 a。
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

片段可放在业务函数内。输入 `[8, 3, 5, 3]` 时，返回值为 `[3, 3, 5, 8]`：

```text
vector<int> a = {8, 3, 5, 3};
vector<int> result = heapOrder(a);
// result: 3 3 5 8；a 仍为 8 3 5 3
```

**5. 要改哪里**

- 要取最大值，改用默认大根堆；要按其他优先级排序，换元素类型或提供比较器，并明确比较器定义的“优先”方向。
- 要处理 `(距离, 点编号)` 等状态，可存 `pair`；`greater<pair<...>>` 按字典序比较，先比较距离，再比较点编号。
- 若在 Dijkstra 等算法中更新同一状态，不能原地修改堆内记录。可把新状态再次 `push`，取出时与当前最佳状态比较，跳过过期项；注意这种懒删除可能让堆暂时大于有效状态数。
- 要删除任意元素或频繁修改优先级，考虑维护索引的堆或其他数据结构；普通 `priority_queue` 没有对应接口。
- 若只想取得前 `k` 个值，可在读取至多 `k` 次后停止，不必把剩余元素全部弹出；堆仍需先容纳本模板插入的全部 `n` 个元素。

**6. 自检**

对 `[8, 3, 5, 3]`，小根堆连续弹出应为 `3, 3, 5, 8`，元素总数保持为 4，重复的 `3` 不会丢失。单元素 `[6]` 返回 `[6]`；空向量返回空向量。若去掉 `greater<int>`，同一输入应按 `8, 5, 3, 3` 弹出，借此确认比较器方向。

**7. 坑**

1. 默认 `priority_queue` 是大根堆；求最小值时忘记 `greater<T>` 会让结果顺序反过来。
2. 对空堆调用 `top()` 或 `pop()` 会导致未定义行为；先检查 `empty()`。
3. `pop()` 只删除，不返回元素；在删除前保存 `top()`。
4. 误以为堆内所有元素都已排序；只有堆顶有优先级保证，完整排序需反复弹出或使用排序算法。
5. 自定义比较器方向弄反会改变堆顶含义；用两个可区分元素手动核对比较关系。

**8. 一句话原理**

堆只维护最高优先级元素位于顶端，因此能快速查看它，并在每次插入或删除后用对数时间恢复这一结构。

**参考：**

- [OI Wiki：堆](https://oi-wiki.org/ds/heap/)

## 5.5 并查集

**1. 它是做什么的**

并查集维护元素只合并、不拆分的分组关系，支持判断是否同组、查询代表元和集合大小。元素编号为 `1..n`。构造初始化时间与空间为 $O(n)$；路径压缩配合按大小合并后，`find`、`unite`、`same`、`size` 的均摊时间为 $O(\alpha(n))$，其中 $\alpha$ 是反 Ackermann 函数。它不能任意拆分集合，也不直接维护集合内部路径等信息。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `parent[x]` | 元素 `x` 的父节点；根满足 `parent[x] == x`。 |
| `sizeOf[x]` | 仅当 `x` 是根时有效，表示该根代表的集合大小。 |
| `n` | 构造参数和最大合法编号；底层数组长为 `n+1`，下标 0 不作为元素使用。 |
| `a`, `b`, `x` | 操作涉及的元素编号，必须在 `1..n`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `DSU(n)` | 初始化 `1..n` 为 `n` 个单元素集合；构造参数应为非负数。 |
| `find(x)` | 要求 `x` 在 `1..n`；返回所在集合的根，并通过路径压缩修改访问路径上的 `parent`。 |
| `unite(a,b)` | 要求两参数均在 `1..n`；合并所在集合，成功返回 `true`，原已连通返回 `false`；成功时修改根的 `parent` 和 `sizeOf`。 |
| `same(a,b)` | 返回两元素是否同组；查询会调用 `find`，因此可能压缩路径。 |
| `size(x)` | 返回 `x` 所在集合大小；查询会调用 `find` 并可能压缩路径。 |

**4. 怎么调用**

创建对象后，对每条需要加入连通关系的边调用 `unite`；再用 `same` 或 `size` 查询：

```text
DSU dsu(4);
dsu.unite(1, 2);
dsu.unite(2, 3);
// dsu.same(1, 3) 为 true；dsu.size(2) 为 3
// dsu.unite(1, 3) 返回 false，因为二者已经连通
```

原模板：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct DSU {
    // parent[x] 指向父节点；仅根满足 parent[x]==x，且只有根的 sizeOf 有效。
    vector<int> parent, sizeOf;

    // 参数 n 是元素上界；建立编号 1..n 的单元素集合，初始化内部 parent/sizeOf。
    explicit DSU(int n) : parent(n + 1), sizeOf(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    // 参数 x 是 1..n 的元素；返回其集合根，并对访问路径做路径压缩。
    int find(int x) {
        if (parent[x] == x) return x;
        // 路径压缩保持集合不变，只把查询路径上的点直接挂到根。
        return parent[x] = find(parent[x]);
    }

    // 参数 a、b 是 1..n 的元素；合并两集合，成功返回 true、原已连通返回 false；修改根和集合大小。
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
    // 参数 a、b 是 1..n 元素；返回是否同属一集合，查询会通过 find 压缩路径。
    bool same(int a, int b) { return find(a) == find(b); }
    // 参数 x 是 1..n 元素；返回其所在集合大小，查询会通过 find 压缩路径。
    int size(int x) { return sizeOf[find(x)]; }
};
```

**5. 要改哪里**

- 若改成 0-based 编号，需同步调整数组长度、初始化范围和每个接口的合法下标。
- 若需维护集合聚合信息，在成功合并时将两个根的状态合并到新根；非根上的旧聚合值不再有效。
- 若需要按后进先出顺序撤销已记录的合并，可使用回滚并查集并记录每次修改；它只能按操作历史撤销，不能任意拆分某个集合。常见回滚实现不做路径压缩，以便恢复修改。
- 多组数据可每组重新构造对象；普通并查集不提供清空或撤销接口。

**6. 自检**

初始 `DSU(3)` 中 `same(1,2)` 为 `false`、`size(1)` 为 1。`unite(1,2)` 返回 `true` 后两点同组且大小为 2；再次 `unite(2,1)` 返回 `false`，大小仍为 2。再合并 2 和 3 后，三个元素应同组、`size(3)` 为 3。

**7. 坑**

- 直接改 `parent[a]`：`a` 可能不是根；先用 `find` 取得两个根。
- 读取非根的 `sizeOf`：集合大小只保证存于根节点。
- 把 `unite` 的返回值当新根：它只表示本次是否真正合并。
- 需要拆分却使用普通并查集：已合并的信息无法恢复；回滚也只支持按记录顺序撤销，不支持任意拆分。

**8. 一句话原理**

每个集合由根代表，合并时小树挂到大树上，查询时压缩访问路径。

**参考：**

- [OI Wiki：并查集](https://oi-wiki.org/ds/dsu/)

## 5.6 树状数组

**1. 它是做什么的**

树状数组维护长度 `n>=1` 的 1-based 数组的可加减信息，支持单点增加、前缀和与区间和。本模板另提供 `lowerBound`：在每个位置的频次非负时，找前缀和首次达到目标的位置。更新与每次查询均为 $O(\log n)$，空间为 $O(n)$；构造全零结构的初始化为 $O(n)$，若逐点插入初始值则为 $O(n\log n)$。它适合和、频次等可做加减的量，不直接支持任意区间最值或区间赋值。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `n` | 最大有效下标；合法位置为 `1..n`。 |
| `tree[i]` | Fenwick 分块和，覆盖 `(i-lowbit(i), i]`，其中 `lowbit(i) = i & -i`。 |
| `index` | `add` 的更新位置，或 `prefixSum` 的查询右端点；前者必须至少为 1，后者可为 0。 |
| `left`, `right` | `rangeSum` 的闭区间端点。若 `left > right`，实现返回 0。 |
| `target` | `lowerBound` 要达到的前缀和目标。 |
| `accumulated` | `lowerBound` 二进制提升过程中，已确认小于 `target` 的前缀和。 |

下标从 1 开始；`tree[0]` 不参与更新。`lowerBound(target)` 返回最小的 `i`，使 `prefixSum(i) >= target`；没有满足位置时返回 `n+1`。本实现对 `target <= 0` 返回 1。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `Fenwick(n)` | 创建最大下标为 `n` 的全零结构，内部数组长度为 `n+1`。 |
| `add(index, delta)` | 将位置 `index` 增加 `delta`，修改覆盖该位置的分块；要求 `1 <= index <= n`。 |
| `prefixSum(index)` | 返回闭区间 `[1,index]` 的和，`index` 可为 `0..n`；不修改结构。 |
| `rangeSum(left, right)` | 返回闭区间和 `prefixSum(right)-prefixSum(left-1)`；要求端点在有效范围内，空区间返回 0。 |
| `lowerBound(target)` | 在各点值非负时返回最小满足前缀和至少为 `target` 的下标；无解为 `n+1`。不修改结构。 |

**4. 怎么调用**

先构造容量，再用 `add` 记录每个位置的增量；前缀和与区间和可以随时查询。`lowerBound` 只适用于各点频次非负的情形，例如频次统计：

```text
Fenwick fw(5);
fw.add(1, 2);
fw.add(3, 1);
fw.add(5, 2);
// fw.prefixSum(3) == 3，fw.rangeSum(2, 5) == 3
// fw.lowerBound(4) == 5，fw.lowerBound(6) == 6（无解，n+1）
```

模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Fenwick {
    int n;
    // 仅使用 1..n；tree[i] 保存 (i-lowbit(i), i] 这一段的和。
    vector<ll> tree;

    // 参数 n 是正的最大下标；创建全零 1-based 树状数组，初始化内部 tree。
    explicit Fenwick(int n) : n(n), tree(n + 1, 0) {}

    // 参数 index 属于 1..n、delta 为增量；返回 void，修改覆盖 index 的 Fenwick 节点。
    void add(int index, ll delta) {
        // index 必须 >=1；向父区间跳转，直到超过 n。
        for (int i = index; i <= n; i += i & -i) tree[i] += delta;
    }

    // 参数 index 属于 0..n；返回原数组闭区间 [1,index] 的和，不改结构。
    ll prefixSum(int index) const {
        // 查询闭区间 [1,index]；每次删掉当前下标最低位的 1。
        ll result = 0;
        for (int i = index; i > 0; i -= i & -i) result += tree[i];
        return result;
    }

    // 参数 left/right 为合法 1-based 闭区间；返回当前区间和，不修改结构。
    ll rangeSum(int left, int right) const {
        if (left > right) return 0;
        return prefixSum(right) - prefixSum(left - 1);
    }

    // 频次数组非负时，返回最小 i 使 prefixSum(i)>=target；无解返回 n+1。
    // 参数 target 为目标前缀频次；要求各点频次非负，返回最小满足前缀和>=target 的下标，无解为 n+1。
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

**5. 要改哪里**

- 单点赋值需先保存旧值，再调用 `add(index, newValue-oldValue)`；直接把新值作为增量会把旧值重复计入。
- 若要维护频次并按累计频次定位，保证每次更新后每个位置的频次仍非负，再调用 `lowerBound`。普通数组值可以为负，但此时前缀和不再单调，不能用该函数二进制提升。
- 想从一组初始值建树，当前结构没有批量 `build` 接口；可逐点 `add`，时间为 $O(n\log n)$，或另行实现线性建树。
- 区间加、区间和等需求通常需要两棵树状数组并重新推导更新公式；区间最值或任意赋值应换用支持相应操作的数据结构。

**6. 自检**

上面的示例各点值为 `[2,0,1,0,2]`，所以前三项和为 `3`，区间 `[2,5]` 和为 `3`。累计和首次达到 4 的位置是 5；目标 6 大于总和 5，返回 `n+1=6`。单位置更新后可用 `rangeSum(i,i)` 核对；目标为 1 时应返回第一个正频次位置。更新下标 0 会导致循环无法前进，必须始终使用 `1..n`。

**7. 坑**

- 更新后程序卡住：`add(0, delta)` 中 `i & -i` 为 0，循环不前进；更新位置必须至少为 1。
- 区间和差一位：区间是闭区间，公式要减去 `prefixSum(left-1)`。
- `lowerBound` 给出错误位置：某次减量让某个点频次变成负数，前缀和不再单调；保持所有点频次非负。
- 无解时访问数组越界：目标超过总频次会返回 `n+1`，调用方要先处理这个哨兵值。
- `target <= 0` 的边界与直觉不同：本实现仍返回 1；若题意需要空前缀下标 0，需调整接口约定和实现。

**8. 一句话原理**

用 `i & -i` 把前缀拆成少量不重叠分块，并在二进制提升时跳过仍达不到目标的整段。

**参考：**

- [OI Wiki：树状数组](https://oi-wiki.org/ds/fenwick/)

## 5.7 线段树（区间加、区间和）

**1. 它是做什么的**

这棵线段树维护一个长度为 `n` 的 1-based 数组，支持把闭区间 `[l,r]` 每个数加上 `delta`，以及查询该区间的元素和。两种操作可以交错进行；单点加是 `rangeAdd(i,i,delta)`。适合区间更新和区间查询混合出现的场景，不能直接支持区间赋值或任意其他统计量。

构造对象及开辟数组空间为 $O(n)$；对初值建树为 $O(n)$；一次合法区间加或区间和查询为 $O(\log n)$。空间为 $O(n)$，本实现使用约 `4n` 个节点槽位。每个值及区间和均使用 `long long`，题目数据仍须保证乘法和总和不溢出。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 数组长度，必须大于 0。有效位置为 `1..n`。 |
| `sum[p]` | 线段树节点 `p` 所管理闭区间的当前总和，已计入该节点上的整段修改。 |
| `lazy[p]` | 已计入 `sum[p]`、但尚未传给孩子的每项增量。下传后必须清零，避免重复应用。 |
| `p, left, right` | 递归内部使用的节点编号和当前闭区间；不是使用者传入数组的零基下标。 |
| `ql, qr` | 查询或更新的目标闭区间，要求 `1 <= ql <= qr <= n`。 |
| `delta` | 对目标区间每个元素增加的值。 |
| `a` | 初始值向量；`a[1]` 到 `a[n]` 对应数组位置，`a[0]` 不参与构建。 |

内部节点的左右孩子分别代表 `[left,mid]` 和 `[mid+1,right]`。`sum[p]` 已计入本节点收到的更新；祖先尚未下传的标记可能还未反映在子节点中。访问子节点前必须先下传。若整段加 `delta`，总和应增加 `delta * (right-left+1)`。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及调用条件 |
|---|---|---|
| `SegmentTree(int n)` | 长度 `n`；构造对象。 | 分配并将 `sum`、`lazy` 初始化为零；要求 `n > 0`。 |
| `build(a)` | 1-based 初值向量；返回 `void`。 | 初始化节点和。仅应在刚构造的新对象上调用一次；它不清除已有 `lazy` 标记，带更新状态的对象不能靠再次 `build` 重置，应重新构造对象。 |
| 内部 `build(a,p,left,right)` | 初值及当前节点区间；返回 `void`。 | 递归建立 `sum`，不触碰 `lazy`，使用者无需直接调用。 |
| `apply(p,left,right,delta)` | 节点区间和增量；返回 `void`。 | 更新本段和与本段懒标记，供内部调用。 |
| `pushDown(p,left,right)` | 当前节点及其区间；返回 `void`。 | 将增量按左右子区间的实际长度下传并清空父标记；叶节点无需下传。 |
| `rangeAdd(l,r,delta)` | 合法 1-based 闭区间和增量；返回 `void`。 | 修改区间内所有元素。 |
| `rangeSum(l,r)` | 合法 1-based 闭区间；返回 `long long`。 | 查询区间和；查询时可能下传懒标记，但不改变逻辑数组的值。 |
| 内部重载 `rangeAdd` / `rangeSum` | 额外接收 `p,left,right`；更新返回 `void`，查询返回和。 | 递归实现，使用者调用公开的三参数或双参数接口即可。 |

**4. 怎么调用**

令 `n >= 1`，准备长度至少 `n+1` 的向量，使初值放在 `a[1..n]`；构造一个新对象并调用一次 `build(a)`。之后对所有操作使用合法闭区间。模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SegmentTree {
    int n;
    // 节点 p 管理闭区间 [left,right]。
    // sum[p] 已含本节点全部修改；lazy[p] 表示尚未下传给子节点的“每项增量”。
    vector<ll> sum, lazy;

    // 参数 n 为正数组长度；分配区间和与懒标记空间，初始值均为 0。
    explicit SegmentTree(int n) : n(n), sum(4 * n + 4), lazy(4 * n + 4) {}

    // 参数 a 为 1-based 初值；p 管理闭区间 [left,right]，递归写入 sum、不触碰 lazy；区间合法且非空，只应对全零新对象构建。
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

    // 参数 a[1..n] 是初值；返回 void，只初始化节点 sum，不清 lazy；须对刚构造的新对象调用一次，已有更新后重建需重新构造对象。
    void build(const vector<ll>& a) { build(a, 1, 1, n); }

    // 参数指定节点区间和增量 delta；返回 void，直接修改该节点 sum/lazy。
    void apply(int p, int left, int right, ll delta) {
        // 整段每项增加 delta，所以区间和增加 delta * 区间长度。
        sum[p] += delta * (right - left + 1);
        lazy[p] += delta;
    }

    // 参数 p 管理闭区间 [left,right]；返回 void，将未下传增量写到子节点并清父标记。
    void pushDown(int p, int left, int right) {
        if (lazy[p] == 0 || left == right) return;
        int mid = (left + right) / 2;
        // 下传必须使用子区间真实长度；完成后清空父标记，避免重复应用。
        apply(p * 2, left, mid, lazy[p]);
        apply(p * 2 + 1, mid + 1, right, lazy[p]);
        lazy[p] = 0;
    }

    // ql/qr 为待加闭区间，p,left,right 为当前节点；要求区间合法且相交，返回 void 并修改覆盖节点。
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

    // 参数 left/right 为合法 1-based 闭区间、delta 为每项增量；返回 void，更新覆盖节点的和及懒标记。
    void rangeAdd(int left, int right, ll delta) {
        rangeAdd(left, right, delta, 1, 1, n);
    }

    // ql/qr 为查询闭区间，p,left,right 为当前节点；返回两区间交集之和，并可能下传懒标记。
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

    // 参数为合法 1-based 闭区间；返回区间和，查询可能下传内部懒标记。
    ll rangeSum(int left, int right) {
        return rangeSum(left, right, 1, 1, n);
    }
};
```

片段可放在业务函数内。初值 `[1,2,3,4,5]`，将 `[2,4]` 每项加 `3` 后，数组逻辑值为 `[1,5,6,7,5]`，`rangeSum(3,5)` 返回 `18`：

```text
vector<ll> a = {0, 1, 2, 3, 4, 5}; // a[0] 不使用
SegmentTree st(5);
st.build(a);
st.rangeAdd(2, 4, 3);
ll answer = st.rangeSum(3, 5); // 18
```

**5. 要改哪里**

- 单点增量直接调用 `rangeAdd(i,i,delta)`；查询单点也可调用 `rangeSum(i,i)`。
- 若要区间赋值，需要新增赋值标记及其与加法标记的组合规则，不能把赋值当作一次区间加处理。
- 若要维护区间最小值/最大值等统计量，需修改 `sum` 的含义、节点合并方式、整段更新规则和查询返回值；仅改变量名不够。
- 若初值为全零，可不调用 `build`，因为构造函数已将节点初始化为零；有非零初值时必须构建。
- 多组数据或需要彻底重置时，为每组新建 `SegmentTree` 对象。当前 `build` 不清理旧懒标记，不能复用于已经做过更新的对象。
- 空数组不受支持；区间接口没有边界检查，调用者需保证 `1 <= l <= r <= n`。

**6. 自检**

初值 `[1,2,3,4,5]` 的总和是 `15`。执行 `rangeAdd(2,4,3)` 后，区间 `[2,4]` 的和应为 `18`，全数组和应为 `24`，`rangeSum(3,5)` 为 `18`。再执行 `rangeAdd(3,3,-6)`，位置 3 变为 0，`rangeSum(1,5)` 应为 `18`。单元素数组 `[7]` 上查询 `[1,1]` 得 `7`，加 `-7` 后得 `0`。这些检查也覆盖负增量和端点区间。

**7. 坑**

1. 把区间增量只加到区间和一次；正确增量是 `delta * 区间长度`。
2. 部分访问前未下传懒标记，子节点记录因此过期；检查递归进入孩子前是否调用 `pushDown`。
3. 下传后没清父标记会重复加；本模板在更新完孩子后将 `lazy[p]` 置零。
4. 把 0-based 区间传给接口；本模板所有公开区间和初值位置都是 1-based 闭区间。
5. 对已更新对象再次 `build` 试图重置；它只写 `sum`，不会清 `lazy`，重置时重新构造对象。

**8. 一句话原理**

整段更新先记在节点的和与懒标记中，只有递归访问子区间时才下传，从而避免逐个修改区间元素。

**参考：**

- [OI Wiki：线段树](https://oi-wiki.org/ds/seg/)

## 5.8 ST 表（静态 RMQ）

**1. 它是做什么的**

ST 表用于静态、不可修改的数组，预处理后查询闭区间最大值。本模板的数组按 `1..n` 存储，要求至少一个有效元素；构造时间和空间均为 $O(n\log n)$，每次查询为 $O(1)$。查询将两个长度为 $2^j$ 的区间合并，二者可能重叠，因此运算须同时满足结合律和幂等性；`max`、`min`、`gcd` 都满足这两个条件，区间和不满足幂等性，不能这样查询。数组修改后需重建或改用支持更新的结构。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `n` | 有效元素数，输入 `a` 的下标 `1..n` 有效，`a[0]` 不用。 |
| `levels` | 预处理层数，覆盖长度 `2^0` 至 `2^(levels-1)`。 |
| `log2Floor[len]` | `floor(log2(len))`，用于选取不超过查询长度的最大幂次。 |
| `st[j][i]` | 闭区间 `[i, i+2^j-1]` 的最大值；只有该区间完全落在数组内的位置才用于查询。 |
| `left`, `right` | `query` 的 1-based 闭区间端点。 |

对长度 `len=right-left+1`，令 `j=floor(log2(len))`、`blockLen=2^j`。查询合并 `[left,left+blockLen-1]` 与 `[right-blockLen+1,right]`：两段长度相同，第一段从 `left` 开始，第二段从 `right-blockLen+1` 开始；因 `2*blockLen >= len`，它们覆盖查询区间，重叠部分由幂等运算安全重复计算。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `SparseTableMax(a)` | 参数为 1-based 非空静态数组；构造各幂长区间的最大值表，不修改 `a`。 |
| `query(left,right)` | 参数为满足 `1<=left<=right<=n` 的闭区间；返回该段最大值，不修改表。 |

**4. 怎么调用**

先把数据放入长度 `n+1` 的数组并保留 `a[0]` 作为占位，再构造一次，之后可重复查询：

```text
vector<int> a = {0, 4, 2, 7, 1, 5};
SparseTableMax rmq(a);
// rmq.query(2, 5) 为 7；rmq.query(3, 4) 为 7
```

原模板：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct SparseTableMax {
    int n, levels;
    vector<int> log2Floor;
    // st[j][i] 保存闭区间 [i, i+2^j-1] 的最大值；输入 a 为 1-based。
    vector<vector<int>> st;

    // 参数 a 为 1-based 非空静态数组；构造各级区间最大值表，不修改 a。
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

    // 参数为合法闭区间 1<=left<=right<=n；返回该区间最大值，不修改表。
    int query(int left, int right) const {
        // max 可重复贡献：用两个可能重叠的 2^j 区间覆盖 [left,right]。
        int j = log2Floor[right - left + 1];
        return max(st[j][left], st[j][right - (1 << j) + 1]);
    }
};
```

**5. 要改哪里**

- 求区间最小值时，将构造和查询中的 `max` 都改为 `min`。
- 求 GCD 时将两处合并都改为 `gcd`，并确保运算实现可用。
- 区间和不满足重叠计算的幂等条件，应使用前缀和、树状数组或线段树。
- 数组发生修改后，当前表不会自动更新；可重建整张表，或换用支持修改的数据结构。

**6. 自检**

数组 `[4,2,7,1,5]` 映射到下标 `1..5` 后，`query(2,5)` 和 `query(3,4)` 都应为 7，单点 `query(4,4)` 应为 1。包含负数的数组 `[-8,-3,-11]` 上，`query(1,3)` 应为 -3，`query(2,3)` 应为 -3；这能检查最大值初始化和重叠区间起点是否正确。长度为 1 时唯一合法查询返回该元素。

**7. 坑**

- 把 `a[0]` 当有效数据：输入约定从 1 开始。
- 第二段起点写错：应为 `right-2^j+1`；漏掉 `+1` 会错位。
- 把 ST 表用于求和：两段会重叠，重叠元素被重复计入。
- 在数组修改后沿用旧表：查询仍反映构造时的数据。

**8. 一句话原理**

预存各个 2 的幂长度区间的最大值，再用两个可能重叠的等长区间覆盖查询段。

**参考：**

- [OI Wiki：ST 表](https://oi-wiki.org/ds/sparse-table/)

## 5.9 分块（区间加、区间和）

**1. 它是做什么的**

本模板把非空 1-based 数组分成约 $\sqrt n$ 个块，支持闭区间加一个增量和查询闭区间和。数组长度为 `n` 时，构造耗时、空间均为 $O(n)$；一次 `rangeAdd` 或 `rangeSum` 最多扫描两端散块并处理完整中间块，时间为 $O(\sqrt n)$。它适合整块更新和查询都容易维护的场景；区间最值、赋值等操作需要重新设计块内状态，不能直接使用本模板。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `value[i]` | 下标 `i` 的基础值，不含所在块的懒标记。实际值是 `value[i] + lazy[belong[i]]`。 |
| `sum[b]` | 块 `b` 所有 `value` 的和，同样不含懒标记。 |
| `lazy[b]` | 整块统一增加的量。整块实际和为 `sum[b] + lazy[b] * 块长`。 |
| `belong[i]` | 1-based 位置 `i` 所属的 0-based 块编号。 |
| `leftEnd[b]`, `rightEnd[b]` | 块 `b` 的实际闭区间端点；末块可能比其他块短。 |
| `blockSize`, `blockCount` | 目标块长和实际块数，块长取 `max(1, floor(sqrt(n)))`。 |

输入数组需满足 `a.size() >= 2`，有效元素为 `a[1..n]`，`a[0]` 不使用。元素、懒标记、整块和及其乘积均须能放入 `long long`。所有操作端点必须满足 `1 <= left <= right <= n`。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `SqrtDecomposition(a)` | 用 `a[1..n]` 初始化块，复制数据，不修改输入；要求数组非空且采用 1-based 存储。 |
| `rangeAdd(left,right,delta)` | 将闭区间内每项增加 `delta`，修改基础值或完整块懒标记，并同步散块的 `sum`；无返回值。 |
| `rangeSum(left,right)` | 返回当前闭区间和；读取散块时补上懒标记，读取完整块时整块计入标记贡献，不修改结构。 |

**4. 怎么调用**

先准备一个首项不用的数组，再构造一次；后续更新和查询都调用对象方法。下面片段可放在业务函数内：

```text
vector<long long> a = {0, 1, 2, 3, 4, 5};
SqrtDecomposition ds(a);
ds.rangeAdd(2, 4, 10);
// ds.rangeSum(1, 5) == 45；ds.rangeSum(2, 4) == 39
```

模板代码如下：

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

    // 参数 a[1..n] 为非空初始数组；构造块和懒标记副本，不修改 a。
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

    // 参数为合法闭区间及每项增量；返回 void，更新散块元素/整块懒标记。
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

    // 参数 left/right 为合法 1-based 闭区间；返回当前区间和，不修改结构。
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

**5. 要改哪里**

- 改成区间加、单点查询时，可查询 `value[i] + lazy[belong[i]]`；若还维护其他聚合量，需同步更新散块和完整块状态。
- 增加区间赋值、区间最值等操作时，必须重新定义懒标记和块汇总值的组合及更新规则；不能只把某个循环里的加法替换掉。
- 若采用不同块长，应同时检查两端扫描长度与中间块数量，确保最坏时间仍符合预期。多组数据应为每组重新构造对象；构造函数会初始化全部块状态。

**6. 自检**

示例初始数组为 `[1,2,3,4,5]`，对 `[2,4]` 加 10 后为 `[1,12,13,14,5]`，总和 45，区间 `[2,4]` 和为 39。可用长度为 1 的区间检查点值，再查询整段核对总和；特意选跨块区间和落在最后一个短块的区间，检查边界端点及实际块长是否正确。

**7. 坑**

- 整块更新后散块查询少算：`value` 不含 `lazy`，扫描单个元素时必须加上所在块标记。
- 整块查询重复或漏算标记：`sum[b]` 也不含标记，应额外加 `lazy[b] * 块长`。
- 最后一块结果错误：末块长度可能不足 `blockSize`，计算整块贡献应使用 `rightEnd[b]-leftEnd[b]+1`。
- 用 0-based 输入直接调用：构造和操作都约定有效下标从 1 开始，需先调整存储方式或改写映射。

**8. 一句话原理**

两端不完整的块逐项处理，中间完整块用块和与懒标记一次处理。

**参考：**

- [OI Wiki：分块](https://oi-wiki.org/ds/decompose/)

## 5.10 树状数组：区间加与区间和

**1. 它是做什么的**

`RangeFenwick` 在长度为 `n` 的 1-based 数组上支持闭区间加法和区间求和。它把数组变化表示为差分，再用两棵 5.6 节的 `Fenwick` 维护差分系数。适用于区间加、区间和交错出现；不能直接支持区间赋值或区间最值。

构造两棵全零树状数组为 $O(n)$ 时间和空间。一次区间加和一次区间求和均为 $O(\log n)$；查询前缀同样为 $O(\log n)$。非零初值需逐点调用 `addRange(i,i,a[i])`，总初始化时间为 $O(n\log n)$。数组值及中间乘积使用 `long long`，需保证数值不溢出。本代码依赖 5.6 节的 `Fenwick` 类型及 `ll` 别名；单独摘出代码块不能编译。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 逻辑数组长度；合法位置为 `1..n`，构造要求正数。 |
| `b1`、`b2` | 两棵差分 Fenwick，分别存差分值和乘以位置偏移后的系数。 |
| `x` | 前缀右端点，`prefix(x)` 接受 `0..n`。 |
| `l`、`r` | 公开区间的左右端点，使用 1-based 闭区间。 |
| `v` | 每个被覆盖位置增加的值。 |
| `addPoint(x,v)` | 内部更新差分端点；`n+1` 是区间右界之后的哨兵，不写入树。 |

设 `D[i]=A[i]-A[i-1]`，则 `A[i]` 是 `D[1..i]` 的和。对 `A[l..r]` 加 `v`，令 `D[l]+=v`、`D[r+1]-=v` 即可。前缀数组和由 `x * sum(D[1..x]) - sum((i-1)D[i])` 得出，即 `x*b1.prefixSum(x)-b2.prefixSum(x)`。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及调用条件 |
|---|---|---|
| `RangeFenwick(size)` | 长度 `size`；构造对象。 | 初始化两棵全零 Fenwick，逻辑数组初值全为 0；要求 `size > 0`。 |
| `addPoint(x,v)` | 差分位置 `x` 与增量；返回 `void`。 | 同步修改两棵树；允许 `x=n+1` 哨兵并忽略该更新。内部辅助函数，通常通过 `addRange` 使用。 |
| `addRange(l,r,v)` | 1-based 闭区间及增量；返回 `void`。 | 通过两个差分端点更新逻辑数组；若 `l>r` 则不做事。非空区间要求 `1<=l<=r<=n`。 |
| `prefix(x)` | `x` 属于 `0..n`；返回 `long long`。 | 返回逻辑数组 `[1,x]` 的和；`x=0` 返回 0。 |
| `query(l,r)` | 1-based 闭区间；返回 `long long`。 | 返回 `[l,r]` 的和；若 `l>r` 返回 0。非空查询须在数组范围内。 |
| 依赖的 `Fenwick::add` | 位置 `1..n` 和增量；返回 `void`。 | 更新单点差分系数；不能对位置 0 调用。 |
| 依赖的 `Fenwick::prefixSum` | 位置 `0..n`；返回前缀和。 | 被 `prefix` 调用以取得系数前缀。 |

**4. 怎么调用**

先提供 5.6 节的 `Fenwick` 和 `ll` 定义，再构造 `RangeFenwick(n)`。它默认代表全零数组；非零初值按点初始化，然后使用 `addRange` 和 `query`。模板如下：

```cpp

struct RangeFenwick {
    // 两棵树保存差分系数，prefix(x)=x*B1.prefix-B2.prefix。
    int n;
    Fenwick b1,b2;
    // 参数 size 为正数组长度；初始化两棵差分 Fenwick，逻辑数组初始为零。
    explicit RangeFenwick(int size) : n(size), b1(size), b2(size) {}
    // 参数 x 属于 1..n+1，v 是差分增量；返回 void，更新系数树，n+1 哨兵不写树。
    void addPoint(int x, ll v) {
        // 差分在 l 加 v、在 r+1 减 v；n+1 的哨兵不需要写入树中。
        if (x <= n) {
            b1.add(x, v);
            b2.add(x, v * (x - 1));
        }
    }
    // 参数为 1-based 闭区间及增量；返回 void，修改两棵树表示的逻辑数组，空区间无操作。
    void addRange(int l, int r, ll v) {
        if (l > r) {
            return;
        }
        addPoint(l, v);
        addPoint(r + 1, -v);
    }
    // 参数 x 属于 0..n；返回逻辑数组 [1,x] 之和，不修改树。
    ll prefix(int x) const {
        return b1.prefixSum(x) * x - b2.prefixSum(x);
    }
    // 参数为合法闭区间；返回逻辑数组区间和，空区间返回 0。
    ll query(int l, int r) const {
        return l > r ? 0 : prefix(r) - prefix(l - 1);
    }
};
```

片段可放在业务函数内。初值 `[1,2,3,4,5]`，对 `[2,4]` 加 2 后数组为 `[1,4,5,6,5]`，查询 `[3,5]` 得 `16`：

```text
RangeFenwick fw(5);
for (int i = 1; i <= 5; ++i) fw.addRange(i, i, i);
fw.addRange(2, 4, 2);
long long answer = fw.query(3, 5); // 16
```

**5. 要改哪里**

- 单点增加用 `addRange(i,i,v)`；区间和使用 `query(l,r)`。
- 非零初值逐点调用 `addRange(i,i,a[i])`，总计 $O(n\log n)$；本模板没有线性建树接口。
- 区间赋值、区间最值等需求不能只改查询公式；差分及两棵和树的状态不足以维护它们，需换用或设计相应数据结构。
- 空更新区间 `l>r` 会忽略；空查询区间 `l>r` 返回 0。其他下标没有边界检查，调用者须保证合法。
- `r=n` 时 `r+1` 是 `n+1` 哨兵，`addPoint` 会跳过它；不要把哨兵传入底层 `Fenwick::add`。更新位置不能为 0。

**6. 自检**

构造长度 5 的全零数组，逐点加入 `[1,2,3,4,5]` 后 `query(1,5)` 应为 15。将 `[2,4]` 加 2 后，逻辑值为 `[1,4,5,6,5]`，`query(3,5)` 为 16，`query(1,1)` 仍为 1。`query(2,1)` 返回 0，`addRange(4,3,100)` 不改变数据。再执行 `addRange(5,5,1)`，`query(5,5)` 应为 6，可核对右端点哨兵。

**7. 坑**

1. 区间加没有转为两个差分端点；应在 `l` 加 `v`、在 `r+1` 减 `v`。
2. 忘记偏移树 `b2` 或写错 `x-1`，前缀公式会出错；核对 `x*b1.prefixSum(x)-b2.prefixSum(x)`。
3. `r=n` 时把 `n+1` 传给底层 Fenwick；底层合法下标只有 `1..n`，本实现会忽略哨兵。
4. 初始化非零数组后遗漏逐点加入；构造函数只创建全零逻辑数组。
5. 复制此结构时漏掉 5.6 节的 `Fenwick` / `ll`；需将依赖一并提供。

**8. 一句话原理**

把区间加转换为差分数组的两个端点变化，再用两棵 Fenwick 将差分前缀还原成原数组前缀和。

**参考：**

- [OI Wiki：树状数组](https://oi-wiki.org/ds/fenwick/)

## 5.11 DFS 序与子树展平

**1. 它是做什么的**

对一棵静态、连通无向树选定根后，DFS 序把每个节点的子树映射为连续闭区间 `[tin[u],tout[u]]`。因此可把子树查询或修改交给树状数组、线段树等区间结构。建序耗时 $O(n)$，辅助空间为 $O(n)$。本模板每个节点只记录一次，不是 LCA 常用的进入与回溯都记录的欧拉游程。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `g` | 1-based 无向邻接表。 |
| `timer` | 已进入 DFS 的节点数；每进入一个节点递增一次。 |
| `tin[u]` | 节点 `u` 的进入时间戳。 |
| `tout[u]` | `u` 子树遍历完成时的时间戳，与 `tin[u]` 构成闭区间。 |
| `order[t]` | DFS 时间戳 `t` 对应的节点编号，即 `order[tin[u]] == u`。 |
| `u`, `p` | 当前节点及父节点；根调用时父节点传 0。 |

两种映射用途不同：若要把每个节点的点值放进线段树或树状数组，应按 `tin[u]` 作为位置写入；若要逐个枚举子树节点，则遍历 `t=tin[u]..tout[u]`，并用 `order[t]` 取回节点编号。不能把时间戳 `t` 当成点编号。

例如边为 `1-2、1-3、2-4、2-5`，根为 1 且按邻接顺序访问时，`order` 为 `[1,2,4,5,3]`；节点 2 的区间 `[2,4]` 对应节点 2、4、5。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `DfsOrder(n)` | 分配图和序列数组；点编号范围为 `1..n`，应传正点数。 |
| `addEdge(u,v)` | 参数为合法树点编号；向 `g` 双向加入一条边，修改邻接表，无返回值；每条无向边只调用一次。 |
| `dfs(u,p)` | 从 `u` 开始遍历，写入 `tin`、`tout`、`order` 并增加 `timer`，无返回值；输入必须是树且不能形成递归环。根的 `p` 传 0，整张树由调用方指定根后调用一次。 |

**4. 怎么调用**

先构造对象并加入全部 `n-1` 条边，再从选定根调用 `dfs(root,0)`。之后点值按 `tin` 放入区间结构，或通过 `order` 枚举子树：

```text
DfsOrder d(5);
d.addEdge(1, 2); d.addEdge(1, 3);
d.addEdge(2, 4); d.addEdge(2, 5);
d.dfs(1, 0);
// tin[2]=2、tout[2]=4；order[2..4] 为 2,4,5
// 将点值 value[u] 写入序列位置 tin[u]；枚举子树 2 则读取 order[2..4]
```

原模板：

```cpp

struct DfsOrder {
    vector<vector<int>> g;
    vector<int> tin,tout,order;
    int timer=0;
    // 参数 n 为树点数；分配 1-based 图与 DFS 序数组，timer 初始为 0。
    explicit DfsOrder(int n)
        : g(n + 1), tin(n + 1), tout(n + 1), order(n + 1) {}
    // 参数 u、v 是 1..n 树点；返回 void，向 g 双向加入边；建 DFS 序前每条树边调用一次。
    void addEdge(int u, int v) {
        g[u].push_back(v);
        g[v].push_back(u);
    }
    // 参数 u 是当前子树根、p 是父点（根传 0）；返回 void，写 tin/tout/order/timer；输入须为树。
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

**5. 要改哪里**

- 更换根或重新计算 DFS 序：创建新对象，重新加入全部边，再调用 `dfs(newRoot,0)`。旧对象的 `timer` 和时间戳已被使用；不必在它上面清空图。
- 子树点值求和或更新：把 `value[u]` 放在位置 `tin[u]`，对闭区间 `[tin[u],tout[u]]` 操作。
- 需要枚举子树中的原节点编号：对 `t` 遍历该闭区间，再读取 `order[t]`。这是枚举映射，不等同于直接把 DFS 位置当作节点编号。
- 需要 LCA 的欧拉游程：另建会在进入及回溯时记录节点的序列，当前 `order` 每点只出现一次。

**6. 自检**

按示例树从根 1 遍历，应得到 `tin[1]=1`、`tin[2]=2`、`tin[4]=3`、`tin[5]=4`、`tin[3]=5`，并有 `tout[2]=4`。每个节点的 `tout[u]-tin[u]+1` 应等于其子树节点数；节点 2 的区间位置 `2..4` 映回节点应为 `2,4,5`。

**7. 坑**

- 把区间端点当半开区间：本模板的 `[tin,tout]` 两端都包含。
- 把 `order` 位置当作节点编号：应使用 `order[t]` 映回节点。
- 对一般图直接运行：代码只跳过父节点，没有 visited 标记；输入需为树。
- 重用已遍历对象：`timer` 和数组不会自动重置；重根或重新建序时新建对象并重新加边。

**8. 一句话原理**

DFS 完整遍历完一个节点的子树后才离开它，因此子树节点的进入时间连续排列。

## 5.12 树链剖分

**1. 它是做什么的**

树链剖分把一棵 1-based 连通无向树上两点间的路径拆成 $O(\log n)$ 个连续位置区间，供线段树等结构逐段处理。建树剖分耗时 $O(n)$、空间 $O(n)$；本模板的 `forPath` 产生 $O(\log n)$ 段。若每段在线段树上查询或更新一次，单次路径操作为 $O(\log^2 n)$。回调收到的区间端点闭合，但区间顺序不保证等于从 `u` 到 `v` 的路径顺序；可用于可交换聚合或各段独立更新。需要方向敏感的非交换运算时，必须额外记录方向并按路径顺序合并。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `g[u]` | 无向邻接表；所有边必须在 `build` 前加入。 |
| `parent[u]`, `depth[u]` | 以指定根定根后的父节点和深度，根深度为默认初值 0。 |
| `sz[u]` | 以 `u` 为根的子树大小。 |
| `heavy[u]` | `u` 的最大子树孩子；无孩子时为 `-1`。 |
| `top[u]` | `u` 所在重链的链头。 |
| `pos[u]` | 剖分后的 1-based 连续位置；同一重链连续，子树也对应连续区间。 |
| `timer` | 分配 `pos` 时递增的全局位置计数器；对象构造时为 0。 |

点编号和剖分位置是两个不同维度：路径区间传给维护结构时使用 `pos`，建树时遍历点编号，令 `base[pos[u]]=weight[u]` 即可，不需要逆映射；若要从位置取回点编号，再另建 `vertexAt[pos[u]]=u`。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `HLD(nodeCount)` | 分配 `1..nodeCount` 的邻接表和数组；点数应为正。 |
| `dfs1(u,p)` | 内部递归，设置父亲、深度、子树大小及重儿子，返回子树大小；在合法树上由 `build` 调用。 |
| `dfs2(u,head)` | 内部递归，设置链头和位置，并优先遍历重儿子；无返回值。 |
| `build(root)` | 完成剖分；要求所有边已加入，`root` 在 `1..n`。对象只应构建一次；重复构建前须创建新对象，因为 `timer` 和 `heavy` 不会清零。省略参数时根为 1。 |
| `forPath(u,v,use)` | 将路径拆成闭区间并逐段调用 `use(l,r)`；回调返回值被忽略，需通过捕获外部对象实现查询或更新。区间参数是剖分位置，次序不承诺对应原路径方向。 |

**4. 怎么调用**

先加边，再调用一次 `build`；随后让 `forPath` 的回调把区间交给线段树。下例为链 `1-2-3`，路径查询得到的位置区间 `[1,3]`：

```text
HLD hld(3);
hld.g[1].push_back(2); hld.g[2].push_back(1);
hld.g[2].push_back(3); hld.g[3].push_back(2);
hld.build();
// l/r 为剖分位置闭区间；回调输出端点，不修改 hld。
hld.forPath(1, 3, [&](int l, int r) { cout << l << " " << r << "\n"; });
// 输出：1 3
```

模板代码如下：

```cpp

struct HLD {
    // heavy 子树最大者优先同链；任意树路径被拆成 O(log n) 个连续区间。
    int n,timer=0;
    vector<vector<int>> g;
    vector<int> parent,depth,sz,heavy,top,pos;
    // 参数 nodeCount 为点数；分配 1-based 邻接表和剖分数组，所有位置初始未构建。
    explicit HLD(int nodeCount)
        : n(nodeCount), g(nodeCount + 1), parent(nodeCount + 1),
          depth(nodeCount + 1), sz(nodeCount + 1),
          heavy(nodeCount + 1, -1), top(nodeCount + 1), pos(nodeCount + 1) {}
    // 参数 u 为当前子树根、p 为父点；返回子树大小，并写 parent/depth/sz/heavy；须在树上调用。
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
    // 参数 u 为子树根、head 为其重链链头；返回 void，按重儿子优先写 top/pos 并递增 timer。
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
    // 参数 root 是 1..n 的定根；返回 void，以当前 g 首次建立父深度、重儿子和重链位置。要求新对象且先加完所有边；重复 build 前须重新创建对象，因为 timer/heavy 不会清零。
    void build(int root = 1) {
        dfs1(root, 0);
        dfs2(root, root);
    }
    // 参数 u/v 为树上端点，use(l,r) 接收闭区间且返回值被忽略，可更新调用方维护的结构；返回 void，仅改局部端点副本，区间顺序不保证路径方向。
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


若要实际查询点权路径和，先提供 5.7 节的 `SegmentTree`，再将点权放到剖分位置上。接着上面的三点链，在业务函数中继续写：

```text
vector<ll> weight = {0, 10, 20, 30}, base(4);
for (int u = 1; u <= 3; ++u) base[hld.pos[u]] = weight[u];
SegmentTree st(3);
st.build(base);
ll pathSum = 0;
// l/r 为剖分位置闭区间；将该段和累加到 pathSum，返回 void。
hld.forPath(1, 3, [&](int l, int r) { pathSum += st.rangeSum(l, r); });
// pathSum == 60
```

子树查询可直接使用 `[pos[u], pos[u]+sz[u]-1]`，同样交给数组维护结构处理。

**5. 要改哪里**

- 点权路径查询或更新：把回调区间 `[l,r]` 交给线段树处理，线段树下标使用 `pos`。
- 边权路径查询：约定每条边的权值放在较深端点对应的位置；当两个端点落在同一条链时，最终区间要从 `pos[LCA]+1` 开始，排除代表 LCA 的位置。跨链段的链头位置代表的是与父亲相连的边，应保留。
- 非交换聚合（如字符串拼接、矩阵乘法）：当前回调区间无方向信息且分段顺序不保证，需改写分解接口，同时维护从两端收集的区间和方向；不能直接按回调顺序合并。
- 多测或更换根：每组数据/每次重建创建新对象，将边加入后以新根调用 `build(root)`。不要在旧对象上重复 `build`。

**6. 自检**

在链 `1-2-3` 上构建后，`forPath(1,3,...)` 应只回调一次，区间为 `[1,3]`；`forPath(2,2,...)` 应得到单点区间。再用树 `1-2, 1-3` 测 `forPath(2,3,...)`，回调区间覆盖点 2、1、3 对应的位置，不能遗漏 LCA。边权版本还要确认同链查询排除了 LCA 的位置。

**7. 坑**

- 结果像用了旧树：在加完边之前调用了 `build`；先完整建图再剖分。
- 第二次 `build` 位置异常：`timer` 未归零且 `heavy` 可能残留；每次重建使用新对象。
- 路径和/最值适用、路径拼接错误：回调区间顺序不保证路径方向；方向敏感操作需同时维护区间方向和两端的合并顺序。
- 边权答案多一条或少一条：最终同链段包含 LCA；将该段左端改为 `pos[LCA]+1`。

**8. 一句话原理**

每次跳过一条重链的链头向父亲移动，轻边跳转次数为 $O(\log n)$，每条重链则映射成连续位置区间。

## 5.13 线段树：区间加、赋值与求和

**1. 它是做什么的**

`AssignAddSegmentTree` 在长度为 `n` 的 1-based 数组上支持三种操作：把闭区间每项加上一个值、把闭区间每项设成同一个值、查询闭区间和。适合两种更新交错出现的场景；数组值、区间和及乘积必须能放进 `long long`。

构造节点空间为 $O(n)$，调用 `build` 初始化为 $O(n)$；一次区间加、区间赋值或区间求和均为 $O(\log n)$；空间为 $O(n)$，节点数组约为 `4n`。要求 `n>=1`，公开操作的区间须满足 `1<=l<=r<=n`，接口不检查这些条件。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 数组长度；位置从 1 到 `n`。 |
| `tr[p].sum` | 节点 `p` 管辖区间的当前总和，包含本节点尚未下传的更新效果。 |
| `tr[p].hasSet` | 是否存在等待下传的赋值操作；赋值为 0 时也必须为真。 |
| `tr[p].setValue` | `hasSet` 为真时，表示该节点区间每项待赋成的值。 |
| `tr[p].add` | 独立的待下传增量；若赋值标记存在，之后的增量会合并进 `setValue`，不另存此标记。 |
| `p,l,r` | 递归内部的节点编号和它管理的闭区间。 |
| `ql,qr` | 更新或查询目标闭区间；所有接口采用 1-based 下标。 |
| `assign` | 内部更新参数；真表示赋值，假表示加法。公开接口会替调用者设置它。 |

标记表示对整段尚未传给孩子的操作。组合顺序遵循时间先后：新赋值会覆盖旧赋值和旧加法；有赋值标记时再加 `delta`，应把 `delta` 加到待赋值数上；没有赋值标记时，加法累积在 `add` 中。向下传递时先赋值，再加法。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及调用条件 |
|---|---|---|
| `AssignAddSegmentTree(size)` | 正数组长度；构造对象。 | 创建初值为零、无标记的节点空间。 |
| `build(a)` | 1-based 初值 `a[1..n]`；返回 `void`。 | 仅初始化 `sum`，不清懒标记；在新对象上调用，重置需重新构造。 |
| 内部 `build(p,l,r,a)` | 初值和当前区间；返回 `void`。 | 递归写叶值并合并区间和，不重置标记；无需直接调用。 |
| `applySet(p,l,r,value)` | 当前节点和赋值值；返回 `void`。 | 更新区间和，设置赋值标记并清除加法标记。 |
| `applyAdd(p,l,r,delta)` | 当前节点和增量；返回 `void`。 | 更新区间和；依据是否已有赋值标记，把增量合并到赋值值或独立加法标记。 |
| `push(p,l,r)` | 当前节点及闭区间；返回 `void`。 | 先把赋值、再把加法下传到左右孩子，并清除父标记；内部调用。 |
| `rangeAdd(l,r,value)` | 合法闭区间和增量；返回 `void`。 | 将每个区间元素增加 `value`。 |
| `rangeSet(l,r,value)` | 合法闭区间和赋值值；返回 `void`。 | 将每个区间元素覆盖为 `value`，包括 0。 |
| `rangeSum(l,r)` | 合法闭区间；返回 `long long`。 | 返回区间和；部分查询可能下传标记。 |
| 内部 `update` / `query` | 当前节点、目标区间和操作参数；更新返回 `void`，查询返回区间和。 | 递归处理；通常使用上述公开接口，不直接调用。 |

**4. 怎么调用**

构造正长度的新对象；若有非零初值，准备 `a[1..n]` 并调用一次 `build(a)`。之后按需要调用 `rangeSet`、`rangeAdd` 和 `rangeSum`。模板如下：

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

    // 参数 size 为正数组长度；分配初始零值节点，标记均无效。
    explicit AssignAddSegmentTree(int size) : n(size), tr(4 * size + 4) {}

    // 参数 p 管理闭区间 [l,r]、value 为赋值；返回 void，覆盖该节点和并设置赋值标记。
    void applySet(int p, int l, int r, ll value) {
        // 覆盖整个节点：清除旧加法，并留下待下传的赋值。
        tr[p].sum = value * (r - l + 1);
        tr[p].setValue = value;
        tr[p].add = 0;
        tr[p].hasSet = true;
    }
    // 参数 p 管理闭区间 [l,r]、delta 为增量；返回 void，修改该节点和并合并加法/赋值标记。
    void applyAdd(int p, int l, int r, ll delta) {
        tr[p].sum += delta * (r - l + 1);
        // 赋值标记仍在时把增量合并到赋值值，否则累积为独立加法标记。
        if (tr[p].hasSet) tr[p].setValue += delta;
        else tr[p].add += delta;
    }
    // 参数 p 管理闭区间 [l,r]；返回 void，按赋值后加法顺序下传标记并清理父标记。
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
    // 参数 a 为 1-based 初值，p 管理闭区间 [l,r]；返回 void，递归建立节点和。
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
    // 参数 a[1..n] 为初值；返回 void，只建立节点和、不清懒标记；须在新对象上初始化，重置需重新构造对象。
    void build(const vector<ll>& a) { build(1, 1, n, a); }

    // 参数 p/l/r 为当前节点，ql/qr 为合法修改区间，value 为操作值、assign 选择赋值或加法；返回 void 并更新节点。
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
    // 参数为合法闭区间及增量；返回 void，将区间每项增加 value 并修改树状态。
    void rangeAdd(int l, int r, ll value) { update(1, 1, n, l, r, value, false); }
    // 参数为合法闭区间及赋值；返回 void，将区间每项设为 value 并修改树状态。
    void rangeSet(int l, int r, ll value) { update(1, 1, n, l, r, value, true); }

    // 参数 p/l/r 为当前节点，ql/qr 为合法查询区间；返回交集和，并可能下传懒标记。
    ll query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[p].sum;
        push(p, l, r);
        int m = (l + r) / 2;
        ll result = 0;
        if (ql <= m) result += query(p * 2, l, m, ql, qr);
        if (qr > m) result += query(p * 2 + 1, m + 1, r, ql, qr);
        return result;
    }
    // 参数为合法闭区间；返回区间和，查询可能下传内部标记。
    ll rangeSum(int l, int r) { return query(1, 1, n, l, r); }
};
```

片段可放在业务函数内。初值 `[1,2,3,4,5]`，先将 `[2,4]` 赋成 `7`，再给 `[3,5]` 加 `2`，数组变成 `[1,7,9,9,7]`，`rangeSum(2,5)` 返回 `32`：

```text
vector<ll> a = {0, 1, 2, 3, 4, 5};
AssignAddSegmentTree st(5);
st.build(a);
st.rangeSet(2, 4, 7);
st.rangeAdd(3, 5, 2);
ll answer = st.rangeSum(2, 5); // 32
```

**5. 要改哪里**

- 单点操作用 `[i,i]` 区间即可，例如 `rangeSet(i,i,v)` 或 `rangeAdd(i,i,d)`。
- 若只需要区间加与区间和，可使用更简单的 5.7 节模板；若还需要区间最值，须重新设计节点聚合和更新逻辑。
- 要增加新的更新类型，须定义其对 `sum` 的影响、懒标记的存法，以及它与现有赋值和加法标记的时间顺序组合；不能只增加一个接口函数。
- 初始数组全零时，构造后的逻辑值已为零，可跳过 `build`。非零初值需在新对象上构建。多测重置或重复初始化时重新构造对象，因为 `build` 不会清理旧标记。
- `n` 必须为正数，区间须合法；实现不做边界检查。还需保证所有中间乘法和区间和不溢出 `long long`。

**6. 自检**

对初值 `[1,2,3,4,5]`，先 `rangeSet(2,4,7)` 后为 `[1,7,7,7,5]`；再 `rangeAdd(3,5,2)` 后为 `[1,7,9,9,7]`，全数组和为 33，`rangeSum(2,5)` 为 32。再把 `[1,5]` 赋为 0，查询 `[1,5]` 必须得到 0，这能检查“赋值为零”由 `hasSet` 区分的行为。单元素数组 `[6]` 执行加 `-2` 后查询得 4；随后赋值 0 得 0。

**7. 坑**

1. 用 `setValue==0` 判断是否有赋值标记；0 是合法赋值，必须看 `hasSet`。
2. 有待下传赋值时仍把新加法记入独立 `add`；本实现将它合并到 `setValue`，保证时间顺序正确。
3. 下传时先加后赋值，会把较新的加法覆盖掉；应先下传赋值，再下传加法。
4. 用 `build` 重建一个已操作的对象；该函数只写节点和、不清标记，应重新构造对象后初始化。
5. 更新或查询越界、使用 0-based 区间；公开接口无边界保护，必须传入合法 1-based 闭区间。

**8. 一句话原理**

线段树用赋值标记表达覆盖、用加法标记表达增量，并按操作发生顺序合并和下传，从而在对数时间内维护区间和。

## 5.14 DSU on Tree（树上启发式合并）

**1. 它是做什么的**

给定一棵静态有根树和每个节点的颜色，本模板一次求出所有节点子树中的不同颜色数。颜色可以是负数或很大的整数，模板会先离散化。输入是 1-based 连通无向树 `tree`、颜色数组 `color[1..n]` 和根 `root`；`solve()` 返回长度 `n+1` 的数组，`answer[u]` 是节点 `u` 的子树答案，0 号位不用。

DSU on Tree 负责安排哪些节点加入或移出当前集合，桶、树状数组或线段树负责维护集合里的统计。本模板用颜色频次桶统计不同颜色数。它与普通并查集不同：这里没有合并集合代表元的操作，保留的是重儿子已经算好的频次状态。适合离线回答固定根下的子树统计，不直接支持在线改色、动态换根或路径查询。

预处理 DFS 序为 $O(n)$，颜色排序与压缩为 $O(n\log n)$。统计中节点的加入、删除共 $O(n\log n)$ 次；本模板每次频次变化为 $O(1)$，所以总时间为 $O(n\log n)$、额外空间为 $O(n)$，包括递归栈。若改用每次增删为 $O(\log n)$ 的统计结构，统计总时间就会变成 $O(n\log^2 n)$。这些界限还要求每个节点的答案能在对应代价内读出。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `tree`、`color` | 输入树和颜色的常量引用；被引用对象必须比求解器活得更久。 |
| `n`、`root` | 节点数与固定根；要求 `n>=1`、`1<=root<=n`。 |
| `parent[u]`、`subtreeSize[u]` | 定根后的父节点与子树大小。 |
| `heavy[u]` | 子树最大的那个儿子；叶子为 0。大小并列时选最先遇到的一个即可。 |
| `tin[u]`、`tout[u]` | 子树在 DFS 序上的闭区间 `[tin[u],tout[u]]`。 |
| `order[i]` | DFS 位置 `i` 对应的节点编号，满足 `order[tin[u]]==u`。 |
| `compressed[u]` | 节点 `u` 的颜色编号，范围为 `0..颜色种类数-1`。 |
| `frequency[c]`、`distinct` | 当前活跃集合中颜色编号 `c` 的次数，以及次数非零的颜色数。 |
| `answer[u]`、`timer` | 各子树答案，以及预处理时分配 DFS 位置的计数器。 |
| `keep` | 当前子树算完后是否保留频次；不是永久标记，也不表示跳过该子树。 |

例如边按 `1-2、1-3、2-4、2-5` 加入，根为 1，DFS 顺序是 `order[1..5]=[1,2,4,5,3]`。子树 2 对应位置 `[2,4]`，映回节点是 `{2,4,5}`。枚举它时先取 `order[i]`，再读该节点颜色；不能把位置 `i` 直接当节点号。

统计结构的下标由统计维度决定：这里是 `frequency[compressed[u]]`；若按深度计数，则用深度作桶或线段树的下标。只有维护“DFS 位置上的点值”时才把 `tin[u]` 用作线段树位置，不能把所有统计都套到 DFS 下标上。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `DSUOnTree(tree,color,root)` | 保存输入引用并分配内部数组；树必须连通无环，颜色数组覆盖 `1..n`，构造时不修改输入。 |
| `prepare(u,p)` | 内部预处理；`u` 是当前点，`p` 是父点，根传 0；返回子树大小，并写父节点、DFS 区间和重儿子。 |
| `build()` | 无参数、无返回值；清空旧预处理状态，再以 `root` 建立 DFS 序等信息。只做结构预处理，不初始化频次。 |
| `changeColor(x,delta)` | 内部把节点 `x` 的颜色次数增减 1，`delta` 为 `+1/-1`；无返回值，修改频次和 `distinct`。压缩与频次数组须已就绪，删除的是当前集合中已有的节点贡献。 |
| `addSubtree(u,add)` | 内部枚举 `[tin[u],tout[u]]`，`add=true` 加入、`false` 移除；无返回值，修改频次状态，依赖预处理与频次初始化。 |
| `dfs(u,p,keep)` | 内部统计；记录 `u` 子树答案，`keep=true` 保留贡献，`false` 则移除；无返回值，修改答案与活跃集合。只应由 `solve()` 从空状态启动。 |
| `solve()` | 无参数；重新预处理、压缩颜色、清空频次后计算全部答案，返回 `vector<int>`；不修改输入，允许重复调用。 |

业务代码只需构造对象并调用 `solve()`。内部过程在计算 `u` 的答案时按以下顺序执行：

1. 递归处理所有轻儿子，传 `keep=false`；各自记下答案后清空，避免污染兄弟子树。
2. 递归处理重儿子，传 `keep=true`；保留它的整棵子树贡献。
3. 枚举每棵轻子树重新加入，再加入 `u` 自己；重子树已经在集合中，不能再加一次。
4. 此时活跃集合恰好是 `u` 的子树，令 `answer[u]=distinct`。
5. 若本层 `keep=false`，移除 `u` 整棵子树；否则保留给父层继续用。

在上述五点树中，颜色设为 `[3,3,5,5,3]`。根的轻儿子 3 先得到答案 1 后清空。处理重儿子 2 时，先算轻儿子 5 并清空，再保留重儿子 4 的颜色 5；重新加入节点 5 的颜色 3 和节点 2 的颜色 3 后，频次为 `{3:2,5:1}`，得到 `answer[2]=2`。回到根，再加入节点 3 和根，频次为 `{3:3,5:2}`，得到 `answer[1]=2`。

**4. 怎么调用**

先准备树和颜色，再构造求解器。以下模板统计不同颜色数，无需额外接线段树：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct DSUOnTree {
    int n, root;
    const vector<vector<int>>& tree;
    const vector<int>& color;
    vector<int> compressed, parent, subtreeSize, heavy;
    vector<int> tin, tout, order, frequency, answer;
    int timer = 0, distinct = 0;

    // 输入 tree 为 1-based 连通无向树，color[1..n] 为任意整数颜色；引用对象须长于本对象。
    // 初始化数组；不修改 tree 或 color。要求 n>=1 且 root 在 1..n。
    DSUOnTree(const vector<vector<int>>& tree, const vector<int>& color, int root)
        : n((int)tree.size() - 1), root(root), tree(tree), color(color),
          compressed(n + 1), parent(n + 1), subtreeSize(n + 1), heavy(n + 1, 0),
          tin(n + 1), tout(n + 1), order(n + 1), answer(n + 1) {}

    // 对 u 子树做一次 DFS 序展平，计算 parent、子树大小和最大子树的重儿子；返回 subtreeSize[u]。
    // p 是 u 的父节点，根调用时 p=0；写入内部预处理数组，不改变输入树。
    int prepare(int u, int p) {
        parent[u] = p;
        subtreeSize[u] = 1;
        tin[u] = ++timer;
        order[timer] = u;
        int largest = 0;
        for (int v : tree[u]) {
            if (v == p) continue;
            int childSize = prepare(v, u);
            subtreeSize[u] += childSize;
            if (childSize > largest) {
                largest = childSize;
                heavy[u] = v;
            }
        }
        tout[u] = timer;
        return subtreeSize[u];
    }

    // 无参数；重新以 root 为根建立 DFS 序区间、父节点、子树大小和重儿子信息；清空旧预处理数组，不修改输入树。
    // 仅完成结构预处理；颜色频次要由 solve() 初始化后才能用于 dfs() 统计。
    void build() {
        timer = 0;
        fill(parent.begin(), parent.end(), 0);
        fill(subtreeSize.begin(), subtreeSize.end(), 0);
        fill(heavy.begin(), heavy.end(), 0);
        fill(tin.begin(), tin.end(), 0);
        fill(tout.begin(), tout.end(), 0);
        prepare(root, 0);
    }

    // 将节点 x 的颜色频次增加 delta（+1 或 -1）；更新 distinct，保持频次非负。
    // x 是 1..n 点号；只修改内部 frequency/distinct。
    void changeColor(int x, int delta) {
        int id = compressed[x];
        if (frequency[id] == 0 && delta == 1) ++distinct;
        frequency[id] += delta;
        if (frequency[id] == 0 && delta == -1) --distinct;
    }

    // 将以 u 为根的整棵子树加入当前频次表或移除；add=true 表示加入。
    // u 必须已由 prepare 建立 DFS 区间；只修改内部频次状态。
    void addSubtree(int u, bool add) {
        int delta = add ? 1 : -1;
        for (int i = tin[u]; i <= tout[u]; ++i) changeColor(order[i], delta);
    }

    // 处理 u 子树；keep=true 时保留该子树颜色频次供父层合并，false 时清空。
    // p 为父节点；结束时 answer[u] 是子树 distinct 数，频次表依 keep 决定是否保留。
    void dfs(int u, int p, bool keep) {
        for (int v : tree[u]) {
            if (v != p && v != heavy[u]) dfs(v, u, false);
        }
        if (heavy[u] != 0) dfs(heavy[u], u, true);
        for (int v : tree[u]) {
            if (v != p && v != heavy[u]) addSubtree(v, true);
        }
        changeColor(u, 1);
        answer[u] = distinct;
        if (!keep) addSubtree(u, false);
    }

    // 重新预处理并计算所有子树答案；每次调用都会清空并重建结果，允许安全重复调用。
    // 返回 n+1 长度数组，answer[0] 不使用；不修改输入 tree/color。
    vector<int> solve() {
        build();
        fill(answer.begin(), answer.end(), 0);

        vector<int> values(color.begin() + 1, color.begin() + n + 1);
        sort(values.begin(), values.end());
        values.erase(unique(values.begin(), values.end()), values.end());
        for (int u = 1; u <= n; ++u) {
            compressed[u] = lower_bound(values.begin(), values.end(), color[u]) - values.begin();
        }
        frequency.assign(values.size(), 0);
        distinct = 0;
        dfs(root, 0, true);
        return answer;
    }
};

// 示例：tree 为 1-based 无向邻接表，color[1..n] 可使用任意整数；答案按点号读取。
// DSUOnTree solver(tree, color, 1); vector<int> distinct = solver.solve();
```

下面片段可放入业务函数。注意输入数组的生命周期要覆盖 `solver.solve()`：

```text
vector<vector<int>> tree(6);
// u/v 为 1..5 的树点；向捕获的 tree 双向加边，返回 void。
auto addEdge = [&](int u, int v) {
    tree[u].push_back(v);
    tree[v].push_back(u);
};
addEdge(1, 2); addEdge(1, 3);
addEdge(2, 4); addEdge(2, 5);
vector<int> color = {0, 3, 3, 5, 5, 3};
DSUOnTree solver(tree, color, 1);
vector<int> answer = solver.solve();
// answer 为 {0, 2, 2, 1, 1, 1}，0 号位不使用
```

**5. 要改哪里**

| 需求 | 改动 |
|---|---|
| 换成颜色次数、众数等统计 | 改 `changeColor` 的状态维护与 `answer[u]` 的读取方式；不同颜色数的加减规则不能直接当作众数维护。 |
| 按深度或权值统计 | 将统计键改为深度或权值，调整离散化和桶/树的容量；DFS 序仍只负责枚举节点。 |
| 换成线段树维护频次 | 在节点增删时更新对应统计键的叶子，重算单次增删和读答案的代价；不把总时间一律写成 $O(n\log n)$。 |
| 换根或多组数据 | 为新根/新数据构造对象后运行 `solve()`；同一输入上重复 `solve()` 也会完整清空并重算。 |
| 维护子树内部边权 | 可将边放在较深端点上，但对 `u` 子树应排除连接 `u` 与父亲的那条边；不能把原点权统计原样套过去。 |
| 深链数据 | 递归深度可达 `n`；栈不足时需将预处理和统计遍历改为显式栈。 |

**6. 自检**

用上述五点树检查 `order[tin[u]]==u`、`tout[u]-tin[u]+1==subtreeSize[u]`，以及 `heavy[u]` 是否为最大子树的孩子。答案应为 `[2,2,1,1,1]`；若所有颜色相同则每个答案都为 1，若各节点颜色不同则 `answer[u]==subtreeSize[u]`。单点树答案为 1；负颜色、大颜色经压缩后仍应满足这些规律。连续调用两次 `solve()`，结果必须相同。

调试时在 `dfs` 的 `keep=false` 分支结束后，检查本次子树贡献已清除；按此框架调用时应回到空频次状态，`distinct==0`。保留分支返回时，频次则恰好描述该子树。不要在重儿子返回后把全局频次清零。

**7. 坑**

- 子树统计像用了别的节点：把 DFS 位置当成节点号；必须通过 `order[i]` 映回节点，再查 `compressed`。
- 兄弟子树的答案偏大：轻子树处理后未完整删除；检查 `keep=false` 分支及所有统计变量的清理规则。
- 重子树频次翻倍：保留后又加入了一次；父层只重新枚举轻子树。
- 颜色越界：直接用原始负颜色或大颜色作桶下标；使用离散化编号。
- 改统计量后清空出错：新的状态未必能仅靠减频次还原；增删和清空必须成套设计，不能只替换取答案的一行。

**8. 一句话原理**

保留最大子树的状态，只重扫轻子树；沿轻边子树大小至少减半，因此每个节点只被反复加入、删除 $O(\log n)$ 次。

## 5.15 单点修改线段树与自定义合并 {#point-segment-tree-custom-merge}

**1. 它是做什么的**

这棵迭代线段树维护固定长度的非空 1-based 序列，支持单点替换和闭区间聚合。合并器 `merge` 必须满足结合律，并有左右两侧都成立的单位元 `identity`；合并器还必须能在 `rangeQuery` 的 `const` 函数中调用。构造时间为 $O(n)$，单点修改和区间查询各需 $O(\log n)$ 次合并，空间为 $O(n)$；这里按摘要的复制、存储和一次 `merge` 均为 $O(1)$ 计；若摘要或合并本身更昂贵，需乘上对应代价。它不支持非结合操作，也没有懒标记，不能直接执行区间更新。

示例用仿射函数 `f(x)=ax+b (mod MOD)` 作摘要。区间元素按下标从左到右依次作用，所以合并 `[left,right]` 时结果是 `right ∘ left`。模板保留查询区间的原始顺序，因而也能处理这种不满足交换律的合并。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `n` | 序列元素个数；输入的有效元素位于 `initial[1..n]`。 |
| `tree` | 长度 `2*n` 的紧凑迭代树；叶子 `tree[n+i-1]` 对应原位置 `i`，内部节点合并左右孩子的摘要；非二次幂长度时，部分内部节点不对应原数组上的连续区间。 |
| `identity` | `merge` 的双侧单位元，用于查询左右累积器的初值；示例中为恒等仿射函数。 |
| `merge` | 用户提供的结合合并操作；参数顺序有意义，必须可在常量查询中调用。 |
| `leftResult`, `rightResult` | 查询期间分别从区间左侧和右侧累积摘要，最后按 `leftResult` 在前、`rightResult` 在后的次序合并。 |
| `Affine{a,b}` | 仿射摘要，表示模 `MOD` 下的函数 `a*x+b`，系数存为 `[0,MOD)`。 |

输入及查询端点都是 1-based 闭区间；`rangeQuery(l,r)` 要求 `1 <= l <= r <= n`。非二次幂长度时，紧凑树的 `tree[1]` 不一定代表原序列整体，需用 `rangeQuery(1,n)` 查询整段。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `PointSegmentTree(initial, identity, merge)` | 复制 `initial[1..n]`，建立树；`initial` 必须非空且为 1-based，构造器用 `assert` 检查 `n>=1`。单位元和合并器需匹配且满足结合律。 |
| `pointSet(pos,value)` | 把位置 `pos` 替换为 `value`，重算叶子到根的摘要；要求 `1<=pos<=n`，无返回值。 |
| `rangeQuery(l,r)` | 返回闭区间 `[l,r]` 按原下标次序合并的摘要；要求合法非空区间，不修改树。 |
| `normalizeMod(x)` | 将任意 `long long` 规范到 `[0,MOD)`。 |
| `ComposeAffine::operator()(left,right)` | 返回先执行 `left` 再执行 `right` 的 `right∘left`；两输入系数应已规范化。 |
| `makeAffine(a,b)` | 建立 `a*x+b`，并将系数规范到 `[0,MOD)`。 |
| `affineExample()` | 演示初始化、点替换、区间查询和代入；返回最终模值。 |

**4. 怎么调用**

准备 1-based 的初始摘要、符合代数条件的合并器和单位元，构造后调用 `pointSet` / `rangeQuery`。示例中点 2 被替换为 `7x+2`，区间组合为 `70x+51`；代入 `x=11` 得到 `821`：

```text
ll result = affineExample();
// result == 821
```

模板代码如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

template<class T, class Merge>
struct PointSegmentTree {
    int n;
    T identity;
    Merge merge;
    vector<T> tree;

    // initial 为 1-based 非空序列，identity 是 merge 的双侧单位元，merge 满足结合律；复制到内部树并建树，不修改入参。
    explicit PointSegmentTree(const vector<T>& initial, T identity, Merge merge)
        : n((int)initial.size() - 1), identity(identity), merge(merge), tree(2 * n, identity) {
        assert(n >= 1);
        for (int i = 1; i <= n; ++i) tree[n + i - 1] = initial[i];
        for (int i = n - 1; i >= 1; --i) tree[i] = this->merge(tree[i << 1], tree[i << 1 | 1]);
    }

    // pos 为 1..n 的位置，value 是替换后的元素；返回 void，更新叶子及其祖先摘要，不改其他位置。
    void pointSet(int pos, const T& value) {
        int p = n + pos - 1;
        tree[p] = value;
        while (p > 1) {
            p >>= 1;
            tree[p] = merge(tree[p << 1], tree[p << 1 | 1]);
        }
    }

    // l、r 为 1-based 闭区间且 1<=l<=r<=n；返回按原序聚合的摘要，不修改树。
    T rangeQuery(int l, int r) const {
        int left = l + n - 1, right = r + n;
        T leftResult = identity, rightResult = identity;
        while (left < right) {
            if (left & 1) leftResult = merge(leftResult, tree[left++]);
            if (right & 1) rightResult = merge(tree[--right], rightResult);
            left >>= 1;
            right >>= 1;
        }
        return merge(leftResult, rightResult);
    }
};

constexpr ll MOD = 1000000007;

// x 为任意 long long；返回模 MOD 的 [0,MOD) 代表元。
ll normalizeMod(ll x) {
    x %= MOD;
    if (x < 0) x += MOD;
    return x;
}

struct Affine {
    ll a, b;
};

struct ComposeAffine {
    // left、right 的系数均已归一化；返回先执行 left 再执行 right 的复合 right∘left。
    Affine operator()(const Affine& left, const Affine& right) const {
        return {right.a * left.a % MOD,
                (right.a * left.b + right.b) % MOD};
    }
};

// 原始系数可为任意 long long；返回系数归一化后的 f(x)=ax+b。
Affine makeAffine(ll a, ll b) {
    return {normalizeMod(a), normalizeMod(b)};
}

// 示范仿射函数的顺序组合与点替换；仅修改本地线段树，返回区间函数作用于 x 的结果。
ll affineExample() {
    vector<Affine> functions(4);
    functions[1] = makeAffine(2, 1);
    functions[2] = makeAffine(3, 4);
    functions[3] = makeAffine(5, 6);
    PointSegmentTree<Affine, ComposeAffine> st(functions, makeAffine(1, 0), ComposeAffine{});
    st.pointSet(2, makeAffine(7, 2));
    Affine combined = st.rangeQuery(1, 3);
    ll x = normalizeMod(11);
    return (combined.a * x + combined.b) % MOD;
}
```

**5. 要改哪里**

- 维护区间和、最大值等摘要时，替换 `T`、`identity` 和 `merge`，并确保 `merge` 结合、`identity` 左右两侧均为单位元。最小值的单位元须不小于所有可能输入的值（如该类型的最大值），不能随意取 0。
- 维护非交换摘要时，严格保留“左段在前、右段在后”的合并顺序；不要交换 `merge(left,right)` 参数，也不要只用一个累积器改写查询。
- 仿射函数的作用顺序若改为从右向左，应同步重定义合并器和示例的区间语义，不能只交换说明。
- 增加区间修改需要引入懒标记及其与摘要的作用规则，当前模板没有这部分能力，应按操作重新设计。

**6. 自检**

示例的三项初值是 `2x+1`、`3x+4`、`5x+6`；将第二项替换为 `7x+2` 后，按顺序复合得到 `5(7(2x+1)+2)+6 = 70x+51`，代入 11 为 821。可分别检查单点区间、全区间和修改后查询；再用非二次幂长度（如 `n=3`）核对 `rangeQuery(1,n)`，不要把 `tree[1]` 当成全序列结果。

**7. 坑**

- 部分区间结果顺序反了：非交换合并时，右侧累积器必须用新块放在已有结果左侧；本模板通过 `merge(tree[--right], rightResult)` 保持顺序。
- 更新后结果异常：合并规则不满足结合律或单位元不匹配，线段树分组将改变结果。
- 整段查询拿错：`n` 非二次幂时 `tree[1]` 不是原序列整体摘要；使用 `rangeQuery(1,n)`。
- 下标越界或访问空叶子：接口按 1-based 编号且要求非空序列；构造输入的 `initial[0]` 不使用，查询端点须合法。

**8. 一句话原理**

每个节点保存其左段再接右段的摘要，单点替换后沿祖先重算，查询时按原序合并覆盖区间的节点。
