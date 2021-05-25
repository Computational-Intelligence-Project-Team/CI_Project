import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from BPSO import *
from ImportGraph import *
from Visualize_Graph import *
from LocalOptimizationFunctions import ExpandExistingClique,LimitClique


graph1fileName = "Graphs/C125.9.txt"
G = ImportGraph(graph1fileName)

print("G",G[36])

def maxFunc(array):
    return maxCliqueFitness(array,G)

def ParticleExpandClique(array):
    return ExpandExistingClique(LimitClique(array,G),G)

def results_bpso_locally_optimized(Iters,Graph):
    bpso = BPSO(numOfParticles=50, dimensions=G.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter= Iters, particleLocalOptimizationFunc = ParticleExpandClique,
            printParticles = False, printGbest = False)
    return bpso.benchmark()

def results_bpso(Iters,Graph):
    bpso = BPSO(numOfParticles=50, dimensions=G.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter= Iters, particleLocalOptimizationFunc = None,
            printParticles = False, printGbest = False)
    return bpso.benchmark()

def compare_Fitness(graph,n_iters=15):
    
    iters = [i for i in range(n_iters)]
    avgFitness_bpso,bestFitness_bpso,maxCliqueNodes_bpso = results_bpso(n_iters,graph)
    avgFitness_bpso_LO,bestFitness_bpso_LO, maxCliqueNodes_bpso_LO = results_bpso(n_iters,graph)

    avgFitness = {"Iterations" : iters, "BPSO": avgFitness_bpso, "BPSO with Local Optimization": avgFitness_bpso_LO } 
    frame = pd.DataFrame(avgFitness)
    frame.plot(x ='Iterations', y=['BPSO', "BPSO with Local Optimization"], style='o')
    plt.title('Average Fitness against Number of Iterations')
    plt.savefig('Plots/plot-average-fitness.png')
    plt.show()
    print(frame)

    bestFitness = {"Iterations" : iters, "BPSO": avgFitness_bpso, "BPSO with Local Optimization": avgFitness_bpso_LO } 
    frame = pd.DataFrame(avgFitness)
    frame.plot(x ='Iterations', y=['BPSO', "BPSO with Local Optimization"], style='o')
    plt.title('Average Fitness against Number of Iterations')
    plt.savefig('Plots/plot-average-fitness.png')
    plt.show()
    print(frame)


compare_avgFitness(G,400)

# bpso = BPSO(numOfParticles=5, dimensions=G.number_of_nodes(),
#             fitnessFunc=maxFunc, maxIter=30, particleLocalOptimizationFunc = ParticleExpandClique,
#             printParticles = True, printGbest = True)
