import randomflow as rf
import fulkerson_parts as fp


# BFS for a flow graph

# flow - flow of the input graph
# cflow - solution flow

def ford_fulkerson(G, s_node, t_node):

    # Initialize
    for edge in G.edges:
        G.edges[edge]['cflow'] = 0

    # First time search for path
    Gf = fp.make_residual_net(G)
    s, cf = fp.extendi_path_step(Gf, s_node, t_node)
    print(s, cf)

    # Algorithm loop
    while s is not None:
        for i in range(0, len(s) - 1):
            u = s[i]
            v = s[i+1]
            if (u, v) in G.edges:
                G.edges[(u,v)]['cflow'] = G.edges[(u,v)]['cflow'] + cf
            else:
                G.edges[(v, u)]['cflow'] = G.edges[(v, u)]['cflow'] - cf

        Gf = fp.make_residual_net(G)
        s, cf = fp.extendi_path_step(Gf, s_node, t_node)


    return G

G = rf.random_flow_graph(3)
rf.draw_flow(G, 'flow')
G = ford_fulkerson(G, 0, 5)
rf.draw_flow(G, 'cflow')