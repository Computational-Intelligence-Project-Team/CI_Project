import random
import numpy as np
import pandas as pd
import networkx as nx

population_size = 20
no_parents = 2
fitness = []
population = []
b_population = []
mutation_rate = 1
crossover_rate = 0.1
# G = {}

# graph = {1:[2, 5], 
#         2:[1, 3, 4, 6],
#         3:[2, 4, 6], 
#         4:[2, 3, 5, 6], 
#         5:[1, 4, 6], 
#         6:[2, 3, 4, 5]}

def importGs(G, fileName):

    with open(fileName, 'r') as f:
        content = f.read().splitlines()

    # Extract Number of Nodes
    for line in content:
        if "c number of vertices :" in line:
            NumOfNodes = int(line.split()[-1])
            # print(NumOfNodes)
            break

    # total_vertices = 6
    indices = list(range(1, NumOfNodes))
    i = 0
    while (i < len(content) and content[i][0] != 'e'):
        i+=1
    content = content[i:]
    content = [x.split()[1:] for x in content]
    
    relation = [(int(x[0]),int(x[1])) for x in content]

    #dictionary initialization
    # G = {}
    
    #Using networkx to solve 
    temp = nx.Graph(relation)
    temp.add_nodes_from(indices)
    G = nx.to_dict_of_lists(temp)


    # print(G)
    # print(len(G.keys()))
    return G

def init_pop(G):
    # print("len(graph.keys())", len(G.keys()))
    vertices = random.sample(range(1,len(G.keys())+1), population_size)
    # print(vertices)

    for vert in vertices:
        CliqueV = [] 
        CliqueV.append(vert)
        # print(graph[vert])
        random.shuffle(G[vert])
        # print(random_values)
        # print(graph[vert])
        for n in G[vert]:
            if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
                CliqueV.append(n)

        # Create New Chromosome of updated clique       
        NewChrom = [0] * len(G.keys())
        for v in CliqueV:
            NewChrom[v-1] = 1
        b_population.append(NewChrom)

    # print("new", b_population)
    return G




def fit(arr):
    # fitness = []
    for i in range(len(arr)):
        fitness.append(sum(arr[i]))

    # print("fitness" , fitness)


def fps_selection(no_parents, survival=False):
    selected = list()
    prob = []
    # print("fitness", fitness)

    # calculating fitness probability
    sum_fitness = np.sum(fitness)
    sum_fitness_inv = - np.sum(fitness - sum_fitness)
    if survival:
        selected = set()
        for i in range(len(fitness)):
            prob.append((sum_fitness-fitness[i])/sum_fitness_inv)
    else:
        for i in range(len(fitness)):
            prob.append(fitness[i]/sum_fitness)

    # print("prob", prob)


    # cumulative sum
    series = pd.Series(prob)
    cums_prob = series.cumsum()
    # print(cums_prob)



    # selecting parents/non-survivors
    if survival == True:
        count = no_parents//2
    else:
        count = no_parents

    while len(selected) < count:
        rand = random.random()
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



# def random():




def finding_children(new_parents): #new parents is the list of indices of the parent
    children = []
    for i in range(0, len(new_parents), 2):
        child = crossover(b_population[new_parents[i]], b_population[new_parents[i+1]])
        children.append(child)
    return children
    
def crossover(parent1, parent2):
    if(random.random() < crossover_rate ):
        child = np.bitwise_and(parent1, parent2)
    else: 
        child = parent1           #if crossover doesnt happen then just return a copy of a parent
    return child

def mutation(children_to_mutate, mutation_rate):
    for c in children_to_mutate:
        if(random.random() < mutation_rate ):

            #the selected vertex to flip
            vertex = random.randint(0, len(c) - 1 )
            # print("vertex", vertex)

            #flipping
            c[vertex]= 1 - c[vertex]

    return children_to_mutate

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


# ------------------------- Clique optimization functions ----------------
def check_Clique(Chrom, G):
    #Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    if (sum(nodes) != 0):
        k = nodes.pop(random.randrange(len(nodes)))
    else:
        k = random.randint(1, len(G.keys()))
    
    # print(k)

    CliqueV = [] 
    CliqueV.append(k)
    # m = G.keys()
    # random.shuffle(m)
    for n in G.keys():
        if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                
    # print(CliqueV)

    # Create New Chromosome of updated clique       
    NewChrom = [0] * len(Chrom)
    for v in CliqueV:
        NewChrom[v-1] = 1

    # print("new", NewChrom)
    return NewChrom


def expand_clique(Chrom, G):

    #elements not a part of the clique
    nodes0 = []
    for i in range(len(Chrom)):
        if Chrom[i] == 0:
            nodes0.append(i+1)

    #already present clique elements
    nodes1 = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes1.append(i+1)

    
    #we now have all the indexes and vertices where we have a zero and currently
    #they are not a part of the clique
    new_clique_elements = [] 
    # CliqueV.append(k)

    for i in nodes0:
        for x in nodes1:
            if i in G[x]:
                p = True
            else:
                p = False
                break
        
        if p == True:
            new_clique_elements.append(i)

    # print("new", new_clique_elements)
    # Create New Chromosome of updated clique       
    # NewChrom = [0] * len(Chrom)
    for v in new_clique_elements:
        Chrom[v-1] = 1

    return Chrom




#--------------------------------------- main ------------------------
def results_ga(generations, gr):

    # G = importGs(G, "graphs\c125.9.txt")

    return main(generations, gr)


def main(iterr, graph):
    #function testing
    G = graph
    generations = iterr

    init_pop(G)
    # print("G", G)

    # print("Binary population", b_population)
    fit(b_population)
    # print("fitnesss", fitness)

    max_fitness_array = []
    avg_fitness_array = []
    max_nodes = []

    for num in range(generations):

        parents = fps_selection(no_parents, False)
        # print("parents", parents)
        
        offspring = finding_children(parents)
        for y in range(len(offspring)):
            offspring[y] = check_Clique(offspring[y] , G)

        # print("Offspring", offspring)

        mutated_offspring =  mutation(offspring, mutation_rate)
        # print("Mutated Offspring", mutated_offspring)

        #check if each offspring satisfies the condition of a clique
        #if not a clique, then make it a clique
        for y in range(len(mutated_offspring)):
            mutated_offspring[y] = check_Clique(mutated_offspring[y], G)

        for y in range(len(mutated_offspring)):   
            mutated_offspring[y] = expand_clique(mutated_offspring[y], G)
        # print("mutated_final_cliques", mutated_offspring)

        add_to_pop(mutated_offspring)
        # print("after add to pop", len(b_population))
        # to_remove = fps_selection(no_parents, True)
        to_remove = trunc()
        # print("indices to be removed from pop", to_remove)

        pop_resize(to_remove)

        # print(len(b_population))

        # print("final fitness array", fitness)

        #for graphs
        avg_fitness_array.append(sum(fitness)/population_size)
        max_fitness_array.append(max(fitness))

    #----------------------------------------------------for graph---------------------------------------------#
    max_clique_idx = fitness.index(max(fitness))
    max_clique_chrom = b_population[max_clique_idx]

    # print("max_clique_chrom", max_clique_chrom)
    for i in range(len(max_clique_chrom)):
        if max_clique_chrom[i] == 1:
            max_nodes.append(i+1)
        
    return (max_fitness_array, avg_fitness_array, max_nodes)



G = {}
G = importGs(G, "graphs/C125.9.txt")
print(results_ga(100, G))
