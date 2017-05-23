import math
from vectmat import *
 
class Shape():
    def __init__(self):
        pass
    
class Point(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        return [self.fpt.coords, self.tpt.coords]
    
    def length(self):
        return math.hypot(self.fpt.x - self.tpt.x, self.fpt.y - self.tpt.y)

    def distance(self, pt):
        v2 = [pt.x - self.fpt.x, pt.y - self.fpt.y]
        v1 = [self.tpt.x - self.fpt.x, self.tpt.y  - self.fpt.y]
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        height = math.fabs(cross) / math.hypot(v1[0], v1[1])
        return height

class Line(Shape):
    def __init__(self, a, b, c):
        '''
        line : A * x + B * y + C = 0
        '''
        self.A = a
        self.B = b
        self.C = c

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "Line ( %sx + %sx + %s = 0 )" % (str(self.A), str(self.B), str(self.C))

    def parameters(self):
        return [self.A, self.B, self.C]

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
        return [p.coords for p in self.points]
    
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
    def __init__(self, points):
        '''
        only simple polygon, no holes
        '''
        self.points = points

    def __repr__(self):
        str(self)
    
    def __str__(self):
        return "Polygon ( %d points,[%s,..., %s )" % (len(self.points), self.points[0], self.points[len(self.points)-1])

    def coords(self):
        return [p.coords for p in self.points]
    
    def perimeter(self):
        length = 0.0
        N = len(self.points)
        for i in range(N):       
            length += self.points[i].distance(self.points[(i+1) % N])
        return length

    def area(self):
        N = len(self.points)
        area2 = 0.0
        for i in range(N):
            j = (i+1) % N
            v1 = Vector2(self.points[i].x, self.points[i].y)
            v2 = Vector2(self.points[j].x, self.points[j].y)
            area2 += v1.cross(v2)
        return area2 / 2.0