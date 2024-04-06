from lab3.utils import *

def dijkstra_undirected(G, s, verbose = False):

    # Init graph metadata
    for node in G.nodes:
        G.nodes[node]["distance"] = 9000000 # well over 9000
        G.nodes[node]["parent"] = -1
    G.nodes[s]["distance"] = 0

    S = []

    while len(S) != len(G.nodes):
        u = -1

        # Find starter unvisited
        for node in G.nodes:
            if node not in S:
                u = node
                break

        for node in range(u, len(G.nodes)):
            if (G.nodes[node]["distance"] < G.nodes[u]["distance"] and node not in S):
                u = node

        S.append(u)

        if verbose:
            print("Processing ", u)

        # Relax all neighbors of u
        for nbr in G.neighbors(u):
            if verbose:
                print(" Relaxing ", u, ' -- ', nbr)
            if G.nodes[nbr]["distance"] > G.nodes[u]["distance"] + G.edges[u, nbr]["weight"]:
                G.nodes[nbr]["distance"] = G.nodes[u]["distance"] + G.edges[u, nbr]["weight"]
                G.nodes[nbr]["parent"] = u
                if verbose:
                    print("  Relaxed ", nbr, " distance ", G.nodes[nbr]["distance"])

    return G # All data is stored in the graph




graph = random_weighted(6, 9, 11, random_state=42)
graph = merge_components(graph, wmax=11, random_state=42)
dijkstra_undirected(graph,0, True)

draw_weighted(graph)
