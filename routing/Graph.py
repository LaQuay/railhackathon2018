from collections import deque, namedtuple

Edge = namedtuple('Edge', 'start, end, cost')



class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [self.make_edge(*edge) for edge in edges]

    def make_edge(self, start, end, cost=1):
        return Edge(start, end, cost)

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=False):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=False):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=False):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    def update_edge(self, n1, n2, cost=1, both_ends=False):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        self.remove_edge(n1, n2, both_ends)
        self.add_edge(n1, n2, cost, both_ends)

    def print_graph(self):
        edges = self.edges[:]

        print("GRAPH ----------------")
        for edge in self.edges:
            node_pairs = self.get_node_pairs(edge.start, edge.end, both_ends=False)
            for edgeway in node_pairs:
                print(str(edgeway[0]) + "\t" + str(edgeway[1]) + "\t" + str(edge.cost) + "\t\t", end='')
            print()
