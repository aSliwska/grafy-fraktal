import networkx as nx
import matplotlib.pyplot as plt
import argparse
from enum import Enum
import sys
import random

class InputType(Enum):
	ADJACENCY_LIST = 'ls'
	ADJACENCY_MATRIX = 'ms'
	INCIDENCE_MATRIX = 'mi'

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('num_swaps', type = int)
    return parser.parse_args()

def read_input(args):

	input_stream = sys.stdin if not sys.stdin.isatty() else open(args.input_file, 'r')
    
	input_type_string = input_stream.readline().strip()
	if (input_type_string not in [it.value for it in InputType]):
		raise ValueError('first line in file must indicate encoding type')
	input_type = InputType(input_type_string)
      
	input_data = []
	for line in input_stream:
		if len(line.strip()) != 0:
			input_data.append(line.strip().split(' '))
    
	return input_type, input_data

def create_graph_from_adjacency_matrix(input_data):
    edge_list = []
    nodes_num = len(input_data)
    isolated_nodes = [] 

    for row in range(nodes_num):
        has_edge = False 
        
        for col in range(nodes_num):
            if input_data[row][col] == '1':
                edge_list.append((row, col))
                has_edge = True
        
        if not has_edge:
            isolated_nodes.append(row) 

    G = nx.Graph()
    G.add_edges_from(edge_list)

    for node in isolated_nodes:
        G.add_node(node)

    return G

def can_be_randomized(G):
    if len(G.nodes()) < 4:
        return False

    if len(G.edges()) < 2:
        return False

    edges = list(G.edges())
    n = len(edges)
    for i in range(n):
        for j in range(i + 1, n):
            e1, e2 = edges[i], edges[j]
            a, b = e1
            c, d = e2
            if len(set([a, b, c, d])) == 4: 
                if not G.has_edge(a, c) and not G.has_edge(b, d):
                    return True
                if not G.has_edge(a, d) and not G.has_edge(b, c):
                    return True
    return False

def randomize(G):
    args = read_args()
    num_swaps = args.num_swaps
    curr_swaps = 0

    while curr_swaps < num_swaps:
        edges = list(G.edges())
        edge1, edge2 = random.sample(edges, 2)

        a, b = edge1
        c, d = edge2

        if not G.has_edge(a, d) and not G.has_edge(b, c) and a != d and b != c:

            G.remove_edge(a, b)
            G.remove_edge(c, d)

            G.add_edge(a, d)
            G.add_edge(b, c)

            curr_swaps+=1

def main():
    args = read_args()
    input_type, input_data = read_input(args)

    if input_type != InputType.ADJACENCY_MATRIX:
        print('Graph needs to be encoded as an adjacency matrix.')
        return
    
    G = create_graph_from_adjacency_matrix(input_data)
    if can_be_randomized(G):
        plt.subplot(1, 2, 1)
        plt.title("Przed")
        nx.draw_circular(G,with_labels = True)
        randomize(G)
        plt.subplot(1, 2, 2)
        plt.title("Po")
        nx.draw_circular(G,with_labels = True)
        plt.show()
    else:
        print("Graph cannot be randomized.")
        nx.draw_circular(G,with_labels = True)
        plt.show()

if __name__ == '__main__':
    main()
