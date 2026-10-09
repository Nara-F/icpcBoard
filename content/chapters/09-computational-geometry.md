
# 9. 计算几何

本章要求浮点输入为有限值，并采用两套明确的数值约定：含交点、距离、投影时使用 `long double` 和绝对误差 `EPS = 1e-12L`；坐标尺度变化明显时应按题目精度调整 EPS，或采用相对误差。整数输入只判断方向、求凸包或平方距离时，输入用 `long long`、运算前提升到 `__int128`；坐标差、乘积、叉积、面积和平方距离的中间量都必须落在 signed `__int128` 范围内，否则需增加坐标限制或使用大整数。浮点数不能直接用于有序容器的“近似相等”比较。

## 9.1 点、向量与基本运算

**适用范围：** 二维向量加减、缩放、点积/叉积、长度和旋转；含除法与三角函数的量使用 `long double`。
**能做什么：** 各操作 $O(1)$；`sgn` 使用绝对 EPS=1e-12，坐标尺度过大需重新选择容差。
**输入 / 输出：** `Point` 字段为实数坐标；运算符返回新值不修改操作数。`dot/cross/norm2/length` 分别返回标量量值；`rotate(a,angle)` 以弧度逆时针旋转。除法标量必须非零。

**用法：**

- `Point(x,y)` 表示浮点坐标；向量 `b-a` 从 `a` 指向 `b`。
- `dot(a,b)` 为点积，`cross(a,b)` 为二维叉积标量。
- `length(v)` 求长度，`rotate(v,angle)` 按弧度逆时针旋转。
- `sgn(x)` 将浮点量按 EPS 归为负、零、正。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;

const ld EPS = 1e-12L;
const ld PI = acosl(-1.0L);

// 这是绝对误差判号；若坐标尺度极大，应按题目误差要求调整 EPS 或改用相对误差。
// 参数 x 为 long double；按绝对 EPS 返回 -1/0/1，不修改全局容差。
int sgn(ld x) {
    if (x > EPS) return 1;
    if (x < -EPS) return -1;
    return 0;
}

struct Point {
    // 浮点点也作为向量使用；b-a 表示从 a 指向 b，坐标下标不涉及点编号。
    ld x = 0, y = 0;
    // 参数 p 是另一向量；返回逐坐标相加的新点，不改两操作数。
    Point operator+(const Point& p) const { return {x + p.x, y + p.y}; }
    // 参数 p 是被减向量；返回 this-p 的新向量，不改两操作数。
    Point operator-(const Point& p) const { return {x - p.x, y - p.y}; }
    // 参数 k 为实数缩放因子；返回缩放后的新向量，不改 this。
    Point operator*(ld k) const { return {x * k, y * k}; }
    // 参数 k 必须非零；返回逐坐标除以 k 的新向量，不改 this。
    Point operator/(ld k) const { return {x / k, y / k}; }
};

// 参数 a,b 为向量；返回点积标量，不修改输入。
ld dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
// cross(a,b)>0 表示从向量 a 逆时针转到 b；绝对值是平行四边形面积。
// 参数 a,b 为向量；返回有向叉积标量，不修改输入。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
// 参数 a 为向量；返回平方长度，不开方且不修改输入。
ld norm2(Point a) { return dot(a, a); }
// 参数 a 为向量；返回非负欧氏长度，不修改输入。
ld length(Point a) { return sqrtl(norm2(a)); }

