import networkx as nx


def ImportGraph(fileName):

    with open(fileName, 'r') as f:
        content = f.read().splitlines()

    # Extract Number of Nodes
    for line in content:
        if line[0] == "p":
            NumOfNodes = int(line.split()[2])
            break

    # Extract Edges
    i = 0
    while (i < len(content) and content[i][0] != 'e'):
        i += 1
    content = content[i:]
    edges = []
    for x in content:
        x = x.split()
        edges.append((int(x[1]), int(x[2])))

    # create graph
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, NumOfNodes+1)])
    G.add_edges_from(edges)
    return G
    
# ImportGraph("Graphs/r125.1.col.txt")
