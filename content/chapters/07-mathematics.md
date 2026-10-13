
# 7. 数学

本章默认整数为 `long long`，模数记为 `mod`。若无特别说明，模运算结果规范到 $[0,mod)$；乘法可能超过 `long long` 时用 `__int128`。

## 7.1 GCD 与扩展 GCD

**适用范围：** 整数最大公约数、Bézout 系数与同余预处理；输入及递归系数乘积须可由 `long long` 表示，不能含 `LLONG_MIN`。
**能做什么：** 欧几里得算法与扩展欧几里得算法在 $O(\log \min(|a|,|b|))$ 时间内求 gcd 和一组系数；`norm` 规范余数。
**输入 / 输出：** `exgcd(a,b,x,y)` 返回非负 gcd 并写 `x,y` 使 `ax+by=gcd`；(0,0) 返回 0、系数为 (1,0)。`norm(x,mod)` 要求 `mod>0`，返回 `[0,mod)`。

**用法：**

- `std::gcd(a,b)` 可直接求非负最大公约数。
- `exgcd(a,b,x,y)` 返回 `gcd(a,b)`，并写入一组 Bézout 系数。
- 方程 $ax+by=c$ 有整数解当且仅当 `c % gcd(a,b) == 0`。
- 模数、输入可能为负时，先用 `norm` 规范余数。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 输入可为负数；返回非负 gcd，并令 a*x+b*y=gcd(a,b)。系数本身不取模。
// 参数 a,b 及递归系数中间值须可由 long long 表示，不能含 LLONG_MIN；返回 gcd>=0，并覆盖 x,y 为 Bézout 系数。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) {
        // 选 x 的符号是为了即使 a<0，右侧仍为非负的 |a|。
        x = (a >= 0 ? 1 : -1);
        y = 0;
        return llabs(a);
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    // 由 b*x1+(a%b)*y1=g 反代；若输入接近 long long 上界，乘法可能溢出。
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

// 要求 mod>0；C++ 的负数余数可能为负，所以统一规范到 [0,mod)。
// 参数 mod>0；返回 x 的规范模余数 [0,mod)，不修改实参。
ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}
```

**易错点：**

1. `gcd(0,0)` 通常按 0 处理，但对应的 Bézout 系数不唯一。
2. C++ 负数取模仍可能为负；作为答案或下标前必须规范化。
3. 系数可能很大，中间乘法可能溢出 `long long`。

**参考：**

- [OI Wiki：最大公约数](https://oi-wiki.org/math/number-theory/gcd/)

## 7.2 快速幂

**适用范围：** 非负整数指数的模幂；负指数须先求逆元，模数必须为正。
**能做什么：** `qpow` 用二进制平方计算 $a^e\bmod mod$，$O(\log e)$ 时间、$O(1)$ 额外空间；`mul_mod` 以 `__int128` 承接乘积。
**输入 / 输出：** `mul_mod(a,b,mod)` 要求 `mod>0`，返回 C++ 有符号余数；`qpow(a,e,mod)` 要求 `e>=0,mod>0`，返回 `[0,mod)`，包括 `mod==1` 时为 0，`0^0` 按空乘积约定为 `1%mod`。

**用法：**

- 调用 `qpow(a, e, mod)`，要求 `e >= 0`、`mod > 0`。
- `mod == 1` 时答案为 0。
- 负底数会先规范到 $[0,mod)$。
- 负指数不能直接使用；模意义下应先求逆元。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 要求 mod>0，且 a、b 已在 long long 内；用 __int128 避免乘法先溢出再取模。
// 参数 mod>0；返回 a*b 的 C++ 余数，乘积在 __int128 中求值，不改实参。
ll mul_mod(ll a, ll b, ll mod) {
    // 提升后再乘，避免两个 long long 先溢出；要求 mod>0。
    return (ll)((__int128)a * b % mod);
}

// 参数 e>=0、mod>0；返回规范化的 a^e mod mod，内部不持有可变共享状态。
ll qpow(ll a, long long e, ll mod) {
    // e 必须非负；若题目出现负指数，应先求 a 的模逆元再调用。
    a %= mod;
    if (a < 0) a += mod;
    ll ans = 1 % mod;
    while (e > 0) {
        // 不变量：ans * a^e 与原始 a^原始e 在模 mod 下同余。
        if (e & 1) ans = mul_mod(ans, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return ans;
}
```

**易错点：**

1. 指数必须是非负整数；不要把负指数传入循环。
2. `a * a` 即使最终取模也可能先溢出。
3. 不要把按位与写成 `e & 1 == 1`；加括号更清楚。

**参考：**

