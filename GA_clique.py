import random
import numpy as np
import pandas as pd

population_size = 5
no_parents = 2
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
    selected_vertex = random. sample(range(len(d)), population_size)
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
                    


def fit(arr):
    # fitness = []
    for i in range(len(arr)):
        fitness.append(sum(arr[i]))

    print("fitness" , fitness)
    # return fitness
    # total = sum(sum_fitness)

    # for i in range(len(sum_fitness)):
    #     fitness.append(sum_fitness[i]/total)

    # print("Fitness array", fitness)

def fps_selection(fitness, no_parents, survival=False):
    selected = list()
    prob = []

    # calculating fitness probability
    sum_fitness = np.sum(fitness)
    if survival:
        selected = set()
        for i in range(len(fitness)):
            prob.append((sum_fitness-fitness[i])/sum_fitness)
    else:
        for i in range(len(fitness)):
            prob.append(fitness[i]/sum_fitness)
    print("probilities = ", prob)
    # cumulative sum
    series = pd.Series(prob)
    cums_prob = series.cumsum()
    print("cumulative probs", cums_prob)

    # selecting parents/non-survivors
    while len(selected) < no_parents:
        rand = random.random()
        # print(cums_prob)
        if rand < cums_prob[0]:
            if survival:
                selected.add(0)
            else:
                selected.append(0)
        else:
            for j in range(population_size):
                if cums_prob[j] < rand < cums_prob[j+1]:
                    if survival:
                        selected.add(j+1)
                    else:
                        selected.append(j+1)
                    break
    return list(selected)





def finding_children(new_parents): #new parents is the list of indices of the parent
    children = []
    for i in range(0, len(new_parents), 2):
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


def ExpandClique(Chrom,G):
    #Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    if (sum(nodes) != 0):
        k = nodes.pop(random.randrange(len(nodes)))
    else:
        k = random.randint(1,len(graph.keys()))
    
    print(k)

    CliqueV = [] 
    CliqueV.append(k)

    for n in graph.keys():
        if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                
    print(CliqueV)

    # Create New Chromosome of updated clique       
    NewChrom = [0] * len(Chrom)
    for v in CliqueV:
        NewChrom[v-1] = 1

    print("new", NewChrom)
    return NewChrom

def trunc():
    worst = []
    for i in range(no_parents//2):
        worst.append(fitness.index(min(fitness)))
    
    return worst
    




def add_to_pop(new_members):
    for i in new_members: 
        b_population.append(i)
    fit(new_members)

def pop_resize(selected):

    for i in selected:
        del b_population[i]
        del fitness[i]


def clique_optimization():
    pass

def main():
    #function testing
    generations = 10
    init_pop()
    fit(b_population)
    for num in range(generations):

        parents = fps_selection(fitness, no_parents, False)
        print("parents", parents)
        
        offspring = finding_children(parents)
        print("Offspring", offspring)

        mutated_offspring =  mutation(offspring, mutation_rate)
        print("Mutated Offspring", mutated_offspring)

        #check if each offspring satisfies the condition of a clique
        #if not a clique, then make it a clique
        for y in range(len(mutated_offspring)):
            mutated_offspring[y] = ExpandClique(mutated_offspring[y], graph)

        print("mutated_final_cliques", mutated_offspring)

        add_to_pop(mutated_offspring)
        print(len(b_population))
        to_remove = trunc()
        print("indices to be removed from pop", to_remove)

        pop_resize(to_remove)

        print(len(b_population))

        print("final fitness array", fitness)


main()
