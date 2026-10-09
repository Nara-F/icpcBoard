
# 9. 计算几何

本章采用两套明确的数值约定：含交点、距离、投影时使用 `long double` 和 `EPS = 1e-12L`；输入为整数且只判断方向、求凸包或平方距离时，保留整数坐标并用 `__int128` 计算叉积。浮点数只用带 EPS 的符号函数比较，不能直接用于有序容器的“近似相等”比较。

## 9.1 点、向量与基本运算

**问题与思路：** 二维点也可视作从原点出发的向量；加减表示平移，点积处理夹角与投影，叉积处理有向面积与方向。每次运算均为 $O(1)$、空间 $O(1)$。涉及除法、旋转或距离时用 `long double`，判断零使用统一 EPS。

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
int sgn(ld x) {
    if (x > EPS) return 1;
    if (x < -EPS) return -1;
    return 0;
}

struct Point {
    // 浮点点也作为向量使用；b-a 表示从 a 指向 b，坐标下标不涉及点编号。
    ld x = 0, y = 0;
    Point operator+(const Point& p) const { return {x + p.x, y + p.y}; }
    Point operator-(const Point& p) const { return {x - p.x, y - p.y}; }
    Point operator*(ld k) const { return {x * k, y * k}; }
    Point operator/(ld k) const { return {x / k, y / k}; }
};

ld dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
// cross(a,b)>0 表示从向量 a 逆时针转到 b；绝对值是平行四边形面积。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
ld norm2(Point a) { return dot(a, a); }
ld length(Point a) { return sqrtl(norm2(a)); }

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

**问题与思路：** $cross(b-a,c-a)$ 的正、零、负分别表示从 `ab` 转向 `ac` 为逆时针、共线、顺时针，也等于三角形有向面积的两倍。每次 $O(1)$。整数坐标应使用精确叉积；若坐标乘积可能超过 `long long`，用 `__int128`。

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
i128 cross(IPoint a, IPoint b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

i128 cross(IPoint a, IPoint b, IPoint c) {
    // 返回 (b-a)x(c-a)：正为 a->b 到 a->c 左转，负为右转，零为共线。
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

int orientation(IPoint a, IPoint b, IPoint c) {
    i128 value = cross(a, b, c);
    return (value > 0) - (value < 0);
}

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

**问题与思路：** 直线写成 `p+t*v`。两方向叉积非零时有唯一交点；两闭线段相交则两端点分别位于对方直线两侧，或存在端点共线且落在线段上。判断与求交均为 $O(1)$。浮点模板含端点接触，平行重合时不返回唯一交点。

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
int sgn(ld x) { return (x > EPS) - (x < -EPS); }

struct Point {
    ld x = 0, y = 0;
    Point operator+(Point p) const { return {x + p.x, y + p.y}; }
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
    Point operator*(ld k) const { return {x * k, y * k}; }
};

ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
ld cross(Point a, Point b, Point c) { return cross(b - a, c - a); }

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

bool onSegment(Point a, Point b, Point p) {
    // 使用闭区间语义并包含端点；退化线段 a==b 时仅该点自身通过判定。
    return sgn(cross(a, b, p)) == 0 &&
           sgn((p.x - a.x) * (p.x - b.x)) <= 0 &&
           sgn((p.y - a.y) * (p.y - b.y)) <= 0;
}

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

**问题与思路：** 点到直线的投影参数为 $t=dot(p-a,b-a)/|b-a|^2$；直线投影不限制 $t$，线段最近点需把 $t$ 截到 `[0,1]`。单次时间、空间均为 $O(1)$。模板使用浮点；退化线段按单点处理。

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
    Point operator+(Point p) const { return {x + p.x, y + p.y}; }
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
    Point operator*(ld k) const { return {x * k, y * k}; }
};

ld dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
ld norm2(Point a) { return dot(a, a); }
ld distance(Point a, Point b) { return sqrtl(norm2(a - b)); }

Point projectionOnLine(Point p, Point a, Point b) {
    // 求无限直线参数 t；前提 a!=b，否则 norm2(b-a)=0。线段版本在下方单独处理退化。
    Point v = b - a;
    return a + v * (dot(p - a, v) / norm2(v));
}

ld distanceToLine(Point p, Point a, Point b) {
    return distance(p, projectionOnLine(p, a, b));
}

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

**问题与思路：** 鞋带公式把按边界顺序排列的顶点相邻叉积求和；和的一半是有向面积，逆时针为正、顺时针为负。时间 $O(n)$、空间 $O(1)$。整数坐标可用 `__int128` 精确保存二倍面积，避免浮点误差。

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
i128 cross(IPoint a, IPoint b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

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

**问题与思路：** 射线法从查询点向右作射线，统计与多边形边界的有效交点数：奇数在内，偶数在外；先单独检查边界。对含凹多边形也适用，要求多边形简单且顶点沿边界有序。单次查询时间 $O(n)$、空间 $O(1)$。

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

int sgn(ld x) { return (x > EPS) - (x < -EPS); }
struct Point {
    ld x = 0, y = 0;
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
};
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }

bool onSegment(Point a, Point b, Point p) {
    // 边界优先单独判定，避免射线与水平边或顶点重合时归属不明确。
    return sgn(cross(b - a, p - a)) == 0 &&
           sgn((p.x - a.x) * (p.x - b.x)) <= 0 &&
           sgn((p.y - a.y) * (p.y - b.y)) <= 0;
}

enum PointLocation { OUTSIDE, BOUNDARY, INSIDE };

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

**问题与思路：** 凸包是包含点集的最小凸多边形。Andrew 算法先按 `(x,y)` 排序，再分别维护下凸壳和上凸壳，遇到非左转就弹栈。排序主导时间 $O(n\log n)$，空间 $O(n)$。模板使用整数精确叉积，并删除边上的中间共线点。

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
    bool operator<(const IPoint& p) const { return tie(x, y) < tie(p.x, p.y); }
    bool operator==(const IPoint& p) const { return x == p.x && y == p.y; }
};

