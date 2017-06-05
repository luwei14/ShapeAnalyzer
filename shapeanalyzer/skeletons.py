from shapes import *
from utilities import TinyQueue

class StraightSkeleton:
    def __init__(self, poly):
        self.poly = poly

    def skeleton(self):
        pass

class _Vertex:
    def __init__(self, pt, pedge, nedge):
        self.pt = pt
        self.pedge = pedge
        self.nedge = nedge
        self.prev = None
        self.next = None
        self.is_reflex = self.pedge.vector().cross(self.nedge.vector()) < 0
        bv = -self.pedge.vector().normalize() + self.nedge.vector().normalize()
        self.bisector = Ray(self.pt,-bv.normalize()) if self.is_reflex else Ray(self.pt,bv.normalize())
        self.processed=False

class _Event:
    def __init__(self, inter, Va, Vb, dis, etype):
        self.inter = inter
        self.Va = Va
        self.Vb = Vb
        self.dis = dis
        self.etype = etype

class _LAV:
    def __init__(self):
        self.head = None
        self.len = 0

    def form_points(self, points):
        N = len(points)
        for i in range(N):
            pi = (i-1 + N) % N
            ni = (i+1 + N) % N
            ppt = points[pi]
            cpt = points[i]
            npt = points[ni]
            pedge = LineSegment(ppt, cpt)
            nedge = LineSegment(cpt, npt)
            vt = _Vertex(cpt, pedge, nedge)
            if self.head is None:
                self.head = vt
                vt.prev = vt.next = vt
            else:
                vt.next = self.head
                vt.prev = self.head.prev
                vt.prev.next = vt
                self.head.prev = vt

    def __iter__(self):
        pos = self.head
        while True:
            yield pos
            pos = pos.next
            if pos == self.head:
                raise StopIteration