// 参数 a 为向量、angle 为弧度；返回逆时针旋转后的新向量，不改输入。
Point rotate(Point a, ld angle) {
    // angle 使用弧度，正值按数学坐标系逆时针旋转；屏幕 y 轴向下时视觉方向相反。
    ld c = cosl(angle), s = sinl(angle);
    return {a.x * c - a.y * s, a.x * s + a.y * c};
}
```

**易错点：**

1. 角度函数使用弧度；角度制需乘 `PI/180`。
2. 浮点判零用 `sgn`，不要直接写 `x == 0`。
3. 除以向量长度前要先判断是否为零向量。

**参考：**

- [OI Wiki：二维计算几何基础](https://oi-wiki.org/geometry/2d/)

## 9.2 叉积与方向判断

**适用范围：** 整数点的精确方向、共线和闭线段包含判断；坐标差及叉积须能由 signed `__int128` 表示。
**能做什么：** `cross` 与 `orientation` 为 $O(1)$；`onSegment` 为 $O(1)$ 且端点包含。
**输入 / 输出：** `cross(a,b)` 返回向量叉积；三点重载返回 `(b-a)x(c-a)`；`orientation` 输出 1/0/-1；`onSegment(a,b,p)` 返回布尔值。输入点为 `long long` 整数坐标。

**用法：**

- `orientation(a,b,c)` 返回 1、0、-1，分别表示左转、共线、右转。
- `onSegment(a,b,p)` 判断 `p` 是否在闭线段 `ab` 上，包含端点。
- 模板适用于整数输入，坐标类型为 `long long`。
- 浮点坐标应把叉积传给 9.1 的 `sgn`，并用 EPS 判断范围。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint {
    ll x = 0, y = 0;
};

// 两向量叉积；整数坐标下精确判号，乘法提升到 i128 以避免 long long 溢出。
// 参数 a,b 为整数向量；返回叉积，结果须可由 signed i128 表示。
i128 cross(IPoint a, IPoint b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

// 参数 a,b,c 为整数点；返回 (b-a)x(c-a)，精确结果须在 signed i128 范围内。
i128 cross(IPoint a, IPoint b, IPoint c) {
    // 返回 (b-a)x(c-a)：正为 a->b 到 a->c 左转，负为右转，零为共线。
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

// 参数为三点；返回左转 1、共线 0、右转 -1，不修改输入。
int orientation(IPoint a, IPoint b, IPoint c) {
    i128 value = cross(a, b, c);
    return (value > 0) - (value < 0);
}

// 参数 a,b 定义闭线段、p 为查询点；共线且在包围盒内（含端点）时返回 true。
bool onSegment(IPoint a, IPoint b, IPoint p) {
    // 闭线段判定：共线还不够，还要落在两端点的横纵坐标包围盒内；端点算在线。
    return orientation(a, b, p) == 0 &&
           min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
           min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
```

**易错点：**

1. 三点顺序决定叉积符号，交换两个点会反号。
2. 共线不等于在线段上，还需检查横纵坐标范围。
3. 三点叉积先把坐标提升到 `__int128` 再相减；若坐标接近 `long long` 极限，叉积本身仍可能越界。

**参考：**

