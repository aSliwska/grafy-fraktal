import random

import networkx as nx
import argparse

from matplotlib import pyplot as plt

from graphic_sequence import generate_graph, draw_graph, is_graphic_sequence
from randomize import randomize, read_input
from component import dfs


def main():
    parser = argparse.ArgumentParser(description="Random Regular Graph Generator")
    parser.add_argument("degree", type=int, help="Degree of random graph")
    degree = parser.parse_args().degree

    random_length = random.randint(4, 10)

    if degree == 0:
        G = nx.Graph()
        for i in range(random_length):
            G.add_node(i)
        nx.draw_circular(G, with_labels=True)
        plt.show()
        exit(0)



    while True:
        sequence = [degree] * random_length
        if not is_graphic_sequence(sequence):
            random_length += 1
        else:
            break

    G = generate_graph(sequence)
    draw_graph(sequence)
    print(G)



if __name__ == "__main__":
    main()
