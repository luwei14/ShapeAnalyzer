#coding=utf-8
import math
import triangle
import matplotlib.pyplot as plt

class TriAxisCenter:
    def __init__(self, points):
        '''
            initiate the triaxiscenter with points list without duplicate point
            points: [[x0,y0],[x1,y1],...,[xn,yn]]

        '''
        # initiate polygon points, and point number
        self.vertices = points
        self.ptnum = len(points)

        # calculate pslg, and cdt
        self._cdt()
        self._top_axis_graph()

    def betweenness_center(self, top = 1):
        ears = self.top_axis_graph.findVertex(1)
        results = {}
        for branch in self.top_axis_graph.findVertex(3):
            results[branch] = {}
            results[branch]["xy"] = self.axisverts[branch]
            results[branch]["degree"] = 0
        for ear in ears:
            for path in self.top_axis_graph.paths_to_ear(ear):
                for k in results.keys():
                    if k in path:
                        results[k]["degree"] += 1
        return sorted(results.iteritems(), key=lambda (k,v): (v["degree"], k), reverse=True)[0:top]
            
    def closeness_center(self, weight="length", top = 1):
        results = {}
        for v in self.axis.vertices():
            if self.axis.degree(v) > 1:
                plen = []
                for path in self.axis.paths_to_ear(v):
                    length = self.axis.path_length(path, weight)
                    plen.append(length)
                mean = sum(plen) * 1.0 / len(plen)
                sq_sum = 0.0
                for l in plen:
                    sq_sum += ((l - mean) * (l - mean))
                std = math.sqrt(sq_sum / len(plen))
                results[v] = {}
                results[v]["degree"] = std
                results[v]["xy"] = self.axisverts[v]
        return sorted(results.iteritems(), key=lambda (k,v): (v["degree"], k))[0:top]

    def _next(self, i):
        '''
            for circulate the points list
        '''
        return (i+1) % self.ptnum
    
    def _tcenter(self, tri):
        '''
            mass center of a triangle
        '''
        pi, pj, pk = [self.vertices[t] for t in tri]
        cx = (pi[0] + pj[0] + pk[0]) / 3.0
        cy = (pi[1] + pj[1] + pk[1]) / 3.0
        return [cx,cy]
    
    def _tarea(self, tri):
        '''
            area of a triangle
        '''
        pi, pj, pk = [self.vertices[t] for t in tri]
        a = math.sqrt((pi[0]-pj[0])*(pi[0]-pj[0]) + (pi[1]-pj[1])*(pi[1]-pj[1]))
        b = math.sqrt((pi[0]-pk[0])*(pi[0]-pk[0]) + (pi[1]-pk[1])*(pi[1]-pk[1]))
        c = math.sqrt((pk[0]-pj[0])*(pk[0]-pj[0]) + (pk[1]-pj[1])*(pk[1]-pj[1]))
        s = 0.5 * (a +b +c)
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        return area

    def _has_pair(self, e, segs):
        '''
            decide if an edge pair in segments list
        '''
        if [e[0], e[1]] in segs or [e[1], e[0]] in segs:
            return True
        else:
            return False

    def _cdt(self):
        '''
            build the CDT, Dual Graph
        '''
        data = {"vertices":[], "segments":[]}
        ptnum = self.ptnum
        for i in range(self.ptnum):
            data["vertices"].append(self.vertices[i])
            data["segments"].append([i, (i+1) % ptnum])
        # triangulate the polygon
        cdt = triangle.triangulate(data,"p")
        self.cdt = {
                        "vertices" : cdt["vertices"],
                        "segments" : data["segments"],
                        "triangles" : cdt["triangles"],
                        "ttype":[]
                    }

        # update triangle's type and edges list in cdt
        edge_tri = {} # edge - triangle relation dict, for building dual graph
        
        self.tcenters = []  # mass center of triangles
        self.axisverts = [] # vertices of axis graph
        self.dual = Graph() # dual graph initiate
        self.axis = Graph() # axis graph initiate
        vidx = 0    # axis graph vertex index counter
        vnames = {} # vertex names, for filtering duplicate diagonal edge center point
        for ti, tri in enumerate(cdt["triangles"]):
            cpt = self._tcenter(tri) # calculate mass center of triangle
            self.tcenters.append(cpt)
            area = self._tarea(tri) # area of triangle

            # initiate triangle type to 3
            ttype = 3
            # initiate triangle edge to type 1, the edge of polygon, if is diagonal, set to 0
            isside = [1,1,1]
            # save center point index of triangle edge in axis graph vertices list [axisverts]
            edge_cpt_idx = []
            # loop on edges of the triangle
            for i in range(3):
                # get an edge index of the triangle
                e = [tri[i], tri[(i+1) % 3]]
                # update the segments list of CDT
                if self._has_pair(e, self.cdt["segments"]) is False:
                    self.cdt["segments"].append(e)
                # build dual graph
                ename = "-".join([str(ev) for ev in sorted(e)])
                if edge_tri.has_key(ename):
                    self.dual.addEdge(edge_tri[ename][0], ti)
                else:
                    edge_tri[ename] = [ti]
                # build the axis graph
                if self._next(e[0]) == e[1] or self._next(e[1]) == e[0]:
                    ttype -= 1 # if the edge is edge of the polygon , decreate the type
                else:
                    # else, set the edge to diagonal, 0
                    isside[i] = 0
                    # middle point of the edge, name, if it is calculated, pass and store into edge_cpt_idx
                    vn = "-".join([str(vi) for vi in sorted(e)])
                    if vnames.has_key(vn) is False:
                        x = (self.cdt["vertices"][e[0]][0] + self.cdt["vertices"][e[1]][0])  / 2.0
                        y = (self.cdt["vertices"][e[0]][1] + self.cdt["vertices"][e[1]][1])  / 2.0
                        self.axisverts.append([x, y])
                        edge_cpt_idx.append(vidx)
                        vnames[vn] = vidx
                        vidx += 1
                    else:
                        edge_cpt_idx.append(vnames[vn])
         
            if ttype == 1: # type I triangle
                diag_idx = isside.index(0)    # diagonal edge index
                ear_vert_idx = tri[(diag_idx + 2) % 3]  # ear vertex index
                ear_vert = self.cdt["vertices"][ear_vert_idx]   # ear vertex
                
                # add a vertex
                self.axisverts.append(ear_vert)
                x, y = self.axisverts[edge_cpt_idx[0]]
                length = math.sqrt(pow(ear_vert[0] - x, 2) + pow(ear_vert[1] - y, 2))
                width = area / length
                self.axis.addEdge(vidx, edge_cpt_idx[0], weights={"length" : length, "width" : width, "area" : area})
                vidx += 1
            elif ttype == 2: # type II triangle, add edge
                x1, y1 = self.axisverts[edge_cpt_idx[0]]
                x2, y2 = self.axisverts[edge_cpt_idx[1]]
                length = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
                width = area / length
                self.axis.addEdge(edge_cpt_idx[0],edge_cpt_idx[1], weights={"length" : length, "width" : width, "area" : area})
            elif ttype == 3: # type III triangle, add 3 edges, and a vertex, the mass center
                self.axisverts.append(cpt)
                cidx = vidx
                for eidx in edge_cpt_idx:
                    x1, y1 = self.axisverts[eidx]
                    length = math.sqrt(pow(x1 - cpt[0], 2) + pow(y1 - cpt[1], 2))
                    width = area / length
                    self.axis.addEdge(cidx, eidx, weights={"length" : length, "width" : width, "area" : area})
                vidx += 1
            
            # save triangle type information into CDT
            self.cdt["ttype"].append(ttype)

    def _top_axis_graph(self):
        '''
            build the topology axis graph
        '''
        # init the graph
        self.top_axis_graph = Graph()
        # find vertices has degree 3
        deg3v = self.axis.findVertex(3)

        # if no branck vertices,
        if len(deg3v) == 0:
            deg1v = self.axis.findVertex(1)
            self.top_axis_graph.addEdge(deg1v[0], deg1v[1])
            return

        # traverse the axis graph from a vertex with degree of 3
        start = deg3v[0]
        curr = start # current vertex, a cursor
        # stack for traverse, to lambda function: pushStack, topStack, popStack
        stack = []
        pushStack = lambda li, x: li.append(x)
        topStack = lambda li: li[-1]
        popStack = lambda li: li.pop()
        pushStack(stack, start)

        # visited flag
        visited = [0] * self.axis.V
        visited[start] = 1
        while len(stack) > 0:
            dead = 1 # if no neighbor to go, this vertex is dead, means I, III vertex
            for i in self.axis.neighbor(curr):
                if visited[i] == 0:
                    curr = i 
                    visited[i] = 1
                    dead = 0
                    break
            if dead:
                # if it is a dead vertex, find a branch, and change current vertex
                topN = popStack(stack)
                if len(stack):
                    self.top_axis_graph.addEdge(topN, topStack(stack))
                    curr = topStack(stack)
            else:
                curr_deg = self.axis.degree(curr)
                if curr_deg == 2:
                    # go further
                    continue
                else:
                    # I, III vertex, push to stack
                    pushStack(stack, curr)
                
