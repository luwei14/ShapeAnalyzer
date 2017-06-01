import math
from shapes import * 
from vectmat import *
class GeometryUtility():
    def ccw(self, p1, p2, p3):
        return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)

    def area2(self, p1, p2, p3):
        return math.fabs(self.ccw(p1, p2, p3))

    def graham_scan(self,points):
        num = len(points)
        cpt = Point(0.0,0.0)
        for i in range(num-2):
            if self.ccw(points[i], points[i+1], points[i+2]) != 0:
                cptx = (points[i].x + points[i+1].x + points[i+2].x) / 3
                cpty = (points[i].y + points[i+1].y + points[i+2].y) / 3
                cpt = Point(cptx, cpty)
                break
        angles = []
        distances = []
        for i in range(num):
            distances.append(cpt.distance(points[i]))
            dx = points[i].x - cpt.x
            dy = points[i].y - cpt.y
            th = math.atan2(dy, dx)
            angles.append(th)
        idx = range(num)
        data = zip(idx, points, angles, distances)
        data = sorted(data, key = lambda it: it[2])
        i = 1
        convex_runs = 0
        kk = 0
        while (convex_runs < num):
            kk +=1
            mod = len(data)
            curr = data[i][1]
            forw = data[(i+1) % mod][1]
            back = data[(i-1) % mod][1]
            if self.ccw(back, curr, forw) <= 0:
                data.pop(i)
                convex_runs = 0
            else:
                convex_runs += 1
            mod = len(data)
            i = (i+1) % mod
        return list(zip(*data)[1])
    
    def MakeCircle(self, points):
        num = len(points)
        if num == 1:
            return Circle(points[0], 0)
        elif num == 2:
            cx = (points[0].x + points[1].x) / 2.0
            cy = (points[0].y + points[1].y) / 2.0
            r = math.hypot(points[0].x - cx, points[0].y - cy)
            return Circle(Point(cx, cy), r)
        elif num == 3:
            ax = points[0].x; ay = points[0].y
            bx = points[1].x; by = points[1].y
            cx = points[2].x; cy = points[2].y
            d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
            if d == 0.0:
                print "return None, d==0"
                return None
            x = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
            y = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
            r = math.hypot(x - ax, y - ay)
            return Circle(Point(x, y), r)
        else:
            print "return None"
            return None

    def UpdateMinCircle(self, support, points, i):
        if len(support) == 1:
            pts = [points[support[0]], points[i]]
            return self.MakeCircle(pts), [support[0],i]
    
        if len(support) == 2:
            pts = [points[support[0]], points[support[1]], points[i]]
            cmin = self.MakeCircle(pts)
            #print cmin
            k = -1
            c21 = self.MakeCircle([pts[0], pts[2]])
            if c21.incircle(pts[1]) and c21.radius < cmin.radius:
                cmin = c21
                k = 0
            c22 = self.MakeCircle([pts[1], pts[2]])
            if c22.incircle(pts[0]) and c22.radius < cmin.radius:
                cmin = c22
                k = 1
            if k < 0:
                support.append(i)
                return cmin, support
            else:
                return cmin, [support[k], i]
    
        if len(support) == 3:
            pts = [points[support[0]], points[support[1]], points[support[2]]]
            cmin = Circle(Point(0,0),float('inf'))
            k = -1
            for j in range(3):
                c = self.MakeCircle([pts[j], points[i]])
                if c.incircle(pts[(j+1) % 3]) and c.incircle(pts[(j+2) % 3]) and c.radius < cmin.radius:
                    cmin = c
                    k = j
            k1, k2 = -1, -1
            for j in range(3):
                c = self.MakeCircle([pts[j], pts[(j+1) % 3], points[i]])
                if c.incircle(pts[(j+2) % 3]) and c.radius < cmin.radius:
                    cmin = c
                    k1 = j
                    k2 = (j+1) % 3
            if k1 < 0:
                support = [support[k], i]
                return cmin, support
            else:
                support = [support[k1], support[k2], i]
                return cmin, support


class TinyQueue():
    def __init__(self, data=None, compare=None):
        self.data = data[:] if data else []
        self.length = len(self.data)
        self.compare = compare if compare else self._compare
        if self.length > 0:
            i = self.length >> 1
            while i >= 0:
                self._down(i)
                i -= 1

    def _compare(self, a, b):
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0

    def push(self, item):
        self.data.append(item)
        self.length += 1
        self._up(self.length - 1)

    def pop(self):
        if self.length == 0:
            return None
        top = self.data[0]
        self.length -= 1
        if self.length > 0:
            self.data[0] = self.data[self.length]
            self._down(0)
        self.data.pop()
        return top

    def peek(self):
        if self.length == 0:
            return None
        return self.data[0]

    def _up(self, pos):
        data = self.data
        compare = self.compare
        item = data[pos]

        while pos > 0:
            pPos = (pos - 1) >> 1
            cItem = data[pPos]
            if compare(item, cItem) >= 0:
                break
            data[pos] = cItem
            pos = pPos
        data[pos] = item
    
    def _down(self, pos):
        data = self.data
        compare = self.compare
        item = data[pos]
        halflen = self.length >> 1
        while pos < halflen:
            lpos = (pos << 1) + 1
            rpos = lpos + 1
            priorItem = data[lpos]
            if rpos < self.length and compare(data[rpos], priorItem) < 0:
                lpos = rpos
                priorItem = data[rpos]

            if compare(priorItem, item) >= 0:
                break
            data[pos] = priorItem
            pos = lpos
        data[pos] = item
