from random import random
import numpy as np
import random

# print(np.logical_xor([1, 1, 0, 0], [1, 0, 1, 0]))
# print(1 & 0)

# import networkx as nx
# G = nx.Graph()
# elist = [(1, 2), (2, 3), (1, 4), (4, 2), (2,1)]
# G.add_edges_from(elist)
# print(G[1])
# for i in G[1]:
#     print(i)

# L = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0"

# c = 0
# while c < len(L):
#     # print(c)
#     if L[c] == '1':
#         print(c//2)
#     c+=2

def ExpandClique(Chrom,G):
    # Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    k = nodes.pop(random.randrange(len(nodes)))
    CliqueV = [] 
    CliqueV.append(k)

    for n in nodes:
        if all( if (n in G[v]) for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                

    # Create New Chromosome of updated clique       
    NewChrom = [0] * len(Chrom)
    for v in CliqueV:
        NewChrom[v-1] = 1
    

