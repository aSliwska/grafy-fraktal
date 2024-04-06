import itertools

import networkx as nx
import matplotlib.pyplot as plt
import random

# Supports drawing a graph with weighted edges
def draw_flow(G):
    pos = nx.spring_layout(G)
    color_map = []
    for node in G.nodes:
        color_map.append(G.nodes[node]["color"])
    nx.draw_networkx(G, pos, node_color=color_map)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def random_flow_graph(inter_layers, random_state = 69):
    # Generate the structure
    layerStructure = [[0]]
    nodeNumber = 1
    random.seed(random_state)

    for i in range(1, inter_layers):
        layer = []
        for i in range(0, random.randint(2, inter_layers)):
            layer.append(nodeNumber)
            nodeNumber = nodeNumber + 1
        layerStructure.append(layer)
    layerStructure.append([nodeNumber])

    print(layerStructure)

    lnumber = 0
    # Write the structure to the graph
    G = nx.DiGraph(directed=True)
    for layer in layerStructure:
        lnumber = lnumber + 1
        for node in layer:
            r = 255 // lnumber
            b = 255 // (inter_layers + 2 - lnumber)
            G.add_node(node, color=rgb_to_hex(r, 0, b))

    # Add edges between layers
    for i in range(0, len(layerStructure) - 1):
        # Prioritize connecting unconnected
        l1 = layerStructure[i].copy()
        l2 = layerStructure[i + 1].copy()

        while (len(l1) and len(l2)):
            n1 = random.choice(l1)
            n2 = random.choice(l2)
            l1.remove(n1)
            l2.remove(n2)
            G.add_edge(n1, n2, weight=random.randint(1, 10))

        while (len(l1) > 0):
            G.add_edge(l1.pop(), random.choice(layerStructure[i + 1]), weight=random.randint(1, 10))

        while (len(l2) > 0):
            G.add_edge(random.choice(layerStructure[i]), l2.pop(),weight=random.randint(1, 10))

    # Add random edges globally
    # Generate possible edges to add
    anodes = itertools.product(range(1, nodeNumber), range(1, nodeNumber))

    f1 = lambda val: val[0] != val[1]

    anodes = filter(f1, anodes)

    existing = list(map(tuple, G.edges))
    f2 = lambda val: val not in existing and (val[1], val[0]) not in existing

    anodes = list(filter(f2, anodes))

    for i in range(0, inter_layers * 2):
        nedge = random.choice(anodes)
        anodes.remove(nedge)
        G.add_edge(nedge[0], nedge[1], weight=random.randint(1, 10))


    return G

G = random_flow_graph(4)
draw_flow(G)



