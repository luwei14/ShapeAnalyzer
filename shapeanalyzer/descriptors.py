#coding=utf-8
'''
https://fisherzachary.github.io/public/r-output.html
'''
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

    def PolsbyPopper(self):
        '''
            The Polsby-Popper (PP) measure (polsby & Popper, 1991) is the ratio of the area of the district (AD) 
            to the area of a circle whose circumference is equal to the perimeter of the district (PD). 
            A district’s Polsby-Popper score falls with the range of [0,1] and a score closer to 1 indicates
            a more compact district.
        '''
        return 4 * math.pi * self.Area() / (self.Perimeter() ** 2)
    def Schwartzberg(self):
        '''
            The Schwartzberg score (S) compactness score is the ratio of the perimeter of the district (PD) 
            to the circumference of a circle whose area is equal to the area of the district. 
            A district’s Schwartzberg score as calculated below falls with the range of [0,1] 
            and a score closer to 1 indicates a more compact district.
        '''
        r = math.sqrt(self.Area() / math.pi)
        C = 2 * math.pi * r
        return C / self.Perimeter()

    def Convesness(self):
        '''
            The Convex Hull score is a ratio of the area of the district to the area of the minimum convex polygon 
            that can encloses the district’s geometry. A district’s Convex Hull score falls within the range of [0,1] 
            and a score closer to 1 indicates a more compact district.
        '''
        hull = Polygon(self.BG.ConvexHull())
        return self.Area() / hull.area()
    
    def Eccentricity(self):
        ''' 
            Eccentricity : the Length-Width Ratio (LW) is calculated as the ratio of the length (LMBR) to the width (WMBR) of 
            the minimum width rectangle surrounding the district.
        '''
        rect = self.BG.MinimumWidthRectangle()
        return rect.extents[1] / rect.extents[0]

    def Rectangularity(self):
        '''
             Rectangularity: the ratio of the region’s area against the area of the its minimum bounding rectangle (MBR)
        '''
        rect = self.BG.MinimumWidthRectangle()
        return self.Area() / rect.area()

    def ReockScore(self):
        '''
            The Reock Score (R) is the ratio of the area of the district AD to the area of a minimum bounding cirle (AMBC) 
            that encloses the district’s geometry. A district’s Reock score falls within the range of [0,1] and a score 
            closer to 1 indicates a more compact district.
        '''
        circle, support = self.BG.MinimumAreaCircle()
        return self.Area() / circle.area()

    def Descriptors(self):
        descriptors = [method for method in dir(self) if callable(getattr(self, method)) if not method.startswith('_')] 
        descriptors.remove("Descriptors")
        results = {}
        for method in descriptors:
            results[method] = getattr(self, method)()
        return results

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    fig_size = [10,10]
    plt.rcParams["figure.figsize"] = fig_size
    poly = Polygon([Point(10, 15), Point(27, 21), Point(50, 89), Point(60, 45), Point(45, 20), Point(16, 10)])
    print poly.area()
    sd = ShapeDescriptor(poly)
    print sd.Descriptors()
    coords = poly.coords()
    coords.append(coords[0])
    coords = np.asarray(coords)
    plt.plot(coords[:,0], coords[:,1],"r-")
    plt.show()
