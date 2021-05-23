import random
import numpy as np
 

population_size = 10
fitness = []
population = []
b_population = []
mutation_rate = 0.9

graph = {1:[2, 5], 
        2:[1, 3, 4, 6],
        3:[2, 4, 6], 
        4:[2, 3, 5, 6], 
        5:[1, 4, 6], 
        6:[2, 3, 4, 5]}

def init_pop():

    d = dict.fromkeys(graph)

    #select vertex for the creation of chromosomes
    selected_vertex = random.sample(list(d), len(d))
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
        print(i)
        print(b_population[new_parents[i]], b_population[new_parents[i+1]])
        child = crossover(b_population[new_parents[i]], b_population[new_parents[i+1]])
        children.append(child)
    return children
    
def crossover(parent1, parent2):
    child = np.bitwise_and(parent1, parent2)
    return child

def mutation(children_to_mutate, mutation_rate):
    for c in children_to_mutate:
        if(random.random() < mutation_rate ):

            #the selected vertex to flip
            vertex = random.randint(0, len(c) - 1 )
            print("vertex", vertex)

            #flipping
            c[vertex]= not c[vertex]

    return children_to_mutate


def clique_optimization():
    pass

def fps_survival():
    pass


def main():
    #function testing

    init_pop()
    fit()
    offspring = finding_children([0, 1, 2, 4, 5, 3])
    print("Offspring", offspring)

    mutated_offspring =  mutation(offspring, mutation_rate)
    print("Mutated Offspring", mutated_offspring)

main()
