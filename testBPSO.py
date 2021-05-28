
from BPSO import *
from ImportGraph import *
from Visualize_Graph import *
from LocalOptimizationFunctions import ExpandExistingClique,LimitClique

graph1fileName = "Graphs/r125.1.col.txt"
graph2fileName = "Graphs/keller4.txt"
G = ImportGraph(graph1fileName)


def maxFunc(array):
    return maxCliqueFitness(array,G)

def ParticleExpandClique(array):
    return ExpandExistingClique(LimitClique(array,G),G)

# bpso = BPSO(numOfParticles=5, dimensions=G.number_of_nodes(),
#             fitnessFunc=maxFunc, maxIter=30, particleLocalOptimizationFunc = ParticleExpandClique,
#             printParticles = True, printGbest = True)

bpso = BPSO(numOfParticles=50, dimensions=G.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter=100, particleLocalOptimizationFunc = ParticleExpandClique,
            printParticles = False, printGbest = True)

bpso.benchmark()
maxCliqueNodes = bpso.gBestDimensionPositions()
print("maxCliqueNodes: ",maxCliqueNodes)
visualizeClique(G,maxCliqueNodes,"BPSO Max Clique")