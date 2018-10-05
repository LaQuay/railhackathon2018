from Graph import Graph
from Algorithm import Algorithm

graph = Graph([
    ("a", "b", 7),  ("b", "a", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
    ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
    ("e", "f", 9)])

algorithm = Algorithm(graph)

print(algorithm.dijkstra("a", "e"))

graph.print_graph()
graph.update_edge("a","c",25)
graph.print_graph()

print(algorithm.dijkstra("a", "e"))
