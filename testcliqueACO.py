from cliqueAco import *
from ImportGraph import *
from Visualize_Graph import *


graph1fileName = "Graphs/r125.1.col.txt"
graph2fileName = "Graphs/keller4.txt"
G = ImportGraph(graph1fileName)

maxCliqueNodes = results_aco(50, G)[2]
print("maxCliqueNodes: ",maxCliqueNodes)
visualizeClique(G,maxCliqueNodes,"ACO Max Clique")