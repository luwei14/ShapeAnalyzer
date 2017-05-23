import math
from boundings import *
from shapes import *

class ShapeDescriptor():
    def __init__(self, poly):
        self._poly = poly
        self.BG = BoundingGeometry(self._poly.points)
    def Area(self):
        return self._poly.area()

    def Perimeter(self):
        return self._poly.perimeter()

    def Roundness(self):
        return 4 * math.pi * self.Area() / (self.Perimeter() ** 2)
    
    def Convesness(self):
        hull = Polygon(self.BG.ConvexHull())
        return self.Area() / hull.area()
    
    def Curvature(self):
        rect = self.BG.MinimumWidthRectangle()
        return rect.extents[1] / rect.extents[0]

    def Circularity(self):
        circle, support = self.BG.MinimumAreaCircle()
        return self.Area() / circle.area()

    def Descriptors(self):
        descriptors = [method for method in dir(self) if callable(getattr(self, method)) if not method.startswith('_')] 
        descriptors.remove("Descriptors")
        results = {}
        for method in descriptors:
            results[method] = getattr(self, method)()
        return results
    