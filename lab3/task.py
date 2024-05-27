# This file contains the task

from lab3.distmat import *
from lab3.spanningtree import *

# Task 1 - Random graph

graph = random_weighted(6, 3, 11, random_state=42)
draw_weighted(graph)
graph = merge_components(graph, wmax=11, random_state=42)
draw_weighted(graph)

# Task 2 - Dijkstra's algorithm

graph = dijkstra_undirected(graph,0, True)
shortest_paths(graph, verbose=True)

# Task 3 - Macierz odległości

mat = make_distance_matrix(graph)
print("Macierz odległości")
print(mat)
centers(mat)

draw_weighted(graph)

tree = Kruskal(graph)

draw_weighted(tree)