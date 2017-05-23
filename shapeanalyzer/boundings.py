from utilities import *
from calipers import *

GU = GeometryUtility()

class BoundingGeometry():
    def __init__(self, points):
        self._points = points

    def Envelope(self):
        minx, miny = self._points[0].x, self._points[0].y
        maxx, maxy = self._points[0].x, self._points[0].y
        for p in self._points:
            if p.x < minx:
                minx = p.x
            if p.x > maxx:
                maxx = p.x
            if p.y < miny:
                miny = p.y
            if p.y > maxy:
                maxy = p.y
        return [minx, miny, maxx, maxy]
    
    def ConvexHull(self):
        hull = GU.graham_scan(self._points)
        return hull

    def MinimumAreaCircle(self):
        minCir = GU.MakeCircle([self._points[0]])
        support = [0]
        i = 1
        N = len(self._points)
        while i < N:
            if i not in support:
                if minCir.incircle(self._points[i]) is False:
                    minCir, support = GU.UpdateMinCircle(support, self._points, i)
                    i = 0
                    continue
            i += 1
        return minCir, support

    def MinimumAreaRectangle(self):
        pass

    def MinimumWidthRectangle(self):
        hull = self.ConvexHull()
        rc = RotatingCaliper(hull)
        width, support = rc.Width()
        min0, max0 = 0, 0
        V0 = Vector2(support[1].x - support[0].x, support[1].y - support[0].y)
        V0.normalize()
        Vh = Vector2(-V0.y, V0.x)
        Vh.normalize()
        for i in range(len(hull)):
            Vi = Vector2(hull[i].x - support[0].x, hull[i].y - support[0].y)
            dot = V0.dot(Vi)
            if dot < min0:
                min0 = dot
            elif dot > max0:
                max0 = dot
        #area = (max0 - min0) * width
        extx = max0 - min0
        exty = width
        cx = support[0].x + (min0 + max0) / 2.0 * V0.x + width / 2.0 * Vh.x
        cy = support[0].y + (min0 + max0) / 2.0 * V0.y + width / 2.0 * Vh.y
        center = Point(cx, cy)
        rect = Rectangle(center, [V0, Vh], [extx, exty])
        return rect