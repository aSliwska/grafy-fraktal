import networkx as nx
import matplotlib.pyplot as plt
from lab2.randomize import read_args, read_input, InputType
from lab2.randomize import create_graph_from_adjacency_matrix


def dfs(visited, graph, node):
    if node not in visited:
        visited.append(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
    return visited  

def find_largest_component(G):
    largest_component = []
    visited_global = set()
    
    for node in G:
        if node not in visited_global:
            visited_component = dfs([], G, node)
            visited_global.update(visited_component) 
            
            if len(visited_component) > len(largest_component):
                largest_component = visited_component
    print(visited_global)
    return largest_component

def main():
    args = read_args()
    input_type, input_data = read_input(args)

    if input_type != InputType.ADJACENCY_MATRIX:
        print('Graph needs to be encoded as an adjacency matrix')
        return
    
    G = create_graph_from_adjacency_matrix(input_data)

    largest_component = find_largest_component(G)

    print("Największa spójna składowa:")
    print("->".join(str(node) for node in largest_component))

    node_colors = ['green' if node in largest_component else 'grey' for node in G.nodes()]    
    edge_colors = ['green' if u in largest_component and v in largest_component else 'grey' for u, v in G.edges()]
    nx.draw_circular(G, with_labels=True, node_color=node_colors, edge_color=edge_colors)

    plt.show()

if __name__ == '__main__':
    main()
