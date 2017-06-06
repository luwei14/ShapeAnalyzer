import math
from vectmat import *

class Shape():
    def __init__(self):
        pass

class Point(Shape):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Point ( %s, %s )" % (str(self.x), str(self.y))

    def coords(self):
        return [self.x, self.y]


    def distance(self, p):
        return math.hypot(self.x - p.x, self.y - p.y)


class LineSegment(Shape):
    def __init__(self, fpt, tpt):
        self.fpt = fpt
        self.tpt = tpt

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "LineSegment ( %s, %s )" % (str(self.fpt), str(self.tpt))

    def coords(self):
        return [self.fpt.coords(), self.tpt.coords()]

    def length(self):
        return math.hypot(self.fpt.x - self.tpt.x, self.fpt.y - self.tpt.y)

    def height(self, pt):
        v2 = [pt.x - self.fpt.x, pt.y - self.fpt.y]
        v1 = [self.tpt.x - self.fpt.x, self.tpt.y  - self.fpt.y]
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        height = math.fabs(cross) / math.hypot(v1[0], v1[1])
        return height

    def distance(self, pt):
        op = Point(self.fpt.x, self.fpt.y)
        dx, dy = self.tpt.x - op.x, self.tpt.y - op.y

        ratio = ((pt.x - op.x) * dx + (pt.y - op.y) * dy) / (dx * dx + dy * dy)
        if ratio > 1:
            op = self.tpt
        elif ratio > 0:
            op.x += ratio * dx
            op.y += ratio * dy

        dx = pt.x - op.x
        dy = pt.y - op.y

        return math.hypot(dx, dy)

    def distance2(self, pt):
        op = Point(self.fpt.x, self.fpt.y)
        dx, dy = self.tpt.x - op.x, self.tpt.y - op.y
        #print self
        ratio = ((pt.x - op.x) * dx + (pt.y - op.y) * dy) / (dx * dx + dy * dy)
        if ratio > 1:
            op = self.tpt
        elif ratio > 0:
            op.x += ratio * dx
            op.y += ratio * dy

        dx = pt.x - op.x
        dy = pt.y - op.y

        return dx * dx + dy * dy

    def vector(self):
        return Vector2(self.tpt.x - self.fpt.x, self.tpt.y - self.fpt.y)

class Ray(Shape):
    '''
    Ray: origin point, direction vector
    '''
    def __init__(self, po, dv):
        self.origin = po
        self.direction = dv
    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Ray (%s, %s)" % (str(self.origin) , str(self.direction))

    def intersection(self, other):
        '''
            p1.x + v1.x * t1 = p2.x + v2.x * t2
            p1.y + v1.y * t1 = p2.y + v2.y * t2
                =>
            v1.x * t1 - v2.x * t2 + (p1.x - p2.x) = 0
            v1.y * t1 - v2.y * t2 + (p1.y - p2.y) = 0
                =>
            --           --  --  --     --           --
            | v1.x  -v2.x |  | t1 |     | p2.x - p1.x |
            |             |  |    |  =  |             |
            | v1.y  -v2.y |  | t2 |     | p2.y - p1.y |
            --           --  --  --     --           --
                =>
            A*x = B
        '''
        a = self.direction.x
        b = -other.direction.x
        c = self.direction.y
        d = -other.direction.y
        beta1 = -self.origin.x + other.origin.x
        beta2 = -self.origin.y + other.origin.y
        det = a * d - b * c
        if det == 0:
            #print "parallel"
            return None

        inva, invb, invc, invd = d/det, -b/det, -c/det, a/det
        t1 = inva * beta1 + invb * beta2
        t2 = invc * beta1 + invd * beta2
        if t1 < 0 or t2 < 0:
            #print "no inter"
            return None

        return Point(self.origin.x + a * t1, self.origin.y + c * t1)

