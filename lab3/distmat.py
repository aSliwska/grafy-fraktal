import numpy as np # Is it even science if numpy doesn't show up at least once?
from lab3.dijkstra import *

def make_distance_matrix(G):

    node_count = len(G.nodes)

    matrix = np.zeros((node_count, node_count), dtype=int)

    for i in range(0, node_count - 1):
        G = dijkstra_undirected(G, i)
        paths = shortest_paths(G)
        for path in paths:
            end = path[0][len(path[0]) - 1]
            matrix[i, end] = path[1]
            matrix[end, i] = path[1]

    return matrix

# Support multiple finds
def centers(matrix):
    sums = np.sum(matrix, 0)
    minval = np.min(sums)
    print("Znaleziono centra grafu: ")
    idx = 0
    for val in np.nditer(sums):
        if val == minval:
            print("ID: ", idx, " wartość: ", val)
        idx = idx + 1

    print("Znaleziono centra minimax: ")
    maximums = np.max(matrix, 0)
    minval = np.min(maximums)
    idx = 0
    for val in np.nditer(maximums):
        if val == minval:
            print("ID: ", idx, " wartość: ", val)
        idx = idx + 1


