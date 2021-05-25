import numpy
from ImportGraph import ImportGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import pandas as pd


class AntClique:
    def __init__(self, G, noAnts=10, taoMax=4, taoMin=0.01, decay=0.995, iterr=3000, alpha=2):
        self.noAnts = noAnts
        self.taoMax = taoMax
        self.taoMin = taoMin
        self.decay = decay
        self.iterr = iterr
        self.alpha = alpha
        self.pher_matrix = None
        self.G = G
        self.best_clique_global = []

    def init_pher_matrix(self):
        # initialize pheromone matrix with maximum tao value
        size = self.G.number_of_nodes()
        self.pher_matrix = np.zeros((size, size))

        for node in self.G.nodes():
            for nbr in self.G.neighbors(node):
                self.pher_matrix[node-1][nbr-1] = self.taoMax
        return self.pher_matrix

    def create_clique(self, indx):

        # initialize clique and possible candidates for clique as sets
        clique = set()
        candidates = set()

        def nbrs(node): return set(self.G.neighbors(node))

        def pher_clique_sum(node): return sum([
            self.pher_matrix[node-1][clique_node-1] for clique_node in clique])

        init_node = random.sample(self.G.nodes(), 1)[0]
        clique.add(init_node)
        candidates.update(self.G.neighbors(init_node))

        while candidates:
            # print(pher_matrix, clique)
            pher_values = [pher_clique_sum(
                node)**self.alpha for node in candidates]
            sum_pher = sum(pher_values)
            if sum_pher != 0:
                probs = [pher_value/sum_pher for pher_value in pher_values]
            else:
                probs = [0.0 for pher_value in pher_values]
            next_vertex = np.random.choice(
                list(candidates), size=1, p=probs)[0]
            clique.add(next_vertex)
            candidates = candidates.intersection(nbrs(next_vertex))
        return clique

    def update_pher_matrix(self, ant_cliques):
        best_clique = max(ant_cliques, key=lambda x: len(x))
        # print(best_clique)

        if len(best_clique) > len(self.best_clique_global):
            self.best_clique_global = best_clique.copy()

        best_len_global = len(self.best_clique_global)
        best_len = len(best_clique)

        # applying evaporation
        for node in self.G.nodes():
            for nbr in self.G.neighbors(node):
                if node != nbr:
                    self.pher_matrix[node-1][nbr -
                                             1] = max(self.taoMin, self.decay*self.pher_matrix[node-1][nbr-1])

        # updating the pheromone matrix according to the best ant in an iteration
        for node in best_clique:
            for nbr in self.G.neighbors(node):
                if node != nbr:
                    self.pher_matrix[node-1][nbr-1] = min(self.taoMax, (1/(
                        1 + best_len_global - best_len)) + self.pher_matrix[node-1][nbr-1])

    def max_clique_ACO(self):

        # initialize pheromone matrix
        self.pher_matrix = self.init_pher_matrix()
        # print(self.pher_matrix)
        # print(self.pher_matrix[29][9])
        best, avg = [], []
        ant_cliques = []
        for i in range(self.iterr):
            temp_avg = []
            for i in range(self.noAnts):
                clique = self.create_clique(i)
                ant_cliques.append(clique)
                temp_avg.append(len(clique))
            # ant_cliques = [self.create_clique(i) for i in range(self.noAnts)]
            self.update_pher_matrix(ant_cliques)
            best.append(len(self.best_clique_global))
            avg.append(sum(temp_avg)/self.noAnts)
        length = len(self.best_clique_global)
        print("The length of global best clear after",
              self.iterr, "iterations is", length)
        return avg, best


def results_aco(iterr, G):
    antClique = AntClique(G=G, iterr=iterr)
    avg, best = antClique.max_clique_ACO()
    return avg, best, antClique.best_clique_global


# G = ImportGraph("graphs/c125.9.txt")

# print(results_aco(10, G))
# print(ant.init_pher_matrix())
# print(ant.create_clique())
# print(ant.max_clique_ACO())


# G = nx.Graph()
# G.add_nodes_from([i for i in range(1, 6+1)])
# G.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 4), (2, 6),
#                   (3, 4), (3, 6), (4, 5), (5, 6), (4, 6)])

# def init_pher_matrix(G):
#     # initialize pheromone matrix with maximum tao value
#     size = G.number_of_nodes()
#     pher_matrix = np.zeros((size, size))

#     for node in G.nodes():
#         for nbr in G.neighbors(node):
#             pher_matrix[node-1][nbr-1] = taoMax
#     return pher_matrix


# def create_clique(G):

#     # initialize clique and possible candidates for clique as sets
#     clique = set()
#     candidates = set()

#     def nbrs(node): return set(G.neighbors(node))

#     def pher_clique_sum(node): return sum([
#         pher_matrix[node-1][clique_node-1] for clique_node in clique])

#     init_node = random.sample(G.nodes(), 1)[0]
#     clique.add(init_node)
#     candidates.update(G.neighbors(init_node))

#     while candidates:
#         # print(pher_matrix, clique)
#         pher_values = [pher_clique_sum(node)**alpha for node in candidates]
#         print(pher_values)
#         sum_pher = sum(pher_values)
#         if sum_pher != 0:
#             probs = [pher_value/sum_pher for pher_value in pher_values]
#         else:
#             probs = [0.0 for pher_value in pher_values]
#         print(probs)
#         next_vertex = np.random.choice(list(candidates), size=1, p=probs)[0]
#         clique.add(next_vertex)
#         candidates = candidates.intersection(nbrs(next_vertex))
#     return clique


# def update_pher_matrix(ant_cliques):
#     best_clique = max(ant_cliques, key=lambda x: len(x))
#     # print(best_clique)

#     if len(best_clique) > len(best_clique_global):
#         best_clique_global = best_clique.deepcopy()

#     best_len_global = len(best_clique_global)
#     best_len = len(best_clique)

#     for node in G.nodes():
#         for nbr in G.neighbors(node):
#             if n != nbr:
#                 pher_matrix[node-1][nbr -
#                                     1] = max(taoMin, decay*pher_matrix[node-1][nbr-1])

#     for node in best_clique:
#         for nbr in G.neighbors(node):
#             if n != nbr:
#                 pher_matrix[node-1][nbr-1] = min(taoMax, (1/(
#                     1 + best_len_global - best_len)) + pher_matrix[node-1][nbr-1])


# def max_clique_ACO(filname="graphs/r125.col-1.txt", noAnts_=7, taoMax_=4, taoMin_=0.01, decay_=0.995, alpha_=2, iterr_=3000):
#     #global parameters
#     global taoMax
#     global taoMin
#     global noAnts
#     global decay
#     global alpha
#     global iterr
#     global pher_matrix
#     global G

#     # initialize
#     # best_clique_global = None
#     noAnts = noAnts_
#     taoMax = taoMax_
#     taoMin = taoMin_
#     decay = decay_
#     iterr = iterr_
#     alpha = alpha_

#     #import Graph
#     G = nx.Graph()
#     G.add_nodes_from([i for i in range(1, 6+1)])
#     G.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 4), (2, 6),
#                       (3, 4), (3, 6), (4, 5), (5, 6), (4, 6)])

#     # initialize pheromone matrix
#     pher_matrix = init_pher_matrix(G)
#     # print(pher_matrix)

#     for i in range(iterr):
#         ant_cliques = [create_clique(G) for i in range(noAnts)]
#         update_pher_matrix(ant_cliques)
#     length = len(best_clique_global)
#     return length


# print(max_clique_ACO())
# # pher_matrix = init_pher_matrix(G)
# # print(create_clique(G))