class Line(Shape):
    def __init__(self, pt, direction):
        '''
        line : a point and direction Vector2
        '''
        self.origin = pt
        self.direction = direction

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Line (%s, %s)" % (str(self.origin) , str(self.direction))

    def intersection(self, other):
        '''
            p1.x + v1.x * t1 = p2.x + v2.x * t2
            p1.y + v1.y * t1 = p2.y + v2.y * t2
                =>
            v1.x * t1 - v2.x * t2 + (p1.x - p2.x) = 0
            v1.y * t1 - v2.y * t2 + (p1.y - p2.y) = 0
                =>
            --           --  --  --     --           --
            | v1.x  -v2.x |  | t1 |     | p2.x - p1.x |
            |             |  |    |  =  |             |
            | v1.y  -v2.y |  | t2 |     | p2.y - p1.y |
            --           --  --  --     --           --
                =>
            A*x = B
        '''
        a = self.direction.x
        b = -other.direction.x
        c = self.direction.y
        d = -other.direction.y
        beta1 = -self.origin.x + other.origin.x
        beta2 = -self.origin.y + other.origin.y
        det = a * d - b * c
        if det == 0:
            #print "parallel"
            return None

        inva, invb, invc, invd = d/det, -b/det, -c/det, a/det
        t1 = inva * beta1 + invb * beta2
        t2 = invc * beta1 + invd * beta2

        return Point(self.origin.x + a * t1, self.origin.y + c * t1)

    def intersection_ray(self, other):
        '''
            p1.x + v1.x * t1 = p2.x + v2.x * t2
            p1.y + v1.y * t1 = p2.y + v2.y * t2
                =>
            v1.x * t1 - v2.x * t2 + (p1.x - p2.x) = 0
            v1.y * t1 - v2.y * t2 + (p1.y - p2.y) = 0
                =>
            --           --  --  --     --           --
            | v1.x  -v2.x |  | t1 |     | p2.x - p1.x |
            |             |  |    |  =  |             |
            | v1.y  -v2.y |  | t2 |     | p2.y - p1.y |
            --           --  --  --     --           --
                =>
            A*x = B
        '''
        a = self.direction.x
        b = -other.direction.x
        c = self.direction.y
        d = -other.direction.y
        beta1 = -self.origin.x + other.origin.x
        beta2 = -self.origin.y + other.origin.y
        det = a * d - b * c
        if det == 0:
            #print "parallel"
            return None

        inva, invb, invc, invd = d/det, -b/det, -c/det, a/det
        t1 = inva * beta1 + invb * beta2
        t2 = invc * beta1 + invd * beta2
        if t2 < 0:
            return None
        return Point(self.origin.x + a * t1, self.origin.y + c * t1)

class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Circle ( Center: %s, Radius: %s )" % (str(self.center), str(self.radius))

    def perimeter(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * self.radius * self.radius

    def incircle(self, pt):
        return self.center.distance(pt) < self.radius

class Rectangle(Shape):
    def __init__(self, center, axes, extents):
        self.center = center
        self.axes = axes
        self.extents = extents

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Rectangle ( Center: %s, Axes: %s, Extents: %s )" % (str(self.center), str(self.axes), str(self.extents))

    def perimeter(self):
        return (self.extents[0] + self.extents[1]) * 2

    def area(self):
        return self.extents[0] * self.extents[1]

    def coords(self):
        pass

class LineString(Shape):
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        str(self)

    def __str__(self):
        return "LineString ( %d points,[%s,..., %s )" % (len(self.points), self.points[0], self.points[len(self.points)-1])

    def coords(self):
        return [p.coords() for p in self.points]

    def length(self):
        length = 0.0
        N = len(self.points)
        for i in range(N-1):
            length += self.points[i].distance(self.points[i+1])
        return length

class LineRing(Shape):
    def __init__(self, points):
        pass

class Polygon(Shape):
    def __init__(self, points, inters=[]):
        '''
        only simple polygon, no holes
        '''
        self.points = points
        self.inters = inters
        if self.signarea() < 0:
            self.reverse()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Polygon ( %d points,[%s,...,%s] )" % (len(self.points), self.points[0], self.points[len(self.points)-1])

    def coords(self):
        return [p.coords() for p in self.points]

    def perimeter(self):
        length = 0.0
        N = len(self.points)
        for i in range(N):
            length += self.points[i].distance(self.points[(i+1) % N])
        return length

    def area(self):
        return math.fabs(self.signarea())

    def signarea(self):
        N = len(self.points)
        area2 = 0.0
        for i in range(N):
            j = (i+1) % N
            v1 = Vector2(self.points[i].x, self.points[i].y)
            v2 = Vector2(self.points[j].x, self.points[j].y)
            area2 += v1.cross(v2)
        return area2 / 2.0

    def reverse(self):
        self.points.reverse()

    def distance(self, pt):
        '''
        if pt in polygon, distance is positive, else negtive
        todo: handle on edge case, pt on vertex, ray got through edge cases
        '''
        N = len(self.points)
        inside = False
        dis2 = float('inf')
        for i in range(N):
            j = (i+1) % N
            p1, p2 = self.points[i], self.points[j]
            if ((p1.y > pt.y) is not (p2.y > pt.y)) and pt.x < p1.x + (p2.x - p1.x) * (pt.y - p1.y) / (p2.y - p1.y):
                inside = not inside
            dis2 = min(LineSegment(p1, p2).distance2(pt), dis2)
        return math.sqrt(dis2) if inside else - math.sqrt(dis2)

    def isinside(self, pt):
        N = len(self.points)
        print self.coords()
        inside = False
        dis2 = float('inf')
        for i in range(N):
            j = (i+1) % N
            p1, p2 = self.points[i], self.points[j]
            if ((p1.y > pt.y) is not (p2.y > pt.y)) and (pt.x < p1.x + (p2.x - p1.x) * (pt.y - p1.y) / (p2.y - p1.y)):
                print p1, p2, pt
                inside = not inside
        return inside
