import networkx
import csv   
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
    print("bpso Complete")
    avgFitness_bpso_LO, bestFitness_bpso_LO, maxCliqueNodes_bpso_LO = results_bpso(n_iters,graph)
    print("bpso_LO Complete")
    avgFitness_GA, bestFitness_GA, maxCliqueNodes_GA = results_GA(n_iters,graph)
    print("GA Complete")
    avgFitness_ACO, bestFitness_ACO, maxCliqueNodes_ACO = results_aco(n_iters,graph)
    print("ACO Complete")

    y_names = ['BPSO', "BPSO with Local Optimization","ACO", "GA"]
    plot_style = '*'
    
    # Plot Average Fitness comparision graphs
    avgFitness = {"Iterations" : iters, "BPSO": avgFitness_bpso, "BPSO with Local Optimization": avgFitness_bpso_LO 
        , "ACO" : avgFitness_ACO , "GA" : avgFitness_GA
    } 
    frame = pd.DataFrame(avgFitness)
    frame.plot(x ='Iterations', y = y_names)
    plt.title('Average Fitness against Number of Iterations')
    plt.ylabel("Fitness (Nodes in Clique)")
    plt.savefig('Plots/plot-average-fitness-' + graphName + '.png')
    plt.show()
    print(frame)

    # Plot Best Fitness comparision graphs
    bestFitness = {"Iterations" : iters, "BPSO": bestFitness_bpso, "BPSO with Local Optimization": bestFitness_bpso_LO  
       , "ACO" : bestFitness_ACO  , "GA" : bestFitness_GA
        } 
    frame = pd.DataFrame(bestFitness)
    frame.plot(x ='Iterations', y = y_names)
    plt.title('Best Fitness (Clique Size) against Number of Iterations')
    plt.ylabel("Fitness (Maximum Clique Nodes)")
    plt.savefig('Plots/plot-best-fitness-'+ graphName +'.png')
    plt.show()
    print(frame)

    visualizeClique(graph,maxCliqueNodes_bpso)
    visualizeClique(graph,maxCliqueNodes_bpso_LO)

def compare_metaheuristics_graphs(n_iters=15):
    
    print("Starting Comparision...")

    graphFileNames = os.listdir("Graphs/") 
    print(graphFileNames)
     
    fields=['Graph Name','BPSO','ACO']
    with open('output.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    
    allGraphNames = []
    bestFitness_bpso_LO = []
    # bestFitness_GA = [] 
    bestFitness_ACO = []
    iters = [i for i in range(n_iters)]
    for fileName in graphFileNames:
        graph = ImportGraph("Graphs/"+fileName)
        
        graphName = fileName[:-4]
        if graphName[-4:] == ".col":
            graphName = graphName[:-4]
        
        print(graphName)
        allGraphNames.append(graphName)

        bestFitness_bpso_LO.append(max(results_bpso_locally_optimized(n_iters,graph)[1]))
        # bestFitness_GA.append(max(results_GA(n_iters,graph)[1]))
        bestFitness_ACO.append(max(results_aco(n_iters,graph)[1])) 

        fields=[graphName,str(bestFitness_bpso_LO[-1]),bestFitness_ACO[-1]]
        with open('output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)


    bestFitness = {"Graph Name" : allGraphNames, "BPSO": bestFitness_bpso_LO  
    , "ACO" : bestFitness_ACO  ,# "GA" : bestFitness_GA
        } 
    frame = pd.DataFrame(bestFitness)
    frame.to_csv("Fitness_Comparision_Table.csv")
    print(frame)

graph1fileName = "Graphs/C125.9.txt"
graph2fileName = "Graphs/MANN_a27.txt"
G = ImportGraph(graph1fileName)

# compare_metaheuristics(G,1000)

# compare_metaheuristics_graphs(800)

