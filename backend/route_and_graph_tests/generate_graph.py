import matplotlib.pyplot as plt
import networkx as nx
import random
import pickle as pkl
import math


def create_graph():
    G = nx.generators.directed.random_uniform_k_out_graph(20, 4, self_loops=False, seed=1)
    pos = nx.layout.spring_layout(G, seed=10)
    remove_edges = []

    for node_num in G.nodes:
        G.nodes[node_num]['x'] = pos[node_num][0] * 100
        G.nodes[node_num]['y'] = pos[node_num][1] * 100
        G.nodes[node_num]['elevation'] = random.randint(1, 50)
        # print(G.in_edges(node_num))
        # print(G.out_edges(node_num))
        # print(G.nodes[node_num])
        # print("\n")
        edges_in = {}
        edges_out = {}
        for edge in G.in_edges(node_num):
            if edge in edges_in:
                remove_edges.append(edge)
            else:
                edges_in[edge] = 'there'
        for edge in G.out_edges(node_num):
            if edge in edges_out:
                remove_edges.append(edge)
            else:
                edges_out[edge] = 'there'

    for edge in set(remove_edges):
        G.remove_edge(edge[0], edge[1])

    labels = {}
    for node_num in G.nodes:
        labels[node_num] = node_num

    for edge in G.edges:
        G.edges[edge[0], edge[1], 0]['length'] = int(distance(G.nodes[edge[0]], G.nodes[edge[1]]))
        print(G.edges[edge[0], edge[1], 0]['length'])

    pkl.dump(G, open("test_graph.pkl", "wb"))

    nx.draw(G, pos)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    nx.draw_networkx_edge_labels(G, pos)
    plt.show()


def distance(node1, node2):
    dx = node1['x'] - node2['x']
    dy = node1['y'] - node2['y']
    return math.sqrt(dx * dx + dy * dy)


if __name__ == "__main__":
    create_graph()
