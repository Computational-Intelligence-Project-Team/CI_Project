import networkx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os      

from BPSO import *
from GA_clique import *
from cliqueAco import results_aco 

from ImportGraph import *
from Visualize_Graph import *
from LocalOptimizationFunctions import ExpandExistingClique,LimitClique


graph1fileName = "Graphs/C125.9.txt"
G = ImportGraph(graph1fileName)


def results_GA(Iters,Graph):
    return main(Iters,nx.to_dict_of_lists(Graph))
 
def results_bpso_locally_optimized(Iters,Graph):
    def maxFunc(array):
        return maxCliqueFitness(array,Graph)

    def ParticleExpandClique(array):
        return ExpandExistingClique(LimitClique(array,Graph),Graph)

    bpso = BPSO(numOfParticles=100, dimensions=Graph.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter= Iters, particleLocalOptimizationFunc = ParticleExpandClique,
            printParticles = False, printGbest = False)
    return bpso.benchmark()

def results_bpso(Iters,Graph):
    def maxFunc(array):
        return maxCliqueFitness(array,Graph)

    bpso = BPSO(numOfParticles=200, dimensions=Graph.number_of_nodes(),
            fitnessFunc=maxFunc, maxIter= Iters, particleLocalOptimizationFunc = None,
            printParticles = False, printGbest = False)
    return bpso.benchmark()



def compare_metaheuristics(graph,n_iters=15,graphName = "C125.9"):
    print("Starting Comparision...")

    iters = [i for i in range(n_iters)]
    avgFitness_bpso, bestFitness_bpso, maxCliqueNodes_bpso = results_bpso(n_iters,graph)
    avgFitness_bpso_LO, bestFitness_bpso_LO, maxCliqueNodes_bpso_LO = results_bpso(n_iters,graph)
    avgFitness_GA, bestFitness_GA, maxCliqueNodes_GA = results_GA(n_iters,graph)
    avgFitness_ACO, bestFitness_ACO, maxCliqueNodes_ACO = results_aco(n_iters,graph)

    y_names = ['BPSO', "BPSO with Local Optimization","ACO", "GA"]
    plot_style = '*'
    
    avgFitness = {"Iterations" : iters, "BPSO": avgFitness_bpso, "BPSO with Local Optimization": avgFitness_bpso_LO 
        , "ACO" : avgFitness_ACO , "GA" : avgFitness_GA
    } 
    frame = pd.DataFrame(avgFitness)
    frame.plot(x ='Iterations', y = y_names, style=plot_style)
    plt.title('Average Fitness against Number of Iterations')
    plt.savefig('Plots/plot-average-fitness-' + graphName + '.png')
    plt.show()
    print(frame)

    bestFitness = {"Iterations" : iters, "BPSO": bestFitness_bpso, "BPSO with Local Optimization": bestFitness_bpso_LO  
       , "ACO" : bestFitness_ACO  , "GA" : bestFitness_GA
        } 
    frame = pd.DataFrame(bestFitness)
    frame.plot(x ='Iterations', y = y_names, style=plot_style)
    plt.title('Best Fitness (CLique Size) against Number of Iterations')
    plt.savefig('Plots/plot-best-fitness-'+ graphName +'.png')
    plt.show()
    print(frame)

def compare_metaheuristics_graphs(n_iters=15):
    print("Starting Comparision...")

    graphFileNames = os.listdir("Graphs/") 
    allGraphNames = []
    bestFitness_bpso = []
    bestFitness_bpso_LO = []
    bestFitness_GA = [] 
    bestFitness_ACO = []
    iters = [i for i in range(n_iters)]

    for fileName in graphFileNames:
        graph = ImportGraph("Graphs/"+fileName)
        
        graphName = fileName[:-5]
        if graphName[-4:] == ".col":
            graphName = graphName[:-5]
        
        print(graphName)
        allGraphNames.append(graphName)

        bestFitness_bpso.append(max(results_bpso(n_iters,graph)[1]))
        bestFitness_bpso_LO.append(max(results_bpso_locally_optimized(n_iters,graph)[1]))
        bestFitness_GA.append(max(results_GA(n_iters,graph)[1]))
        bestFitness_ACO.append(max(results_aco(n_iters,graph)[1]))    


    bestFitness = {"Graph Name" : iters, "BPSO": bestFitness_bpso, "BPSO with Local Optimization": bestFitness_bpso_LO  
    , "ACO" : bestFitness_ACO  , "GA" : bestFitness_GA
        } 
    frame = pd.DataFrame(bestFitness)
    print(frame)


# compare_metaheuristics(G,400)

compare_metaheuristics_graphs(3)

