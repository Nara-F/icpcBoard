
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

先看复杂度从哪里来：若沿树路径逐点向父亲走，最坏要访问 $O(n)$ 个点；DFS 序只能把子树展平，不能让任意路径成为单段。HLD 选最大子树孩子为重儿子，第二次 DFS 优先走它，使重链连续。沿路径向上跨一条轻边时，父点的子树规模至少是轻儿子子树规模的两倍；反向从父点走向轻儿子时，子树规模至少减半。因此每条根到点路径经过 $O(\log n)$ 条轻边，任意两点路径也只跨 $O(\log n)$ 条重链。

小例子：边为 `1-2,1-3,3-4,3-5`，以 1 为根，3 是 1 的重儿子，2 是轻儿子；若 4 被选为 3 的重儿子，重链为 `1-3-4`。查询 2 到 5 会得到覆盖点 2、1、3、5 的若干闭区间。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `g[u]` | 无向邻接表；通过 `addEdge` 加边，所有边必须在 `build` 前加入。 |
| `parent[u]`, `depth[u]` | 以指定根定根后的父节点和深度，根深度为默认初值 0。 |
| `sz[u]` | 以 `u` 为根的子树大小。 |
| `heavy[u]` | `u` 的最大子树孩子；无孩子时为 `-1`。 |
| `top[u]` | `u` 所在重链的链头。 |
| `pos[u]` | 剖分后的 1-based 连续位置；同一重链连续，子树也对应连续区间。 |
| `timer` | 分配 `pos` 时递增的全局位置计数器；对象构造时为 0，`build` 会重置。 |

点编号和剖分位置是两个不同维度：路径区间传给维护结构时使用 `pos`，建树时遍历点编号，令 `base[pos[u]]=weight[u]` 即可，不需要逆映射；若要从位置取回点编号，再另建 `vertexAt[pos[u]]=u`。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `HLD(nodeCount)` | 分配 `1..nodeCount` 的邻接表和数组；点数应为正。 |
| `addEdge(u,v)` | 要求两个合法不同点；向邻接表双向加入一条边，须在 `build` 前且每条边只加一次。 |
| `dfs1(u,p)` | 内部递归，设置父亲、深度、子树大小及重儿子，返回子树大小；在合法树上由 `build` 调用。 |
| `dfs2(u,head)` | 内部递归，设置链头和位置，并优先遍历重儿子；无返回值。 |
| `build(root)` | 完成剖分；要求所有边已加入，`root` 在 `1..n`。会清空旧剖分数组并重建，要求输入仍为连通树；可重复调用或更换根。省略参数时根为 1。 |
| `forPath(u,v,use)` | 将路径拆成闭区间并逐段调用 `use(l,r)`；回调返回值被忽略，需通过捕获外部对象实现查询或更新。区间参数是剖分位置，次序不承诺对应原路径方向。 |

**4. 怎么调用**

用 `addEdge` 加完边，再调用 `build`；随后让 `forPath` 的回调把区间交给线段树。下例为链 `1-2-3`，路径查询得到的位置区间 `[1,3]`：

```text
HLD hld(3);
hld.addEdge(1, 2);
hld.addEdge(2, 3);
hld.build();
// l/r 为剖分位置闭区间；回调输出端点，不修改 hld。
hld.forPath(1, 3, [&](int l, int r) { cout << l << " " << r << "\n"; });
// 输出：1 3
```

模板代码如下：

```cpp

struct HLD {
    // heavy 子树最大者优先同链；任意树路径被拆成 O(log n) 个连续区间。
    int n, timer = 0;
    vector<vector<int>> g;
    vector<int> parent,depth,sz,heavy,top,pos;
    // nodeCount 为点数（须 >=1）；分配 1-based 邻接表和剖分数组，不修改调用方点权。
    explicit HLD(int nodeCount)
        : n(nodeCount), g(nodeCount + 1), parent(nodeCount + 1),
          depth(nodeCount + 1), sz(nodeCount + 1),
          heavy(nodeCount + 1, -1), top(nodeCount + 1), pos(nodeCount + 1) {
        assert(n >= 1);
    }
    // u、v 为 1..n 的树点；返回 void，向 g 双向加入一条边；必须在 build 前且每条边只加一次。
    void addEdge(int u, int v) {
        assert(1 <= u && u <= n && 1 <= v && v <= n && u != v);
        g[u].push_back(v);
        g[v].push_back(u);
    }
    // u 为当前子树根、p 为父点；返回子树大小，并写 parent/depth/sz/heavy；输入必须是树。
    int dfs1(int u, int p) {
        parent[u] = p;
        sz[u] = 1;
        heavy[u] = -1;
        int best = 0;
        for (int v : g[u]) {
            if (v == p) continue;
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
    // u 为子树根、head 为其链头；返回 void，按重儿子优先写 top/pos 并递增 timer。
    void dfs2(int u, int head) {
        top[u] = head;
        pos[u] = ++timer;
        if (heavy[u] != -1) dfs2(heavy[u], head);
        for (int v : g[u]) {
            if (v != parent[u] && v != heavy[u]) dfs2(v, v);
        }
    }
    // root 为 1..n 的定根；返回 void，清空旧剖分并重建所有数组；要求 g 是连通树。
    void build(int root = 1) {
        assert(1 <= root && root <= n);
        timer = 0;
        fill(parent.begin(), parent.end(), 0);
        fill(depth.begin(), depth.end(), 0);
        fill(sz.begin(), sz.end(), 0);
        fill(heavy.begin(), heavy.end(), -1);
        fill(top.begin(), top.end(), 0);
        fill(pos.begin(), pos.end(), 0);
        dfs1(root, 0);
        dfs2(root, root);
        assert(timer == n);
    }
    // u/v 为已 build 的树端点；use(l,r) 接收 1-based 闭区间且返回值被忽略；区间方向不保证，返回 void。
    template<class F>
    void forPath(int u, int v, F use) const {
        assert(1 <= u && u <= n && 1 <= v && v <= n);
        while (top[u] != top[v]) {
            if (depth[top[u]] < depth[top[v]]) swap(u, v);
            use(pos[top[u]], pos[u]);
            u = parent[top[u]];
        }
        if (depth[u] > depth[v]) swap(u, v);
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
- 多测或更换根：边加入后可再次调用 `build(root)`；它会清空并重建剖分数组。外部线段树也须按新 `pos` 重排。

区分模型：路径加、路径和或路径最值通常使用 HLD 加线段树；只有子树操作时 DFS 序更简单。路径上的字符串拼接、矩阵乘法等不可交换操作，需要记录每段方向并按原路径顺序合并，当前 `forPath` 不提供方向。

**6. 自检**

在链 `1-2-3` 上构建后，`forPath(1,3,...)` 应只回调一次，区间为 `[1,3]`；`forPath(2,2,...)` 应得到单点区间。再用树 `1-2, 1-3` 测 `forPath(2,3,...)`，回调区间覆盖点 2、1、3 对应的位置，不能遗漏 LCA。边权版本还要确认同链查询排除了 LCA 的位置。

**7. 坑**

- 结果像用了旧树：在加完边之前调用了 `build`；先完整建图再剖分。
- 深链上递归深度可达 $n$，栈不足时需将两次 DFS 改为显式栈。
- 重建后外部权值看似错乱：`build` 会改变 `pos`，需按新位置重建外部维护结构。
- 路径和/最值适用、路径拼接错误：回调区间顺序不保证路径方向；方向敏感操作需同时维护区间方向和两端的合并顺序。
- 边权答案多一条或少一条：最终同链段包含 LCA；将该段左端改为 `pos[LCA]+1`。

**8. 一句话原理**

最大子树孩子优先进入同一条链；每次跨轻边时子树规模至少减半，所以任一路径只跨 $O(\log n)$ 条链，每条链映射成连续区间。

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

朴素地为每个点单独 DFS 其子树，一条链会扫描 $n+(n-1)+\cdots=O(n^2)$ 个节点；仅把子树展平为区间并不能消除重复扫描。DSU on Tree 的关键是保留最大子树的统计表，轻子树算完答案后清空，稍后再作为轻子树重新加入。每条轻边都会让子树规模至少翻倍，因此每个节点最多重新加入 $O(\log n)$ 次。 DSU on Tree 负责安排哪些节点加入或移出当前集合，桶、树状数组或线段树负责维护集合里的统计。本模板用颜色频次桶统计不同颜色数。它与普通并查集不同：这里没有合并集合代表元的操作，保留的是重儿子已经算好的频次状态。适合离线回答固定根下的子树统计，不直接支持在线改色、动态换根或路径查询。

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

扩展到子树众数时，需同步改变加入、删除和答案读取。若只要求最高频率，可维护 `frequency[color]`、`countAtFrequency[f]` 和 `bestFrequency`：加入时更新频率桶并可能提高最大频率，删除时减少桶计数并在最高频率桶为空时向下移动。`keep=false` 仍须逐节点撤销。若还要并列时最小颜色，可对每个频率维护有序集合，操作增加 $O(\log n)$ 因子。只求最高频率时频率桶可均摊 $O(1)$。众数扩展不适用于在线改色或路径众数。

模型识别：静态树、每个点都要回答一个子树统计，且统计可以由频率表增删维护时考虑 DSU on Tree；少数子树区间查询可考虑 DFS 序加离线树状数组，在线修改则考虑动态结构。


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

## 5.16 启发式合并（Small-to-Large） {#small-to-large}

**1. 它是做什么的**

输入是一棵静态、连通、1-based 有根树，每个点有一个可插入集合元素的颜色；更一般地，两个子问题的摘要可以逐元素合并。 对每个点输出其子树颜色集合的大小；模板实际只保存答案，集合所有权在递归返回时转移。 构造器输入 `tree[1..n]`、`color[1..n]` 和根 `root`；`solve()` 输出 `answer[1..n]`，下标 0 不使用，允许重复调用且不修改输入。 复杂度：本实现按子树节点数（质量）选择容器；若集合插入为 $O(\log n)$，总时间 $O(n\log^2 n)$、空间 $O(n)$；若哈希集合期望 $O(1)$ 插入，总时间期望 $O(n\log n)$。

“小集合并入大集合”是一个通用的摊还技巧，不是某一种容器。朴素地把子树 `v` 的所有元素复制到 `u`，链状树会产生 $O(n^2)$ 次插入。这里不能把“不同颜色数”直接当作翻倍依据：例如 `{1,2}` 并 `{1,2,3}` 后只有一个新颜色。模板为每个返回的集合同时记录子树节点数 `mass`，按 `mass` 选较小的一侧；一次合并的扫描项数不超过质量较小侧的节点数。对每个原始节点项收费：若它的颜色已在大侧，项在这次扫描后消失，只收费这一次；若颜色保留为代表，它下一次随集合被搬运时，接收子树质量至少相对其所属子问题翻倍。因此每个原始项最多被收费 $O(\log n)$ 次，重复颜色不会被错误地用“集合大小翻倍”来证明。代码必须按质量比较，不能只按儿子编号或 DFS 顺序合并。

看到“合并若干子树集合、查询不同元素/频次/集合摘要”，先问摘要是否支持逐元素插入和合并。如果摘要只能整体合并（例如某些复杂 DP），就不能直接套本节。DSU on Tree 通过清空临时表回答许多子树询问；启发式合并把每个递归结果的集合所有权转给父节点，孩子容器在合并后销毁，只在 `answer` 中保留孩子结果。线段树合并则把“元素”换成值域线段树节点，适合值域统计和第 k 小。

下例返回每个点子树的不同颜色数。`set` 保证元素唯一但单次插入为 $O(\log n)$；要换成期望更快的 `unordered_set`，应同时处理哈希退化风险。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `Bag::values` | 当前子树的颜色集合，使用 `set<int>` 去重；所有权由 `unique_ptr` 独占。 |
| `Bag::mass` | 当前子树包含的节点数，用于选定较小容器；不能用不同颜色数替代。 |
| `n`, `root` | 输入树点数与固定根；点号为 `1..n`。 |
| `tree`, `color` | 输入树及颜色的常量引用；必须比对象活得更久。 |
| `answer[u]` | 根为 `u` 的子树不同颜色数；0 号位不用。 |

**3. 函数在做什么**

| 函数 | 参数、返回与副作用 |
|---|---|
| `SmallToLargeDistinct(tree,color,root)` | 接收 1-based 连通无向树、`color[1..n]` 与合法根；保存输入引用并分配答案，不改输入。 |
| `dfs(u,p)` | `u` 为当前子树根、`p` 为父点；返回含集合所有权和节点质量的 `Bag`，写入 `answer[u]`。仅供递归内部使用。 |
| `solve()` | 无参数；重置答案并从 `root` 计算；返回长度 `n+1` 的答案向量，可重复调用。 |

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SmallToLargeDistinct {
    struct Bag {
        unique_ptr<set<int>> values;
        int mass = 0; // 对应子树节点数，用于严谨的小并大选择
    };
    int n, root;
    const vector<vector<int>>& tree;
    const vector<int>& color;
    vector<int> answer;

    // tree/color 为 1-based 连通无向树和颜色；root 在 1..n；只保存引用，调用期间入参须保持有效。
    SmallToLargeDistinct(const vector<vector<int>>& tree,
                         const vector<int>& color, int root)
        : n((int)tree.size() - 1), root(root), tree(tree), color(color),
          answer(n + 1) {
        assert(n >= 1 && 1 <= root && root <= n);
    }

    // 在 u 的子树建立集合；p 是父点；返回集合所有权及子树质量，并写 answer[u]。
    Bag dfs(int u, int p) {
        Bag current{make_unique<set<int>>(), 1};
        current.values->insert(color[u]);
        for (int v : tree[u]) if (v != p) {
            Bag other = dfs(v, u);
            // 质量而非不同颜色数决定小侧；这样重复颜色也有明确的摊还收费。
            if (current.mass < other.mass) swap(current, other);
            current.values->insert(other.values->begin(), other.values->end());
            current.mass += other.mass;
        }
        answer[u] = (int)current.values->size();
        return current;
    }

    // 重新计算所有子树不同颜色数；返回下标 1..n 的答案，允许重复调用且不改输入。
    vector<int> solve() {
        fill(answer.begin(), answer.end(), 0);
        Bag result = dfs(root, 0);
        (void)result; // 根集合所有权在本次调用结束时释放，只保留 answer。
        return answer;
    }
};
```

最小完整调用示例，树为 `1-2,1-3`，颜色为 `[5,5,8]`：

```text
vector<vector<int>> tree(4);
tree[1] = {2, 3}; tree[2] = {1}; tree[3] = {1};
vector<int> color = {0, 5, 5, 8};
SmallToLargeDistinct solver(tree, color, 1);
auto answer = solver.solve();
assert(answer[1] == 2 && answer[2] == 1 && answer[3] == 1);
```

**5. 要改哪里**

先确认摘要支持逐元素插入，且能定义重复元素规则；只支持整体合并的 DP 摘要不能套此模板。练习顺序：先统计不同颜色；再以 `unordered_map<颜色,频次>` 求子树众数；最后替换成自定义可插入摘要，并证明元素搬运次数。与 DSU on Tree 相比，本法把子树集合所有权交给父节点，孩子集合被消费；与线段树合并相比，本法逐元素插入，不保留值域分布结构。

**6. 自检**

手算两个子树质量分别为 2 和 7，且各有两个不同颜色：质量 2 的容器应并入质量 7 的容器，合并后 `mass=9`，答案按集合去重结果计算。重复调用 `solve()` 应得到相同答案。

**7. 坑**

不要按不同颜色数而非 `mass` 选小侧；重复颜色会破坏翻倍证明。交换 `Bag` 后继续使用新的 `current` 所有权，不能再访问已转移的容器。递归必须以父节点过滤邻接边；输入有环时会无限递归。`set` 插入为 $O(\log n)$，换哈希容器后复杂度是期望界且需考虑退化风险。

**8. 一句话原理**

始终把较小质量侧逐项加入较大侧，使仍存活的元素每次搬运后面对的子树质量至少翻倍。

## 5.17 线段树合并（Segment Tree Merge） {#segment-tree-merge}

**1. 它是做什么的**

多棵互不共享节点、覆盖相同离散值域 $[lo,hi]$ 的动态线段树，要求合并值域频次、求第 k 小或继续修改；常见于树上每个子树的权值集合。 复用相同值域的空节点，把两棵动态开点线段树合成一棵。 `add(root,pos,delta)` 输入合法根编号、值域内位置和使所有频次非负的 `delta`，输出更新后的根；`merge(a,b)` 输入同一节点池、同一值域且节点集合完全不相交的两棵树（允许空根 0），输出合并后的唯一有效根；两个旧集合均被消费，不能再作为独立集合读取、修改或参与合并。不同根编号本身不足以保证不共享节点；非空时 `merge(a,a)` 非法。根编号是 `vector` 的 `int` 下标，`sum` 和计数必须不超过 `INT_MAX`。 复杂度：`add` 为 $O(\log\sigma)$；一次破坏性合并访问第二棵树的非空节点及重叠分支。设总共创建 $P$ 个节点、外部调用合并 $M$ 次，则这批合并的总成本为 $O(P+M)$：每次两个非空节点相遇都会让第二个节点退出独立可用的森林，它不能再次被消费；空节点返回的次数至多为这些递归分叉数的常数倍再加 $M$。典型每个点先建立一条值域路径，再沿原树合并 $n-1$ 次，创建与合并共 $O(n\log(\sigma+1))$。空间为已创建节点数。

**先理解值域线段树。** 普通线段树的叶子常是数组位置；这里的叶子是“某个值”，叶子存这个值出现了几次。比如值域 `[1,8]` 中只有值 3 出现一次，只需创建 `[1,8]→[1,4]→[3,4]→[3,3]` 的四个节点，其余分支用编号 0 表示。这叫动态开点：需要哪条路径才创建哪些节点。`root` 是节点池下标，不是原树的点号，多个集合各自持有一个根。

