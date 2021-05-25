import networkx as nx

def ImportGraph(fileName):

    with open(fileName, 'r') as f:
        content = f.read().splitlines()

    # Extract Number of Nodes
    for line in content:
        if "c number of vertices :" in line:
            NumOfNodes = int(line.split()[-1])
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

# def ImportGraph(fileName):

#     with open(fileName, 'r') as f:
#         content = f.read().splitlines()
    
#     # Extract Number of Nodes
#     for line in content:
#         if "c number of vertices :" in line:
#             NumOfNodes = int(line.split()[-1])
#             break
    
#     # Extract Edges
#     i = 0
#     while (i < len(content) and content[i][0] != 'e'):
#         i+=1
#     content = content[i:]
#     content = [x.split()[1:] for x in content]
    
#     edges = [(int(x[0]),int(x[1])) for x in content]

#     # for j in edges:
#     #     print(j)
    
#     G = nx.Graph()
#     G.add_nodes_from([i for i in range(1,NumOfNodes+1)])
#     G.add_edges_from(edges)
#     return G
    
# ImportGraph("Graphs/r125.1.col.txt")
