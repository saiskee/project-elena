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


# Test dijkstra's shortest path and compare to networkx shortest_path
# Passes if the path lengths are the same
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


# Test dijkstra's min elevation path
# Passes if the min_elevation path has a smaller path length than the limit and
# if the min_elevation is less than the regular elevation
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


# Test dijkstra's max elevation path
# Passes if the max_elevation path has a smaller path length than the limit and
# if the max_elevation is greater than the regular elevation
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


# Test BFS's shortest path and compare to networkx shortest_path
# Passes if number of nodes in the BFS path is <= to the networkx path because BFS always returns the least
# number of edges
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


# Test dijkstra's shortest path and compare to networkx shortest_path
# Passes if the path lengths are the same
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


# Test A* min elevation path
# Passes if the min_elevation path has a smaller path length than the limit and
# if the min_elevation is less than the regular elevation
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


# Test A* max elevation path
# Passes if the max_elevation path has a smaller path length than the limit and
# if the max_elevation is greater than the regular elevation
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


# Networkx shortest path algorithm using Dijkstra's
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
    a_star_shortest_path(0, 10)
    a_star_min_elevation(0, 10)
    a_star_max_elevation(0, 10)
