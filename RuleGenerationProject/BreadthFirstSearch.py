from enum import Enum
from array import array

class Command(Enum):
    NOTHING = 0
    MOVELEFT = 1
    MOVERIGHT = 2
    MOVEUP = 3
    MOVEDOWN = 4
    SPECIAL = 5


class Vertex:
    def __init__(self, n, _commands):
        self.name = n
        self.neighbors = list()
        self.win = False
        self.commands = _commands
        self.distance = 9999
        self.color = 'black'

    def addNeighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()



class Graph:
    vertices = {}

    def addVertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    def addEdge(self, u, v):
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.addNeighbor(v)
                if key == v:
                    value.addNeighbor(u)
            return True
        else: return False

    def printGraph(self):
        for key in sorted(list(self.vertices.keys())):
            print(key + str(self.vertices[key].neighbors) + "   " + str(self.vertices[key].distance))
    
    def bfs(self, vert):
        q = list()
        vert.distance = 0
        vert.color = 'red'
        vert.command = Command.NOTHING

        for v in vert.neighbors:
            self.vertices[v].distance = vert.distance + 1
            q.append(v)

        while len(q) > 0:
            u = q.pop(0)
            node_u = self.vertices[u]
            node_u.command = Command.NOTHING
            node_u.color = 'red'

            for v in node_u.neighbors:
                node_v = self.vertices[v]
                if node_v.color == 'black':
                    q.append(v)
                    if node_v.distance > node_u.distance + 1:
                        node_v.distance = node_u.distance + 1