它和启发式合并的区别是：这里不搬运每个值，直接按值域递归。每个节点保存区间内出现次数；两个根相加，左儿子和左儿子合并，右儿子同理。零根 `0` 表示空树，因此可以把一棵空树直接返回。值域必须固定且两个根的 `[lo,hi]` 相同；因为节点不共享，递归才能把被消费的第二棵树节点计入一次。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `lo`, `hi` | 所有集合共享的闭值域；中点计算要求 `hi-lo` 不溢出 `int`。 |
| `tr` | 动态节点池；下标是节点编号，`tr[0]` 是全零空节点。 |
| `Node::left/right` | 当前值域区间左右半边的根编号；0 表示该侧为空。 |
| `Node::sum` | 当前区间的总频次；必须非负且不超过 `INT_MAX`。 |

**3. 函数在做什么**

| 函数 | 参数、返回与副作用 |
|---|---|
| `SegmentTreeMerge(lo,hi,reserveNodes)` | 建立本节点池和空根 0；要求 `lo<=hi`，预留容量只影响扩容。 |
| `add(root,pos,delta)` | 在本池根表示的频次中将 `pos` 加 `delta`；返回更新根并修改节点池，要求位置合法且频次不变负。 |
| `merge(a,b)` | 合并两根并返回唯一有效根；原集合被消费，要求相同节点池/值域且节点集合不共享。 |
| `count(root,pos)` | 返回值 `pos` 的频次；不修改节点池，空根返回 0。 |
| `kth(root,k)` | 返回根所表示多重集合的第 `k` 小值，`k` 从 1 起；非法根或排名触发断言。 |

根编号必须来自当前对象，并满足 `0 <= root < tr.size()`；0 表示空树。接口不会全面检查根编号，`merge` 的两个根还必须满足不共享节点的所有权前提。

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SegmentTreeMerge {
    struct Node { int left = 0, right = 0, sum = 0; };
    int lo, hi;
    vector<Node> tr;

    // lo/hi 是所有权值的闭区间；节点 0 为空；预留容量仅影响常数，不改变结果。
    SegmentTreeMerge(int lo, int hi, int reserveNodes = 0)
        : lo(lo), hi(hi) {
        assert(lo <= hi);
        tr.reserve(max(1, reserveNodes));
        tr.push_back(Node{});
    }

    // 在 root 表示的树中把位置 pos 的计数增加 delta；返回新根，要求 pos 在值域内且计数不变为负。
    int add(int root, int l, int r, int pos, int delta) {
        if (!root) { root = (int)tr.size(); tr.push_back(Node{}); }
        tr[root].sum += delta;
        assert(tr[root].sum >= 0);
        if (l == r) return root;
        int m = l + (r - l) / 2;
        if (pos <= m) tr[root].left = add(tr[root].left, l, m, pos, delta);
        else tr[root].right = add(tr[root].right, m + 1, r, pos, delta);
        return root;
    }

    // pos 为 lo..hi 的值；返回更新后的根，原 root 可为 0；只修改内部节点池。
    int add(int root, int pos, int delta = 1) {
        assert(lo <= pos && pos <= hi);
        return add(root, lo, hi, pos, delta);
    }

    // 破坏性合并根 a、b 的频次并返回结果根；a/b 可有一个为 0，非空时必须 a!=b 且两树节点不共享。
    int merge(int a, int b, int l, int r) {
        if (!a) return b;
        if (!b) return a;
        tr[a].sum += tr[b].sum;
        if (l != r) {
            int m = l + (r - l) / 2;
            tr[a].left = merge(tr[a].left, tr[b].left, l, m);
            tr[a].right = merge(tr[a].right, tr[b].right, m + 1, r);
        }
        return a;
    }

    // a、b 来自本池同一值域且节点完全不共享；返回唯一有效的合并根，旧集合不可再独立使用。
    int merge(int a, int b) {
        assert(a == 0 || b == 0 || a != b); // merge(a,a) 会重复累计，调用契约禁止它
        return merge(a, b, lo, hi);
    }

    // root 为当前频次树，pos 为值；返回该值的出现次数，root 可为 0。
    int count(int root, int l, int r, int pos) const {
        if (!root) return 0;
        if (l == r) return tr[root].sum;
        int m = l + (r - l) / 2;
        return pos <= m ? count(tr[root].left, l, m, pos)
                        : count(tr[root].right, m + 1, r, pos);
    }

    // root 为频次树、pos 为 lo..hi 的值；返回该值的出现次数，root 可为 0。
    int count(int root, int pos) const {
        assert(lo <= pos && pos <= hi);
        return count(root, lo, hi, pos);
    }

    // root 为频次树；k 从 1 开始；返回全局第 k 小值，k 非法时断言失败。
    int kth(int root, int l, int r, int k) const {
        assert(root && 1 <= k && k <= tr[root].sum);
        if (l == r) return l;
        int m = l + (r - l) / 2;
        int leftSum = tr[tr[root].left].sum;
        if (k <= leftSum) return kth(tr[root].left, l, m, k);
        return kth(tr[root].right, m + 1, r, k - leftSum);
    }

    // 返回根的第 k 小值；要求根非空且 1<=k<=总计数。
    int kth(int root, int k) const { return kth(root, lo, hi, k); }
};
```

最小调用示例，可直接放在 `main` 函数体内：合并 `{3}` 与 `{1,3}`，结果第 2 小为 3。

```text
SegmentTreeMerge st(1, 8);
int a = st.add(0, 3);
int b = st.add(0, 1);
b = st.add(b, 3);
int merged = st.merge(a, b);
assert(st.count(merged, 3) == 2);
assert(st.kth(merged, 1) == 1 && st.kth(merged, 2) == 3);
```

**5. 要改哪里**

树上后序合并时，先记录孩子答案，再将孩子根交给父亲并把孩子根置 0；该模板不为每棵子树保留版本。先离散化到紧凑值域；练习顺序：频次合并、每个子树第 k 小、再结合差分根或离线删除分析重叠节点。分裂操作需另行设计节点所有权。本结构与主席树不同：本结构破坏旧根并复用节点，主席树复制路径保留历史版本。

**6. 自检**

值域 `[1,8]`：A=`{3:1}`、B=`{1:1,3:1}`，合并后总频次应为 3，`kth(1)=1`、`kth(2)=3`、`count(3)=2`。若合并空根与非空根，结果应等于非空根。

**7. 坑**

两个根必须来自同一节点池和同一值域，且节点集合不得共享；非空 `merge(a,a)` 会重复累计。合并后第二棵树不可继续独立读取或修改。`sum`、总频次、节点池下标和 `hi-lo` 都受 `int` 范围限制；不要把总频次误当不同值个数。

**8. 一句话原理**

相同值域的对应节点频次相加，空分支直接复用另一侧节点；节点所有权随破坏性合并转移。

## 5.18 主席树（可持久化线段树） {#persistent-segment-tree}

**1. 它是做什么的**

静态数组区间第 k 小、前缀版本查询，以及树上路径第 k 小；值域可离散化为 $[1,\sigma]$。 每次单点加入只复制根到叶子的 $O(\log\sigma)$ 个节点，旧版本仍可查询。 `add(previous,pos,delta)` 输入合法旧版本根、值域内离散位置和合法增量，输出不破坏旧版本的新根；`kthRange` 输入两个前缀根及合法 1-based `k`，`kthPath` 输入四根及合法 `k`，均输出离散值编号。每个 `sum`、所有中间频次、节点池下标及 `hi-lo` 必须在 `int` 范围内；推荐离散化为 `[1,σ]`。 复杂度：建立 $n$ 个前缀版本为 $O(n\log\sigma)$ 时间和空间；一次区间/路径第 k 小为 $O(\log\sigma)$；空间不能低于所有版本复制出的节点数。

初学者可以把“主席”理解成“每个前缀都有一份几乎相同的频次表”。版本 `root[i]` 表示前 `i` 个元素；区间 `[l,r]` 的频次等于 `root[r] - root[l-1]`。递归向左时，左半段出现次数是两根左儿子的 `sum` 之差；若 `k` 不超过它就向左，否则减去左计数向右。每次只复制一条根到叶路径，所以不会真的复制整棵树。

数组小例子：`a=[2,1,3,2]` 时，`root[4]-root[1]` 表示区间 `[2,4]` 的频次 `{1:1,2:1,3:1}`，第 2 小是 2。树上例子中总根为 1，路径 `2-1-3` 的点权为 `[3,1,2]`，令 `w=1`，四根公式应得到这三个值，排序后的第 2 小为 2。

树上路径使用四根：令 `root[u]` 表示从总根到 `u`（含 `u`）的权值版本，`w=lca(u,v)`，则路径频次为
`root[u] + root[v] - root[w] - root[parent[w]]`。
不要把它只记成“公共前缀减一次”：根到 `u`、根到 `v` 让 LCA 以上的点被算两次，LCA 本身也被算两次；减去 `root[w]` 和 `root[parent[w]]` 后，LCA 以上的系数为 $2-1-1=0$，LCA 的系数为 $2-1=1$，路径中更深点只出现一次。因而四根在每个值域叶上的组合频次都应非负；若出现负数，通常是 LCA/父根或版本定义错了。`parent[root]=0` 且版本 0 为空，正好统一根的边界。向下递归时左计数使用四个左儿子和的同号组合，`k` 必须在总路径长度内。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `lo`, `hi` | 离散值编号的闭区间；建议取 `[1,σ]`。 |
| `tr` | 持久化节点池；节点下标是根编号，节点 0 表示空版本。 |
| `Node::left/right` | 值域左右半段的版本根。更新时只复制被访问路径上的节点。 |
| `Node::sum` | 当前值域区间的出现次数；路径四根组合得到的各区间频次应非负。 |
| `root[i]` | 由调用方维护的版本根；数组场景可代表前 i 个元素，树场景可代表根到点路径。 |

**3. 函数在做什么**

| 函数 | 参数、返回与副作用 |
|---|---|
| `PersistentSegmentTree(lo,hi,reserveNodes)` | 建立空版本 0；要求 `lo<=hi`，容量参数仅影响扩容。 |
| `add(previous,pos,delta)` | 从已有版本复制根到叶路径，在位置加 `delta`；返回新版本根，旧版本不变；位置合法且任一频次不得为负。 |
| `kthRange(rootR,rootBeforeL,k)` | 两根分别代表前缀 `[1..r]`、`[1..l-1]`；返回区间第 k 小的离散值，k 从 1 起。 |
| `kthPath(ru,rv,rlca,rparent,k)` | 按 `+ru+rv-rlca-rparent` 组合四根；返回树路径第 k 小离散值，父根可为 0。 |
| `kth4(...)` | 内部按四根组合计数递归；要求总路径/区间频次中 k 合法，返回离散编号。 |

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct PersistentSegmentTree {
    struct Node { int left = 0, right = 0, sum = 0; };
    int lo, hi;
    vector<Node> tr;

    // lo/hi 是离散值域闭区间；版本 0 为空；reserveNodes 只用于减少扩容。
    PersistentSegmentTree(int lo, int hi, int reserveNodes = 0) : lo(lo), hi(hi) {
        assert(lo <= hi);
        tr.reserve(max(1, reserveNodes));
        tr.push_back(Node{});
    }

    // 从 previous 版本在 pos 增加 delta；返回新版本根，旧版本不变，pos 必须在值域内。
    int add(int previous, int l, int r, int pos, int delta) {
        int now = (int)tr.size();
        tr.push_back(tr[previous]);
        tr[now].sum += delta;
        assert(tr[now].sum >= 0); // 合法 delta 不得让任一值域区间频次为负
        if (l == r) return now;
        int m = l + (r - l) / 2;
        if (pos <= m) tr[now].left = add(tr[previous].left, l, m, pos, delta);
        else tr[now].right = add(tr[previous].right, m + 1, r, pos, delta);
        return now;
    }

    // previous 是已有版本根；返回只比它多 delta 个 pos 的新根。
    int add(int previous, int pos, int delta = 1) {
        assert(0 <= previous && previous < (int)tr.size());
        assert(lo <= pos && pos <= hi);
        return add(previous, lo, hi, pos, delta);
    }

    // 四个版本根按 +rootU +rootV -rootLca -rootParentLca 组合；返回路径第 k 小的离散值。
    int kth4(int ru, int rv, int rlca, int rparent, int l, int r, int k) const {
        int total = tr[ru].sum + tr[rv].sum - tr[rlca].sum - tr[rparent].sum;
        assert(1 <= k && k <= total);
        if (l == r) return l;
        int m = l + (r - l) / 2;
        int leftCount = tr[tr[ru].left].sum + tr[tr[rv].left].sum
                      - tr[tr[rlca].left].sum - tr[tr[rparent].left].sum;
        if (k <= leftCount)
            return kth4(tr[ru].left, tr[rv].left, tr[rlca].left,
                        tr[rparent].left, l, m, k);
        return kth4(tr[ru].right, tr[rv].right, tr[rlca].right,
                    tr[rparent].right, m + 1, r, k - leftCount);
    }

    // 四根均为本对象版本根，k 从 1 开始；返回路径第 k 小值，父根为空时传 0。
    int kthPath(int ru, int rv, int rlca, int rparent, int k) const {
        return kth4(ru, rv, rlca, rparent, lo, hi, k);
    }

    // 两个前缀版本 rootR、rootBeforeL 表示 [1..r] 和 [1..l-1]；返回区间第 k 小值。
    int kthRange(int rootR, int rootBeforeL, int k) const {
        return kth4(rootR, 0, rootBeforeL, 0, lo, hi, k);
    }
};
```

最小调用示例，可直接放在 `main` 函数体内：数组 `[2,1,3]` 的整个区间第 2 小为 2。

```text
PersistentSegmentTree pst(1, 3);
int root0 = 0;
int root1 = pst.add(root0, 2);
int root2 = pst.add(root1, 1);
int root3 = pst.add(root2, 3);
assert(pst.kthRange(root3, root0, 2) == 2);
assert(pst.kthRange(root3, root1, 1) == 1); // 区间 [2,3]
```

**5. 要改哪里**

先排序去重并把原值映射到 `[1,σ]`，查询后再映射回来。树路径版本令 `root[u]` 表示总根到 u（含 u）的频次，再结合 LCA 和父根；四根公式中的 LCA 父根不能省略。练习顺序：静态数组区间第 k 小、接倍增 LCA 做树路径第 k 小、再估算前缀版本内存。若每次更新复制约 `ceil(log2(σ))+1` 个节点、节点有三个 int，`n=10^5` 且深度约 18 时节点池约 22 MB，另需根数组和容器容量。主席树不适合直接处理会改变大量值的区间更新。

**6. 自检**

数组 `[2,1,3,2]` 中 `root[4]-root[1]` 表示 `[2,4]` 的频次 `{1:1,2:1,3:1}`，第 2 小为 2。路径 `2-1-3` 点权 `[3,1,2]` 时，四根公式应计入这三个点各一次，第 2 小为 2。旧根查询结果在后续 `add` 后仍应不变。

**7. 坑**

漏减 `root[parent[lca]]` 会多算 LCA 以上点；将第 k 小写成第 k 大、忘记离散值映射、传入非法 k 或令 delta 制造负频次也会出错。`sum`、中间频次、节点池下标和 `hi-lo` 必须能放进 int；所有根必须来自同一对象且保持有效。

**8. 一句话原理**

路径复制保留旧版本；两个前缀版本或四个树路径版本的频次差组合后，在值域树上按左侧计数逐层定位第 k 小。

## 5.19 虚树 {#virtual-tree}

**1. 它是做什么的**

原树静态、同一棵树上有很多次询问，每次只关心一小组关键点以及它们之间的祖先关系。 把关键点和它们相邻关键点的 LCA 压缩成一棵边数为 $O(k)$ 的树；本模板输出虚树点集及有向父子边。 构造非空的 1-based 无权连通树并调用 `build(root)`，每次输入合法原树点号组成的关键点列表（允许重复）；返回 `vertices` 原点号列表、`edges` 中的 `(父点,子点,原树边数距离)` 和虚树根，空询问返回空列表及根 0。不改变原树。复杂度：预处理倍增 LCA 为 $O(n\log n)$；一次输入 $k$ 项关键点（允许重复）的询问为 $O(k\log k+k\log n)$：需要对相邻点求 LCA、加入至多 $k-1$ 个 LCA、再次排序并用栈建树。即使调用者已经把关键点按 DFS 序排序，本模板仍会求这些 LCA 并对补点后的 `all` 第二次排序；若另写接口复用排序结果，才可省去第一次排序。空间 $O(n\log n+k)$。

朴素地在原树上对每次询问跑 DFS，会扫描整棵 $n$ 点树，即使询问只给出 $k$ 个关键点。只保留关键点又可能断开祖先关系：两个关键点的路径中间的分叉祖先也会影响距离、染色、最小割等 DP。虚树补入相邻关键点的 LCA，恰好保留了这些分叉点，其他原树枝叶都可以忽略。

建树步骤是：按 `tin` 排序并去重关键点；对相邻点加入 LCA；再排序去重；用单调栈扫描，栈顶是当前 DFS 路径上最近的已保留祖先，弹出到它成为当前点的父亲。$k$ 个关键点只有 $k-1$ 对相邻点，因此至多加入 $k-1$ 个 LCA；合并去重后保留点数至多 $2k-1$，边数至多 $2k-2$。栈扫描本身是线性的，但整个询问不能因此写成线性。代码返回边权 `depth[child]-depth[parent]`，它表示原树路径长度，方便在虚树上做距离 DP。

