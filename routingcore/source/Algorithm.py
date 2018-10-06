from collections import deque, namedtuple
from Graph import Graph

# we'll use infinity as a default distance to nodes.
inf = float('inf')


class Algorithm:
    def __init__(self, graph):
        self.graph = graph

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.graph.vertices}
        for edge in self.graph.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.graph.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.graph.vertices}
        previous_vertices = {
            vertex: None for vertex in self.graph.vertices
        }
        distances[source] = 0
        vertices = self.graph.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path = []
        current_vertex = dest
        while previous_vertices[current_vertex] is not None:
            path.insert(0, current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.insert(0, current_vertex)
        return path
