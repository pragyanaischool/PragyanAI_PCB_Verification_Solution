import networkx as nx
import math

def build_graph(components):

    G = nx.Graph()

    for i, comp in enumerate(components):
        G.add_node(i, pos=comp["center"])

    for i in range(len(components)):
        for j in range(i+1, len(components)):

            x1, y1 = components[i]["center"]
            x2, y2 = components[j]["center"]

            if math.hypot(x1-x2, y1-y2) < 200:
                G.add_edge(i, j)

    return G