虚树和 HLD 的分工不同：HLD 适合动态路径修改/查询；虚树适合“每次询问关键点很少、原树很大”的离线或在线多询问。它通常与 LCA、树上 DP、点权/边权最短距离组合，也可先对关键点做去重和祖先过滤。虚树 DP 的临时标记、度数和答案数组只应访问本次 `vertices` 中的至多 $2k-1$ 个点，询问结束后清空这些点，不能每次清空整棵原树。边界是关键点为空时返回空；只有一个关键点时虚树只有一个点、没有边。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `n`, `logn`, `timer` | 原树点数、倍增层数、DFS 进入计时器。 |
| `g[u]` | 原树无向邻接表；必须在 `build` 前完成。 |
| `tin[u]`, `tout[u]` | DFS 进入时间及子树区间末端；祖先判定使用同一轮 DFS 的两个时间。 |
| `depth[u]` | 相对预处理根的深度；虚树边权用深度差表示原树距离。 |
| `up[j][u]` | 节点 u 向上 `2^j` 步的祖先；0 表示越过根。 |
| `VirtualTreeResult::vertices` | 按 DFS 序排列的保留原树点。 |
| `VirtualTreeResult::edges` | `(父点,子点,原树距离)` 三元组；不是原树直接边。 |
| `VirtualTreeResult::root` | 虚树根；空询问时为 0。 |

**3. 函数在做什么**

| 函数 | 参数、返回与副作用 |
|---|---|
| `VirtualTree(nodeCount)` | 分配 `1..n` 图和 LCA 表；要求 `n>=1`。 |
| `addEdge(u,v)` | 接收合法不同点，双向加入原树边；必须在 `build` 前调用。 |
| `build(root)` | 清空并重建 DFS 序、深度和倍增表；要求原图是连通树，可重复调用或换根。 |
| `isAncestor(u,v)` | 要求已 build 且点号合法；返回 u 是否为 v 的祖先（含相等），不改状态。 |
| `lca(u,v)` | 要求已 build 且点号合法；返回最近公共祖先，不改状态。 |
| `buildVirtual(special)` | 接收原树点号向量（允许重复）；要求已 build；返回去重关键点及必要 LCA 构成的虚树，不改原树。空输入返回空结果。 |

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct VirtualTreeResult {
    vector<int> vertices;                 // 按 DFS 序排列的原树点号
    vector<tuple<int, int, int>> edges;   // (父点, 子点, 原树距离)
    int root = 0;                         // vertices 非空时为虚树根
};

struct VirtualTree {
    int n, logn, timer = 0;
    vector<vector<int>> g;
    vector<int> tin, tout, depth;
    vector<vector<int>> up;

    // nodeCount 为原树点数；分配 1-based 图和 LCA 表，要求随后加入 n-1 条树边。
    explicit VirtualTree(int nodeCount)
        : n(nodeCount), logn(1), g(nodeCount + 1), tin(nodeCount + 1),
          tout(nodeCount + 1), depth(nodeCount + 1) {
        assert(n >= 1);
        while ((1 << logn) <= n) ++logn;
        up.assign(logn, vector<int>(n + 1, 0));
    }

    // u、v 为 1..n；返回 void，向原树加入无向边；必须在 build 前调用。
    void addEdge(int u, int v) {
        assert(1 <= u && u <= n && 1 <= v && v <= n && u != v);
        g[u].push_back(v);
        g[v].push_back(u);
    }

    // u 的 DFS 进入/离开时间；p 是父点；返回 void，写 tin/tout/depth/up[0]。
    void dfs(int u, int p) {
        tin[u] = ++timer;
        up[0][u] = p;
        for (int j = 1; j < logn; ++j) up[j][u] = up[j - 1][up[j - 1][u]];
        for (int v : g[u]) if (v != p) {
            depth[v] = depth[u] + 1;
            dfs(v, u);
        }
        tout[u] = timer;
    }

    // root 为原树根；返回 void，清空并重建 tin/tout/depth/up；要求原图为连通树。
    void build(int root = 1) {
        assert(1 <= root && root <= n);
        timer = 0;
        fill(tin.begin(), tin.end(), 0);
        fill(tout.begin(), tout.end(), 0);
        fill(depth.begin(), depth.end(), 0);
        for (auto& row : up) fill(row.begin(), row.end(), 0);
        dfs(root, 0);
        assert(timer == n);
    }

    // 判断 u 是否为 v 的祖先（包括 u==v）；要求已 build 且点号合法；返回 bool，不改状态。
    bool isAncestor(int u, int v) const {
        return tin[u] <= tin[v] && tout[v] <= tout[u];
    }

    // 返回 u、v 的最近公共祖先；要求已 build 且两点在树中。
    int lca(int u, int v) const {
        if (isAncestor(u, v)) return u;
        if (isAncestor(v, u)) return v;
        int x = u;
        for (int j = logn - 1; j >= 0; --j)
            if (up[j][x] != 0 && !isAncestor(up[j][x], v)) x = up[j][x];
        return up[0][x];
    }

    // special 是本次询问的原树关键点，可重复；返回含关键点及必要 LCA 的虚树，要求已 build。
    VirtualTreeResult buildVirtual(vector<int> special) const {
        VirtualTreeResult result;
        if (special.empty()) return result;
        // 比较器参数是原树点号；返回 DFS 进入时间的严格次序，不修改点集。
        sort(special.begin(), special.end(), [&](int a, int b) { return tin[a] < tin[b]; });
        special.erase(unique(special.begin(), special.end()), special.end());
        vector<int> all = special;
        for (int i = 1; i < (int)special.size(); ++i) all.push_back(lca(special[i - 1], special[i]));
        // 比较器参数是关键点或 LCA；返回同一 DFS 序次序，不修改 all。
        sort(all.begin(), all.end(), [&](int a, int b) { return tin[a] < tin[b]; });
        all.erase(unique(all.begin(), all.end()), all.end());
        result.vertices = all;
        vector<int> st;
        for (int x : all) {
            while (!st.empty() && !isAncestor(st.back(), x)) st.pop_back();
            if (!st.empty())
                result.edges.push_back({st.back(), x, depth[x] - depth[st.back()]});
            st.push_back(x);
        }
        result.root = all.front();
        return result;
    }
};
```

最小调用示例，可直接放在 `main` 函数体内：原树为 `1-2,1-3,2-4,2-5`，关键点 `{4,5,3}`，其虚树应有根 1、五个保留点和四条边。

```text
VirtualTree vt(5);
vt.addEdge(1, 2); vt.addEdge(1, 3);
vt.addEdge(2, 4); vt.addEdge(2, 5);
vt.build(1);
auto result = vt.buildVirtual({4, 5, 3});
assert(result.root == 1);
assert(result.vertices.size() == 5 && result.edges.size() == 4);
```

**5. 要改哪里**

每次询问只在返回的 `vertices` 上初始化并清理 DP 状态，避免扫描整棵原树。虚树边权是原树距离，不是原树单边，距离 DP 应使用该权值。模型选择上，HLD 适合动态路径修改/查询；虚树适合原树大、每次询问关键点少的多询问。练习：输出边和距离、关键点两两路径总长度、在虚树上做关键点覆盖或最近关键点 DP。

**6. 自检**

手算关键点 `{4,5,7}`，若相邻 LCA 为 2 和 1，虚树点集为 `{1,2,4,5,7}`，边为 `1-2,2-4,2-5,1-7`；2 到 4 的压缩边权仍等于原树距离。空关键点返回空点边且根 0；单关键点只有一个点、无边。

**7. 坑**

关键点重复时先去重；只加入关键点会丢失分叉祖先，必须补入 DFS 序相邻关键点的 LCA。`buildVirtual` 会对输入排序、补 LCA 后再次排序，单次复杂度为 $O(k\log k+k\log n)$，不能只报栈扫描的线性复杂度。`tout` 与 `tin` 必须来自同一次 build；虚树边代表原树压缩路径。递归 DFS 在深链上可能栈溢出。若使用同根 HLD，`pos[u] <= pos[v] < pos[u]+sz[u]` 也可用于祖先判断；此实现用 `tin/tout`。

**8. 一句话原理**

关键点按 DFS 序排列后补入相邻 LCA，再用祖先栈连接，删去对本次问题无贡献的原树分支。

## 5.20 带权并查集 {#weighted-dsu}

**1. 它是做什么的**

有若干元素，关系以“两个元素的数值差”给出，并且关系会逐条加入。例如，题目告诉我们 `value[y]-value[x]=w`，还要判断新关系是否与旧关系矛盾，或查询两个已连通元素的差值。它适合只加边、不删除边的约束系统。

在近乎常数的摊还时间内判断两点是否同组、加入差值约束，并查询同组两点的相对差；加入一条已知的矛盾约束时返回 `false`。

顶点编号为 `1..n`。`unite(x,y,w)` 表示约束 `value[y]-value[x]=w`，返回 `true` 表示与当前约束相容，`false` 表示两点已在同组但推导出的差值不同。`relation(x,y)` 返回 `value[y]-value[x]`；两点不连通时返回空的 `optional`。模板假设所有中间和与答案能放进 `long long`，需要更大范围时将 `long long` 换成 `__int128`。

复杂度：每次合并、查找或查询的均摊时间为 $O(\alpha(n))$，空间 $O(n)$。

### 先理解普通并查集

普通并查集把若干元素分成互不相交的集合。每棵树的根代表集合，`find` 找根，`union` 把两棵树接起来；路径压缩和按大小合并使树高极小。普通并查集只能回答“是否连通”，没有记录组内元素之间的距离。

### 多保存一个“到父亲的差”

对每个结点 `x` 维护

$$d[x]=value[x]-value[parent[x]].$$

父亲改变后，`find(x)` 的路径压缩把所有差累加，于是压缩结束时 `d[x]` 变成 `value[x]-value[root]`。设 `dx=d[x]`、`dy=d[y]`，若两点同根，则已知的差必须满足

$$value[y]-value[x]=dy-dx.$$

因此新约束 `value[y]-value[x]=w` 的矛盾判定就是检查 `dy-dx==w`。

若把 `rootX` 接到 `rootY`，需要设置

$$d[rootX]=value[rootX]-value[rootY]=dy-dx-w.$$

若反过来把 `rootY` 接到 `rootX`，则

$$d[rootY]=value[rootY]-value[rootX]=w+dx-dy.$$

这两个式子是带权并查集最容易写反的地方。手算例子：先加入 `value[2]-value[1]=5`，再加入 `value[3]-value[2]=2`，得到 `value[3]-value[1]=7`；若最后要求差为 `6`，就应判定矛盾。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `parent[i]` | 父结点；根的父亲是自身。下标 `1..n` 有效，`0` 是未使用哨兵。 |
| `size[i]` | 仅根结点的集合大小，用于按大小合并。 |
| `potential[i]` | `value[i]-value[parent[i]]`；经过 `find(i)` 后变为 `value[i]-value[root]`。 |

根的 potential 为 0，只是选择参考原点，不代表题目中元素的绝对值。

**3. 函数在做什么**

| 函数 | 参数、返回 | 副作用与前提 |
|---|---|---|
| `WeightedDSU(n)` | `n>=0`；无返回值。 | 初始化编号 `1..n` 的单点集合。 |
| `find(x)` | `x` 在 `1..n`；返回根编号。 | 私有函数；路径压缩并把 `potential[x]` 累加成到根差值。 |
| `unite(x,y,w)` | `x,y` 在 `1..n`，`w` 表示 `value[y]-value[x]`；返回 `bool`。 | 异组时合并，同组时检验；可能路径压缩及改变结构。 |
| `relation(x,y)` | `x,y` 在 `1..n`；返回 `optional<long long>`。 | 查询 `value[y]-value[x]`；不连通返回 `nullopt`，可能路径压缩。 |

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;

class WeightedDSU {
    vector<int> parent, size;
    // potential[x] = value[x] - value[parent[x]]；根的值为 0 只是参考原点。
    vector<long long> potential;

    // x 必须在 1..n；返回代表元，并把 potential[x] 改成 value[x]-value[root]。
    int find(int x) {
        if (parent[x] == x) return x;
        int p = parent[x];
        parent[x] = find(p);
        potential[x] += potential[p];
        return parent[x];
    }

public:
    // n 为元素个数；建立 n 个互不连通的单点集合，初始差值均为 0。
    explicit WeightedDSU(int n)
        : parent(n + 1), size(n + 1, 1), potential(n + 1, 0) {
        assert(n >= 0);
        iota(parent.begin(), parent.end(), 0);
    }

    // x、y 在 1..n，w 表示 value[y]-value[x]=w；返回是否与现有约束相容。
    // 若两点异组则合并；若同组则只检查约束。两种情况都会先 find，可能发生路径压缩，
    // 但同组分割和已经成立的权值约束不会改变。
    bool unite(int x, int y, long long w) {
        int rx = find(x), ry = find(y);
        long long dx = potential[x], dy = potential[y];
        if (rx == ry) return dy - dx == w;
        if (size[rx] > size[ry]) {
            // value[ry]-value[rx] = w + dx - dy。
            parent[ry] = rx;
            potential[ry] = w + dx - dy;
            size[rx] += size[ry];
        } else {
            // value[rx]-value[ry] = dy - dx - w。
            parent[rx] = ry;
            potential[rx] = dy - dx - w;
            size[ry] += size[rx];
        }
        return true;
    }

    // x、y 在 1..n；find 可能压缩路径但不改变集合划分；返回 value[y]-value[x]，
    // 不连通时返回 nullopt。
    optional<long long> relation(int x, int y) {
        if (find(x) != find(y)) return nullopt;
        return potential[y] - potential[x];
    }
};
```

调用示例：

```text
WeightedDSU dsu(3);
assert(dsu.unite(1, 2, 5));
assert(dsu.unite(2, 3, 2));
auto d = dsu.relation(1, 3);
assert(d.has_value() && *d == 7);
assert(!dsu.unite(1, 3, 6));
```

**5. 要改哪里**

模 $3$ 关系时，统一规定 `potential[x]=norm(value[x]-value[parent[x]])`，其中 `norm(t)=((t%3)+3)%3`，所有差值归一化到 `{0,1,2}`；`find` 路径累加后取模，合并公式每次加减后也取模。题目若用“谁吃谁”等方向，先把语义写成 `value[y]-value[x]=w (mod 3)`，再将 `unite` 中的 `dy-dx` 与根挂接公式统一归一化，避免只改比较却没改存储。若要处理删除关系，不能在这个压缩并查集上直接删边，应改为可撤销并查集配合时间分治。

模型识别：出现“相差多少”“时刻差”“坐标偏移”“同组内相对权值”时，先尝试令每条边表示 `value[v]-value[u]`。若只问连通性，用普通并查集即可；若约束会删除、撤销或需要时间分治，改用可撤销并查集等结构。

**6. 自检**

加入 `value[2]-value[1]=5`、`value[3]-value[2]=2` 后，查询 1 到 3 应为 7，反向应为 -7；再加入差值 6 应返回矛盾。未连通两点返回空值，同点差值为 0。

**分层练习：** 入门：食物链或相对距离的三类关系；进阶：带时间戳的坐标约束与矛盾输出；提高：离线删除边、线段树分治和可撤销带权并查集。若关系是在模 $3$ 意义下的类别差，不能直接把本模板的整数加减照搬：`potential`、`w` 和每次加减都要改成模 $3$ 代表元，并按题目定义统一方向。

**7. 坑**

差值方向固定为 `value[y]-value[x]`；方向写反会使合并式和查询错。中间值也须避免溢出。

组合应用：差值约束可先离散化元素，再由带权并查集维护；在线判矛盾可用于检查方程组的一致性；与二分答案结合时，每次二分检查一批差值约束。注意该模板不能处理“边删除”或要求路径上每条边的明细。

**8. 一句话原理**

沿父亲路径累加差值，使并查集同时维护连通性和组内相对值。

## 5.21 离线树状数组 {#offline-fenwick}

**1. 它是做什么的**

查询可以等待输入全部读完，并且每次事件能按某个维度排序。典型任务是二维偏序 `x<=X 且 y<=Y`、区间查询不同数、逆序对。树状数组负责一个维度的前缀聚合，排序把另一个维度变成时间顺序。

支持单点加与前缀和；用排序扫描回答二维计数，用“最后出现位置”回答区间不同数，用从右向左扫描计算逆序对。

下方 `Fenwick` 的位置为 `1..n`，`sumPrefix(0)` 定义为 0。二维模板统计点（可重复）中满足 `px<=qx` 且 `py<=qy` 的个数；区间模板的每个查询为闭区间 `[l,r]`，答案按输入的 `id` 放回；逆序对统计 `i<j 且 a[i]>a[j]` 的对数。

复杂度：树状数组操作为 $O(\log n)$。二维偏序包含 $y$ 坐标压缩、点和询问排序，时间为 $O((p+q)\log(p+q+1))$，空间 $O(p+q)$。区间不同数为 $O(n\log(n+1)+q\log(q+1)+q\log(n+1))$，分别对应最后出现位置维护、询问排序和查询；空间 $O(n+q)$。逆序对为 $O(n\log(n+1))$，空间 $O(n)$。

### 为什么离线能降维

二维查询看似要同时限制 `x`、`y`。把点和询问按 `x` 从小到大排序，处理询问 `(X,Y)` 时，所有 `px<=X` 的点已经加入树状数组；此时树状数组在 `y` 维的前缀和正好是答案。等值事件尤其重要：当前询问的 `X` 若允许点 `px=X`，就必须先加入这些点。下方代码用 `while (point.x <= query.x)` 明确实现“点先于同 `x` 查询”，避免把等号漏掉。

区间不同数的另一种降维方法是固定右端点 `r` 扫描：值 `a[i]` 的贡献只保留它在 `[1,r]` 中最后一次出现的位置 `last[a[i]]`。每次读到新位置 `i`，先在旧位置减一、在 `i` 加一；查询 `[l,r]` 时，前缀和 `sum(r)-sum(l-1)` 恰好数出最后出现位置不小于 `l` 的值。

