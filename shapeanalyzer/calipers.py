from utilities import *
from shapes import *
GU = GeometryUtility()

class RotatingCaliper():
    def __init__(self, points):
        self._points = points
        self._N = len(points)
        self._antipodals = None
        self._calipers()

    def _next(self, i):
        return (i+1) % self._N

    def _calipers(self):
        q = 1
        antipodals = {}
        N = len(self._points)
        for i in range(N):
            antipodals[i] = [-1,-1]
        next = self._next
        PSet = self._points
        for i in range(N):
            j = next(i)
            while GU.area2(PSet[i], PSet[j], PSet[next(q)]) > GU.area2(PSet[i], PSet[j], PSet[q]):
                q = next(q)
            antipodals[j][0] = q
            antipodals[i][1] = q
        self._antipodals = antipodals

    def AntiPodals(self):
        antis = []
        PSet = self._points
        for k, v in self._antipodals.items():
            for i in range(v[0], v[1]+1):
                if [PSet[k], PSet[i]] in antis or [PSet[i], PSet[k]] in antis:
                    continue
                antis.append([PSet[k], PSet[i]])
        return antis

    def Diameter(self):
        antis = self.AntiPodals()
        d = -1
        support = []
        for ppair in antis:
            td = ppair[0].distance(ppair[1])
            if td > d:
                d = td
                support = ppair
        return d, support

    def Width(self):
        w = float("inf")
        support = []
        for i in range(self._N):
            fpt = self._points[i]
            tpt = self._points[(i+1) % self._N]
            lseg = LineSegment(fpt, tpt)
            j = self._antipodals[i][-1]
            pt = self._points[j]
            td = lseg.distance(pt)
            if td < w:
                w = td
                support = [fpt, tpt, pt]
        return w, support