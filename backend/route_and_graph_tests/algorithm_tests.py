import pickle as pkl
import networkx as nx
from backend.src.context import Context
from backend.src import strategies
from backend.src import graph_utils

graph = None
limit = 50


def load_graph():
    global graph
    with open("test_graph.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded test graph')


def dijkstra_shortest_path(start_node, dest_node):
    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    regular_path_length = graph_utils.get_path_length(graph, path)
    print("Dijkstra shortest path", path)
    nx_shortest_path = shortest_path(start_node, dest_node)
    nx_shortest_path_length = graph_utils.get_path_length(graph, nx_shortest_path)
    if nx_shortest_path_length == regular_path_length:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def dijkstra_min_elevation(start_node, dest_node):
    print("Dijkstra min elevation")
    context = Context(strategies.StrategyDijkstra(graph, limit, 'min elevation_change'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    elevation = graph_utils.get_path_elevation(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Elevation:", regular_elevation, "\nNew Elevation:", elevation)
    if max_path_length <= max_length and elevation <= regular_elevation:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def dijkstra_max_elevation(start_node, dest_node):
    print("Dijkstra max elevation")
    context = Context(strategies.StrategyDijkstra(graph, limit, 'max elevation_change'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    elevation = graph_utils.get_path_elevation(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Elevation:", regular_elevation, "\nNew Elevation:", elevation)
    if max_path_length <= max_length and elevation >= regular_elevation:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def bfs_shortest_path(start_node, dest_node):
    context = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("BFS shortest path", path)
    nx_shortest_path = shortest_path(start_node, dest_node)
    if len(path) <= len(nx_shortest_path):
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def bfs_min_elevation(start_node, dest_node):
    print("BFS min elevation")
    context_min = Context(strategies.StrategyBFS(graph, limit, 'min elevation_change'))
    path = context_min.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    elevation = graph_utils.get_path_elevation(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    regular = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    path = regular.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Elevation:", regular_elevation, "\nNew Elevation:", elevation)
    if max_path_length <= max_length and elevation <= regular_elevation:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def bfs_max_elevation(start_node, dest_node):
    print("BFS max elevation")
    context = Context(strategies.StrategyBFS(graph, limit, 'max elevation_change'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    elevation = graph_utils.get_path_elevation(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Elevation:", regular_elevation, "\nNew Elevation:", elevation)
    if max_path_length <= max_length and elevation >= regular_elevation:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def a_star_shortest_path(start_node, dest_node):
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("A star shortest path", path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    nx_shortest_path = shortest_path(start_node, dest_node)
    nx_shortest_path_length = graph_utils.get_path_length(graph, nx_shortest_path)
    if nx_shortest_path_length == regular_path_length:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def a_star_min_elevation(start_node, dest_node):
    print("A star min elevation")
    context = Context(strategies.StrategyAStar(graph, limit, 'min elevation_change'))
    path = context.run_strategy_route(start_node, dest_node)
    print("min path", path)
    elevation = graph_utils.get_path_elevation(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("vanilla path", path)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Elevation:", regular_elevation, "\nNew Elevation:", elevation)
    if max_path_length <= max_length and elevation <= regular_elevation:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def a_star_max_elevation(start_node, dest_node):
    print("A star max elevation")
    context = Context(strategies.StrategyAStar(graph, limit, 'max elevation_change'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    elevation = graph_utils.get_path_elevation(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_elevation = graph_utils.get_path_elevation(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Elevation:", regular_elevation, "\nNew Elevation:", elevation)
    if max_path_length <= max_length and elevation >= regular_elevation:
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def shortest_path(start_node, dest_node):
    route = nx.shortest_path(graph, start_node, dest_node, weight='length')
    print("networkx shortest path", route)
    return route


if __name__ == "__main__":
    load_graph()
    dijkstra_shortest_path(0, 10)
    dijkstra_min_elevation(0, 10)
    dijkstra_max_elevation(0, 10)
    bfs_shortest_path(0, 10)
    bfs_min_elevation(0, 10)
    bfs_max_elevation(0, 10)
    a_star_shortest_path(0, 10)
    a_star_min_elevation(0, 10)
    a_star_max_elevation(0, 10)
