import networkx as nx
def Kruskal(G):
    edgeList = [] # All edges
    tindex = [-1] * len(G.nodes) # Track which tree the nodes belong to
    currentTree = 0 # Tree index to add if new pair
    finalEdges = [] # Edges that make it into the final graph

    for edge in G.edges:
        edgeList.append([edge, G.edges[edge]["weight"]])

    k = lambda val : val[1]
    edgeList.sort(key=k)



    for edge in edgeList:
        t1 = tindex[edge[0][0]]
        t2 = tindex[edge[0][1]]
        add = False

        # Found new pair
        if (t1 == -1 and t2 == -1):
            add = True
            tindex[edge[0][0]] = currentTree
            tindex[edge[0][1]] = currentTree
            currentTree = currentTree + 1

        # Merge node into new tree
        if (t1 == -1 and t2 != -1):
            tindex[edge[0][0]] = tindex[edge[0][1]]
            add = True

        # Merge node into new tree
        if (t2 == -1 and t1 != -1):
            tindex[edge[0][1]] = tindex[edge[0][0]]
            add = True

        # Merge two trees
        if (t2 != -1 and t1 != -1 and t2 != t1):
            for i in range(0, len(G.nodes)):
                if (tindex[i] == t1):
                    tindex[i] = t2
            add = True

        # Add the edge to the graph
        if add:
            finalEdges.append(edge)

        same = False

        # Check if finished
        for i in range(0, len(G.nodes)):
            if not (tindex[i] == tindex[0] and tindex[i] != -1):
                break
            if i == len(G.nodes) - 1:
                same = True

        if same:
            break

    spanningTree = nx.Graph()
    for node in range(0, len(G.nodes)):
        spanningTree.add_node(node)
    for edge in finalEdges:
        spanningTree.add_edge(edge[0][0], edge[0][1], weight=edge[1])
    return spanningTree
