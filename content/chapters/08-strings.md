
# 8. 字符串

本章字符串统一使用 0-based 下标，区间统一写成左闭右开 `[l,r)`。长度为 `n` 的字符串合法字符下标为 `0..n-1`；各模板用 `int` 保存长度和下标，因此输入长度及下标表达式必须可由 `int` 表示。未特别说明时字符按字节处理，不直接支持 UTF-8 的“单个汉字”语义。

## 8.1 字符串哈希

**适用范围：** 字节串的子串快速判等，使用 0-based 半开区间；固定双哈希仍可能碰撞，不适用于要求零误判或可被刻意构造的输入。
**能做什么：** `StringHash` 预处理 $O(n)$、占 $O(n)$ 空间；每次子串哈希 $O(1)$。
**输入 / 输出：** `StringHash(s)` 保存输入串的前缀表；`get(l,r)` 要求 `0<=l<=r<=|s|`，返回 `s[l..r)` 双哈希，空串区间返回 (0,0)。

**用法：**

- 构造 `StringHash(s)` 后，`get(l,r)` 返回 `s[l..r)` 的双哈希。
- 两个子串只有长度相等且哈希相等时才判为相同。
- 同一对象内或使用相同底数、模数的对象间可以比较。
- 对抗性强或必须零误判的题，应改用 KMP、后缀结构或直接校验。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct StringHash {
    // 两个模数与 BASE 必须在所有待比较对象中完全一致；哈希相等仍有极小碰撞概率。
    static constexpr ll MOD1 = 1000000007;
    static constexpr ll MOD2 = 1000000009;
    static constexpr ll BASE = 911382323;
    vector<ll> h1, h2, p1, p2;

    // 参数 s 按字节读取；构造并拥有前缀哈希与幂数组，不修改 s。
    explicit StringHash(const string& s) {
        int n = (int)s.size();
        // h[i] 表示前缀 s[0..i) 的哈希，p[i]=BASE^i；两数组都按长度而非字符下标。
        h1.assign(n + 1, 0); h2.assign(n + 1, 0);
        p1.assign(n + 1, 1); p2.assign(n + 1, 1);
        // 每轮把一个字节扩展进两个前缀哈希，并同步预存下一次查询所需的幂。
        for (int i = 0; i < n; ++i) {
            int value = (unsigned char)s[i] + 1;
            h1[i + 1] = (h1[i] * BASE + value) % MOD1;
            h2[i + 1] = (h2[i] * BASE + value) % MOD2;
            p1[i + 1] = p1[i] * BASE % MOD1;
            p2[i + 1] = p2[i] * BASE % MOD2;
        }
    }

    // 返回 0-based 左闭右开子串 s[l..r) 的双哈希；要求 0<=l<=r<=s.size()。
    // 参数是 s 的 0-based 半开区间 [l,r)；返回双模哈希，调用者须保证边界合法；不改状态。
    pair<ll, ll> get(int l, int r) const {
        // h[r]-h[l]*BASE^(r-l) 消掉左侧前缀，使不同起点的等长子串可直接比较。
        ll x1 = (h1[r] - h1[l] * p1[r - l]) % MOD1;
        ll x2 = (h2[r] - h2[l] * p2[r - l]) % MOD2;
        if (x1 < 0) x1 += MOD1;
        if (x2 < 0) x2 += MOD2;
        return {x1, x2};
    }
};
```

**易错点：**

1. 比较哈希前必须比较子串长度。
2. 区间是 `[l,r)`，幂次应为 `r-l`。
3. 哈希相等不构成数学上的绝对相等，不能忽视碰撞要求。

**参考：**

- [OI Wiki：字符串哈希](https://oi-wiki.org/string/hash/)

## 8.2 前缀函数与 KMP

**适用范围：** 在字节字符串中找模式串的所有出现，支持重叠；空模式按本模板约定返回空列表。
**能做什么：** `prefixFunction` 和 KMP 匹配总时间 $O(n+m)$，前缀表空间 $O(m)$。
**输入 / 输出：** `prefixFunction(s)` 返回每个字符位置的最长相等真前后缀长度；`kmpSearch(text,pattern)` 返回 0-based 起点升序列表，不改动输入。

**用法：**

- `prefixFunction(pattern)` 返回长度为 `m` 的 `pi`，且 `pi[0]=0`。
- `kmpSearch(text,pattern)` 返回模式串在文本中的所有 0-based 起点。
- 模板保留重叠匹配，例如 `"aaa"` 中 `"aa"` 的位置为 0、1。
- 空模式串的定义因题而异，模板直接返回空结果。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数 s 是字节串；返回与 s 等长的 pi 长度数组，空串返回空数组，不改输入。
vector<int> prefixFunction(const string& s) {
    int n = (int)s.size();
    // pi[i] 是 s[0..i] 的最长相等真前后缀“长度”，不是末尾下标。
    vector<int> pi(n, 0);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        // 失配后只可能尝试当前边界的次长边界；因此跳 pi[j-1]，文本位置 i 不回退。
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    return pi;
}

// 参数 text/pattern 是字节串；返回 pattern 的全部 0-based 起点（含重叠），空模式返回空表。
vector<int> kmpSearch(const string& text, const string& pattern) {
    // 返回 pattern 在 text 中所有 0-based 起点；空模式的语义由题目决定，这里返回空。
    vector<int> positions;
    if (pattern.empty()) return positions;
    vector<int> pi = prefixFunction(pattern);
    // 扫描 text[0..i] 前，j 表示已匹配的 pattern 前缀长度，始终有 0<=j<m。
    int j = 0;
    for (int i = 0; i < (int)text.size(); ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) ++j;
        if (j == (int)pattern.size()) {
            positions.push_back(i - j + 1);
            // 匹配后回到最长真边界，才能继续寻找允许重叠的下一次出现。
            j = pi[j - 1];
        }
    }
    return positions;
}
```

