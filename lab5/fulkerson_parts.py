import networkx as nx
INFINITY = 999999999999

def extendi_path(G, s_node, t_node):
    # Init
    for node in G.nodes:
        G.nodes[node]['dist'] = INFINITY
        G.nodes[node]['parent'] = -1
    Q = [s_node]
    G.nodes[s_node]['dist'] = 0

    # Algorithm
    while len(Q):
        v = Q.pop(0)
        for neighbor in G.neighbors(v):
            if G.nodes[neighbor]['dist'] == INFINITY:
                G.nodes[neighbor]['dist'] = G.nodes[v]['dist'] + 1
                G.nodes[neighbor]['parent'] = v
                if neighbor == t_node:
                    break
                Q.append(neighbor)

    # Gather output
    if G.nodes[t_node]['parent'] == -1:
        return None
    else:
        c_node = t_node
        path = []
        while G.nodes[c_node]['parent'] != -1:
            path.append(c_node)
            c_node = G.nodes[c_node]['parent']
        path.append(c_node)
        return list(reversed(path))

def make_residual_net(G):
    Gf = nx.DiGraph(directed=True)

    for node in G.nodes:
        Gf.add_node(node, color=G.nodes[node]['color'])

    for edge in G.edges:
        flow = G.edges[edge]['flow']
        cflow = G.edges[edge]['cflow']

        if cflow == flow:
            Gf.add_edge(edge[1], edge[0], flow=cflow)
        elif cflow == 0:
            Gf.add_edge(edge[0], edge[1], flow=flow)
        else:
            Gf.add_edge(edge[1], edge[0], flow=cflow)
            Gf.add_edge(edge[0], edge[1], flow=flow - cflow)

    return Gf

# Find extending path and cf
def extendi_path_step(Gf, s_node, t_node):
    s = extendi_path(Gf, s_node, t_node)
    if s is None:
        return (None, None)
    cf = Gf.edges[(s[0], s[1])]['flow']
    for i in range(0, len(s) - 1):
        eflow = Gf.edges[(s[i], s[i + 1])]['flow']
        if (eflow < cf):
            cf = eflow
    return (s, cf)