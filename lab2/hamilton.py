import random
from copy import deepcopy

import networkx as nx
import argparse

from matplotlib import pyplot as plt

from graphic_sequence import generate_graph, draw_graph, is_graphic_sequence
from randomize import randomize, read_args, read_input, create_graph_from_adjacency_matrix, InputType


def hamilton(graph: nx.Graph, start_vertex):
    def dfs(vertex, stack, visited):
        stack.append(vertex)
        visited.add(vertex)

        if len(stack) == len(list(graph.nodes)):
            if graph.has_edge(start_vertex, vertex):
                return stack  # Found a Hamiltonian cycle
            else:
                stack.pop()
                visited.remove(vertex)
                return None

        for neighbor in range(len(list(graph.nodes))):
            if graph.has_edge(vertex, neighbor) and neighbor not in visited:
                cycle = dfs(neighbor, stack, visited)
                if cycle:
                    return cycle

        stack.pop()
        visited.remove(vertex)
        return None

    visited_vertices = set()
    vertex_stack = []

    return dfs(start_vertex, vertex_stack, visited_vertices)


def main():
    args = read_args()
    input_type, input_data = read_input(args)

    if input_type != InputType.ADJACENCY_MATRIX:
        print('graph needs to be encoded as an adjacency matrix')
        return

    G = create_graph_from_adjacency_matrix(input_data)

    nx.draw_circular(G, with_labels=True)
    plt.show()

    rand_node = random.choice(list(G.nodes))
    path = hamilton(G, rand_node)
    print(path)


if __name__ == '__main__':
    main()
