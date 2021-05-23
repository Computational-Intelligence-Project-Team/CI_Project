
import random

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
                    

def fitness():
    sum_fitness = []
    for i in b_population:
        sum_fitness[i] = sum(i)
    
    total = sum(sum_fitness)

    for i in range(len(sum_fitness)):
        fitness[i] = 1/sum_fitness


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

main()
