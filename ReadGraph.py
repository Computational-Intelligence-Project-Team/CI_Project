import networkx as nx

def importGraphs(fileName):

    with open(fileName, 'r') as f:
        content = f.read().splitlines()
    
    
    i = 0
    while (i < len(content) and content[i][0] != 'e'):
        i+=1
    content = content[i:]
    content = [x.split()[1:] for x in content]
    
    edges = [(int(x[0]),int(x[1])) for x in content]

    for j in edges:
        print(j)
    
    return edges
    
importGraphs("Graphs/r125.1.col.txt")
