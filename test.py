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

def LimitClique(Chrom,G):
    # Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    k = nodes.pop(random.randrange(len(nodes)))
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

graph = {1:[2, 5], 
    2:[1, 3, 4, 6],
    3:[2, 4, 6], 
    4:[2, 3, 5, 6], 
    5:[1, 4, 6], 
    6:[2, 3, 4, 5]}

Chrom = [1,1,1,1,1,0]

print(LimitClique(Chrom,graph))


import matplotlib.pyplot as plt
import numpy as np

# Some example data to display
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))

plt.show()