例如 `a=[7,3,7]` 扫到 `r=1` 时 7 的最后位置是 1，扫到 `r=3` 时先删掉位置 1，再把 7 的贡献放到位置 3；此时查询 `[2,3]` 能数到 7 和 3 两种值。二维中若两次出现点 `(2,2)`，每个点都执行一次 `add`，所以询问 `(2,2)` 的答案会把它们都计入；这正是“点集合带重复”与“不同坐标点集合”两种题意的区别。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `Fenwick::n/bit` | 有效位置上界 `n` 与树状数组；`bit` 下标从 1 开始。 |
| `PointXY{x,y}` | 一个可重复计数的点坐标。 |
| `QueryXY{x,y,id}` | 询问右上界及原输入编号；`id` 须为 `0..q-1`。 |
| `RangeQuery{l,r,id}` | 1-based 闭区间及答案编号。 |
| `ys`、`rankOf` | 合并点和询问的 y 坐标后离散化；Fenwick rank 为 1-based。 |
| `last[value]` | 区间不同数扫描中，当前前缀内该值最后出现的位置。 |
| `values`、`rank` | 逆序对压缩值域；相同值映射到同一 rank。 |

**3. 函数在做什么**

| 函数 | 参数、返回 | 副作用与前提 |
|---|---|---|
| `Fenwick(n)` | `n>=0`；构造空树状数组。 | 位置范围 `1..n`。 |
| `add(pos,delta)` | `pos` 在 `1..n`；返回 `void`。 | 将单点增量加入内部树状数组。 |
| `sumPrefix(pos)` | `pos` 在 `0..n`；返回 `long long`。 | 返回位置 `1..pos` 的和；不修改结构。 |
| `rangeSum(l,r)` | 合法 1-based 闭区间；返回 `long long`。 | 返回区间和。 |
| `countDominated(points,queries)` | 每个 query id 为 `0..q-1`；返回 `vector<long long>`。 | 返回满足 `px<=qx,py<=qy` 的点重数；不改 points。 |
| `distinctInRanges(a,queries)` | `a` 为 1-based 且 `a[0]` 忽略；区间合法、id 连续；返回 `vector<int>`。 | 按输入 id 返回不同数个数。 |
| `countInversions(a)` | 0-based `vector<long long>`；返回 `long long`。 | 统计严格逆序对 `i<j,a[i]>a[j]`，不改输入。 |

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<ll> bit;

    // n 为有效下标上界；建立全零树状数组。
    explicit Fenwick(int n) : n(n), bit(n + 1, 0) { assert(n >= 0); }

    // pos 必须在 1..n；把 bit[pos..] 对应的前缀结构都增加 delta。
    void add(int pos, ll delta) {
        assert(1 <= pos && pos <= n);
        for (int i = pos; i <= n; i += i & -i) bit[i] += delta;
    }

    // pos 在 0..n；返回原数组下标 1..pos 的元素和。
    ll sumPrefix(int pos) const {
        assert(0 <= pos && pos <= n);
        ll answer = 0;
        for (int i = pos; i > 0; i -= i & -i) answer += bit[i];
        return answer;
    }

    // l、r 为 1-based 合法闭区间；返回该区间和。
    ll rangeSum(int l, int r) const { return sumPrefix(r) - sumPrefix(l - 1); }
};

struct PointXY { ll x, y; };
struct QueryXY { ll x, y; int id; };

// points 为二维点，queries 的 id 必须为 0..queries.size()-1；返回各询问的支配点数。
vector<ll> countDominated(const vector<PointXY>& points, vector<QueryXY> queries) {
    vector<ll> ys;
    ys.reserve(points.size() + queries.size());
    for (const auto& p : points) ys.push_back(p.y);
    for (const auto& q : queries) ys.push_back(q.y);
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    // y 来自点或询问；返回离散化后 1-based 的位置，不修改 ys。
    auto rankOf = [&](ll y) -> int {
        return int(lower_bound(ys.begin(), ys.end(), y) - ys.begin()) + 1;
    };
    vector<PointXY> sortedPoints = points;
    // 比较两个点的 x；相等时任意顺序均可，因为扫描只按 x 判断。
    sort(sortedPoints.begin(), sortedPoints.end(),
         [](const PointXY& a, const PointXY& b) { return a.x < b.x; });
    // 比较两个询问的 x；相等时任意顺序均可，点会在 while 中全部加入。
    sort(queries.begin(), queries.end(),
         [](const QueryXY& a, const QueryXY& b) { return a.x < b.x; });
    Fenwick fw((int)ys.size());
    vector<ll> answer(queries.size());
    size_t ptr = 0;
    for (const auto& q : queries) {
        // <= 保证 px==q.x 的点先进入；重复点会被重复计数。
        while (ptr < sortedPoints.size() && sortedPoints[ptr].x <= q.x) {
            fw.add(rankOf(sortedPoints[ptr].y), 1);
            ++ptr;
        }
        int upto = int(upper_bound(ys.begin(), ys.end(), q.y) - ys.begin());
        answer[q.id] = fw.sumPrefix(upto);
    }
    return answer;
}

struct RangeQuery { int l, r, id; };

// a 为 1-based 数组（a[0] 忽略）；查询合法且 id 连续；返回每个闭区间的不同元素数。
vector<int> distinctInRanges(const vector<int>& a, vector<RangeQuery> queries) {
    int n = (int)a.size() - 1;
    // 按右端点升序处理；右端点相等时按左端点升序只是稳定的次序选择。
    sort(queries.begin(), queries.end(),
         [](const RangeQuery& u, const RangeQuery& v) {
             return u.r != v.r ? u.r < v.r : u.l < v.l;
         });
    Fenwick fw(n);
    map<int, int> last; // 用 map 避免哈希碰撞；值的范围无需预先知道。
    vector<int> answer(queries.size());
    int right = 0;
    for (const auto& q : queries) {
        while (right < q.r) {
            ++right;
            auto it = last.find(a[right]);
            if (it != last.end()) fw.add(it->second, -1);
            fw.add(right, 1);
            last[a[right]] = right;
        }
        answer[q.id] = (int)fw.rangeSum(q.l, q.r);
    }
    return answer;
}

// a 为 0-based 数组；返回所有 i<j 且 a[i]>a[j] 的对数。
ll countInversions(const vector<ll>& a) {
    vector<ll> values = a;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    Fenwick fw((int)values.size());
    ll answer = 0;
    for (auto it = a.rbegin(); it != a.rend(); ++it) {
        int rank = int(lower_bound(values.begin(), values.end(), *it) - values.begin()) + 1;
        answer += fw.sumPrefix(rank - 1); // 已见元素中严格小于当前值，正好构成当前左端点的逆序对。
        fw.add(rank, 1);
    }
    return answer;
}
```

调用示例：

```text
vector<PointXY> points = {{2, 2}, {2, 2}, {3, 1}};
auto dominated = countDominated(points, {{2, 2, 0}});
assert(dominated[0] == 2);
vector<int> a = {0, 7, 3, 7};
auto distinct = distinctInRanges(a, {{2, 3, 0}});
assert(distinct[0] == 2);
auto inversions = countInversions({3, 1, 2});
assert(inversions == 2);
```

**5. 要改哪里**

三种常见边界改法：二维偏序若 x 条件是严格 `<`，把点加入条件 `point.x <= q.x` 改成 `<`；y 条件严格 `<` 时将 `upper_bound(y)` 改为 `lower_bound(y)`。区间不同数按右端点扫描时，先删值的旧最后位置，再在新位置加 1；不要改成“每个位置永久加 1”。逆序对要严格 `a[i]>a[j]`，所以反向扫描查询 `rank-1`；若统计 `>=`，查询前缀应包括当前 rank，但还需明确定义相等对是否计入。

模型识别：全部询问已知、答案互不影响、一个维度能排序时优先考虑离线。看到“所有点左下方有多少点”想到二维偏序；看到“区间有多少种数”想到右端点排序和最后出现位置；看到“`i<j` 且大小关系”想到排序/离散化加树状数组。

**6. 自检**

例中重复点 `(2,2)` 应计两次；数组 `[7,3,7]` 的 `[2,3]` 区间有 2 个不同值；`[3,1,2]` 有 2 个严格逆序对。把所有值改成相等时，逆序对应为 0，任意非空区间的不同数为 1。

**分层练习：** 入门：静态单点修改、区间和与逆序对；进阶：二维矩形左下计数、区间不同数；提高：三维偏序、带时间维度的修改查询和 CDQ 分治。要特别测试空询问列表、相同 `x/y` 的重复点、全相同数组和全逆序数组。

**7. 坑**

等号由扫描条件及 `lower_bound/upper_bound` 决定；重复点按重数计，查询 id 和闭区间范围须合法。

组合应用：二维偏序还能扩展到 CDQ 分治、三维偏序和扫描线；区间不同数可与莫队比较取舍；逆序对可作为归并排序、Fenwick 或线段树的练习。值域很大时先坐标压缩，重复值必须保留相同 rank。

**8. 一句话原理**

排序把一个维度变成扫描进度，树状数组维护剩余维度的前缀统计。

## 5.22 莫队算法 {#mo-algorithm}

**1. 它是做什么的**

数组静态不变，有很多离线区间询问，并且从区间 `[l,r]` 增删一个端点时，答案可以在较小代价内更新。例如区间不同数、区间内出现次数满足条件的值的个数、频率平方和。它要求所有询问可以一起读入并重排。

把任意询问区间逐步移动为当前区间，通过四种操作 `addLeft`、`addRight`、`removeLeft`、`removeRight` 维护答案；下方模板回答区间不同数。

数组 `a[1..n]` 在整个过程中不可修改；查询为合法闭区间 `[l,r]`，输入 `id` 为 `0..q-1`，答案按 `id` 返回。当前窗口初始为空 `[1,0]`，所以每一步都只调用合法的加入或删除。

复杂度：设块长为 $B$。经典按块排序的端点移动上界为 $O(n^2/B+qB)$，每次移动 $O(1)$；排序询问另需 $O(q\log(q+1))$，值离散化预处理需 $O(n\log(n+1))$。取 $B\approx\sqrt n$ 时得到常见的 $O(n\sqrt n+q\sqrt n+q\log(q+1)+n\log(n+1))$ 表达式；空间 $O(n+q)$。这是移动次数上界，蛇形排序通常只改善常数。

### 为什么重排询问有效

如果按输入顺序回答，区间端点可能每次跨过 $n$ 个位置，最坏为 $O(nq)$。把 `l` 按块排序，再让同块内的 `r` 单调（奇偶块交替方向可减少来回），相邻区间只移动有限距离。算法的关键不是“记住一种排序”，而是确认四种单点增删都能维护目标信息。

它不是动态数据结构：数组元素改变后，频率表通常失效。需要修改时应使用带修改莫队（增加时间维度）或其他结构。若答案无法从“加入一个元素/删除一个元素”快速更新，例如任意区间最短路，也不适合直接套莫队。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `MoQuery{l,r,id}` | 1-based 闭区间及原查询编号；id 连续为 `0..q-1`。 |
| `n` | `a.size()-1`，数组有效位置数。 |
| `compressed[i]` | `a[i]` 的离散编号，编号从 0 开始。 |
| `blockLength` | 左端点分块长度，至少为 1。 |
| `frequency[v]` | 当前窗口中离散值 `v` 的出现次数。 |
| `left/right` | 当前闭窗口端点；初始 `left=1,right=0` 表示空区间。 |
| `distinct` | 当前窗口内频次非零的离散值个数。 |

**3. 函数在做什么**

| 函数 | 参数、返回 | 副作用与前提 |
|---|---|---|
| `MoDistinct(a)` | 1-based 静态数组，允许 `n=0`。 | 复制并压缩值，建立频次数组。 |
| `addValue(value,distinct)` | 离散编号、计数器引用；返回 `void`。 | 增加该值频次；从 0 到 1 时增加 distinct。 |
| `removeValue(value,distinct)` | 当前窗口内存在的离散编号、计数器引用；返回 `void`。 | 减少频次；从 1 到 0 时减少 distinct。 |
| `solve(queries)` | 合法 1-based 闭区间、id 连续；返回 `vector<int>`。 | 仅重排参数副本、清频次并计算答案；原数组不变，可重复调用。 |

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct MoQuery { int l, r, id; };

class MoDistinct {
    int n;
    vector<int> compressed;
    int blockLength;
    vector<int> frequency;

    // value 是已离散化的值编号；把它加入当前窗口并更新 distinct 的引用值。
    void addValue(int value, int& distinct) {
        if (frequency[value]++ == 0) ++distinct;
    }

    // value 是已离散化的值编号；它必须当前至少出现一次，再删除并更新 distinct。
    void removeValue(int value, int& distinct) {
        assert(frequency[value] > 0);
        if (--frequency[value] == 0) --distinct;
    }

public:
    // a 为 1-based 静态数组；压缩其值并建立计数表，后续 solve 不修改 a 的逻辑内容。
    explicit MoDistinct(const vector<int>& a) : n((int)a.size() - 1) {
        assert(n >= 0);
        vector<int> values(a.begin() + (n ? 1 : 0), a.end());
        sort(values.begin(), values.end());
        values.erase(unique(values.begin(), values.end()), values.end());
        compressed.assign(n + 1, 0);
        for (int i = 1; i <= n; ++i)
            compressed[i] = int(lower_bound(values.begin(), values.end(), a[i]) - values.begin());
        frequency.assign(values.size(), 0);
        blockLength = max(1, (int)sqrt(max(1, n)));
    }

    // queries 的 l、r 合法且 id 连续；返回各区间不同数，输入查询顺序不影响结果。
    // 每次调用都会清空计数，因此可重复调用；数组本身必须保持静态。
    vector<int> solve(vector<MoQuery> queries) {
        for (int& x : frequency) x = 0;
        // 先按左端点所在块，再按右端点蛇形排序；返回严格弱序比较结果。
        sort(queries.begin(), queries.end(), [this](const MoQuery& a, const MoQuery& b) {
            int ba = a.l / blockLength, bb = b.l / blockLength;
            if (ba != bb) return ba < bb;
            return (ba & 1) ? a.r > b.r : a.r < b.r;
        });
        vector<int> answer(queries.size());
        int left = 1, right = 0, distinct = 0;
        for (const MoQuery& q : queries) {
            while (left > q.l) addValue(compressed[--left], distinct);
            while (right < q.r) addValue(compressed[++right], distinct);
            while (left < q.l) removeValue(compressed[left++], distinct);
            while (right > q.r) removeValue(compressed[right--], distinct);
            answer[q.id] = distinct;
        }
        return answer;
    }
};
```

调用示例：

```text
vector<int> a = {0, 1, 2, 1, 3};
MoDistinct mo(a);
auto answer = mo.solve({{1, 2, 0}, {2, 4, 1}});
assert(answer[0] == 2 && answer[1] == 3);
```

**5. 要改哪里**

把目标改成频次平方和时，维护 `sumSq=Σ_v freq[v]^2`。加入值 `v` 前令 `f=freq[v]`，更新 `sumSq += 2*f+1` 再令频次加一；删除前令 `f=freq[v]`，更新 `sumSq -= 2*f-1` 再减频次。每个端点增删仍为 $O(1)$，`solve` 的排序和移动逻辑不变。若只求最高频次，还需维护桶计数或其他能支持频次变化的结构，不能仅替换答案变量。

模型识别：关键词包括“静态数组”“大量区间询问”“加入/删除一个值即可维护”。如果询问本身在线到达、必须立即输出，无法重排；如果有单点修改，先考虑带修改莫队、线段树或树状数组。

**6. 自检**

**手算小例子：** `a=[1,2,1,3]`，先处理 `[1,2]` 得到频次 `{1:1,2:1}`、答案 2；移动到 `[2,4]` 时删掉位置 1 的 1，再加入位置 3 的 1 和位置 4 的 3，频次 `{1:1,2:1,3:1}`，答案 3。每次只改一个端点，不重新扫描区间。

**分层练习：** 入门：区间不同数；进阶：区间内众数频次、颜色出现次数；提高：带修改莫队、树上莫队和回滚莫队。

**7. 坑**

数组建好对象后保持不变；删除值必须确实在窗口内；查询 id、区间符合模板契约。

组合应用：把 `frequency` 换成维护平方和、最大频次、满足频率条件的计数器，即可解决更多区间统计；树上莫队先用欧拉序和 LCA 把路径转为区间，并额外处理端点。与离线树状数组相比，莫队能处理“可增可删但难以单调扫描”的状态。

**8. 一句话原理**

排序询问后复用当前窗口状态，只为端点移动付出代价。

## 5.23 笛卡尔树 {#cartesian-tree}

**1. 它是做什么的**

给定一个静态序列，需要把“原数组的顺序”和“区间最值的层次结构”同时表示。最小笛卡尔树满足：中序遍历正好得到原序列，且父节点值不大于子节点值；最大树则把“不大于”换成“不小于”。

在线性时间建树，随后可用树上的 LCA 表示 RMQ（区间最小/最大值）；它也常用于单调栈、子数组贡献、区间最值分治。下方模板建立最小笛卡尔树，并规定重复最小值保留更靠左者为祖先。

输入 `a[1..n]`，不能为空；返回根、左右孩子和父亲数组，编号仍为 `1..n`，不存在的孩子或父亲为 `0`。中序遍历返回 `1,2,...,n`，且每个父子边满足最小堆性质。

复杂度：单调栈建树时间 $O(n)$、空间 $O(n)$。

### 单调栈推导

从左到右处理 `i`，栈中下标对应的值非递减（相等值不弹出，所以更左的相等值优先）。新值 `a[i]` 到来时，所有栈顶值大于它的节点都不可能再做这些节点右侧的祖先，连续弹出并记为 `last`。若栈仍非空，当前栈顶是 `i` 的左侧最近小于等于它的值，将它的右儿子设为 `i`；被弹出的整棵子树成为 `i` 的左儿子。最后栈底就是根。

手算 `[3,1,4,2]`：读 3 得栈 `[1]`；读 1 弹出 1，栈空，故 1 为新根且左儿子为 3；读 4，设 1 的右儿子为 4；读 2 弹出 4，设 1 的右儿子为 2、2 的左儿子为 4。中序仍是 3,1,4,2，堆序也成立。

