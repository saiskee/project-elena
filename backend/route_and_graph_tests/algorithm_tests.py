import pickle as pkl
import networkx as nx
from backend.src.context import Context
from backend.src import strategies
from backend.src import graph_utils

graph = None


def load_graph():
    global graph
    with open("test_graph.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded test graph')


def dijkstra_shortest_path(start_node, dest_node):
    print("Dijkstra shortest path")
    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    pass


def dijkstra_min_elevation(start_node, dest_node):
    print("Dijkstra min elevation")
    context = Context(strategies.StrategyDijkstra(graph, 50, 'min'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    min_elevation = graph_utils.get_path_elevation(graph, path)
    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    print(min_elevation, regular_elevation)
    assert (min_elevation <= regular_elevation)
    pass


def dijkstra_max_elevation(start_node, dest_node):
    print("Dijkstra max elevation")
    context = Context(strategies.StrategyDijkstra(graph, 50, 'max'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    max_elevation = graph_utils.get_path_elevation(graph, path)
    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    print(max_elevation, regular_elevation)
    assert(max_elevation >= regular_elevation)


def bfs_shortest_path(start_node, dest_node):
    print("BFS shortest path")
    context = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    pass


def bfs_min_elevation(start_node, dest_node):
    print("BFS min elevation")
    context_min = Context(strategies.StrategyBFS(graph, 50, 'min'))
    path = context_min.run_strategy_route(start_node, dest_node)
    print_path(path)
    min_elevation = graph_utils.get_path_elevation(graph, path)
    regular = Context(strategies.StrategyBFS(graph, 50, 'vanilla'))
    path = regular.run_strategy_route(start_node, dest_node)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    print(min_elevation, regular_elevation)
    assert (min_elevation <= regular_elevation)
    pass


def bfs_max_elevation(start_node, dest_node):
    print("BFS max elevation")
    context = Context(strategies.StrategyBFS(graph, 50, 'max'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    max_elevation = graph_utils.get_path_elevation(graph, path)
    context = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    assert (max_elevation >= regular_elevation)
    pass


def a_star_shortest_path(start_node, dest_node):
    print("A star shortest path")
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    pass


def a_star_min_elevation(start_node, dest_node):
    print("A star min elevation")
    context = Context(strategies.StrategyAStar(graph, 50, 'min'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    min_elevation = graph_utils.get_path_elevation(graph, path)
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    print(min_elevation, regular_elevation)
    assert (min_elevation <= regular_elevation)
    pass


def a_star_max_elevation(start_node, dest_node):
    print("A star max elevation")
    context = Context(strategies.StrategyAStar(graph, 0, 'max'))
    path = context.run_strategy_route(start_node, dest_node)
    print_path(path)
    max_elevation = graph_utils.get_path_elevation(graph, path)
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    print(max_elevation, regular_elevation)
    assert (max_elevation >= regular_elevation)
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


def shortest_path(start_node, dest_node):
    print("networkx shortest path")
    route = nx.shortest_path(graph, start_node, dest_node, weight='length')
    print_path(route)
    return route


if __name__ == "__main__":
    load_graph()
    shortest_path(0, 10)
    # dijkstra_shortest_path(0, 10)
    # dijkstra_min_elevation(0, 10)
    # dijkstra_max_elevation(0, 10)
    # bfs_shortest_path(0, 10)
    # bfs_min_elevation(0, 10)
    # bfs_max_elevation(0, 10)
    # a_star_shortest_path(0, 10)
    a_star_min_elevation(0, 10)
    a_star_max_elevation(0, 10)