class Graph:
    def __init__(self):
        '''
            initiate undirected graph, adjacent dict, vertex and edge list, 
        '''
        self.adj = {}       # adjacent dict
        self.weights = {}   # weight
        self.edges = []
        self.V = 0          # vertex number
        self.E = 0          # edge number
    
    def findVertex(self, deg):
        '''
            find vertices with degree deg
        '''
        verts = []
        for v, nlist in self.adj.items():
            if len(nlist) == deg:
                verts.append(v)
        return verts

    def degree(self, v):
        '''
            degree of a vertex
        '''
        return len(self.adj[v])
    
    def neighbor(self, v):
        '''
            neighbor of vertex
        '''
        return self.adj[v]

    def vertices(self):
        '''
            get vertices in the graph
        '''
        return self.adj.keys()

    def addEdge(self, s, e, weights=None):
        '''
            add a edge, with weight dict ew
        '''
        if self.adj.has_key(s) is False:
            self.adj[s] = []
            self.V += 1
        if self.adj.has_key(e) is False:
            self.V += 1
            self.adj[e] = []
        # add new edges
        if e not in self.adj[s]:
            self.adj[s].append(e)
            self.adj[e].append(s)
            self.E += 1
            self.edges.append([s,e])
            if weights:
                en = "-".join([str(v) for v in sorted([s, e])])
                self.weights[en] = weights

    def path_length(self, path, weight=None):
        length = 0
        for i in range(len(path) - 1):
            pi, pj = path[i], path[i+1]
            if weight:
                en = "-".join([str(v) for v in sorted([pi, pj])])
                length += self.weights[en][weight]
            else:
                length += 1
        return length
    
    def paths_to_ear(self, v):
        '''
            1 degree vertex V to all other 1 degree vertices' paths
        '''
        start = v
        curr = start # current vertex, a cursor
        # stack for traverse, to lambda function: pushStack, topStack, popStack
        stack = []
        pushStack = lambda li, x: li.append(x)
        topStack = lambda li: li[-1]
        popStack = lambda li: li.pop()
        pushStack(stack, start)

        # visited flag
        #visited = [0] * self.V
        visited = {}
        for k in self.adj.keys():
            visited[k] = 0
        visited[start] = 1
        paths = []
        curpath = [start]
        while len(stack) > 0:
            dead = 1 # if no neighbor to go, this vertex is dead, means I, III vertex
            for i in self.neighbor(curr):
                if visited[i] == 0:
                    curr = i 
                    visited[i] = 1
                    curpath.append(i)
                    dead = 0
                    break
            if dead:
                # if it is a dead vertex, find a branch, and change current vertex
                topN = popStack(stack)
                
                if len(stack):
                    curr = topStack(stack)
                    if self.degree(topN) == 1:
                        paths.append(curpath[:])
                    backi = curpath.index(curr)
                    curpath = curpath[0:backi+1]
            else:
                curr_deg = self.degree(curr)
                if curr_deg == 2:
                    # go further
                    continue
                else:
                    # I, III vertex, push to stack
                    pushStack(stack, curr)
        return paths
        
if __name__ == "__main__":
    '''
    import csv
    data = []
    with open("data/poly.csv") as ifile:
        reader = csv.DictReader(ifile)
        for row in reader:
            data.append([float(row["x"]), float(row["y"])])
    TAC = TriAxisCenter(data)
    print "poly vertices:", len(TAC.cdt["vertices"])
    print "cdt edges:", len(TAC.cdt["segments"])
    print "triangles:", len(TAC.cdt["triangles"])'''
    pass