import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import random
import pickle as pkl
import heapq
from itertools import count
import math


def create_graph():
    G = nx.generators.directed.random_uniform_k_out_graph(10, 2, self_loops=False, seed=1)
    pos = nx.layout.spring_layout(G)
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

    for node_num in G.nodes:
        print(G.in_edges(node_num))
        print(G.out_edges(node_num))
        print("\n")

    for edge in G.edges:
        G.edges[edge[0], edge[1], 0]['length'] = distance(G.nodes[edge[0]], G.nodes[edge[1]])
        print(G.edges[edge[0], edge[1], 0]['length'])

    pkl.dump(G, open("test_graph.pkl", "wb"))

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos)
    # nx.draw_networkx_edge_labels(G, pos)
    # plt.show()
    node_sizes = [10 for i in range(len(G))]
    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                                   arrowsize=10, edge_color=edge_colors, width=2)

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()


def distance(node1, node2):
    dx = node1['x'] - node2['x']
    dy = node1['y'] - node2['y']
    return math.sqrt(dx * dx + dy * dy)


if __name__ == "__main__":
    create_graph()