**最小值贡献：** 对节点 `i`，设笛卡尔树左、右子树大小为 `L`、`R`。以 `i` 为最小值归属点的子数组必须从 `i` 的左子树中任选一段向左延伸（或不延伸），从右子树中任选一段向右延伸（或不延伸），因此贡献次数是 `(L+1)(R+1)`。相等值按“更左者优先”归属：相等节点在右侧链上，包含左侧相等节点的区间会归给更左节点，不会重复计数。若每个元素权值为 `a[i]`，所有子数组最小值之和即可写为 `sum(a[i]*(L+1)*(R+1))`；最大值贡献则建立最大笛卡尔树。

**2. 变量在做什么**

| 字段/局部量 | 含义 |
|---|---|
| `root` | 树根的原数组下标，范围 `1..n`。 |
| `left[u]`,`right[u]` | 下标 `u` 的左右孩子；0 表示没有孩子。 |
| `parent[u]` | 下标 `u` 的父亲；根和不存在的结点均为 0。 |
| `stack` | 建树过程中的候选祖先下标；从底到顶对应值非递减。 |
| `last` | 本轮最后弹出的下标，位于本轮弹出段的最底部，成为新节点的左子树根。 |

**3. 函数在做什么**

| 函数 | 参数、返回 | 副作用与前提 |
|---|---|---|
| `buildMinCartesian(a)` | 1-based 非空 `vector<long long>`；返回 `CartesianTree`。 | 不改输入；结果编号为 `1..n`，不存在的连接为 0。 |

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct CartesianTree {
    int root = 0;
    vector<int> left, right, parent;
};

// a 为 1-based 非空数组；返回满足中序顺序和最小堆性质的笛卡尔树。
// 相等值不弹栈，因此相等最小值中下标较小者为祖先。
CartesianTree buildMinCartesian(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    assert(n >= 1);
    CartesianTree result;
    result.left.assign(n + 1, 0);
    result.right.assign(n + 1, 0);
    result.parent.assign(n + 1, 0);
    vector<int> stack;
    for (int i = 1; i <= n; ++i) {
        int last = 0;
        while (!stack.empty() && a[stack.back()] > a[i]) {
            last = stack.back();
            stack.pop_back();
        }
        if (!stack.empty()) result.right[stack.back()] = i;
        result.left[i] = last;
        stack.push_back(i);
    }
    result.root = stack.front();
    for (int u = 1; u <= n; ++u) {
        if (result.left[u]) result.parent[result.left[u]] = u;
        if (result.right[u]) result.parent[result.right[u]] = u;
    }
    return result;
}
```

调用示例：

```text
vector<ll> a = {0, 3, 1, 4, 2};
CartesianTree tree = buildMinCartesian(a);
assert(tree.root == 2);
assert(tree.left[2] == 1 && tree.right[2] == 4);
// 对完整验证，另做中序遍历并核对结果为 1,2,3,4。
```

**5. 要改哪里**

要让相等最小值中更靠右者优先，把弹栈比较从 `a[top] > a[i]` 改为 `a[top] >= a[i]`；这样等值旧节点被弹出，较右节点成为祖先。做“每个元素作为区间最小值”的贡献时，必须让左右边界的严格/非严格约束只在一侧处理相等，避免重复计数；当前树对应左侧相等优先。子数组最小值总和用 `a[i]*(L+1)*(R+1)` 累加，`L/R` 是左右子树大小，乘积和累加类型要足够宽。最大值版本换成最大笛卡尔树并同步调整比较符。

模型识别：看到“区间最小值的分治结构”“中序必须保留原下标顺序”“所有子数组的最小值贡献”，想到笛卡尔树。静态 RMQ 也可以用稀疏表，动态修改通常改用线段树；笛卡尔树本身不支持原数组值的在线修改。

**6. 自检**

数组 `[3,1,4,2]` 的根为下标 2，左儿子为 1、右儿子为 4；中序遍历须恢复下标 `[1,2,3,4]`。全相等数组在严格 `>` 弹栈规则下形成向右的链，根为最左位置。

**分层练习：** 入门：验证中序和堆性质；进阶：用笛卡尔树加 LCA 做静态 RMQ；提高：所有子数组最小值之和及重复最值的贡献分配。

**7. 坑**

比较条件决定相等值归属；本模板严格用 `>`，较左相等最小值优先；数组不可为空。

组合应用：笛卡尔树的父子关系可让某些子数组贡献转为子树贡献；建树后给每个节点做 DFS 序，再用 LCA 回答 RMQ。大数组递归 DFS 可能爆栈，应改写为显式栈或使用安全的递归深度策略。

**8. 一句话原理**

单调栈把原序列中序次序和最值堆序编码为一棵树。

## 5.24 李超线段树 {#li-chao-tree}

**1. 它是做什么的**

维护许多直线 `y=kx+b`，在线加入直线，并在一组已知横坐标上询问最大值。它适合“每次转移都是某条直线在当前 `x` 的值”的 DP 优化；直线可以任意交叉，插入后不能删除。

支持插入整条直线和单点最大值查询；没有插入任何直线的查询返回空 `optional`。横坐标先压缩为实际会查询的坐标，因此不要求 `x` 连续，也能正确处理负数、重复坐标和空坐标集合。平行线会自然保留截距较大的那条。

下方 `LiChaoMax` 构造时接收所有可能查询的 `x`，自动排序去重。`addLine(k,b)` 加入 `kx+b`；`query(x)` 要求 `x` 在构造时给出的坐标集合中，返回 `optional<__int128_t>`。比较和计算均使用 `__int128`，因为即使 `k`、`x`、`b` 各自能放入 `long long`，乘积 `k*x` 也可能溢出。

复杂度：每次插入和查询 $O(\log m)$，其中 $m$ 是不同查询横坐标数；空间 $O(m)$。若要在任意整数区间在线询问，可将离散坐标树改为固定整数域的动态节点实现。

### 为什么一个节点只需保留一条线

节点代表一段已压缩横坐标。两条直线至多交一次：在区间中点比较后，较差的那条若在左端更优，就只可能继续在左半边胜出；若右端更优，就只递归右半边。每次比较后节点保存两条候选中在该区间中点更优的直线，另一条沿可能获胜的方向下传。因此不会遗漏任何查询点。

DP 中常见的推导是

$$dp[i]=\max_j(m_jx_i+b_j)$$

或最小值版本。把关于 `j` 的部分整理为直线 `y=m_jx+b_j`，每计算一个 `dp[i]` 就查询 `x_i`；若之后的状态会使用 `dp[i]`，再把由 `dp[i]` 生成的直线插入。最小值可以把所有斜率和截距取负后调用最大值结构，再把答案取负。

例如转移

$$dp[i]=\max_j\{dp[j]+a[j]x_i+c[j]\}$$

在计算 `i` 前，把每个已知状态 `j` 加入直线 `k=a[j]`、`b=dp[j]+c[j]`，然后 `dp[i]=query(x_i)`；若 `i` 也能成为后继，就在得到答案后再加入 `(a[i],dp[i]+c[i])`。这就是“先查后插”还是“先插后查”必须按转移下标严格确定的原因。最小值取反时要先在 `__int128` 中取负，不能对 `LLONG_MIN` 做 `-x`；同时本模板的 `Line::b` 是 `long long`，整理出的截距必须确实落在 `long long`，否则需要把直线参数也扩展为 `__int128`。

**2. 变量在做什么**

| 字段/局部量 | 含义 |
|---|---|
| `Line{k,b}` | 斜率与截距，均为 `long long`；代表 `y=kx+b`。 |
| `xs` | 构造时坐标排序去重后的数组；只有这些坐标可查询。 |
| `tree[node]` | 节点区间当前保留的直线。 |
| `used[node]` | 是否已有直线；区分空树与有效直线。 |
| `left/right/mid` | 当前离散下标区间及中点；不是原始 x 值。 |
| `position` | 查询坐标在 `xs` 中的下标。 |

**3. 函数在做什么**

| 函数 | 参数、返回 | 副作用与前提 |
|---|---|---|
| `Line::value(x)` | `x` 为 `long long`；返回 `i128`。 | 精确计算 `k*x+b`。 |
| `LiChaoMax(xs)` | 所有可能查询的坐标；返回对象。 | 排序去重，允许空坐标集合，初始化空树。 |
| `insert(...)` | 私有节点、离散闭区间及直线；无返回值。 | 插入/交换节点代表线并向可能胜出的一侧递归。 |
| `indexOf(x)` | x 必须属于 `xs`；返回 0-based 下标。 | 只查找，不修改。 |
| `addLine(k,b)` | `long long` 斜率、截距；返回 `void`。 | 改变线段树；空坐标集合时忽略插入。 |
| `query(x)` | x 必须属于 `xs`；返回 `optional<i128>`。 | 查询已插入直线最大值；无直线或坐标集合为空返回 `nullopt`。 |

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct LiChaoMax {
    struct Line {
        ll k = 0, b = 0;
        // x、k、b 可为 long long；返回 k*x+b 的精确 __int128 值。
        i128 value(ll x) const { return (i128)k * x + b; }
    };

    vector<ll> xs;
    vector<Line> tree;
    vector<char> used;

    // xs 可以为空；保存排序去重后的所有合法查询横坐标，并建立空节点树。
    explicit LiChaoMax(vector<ll> xs) : xs(std::move(xs)) {
        sort(this->xs.begin(), this->xs.end());
        this->xs.erase(unique(this->xs.begin(), this->xs.end()), this->xs.end());
        tree.assign(max(1, 4 * (int)this->xs.size()), Line{});
        used.assign(tree.size(), false);
    }

private:
    // node 代表离散下标 [left,right]；把 line 加入该节点及必要的子节点。
    void insert(int node, int left, int right, Line line) {
        if (!used[node]) {
            tree[node] = line;
            used[node] = true;
            return;
        }
        int mid = (left + right) / 2;
        if (line.value(xs[mid]) > tree[node].value(xs[mid]))
            swap(line, tree[node]);
        if (left == right) return;
        // swap 后 tree[node] 在中点不劣，line 才是需要继续寻找胜点的候选。
        bool lineBetterAtLeft = line.value(xs[left]) > tree[node].value(xs[left]);
        bool lineBetterAtRight = line.value(xs[right]) > tree[node].value(xs[right]);
        if (lineBetterAtLeft)
            insert(node * 2, left, mid, line);
        else if (lineBetterAtRight)
            insert(node * 2 + 1, mid + 1, right, line);
    }

    // 返回 x 在 xs 中的下标；调用者必须保证 x 确实是构造时的坐标。
    int indexOf(ll x) const {
        auto it = lower_bound(xs.begin(), xs.end(), x);
        assert(it != xs.end() && *it == x);
        return int(it - xs.begin());
    }

    // 在离散下标 position 的根到叶路径上取已插入直线的最大值。
    optional<i128> queryNode(int node, int left, int right, int position) const {
        optional<i128> answer;
        if (used[node]) answer = tree[node].value(xs[position]);
        if (left == right) return answer;
        int mid = (left + right) / 2;
        optional<i128> child = position <= mid
            ? queryNode(node * 2, left, mid, position)
            : queryNode(node * 2 + 1, mid + 1, right, position);
        if (!child) return answer;
        if (!answer || *child > *answer) return child;
        return answer;
    }

public:
    // k、b 表示新直线 y=kx+b；空横坐标集合时忽略插入，其他情况修改树。
    void addLine(ll k, ll b) {
        if (!xs.empty()) insert(1, 0, (int)xs.size() - 1, Line{k, b});
    }

    // x 必须属于构造时坐标集合；返回所有已加入直线在 x 处的最大值，空集合返回 nullopt。
    optional<i128> query(ll x) const {
        if (xs.empty()) return nullopt;
        return queryNode(1, 0, (int)xs.size() - 1, indexOf(x));
    }
};
```

调用示例：

```text
LiChaoMax lc({0, 2, 5});
lc.addLine(1, 0);
lc.addLine(-1, 4);
auto best = lc.query(2);
assert(best.has_value() && *best == 2);
auto missing = lc.query(0);
assert(missing.has_value() && *missing == 4);
```

**5. 要改哪里**

最小值可把直线系数取反后用最大值树，再将查询结果取反；先转成 `i128` 再取负，避免 `LLONG_MIN` 溢出。当前 `Line::k,b` 仍是 `long long`，所以取反后的斜率、截距也必须能放回 `long long`；若题目系数超出该范围，需要把字段与 `addLine` 参数也改为 `i128`。插入阶段中点交换后，节点保存中点更优直线，剩下的候选线只沿端点仍更优的一侧递归；不要把分支判断套用到交换前的线。

模型识别：DP 转移中若能整理成“枚举旧状态的斜率和截距，再代入当前 `x`”，并且只需单点查询，就考虑李超树。若斜率单调、查询横坐标单调，凸包优化可能更简单；若需要区间插入直线，可使用李超树的区间递归扩展。

**6. 自检**

**手算小例子：** 先加入 `y=x`，再加入 `y=-x+4`，查询 `x=0,2,5` 得到 `4,2,5`。两线在 `x=2` 相等，李超树在中点保留哪一条都不影响答案；若再加入平行线 `y=x+3`，它会在所有查询点压过 `y=x`，而无需特殊分支。

**分层练习：** 入门：固定横坐标集合上的直线最大值；进阶：斜率优化 DP、平行线和负坐标；提高：区间加线、持久化李超树和动态坐标域。

**7. 坑**

查询 x 必须属于构造坐标；直线不能删除；参数为 long long，只有求值扩展到 __int128。

组合应用：与坐标压缩结合处理离散 `x`；与前缀最优、斜率优化 DP 结合时按状态产生直线；将符号全部取反可把最大值模板用于最小值，但取反必须使用 `__int128` 避免 `LLONG_MIN` 溢出，且转换后的斜率、截距要满足模板的 `long long` 契约。若答案要打印，另写 `__int128` 转十进制函数，不能直接交给 `cout`。

**8. 一句话原理**

两条直线至多交一次，节点保留中点胜者并沿可能获胜的方向下传另一条线。

## 5.25 差分 + GCD 线段树 {#difference-gcd-tree}

**1. 它是做什么的**

数组 `a[1..n]` 需要区间加法和区间 GCD 查询；操作在线给出，要求 `n,q` 较大。元素、差分、前缀和、`-x` 以及绝对值中间结果都必须能表示为 `long long`；特别地，不能出现 `LLONG_MIN`，因为它的绝对值无法表示。
`rangeAdd(l,r,x)` 把闭区间每项加上 `x`；`rangeGcd(l,r)` 返回更新后 `gcd(|a[l]|,...,|a[r]|)`。
构造器接收非空的 1-based 数组；区间必须满足 `1<=l<=r<=n`。GCD 取非负值，负数数组也可以输入。
复杂度：建树 $O(n\log V)$，每次操作 $O(\log n\log V)$，空间 $O(n)$；`V` 是中间数值的上界，64 位整数上的欧几里得算法最多迭代常数次，竞赛中常把额外的 $\log V$ 视为常数。

### 从朴素做法到两个可维护量

若每次区间加都逐项修改，再逐项求 GCD，单次操作最坏是 $O(n)$。关键恒等式是

$$
\gcd(a_l,a_{l+1},\ldots,a_r)=\gcd(a_l,a_{l+1}-a_l,\ldots,a_r-a_{r-1}).
$$

记差分数组 `b[1]=a[1]`、`b[i]=a[i]-a[i-1]`。区间 `[l,r]` 加 `x` 只会改变两个差分点：`b[l]+=x`，以及存在时 `b[r+1]-=x`。所以用树状数组维护 `b` 的前缀和，就能在 $O(\log n)$ 得到 `a[l]`；用线段树维护 `|b[i]|` 的 GCD，就能在 $O(\log n)$ 查询 `b[l+1..r]` 的 GCD。查询答案是两者的 GCD。不能把一个节点的 GCD 直接加上 `x`：例如节点值为 `[6,10]` 时 GCD 是 `2`，整体加 `1` 后变成 `[7,11]`，新 GCD 是 `1` 而不是 `3`。差分只改边界，才把区间加转成了可维护的点加。