- [OI Wiki：极坐标与叉积](https://oi-wiki.org/geometry/2d/)

## 9.3 直线交点与线段相交

**适用范围：** 浮点直线唯一交点与两条闭线段相交判断；直线方向向量平方长度须大于 EPS，几何判断采用绝对 EPS=1e-12。
**能做什么：** 所有单次操作 $O(1)$；端点接触、共线重叠均算线段相交。
**输入 / 输出：** `lineIntersection(p,v,q,w,out)` 对 `p+t*v` 与 `q+s*w` 成功时写交点并返回 true；平行/重合返回 false 且 out 不变。`segmentsIntersect(a,b,c,d)` 返回是否共享点。

**用法：**

- `lineIntersection(p,v,q,w,out)` 求两无限直线唯一交点。
- 返回 `false` 表示平行或重合，此时 `out` 无效。
- `segmentsIntersect(a,b,c,d)` 判断两条闭线段是否有公共点。
- 若整数输入只需判断相交，优先使用 9.2 的整数叉积改写，结果精确。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;
const ld EPS = 1e-12L;

// EPS 是绝对误差阈值；整数输入且只判相交时应改用 i128 叉积以得到精确结果。
// 参数 x 为浮点量；按本节绝对 EPS 返回 -1/0/1。
int sgn(ld x) { return (x > EPS) - (x < -EPS); }

struct Point {
    ld x = 0, y = 0;
    // 参数 p 为向量；返回坐标和的新值，不改操作数。
    Point operator+(Point p) const { return {x + p.x, y + p.y}; }
    // 参数 p 为向量；返回 this-p 的新值，不改操作数。
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
    // 参数 k 为实数；返回按 k 缩放的新向量，不改 this。
    Point operator*(ld k) const { return {x * k, y * k}; }
};

// 参数 a,b 为向量；返回浮点有向叉积，不修改输入。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
// 参数为三点；返回 (b-a)x(c-a)，供方向判定使用。
ld cross(Point a, Point b, Point c) { return cross(b - a, c - a); }

// 参数给出 p+t*v、q+s*w 且方向非零；成功写 out 返回 true，平行/重合返回 false 且 out 不变。
bool lineIntersection(Point p, Point v, Point q, Point w, Point& out) {
    // 两条无限直线分别是 p+t*v、q+s*w；v、w 必须是非零方向向量。
    ld denominator = cross(v, w);
    // 叉积近零包含“平行不重合”和“整条重合”，二者都没有唯一交点。
    if (sgn(denominator) == 0) return false;
    // 由 (q-p)xw=t*(v x w) 解出参数 t；交换叉积顺序会把符号写反。
    ld t = cross(q - p, w) / denominator;
    out = p + v * t;
    return true;
}

// 参数 a,b 定义闭线段；p 在线段上或端点处返回 true，a==b 时只包含该点。
bool onSegment(Point a, Point b, Point p) {
    // 使用闭区间语义并包含端点；退化线段 a==b 时仅该点自身通过判定。
    return sgn(cross(a, b, p)) == 0 &&
           sgn((p.x - a.x) * (p.x - b.x)) <= 0 &&
           sgn((p.y - a.y) * (p.y - b.y)) <= 0;
}

// 参数为两条闭线段端点；返回是否共享一点，端点接触和共线重叠都算相交。
bool segmentsIntersect(Point a, Point b, Point c, Point d) {
    // c1、c2 是 c、d 相对有向直线 a->b 的方向；异号才是严格跨越。
    int c1 = sgn(cross(a, b, c)), c2 = sgn(cross(a, b, d));
    int c3 = sgn(cross(c, d, a)), c4 = sgn(cross(c, d, b));
    if (c1 * c2 < 0 && c3 * c4 < 0) return true;
    return (c1 == 0 && onSegment(a, b, c)) ||
           (c2 == 0 && onSegment(a, b, d)) ||
           (c3 == 0 && onSegment(c, d, a)) ||
           (c4 == 0 && onSegment(c, d, b));
}
```

**易错点：**

1. “严格相交”不含端点和重合；本模板判断的是闭线段有公共点。
2. 平行直线可能重合，`false` 不等于“没有公共点”。
3. 退化线段 `a==b` 仍可由 `segmentsIntersect` 判断，但不能作为直线方向。

**参考：**

- [OI Wiki：直线与线段相关](https://oi-wiki.org/geometry/2d/)

## 9.4 距离与投影

**适用范围：** 实数坐标的垂足、点到无限直线或闭线段的距离；直线端点不同，短线段按 EPS² 退化处理。
**能做什么：** 每次投影/距离 $O(1)$；线段投影参数截到 `[0,1]`。
**输入 / 输出：** `projectionOnLine/distanceToLine(p,a,b)` 以 a、b 定义无限直线且要求 `a!=b`；`closestPointOnSegment` 退化时返回 a；距离函数返回非负 `long double`。

**用法：**

- `projectionOnLine(p,a,b)` 返回 `p` 到无限直线 `ab` 的垂足。
- `distanceToLine` 返回点到无限直线距离。
- `closestPointOnSegment` 返回闭线段上离 `p` 最近的点。
- `distanceToSegment` 同时处理垂足在线段外和 `a==b`。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;
const ld EPS = 1e-12L;

struct Point {
    ld x = 0, y = 0;
    // 参数 p 为向量；返回坐标和的新值，不改操作数。
    Point operator+(Point p) const { return {x + p.x, y + p.y}; }
    // 参数 p 为向量；返回 this-p 的新值，不改操作数。
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
    // 参数 k 为缩放因子；返回新向量，不改 this。
    Point operator*(ld k) const { return {x * k, y * k}; }
};

// 参数 a,b 为向量；返回点积标量。
ld dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
// 参数 a 为向量；返回平方长度。
ld norm2(Point a) { return dot(a, a); }
// 参数为两点；返回非负欧氏距离，平方量以 long double 计算。
ld distance(Point a, Point b) { return sqrtl(norm2(a - b)); }

// 参数 p 为查询点、a!=b 定义无限直线；返回垂足，不限制投影参数。
Point projectionOnLine(Point p, Point a, Point b) {
    // 求无限直线参数 t；前提 a!=b，否则 norm2(b-a)=0。线段版本在下方单独处理退化。
    Point v = b - a;
    return a + v * (dot(p - a, v) / norm2(v));
}

// 参数 p 为查询点、a!=b 定义直线；返回到无限直线的非负距离。
ld distanceToLine(Point p, Point a, Point b) {
    return distance(p, projectionOnLine(p, a, b));
}

// 参数 p 为查询点、a,b 为线段端点；返回最近点，EPS² 内退化段返回 a。
Point closestPointOnSegment(Point p, Point a, Point b) {
    Point v = b - a;
    ld length2 = norm2(v);
    // EPS^2 与平方长度同量纲；退化或极短线段按单点 a 处理。
    if (length2 < EPS * EPS) return a;
    ld t = dot(p - a, v) / length2;
    // 无限直线投影参数截到 [0,1]，分别对应端点 a、b 和线段内部。
    t = max((ld)0, min((ld)1, t));
    return a + v * t;
}

// 参数 p 为查询点、a,b 为闭线段端点；返回非负距离，退化段按点 a 计算。
ld distanceToSegment(Point p, Point a, Point b) {
    return distance(p, closestPointOnSegment(p, a, b));
}
```

**易错点：**

1. 点到直线与点到线段不同；线段要截断投影参数。
2. `a==b` 时分母为零，必须退化为点距离。
3. 比较距离大小时可优先比较平方距离，减少开方误差与开销。

**参考：**

- [OI Wiki：距离](https://oi-wiki.org/geometry/distance/)

## 9.5 多边形面积

**适用范围：** 顶点按简单多边形边界顺序排列的整数多边形；坐标差、叉积和总和都须能放进 signed `__int128`。
**能做什么：** 鞋带公式一次遍历，$O(n)$ 时间、$O(1)$ 额外空间；精确得到有向二倍面积。
**输入 / 输出：** `signedDoubleArea(polygon)` 不修改输入，首点不需重复；返回逆时针为正的二倍面积，少于 3 点或空点集返回 0。

**用法：**

- 顶点必须按多边形边界的顺时针或逆时针顺序给出。
- 首点无需在数组末尾重复，模板用取模闭合末边。
- `signedDoubleArea` 返回整数有向二倍面积；实际面积取绝对值除以 2。
- 若答案可能为半整数，可输出 `abs(value)/2` 加 `.0` 或 `.5`。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint { ll x = 0, y = 0; };

// 单项叉积提升到 i128；若坐标约在 1e18 量级，多个叉积之和仍可能超过 i128。
// 参数 a,b 为整数位置向量；返回叉积，signed i128 须容纳乘积差。
i128 cross(IPoint a, IPoint b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

// 参数为按边界顺序且首点不重复的顶点列；返回有向二倍面积，逆时针为正，不改输入。
i128 signedDoubleArea(const vector<IPoint>& polygon) {
    // 顶点须按边界顺序给出且不重复首点；返回有向二倍面积，逆时针为正。
    i128 sum = 0;
    int n = (int)polygon.size();
    // (i+1)%n 自动补上末点到首点的闭合边；n<3 时自然得到退化面积 0。
    for (int i = 0; i < n; ++i)
        sum += cross(polygon[i], polygon[(i + 1) % n]);
    return sum;
}
```

**易错点：**

1. 无序点集不能直接代入公式，必须先得到边界顺序。
2. 有向面积可能为负；只求面积时取绝对值。
3. 面积公式返回二倍面积，别忘记除以 2。

**参考：**

- [OI Wiki：多边形面积](https://oi-wiki.org/geometry/2d/)

## 9.6 点在多边形内

**适用范围：** 顶点顺序给定的简单浮点多边形；采用绝对 EPS=1e-12。自交多边形不适用。
**能做什么：** 射线奇偶规则单次 $O(n)$、额外空间 $O(1)$，并区分边界。
**输入 / 输出：** `pointInPolygon(polygon,p)` 返回 OUTSIDE/BOUNDARY/INSIDE；空点列返回 OUTSIDE，边界按闭边判定。坐标尺度过大时需调整 EPS。

**用法：**

- `pointInPolygon` 返回 `OUTSIDE`、`BOUNDARY` 或 `INSIDE`。
- 多边形可以顺时针或逆时针，首点无需重复。
- 模板使用浮点 EPS，适合一般实数坐标。
- 整数坐标且要求精确时，可用 `__int128` 叉积实现相同的奇偶规则。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;
const ld EPS = 1e-12L;

// 参数 x 为浮点量；按本节绝对 EPS 返回 -1/0/1。
int sgn(ld x) { return (x > EPS) - (x < -EPS); }
struct Point {
    ld x = 0, y = 0;
    // 参数 p 为向量；返回 this-p 的新值，不改操作数。
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
};
// 参数 a,b 为向量；返回有向叉积标量。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }

// 参数 a,b 定义闭边、p 为点；共线且落在包围盒内（含端点）时返回 true。
bool onSegment(Point a, Point b, Point p) {
    // 边界优先单独判定，避免射线与水平边或顶点重合时归属不明确。
    return sgn(cross(b - a, p - a)) == 0 &&
           sgn((p.x - a.x) * (p.x - b.x)) <= 0 &&
           sgn((p.y - a.y) * (p.y - b.y)) <= 0;
}

enum PointLocation { OUTSIDE, BOUNDARY, INSIDE };

// 参数是按边界顺序的简单多边形和查询点；返回 OUTSIDE/BOUNDARY/INSIDE，不修改输入。
PointLocation pointInPolygon(const vector<Point>& polygon, Point p) {
    // 适用于顶点按边界排列的简单多边形；返回值明确区分边界与内部。
    bool inside = false;
    int n = (int)polygon.size();
    for (int i = 0; i < n; ++i) {
        Point a = polygon[i], b = polygon[(i + 1) % n];
        if (onSegment(a, b, p)) return BOUNDARY;
        // 半开高度条件保证射线经过顶点时只让相邻两边中的一条计数。
        bool straddles = (a.y > p.y) != (b.y > p.y);
        if (straddles) {
            ld intersectionX = a.x + (b.x - a.x) *
                (p.y - a.y) / (b.y - a.y);
            // 只统计查询点右侧交点；每跨过一次边界就翻转内外奇偶性。
            if (intersectionX > p.x + EPS) inside = !inside;
        }
    }
    return inside ? INSIDE : OUTSIDE;
}
```

**易错点：**

1. 射线恰过顶点时不能把相邻两条边重复计数；模板用半开高度条件处理。
2. 必须先判断边界，否则题意中的边界归属会混乱。
3. 自交多边形的“内部”定义不同，本模板按简单多边形使用。

**参考：**

- [OI Wiki：判断一个点是否在多边形内部](https://oi-wiki.org/geometry/2d/)

## 9.7 凸包

**适用范围：** 无序整数点集求凸包；输入重复点可有，坐标差与叉积必须适配 signed `__int128`。
**能做什么：** Andrew 单调链 $O(n\log n)$ 时间、$O(n)$ 空间；删去边上中间共线点。
**输入 / 输出：** `convexHull(points)` 按值接收并排序去重，返回逆时针点列且不重复首点；空集空返回、单点保留、全共线只返两端点。

**用法：**

- `convexHull(points)` 返回逆时针顶点，起点为字典序最小点。
- 返回结果不重复首点；重复输入点会先被删除。
- 全部共线时只返回两个端点；单点时返回该点。
- 若要保留凸包边上的所有共线点，把弹栈条件改为 `< 0`，并谨慎处理全共线情形。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint {
    ll x = 0, y = 0;
    // 参数 p 为另一整数点；按 x 再 y 严格字典序比较，用于排序，不改点。
    bool operator<(const IPoint& p) const { return tie(x, y) < tie(p.x, p.y); }
    // 参数 p 为另一整数点；仅两坐标完全相等时返回 true。
    bool operator==(const IPoint& p) const { return x == p.x && y == p.y; }
};

// 参数为整数点；返回 (b-a)x(c-a)，坐标差和乘积差须在 signed i128 范围。
i128 cross(IPoint a, IPoint b, IPoint c) {
    // (b-a)x(c-a)>0 是严格左转；整数 i128 判号不需要 EPS。
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

// 参数 points 按值接收，可乱序/重复；返回逆时针凸包且不重复首点，删去边上中间共线点。
vector<IPoint> convexHull(vector<IPoint> points) {
    // 输入可无序且可重复；输出 0-based vector 中按逆时针排列，不重复首点。
    sort(points.begin(), points.end());
    points.erase(unique(points.begin(), points.end()), points.end());
    if (points.size() <= 1) return points;

    vector<IPoint> hull;
    for (const IPoint& p : points) {
        // 维护下凸壳连续三点严格左转；<=0 会同时删除右转和边上共线中间点。
        // 若题目要求保留边界共线点，改为 <0，并额外处理全部共线的输入。
        while (hull.size() >= 2 &&
               cross(hull[hull.size() - 2], hull.back(), p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    size_t lowerSize = hull.size();
    // 逆序扫描构造上凸壳；lowerSize 是边界，防止弹掉已完成的整条下凸壳。
    for (int i = (int)points.size() - 2; i >= 0; --i) {
        const IPoint& p = points[i];
        while (hull.size() > lowerSize &&
               cross(hull[hull.size() - 2], hull.back(), p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    // 最后压入的是起点副本，删除它以保持“首点不重复”的返回约定。
    hull.pop_back();
    return hull;
}
```

**易错点：**

1. 必须先去重，否则相同点会破坏转向判断。
2. `<= 0` 会删除边上共线点，改成 `< 0` 的语义不同。
3. 返回值不含重复首点，遍历边时应使用 `(i+1)%n`。

**参考：**

- [OI Wiki：凸包](https://oi-wiki.org/geometry/convex-hull/)

## 9.8 旋转卡壳：凸包直径

**适用范围：** 点集已是逆时针凸包且不重复首点；叉积、绝对值及平方距离全部须适配 signed `__int128`。
**能做什么：** 旋转卡壳 $O(h)$ 时间、$O(1)$ 额外空间；含建凸包总计 $O(n\log n)$。
**输入 / 输出：** `convexDiameterSquared(hull)` 返回最远点对的平方距离；0/1 个点返回 0，2 点返回唯一距离。`toString` 仅接受非负值。

**用法：**

- 输入 `hull` 必须是逆时针严格凸包，且不重复首点，可直接接 9.7 输出。
- `convexDiameterSquared` 返回最大欧氏距离的平方。
- 一个点时答案为 0；两个点时直接返回二者平方距离。
- 需要实际距离时转成 `long double` 后开方；需要点对可在更新最大值时同步记录下标。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint {
    ll x = 0, y = 0;
};

// 参数为整数点；返回有向叉积，调用者保证差值和乘积在 signed i128 范围。
i128 cross(IPoint a, IPoint b, IPoint c) {
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

// 参数为两整数点；返回平方距离，坐标差、平方和须可由 signed i128 表示。
i128 distanceSquared(IPoint a, IPoint b) {
    // 差值和平方均在 i128 中完成；返回平方距离，避免开方误差。
    i128 dx = (i128)a.x - b.x;
    i128 dy = (i128)a.y - b.y;
    return dx * dx + dy * dy;
}

// 参数 x 不得是 signed i128 最小值；返回 |x|，不修改外部状态。
i128 abs128(i128 x) { return x < 0 ? -x : x; }

// 参数是逆时针且不重复首点凸包；返回最远平方距离，0/1 点为 0、2 点为点距。
i128 convexDiameterSquared(const vector<IPoint>& hull) {
    // 前提：hull 是逆时针严格凸包且不重复首点；可直接接 convexHull 的输出。
    int n = (int)hull.size();
    if (n <= 1) return 0;
    if (n == 2) return distanceSquared(hull[0], hull[1]);

    i128 answer = 0;
    int j = 1;
    for (int i = 0; i < n; ++i) {
        int nextI = (i + 1) % n;
        // 固定有向边 i->nextI，面积随对踵点前进先增后减，因此 j 全程只向前转。
        // 使用严格 > 可停在面积平台任一端；随后同时检查边的两个端点与 j。
        while (abs128(cross(hull[i], hull[nextI], hull[(j + 1) % n])) >
               abs128(cross(hull[i], hull[nextI], hull[j]))) {
            j = (j + 1) % n;
        }
        answer = max(answer, distanceSquared(hull[i], hull[j]));
        answer = max(answer, distanceSquared(hull[nextI], hull[j]));
    }
    return answer;
}

// 参数 x>=0；返回十进制字符串，仅转换非负距离值，不修改输入。
string toString(i128 x) {
    // 本章仅用它输出非负平方距离；若复用于有向面积，需先处理负号和最小值。
    if (x == 0) return "0";
    string s;
    while (x > 0) {
        s.push_back(char('0' + x % 10));
        x /= 10;
    }
    reverse(s.begin(), s.end());
    return s;
}
```

**易错点：**

1. 旋转卡壳不能直接用于未排序点集；必须先求凸包。
2. 凸包含重复首点或大量边上共线点时，指针逻辑容易出错。
3. `__int128` 不能直接用 `cout` 输出，模板提供了非负整数转换函数。

**参考：**

- [OI Wiki：旋转卡壳](https://oi-wiki.org/geometry/rotating-calipers/)


## 9.9 圆与直线、圆与圆

**适用范围：** 圆半径非负，直线方向向量平方长度须大于 EPS；圆心、半径均为 `long double`，判别式使用绝对 EPS=1e-12。
**能做什么：** 求直线/圆及圆/圆交点每次 $O(1)$；切点只返回一个点。
**输入 / 输出：** `lineCircleIntersections(p,v,c)` 返回 0/1/2 个点；`dot(v,v)<=EPS` 的近零方向与无交点都返回空。`circleIntersections(a,b)` `d<=EPS` 的近同心情形（包括重合圆的无限交点情形）返回空；相切返回一个点，分离/包含返回空。

```cpp
struct Circle {
    Point o;
    long double r;
};
// 参数 p,v 定义直线且 dot(v,v)>EPS，圆半径非负；返回 0/1/2 交点，近零方向返回空。
vector<Point> lineCircleIntersections(Point p,Point v,Circle c) {
    long double vv=dot(v,v);
    if (vv <= EPS) return {};
    Point foot=p+v*(dot(c.o-p,v)/vv);
    long double h2=c.r*c.r-dot(foot-c.o,foot-c.o);
    if (h2 < -EPS) return {};
    if (h2 <= EPS) return {foot};
    Point off=v*(sqrtl(max((long double)0,h2)/vv));
    return {foot-off,foot+off};
}
// 参数是半径非负的两圆；返回 0/1/2 交点，`d<=EPS` 的近同心情形（含重合圆）返回空，切点只返一次。
vector<Point> circleIntersections(Circle a,Circle b) {
    // 先判相离、包含、同心等退化，再计算垂足与偏移。
    Point dvec=b.o-a.o;
    long double d=length(dvec);
    if(d<=EPS) {
        return {};
    }
    // 同心：无交点或无穷多交点，均返回空
    if (d > a.r + b.r + EPS || d < fabsl(a.r - b.r) - EPS) return {};
    long double x = (a.r * a.r - b.r * b.r + d * d) / (2 * d);
    long double h2 = a.r * a.r - x * x;
    Point base = a.o + dvec * (x / d);
    if (h2 <= EPS) return {base};
    Point perp{-dvec.y / d, dvec.x / d};
    Point off = perp * sqrtl(max((long double) 0, h2));
    return {base - off, base + off};
}
```

坑：零方向向量不是直线；同心圆要区分无交点与无限交点时应另设返回状态；先用 EPS 判定再对根号内取 `max(0,·)`。

## 9.10 整数几何方向模板

**适用范围：** 整数坐标下精确判方向和点在线段上；坐标差及叉积需不超出 signed `__int128`。
**能做什么：** 叉积、符号和闭线段判断各 $O(1)$，无浮点 EPS。
**输入 / 输出：** `crossInt(a,b,c)` 返回三点有向叉积；`signInt(x)` 返回 -1/0/1；`onSegmentInt(p,a,b)` 端点包含并返回布尔值。距离平方需另行检查 i128 范围。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct IPoint {
    ll x,y;
};
// 参数为整数点；返回 (b-a)x(c-a)，坐标差和叉积须在 signed i128 范围。
__int128 crossInt(IPoint a, IPoint b, IPoint c) {
    // 转换发生在减法之前，避免 long long 坐标差先溢出。
    __int128 abx = (__int128)b.x - a.x, aby = (__int128)b.y - a.y;
    __int128 acx = (__int128)c.x - a.x, acy = (__int128)c.y - a.y;
    return abx * acy - aby * acx;
}
// 参数 x 为 signed i128；返回 -1/0/1，不修改输入。
int signInt(__int128 x) {
    return (x>0)-(x<0);
}
// 参数 p 为查询点、a,b 为线段端点；闭线段含端点判定，crossInt 不得溢出。
bool onSegmentInt(IPoint p,IPoint a,IPoint b) {
    return crossInt(a, b, p) == 0
        && min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x)
        && min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
```

坑：`__int128` 输出需自行转换；距离平方也可能超过 `long long`；真正交点通常是分数，不能强行存整数点。
