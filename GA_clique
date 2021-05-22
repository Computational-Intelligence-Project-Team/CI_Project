
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

    

def main():
    init_pop()

main()
