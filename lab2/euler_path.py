import random

import networkx as nx
import argparse

from matplotlib import pyplot as plt

from graphic_sequence import generate_graph, draw_graph
from randomize import randomize
from component import dfs


def is_bridge(graph, edge):
    tempG = graph.copy()
    tempG.remove_edge(edge[0], edge[1])
    # sprawdzamy, czy graf traci spójność po usunięciu krawędzi
    return not len(dfs([], tempG, list(tempG.nodes)[0])) == len(dfs([], graph, list(graph.nodes)[0]))


def euler_path(graph, path=[], node=None):
    if len(graph.nodes) == 1:
        return path

    if node is None:
        node = random.choice(list(graph.nodes))

    bridges = []
    nonBridge = None
    for neighbor in graph.neighbors(node):
        edge = (neighbor, node)
        if is_bridge(graph, edge):
            bridges.append(edge)
        else:
            nonBridge = edge
            break

    path.append(node)
    chosen_edge = nonBridge if nonBridge else bridges[0]
    graph.remove_edge(*chosen_edge)

    if len(list(graph.neighbors(node))) == 0:
        graph.remove_node(node)

    nx.draw_circular(graph, with_labels=True)
    plt.show()

    return euler_path(graph, path, chosen_edge[0])


def main():
    parser = argparse.ArgumentParser(description="Euler Path Algorithm")
    parser.add_argument("-sq", nargs="+", type=int, help="List of integers")
    args = parser.parse_args()

    if not args.sq:
        raise IOError("Please enter an integer list")

    listOfDegrees = args.sq

    G = generate_graph(listOfDegrees)  # tworzenie grafu z ciągu

    while len(dfs([], G, list(G.nodes)[0])) < len(listOfDegrees):
        randomize(G)  # zmiana krawędzi do momentu uzyskania spójności

    nx.draw_circular(G, with_labels=True)
    plt.show()

    ep = euler_path(G)
    print(ep)


if __name__ == "__main__":
    main()
