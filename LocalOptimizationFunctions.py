import random
import numpy as np 

def ExpandClique(Chrom,G):
    #Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    if (sum(nodes) != 0):
        k = nodes.pop(random.randrange(len(nodes)))
    else:
        k = random.randint(1,len(G.nodes()))
    

    CliqueV = [] 
    CliqueV.append(k)

    for n in list(G.nodes()):
        if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                
    # Create New Chromosome of updated clique       
    NewChrom = np.zeros(len(Chrom))
    for v in CliqueV:
        NewChrom[v-1] = 1

    return NewChrom

def ExpandExistingClique(Chrom,G):
    #Chrom is a vector with binary values

    CliqueV = [] 
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            CliqueV.append(i+1)

    for n in list(G.nodes()):
        if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                
    # Create New Chromosome of updated clique       
    NewChrom = np.zeros(len(Chrom))
    for v in CliqueV:
        NewChrom[v-1] = 1

    return NewChrom


def LimitClique(Chrom,G):
    # Chrom is a vector with binary values

    nodes = []
    for i in range(len(Chrom)):
        if Chrom[i] == 1:
            nodes.append(i+1)

    if (sum(nodes) != 0):
        k = nodes.pop(random.randrange(len(nodes)))
    else:
        k = random.randint(1,len(G.nodes()))
        
    CliqueV = [] 
    CliqueV.append(k)

    for n in nodes:
        if all(True if n in G[v] else False for v in CliqueV): # If n is in the neighbourhood of all nodes in the clique
            CliqueV.append(n)
                

    # Create New Chromosome of updated clique       
    NewChrom = np.zeros(len(Chrom))
    for v in CliqueV:
        NewChrom[v-1] = 1

    return NewChrom

graph = {
    1:[2, 5], 
    2:[1, 3, 4, 6],
    3:[2, 4, 6], 
    4:[2, 3, 5, 6], 
    5:[1, 4, 6], 
    6:[2, 3, 4, 5]
    }

# Chrom = [1,1,1,1,1,0]

# print(LimitClique(Chrom,graph))