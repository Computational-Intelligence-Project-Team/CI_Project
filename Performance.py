import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from BPSO import *
from GA_clique import main
from cliqueAco import results_aco 

from ImportGraph import *
from Visualize_Graph import *
from LocalOptimizationFunctions import ExpandExistingClique,LimitClique


graph1fileName = "Graphs/C125.9.txt"
G = ImportGraph(graph1fileName)


def maxFunc(array):
    return maxCliqueFitness(array,G)

def ParticleExpandClique(array):
    return ExpandExistingClique(LimitClique(array,G),G)

def results_GA(Iters,Graph):
    return main(nx.to_dict_of_lists(Graph),Iters)
 
def results_bpso_locally_optimized(Iters,Graph):
    bpso = BPSO(numOfParticles=50, dimensions=Graph.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter= Iters, particleLocalOptimizationFunc = ParticleExpandClique,
            printParticles = False, printGbest = False)
    return bpso.benchmark()

def results_bpso(Iters,Graph):
    bpso = BPSO(numOfParticles=50, dimensions=Graph.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter= Iters, particleLocalOptimizationFunc = None,
            printParticles = False, printGbest = False)
    return bpso.benchmark()



def compare_metaheuristics(graph,n_iters=15):
    print("Starting Comparision...")
    iters = [i for i in range(n_iters)]
    avgFitness_bpso, bestFitness_bpso, maxCliqueNodes_bpso = results_bpso(n_iters,graph)
    avgFitness_bpso_LO, bestFitness_bpso_LO, maxCliqueNodes_bpso_LO = results_bpso(n_iters,graph)
    avgFitness_GA, bestFitness_GA, maxCliqueNodes_GA = results_GA(n_iters,graph)
    avgFitness_ACO, bestFitness_ACO, maxCliqueNodes_ACO = results_aco(n_iters,graph)

    y_names = ['BPSO', "BPSO with Local Optimization","ACO"]
    
    avgFitness = {"Iterations" : iters, "BPSO": avgFitness_bpso, "BPSO with Local Optimization": avgFitness_bpso_LO 
        , "ACO" : avgFitness_ACO #, "GA" : avgFitness_GA
    } 
    frame = pd.DataFrame(avgFitness)
    frame.plot(x ='Iterations', y = y_names, style='o')
    plt.title('Average Fitness against Number of Iterations')
    plt.savefig('Plots/plot-average-fitness.png')
    plt.show()
    print(frame)

    bestFitness = {"Iterations" : iters, "BPSO": bestFitness_bpso, "BPSO with Local Optimization": bestFitness_bpso_LO  
       , "ACO" : bestFitness_ACO # , "GA" : bestFitness_GA
        } 
    frame = pd.DataFrame(bestFitness)
    frame.plot(x ='Iterations', y = y_names, style='o')
    plt.title('Best Fitness (CLique Size) against Number of Iterations')
    plt.savefig('Plots/plot-best-fitness.png')
    plt.show()
    print(frame)


compare_metaheuristics(G,800)