例如 `a=[6,10,14,15]` 的差分是 `[6,4,4,1]`。给 `[2,3]` 加 `5` 后，只改成 `[6,9,4,-4]`，恢复出的数组是 `[6,15,19,15]`；查询 `[2,4]` 只需 `gcd(15,4,-4)=1`。实现中 `diff[pos] += delta` 和 `-x` 也要求不溢出；当 `x==LLONG_MIN` 时 `-x` 无法表示，`llabs(LLONG_MIN)` 同样未定义可表示结果，调用者必须排除这些输入。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `n` | 原数组长度；所有公开区间是 1-based 闭区间。 |
| `diff[i]` | 差分 `b[i]`，`b[1]=a[1]`，`b[i]=a[i]-a[i-1]`。 |
| `bit` | Fenwick 树，维护 `diff` 的前缀和；`sumBit(i)` 还原 `a[i]`。 |
| `seg` | GCD 线段树，叶子为 `|diff[i]|`，内部为儿子 GCD。 |
| `p,l,r` | 递归树节点编号及其管理的闭区间；`pos` 是被改的差分下标。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `DifferenceGcdTree(a)` | 要求 `a` 是非空 1-based `vector<ll>`；复制并初始化差分、BIT 与 GCD 树，不改输入。 |
| `addBit(i,delta)` | `i∈[1,n]`；把差分点增量加到 BIT，返回 `void`。 |
| `sumBit(i)` | `i∈[0,n]`；返回 `b[1..i]` 之和，i=0 返回 0。 |
| `build(p,l,r)` | 初始化管理 `[l,r]` 的 GCD 摘要；递归辅助函数，仅应按本结构的节点区间约定调用。 |
| `pointAdd(p,l,r,pos,delta)` | 改 `diff[pos]` 并重算祖先 GCD；位置必须在当前节点区间。 |
| `query(p,l,r,ql,qr)` | 返回合法闭子区间差分绝对值的 GCD。 |
| `rangeAdd(l,r,x)` | 合法闭区间加 x；修改 BIT 与 GCD 树，无返回值。要求所有中间值可表示且 `x!=LLONG_MIN`。 |
| `rangeGcd(l,r)` | 返回当前闭区间非负 GCD；不修改结构。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<long long> a = {0, 6, 10, 14, 15};
DifferenceGcdTree st(a);
st.rangeAdd(2, 3, 5);
long long answer = st.rangeGcd(2, 4);
assert(answer == 1);
```


```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DifferenceGcdTree {
    int n;
    vector<ll> diff, bit, seg;

    // a[1..n] 是非空 1-based 初值；复制差分并建立树状数组和 GCD 线段树，不修改 a。
    explicit DifferenceGcdTree(const vector<ll>& a) : n((int)a.size() - 1), diff(n + 1, 0), bit(n + 1, 0), seg(4 * n + 4, 0) {
        assert(n >= 1);
        for (int i = 1; i <= n; ++i) diff[i] = a[i] - (i == 1 ? 0 : a[i - 1]);
        for (int i = 1; i <= n; ++i) bit[i] += diff[i];
        for (int i = 1; i <= n; ++i) if (i + (i & -i) <= n) bit[i + (i & -i)] += bit[i];
        build(1, 1, n);
    }

    // i 为 1..n；delta 为差分点增量；返回 void，更新 bit[i..n] 的前缀和结构。
    void addBit(int i, ll delta) {
        for (; i <= n; i += i & -i) bit[i] += delta;
    }

    // i 为 0..n；返回差分 b[1..i] 的和，即原数组 a[i]（i=0 时返回 0）。
    ll sumBit(int i) const {
        ll result = 0;
        for (; i > 0; i -= i & -i) result += bit[i];
        return result;
    }

    // p 管理闭区间 [l,r]；按叶子的差分值建立 GCD 摘要；返回 void，只写 seg。
    void build(int p, int l, int r) {
        if (l == r) { seg[p] = llabs(diff[l]); return; }
        int m = (l + r) / 2;
        build(p * 2, l, m); build(p * 2 + 1, m + 1, r);
        seg[p] = gcd(seg[p * 2], seg[p * 2 + 1]);
    }

    // p 管理 [l,r]，pos 是合法差分点，delta 是该点增量；返回 void，维护叶子及祖先 GCD。
    void pointAdd(int p, int l, int r, int pos, ll delta) {
        if (l == r) { diff[pos] += delta; seg[p] = llabs(diff[pos]); return; }
        int m = (l + r) / 2;
        if (pos <= m) pointAdd(p * 2, l, m, pos, delta);
        else pointAdd(p * 2 + 1, m + 1, r, pos, delta);
        seg[p] = gcd(seg[p * 2], seg[p * 2 + 1]);
    }

    // p 管理 [l,r]；返回区间差分的非负 GCD，ql..qr 必须是合法闭区间。
    ll query(int p, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) return seg[p];
        int m = (l + r) / 2; ll result = 0;
        if (ql <= m) result = gcd(result, query(p * 2, l, m, ql, qr));
        if (qr > m) result = gcd(result, query(p * 2 + 1, m + 1, r, ql, qr));
        return result;
    }

    // l,r 为 1-based 合法闭区间；x 为任意增量；返回 void，修改原数组的逻辑表示。
    void rangeAdd(int l, int r, ll x) {
        assert(1 <= l && l <= r && r <= n);
        assert(x != LLONG_MIN);
        addBit(l, x); pointAdd(1, 1, n, l, x);
        if (r < n) { addBit(r + 1, -x); pointAdd(1, 1, n, r + 1, -x); }
    }

    // l,r 为 1-based 合法闭区间；返回当前 a[l..r] 的非负 GCD，不修改结构。
    ll rangeGcd(int l, int r) const {
        assert(1 <= l && l <= r && r <= n);
        ll inside = (l == r ? 0 : query(1, 1, n, l + 1, r));
        return gcd(sumBit(l), inside);
    }
};
```

**5. 要改哪里**

- 若更新只发生在单点 `[l,l]`，仍须在存在时修改 `b[l+1]`，才能抵消对后续元素的影响；只有右端点等于 `n` 时跳过 `b[n+1]`。
- 如果需要查询区间和，应另维护前缀和结构或换用懒标记线段树；GCD 摘要无法直接支持区间加。
- 若改为区间赋值，差分会影响边界内的大量差分项，不能只调用两次 `pointAdd`。

**6. 自检**

原数组 `[6,10,14,15]` 经 `[2,3] += 5` 后为 `[6,15,19,15]`，故 `rangeGcd(2,4)==1`；`rangeGcd(3,3)==19`。`r=n` 的更新后查询不可触及 `n+1`。

**7. 坑**

- GCD 必须按非负绝对值计算；不能直接把有符号差分送给 `llabs` 并忽略 `LLONG_MIN`。
- 更新 `[l,r]` 时忘记在 `r+1` 减去 x，会让区间右侧整体偏移。
- 区间 GCD 由 `gcd(a[l], gcd(b[l+1..r]))` 得出，不能错误查询 `b[l..r]` 后再与 `a[l]` 合并。
- `rangeAdd` 断言范围，不代表算术溢出会被检测；调用者仍须保证所有中间值安全。

**8. 一句话原理**

区间加只改变差分数组的两个端点，而区间 GCD 可由左端原值与内部差分的 GCD 合成。

## 5.26 扫描线 + 线段树 {#sweep-line-segment-tree}

**1. 它是做什么的**

给出轴对齐矩形，计算它们的并面积；坐标可为负数，矩形边界为整数且总面积应能放入 `long long`。还要求每个 `x` 差、每个 `y` 覆盖跨度以及每次 `coveredY*(x-prevX)` 的乘积中间值都能放入 `long long`；否则应改用更宽整数。退化矩形（宽或高为零）不贡献面积。
在线性事件数乘对数坐标数的时间内，维护当前竖直扫描线覆盖的 `y` 长度，并累积矩形并面积。
矩形使用半开区域 `[x1,x2)×[y1,y2)`；返回并集面积。边界重合不重复计算，输入顺序不影响结果。
复杂度：过滤后有 $m$ 个矩形、至多 $2m$ 个不同 `y` 坐标时，时间 $O(m\log m)$，空间 $O(m)$。

### 为什么线段树维护“间隔”

把所有竖边按 `x` 排序，从左向右移动扫描线。相邻事件的横宽是 `x-prevX`，这段宽度内当前被覆盖的纵向长度若是 `coveredY`，就贡献 `coveredY*(x-prevX)`。到达同一个 `x` 时，必须先累积旧状态的面积，再同时处理这个 `x` 的加入和移除事件。

手算两个矩形 `A=[0,2)×[0,2)`、`B=[1,3)×[1,3)`：在 `x=0` 更新 A，当前覆盖长度为 2；到 `x=1` 先累积 `2*(1-0)=2`，再加入 B，此时覆盖 `[0,3)` 的长度为 3；到 `x=2` 先累积 `3*(2-1)=3`，再移除 A，覆盖 `[1,3)` 的长度为 2；到 `x=3` 累积 `2*(3-2)=2`。面积为 `2+3+2=7`。这个过程也说明同一横坐标必须先算旧覆盖再更新，否则会把 A 在 `x=1` 的边界错误地算进下一段。

线段树的叶子不是某个坐标点，而是相邻坐标形成的半开间隔 `[ys[i],ys[i+1])`。节点记录 `coverCount`：若大于零，整个节点间隔都被覆盖；否则取两个儿子的覆盖长度。这样既不会把边界当成有面积的点，也能正确处理多个重叠矩形。

**2. 变量在做什么**

| 字段/变量 | 含义 |
|---|---|
| `Rectangle` | `x1,y1,x2,y2` 定义半开矩形 `[x1,x2)×[y1,y2)`。 |
| `Event` | 扫描线事件 `(x,y1,y2,delta)`；左边 `+1`，右边 `-1`。 |
| `ys` | 所有有效矩形的纵坐标去重排序；叶子对应相邻坐标间隔。 |
| `cover[p]` | 节点区间被完整覆盖的矩形层数。 |
| `length[p]` | 节点区间当前被覆盖的总 y 长度；根值是扫描线覆盖长度。 |
| `area,previousX` | 已累计面积和上一批事件横坐标。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `CoveredLengthTree(ys)` | `ys` 至少含两个严格递增坐标；初始化空覆盖结构。 |
| `update(y1,y2,delta)` | y1/y2 必须是压缩坐标端点且 `y1<y2`；delta 为 +1 加覆盖或 -1 移除同一区间，修改树。 |
| `covered()` | 返回当前所有活动区间覆盖的 y 长度。 |
| `rectangleUnionArea(rectangles)` | 输入矩形向量；跳过退化矩形，返回并集面积；中间乘积及和须能装入 `ll`。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<Rectangle> rectangles = {{0, 0, 2, 2}, {1, 1, 3, 3}};
long long area = rectangleUnionArea(rectangles);
assert(area == 7);
```


```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Rectangle { ll x1, y1, x2, y2; };

struct CoveredLengthTree {
    vector<ll> y;
    vector<int> cover;
    vector<ll> length;

    // ys 严格递增，叶子代表 ys[i] 到 ys[i+1] 的间隔；初始化空覆盖树。
    explicit CoveredLengthTree(vector<ll> ys) : y(move(ys)), cover(4 * max(1, (int)y.size()) + 4, 0), length(cover.size(), 0) {
        assert(y.size() >= 2);
    }

    // p 管理间隔下标 [l,r]；根据覆盖计数和儿子长度重算该节点覆盖长度。
    void pull(int p, int l, int r) {
        if (cover[p] > 0) length[p] = y[r + 1] - y[l];
        else if (l == r) length[p] = 0;
        else length[p] = length[p * 2] + length[p * 2 + 1];
    }

    // p 管理 [l,r]，ql..qr 是要加 delta 的合法间隔下标；返回 void，保持 length 正确。
    void update(int p, int l, int r, int ql, int qr, int delta) {
        if (ql <= l && r <= qr) { cover[p] += delta; pull(p, l, r); return; }
        int m = (l + r) / 2;
        if (ql <= m) update(p * 2, l, m, ql, qr, delta);
        if (qr > m) update(p * 2 + 1, m + 1, r, ql, qr, delta);
        pull(p, l, r);
    }

    // y1,y2 必须是构造时 ys 中的两个端点且 y1<y2；delta=+1 加入、-1 移除一个已加入的完全相同区间；返回 void，修改当前覆盖长度。
    void update(ll y1, ll y2, int delta) {
        auto leftIt = lower_bound(y.begin(), y.end(), y1);
        auto rightIt = lower_bound(y.begin(), y.end(), y2);
        assert(y1 < y2 && leftIt != y.end() && rightIt != y.end() && *leftIt == y1 && *rightIt == y2);
        int l = leftIt - y.begin();
        int r = rightIt - y.begin() - 1;
        if (l <= r) update(1, 0, (int)y.size() - 2, l, r, delta);
    }

    // 无参数；返回当前所有活动区间覆盖的 y 长度，非负且不修改树。
    ll covered() const { return length[1]; }
};

// rectangles 中每个矩形按半开区域解释；返回并集面积，跳过退化矩形。
ll rectangleUnionArea(const vector<Rectangle>& rectangles) {
    struct Event { ll x, y1, y2; int delta; };
    vector<Event> events; vector<ll> ys;
    for (const Rectangle& rec : rectangles) {
        if (rec.x1 >= rec.x2 || rec.y1 >= rec.y2) continue;
        events.push_back({rec.x1, rec.y1, rec.y2, +1});
        events.push_back({rec.x2, rec.y1, rec.y2, -1});
        ys.push_back(rec.y1); ys.push_back(rec.y2);
    }
    if (events.empty()) return 0;
    sort(ys.begin(), ys.end()); ys.erase(unique(ys.begin(), ys.end()), ys.end());
    // lambda 参数是两个事件，返回它们的 x 严格升序关系；同 x 的顺序不影响批量更新。
    sort(events.begin(), events.end(), [](const Event& a, const Event& b) {
        return a.x < b.x;
    });
    CoveredLengthTree tree(ys); ll area = 0, previousX = events.front().x;
    size_t i = 0;
    while (i < events.size()) {
        ll x = events[i].x;
        // 先用旧覆盖长度累积 [previousX,x)，再处理同 x 的所有事件。
        area += tree.covered() * (x - previousX);
        while (i < events.size() && events[i].x == x) {
            tree.update(events[i].y1, events[i].y2, events[i].delta); ++i;
        }
        previousX = x;
    }
    return area;
}
```

**5. 要改哪里**

- 若要计算矩形并周长，单靠根覆盖长度不够，还需维护覆盖段数及左右端覆盖状态，且同一 x 的加入/删除要按周长规则处理。
- 要求输出覆盖次数至少 k 的长度时，把节点摘要从 `cover>0` 的长度扩展为覆盖层数分布。
- 坐标或面积可能超出 `long long` 时，统一将差、乘积、面积改为更宽类型；只改最终返回类型不够。

**6. 自检**

矩形 `[0,2)×[0,2)` 与 `[1,3)×[1,3)` 的并面积为 7；单个矩形面积为宽乘高；空输入和全部退化矩形返回 0。

**7. 坑**

- 叶子代表坐标间隔 `[ys[i],ys[i+1])`，不是坐标点；更新右端点映射到 `index(y2)-1`。
- 面积必须用到达 x 前的覆盖长度乘 `x-previousX`，再处理该 x 的事件。
- 同 x 的事件顺序不影响面积，但不得把边界本身计为正面积。
- 面积乘积可能先溢出再累加；返回类型足够不等于中间乘法安全。

**8. 一句话原理**

按 x 切片累加面积，并在线段树上维护当前被矩形覆盖的 y 间隔总长度。

## 5.27 线段树 + 矩阵乘法 {#matrix-segment-tree}

**1. 它是做什么的**

一串按顺序执行的线性状态转移需要单点修改和区间复合，例如字符 DP、自动机转移或路径计数。矩阵维数 `k` 固定且较小，运算在模数 `MOD` 下进行。
把位置 `i` 的转移矩阵存在线段树叶子，区间查询返回按从左到右顺序复合的总转移；`pointSet` 修改一处转移。
矩阵均为 `k×k`；向量视为列向量，区间 `[l,r]` 的结果是 `M_r⋯M_l`。本节复用 5.15 节的 `PointSegmentTree<T,Merge>`，需先合并该节代码；它要求合并器满足结合律。
复杂度：一次矩阵乘法 $O(k^3)$；建树 $O(nk^3)$，单点修改与区间查询 $O(k^3\log n)$，空间 $O(nk^2)$。若只把一个向量依次应用区间内的矩阵，朴素代价是 $O((r-l+1)k^2)$；若要显式算出整个区间总矩阵，朴素代价才是 $O((r-l+1)k^3)$。

最直接地把一个状态向量逐个应用区间内的矩阵只需 $O((r-l+1)k^2)$，但无法复用多次查询；若需要区间总矩阵，逐个合并是 $O((r-l+1)k^3)$。矩阵乘法满足结合律，因此可以把连续转移压成线段树节点摘要。合并顺序不能写反：左区间先作用，右区间后作用，所以 `merge(left,right)=right*left`。单位矩阵是双侧单位元。

例如状态 `(末位是 0 的方案数, 末位是 1 的方案数)` 在读入一个字符后由一个 `2×2` 矩阵转移；查询 `[l,r]` 得到 `M_r⋯M_l` 后，只需一次矩阵乘列向量。字符规则改变时调用 `tree.pointSet(pos, normalizedMatrix(updated))`，之后用 `tree.rangeQuery(l,r)` 查询新总转移，不必重建整棵树。

**2. 变量在做什么**

| 字段/变量 | 含义 |
|---|---|
| `Matrix::n`、`Matrix::a` | 方阵维数及元素；代码要求维数为正，归一化值位于 `[0,MATRIX_MOD)`。 |
| `identityMatrix(n)` | 线段树空区间的双侧单位元。 |
| `MatrixCompose` | 组合器；`operator()(left,right)` 返回 `right*left`，表示先执行左段再执行右段。 |
| `PointSegmentTree` | 来自 5.15 的通用线段树，存矩阵摘要并提供 `pointSet/rangeQuery`。 |
| `initial` | 1-based 初始转移矩阵数组；位置 0 不参与。 |

**3. 函数在做什么**

| 函数/操作 | 契约 |
|---|---|
| `identityMatrix(n)` | `n>0`；返回 n 阶单位矩阵。 |
| `normalizedMatrix(matrix)` | 正维矩阵按模数归一化后返回副本，不改实参。 |
| `multiplyMatrix(left,right)` | 同阶正维且元素已归一化；返回 `left*right`。 |
| `MatrixCompose::operator()(left,right)` | 同阶矩阵；返回 `right*left`，用于从左到右应用转移。 |
| `matrixRange(initial,l,r)` | 依赖 5.15 的 `PointSegmentTree`；返回区间总转移 `M_r…M_l`。 |
| `replaceAndQuery(tree,pos,updated,l,r)` | 替换 pos 处矩阵并返回新区间总转移；索引及矩阵阶数合法。 |
| `pointSet/rangeQuery` | 通用线段树接口：点赋值、查询闭区间摘要；操作复杂度按 5.15 契约。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
Matrix a(2), b(2);
a.a = {{1, 1}, {0, 1}};
b.a = {{1, 0}, {1, 1}};
vector<Matrix> initial = {Matrix(2), a, b};
MatrixSegmentTree tree(initial, identityMatrix(2), MatrixCompose{});
Matrix product = tree.rangeQuery(1, 2); // b*a
assert((product.a == vector<vector<ll>>{{1, 1}, {1, 2}}));
tree.pointSet(2, identityMatrix(2));
assert(tree.rangeQuery(1, 2).a == a.a);
```


```cpp
// 依赖：先放入 5.15 节的 PointSegmentTree<T, Merge> 定义。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
constexpr ll MATRIX_MOD = 1000000007;

