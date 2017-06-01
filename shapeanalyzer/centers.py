from shapes import *
from utilities import *
class Center():
    def __init__(self, polygon):
        self.poly = polygon

    def Centroid(self):
        N = len(self.poly.points)
        points = self.poly.points
        area = 0.0
        cx = 0.0
        cy = 0.0
        for i in range(N):
            j = (i +1) % N
            p1, p2 = points[i], points[j]
            sign_area = p1.x * p2.y - p1.y * p2.x
            cx += (p1.x + p2.x) * sign_area
            cy += (p1.y + p2.y) * sign_area
            area += sign_area * 3
        cx = cx / area
        cy = cy / area
        return Point(cx, cy)

    def VisualCenter(self):
        tolerance = 0.1
        points = self.poly.points
        polygon = self.poly
        minx, miny = points[0].x, points[0].y
        maxx, maxy = points[0].x, points[0].y
        for p in points:
            minx = p.x if p.x < minx else minx
            maxx = p.x if p.x > maxx else maxx
            miny = p.y if p.y < miny else miny
            maxy = p.y if p.y > maxy else maxy

        width = maxx - minx
        height = maxy - miny
        cellsize = min(width,height)
        if cellsize == 0:
            return Point(minx, miny)

        h = cellsize / 2.0

        compare = lambda a, b : a["maxdis"] - b["maxdis"]
        cellQ = TinyQueue(compare=compare)
        x = minx
        while x < maxx:
            y = miny
            while y < maxy:
               # print polygon.coords()
                cellQ.push(self._cell(x+h, y+h, h, polygon))
               # print polygon.coords()
                y += cellsize
            x += cellsize
        centroid = self.Centroid()
        initcell = self._cell(centroid.x, centroid.y, 0, polygon)
        #print "Init0:", initcell
        bboxcell = self._cell(minx + width/2, miny + height/2, 0, polygon)
        initcell = bboxcell if bboxcell["d"] > initcell["d"] else initcell
        #print "Init1:", initcell
        pts = []
        cells =[]
        while cellQ.length:
            cell = cellQ.pop()
            cells.append(cell)
            if cell["d"] > initcell["d"]:
                initcell = cell
                #print initcell
                pts.append([cell["x"], cell["y"]])
            if cell["maxdis"] - initcell["d"] <= tolerance:
                #print cell, initcell
                continue
            h = cell["h"] / 2.0
            cellQ.push(self._cell(cell["x"]-h, cell["y"]-h, h, polygon))
            cellQ.push(self._cell(cell["x"]+h, cell["y"]-h, h, polygon))
            cellQ.push(self._cell(cell["x"]-h, cell["y"]+h, h, polygon))
            cellQ.push(self._cell(cell["x"]+h, cell["y"]+h, h, polygon))
        #print initcell
        #print polygon.isinside(Point(initcell["x"], initcell["y"]))
        return Point(initcell["x"], initcell["y"]), pts, cells

    def CentroidBySkeleton(self):
        pass

    def _cell(self, x, y, h, polygon):
        dis = polygon.distance(Point(x,y))
        maxdis = dis + h * math.sqrt(2)
        return {"x":x,"y":y,"h":h,"d":dis,"maxdis":maxdis}