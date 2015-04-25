import copy
from collections import deque
import operator

class Graph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}
    
    def add_node(self, n):
        self._nodes[n] = {}
        self._edges[n] = {}

    def addedge(self, edges):
        for each in edges:
            if not each[0] in self._nodes:
                self.add_node(e[0])
            if not each[1] in self._nodes:
                self.add_node(each[1])
            self._edges[each[0]][each[1]] = each[2]        
        
    def __len__(self):
        return len(self._nodes)

    def nodes(self):
        return iter(self._nodes.keys())

    def edges(self):
        for n, neighbors in self._edges.iteritems():
            for neigh, w in neighbors.iteritems():
                yield (n, neigh, w)
                
    def neighbors(self, node):
        return iter([n[0] for n in self._edges[node].iteritems()])

    def transpose(self):      
    	#create new graph
        revgraph = Graph()
        #go through each node in original and add it in the reverse
        for eachnode in self.nodes():
            revgraph.add_node(eachnode)
        #reverse each edge
        new_edges = [(each[1], each[0], each[2]) for each in self.edges()]
        #add to graph
        revgraph.addedge(new_edges)
        return revgraph
    
    def components(self):
        stronglycc = []
        revegraph = self.transpose()
        queuenodes = deque(self.nodes())
        visit = {}
        for eachnode in self.nodes():
            visit[eachnode] = False
        while len(queuenodes) > 0:
            currennode = queuenodes.pop()
            if not visit[currennode]:
                c = dfs(self, currennode)
                c_rev = dfs(revegraph, currennode)
                tempstronglycc = []
                for nextto in c:
                    if nextto in c_rev:
                        visit[nextto] = True
                        tempstronglycc.append(nextto)
                stronglycc.append(tempstronglycc)
        return stronglycc

def getDegrees(graph, nodes):
    outdegree = 0
    indegree = 0
    node_list = []
    for node in nodes:
        node_info = {}
        for item in graph.edges():
            if item[0] == node:
                outdegree += 1
            if item[1] == node:
                indegree +=1 
        node_info["node"] = node
        node_info["outdegree"] = outdegree
        node_info["indegree"] = indegree
        node_list.append(node_info)
        indegree = outdegree = 0
    return node_list

def read(filename, direction):
    g = Graph()
    edges = []
    vertices = []
    with open(filename) as FP:
        file_as_list = list(FP)
        numofvertices = int(file_as_list[0].strip("\n"))
        vertices = [str(item.strip("\n").rstrip()) for item in file_as_list][1:numofvertices+1]
    with open(filename) as FP2:
        preliminary = list(FP2)[numofvertices+3:]
        for line in preliminary:
            edges.append(tuple(line.strip("\n").rstrip().split(" ")))
        FP2.close()
    for v in vertices:
        g.add_node(v)
    edgestuple = []
    for e in edges:
        if (direction):
            edgestuple.append((e[0], e[1], 1))
            edgestuple.append((e[1], e[0], 1))
        else:
            edgestuple.append((e[1], e[0], 1))
    g.addedge(edgestuple)    
    return (g, vertices)

def dfs(g, beginnode = None):       
    visit = {}
    for eachnode in g.nodes():
        visit[eachnode] = False
    if beginnode is None:
        beginnode = n
    queuenodes = deque([beginnode])
    result = []
    while len(queuenodes) > 0:
        currennode = queuenodes.pop()
        if not visit[currennode]:
            result.append(currennode)
            visit[currennode] = True
            for nextto in g.neighbors(currennode):
                if not visit[nextto]:
                    queuenodes.append(nextto)
    return result

def bellman_ford(g, beginnode):       
    distance = {}
    for eachnode in g.nodes():
        distance[eachnode] = float('inf')
    distance[beginnode] = 0
    for i in range(len(g) - 1):
        check = False
        for e in g.edges():
            begin = e[0]
            last = e[1]
            cost = e[2]
            newdistance = distance[begin] + cost
            if distance[last] > newdistance:
                check = True
                distance[last] = newdistance
        if not check:
            break
    for e in g.edges():
        begin = e[0]
        last = e[1]
        cost = e[2]
        newdistance = distance[begin] + cost
    return distance

def shortest_path(g, beginnode, end_node = None):
    dist = bellman_ford(g, beginnode)
    if not end_node is None:
        dist = dist[end_node]
    return dist

if __name__ == "__main__":
    print "\nFacebook Interaction\n"

    filedata = read("FBdata.txt",True)
    graph_FB_undirected = filedata[0]
    vertices = filedata[1]


    degreelist = getDegrees(graph_FB_undirected, vertices)
    
    indegreemax = 0
    maxinteract = []
    finalsum = 0.0
    
    for i, each in enumerate(degreelist):
        finalsum += degreelist[i]["indegree"]
        if degreelist[i]["indegree"] > indegreemax:
            maxinteract = degreelist[i]
            indegreemax = degreelist[i]["indegree"]
    
    print "Most Interacted: ", maxinteract["node"], "with", maxinteract["indegree"], "interactions"
    print "Average: ", float(finalsum / len(vertices))
    
    sccs = graph_FB_undirected.components()
    sccnum = 0
    maxscc = []
    for sccnum in sccs:
        maxscc.append(len(sccnum))

    print "Number of Users in Largest Subgroup: ", max(maxscc)

    print "\nCS Web Interaction\n"

    filedata = read("cswebData.txt", False)
    graph_CS_directed = filedata[0]
    vertices = filedata[1]

    degreelistCSgraph = getDegrees(graph_CS_directed, vertices)

    outdegreemax = 0
    indegreemax = 0
    maxinteractout = []
    maxinteractin = []

    for i, each in enumerate(degreelistCSgraph):
        if degreelistCSgraph[i]["outdegree"] > outdegreemax:
            maxinteractout = degreelistCSgraph[i]
            outdegreemax = degreelistCSgraph[i]["outdegree"]

        if degreelistCSgraph[i]["indegree"] > indegreemax:
            maxinteractin = degreelistCSgraph[i]
            indegreemax = degreelistCSgraph[i]["indegree"]

    print "Web Page with Largest Links within: ", maxinteractout["node"] 
    print "Web Page with Most Links to Others: ", maxinteractin["node"]

    sccs = graph_CS_directed.components()
    sccnum = 0
    maxscc = []

    for sccnum in sccs:
        maxscc.append(len(sccnum))

    print "Size of Largest Cycle: ", max(maxscc)
    
    doublecheck = False
    shortestpath = shortest_path(graph_CS_directed, "http://www.wfu.edu", end_node="http://csweb.cs.wfu.edu")
    if shortestpath != float('Inf'):
        doublecheck = True
    path = dfs(graph_CS_directed, beginnode = "http://www.wfu.edu")
    #print "Shortest Path: ", path

    for p in path:
        if p =="http://csweb.cs.wfu.edu":
            doublecheck = True
    if doublecheck == False:
        print "Bonus: No Path Found, does not exist"
    if doublecheck == True:
        print "Bonus: Path Found"
 
    print "\nTest:\n"
    filedata = read("test.txt", False)
    graph_CS_directed = filedata[0]
    vertices = filedata[1]

    shortestpath = shortest_path(graph_CS_directed, "A", end_node="J")

    print "Shortest Path: ", shortestpath