struct Matrix {
    int n;
    vector<vector<ll>> a;
    // n 为正维数时返回 n*n 零矩阵；n=0 仅可作为未初始化占位，不能传给矩阵乘法或线段树。
    explicit Matrix(int n = 0) : n(n), a(n, vector<ll>(n, 0)) {}
};

// n 为正维数；返回 n*n 单位矩阵，作为 PointSegmentTree 的双侧单位元。
Matrix identityMatrix(int n) {
    assert(n > 0);
    Matrix result(n);
    for (int i = 0; i < n; ++i) result.a[i][i] = 1;
    return result;
}

// matrix 维数为正；返回每个元素归一化到 [0,MATRIX_MOD) 的副本，不改变入参。
Matrix normalizedMatrix(Matrix matrix) {
    assert(matrix.n > 0);
    for (auto& row : matrix.a) for (ll& value : row) {
        value %= MATRIX_MOD;
        if (value < 0) value += MATRIX_MOD;
    }
    return matrix;
}

// left/right 为同维数且元素已在 [0,MATRIX_MOD) 的矩阵；返回 left*right，参数不被修改。
Matrix multiplyMatrix(const Matrix& left, const Matrix& right) {
    assert(left.n == right.n && left.n > 0);
    Matrix result(left.n);
    for (int i = 0; i < left.n; ++i)
        for (int k = 0; k < left.n; ++k) if (left.a[i][k])
            for (int j = 0; j < left.n; ++j)
                result.a[i][j] = (result.a[i][j] + left.a[i][k] * right.a[k][j]) % MATRIX_MOD;
    return result;
}

struct MatrixCompose {
    // left/right 同维；返回先作用 left、再作用 right 的列向量转移 right*left。
    Matrix operator()(const Matrix& left, const Matrix& right) const {
        return multiplyMatrix(right, left);
    }
};

// 有序复合树的类型别名，本身不做归一化；构造时 initial[1..n] 必须同维且元素已在模范围内。
using MatrixSegmentTree = PointSegmentTree<Matrix, MatrixCompose>;

// initial[1..n] 为同维数转移矩阵；返回 M_r...M_l 作用于初始列向量的矩阵摘要。
Matrix matrixRange(const vector<Matrix>& initial, int l, int r) {
    assert(l >= 1 && l <= r && r < (int)initial.size());
    vector<Matrix> normalized(initial.size());
    for (int i = 1; i < (int)initial.size(); ++i) normalized[i] = normalizedMatrix(initial[i]);
    MatrixSegmentTree tree(normalized, identityMatrix(normalized[1].n), MatrixCompose{});
    return tree.rangeQuery(l, r);
}

// tree 已用同维数归一化矩阵构造；pos、l、r 合法；替换 pos 后返回新区间 [l,r] 的总转移。
Matrix replaceAndQuery(MatrixSegmentTree& tree, int pos, Matrix updated, int l, int r) {
    tree.pointSet(pos, normalizedMatrix(move(updated)));
    return tree.rangeQuery(l, r);
}
```

**5. 要改哪里**

- 若区间转移次序相反，应同步改 `MatrixCompose` 的乘法顺序，并用两个不交换矩阵验证。
- 若更新字符或状态，替换对应叶矩阵后查询受影响区间；不必重建整个树。
- 若改模数，更新 `MATRIX_MOD` 并确认乘法中间值仍不溢出；当前 `long long` 乘积要求模数范围受控。

**6. 自检**

用两个不交换矩阵 `A,B` 检查区间 `[1,2]` 结果是 `B*A`，不是 `A*B`；单元素区间应返回该叶矩阵，替换一个叶后其余区间查询不变。

**7. 坑**

- 矩阵乘法通常不交换；本代码有意组合为 `right*left`，不可随手交换。
- `PointSegmentTree` 是 5.15 的依赖，单独编译此片段前需合并依赖定义。
- 传入矩阵维数必须一致且元素先归一化；构造时 `initial[1]` 必须存在。
- 模乘中间乘积需能容纳 `MATRIX_MOD` 下两个元素的乘积。

**8. 一句话原理**

矩阵乘法满足结合律，因此可将一段连续状态转移按顺序合并成线段树摘要。

## 5.28 线段树上二分 {#segment-tree-search}

**1. 它是做什么的**

维护可单点修改的数组，并寻找区间中第一个满足某个可剪枝条件的位置。本模板针对“值至少为阈值”，即节点摘要为区间最大值。
`firstAtLeast(l,r,x)` 返回 `[l,r]` 中最小的 `i` 使 `a[i]>=x`，不存在时返回 `-1`；支持 `pointSet`。
初始数组为 1-based 非空数组；区间合法闭区间；返回位置编号或失败哨兵 `-1`。
复杂度：建树 $O(n)$，单点修改 $O(\log n)$，一次寻找 $O(\log n)$（沿少量被截断的节点下降），空间 $O(n)$。

朴素逐项扫描是 $O(n)$。线段树节点保存最大值：若节点完全落在查询区间且最大值小于 `x`，整段都不可能成为答案，可以直接剪枝；否则优先递归左儿子，就能保证返回最左位置。这个方法不是“对下标做普通二分”，因为数组本身不要求有序，二分依赖的是可合并的节点摘要。

手算 `a=[2,-4,7,1,7]`、查询 `[2,5]` 中第一个 `>=7` 的位置：根节点覆盖 `[1,5]` 的最大值足够，但左侧 `[1,3]` 与查询相交，继续看其右端 `[3,3]`，得到位置 `3`；如果查询改为 `[4,5]`，左侧交集 `[4,4]` 的最大值 `1` 不够，才转到 `[5,5]` 返回 `5`。因此数组不需要有序，树上的“整段不可能”摘要才是二分依据。

**2. 变量在做什么**

| 字段/变量 | 含义 |
|---|---|
| `n` | 初始 1-based 数组长度。 |
| `tree[p]` | 节点管理区间的最大值；若小于 `need`，该段不可能有答案。 |
| `initial` | 构造时传入的 1-based 初值，复制到树中。 |
| `ql,qr,need` | 搜索区间闭端点和目标下界。 |
| `pos,value` | `pointSet` 的 1-based 修改位置和值。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `FirstAtLeastTree(initial)` | 非空 1-based 初值；建立区间最大值树，不改输入。 |
| `pointSet(pos,value)` | `pos∈[1,n]`；将该点赋为 value，更新祖先最大值，无返回值。 |
| `firstAtLeast(l,r,need)` | 合法 1-based 闭区间；返回最小的满足 `a[i]>=need` 的位置，无解返回 -1。 |
| `search(p,l,r,ql,qr,need)` | 递归剪枝并优先搜索左儿子；仅供公开查询使用。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<long long> initial = {0, 1, 2, 3, 4, 5};
FirstAtLeastTree tree(initial);
tree.pointSet(3, 8);
int pos = tree.firstAtLeast(2, 5, 7);
assert(pos == 3);
```


```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct FirstAtLeastTree {
    int n;
    vector<ll> tree;

    // initial[1..n] 为非空 1-based 数组；复制并建立区间最大值树，不修改入参。
    explicit FirstAtLeastTree(const vector<ll>& initial) : n((int)initial.size() - 1), tree(4 * n + 4, LLONG_MIN) {
        assert(n >= 1); build(1, 1, n, initial);
    }

    // p 管理 [l,r]；按 initial 建立最大值摘要；返回 void，仅写 tree。
    void build(int p, int l, int r, const vector<ll>& initial) {
        if (l == r) { tree[p] = initial[l]; return; }
        int m = (l + r) / 2;
        build(p * 2, l, m, initial); build(p * 2 + 1, m + 1, r, initial);
        tree[p] = max(tree[p * 2], tree[p * 2 + 1]);
    }

    // pos 为 1..n；value 为替换值；返回 void，更新叶子和祖先最大值。
    void pointSet(int p, int l, int r, int pos, ll value) {
        if (l == r) { tree[p] = value; return; }
        int m = (l + r) / 2;
        if (pos <= m) pointSet(p * 2, l, m, pos, value);
        else pointSet(p * 2 + 1, m + 1, r, pos, value);
        tree[p] = max(tree[p * 2], tree[p * 2 + 1]);
    }

    // p 管理 [l,r]；在交集内寻找最左 >= need 的位置；不存在时返回 -1。
    int search(int p, int l, int r, int ql, int qr, ll need) const {
        if (r < ql || qr < l || tree[p] < need) return -1;
        if (l == r) return l;
        int m = (l + r) / 2;
        int left = search(p * 2, l, m, ql, qr, need);
        return left != -1 ? left : search(p * 2 + 1, m + 1, r, ql, qr, need);
    }

    // pos/value 合法；返回 void，完成单点替换。
    void pointSet(int pos, ll value) { assert(1 <= pos && pos <= n); pointSet(1, 1, n, pos, value); }

    // l,r 合法闭区间；返回区间内最小的满足 a[i]>=need 的位置，不存在返回 -1。
    int firstAtLeast(int l, int r, ll need) const {
        assert(1 <= l && l <= r && r <= n);
        return search(1, 1, n, l, r, need);
    }
};
```

**5. 要改哪里**

- 若查“最后一个满足条件的位置”，改为先搜右儿子再搜左儿子。
- 若摘要为最小值，寻找首个 `a[i]<=x` 时将剪枝条件改为区间最小值仍大于 x。
- 若用区间和找首个前缀达到阈值，必须保证元素非负；有负数时前缀不单调，不能安全剪枝。

**6. 自检**

初值 `{0,2,7,4,9,1}` 查询 `[2,5]`、need=7 应返回 3；改位置 3 为 0 后应返回 5；need=10 无解返回 -1。

**7. 坑**

- 搜索必须先检查当前节点最大值是否小于 need；不满足时下探会失去剪枝收益。
- 先搜左子树才能保证返回最小下标。
- `tree` 以 `LLONG_MIN` 初始化，构造器要求非空数组。
- 区间求和只有在非负元素保证前缀单调时才能做同类搜索。

**8. 一句话原理**

若一个节点的区间最大值仍小于阈值，节点内所有位置都不可能满足条件，可以整段跳过。

## 5.29 倍增 + 单调栈 {#doubling-monotone-stack}

**1. 它是做什么的**

静态数组上反复询问“从位置 `i` 开始沿下一个更大元素跳 `k` 次”。本节使用严格更大关系 `a[next]>a[i]`；数组不修改。
预处理每个位置的 next greater element，再用倍增在 $O(\log k)$ 内回答第 `k` 个更大元素位置。
数组 1-based；不存在的跳转为 `0`，起点越界或 `k<=0` 返回 `0`；`firstGreaterWithin` 的右界须由调用方保证不超过 `n`。`k` 用 `long long` 表示。
复杂度：单调栈预处理 $O(n)$，倍增表 $O(n\log n)$，每次查询 $O(\log k)$，空间 $O(n\log n)$。

对每个位置向右扫描并寻找第一个更大值，单次可能 $O(n)$。从右往左维护一个单调递减候选栈：小于等于当前值的候选永远不会成为当前点或更左点的 next greater，直接弹出。得到 `up[0][i]` 后，`up[j][i]=up[j-1][up[j-1][i]]`，二进制拆分 `k` 即可跳跃。这里的 `kthGreater(i,k)` 是后继链上的第 `k` 次跳转，不是区间第 `k` 大；若只问 `[i+1,r]` 内第一个严格大于 `a[i]` 的位置，只需取 `up[0][i]` 并检查它是否不超过 `r`。若阈值是独立给出的 `x`，则应另维护区间最大值树：从左到右剪枝最大值小于 `x` 的节点，定位 `[l,r]` 中第一个 `a[j]>=x`，这正是 5.28 的组合。

**2. 变量在做什么**

| 字段/变量 | 含义 |
|---|---|
| `n` | 1-based 数组长度。 |
| `log` | 倍增层数，表下标为 `0..log-1`；链上最多有 `n-1` 次有效跳转。 |
| `up[j][i]` | 从 i 沿 next-greater 链跳 `2^j` 次的位置；0 表示链已断。 |
| `mono` | 从右往左扫描时的单调栈，保存可能成为 next greater 的下标。 |
| `start,k,right` | 起点、正跳数和查询右边界；`k` 为 `long long`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `NextGreaterDoubling(a)` | 非空 1-based 静态数组；构造严格更大后继和倍增表，不改输入。 |
| `kthGreater(start,k)` | start 合法、k 为正；返回后继链第 k 次跳转位置；非法起点或不存在返回 0。 |
| `firstGreaterWithin(start,right)` | 返回 `[start+1,right]` 内首个严格大于 `a[start]` 的位置；不存在返回 0。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<long long> a = {0, 2, 1, 4, 3, 5};
NextGreaterDoubling jumps(a);
int first = jumps.firstGreaterWithin(1, 4);
int second = jumps.kthGreater(1, 2);
assert(first == 3 && second == 5);
```


```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct NextGreaterDoubling {
    int n, log;
    vector<vector<int>> up;

    // a[1..n] 为静态非空数组；建立严格更大元素的 next 指针和倍增表，不修改 a。
    explicit NextGreaterDoubling(const vector<ll>& a) : n((int)a.size() - 1), log(1) {
        assert(n >= 1);
        while ((1LL << log) <= n) ++log;
        up.assign(log, vector<int>(n + 1, 0));
        vector<int> mono;
        for (int i = n; i >= 1; --i) {
            while (!mono.empty() && a[mono.back()] <= a[i]) mono.pop_back();
            up[0][i] = mono.empty() ? 0 : mono.back();
            mono.push_back(i);
        }
        for (int j = 1; j < log; ++j)
            for (int i = 1; i <= n; ++i)
                up[j][i] = up[j - 1][up[j - 1][i]];
    }

    // start 为 1..n，k 为正跳数；返回第 k 个严格更大元素的位置，不存在返回 0。
    int kthGreater(int start, ll k) const {
        if (start < 1 || start > n || k <= 0) return 0;
        int node = start;
        for (int bit = 0; k > 0 && node != 0; ++bit, k >>= 1)
            if (k & 1) node = bit < log ? up[bit][node] : 0;
        return node;
    }

    // start 为 1..n，right 为不小于 start 的右边界；返回 [start+1,right] 内第一个 >a[start] 的位置，否则返回 0。
    int firstGreaterWithin(int start, int right) const {
        if (start < 1 || start > n || right <= start) return 0;
        int next = up[0][start];
        return next != 0 && next <= right ? next : 0;
    }
};
```

**5. 要改哪里**

- 要求“下一个大于等于”时，构栈弹出条件需从 `<=` 改为 `<`，并验证重复值链。
- 若只需单次 next greater 查询，不必建倍增表，单调栈的 `up[0]` 已足够。
- 若问独立阈值 x 在 `[l,r]` 的首个满足位置，本节按跳数查询的接口不能直接回答；可使用 5.28 的区间最大值剪枝，或另设计按值判断的后继链倍增查询。

**6. 自检**

数组 `{0,2,1,4,3,5}` 中 `firstGreaterWithin(1,4)==3`，`kthGreater(1,2)==5`；严格关系下从值 4 不会跳到相等值 4。

**7. 坑**

- 严格更大使用弹栈条件 `<=`；改成 `<` 后语义会包含相等值。
- `up[0][i]` 是下一个更大位置，不是更大值；哨兵 0 不能当数组下标访问。
- `kthGreater` 沿后继链跳 k 次，不等同于区间第 k 大。
- `firstGreaterWithin` 的 `right` 必须是有效数组边界。

**8. 一句话原理**

单调栈找出每个位置的一步更大后继，倍增表将后继链上的多步跳跃拆成二进制块。

## 5.30 可撤销并查集 {#rollback-dsu}

**1. 它是做什么的**

需要在一条递归或离线时间线中反复“临时合并、回到某个历史时刻”的无向连通性问题。只支持合并与回滚，不支持路径压缩。
`unite(u,v)` 合并两个集合，`snapshot()` 记下当前时间点，`rollback(s)` 恢复到快照时的分量数和父子关系；重复边若两端已连通会被记录为无效操作，从而仍可按操作次数回滚。
点编号为 `1..n`；快照是内部修改记录栈的大小，必须来自当前对象且按后进先出回滚。`same` 查询不改变状态。
复杂度：按大小合并后 `find` 和一次成功 `unite` 为 $O(\log n)$，`snapshot` 为 $O(1)$；`rollback(s)` 的时间是实际弹出的记录数，每条记录恢复为 $O(1)$，不能把整次回滚都写成 $O(\log n)$。空间 $O(n+q)$（每次尝试合并最多一条记录）。

普通并查集的路径压缩会改动很多父指针，回滚时必须保存这些变化，代价和实现复杂度都会变高。因此这里明确禁止路径压缩，只按集合大小挂接根；一次 `unite` 最多改变一个根和一个集合大小。快照就是“修改栈的长度”，回滚弹出记录并反向恢复。

**2. 变量在做什么**

| 字段 | 含义 |
|---|---|
| `parent[x]` | 并查集父指针；根满足 `parent[x]==x`。 |
| `size[root]` | 根所代表集合的大小，只对根有意义。 |
| `history` | 每次 `unite` 一条记录；成功记录旧根大小，失败记录 `merged=false`。 |
| `components` | 当前连通分量数。 |
| `Change` | `child`、被挂接的 `parentRoot`、合并前 `oldSize` 及是否成功。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `RollbackDSU(n)` | n>=1；初始化 1..n 为单点集合。 |
| `find(x)` | 合法点；返回根，不压缩路径、不修改状态。 |
| `snapshot()` | 返回当前 history 长度，作为不透明快照。 |
| `unite(u,v)` | 合法点；尝试合并并记录一条历史；返回是否合并成功。 |
| `rollback(snap)` | snap 必须是当前或更早有效快照；撤销到该历史长度，恢复分量数。 |
| `same(u,v)` | 合法点；返回是否连通，不改结构。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
RollbackDSU dsu(4);
int snap = dsu.snapshot();
dsu.unite(1, 2);
bool connected = dsu.same(1, 2);
assert(connected);
dsu.rollback(snap);
assert(!dsu.same(1, 2));
```