**易错点：**

1. `pi[i]` 存的是长度，不是末尾下标。
2. 失配回退写 `pi[j-1]`，不能写 `pi[j]`。
3. 找到一次匹配后仍要回退，才能找到重叠出现。

**参考：**

- [OI Wiki：前缀函数与 KMP 算法](https://oi-wiki.org/string/kmp/)

## 8.3 Z 函数（扩展 KMP）

**适用范围：** 求字符串各后缀与整串的 LCP，或匹配字节串；匹配时分隔符必须不存在于两输入串。
**能做什么：** `zFunction` 与 Z 匹配均为线性时间，空间 $O(n+m)$。
**输入 / 输出：** `zFunction(s)` 返回长度 `|s|` 的数组，`z[0]=|s|`（空串为空数组）；`zSearch(text,pattern)` 返回所有 0-based 起点，空模式返回空列表。

**用法：**

- 调用 `zFunction(s)` 获得每个后缀与整串的 LCP 长度。
- 匹配 `pattern` 与 `text` 时，可计算 `pattern + '#' + text` 的 Z 数组。
- 分隔符必须是不出现在两个原串中的单个字符。
- 拼接后位置 `m+1+i` 的 Z 值至少为 `m`，表示文本位置 `i` 匹配。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数 s 是字节串；返回各位置的 Z 长度，非空时 z[0]=|s|，空串返回空数组。
vector<int> zFunction(const string& s) {
    int n = (int)s.size();
    // z[i]=LCP(s, s[i..n))；所有字符与区间均为 0-based、左闭右开。
    vector<int> z(n, 0);
    if (n == 0) return z;
    z[0] = n;
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        // [l,r) 是目前右端点最远的前缀匹配段，且 s[l..r)==s[0..r-l)。
        // i 在盒内时先复用镜像 z[i-l]，但不能越过尚未验证的右端点 r。
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
        if (i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    return z;
}

// 参数 text/pattern 为字节串且均不含 '\0' 分隔符；返回 0-based 匹配起点，空模式返回空表。
vector<int> zSearch(const string& text, const string& pattern) {
    // 返回所有 0-based 起点；若字符集可能含 '\0'，需把分隔符换成确定不存在的值。
    vector<int> positions;
    if (pattern.empty()) return positions;
    string joined = pattern + '\0' + text;
    vector<int> z = zFunction(joined);
    int m = (int)pattern.size();
    // joined 中 text[i] 的下标是 m+1+i；z 值至少为 m 才覆盖整个模式串。
    for (int i = 0; i < (int)text.size(); ++i)
        if (z[m + 1 + i] >= m) positions.push_back(i);
    return positions;
}
```

**易错点：**

1. 本模板维护的是左闭右开区间 `[l,r)`，判断条件是 `i < r`。
2. 不同资料对 `z[0]` 定义不同，使用前先统一。
3. 若输入可能含 `\0`，拼接时应换用确定不存在的分隔符或整数数组。

**参考：**

- [OI Wiki：Z 函数（扩展 KMP）](https://oi-wiki.org/string/z-func/)

## 8.4 Manacher

**适用范围：** 单个字节串的所有奇/偶长度回文中心半径；空串可输入。
**能做什么：** Manacher 在线性 $O(n)$ 时间、$O(n)$ 空间得到奇偶半径。
**输入 / 输出：** `manacher(s)` 返回两个与 `s` 等长数组；`odd[i]` 含中心，`even[i]` 对应缝隙 `i-1|i`，空串返回两空数组。

**用法：**

- 最长奇回文长度为 `2*odd[i]-1`，区间为 `[i-odd[i]+1, i+odd[i])`。
- 最长偶回文长度为 `2*even[i]`，区间为 `[i-even[i], i+even[i])`。
- 全局最长值取所有上述长度的最大值。
- 判断 `[l,r)` 是否回文，可按奇偶长度找到中心并检查对应半径。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct ManacherResult {
    // odd/even 均以原串 0-based 字符位置为中心索引，数值是单侧半径而非总长度。
    vector<int> odd, even;
};

// 参数 s 是字节串；返回等长 odd/even 半径数组，空串对应两个空数组，不改输入。
ManacherResult manacher(const string& s) {
    int n = (int)s.size();
    vector<int> odd(n), even(n);

    for (int i = 0, l = 0, r = -1; i < n; ++i) {
        // [l,r] 是当前最右奇回文；盒内位置先复用关于中心的镜像半径。
        int k = (i > r ? 1 : min(odd[l + r - i], r - i + 1));
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) ++k;
        odd[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    for (int i = 0, l = 0, r = -1; i < n; ++i) {
        // even[i] 的中心是缝隙 i-1|i；镜像下标因此比奇回文多一个 +1。
        int k = (i > r ? 0 : min(even[l + r - i + 1], r - i + 1));
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) ++k;
        even[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
    return {odd, even};
}
```

**易错点：**

1. 奇半径含中心，最小为 1；偶半径可为 0。
2. `even[i]` 的中心是 `i-1` 与 `i` 之间，不是字符 `i`。
3. 半径不是回文总长度，输出前需按奇偶换算。

**参考：**

- [OI Wiki：Manacher](https://oi-wiki.org/string/manacher/)

## 8.5 Trie 字典树

**适用范围：** 仅由小写 ASCII 字母构成的字符串多重集合，需前缀或精确计数。
**能做什么：** Trie 插入、完整词计数、前缀计数均为 $O(L)$；空间为已分配节点数乘 26。
**输入 / 输出：** `insert(s)` 修改 Trie 并累计重复次数；`countWord/countPrefix` 返回次数，`findNode` 返回节点号或 `-1`。空串在根节点计数；输入字符必须为 a-z。

**用法：**

- `insert(s)` 插入一个小写串，并保留重复次数。
- `countWord(s)` 返回该完整字符串插入次数。
- `countPrefix(p)` 返回以 `p` 为前缀的已插入字符串数。
- 其他字符集可改 `array<int,26>` 的大小与 `id` 映射。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Trie {
    struct Node {
        // next[c]=0 表示无边；根恰为 0，所以实际新节点编号必须从 1 开始。
        array<int, 26> next{};
        // pass：经过该节点的已插入字符串数；end：恰在该节点结束的字符串数。
        int pass = 0;
        int end = 0;
    };
    vector<Node> node{1};

    // 参数 s 只含 a..z；把一个词加入本 Trie，重复插入会增加 pass/end 计数。
    void insert(const string& s) {
        // 字符映射固定为 'a'..'z'；改题换字符集时同时修改 26 与 ch-'a'。
        int u = 0;
        // 根的 pass 也计数，因此 countPrefix("") 会返回插入串总数。
        ++node[u].pass;
        for (char ch : s) {
            int c = ch - 'a';
            if (node[u].next[c] == 0) {
                node[u].next[c] = (int)node.size();
                node.push_back(Node{});
            }
            u = node[u].next[c];
            ++node[u].pass;
        }
        ++node[u].end;
    }

    // 参数 s 只含 a..z；返回前缀终点节点号，缺边返回 -1；不修改 Trie。
    int findNode(const string& s) const {
        // 返回前缀终点编号；-1 是查询失败状态，与合法根节点 0 区分。
        int u = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (node[u].next[c] == 0) return -1;
            u = node[u].next[c];
        }
        return u;
    }

    // 参数 s 只含 a..z；返回完整词插入次数，未出现为 0；不修改 Trie。
    int countWord(const string& s) const {
        int u = findNode(s);
        return u == -1 ? 0 : node[u].end;
    }

    // 参数 s 只含 a..z；返回以 s 为前缀的插入次数；空串返回总插入次数。
    int countPrefix(const string& s) const {
        int u = findNode(s);
        return u == -1 ? 0 : node[u].pass;
    }
};
```

**易错点：**

1. 根节点编号为 0，因此 0 同时作为“无转移”，新节点编号必须从 1 开始。
2. 模板未检查字符范围，非小写字母会越界。
3. “经过次数”和“单词结束次数”含义不同，不能混用。

**参考：**

- [OI Wiki：字典树](https://oi-wiki.org/string/trie/)

## 8.6 AC 自动机

**适用范围：** 小写 ASCII 字符集下的多模式匹配，要求先插入全部非空模式再 build；状态图为 Trie。
**能做什么：** 固定数组转移构建 $O(SΣ)$、扫描与 fail 传播 $O(T+S)$，空间 $O(SΣ)$。
**输入 / 输出：** `insert(s)` 返回终止节点；`build()` 原地补全转移且只能在插入结束后调用一次；`countOccurrences(text,terminal)` 返回与 terminal 等长的计数，包含重叠，terminal 只能指向非空模式终点。

**用法：**

- 先逐个 `insert(pattern)`，保存返回的终止节点，再调用 `build()`。
- `countOccurrences(text,terminal)` 返回各模式出现次数，包含重叠出现。
- 相同模式的终止节点相同，因此得到相同计数。
- 模板限定小写英文字母；`build()` 后不要再插入模式。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct AhoCorasick {
    struct Node {
        // build 前 next 是 Trie 边；build 后缺边被补为自动机转移，不能再继续 insert。
        array<int, 26> next{};
        // fail 指向当前字符串的最长真后缀状态，根及根的孩子失败时回到根 0。
        int fail = 0;
    };
    vector<Node> node{1};
    vector<int> bfsOrder;

    // 参数 s 是非空小写模式串；加入 Trie 并返回终止节点号，须在 build 前调用。
    int insert(const string& s) {
        // 返回模式串终止节点，调用者须保存它；字符集固定为小写 'a'..'z'。
        int u = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (node[u].next[c] == 0) {
                node[u].next[c] = (int)node.size();
                node.push_back(Node{});
            }
            u = node[u].next[c];
        }
        return u;
    }

    // 无参数；补全本对象转移并填 bfsOrder，改变 Trie 边语义；插入结束后仅调用一次。
    void build() {
        // 只调用一次；BFS 保证计算子节点 fail 前，其 fail 父节点的完整转移已就绪。
        queue<int> q;
        for (int c = 0; c < 26; ++c) {
            int v = node[0].next[c];
            if (v != 0) q.push(v);
        }
        while (!q.empty()) {
            int u = q.front(); q.pop();
            bfsOrder.push_back(u);
            for (int c = 0; c < 26; ++c) {
                int v = node[u].next[c];
                if (v != 0) {
                    // u 经 c 到 v，则 v 的最长可用后缀是 fail[u] 经同一字符的转移。
                    node[v].fail = node[node[u].fail].next[c];
                    q.push(v);
                } else {
                    // 补全缺边后，文本扫描每个字符只做一次数组跳转，不需 while 回退。
                    node[u].next[c] = node[node[u].fail].next[c];
                }
            }
        }
    }

    // 参数 text 是小写文本，terminal 是有效的非根模式终点列表；返回逐项出现次数（允许重叠），不改自动机。
    vector<long long> countOccurrences(
        const string& text, const vector<int>& terminal
    ) const {
        // visits[u] 先统计扫描时恰好落到 u 的次数；terminal 中存各模式的终止节点。
        vector<long long> visits(node.size(), 0), answer;
        int u = 0;
        for (char ch : text) {
            u = node[u].next[ch - 'a'];
            ++visits[u];
        }
        // fail 树上由深到浅累加：到达 u 也代表其每个 fail 后缀模式出现一次。
        for (int i = (int)bfsOrder.size() - 1; i >= 0; --i) {
            int v = bfsOrder[i];
            visits[node[v].fail] += visits[v];
        }
        for (int v : terminal) answer.push_back(visits[v]);
        return answer;
    }
};
```

**易错点：**

1. 必须先插入全部模式串，再构建失配指针。
2. 统计每个模式次数时，要按 BFS 逆序把访问量累加到 fail 父节点。
3. 空模式串会终止在根节点，通常应在输入层单独处理。
4. 模板将缺失转移补全，构建后原 Trie 结构已改变。

**参考：**

- [OI Wiki：AC 自动机](https://oi-wiki.org/string/ac-automaton/)


## 8.7 后缀数组

**适用范围：** 需要按字典序排序所有字节后缀并查询相邻后缀 LCP；适合中等长度字符串。
**能做什么：** `suffixArray` 倍增比较排序 $O(n\log^2 n)$、空间 $O(n)$；Kasai 的 LCP 构造 $O(n)$。
**输入 / 输出：** `suffixArray(s)` 返回按后缀字典序排列的 0-based 起点数组，空串返回空数组；`lcpArray(s,sa)` 要求 `sa` 是按后缀字典序排列的 `[0,n)` 起点排列，返回长度 `max(0,n-1)`，第 i 项为 `sa[i]` 与 `sa[i+1]` 的 LCP。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数 s 是字节串；返回按字典序排列的后缀起点，空串返回空表，不改输入。
vector<int> suffixArray(const string& s) {
    // 倍增按两个 rank 排序，越界第二关键字视为 -1。
    int n = s.size();
    vector<int> sa(n), rk(n), tmp(n);
    iota(sa.begin(), sa.end(), 0);
    for (int i = 0; i < n; ++i) rk[i] = (unsigned char) s[i];
    // k 逐次翻倍，rank 对应长度 2k 的前缀；所有后缀按新 rank 重排。
    for (long long k = 1; k < n; k <<= 1) {
        // 参数 i 是 0..n-1 的后缀起点；返回当前 2k 长度排序键，只读捕获的 rk/k。
        auto rankPair = [&](int i) {
            return pair{rk[i], i + k < n ? rk[i + k] : -1};
        };
        // 比较器参数是两个后缀起点；按 rankPair 严格升序比较，不改捕获状态。
        sort(sa.begin(), sa.end(), [&](int i, int j) {
            return rankPair(i) < rankPair(j);
        });
        if (n) tmp[sa[0]] = 0;
        for (int i = 1; i < n; ++i) {
            int a = sa[i - 1], b = sa[i];
            tmp[b] = tmp[a] + (rankPair(a) < rankPair(b));
        }
        rk=tmp;
        if (n && rk[sa.back()] == n - 1) break;
    }
    return sa;
}
// 参数 sa 必须是按后缀字典序排列的 [0,|s|) 起点排列；返回相邻后缀 LCP，长度 max(0,n-1)，不改输入。
vector<int> lcpArray(const string& s, const vector<int>& sa) {
    int n = s.size();
    vector<int> rk(n), lcp(max(0, n - 1));
    for (int i = 0; i < n; ++i) rk[sa[i]] = i;
    // Kasai 复用相邻后缀的公共前缀，向右移动起点后最多只需少比较一个字符。
    for (int i = 0, h = 0; i < n; ++i) {
        int r = rk[i];
        if (r == n - 1) {
            h = 0;
            continue;
        }
        int j = sa[r + 1];
        while (i + h < n && j + h < n && s[i + h] == s[j + h]) ++h;
        lcp[r] = h;
        if (h) --h;
    }
    return lcp;
}
```

坑：空串要单独确认调用逻辑；`lcp[i]` 对应 `sa[i]` 与 `sa[i+1]`；百万级数据应改计数排序版本。
