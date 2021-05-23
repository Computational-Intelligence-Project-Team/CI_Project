import networkx as nx
import matplotlib.pyplot as plt


def ImportGraph(fileName):

    with open(fileName, 'r') as f:
        content = f.read().splitlines()

    NumOfNodes = int(content[0])
    NumOfEdges = int(content[1])

    # Extract Edges
    content = content[2:]
    print(content)
    # content = [x.split()[1:] for x in content]
    edges = []

    for x in content:
        x = x.split()
        edges.append((int(x[1]), int(x[2])))

    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, NumOfNodes+1)])
    G.add_edges_from(edges)
    return G


# G = ImportGraph("r125.col.txt")
# nx.draw(G)
# plt.show()