```cpp
#include <bits/stdc++.h>
using namespace std;

struct RollbackDSU {
    struct Change { int child, parentRoot, oldSize; bool merged; };
    vector<int> parent, size;
    vector<Change> history;
    int components;

    // n 个点编号为 1..n；初始化 n 个单点集合，要求 n>=1。
    explicit RollbackDSU(int n) : parent(n + 1), size(n + 1, 1), components(n) {
        assert(n >= 1);
        iota(parent.begin(), parent.end(), 0);
    }

    // x 为 1..n；返回根。禁止路径压缩，以保证 history 能完整撤销。
    int find(int x) const {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    // 无参数；返回当前 history 长度，作为之后 rollback 的不透明时间点。
    int snapshot() const { return (int)history.size(); }

    // u,v 为合法点；返回是否真的合并了两个分量，并为每次尝试写入一条可回滚记录。
    bool unite(int u, int v) {
        int ru = find(u), rv = find(v);
        if (ru == rv) { history.push_back({0, 0, 0, false}); return false; }
        if (size[ru] < size[rv]) swap(ru, rv);
        history.push_back({rv, ru, size[ru], true});
        parent[rv] = ru; size[ru] += size[rv]; --components;
        return true;
    }

    // snap 必须是当前或更早的 snapshot；返回 void，撤销至该时间点并恢复 components。
    void rollback(int snap) {
        assert(0 <= snap && snap <= (int)history.size());
        while ((int)history.size() > snap) {
            Change change = history.back(); history.pop_back();
            if (!change.merged) continue;
            parent[change.child] = change.child;
            size[change.parentRoot] = change.oldSize;
            ++components;
        }
    }

    // u,v 为合法点；返回当前是否连通，不修改父树或 history。
    bool same(int u, int v) const { return find(u) == find(v); }
};
```

**5. 要改哪里**

- 若上层需要每次尝试都能按次数回滚，保留失败合并的空记录；删除该记录时，上层快照仍可用，但快照语义变为历史修改数而非尝试数。
- 若要维护额外集合摘要（如点权和），需在成功合并记录旧摘要并在 rollback 中恢复。
- 需要在线路径压缩并查集时，不适合本结构；路径压缩会产生多处需记录的父指针变化。

**6. 自检**

4 个点先取快照，合并 1-2、2-3 后 `same(1,3)` 为真且分量数为 2；回滚快照后该查询为假、分量数为 4。重复合并也应能完整回滚。

**7. 坑**

- 不能做路径压缩，否则 `rollback` 没有记录那些被压缩的父指针。
- 快照是 history 长度，必须来自同一对象且不得大于当前长度。
- 快照后的修改必须按后进先出回滚；不能保留后续状态再回滚到更早快照。
- `find/same` 仅在点编号合法时安全；代码不会逐点检查范围。

**8. 一句话原理**

只按大小合并且不压缩路径，使每次合并只需记录少量字段便能按历史逆序恢复。

## 5.31 线段树分治（动态连通性） {#segment-tree-offline}

**1. 它是做什么的**

离线处理一组按时间编号的加边、删边、连通性查询；边的存在状态随时间变化，但查询只问无向图当前是否连通。使用 5.30 的可撤销并查集思想。
把每条边的活跃时间段放入时间线线段树，DFS 到节点时暂时加入该节点覆盖的边，叶子回答该时刻查询，返回父节点前回滚。
`Operation` 的 `A` 表示加边、`D` 表示删边、`?` 表示查询；时间是 `0..q-1` 的操作下标。删除匹配同一无向边最近一次尚未删除的添加（LIFO）；没有活跃实例的删除被忽略；重复添加是多个独立实例。返回按查询出现顺序排列的布尔值。
复杂度：若有 `q` 个操作、最终形成 `s` 个活跃时间区间，每条区间进入 $O(\log(q+1))$ 个树节点；配对操作的 `map` 扫描为 $O(q\log(q+1))$。总时间安全上界为 $O(q\log(q+1)+s\log(q+1)\log(n+1)+q\log(n+1))$，空间 $O(q+s\log(q+1)+n)$；其中 DSU 的对数来自按大小合并的树高，回滚本身按实际弹出记录数计费。

### 时间区间和删除语义

一条边在时刻 `add` 加入、在时刻 `del` 删除，因此只影响半开时间区间 `[add,del)`；若一直未删除，则是 `[add,q)`。在每个线段树节点保存完全覆盖该节点时间区间的边，递归进入节点时调用 `unite`。到叶子时状态正好等于该时刻所有活跃边，回答后回滚。

删除必须先明确语义，否则重复边会产生歧义。本实现采用“最近添加的未删除实例”匹配：`A(1,2), A(1,2), D(1,2)` 只关闭第二条，第一条仍活跃。端点规范化为 `(min(u,v),max(u,v))`，所以反向写的边也视作同一无向边。区间端点按半开处理，`add==del` 的空区间不进入线段树。

**2. 变量在做什么**

| 字段/变量 | 含义 |
|---|---|
| `Operation` | 单个时间点操作：`type` 为 `A`、`D` 或 `?`，`u,v` 是 1..n 端点。 |
| `operations` | 按时间下标 0..q-1 保存的输入操作。 |
| `tree[p]` | 时间线线段树节点所负责时段内始终活跃的边。 |
| `answers` | 依查询出现顺序写入的 0/1 连通结果；每次 `run()` 前清空。 |
| `dsu` | 依赖 5.30 的无路径压缩可撤销并查集。 |
| `starts` | 构造阶段按规范化无向边保存未删除添加时刻的栈。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `OfflineDynamicConnectivity(n, operations)` | n>=1；复制操作，端点须在 1..n，按时间构造边活跃区间树。 |
| `normalized(u,v)` | 返回 `(min(u,v),max(u,v))`，把反向无向边归一。 |
| `buildIntervals()` | 内部配对 A/D，按半开活跃时段写入时间线树；无匹配删除忽略。 |
| `addInterval(...)` | 把边加入完全覆盖的节点；时段采用 `[ql,qr)`。 |
| `solve(p,l,r)` | 临时合并节点边，叶子处理 `?`，返回前回滚；内部递归。 |
| `run()` | 清空结果并从 DSU 初态执行；返回按时间顺序排列的 `vector<int>` 查询答案，可重复调用。 |

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<Operation> ops = {{'A', 1, 2}, {'?', 1, 2}, {'D', 1, 2}};
OfflineDynamicConnectivity solver(3, ops);
vector<int> answers = solver.run();
assert(answers.size() == 1 && answers[0] == 1);
```


```cpp
// 依赖：先放入 5.30 节的 RollbackDSU；本节不重复定义它。
#include <bits/stdc++.h>
using namespace std;

struct Operation { char type; int u, v; };

struct OfflineDynamicConnectivity {
    struct Edge { int u, v; };
    int n, q;
    vector<Operation> operations;
    vector<vector<Edge>> tree;
    vector<int> answers;
    RollbackDSU dsu;

    // operations 按下标 0..q-1 给出；端点为 1..n；复制操作并构造时间线树。
    OfflineDynamicConnectivity(int n, vector<Operation> operations)
        : n(n), q((int)operations.size()), operations(move(operations)), tree(4 * max(1, q) + 4), dsu(n) {
        assert(n >= 1);
        buildIntervals();
    }

    // 无向边规范化；返回按字典序排列的端点，便于把反向边当作同一实例栈。
    pair<int, int> normalized(int u, int v) const { return {min(u, v), max(u, v)}; }

    // 把边 e 加到时间树中完全覆盖 [ql,qr) 的节点；空区间直接忽略。
    void addInterval(int p, int l, int r, int ql, int qr, Edge e) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { tree[p].push_back(e); return; }
        int m = (l + r) / 2;
        addInterval(p * 2, l, m, ql, qr, e);
        addInterval(p * 2 + 1, m, r, ql, qr, e);
    }

    // 扫描 A/D 操作，按 LIFO 配对重复边并生成每条边的半开活跃时间区间。
    void buildIntervals() {
        if (q == 0) return;
        map<pair<int, int>, vector<int>> starts;
        for (int t = 0; t < q; ++t) {
            if (operations[t].type == 'A') {
                starts[normalized(operations[t].u, operations[t].v)].push_back(t);
            } else if (operations[t].type == 'D') {
                auto key = normalized(operations[t].u, operations[t].v);
                auto it = starts.find(key);
                if (it != starts.end() && !it->second.empty()) {
                    int begin = it->second.back(); it->second.pop_back();
                    addInterval(1, 0, q, begin, t, {key.first, key.second});
                }
            }
        }
        for (const auto& item : starts) for (int begin : item.second)
            addInterval(1, 0, q, begin, q, {item.first.first, item.first.second});
    }

    // DFS 时间树节点 [l,r)；进入时加入全部边，离开时回滚，叶子按操作回答查询。
    void solve(int p, int l, int r) {
        int snap = dsu.snapshot();
        for (const Edge& edge : tree[p]) dsu.unite(edge.u, edge.v);
        if (r - l == 1) {
            const Operation& op = operations[l];
            if (op.type == '?') answers.push_back(dsu.same(op.u, op.v));
        } else {
            int m = (l + r) / 2;
            solve(p * 2, l, m); solve(p * 2 + 1, m, r);
        }
        dsu.rollback(snap);
    }

    // 无参数；返回按时间顺序排列的查询结果；可重复调用且每次从空 DSU 状态重新 DFS。
    vector<int> run() {
        answers.clear(); dsu.rollback(0);
        if (q > 0) solve(1, 0, q);
        return answers;
    }
};
```

**5. 要改哪里**

- 若删除匹配最早尚未删除的添加实例，把每条边的起点容器从栈改为队列，并按 FIFO 取出。
- 若要回答组件大小等问题，可扩展 5.30 的 DSU 查询与回滚记录；时间区间分解框架保持不变。
- 若查询要求在线回答，未来操作尚未知，无法预先构造活跃时间段，应选择在线动态连通结构。

**6. 自检**

操作序列 A(1,2), ?(1,2), D(1,2), ?(1,2) 的答案应为 `{1,0}`；空操作列表 `run()` 返回空向量；重复添加后删除一次，另一个实例仍活跃。

**7. 坑**

- 时间区间是半开 `[add,del)`；删除时刻不再包含该边，添加时刻已包含。
- 重复边按规范化端点和 LIFO 实例配对；未匹配删除被忽略。
- 类型为 `?` 的操作必须提供合法 u、v；无关字段虽不读取，也应初始化。
- `run()` 会重置答案并回滚 DSU；不要在递归 DFS 中使用带路径压缩的 DSU。
- 空操作列表不会调用 `solve`，因此时间线根上的空区间不会被访问。

**8. 一句话原理**

把边的活跃时间段分解到时间线线段树节点，DFS 子树期间临时合并，离开时回滚。

## 5.32 P2 进阶：树上莫队、Segment Tree Beats 与 LCT {#advanced-data-structure-guide}

**适用范围：** 已掌握 P0/P1，希望识别更复杂的离线路径、区间最值修改和在线动态森林模型。**能做什么：** 本节讲清三个专题的入门模型、关键不变量、手算例子和学习边界；可撤销并查集与线段树分治的完整实现见 5.30、5.31。**输入 / 输出：** 三者分别输入静态树路径询问、数组最值修改、森林连删边操作，输出路径统计、区间摘要或动态路径答案。这里提供推导和学习指引，不提供可直接提交的这三个进阶模板；下面的复杂度仅对应明确列出的标准版本。

### 树上莫队：为什么树路径能变成区间

普通莫队维护数组窗口；树路径的点在“每点只记录一次”的 DFS 序上通常不连续。改成每个点进入时和退出时各记一次，得到长度 $2n$ 的括号序。窗口中的同一个点出现两次，就把它视为抵消；只保留出现奇数次的点。每次指针经过一个点 `x`，根据 `active[x]` 加入或删除其颜色，再翻转标志。这是集合的奇偶抵消，不能把序列中两次出现当成两个独立点。

设 `tin[u]`、`tout[u]` 分别是两次出现的位置，并先交换端点使 `tin[u]<=tin[v]`。令 `z=LCA(u,v)`：

- 若 `z=u`，窗口取 `[tin[u],tin[v]]`，奇数次出现的点恰好是路径。
- 否则取 `[tout[u],tin[v]]`，奇数次出现的点是路径去掉 `z`；回答时临时加入 `z`，读取答案后立刻删除。

手算树边 `1-2,1-3,2-4`，一种括号序为 `[1,2,4,4,2,3,3,1]`。路径 `4→2→1→3` 使用位置 `[4,6]`，看到 `[4,2,3]`，补上 LCA=1 即完整路径。路径 `2→4` 用 `[2,3]`，已经包含两个端点，不再额外补 LCA。

先用倍增预处理 LCA，莫队排序和移动仍在长度 $2n$ 的数组上进行。单点增删 $O(1)$、块长约 $\sqrt n$ 时，总时间为 $O(n\log n+q\log q+q\log n+(n+q)\sqrt n)$，空间 $O(n\log n+q)$；改变增删代价要相应乘上该代价。它适合静态路径不同数、频率平方和等可增删状态；有颜色修改需要再加时间维度，树结构本身改动则此序列会失效。

基础练习先画括号序并人工验证窗口；实现练习把普通莫队的 `add/remove` 改成 `toggle`；组合练习统计路径颜色对数，针对祖先端点、相同端点、跨根路径和补 LCA 后状态恢复做暴力对拍。参考 [OI Wiki：树上莫队](https://oi-wiki.org/misc/mo-algo-on-tree/)。

### Segment Tree Beats：摘要不足时何时可以直接修改

考虑操作 `a[i]=min(a[i],x)`，即把太大的数压到上限 `x`，并查询区间和。只有 `sum` 和最大值无法判断和减少多少；同样总和与最大值的两个区间可能有不同数量的最大元素。即便有最大值个数，当多个不同数都被压低时，仍不能直接知道变化。

标准的单向 `chmin + sum` 版本在每个节点维护总和 `sum`、最大值 `mx1`、严格次大值 `mx2`、最大值个数 `cnt`。次大值必须是**不同于最大值的第二大值**，全相等区间用负无穷哨兵。覆盖节点后分三种情况：

1. `x>=mx1`：没有数受影响，立即返回。
2. `mx2<x<mx1`：只有最大值变化，`sum -= (mx1-x)*cnt`，再令 `mx1=x`。
3. `x<=mx2`：仅靠这四个字段无法同时更新合并后的最大值个数和次大值，继续递归孩子。

例如 `[8,8,5,2]` 的摘要为 `(23,8,5,2)`。压到 6 时，和变成 19，最大值为 6、个数仍为 2；再压到 5，最大值个数会由 2 变成 3，不能复用“只改最大值”的公式。向下访问前，要把父亲的上限约束应用到最大值超标的孩子，再合并孩子摘要。

“Beats” 的关键是对递归失败次数做摊还分析。不能声称每一次区间压低都是 $O(\log n)$。仅含区间 `chmin` 与求和/最值的标准版本有 $O((n+q)\log n)$ 的总时间界、$O(n)$ 空间；加入 `chmax`、区间加、历史最值后，字段、标记和证明都变化，不能沿用这里的结论。非空数组、哨兵与合法值不冲突、乘积和总和不溢出也是必要前提。

入门先写暴力压低；再用例子证明为何需要严格次大值；最后实现单向版本并重点对拍全相等、`x=mx1`、`x=mx2`、负数和反复收紧。区间取模等“修改让某个量快速下降”的题也可能用势能分析，但不是直接复制此模板。参考 [OI Wiki：区间最值操作](https://oi-wiki.org/ds/seg-beats/)。

### Link-Cut Tree：树的边也在变化时

HLD 预先确定重儿子和 DFS 位置，删边连边会使这一划分失效。LCT 面向在线动态森林，常见基础任务是 `link(u,v)` 连边、`cut(u,v)` 删现有边、点权修改、路径和或异或查询。它要求图始终是森林：连接已连通的两点会制造环，必须拒绝；删边也必须确认两点直接相邻。

LCT 用若干棵 Splay 辅助树表示原森林的一些路径；辅助树的父子关系不等于原树的父子关系。`access(v)` 将通往 `v` 的路径组织成可查询的辅助结构；`makeRoot(u)` 暴露路径并打翻转标记，使 `u` 成为表示上的根。执行 `makeRoot(u)`、`access(v)`、`splay(v)` 后，`v` 的辅助树摘要对应原树 `u→v` 路径。翻转会交换左右孩子；非交换摘要要同时保存正向与反向值。

例如森林有边 `1-2,2-3`，点权 `[4,7,1]`，路径 1 到 3 的和为 12。删除 `2-3` 后，1 与 3 不连通，不能继续查询一条不存在的路径；再连 `1-3`，路径 2 到 3 变为 `2→1→3`，和仍为 12，而路径 1 到 3 的和变为 5。

标准 Splay 型 LCT 的连边、断边、暴露路径及路径查询为摊还 $O(\log n)$，单次不保证最坏 $O(\log n)$，空间 $O(n)$。先学 Splay 的旋转、伸展、下传再旋转，之后逐项实现 LCT。任意图动态连通性不等于动态森林；子树信息也不能直接当成路径摘要，需要另外处理虚子树贡献。

基础练习手算原树与辅助树的区别；实现练习先只做路径异或，随机连删合法森林边与 BFS 暴力对拍；组合练习再加路径懒标记。若全部操作离线且只查连通性，先考虑 5.31；若树边不变，先确认 HLD 是否已经足够。参考 [OI Wiki：Link Cut Tree](https://oi-wiki.org/ds/lct/)。