- [OI Wiki：快速幂](https://oi-wiki.org/math/binary-exponentiation/)

## 7.3 素数筛

**适用范围：** 已知上界 `n>=0`，需要批量判素、查询 `[1,n]` 内各整数的正因数个数或分解范围内整数时使用；单个数值很大的分解更适合 7.14 的试除模板。
**能做什么：** 线性筛在 $O(n)$ 时间和空间内生成质数、最小质因子、该最小质因子的指数及正因数个数；判素和范围内因数个数查询均为 $O(1)$。因数数量维护新增两张长度 `n+1` 的 `int` 表。
**输入 / 输出：** `PrimeSieve(n)` 建立 `[0,n]` 表；`isPrime(x)` 对任意整数返回布尔值，超出范围或 `x<2` 返回 `false`；`countDivisors(x)` 要求 `1<=x<=n`，返回 x 的正因数个数。`divisorCount[1]=1`；`divisorCount[0]=0` 仅为占位，不表示数学上的因数个数。

**用法：**

- 构造 `PrimeSieve sieve(n)` 后通过 `sieve.primes` 读取素数表。
- `primes` 递增，`minPrime[x]` 是 x 的最小质因子，`minPrimeExponent[x]` 是该因子在 x 中的指数。
- `divisorCount[x]` 保存 x 的正因数个数；对素数为 2，对 1 为 1。筛表建好后查询 O(1)。
- 例如 `sieve.countDivisors(12)==6`，`sieve.countDivisors(1)==1`。
- `isPrime(x)` 可判断筛选范围内的整数。
- 多次分解不超过 `n` 的数，可反复除以 `minPrime[x]`。
- 对同一上界内的大量整数做计数适合本表；只分解一个大数时，筛到该数会浪费时间和空间。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct PrimeSieve {
    // 数组下标就是被筛整数；0、1 的 minPrime 和 minPrimeExponent 为 0，divisorCount[0] 仅作占位。
    vector<int> primes, minPrime, minPrimeExponent, divisorCount;

    // 若 i=p^e*m 且 gcd(p,m)=1，则 d(i)=(e+1)d(m)。已有最小质因子时 d(ip)=d(i)/(e+1)*(e+2)，新增质因子时 d(ip)=2d(i)；前者先做精确整除。
    // 参数 n>=0；构造 [0,n] 筛表，填充素数、最小质因子、其指数和正因数个数；n=0/1 也有效。
    explicit PrimeSieve(int n)
        : minPrime(n + 1, 0), minPrimeExponent(n + 1, 0), divisorCount(n + 1, 0) {
        if (n >= 1) divisorCount[1] = 1;
        for (int i = 2; i <= n; ++i) {
            if (minPrime[i] == 0) {
                minPrime[i] = i;
                minPrimeExponent[i] = 1;
                divisorCount[i] = 2;
                primes.push_back(i);
            }
            for (int p : primes) {
                // 只用 p<=minPrime[i]：保证 i*p 恰由其最小质因子筛到一次。
                if (p > minPrime[i] || 1LL * i * p > n) break;
                int product = i * p;
                minPrime[product] = p;
                if (p == minPrime[i]) {
                    // 同一最小质因子指数由 e 增到 e+1，其余质因子的计数因子不变。
                    minPrimeExponent[product] = minPrimeExponent[i] + 1;
                    divisorCount[product] = divisorCount[i] /
                        (minPrimeExponent[i] + 1) * (minPrimeExponent[product] + 1);
                    break;
                }
                // p<minPrime[i] 时新增一个一次因子 p，tau 值乘 2。
                minPrimeExponent[product] = 1;
                divisorCount[product] = divisorCount[i] * 2;
            }
        }
    }

    // 参数 x 为任意整数；返回 x 是否在筛范围内且为素数，越界返回 false，不改对象。
    bool isPrime(int x) const {
        return x >= 2 && x < (int)minPrime.size() && minPrime[x] == x;
    }

    // 参数 x 满足 1<=x<minPrime.size()；返回 x 的正因数个数，读取预处理表且不修改对象。
    int countDivisors(int x) const {
        return divisorCount[x];
    }
};
```

**易错点：**

1. 0 和 1 都不是素数。
2. 判断 `i * p <= n` 时先转成 `long long`。
3. 线性筛内层停止条件不能随意改，否则会失去正确性或线性复杂度。

**参考：**

- [OI Wiki：筛法](https://oi-wiki.org/math/number-theory/sieve/)

## 7.4 质因数分解

**适用范围：** 分解单个正整数 `n>=1`，数值不大到需要 Pollard–Rho 时使用。
**能做什么：** 试除到平方根，时间 $O(\sqrt n)$、额外空间随不同质因子数增长。
**输入 / 输出：** `factorize(n)` 返回按质因子升序排列的 `{p,e}` 向量；`n==1` 返回空向量，不改变输入。

**用法：**

- 调用 `factorize(n)`，要求 `n >= 1`。
- 返回 `{质因子, 指数}`，质因子严格递增。
- 若需约数个数，计算各 `(指数 + 1)` 的乘积。
- 大量且数值有共同上界时，优先预处理最小质因子筛。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=1；返回升序 {质因子,指数}，n==1 返回空表，不改调用者数据。
vector<pair<ll, int>> factorize(ll n) {
    // 要求 n>=1；返回质因子递增的 {质因子, 指数}，不记录因子 1。
    vector<pair<ll, int>> fac;
    // 用 p<=n/p 代替 p*p<=n，避免 long long 乘法溢出；n 会随试除缩小。
    for (ll p = 2; p <= n / p; ++p) {
        if (n % p != 0) continue;
        int e = 0;
        while (n % p == 0) {
            n /= p;
            ++e;
        }
        fac.push_back({p, e});
    }
    // 此时若仍有余数，它不可能再含两个质因子，因此本身就是最后一个质因子。
    if (n > 1) fac.push_back({n, 1});
    return fac;
}
```

**易错点：**

1. 循环条件写 `p <= n / p`，避免 `p * p` 溢出。
2. 试除过程中 `n` 会缩小，循环上界也应随之缩小。
3. 循环结束后若 `n > 1`，不能漏掉这个大质因子。

**参考：**

- [OI Wiki：质因数分解](https://oi-wiki.org/math/number-theory/pollard-rho/#%E6%9C%B4%E7%B4%A0%E7%AE%97%E6%B3%95)

## 7.5 欧拉函数

**适用范围：** 求正整数 `n>=1` 的欧拉函数，或求固定上界内的整张函数表。
**能做什么：** `eulerPhi` 单次试除 $O(\sqrt n)$；`phiSieve` 线性筛 $O(n)$ 时间、$O(n)$ 空间。
**输入 / 输出：** `eulerPhi(n)` 返回 `phi(n)` 且 `phi(1)=1`；`phiSieve(n)` 要求 `n>=0`，返回下标 `[0,n]` 的表，`n==0` 时只含 `phi[0]=0`。

**用法：**

- `eulerPhi(n)` 要求 `n >= 1`，并约定 `phi(1) == 1`。
- 每个不同质因子只更新一次 `ans = ans / p * (p - 1)`。
- 若 `gcd(a,n)==1`，则 $a^{\varphi(n)}\equiv1\pmod n$。
- 需要 $1\ldots n$ 全部函数值时使用 `phiSieve(n)`。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=1；返回 phi(n)，不修改 n 或外部状态。
ll eulerPhi(ll n) {
    // 要求 n>=1；ans 始终等于原 n 乘上已处理质因子的 (p-1)/p。
    ll ans = n;
    for (ll p = 2; p <= n / p; ++p) {
        if (n % p != 0) continue;
        while (n % p == 0) n /= p;
        // p 一定整除当前 ans，先除后乘既保持精确，也降低中间溢出风险。
        ans = ans / p * (p - 1);
    }
    if (n > 1) ans = ans / n * (n - 1);
    return ans;
}

// 参数 n>=0；返回下标 [0,n] 的 phi 表，分配局部筛状态，不修改外部对象。
vector<int> phiSieve(int n) {
    // phi[x] 对应整数 x；线性筛中每个合数只由最小质因子产生一次。
    vector<int> phi(n + 1), primes;
    vector<bool> composite(n + 1, false);
    if (n >= 1) phi[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (!composite[i]) {
            primes.push_back(i);
            phi[i] = i - 1;
        }
        for (int p : primes) {
            if (1LL * i * p > n) break;
            composite[i * p] = true;
            if (i % p == 0) {
                // p 已整除 i：新增一个 p 因子，phi(i*p)=phi(i)*p，随后必须停止。
                phi[i * p] = phi[i] * p;
                break;
            }
            // gcd(i,p)=1，乘入新质因子 p 时欧拉函数乘以 p-1。
            phi[i * p] = phi[i] * (p - 1);
        }
    }
    return phi;
}
```

**易错点：**

1. 欧拉定理要求底数与模数互质。
2. 公式乘除应先做整除再乘，降低溢出风险。
3. `phi(1)` 为 1，不是 0。

**参考：**

- [OI Wiki：欧拉函数](https://oi-wiki.org/math/number-theory/euler-totient/)

## 7.6 模逆元

**适用范围：** 模意义除法且 `mod>1`；逆元存在的充要条件是 `gcd(a,mod)==1`。
**能做什么：** 扩展 GCD 在 $O(\log mod)$ 时间求逆元，支持合数模。
**输入 / 输出：** `modInverse(a,mod)` 返回 `{true,x}` 且 `x∈[0,mod)`；若不互质返回 `{false,0}`。函数先把负 `a` 规范化。

**用法：**

- `modInverse(a, mod)` 返回 `{是否存在, 逆元}`。
- 模数要求 `mod > 1`，结果位于 $[0,mod)$。
- 计算 `b / a (mod mod)` 前先确认逆元存在。
- 组合数的阶乘逆元法通常要求模数为质数且阶乘不为 0。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 a,b 为非负且递归系数运算须可表示；返回 gcd 并写 Bézout 系数 x,y。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

// 参数 mod>1、a 可带符号；返回 {是否存在,规范逆元}，不互质时为 {false,0}。
pair<bool, ll> modInverse(ll a, ll mod) {
    // 要求 mod>1；返回 false 表示 gcd(a,mod)!=1，此时任何模除法都无定义。
    a %= mod;
    if (a < 0) a += mod;
    ll x, y;
    ll g = exgcd(a, mod, x, y);
    if (g != 1) return {false, 0};
    // Bézout 等式给出 a*x+mod*y=1，所以 x 就是逆元；规范到 [0,mod)。
    x %= mod;
    if (x < 0) x += mod;
    return {true, x};
}
```

**易错点：**

1. 不互质时逆元不存在，不能继续做模除法。
2. 费马小定理求逆只适用于质数模数。
3. `a == 0 (mod mod)` 没有逆元。

**参考：**

- [OI Wiki：模逆元](https://oi-wiki.org/math/number-theory/inverse/)

## 7.7 线性同余方程

**适用范围：** 求 `a*x ≡ b (mod m)`，要求正模数 `m>0`；系数和常数允许带符号。
**能做什么：** 扩展 GCD 判定可解性并给出一个剩余类，时间 $O(\log m)$、递归空间 $O(\log m)$。
**输入 / 输出：** `solveCongruence(a,b,m)` 返回 `{exists,x0,step}`；若有解，所有整数解为 `x=x0+k*step`，其中 `x0∈[0,step)`、`step=m/gcd(a,m)`。无解时其余字段为 0。

**用法：**

- `solveCongruence(a,b,m)` 返回 `{是否有解, x0, step}`。
- 所有整数解满足 `x = x0 + k * step`，其中 `step = m / gcd(a,m)`。
- 返回的 `x0` 位于 `[0, step)`。
- 要列出原模数内全部解，取 `x0 + k*step`，`0 <= k < gcd(a,m)`。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 a,b 为非负；返回 gcd 并覆盖 x,y 为 Bézout 系数。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

struct CongruenceSolution {
    bool exists;
    // exists=true 时全部解为 x=x0+k*step，且 x0 位于 [0,step)。
    ll x0, step;
};

// 参数 m>0、a,b 可带符号；返回解存在标志及 x0、step，不解时三字段为 false,0,0。
CongruenceSolution solveCongruence(ll a, ll b, ll m) {
    // 要求 m>0；负系数和负常数先规范化，方程语义不变。
    a %= m;
    b %= m;
    if (a < 0) a += m;
    if (b < 0) b += m;
    ll x, y;
    ll g = exgcd(a, m, x, y);
    // ax≡b (mod m) 可解当且仅当 gcd(a,m) 整除 b。
    if (b % g != 0) return {false, 0, 0};
    ll step = m / g;
    // 约去 g 后 x 是 a/g 在模 m/g 下的逆元；乘法用 __int128 防溢出。
    ll x0 = (ll)((__int128)x * (b / g) % step);
    if (x0 < 0) x0 += step;
    return {true, x0, step};
}
```

**易错点：**

1. 先检查 `b % gcd(a,m)`，否则逆元并不存在。
2. 约去最大公约数后，答案模数是 `m/g` 而不是 `m`。
3. 中间的 `x * (b/g)` 可能溢出，应使用 `__int128`。

**参考：**

- [OI Wiki：线性同余方程](https://oi-wiki.org/math/number-theory/linear-equation/)

## 7.8 中国剩余定理（非互质模数）

**适用范围：** 合并多个模同余式，模数允许不互质但每个 `mod[i]>0`；要求逐步 lcm 可放进 `long long`。
**能做什么：** 逐式合并并用 gcd 判相容，时间约 $O(k\log M)$、额外空间 $O(1)$。
**输入 / 输出：** `crt(rem,mod)` 要求两向量等长；返回 `{true,r,m}` 表示全部解 `x=r+k*m` 且 `r∈[0,m)`，矛盾返回 `{false,0,0}`。空输入返回 `0 (mod 1)`。

**用法：**

- `crt(rem, mod)` 中每个 `mod[i]` 必须为正。
- 返回 `{true, r, m}` 表示全部解为 `x = r + k*m`。
- `r` 会规范到 `[0,m)`；`false` 表示方程组矛盾。
- 若所有模数两两互质，最终模数为其乘积。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 a,b 为正；返回 gcd 并覆盖 x,y 为 Bézout 系数，要求递归乘积不溢出。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

struct CRTResult {
    bool exists;
    // exists=true 时全部解为 x=remainder+k*modulus，余数已规范化。
    ll remainder, modulus;
};

// 参数 rem/mod 等长、每个模数正且逐步 lcm<=LLONG_MAX；返回规范解类或矛盾标志，不改输入。
CRTResult crt(const vector<ll>& rem, const vector<ll>& mod) {
    // 要求 rem.size()==mod.size() 且每个 mod[i]>0；空方程组返回 x≡0 (mod 1)。
    ll r = 0, m = 1;
    for (int i = 0; i < (int)rem.size(); ++i) {
        ll b = rem[i] % mod[i];
        if (b < 0) b += mod[i];
        ll x, y;
        ll g = exgcd(m, mod[i], x, y);
        ll diff = b - r;
        // 令新解为 r+m*t；只有 gcd(m,mod[i]) 能整除 b-r 时才可合并。
        if (diff % g != 0) return {false, 0, 0};

        ll q = mod[i] / g;
        // x 是 m/g 对模 q 的逆元；t 取最小非负剩余类即可。
        ll t = (ll)((__int128)(diff / g) * x % q);
        if (t < 0) t += q;
        __int128 newMod = (__int128)m * q;
        __int128 newR = (__int128)r + (__int128)m * t;
        // 若题目不保证最终 lcm 可放入 long long，需改用大整数。
        m = (ll)newMod;
        r = (ll)(newR % m);
        if (r < 0) r += m;
    }
    return {true, r, m};
}
```

**易错点：**

1. 经典 CRT 的乘积公式不能直接用于不互质模数。
2. `lcm`、余数更新都可能超过 `long long`；模板假设最终答案可表示。
3. 空方程组按 `x ≡ 0 (mod 1)` 处理。

**参考：**

- [OI Wiki：中国剩余定理](https://oi-wiki.org/math/number-theory/crt/)

## 7.9 组合数

**适用范围：** 质数模数下重复查询组合数，预处理界 `N` 满足 `0<=N<mod`、`mod` 为质数且大于 1。
**能做什么：** `Combinations` 预处理阶乘和逆阶乘，构造 $O(N+\log mod)$、单次查询 $O(1)$，空间 $O(N)$。
**输入 / 输出：** `Combinations(N,mod)` 拥有 `[0,N]` 表；`C(n,k)` 返回模 `mod` 的组合数，`n>N`、`k<0` 或 `k>n` 按约定返回 0。

**用法：**

- 构造 `Combinations(N, mod)`，模板要求 `mod` 为质数且 `N < mod`。
- `C(n,k)` 在越界或 `k<0`、`k>n` 时返回 0。
- 多次查询同一模数时只预处理一次。
- 小范围任意模数可用递推 $C(n,k)=C(n-1,k-1)+C(n-1,k)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 0<=a<mod、e>=0、mod>1；返回规范的 a^e 模余数，供阶乘逆元计算。
ll qpow(ll a, ll e, ll mod) {
    ll ans = 1;
    while (e > 0) {
        if (e & 1) ans = (ll)((__int128)ans * a % mod);
        a = (ll)((__int128)a * a % mod);
        e >>= 1;
    }
    return ans;
}

struct Combinations {
    ll mod;
    // fact[i]=i!，invFact[i]=(i!)^{-1}；数组下标覆盖 [0,n]。
    vector<ll> fact, invFact;

    // 参数 0<=n<mod、mod 为质数；构造并拥有 0..n 阶乘和逆阶乘表。
    Combinations(int n, ll mod) : mod(mod), fact(n + 1), invFact(n + 1) {
        // 前提：mod 为质数且 0<=n<mod，否则 fact[n] 可能为 0 且没有逆元。
        fact[0] = 1;
        for (int i = 1; i <= n; ++i)
            fact[i] = (ll)((__int128)fact[i - 1] * i % mod);
        // 费马小定理只在质数模下成立；改成任意模数时需替换整套求逆方案。
        invFact[n] = qpow(fact[n], mod - 2, mod);
        for (int i = n; i >= 1; --i)
            invFact[i - 1] = (ll)((__int128)invFact[i] * i % mod);
    }

    // 参数 n,k 为整数；返回 C(n,k) mod mod，越出预处理范围或 k 不合法时返回 0，不改表。
    ll C(int n, int k) const {
        // 返回 C(n,k) mod mod；非法 k 或超出预处理上界时约定返回 0。
        if (k < 0 || k > n || n >= (int)fact.size()) return 0;
        ll ans = (ll)((__int128)fact[n] * invFact[k] % mod);
        return (ll)((__int128)ans * invFact[n - k] % mod);
    }
};
```

**易错点：**

1. 逆阶乘写法依赖质数模数和 `N < mod`。
2. `k > n` 时组合数是 0，不要访问负下标。
3. 不要为每次查询重复求幂；先统一预处理。

**参考：**

- [OI Wiki：组合数学](https://oi-wiki.org/math/combinatorics/combination/)

## 7.10 容斥原理

**适用范围：** 统计 `[1,n]` 中被给定正除数至少一个整除的数；`n>=0`，条件数必须小于 64 且足够小以承受指数枚举。
**能做什么：** 容斥枚举除数子集并用 lcm 算交集，时间 $O(2^k k)$、额外空间 $O(k)$；超过 `n` 的 lcm 贡献为 0。
**输入 / 输出：** `countDivisible(n,a)` 忽略 0、去重并删除冗余倍数，返回并集计数；负除数不在输入约定内。

**用法：**

- 示例 `countDivisible(n,a)` 统计 `1..n` 中能被至少一个 `a[i]` 整除的数。
- 先删除 0、重复项，以及被更小元素整除的冗余项。
- 子集交集对应被这些数的 lcm 整除。
- 条件数较大时，$2^k$ 不可接受，应寻找其他计数方法。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=0、a 含非负除数且有效项数<64；返回 [1,n] 并集计数，传值副本可排序删项。
ll countDivisible(ll n, vector<ll> a) {
    // 统计闭区间 [1,n]；模板假设 n>=0、除数为非负数，且有效条件数 k<64。
    sort(a.begin(), a.end());
    a.erase(remove(a.begin(), a.end(), 0), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());
    vector<ll> b;
    for (ll x : a) {
        bool redundant = false;
        // 若 x 是已有 y 的倍数，“能被 x 整除”已包含于“能被 y 整除”，可删除。
        for (ll y : b) if (x % y == 0) {
            redundant = true;
            break;
        }
        if (!redundant && x <= n) b.push_back(x);
    }

    ll ans = 0;
    int k = (int)b.size();
    for (unsigned long long mask = 1; mask < (1ULL << k); ++mask) {
        // 一个子集的交集就是被这些除数的 lcm 整除；奇数个集合加，偶数个减。
        ll lcm = 1;
        bool tooLarge = false;
        for (int i = 0; i < k; ++i) if (mask >> i & 1ULL) {
            ll g = std::gcd(lcm, b[i]);
            // 一旦 lcm>n，本子集贡献为 0；先除后比较同时避免 lcm 乘法溢出。
            if (lcm > n / (b[i] / g)) { tooLarge = true; break; }
            lcm *= b[i] / g;
        }
        if (tooLarge) continue;
        if (__builtin_popcountll(mask) & 1) ans += n / lcm;
        else ans -= n / lcm;
    }
    return ans;
}
```

**易错点：**

1. 正负号由所选集合数决定：奇加偶减。
2. lcm 计算前先判断是否超过 `n`，同时避免溢出。
3. `1ULL << k` 要求 `k < 64`，实际指数复杂度通常更早成为瓶颈。

**参考：**

- [OI Wiki：容斥原理](https://oi-wiki.org/math/combinatorics/inclusion-exclusion-principle/)

## 7.11 矩阵快速幂

**适用范围：** 维数较小、指数较大的线性递推或状态转移；指数非负，模数正。
**能做什么：** `matPow` 用二进制快速幂，$O(d^3\log e)$ 时间、$O(d^2)$ 空间。
**输入 / 输出：** `Matrix(r,c,mod)` 建立零矩阵；乘法要求维度匹配、模数一致，`matPow(base,e)` 要求方阵并返回 `base^e`，`e==0` 返回单位矩阵。

**用法：**

- `Matrix::identity(n,mod)` 是乘法单位矩阵。
- `matPow(A,e)` 要求 `A` 为方阵、`e >= 0`。
- 列向量约定下，若 `state(t+1)=A*state(t)`，则答案为 `A^t*state(0)`。
- 模板执行模运算；不取模时需改类型并评估溢出。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Matrix {
    int rows, cols;
    // 本模板所有元素都在同一正模数 mod 下运算；不同矩阵相乘时模数须一致。
    ll mod;
    vector<vector<ll>> a;

    // 参数 r,c>=0、mod>0；构造并拥有 r*c 个零元素。
    Matrix(int r, int c, ll mod) : rows(r), cols(c), mod(mod), a(r, vector<ll>(c)) {}

    // 参数 n>=0、mod>0；返回 n 阶模乘单位阵，不修改外部状态。
    static Matrix identity(int n, ll mod) {
        Matrix id(n, n, mod);
        for (int i = 0; i < n; ++i) id.a[i][i] = 1 % mod;
        return id;
    }
};

// 参数矩阵满足 x.cols==y.rows 且模数相同为正；返回新乘积矩阵，不改 x,y。
Matrix operator*(const Matrix& x, const Matrix& y) {
    // 前提 x.cols==y.rows；i-k-j 顺序可跳过零项，乘积用 __int128 防溢出。
    Matrix z(x.rows, y.cols, x.mod);
    for (int i = 0; i < x.rows; ++i)
        for (int k = 0; k < x.cols; ++k) if (x.a[i][k])
            for (int j = 0; j < y.cols; ++j)
                z.a[i][j] = (z.a[i][j] +
                    (__int128)x.a[i][k] * y.a[k][j]) % x.mod;
    return z;
}

// 参数 base 为正模方阵、e>=0；按值接收底矩阵并返回 base^e，实参不变。
Matrix matPow(Matrix base, long long e) {
    // 要求 base 为方阵、e>=0；列向量转移通常写 state(t)=base^t*state(0)。
    Matrix ans = Matrix::identity(base.rows, base.mod);
    while (e > 0) {
        // 不变量：ans * base^e 等于原矩阵的原指数次幂。
        if (e & 1) ans = ans * base;
        base = base * base;
        e >>= 1;
    }
    return ans;
}
```

**易错点：**

1. 明确状态是列向量还是行向量，矩阵方向不能写反。
2. `e == 0` 应返回单位矩阵。
3. 矩阵维度、模数必须匹配；模板未做运行时检查。

**参考：**

- [OI Wiki：矩阵](https://oi-wiki.org/math/linear-algebra/matrix/)

## 7.12 高斯消元

**适用范围：** 求有限实数系数的线性方程组，至少一行且每行列数相同；尺度适合绝对 EPS 判定。
**能做什么：** 部分主元高斯消元判别无解/唯一/多解，$m×n$ 时间 $O(mn\min(m,n))$、空间 $O(mn)$。
**输入 / 输出：** `gauss(a,answer)` 输入 `m×(n+1)` 增广矩阵并覆盖 `answer`；返回 0 无解（此时答案不可用）、1 唯一解、2 无穷多解（给自由变量取 0 的一组解）。

**用法：**

- 增广矩阵每行含 `n+1` 项，最后一列为常数。
- 返回 `0` 表示无解，`1` 表示唯一解，`2` 表示无穷多解。
- `answer` 在有解时给出一组解；自由变量默认取 0。
- 模意义方程组应改用模逆元，不可照搬浮点模板。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 0：无解；1：唯一解；2：无穷多解。
// 参数 a 为有限数值且形状 m>0、每行 n+1；覆盖 answer，返回 0无解/1唯一/2多解。无解时 answer 不可用。
int gauss(vector<vector<long double>> a, vector<long double>& answer) {
    // a 是 m 行、n+1 列的增广矩阵；模板要求 m>0 且各行长度一致。
    // EPS 应按输入尺度调整：数值很大或病态矩阵可能需要更稳健的方法。
    const long double EPS = 1e-12L;
    int m = (int)a.size();
    int n = (int)a[0].size() - 1;
    vector<int> where(n, -1);
    // where[col] 是该未知数主元所在行；-1 表示自由变量，最终默认取 0。
    int row = 0;

    for (int col = 0; col < n && row < m; ++col) {
        int pivot = row;
        // 部分主元：选绝对值最大项，减少除以小数造成的误差放大。
        for (int i = row; i < m; ++i)
            if (fabsl(a[i][col]) > fabsl(a[pivot][col])) pivot = i;
        // 整列近似为 0 时不能制造主元，这一列成为自由变量候选。
        if (fabsl(a[pivot][col]) < EPS) continue;
        swap(a[pivot], a[row]);
        where[col] = row;

        long double div = a[row][col];
        for (int j = col; j <= n; ++j) a[row][j] /= div;
        // 消去所有其他行，直接得到简化行阶梯形；只消下方则需额外回代。
        for (int i = 0; i < m; ++i) if (i != row) {
            long double factor = a[i][col];
            if (fabsl(factor) < EPS) continue;
            for (int j = col; j <= n; ++j)
                a[i][j] -= factor * a[row][j];
        }
        ++row;
    }

    answer.assign(n, 0);
    for (int col = 0; col < n; ++col)
        if (where[col] != -1) answer[col] = a[where[col]][n];

    for (int i = 0; i < m; ++i) {
        // 用得到的一组解回代等价方程；不满足说明出现 0=非0，即无解。
        long double lhs = 0;
        for (int j = 0; j < n; ++j) lhs += a[i][j] * answer[j];
        if (fabsl(lhs - a[i][n]) > EPS) return 0;
    }
    for (int col = 0; col < n; ++col)
        if (where[col] == -1) return 2;
    return 1;
}
```

**易错点：**

1. 必须选绝对值较大的主元，直接用当前行数值误差更大。
2. 无主元的列对应自由变量，不代表无解。
3. 空矩阵需要在调用前单独处理，模板假设至少有一行。

**参考：**

- [OI Wiki：高斯消元](https://oi-wiki.org/math/numerical/gauss/)

## 7.13 公平组合游戏与 SG 函数

**适用范围：** 无随机、完全信息、正常玩法且状态转移图为 DAG 的公平组合游戏；多个子游戏须彼此独立。
**能做什么：** `sg(u)` 记忆化求 mex，遍历复杂度 $O(V+E)$ 外加 mex 标记；空间 $O(V+E)$。
**输入 / 输出：** `SGGame(graph)` 接管 0-based 状态图；`sg(u)` 返回状态值并写入共享 `memo`；`firstPlayerWins(game,starts)` 会填充 memo，返回起始局面 SG 异或是否非零。节点下标须合法。

**用法：**

- 将每个局面视为节点，可执行操作视为有向边，且状态必须无环。
- `sg(u)` 返回该局面的 Sprague–Grundy 值。
- 多堆或多个独立局面把 SG 值异或；结果 0 为后手必胜。
- 仅判断普通取石游戏时，先确认确实满足正常玩法与独立性。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SGGame {
    // nextState[u] 列出局面 u 一步可达的所有局面；状态图必须是 DAG。
    vector<vector<int>> nextState;
    // memo[u]=-1 表示尚未计算，否则保存 SG(u)，使每个状态只展开一次。
    vector<int> memo;

    // 参数 graph 是 0-based DAG 邻接表；移动其内容初始化游戏和 -1 memo。
    explicit SGGame(vector<vector<int>> graph)
        : nextState(std::move(graph)), memo(nextState.size(), -1) {}

    // 参数 u 是合法状态编号；返回 SG(u)，并递归填充本对象 memo，要求图无环。
    int sg(int u) {
        if (memo[u] != -1) return memo[u];
        vector<int> values;
        values.reserve(nextState[u].size());
        for (int v : nextState[u]) values.push_back(sg(v));

        // k 个后继的 mex 至多为 k，因此只需标记 [0,k]，更大的 SG 值可忽略。
        vector<bool> seen(values.size() + 1, false);
        for (int x : values)
            if (x < (int)seen.size()) seen[x] = true;
        int mex = 0;
        while (mex < (int)seen.size() && seen[mex]) ++mex;
        return memo[u] = mex;
    }
};

// 参数 starts 是合法且互相独立的起始状态；返回 SG 异或非零，并通过 game 填充共享 memo。
bool firstPlayerWins(SGGame& game, const vector<int>& starts) {
    // starts 表示彼此独立的子游戏；普通玩法下异或和非 0 当且仅当先手必胜。
    int total = 0;
    for (int s : starts) total ^= game.sg(s);
    return total != 0;
}
```

**易错点：**

1. SG 定理不直接适用于有环游戏、随机游戏或“不能行动者胜”的反常玩法。
2. 合并独立游戏使用异或，不是相加。
3. `mex` 是未出现的最小非负整数，后继为空时 SG 为 0。

**参考：**

- [OI Wiki：公平组合游戏](https://oi-wiki.org/math/game-theory/impartial-game/)


## 7.14 质因数分解、约数个数与约数和

**适用范围：** 分解 `n>=1` 后计算约数数量、约数和或完整约数列表；各结果须能放进 `long long`。
**能做什么：** 试除分解 $O(\sqrt n)$；枚举约数 $O(\sqrt n+d\log d)$（`d` 为约数个数），额外空间 $O(d)$。
**输入 / 输出：** `factorize(n)` 返回有序 `{p,e}`；`divisorCountSum(n)` 返回 `{约数个数,约数和}`；`enumerateDivisors(n)` 返回升序正约数，`n==1` 三者均给出自然单位结果。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=1；返回按质因子升序的 {p,e}，1 返回空向量，不改外部状态。
vector<pair<ll,int>> factorize(ll n) {
    // 试除到 p*p>n；剩余 n>1 必为大质因子。
    vector<pair<ll, int>> f;
    for (ll p = 2; p <= n / p; ++p) {
        if (n % p != 0) continue;
        int e=0;
        do {
            n/=p;
            ++e;
        }
        while (n % p == 0);
        f.push_back({p,e});
    }
    if(n>1)f.push_back({n,1});
    return f;
}
// 参数 n>=1 且约数个数、约数和及中间幂可放进 ll；返回 {个数,总和}。
pair<ll,ll> divisorCountSum(ll n) {
    // 假设结果可放入 ll
    ll count = 1, sum = 1;
    for (auto [p, e] : factorize(n)) {
        ll term = 1, power = 1;
        for (int i = 0; i < e; ++i) {
            power *= p;
            term += power;
        }
        count*=e+1;
        sum*=term;
    }
    return {count,sum};
}
// 参数 n>=1；返回全部正约数升序列表，1 返回 {1}，不修改输入。
vector<ll> enumerateDivisors(ll n) {
    vector<ll>d;
    for (ll i = 1; i <= n / i; ++i) {
        if (n % i != 0) continue;
        d.push_back(i);
        if(i!=n/i)d.push_back(n/i);
    }
    sort(d.begin(),d.end());
    return d;
}
```

坑：要求 `n>=1`；循环条件写 `p<=n/p` 防平方溢出；约数和与个数也可能溢出，需要时取模或用大整数。
