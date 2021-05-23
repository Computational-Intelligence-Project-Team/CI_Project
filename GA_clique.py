
import random
import numpy as np

population_size = 3
fitness = []
population = []
b_population = []

graph = {1:[2, 5], 
        2:[1, 3, 4, 6],
        3:[2, 4, 6], 
        4:[2, 3, 5, 6], 
        5:[1, 4, 6], 
        6:[2, 3, 4, 5]}

def init_pop():

    d = dict.fromkeys(graph)

    #select vertex for the creation of chromosomes
    selected_vertex = random.sample(list(d), population_size)
    print(selected_vertex)
    for vert in selected_vertex:
        chrom = []
        b_chrom = [0]*6
        chrom.append(vert)
        print("selected vertex = ", vert)
        b_chrom[vert-1] = 1

        for k,v in graph.items():
            if k == vert:
                for edge in v:
                    for i in chrom:
                        if edge in graph[i]:
                            present = True
                        else:
                            present = False
                            break

                    if present == True:
                       chrom.append(edge)
                       b_chrom[edge-1] = 1
                    else:
                       b_chrom[edge-1] = 0

        population.append(chrom)
        b_population.append(b_chrom)
        print("chromosome = ", chrom)
        print("binary_chromosome = ", b_chrom, "\n")


    
    print("vertex clique representation = ", population)
    print("binary clique population = ", b_population)
                    

def fit():
    sum_fitness = []
    for i in range(len(b_population)):
        sum_fitness.append(sum(b_population[i]))
    
    total = sum(sum_fitness)

    for i in range(len(sum_fitness)):
        fitness.append(sum_fitness[i]/total)
    
    print("Fitness array", fitness)

def fps_parent():

    pass

def finding_children(new_parents): #new parents is the list of indices of the parent
    children = []
    for i in range(0, len(new_parents), 2):
        print(b_population[new_parents[i]], b_population[new_parents[i+1]])
        child = crossover(b_population[new_parents[i]], b_population[new_parents[i+1]])
        children.append(child)
    return children
    
def crossover(parent1, parent2):
    child = np.bitwise_and(parent1, parent2)
    return child


def LimitClique(Chrom,G):
    # Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    k = nodes.pop(random.randrange(len(nodes)))
    print(k)
    CliqueV = [] 
    CliqueV.append(k)

    for n in nodes:
        if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                
    print(CliqueV)
    # Create New Chromosome of updated clique       
    NewChrom = [0] * len(Chrom)
    for v in CliqueV:
        NewChrom[v-1] = 1

    return NewChrom

def main():
    init_pop()
    fit()
    offspring = finding_children([0, 2])
    print("Offspring", offspring)

main()