i128 cross(IPoint a, IPoint b, IPoint c) {
    // (b-a)x(c-a)>0 是严格左转；整数 i128 判号不需要 EPS。
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

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

**问题与思路：** 求点集中最远点对时，先求凸包；对凸包每条边维护使三角形面积最大的对踵点，指针只绕一周。已给严格凸包时卡壳为 $O(h)$、空间 $O(1)$；连同建凸包为 $O(n\log n)$。整数坐标用 `__int128` 保存叉积与平方距离。

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

i128 cross(IPoint a, IPoint b, IPoint c) {
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

i128 distanceSquared(IPoint a, IPoint b) {
    // 差值和平方均在 i128 中完成；返回平方距离，避免开方误差。
    i128 dx = (i128)a.x - b.x;
    i128 dy = (i128)a.y - b.y;
    return dx * dx + dy * dy;
}

i128 abs128(i128 x) { return x < 0 ? -x : x; }

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

**用途 / 用法：** 求圆与直线、圆与圆的交点；切线视为一个交点，分离或内含时无交点。每次 $O(1)$。代码复用 9.1 节的 `Point`、`dot`、`length` 与 `EPS`。

```cpp
struct Circle {
    Point o;
    long double r;
};
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

整数坐标只做方向、面积和相交判定时应避免浮点。此处叉积先以 `__int128` 计算坐标差；输入规模仍须保证乘积落在 `__int128` 范围内。

```cpp
struct IPoint {
    ll x,y;
};
__int128 crossInt(IPoint a, IPoint b, IPoint c) {
    // 转换发生在减法之前，避免 long long 坐标差先溢出。
    __int128 abx = (__int128)b.x - a.x, aby = (__int128)b.y - a.y;
    __int128 acx = (__int128)c.x - a.x, acy = (__int128)c.y - a.y;
    return abx * acy - aby * acx;
}
int signInt(__int128 x) {
    return (x>0)-(x<0);
}
bool onSegmentInt(IPoint p,IPoint a,IPoint b) {
    return crossInt(a, b, p) == 0
        && min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x)
        && min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
```

坑：`__int128` 输出需自行转换；距离平方也可能超过 `long long`；真正交点通常是分数，不能强行存整数点。
