import networkx as nx
import matplotlib.pyplot as plt



def visualizeClique(graph,cliqueNodes):
    node_colors = []
    for i in range(1,graph.number_of_nodes()+1):
        if i in cliqueNodes:
            print(i)
            node_colors.append("red")
        else:
            node_colors.append("blue")
    
    nx.draw_planar(graph, with_labels = True, node_color = node_colors)
    plt.show()

graph = {
    0: [1, 2],
    1: [0, 2, 3, 4],
    2: [0, 1],
    3: [0, 1],
    4: [0, 1]
}
elist2 = [(0,1),(0,2),(1,2),(1,3),(1,4)]

G = nx.Graph()
elist = [(1, 2), (2, 3), (1, 4), (4, 2),(2,1)]
G.add_edges_from(elist)
cliqueNodes = [0,1,2]

visualizeClique(G,cliqueNodes)