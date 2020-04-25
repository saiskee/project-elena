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
    print("Calling get_route")
    context = Context(strategies.StrategyDijkstra(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def dijkstra_min_elevation():
    print("Calling get_route")
    context = Context(strategies.StrategyDijkstra(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def dijkstra_max_elevation():
    print("Calling get_route")
    context = Context(strategies.StrategyDijkstra(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def bfs_shortest_path():
    print("Calling get_route")
    context = Context(strategies.StrategyBFS(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def bfs_min_elevation():
    print("Calling get_route")
    context = Context(strategies.StrategyBFS(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def bfs_max_elevation():
    print("Calling get_route")
    context = Context(strategies.StrategyBFS(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def a_star_shortest_path():
    print("Calling get_route")
    context = Context(strategies.StrategyAStar(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def a_star_min_elevation():
    print("Calling get_route")
    context = Context(strategies.StrategyAStar(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def a_star_max_elevation():
    print("Calling get_route")
    context = Context(strategies.StrategyAStar(graph))
    path = context.run_strategy_route(0, 5)
    print_path(path)
    pass


def print_path(path):
    return_path = []
    for node in path:
        print(node)
        print(graph.nodes[node])
        # should be x and y
        lat = graph.nodes[node]["y"]
        lng = graph.nodes[node]["x"]
        return_path.append({'lat': lat, 'lng': lng})
    print(return_path)
    return {"nodes": return_path}


def shortest_path():
    route = nx.shortest_path(graph, 0, 5, weight='length')
    print_path(route)
    return route


if __name__ == "__main__":
    load_graph()
    shortest_path()
    # dijkstra_shortest_path()
    # dijkstra_min_elevation()
    # dijkstra_max_elevation()
    # bfs_shortest_path()
    # bfs_min_elevation()
    # bfs_max_elevation()
    # a_star_shortest_path()
    # a_star_min_elevation()
    # a_star_max_elevation()
