import pickle as pkl
import networkx as nx
from backend.src.context import Context
from backend.src import strategies

graph = None


def load_graph():
    global graph
    with open("test_graph.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded test graph')


def dijkstra_shortest_path():
    print("Dijkstra shortest path")
    context = Context(strategies.StrategyDijkstra(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def dijkstra_min_elevation():
    print("Dijkstra min elevation")
    context = Context(strategies.StrategyDijkstra(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def dijkstra_max_elevation():
    print("Dijkstra max elevation")
    context = Context(strategies.StrategyDijkstra(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def bfs_shortest_path():
    print("BFS shortest path")
    context = Context(strategies.StrategyBFS(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def bfs_min_elevation():
    print("BFS min elevation")
    context = Context(strategies.StrategyBFS(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def bfs_max_elevation():
    print("BFS max elevation")
    context = Context(strategies.StrategyBFS(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def a_star_shortest_path():
    print("A star shortest path")
    context = Context(strategies.StrategyAStar(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def a_star_min_elevation():
    print("A star min elevation")
    context = Context(strategies.StrategyAStar(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def a_star_max_elevation():
    print("A star max elevation")
    context = Context(strategies.StrategyAStar(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def print_path(path):
    return_path = []
    return_nodes = []
    for node in path:
        return_nodes.append(node)
        # should be x and y
        lat = graph.nodes[node]["y"]
        lng = graph.nodes[node]["x"]
        return_path.append({'lat': lat, 'lng': lng})
    print(return_nodes)
    # print(return_path)
    return {"nodes": return_path}


def shortest_path():
    print("networkx shortest path")
    route = nx.shortest_path(graph, 0, 5, weight='length')
    print_path(route)
    return route


if __name__ == "__main__":
    load_graph()
    shortest_path()
    dijkstra_shortest_path()
    # dijkstra_min_elevation()
    # dijkstra_max_elevation()
    bfs_shortest_path()
    # bfs_min_elevation()
    # bfs_max_elevation()
    a_star_shortest_path()
    # a_star_min_elevation()
    # a_star_max_elevation()
