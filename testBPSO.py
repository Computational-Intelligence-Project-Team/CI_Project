
from BPSO import *
from ImportGraph import *
from Visualize_Graph import *

G = ImportGraph("Graphs/r125.1.col.txt")
print("G",G[5])

def maxFunc(array):
    return maxCliqueFitness(array,G)

bpso = BPSO(numOfParticles=30, dimensions=G.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter=100)
bpso.execute()
maxCliqueNodes = bpso.gBestDimensionPositions()

visualizeClique(G,maxCliqueNodes)