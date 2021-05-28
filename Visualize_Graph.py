import networkx as nx
import matplotlib.pyplot as plt



def visualizeClique(graph,cliqueNodes,graphName = None):
    node_colors = []
    for i in range(1,graph.number_of_nodes()+1):
        if i in cliqueNodes:
            node_colors.append("red")
        else:
            node_colors.append("blue")
    
    nx.draw_spring(graph, with_labels = True, node_color = node_colors)
    if graphName != None:
        plt.title(graphName)
    plt.show()
    
def visualizeCliqueSave(graph,cliqueNodes,fileName):
    node_colors = []
    for i in range(1,graph.number_of_nodes()+1):
        if i in cliqueNodes:
            node_colors.append("red")
        else:
            node_colors.append("blue")
    
    nx.draw_spring(graph, with_labels = True, node_color = node_colors)
    plt.savefig(fileName)
