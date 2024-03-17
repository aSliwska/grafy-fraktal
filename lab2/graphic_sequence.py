import networkx as nx
import matplotlib.pyplot as plt
import argparse

def is_graphic_sequence(sequence):
    sequence = sorted(sequence, reverse=True)
    while True:
        if all(i == 0 for i in sequence):
            return True
        if sequence[0] >= len(sequence) or any(i < 0 for i in sequence):
            return False
        first_element = sequence[0]
        for i in range(1, first_element + 1):
            sequence[i] -= 1
        sequence[0] = 0
        sequence.sort(reverse=True)

def generate_graph(sequence):
    if not is_graphic_sequence(sequence):
        raise ValueError("To nie jest ciąg graficzny.")
    
    G = nx.Graph()
    nodes_degrees = sorted(enumerate(sequence), key=lambda x: x[1], reverse=True)
    
    while nodes_degrees[0][1] > 0:
        node, degree = nodes_degrees.pop(0)
        for i in range(degree):
            neighbor, neighbor_degree = nodes_degrees[i]
            G.add_edge(node, nodes_degrees[i][0])
            nodes_degrees[i] = (neighbor, neighbor_degree - 1)
        nodes_degrees.sort(key=lambda x: x[1], reverse=True)
    
    return G

def draw_graph(sequence):
    try:
        G = generate_graph(sequence)
        nx.draw_circular(G, with_labels=True)
        plt.show()
    except ValueError as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description='Wygeneruj graf z zadanego ciągu.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-if', '--input_file', type=str, help='Plik wejściowy zawierający ciąg liczb')
    group.add_argument('-sq', '--sequence', type=int, nargs='+', help='Ciąg liczb')
    
    args = parser.parse_args()
    
    if args.input_file:
        with open(args.input_file, 'r') as file:
            sequence = [int(num) for num in file.read().split()]
    else:
        sequence = args.sequence
    
    draw_graph(sequence)

if __name__ == '__main__':
    main()
