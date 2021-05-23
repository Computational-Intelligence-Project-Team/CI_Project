import numpy
from ImportGraph import ImportGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


#global parameters
noAnts = 7
taoMax = 4
taoMin = 0.01
decay = 0.995
iterr = 10
alpha = 2
pher_matrix = None
G = None

G = nx.Graph()
G.add_nodes_from([i for i in range(1, 6+1)])
G.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 4), (2, 6),
                  (3, 4), (3, 6), (4, 5), (5, 6), (4, 6)])


def init_pher_matrix(G):
    # initialize pheromone matrix with maximum tao value
    size = G.number_of_nodes()
    pher_matrix = np.zeros((size, size))

    for node in G.nodes():
        for nbr in G.neighbors(node):
            pher_matrix[node-1][nbr-1] = taoMax
    return pher_matrix


def create_clique(G):

    # initialize clique and possible candidates for clique as sets
    clique = set()
    candidates = set()

    def nbrs(node): return set(G.neighbors(node))

    def pher_clique_sum(node): return sum([
        pher_matrix[node-1][clique_node-1] for clique_node in clique])

    init_node = random.sample(G.nodes(), 1)[0]
    clique.add(init_node)
    candidates.update(G.neighbors(init_node))

    while candidates:
        # print(pher_matrix, clique)
        pher_values = [pher_clique_sum(node-1)**alpha for node in candidates]
        print(pher_values)
        sum_pher = sum(pher_values)
        if sum_pher != 0:
            probs = [pher_value/sum_pher for pher_value in pher_values]
        else:
            probs = [0.0 for pher_value in pher_values]
        print(probs)
        next_vertex = np.random.choice(list(candidates), size=1, p=probs)[0]
        clique.add(next_vertex)
        candidates = candidates.intersection(nbrs(next_vertex))
    return clique


def update_pher_matrix(ant_cliques, best_clique_global):
    best_idx, best_clique = max(ant_cliques, key=lambda x: len(x[1]))

    if len(best_clique) > len(best_clique_global):
        best_clique_global = best_clique.copy()

    best_len_global = len(best_clique_global)
    best_len = len(best_clique)

    for node in G.nodes():
        for nbr in G.neighbors(node):
            if n != nbr:
                pher_matrix[node-1][nbr -
                                    1] = max(taoMin, decay*pher_matrix[node-1][nbr-1])

    for node in best_clique:
        for nbr in G.neighbors(node):
            if n != nbr:
                pher_matrix[node-1][nbr-1] = min(taoMax, (1/(
                    1 + best_len_global - best_len)) + pher_matrix[node-1][nbr-1])


def max_clique_ACO(filname="graphs/r125.col-1.txt", noAnts_=7, taoMax_=4, taoMin_=0.01, decay_=0.995, alpha_=2, iterr_=3000):
    #global parameters
    global taoMax
    global taoMin
    global noAnts
    global decay
    global alpha
    global iterr
    global best_clique_global
    global pher_matrix
    global G

    # initialize
    best_clique_global = None
    noAnts = noAnts_
    taoMax = taoMax_
    taoMin = taoMin_
    decay = decay_
    iterr = iterr_
    alpha = alpha_

    #import Graph
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, 6+1)])
    G.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 4), (2, 6),
                      (3, 4), (3, 6), (4, 5), (5, 6), (4, 6)])

    # initialize pheromone matrix
    pher_matrix = init_pher_matrix(G)
    # print(pher_matrix)

    for i in range(iterr):
        ant_cliques = [create_clique(G) for i in range(noAnts)]
        update_pher_matrix(ant_cliques, best_clique_global)
    length = len(best_clique_global)
    return length


pher_matrix = init_pher_matrix(G)
print(create_clique(G))
