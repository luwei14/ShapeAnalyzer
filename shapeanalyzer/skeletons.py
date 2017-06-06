from shapes import *
from utilities import TinyQueue

class StraightSkeleton:
    def __init__(self, poly):
        self.poly = poly

    def skeleton(self):
        lav = _LAV()
        lav.form_points(self.poly.points)
        slav = [lav]
        vetQue = TinyQueue(compare=lambda a,b: a.dis - b.dis)
        for lav in slav:
            for v in lav:
                #print v.is_reflex
                vetQue.push(v.event(lav))
        skeles =[]
        while vetQue.length:
            evt = vetQue.pop()
            if evt.type == 0:
                if evt.Va.processed and evt.Vb.processed:
                    continue
                # peaks
                if evt.Va.prev.prev == evt.Vb:
                    skeles.append([evt.inter,evt.Va.prev.pt])
                    skeles.append([evt.inter, evt.Va.pt])
                    skeles.append([evt.inter, evt.Vb.pt])
                    evt.Va.processed = True
                    evt.Vb.processed = True
                    evt.Va.prev.processed = True
                    continue

                skeles.append([evt.inter, evt.Va.pt])
                skeles.append([evt.inter, evt.Vb.pt])
                evt.Va.processed = True
                evt.Vb.processed = True
                
                nVet = _Vertex(evt.inter, evt.Va.pedge, evt.Vb.nedge)
                evt.Va.prev.next = nVet
                evt.Vb.next.prev = nVet
                nVet.next = evt.Vb.next
                nVet.prev = evt.Va.prev
                nevt = nVet.near_bi()
                if nevt:
                    vetQue.push(nevt)

            if evt.type == 1:
                if evt.Vs.processed:
                    continue
                '''
                if evt.Vs.prev.prev == evt.Vy:
                    skeles.append([evt.inter, evt.Vs.pt])
                    skeles.append([evt.inter, evt.Vx.pt])
                    skeles.append([evt.inter, evt.Vy.pt])
                    evt.Vs.processed = True
                    evt.Vx.processed = True
                    evt.Vy.processed = True
                    continue
                '''
                evt.Vs.processed = True
                skeles.append([evt.inter, evt.Vs.pt])
                V1 = _Vertex(evt.inter, evt.Vs.pedge, evt.Vy.pedge)
                V2 = _Vertex(evt.inter, evt.Vx.nedge, evt.Vs.nedge)
                V1.next = evt.Vy
                V1.prev = evt.Vs.prev
                evt.Vs.prev.next = V1
                evt.Vy.prev = V1

                V2.next = evt.Vs.next
                V2.prev = evt.Vx
                evt.Vs.next.prev = V2
                evt.Vx.next = V2
                
                for d in vetQue.data:
                    if d.type == 0:
                        continue
                    if d.Vx == evt.Vs and d.Vy == evt.Vs.next:
                        d.Vx = V2
                    if d.Vx == evt.Vs.prev and d.Vy == evt.Vs:
                        d.Vy = V1
                
                v1Evt = V1.near_bi()
                if v1Evt:
                    vetQue.push(v1Evt)
                v2Evt = V2.near_bi()
                if v2Evt:
                    vetQue.push(v2Evt)
                '''
                if V1.prev.prev == V1:
                    skeles.append([V1.pt, V1.prev.pt])
                    V1.processed = True
                    V1.prev.processed = True
                else:
                    v1Evt = V1.near_bi()
                    if v1Evt:
                        vetQue.push(v1Evt)
                if V2.prev.prev == V2:
                    skeles.append([V2.pt, V2.prev.pt])
                    V2.processed = True
                    V2.prev.processed = True
                else:
                    v2Evt = V2.near_bi()
                    if v2Evt:
                        vetQue.push(v2Evt)'''
        print len(skeles)
        return skeles

class _Vertex:
    def __init__(self, pt, pedge, nedge):
        self.pt = pt
        self.pedge = pedge
        self.nedge = nedge
        self.prev = None
        self.next = None
        self.is_reflex = self.pedge.vector().cross(self.nedge.vector()) < 0
        #print self.is_reflex
        bv = -self.pedge.vector().normalize() + self.nedge.vector().normalize()
        self.bisector = Ray(self.pt,-bv.normalize()) if self.is_reflex else Ray(self.pt,bv.normalize())
        self.processed=False

    def near_bi(self):
        b = self.bisector
        pb = self.prev.bisector
        nb = self.next.bisector
        pi = b.intersection(pb)
        ni = b.intersection(nb)
        pdis = self.pedge.height(pi) if pi else float("inf")
        ndis = self.nedge.height(ni) if ni else float("inf")
        if pdis == float("inf") and ndis == float("inf"):
            #print "all no inter"
            return None
        
        if pdis < ndis:
            evt_edge = _Event({"inter":pi, "Va":self.prev, "Vb":self, "dis":pdis,"type":0})
            return evt_edge
        else:
            evt_edge = _Event({"inter":ni, "Va":self, "Vb":self.next, "dis":ndis,"type":0})
            return evt_edge
        
    def event(self, lav):
        evts = TinyQueue(compare=lambda a, b: a.dis - b.dis)
        # split event
        if self.is_reflex:
            #print "is reflex", self.is_reflex
            for v in lav:
                edge = v.nedge
                pvedge = self.pedge
                nvedge = self.nedge
                bi = v.bisector
                bj = v.next.bisector
                l1 = Line(edge.fpt, edge.vector())
                l2 = Ray(self.pt, pvedge.vector())
                l3 = Ray(self.pt, -nvedge.vector())
                p0 = l1.intersection_ray(l2)
                p1 = l1.intersection_ray(l3)
                if p0 and p1:
                    cpt = Point((p0.x+p1.x+self.pt.x)/3.0, (p0.y+p1.y+self.pt.y)/3.0)
                    tedge = edge.vector().cross(Vector2(cpt.x - edge.fpt.x, cpt.y - edge.fpt.y)) > 0
                    tbi = bi.direction.cross(Vector2(cpt.x - bi.origin.x, cpt.y - bi.origin.y)) < 0
                    tbj = bj.direction.cross(Vector2(cpt.x - bj.origin.x, cpt.y - bj.origin.y)) > 0
                    valid = tedge and tbi and tbj
                    if valid:
                        evt_split =_Event( {"inter":cpt, "dis": edge.height(cpt),"type":1, "Vs":self, "Vx":v, "Vy":v.next})
                        evts.push(evt_split)
        # edge event
        b = self.bisector
        pb = self.prev.bisector
        nb = self.next.bisector
        pi = b.intersection(pb)
        ni = b.intersection(nb)
        if pi:
            pdis = self.pedge.height(pi)
            evt_edge = _Event({"inter":pi, "Va":self.prev, "Vb":self, "dis":pdis,"type":0})
            evts.push(evt_edge)
        if ni:
            ndis = self.nedge.height(ni) if ni else float("inf")
            evt_edge = _Event({"inter":ni, "Va":self, "Vb":self.next, "dis":ndis,"type":0})
            evts.push(evt_edge)
        return evts.pop()

class _Event:
    def __init__(self, params):
        for k, v in params.items():
            setattr(self, k, v)
    
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
