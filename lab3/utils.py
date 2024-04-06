import random
import networkx as nx
import matplotlib.pyplot as plt

from lab2.component import dfs

# Modified version of lab1 randomizer
# Generates a graph_tools graph to work with instead of a file
# Random state ensures the graph stays the same
# Generates an undirected graph
# Should be easy to modify into any kind of graph generator
def random_weighted(vertex_amount, edge_amount, wmax=2,  random_state=42):
    edges = []  # List of edges that will be drawn

    # Lists all edges and chooses a user defined amount of them at random
    available_edges = [[a, b] for a in range(vertex_amount) for b in range(a + 1, vertex_amount)]

    random.seed(random_state) # Thou shalt not debug on truly random data!

    for _ in range(edge_amount):
        index = random.randrange(len(available_edges))
        edge = available_edges.pop(index)
        edges.append(edge)


    outputGraph = nx.Graph()

    for i in range(0, vertex_amount):
        outputGraph.add_node(i)

    for edge in edges:
        outputGraph.add_edge(edge[0], edge[1], weight=random.randrange(1, wmax))

    return outputGraph



# Supports drawing a graph with weighted edges
def draw_weighted(G):
    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


# Modified to find all components
def find_components(G):
    components = []
    visited_global = set()

    for node in G:
        if node not in visited_global:
            visited_component = dfs([], G, node)
            visited_global.update(visited_component)
            components.append(visited_component)
    print(visited_global)
    return components

# Merges a randomized graph into a single component graph
def merge_components(G, wmax=2,  random_state=42):
    random.seed(random_state)  # Thou shalt not debug on truly random data!

    separate_components = find_components(G)

    if (len(separate_components) == 1):
        return G

    merged = separate_components.pop()

    while len(separate_components) > 0:
        to_merge = separate_components.pop()
        G.add_edge(random.choice(merged), random.choice(to_merge), weight=random.randrange(1, wmax))
        merged = merged + to_merge

    return G

# How the process works:
# 1. Generate a random graph
# 2. Merge all separate components in the graph together


graph = random_weighted(6, 9, 11, random_state=42)
graph = merge_components(graph, wmax=11, random_state=42)

draw_weighted(graph)




