
from BPSO import *
from ImportGraph import *
from Visualize_Graph import *
from LocalOptimizationFunctions import ExpandExistingClique,LimitClique

graph1fileName = "Graphs/C125.9.txt"
G = ImportGraph(graph1fileName)

print("G",G[5])

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

bpso.execute()
maxCliqueNodes = bpso.gBestDimensionPositions()
print("maxCliqueNodes: ",maxCliqueNodes)
visualizeClique(G,maxCliqueNodes)