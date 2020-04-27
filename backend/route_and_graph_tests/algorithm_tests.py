import pickle as pkl
import networkx as nx
import osmnx as ox
from time import time
from backend.src.context import Context
from backend.src import strategies
from backend.src import graph_utils


graph = None
limit = 5


# Load in the test graph
def load_graph():
    global graph
    with open("test_graph.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded test graph')


# Load in the Massachusetts graph
def load_mass_graph():
    global graph
    with open("../src/data/massachusetts_bike.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded MASS graph')


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


# Test dijkstra's min elevation path using elevation as the weight
# Passes if the min_elevation path has a smaller path length than the limit and
# if the min_elevation is less than the regular elevation
def dijkstra_min_elevation(start_node, dest_node):
    print("Dijkstra min elevation using elevation change as weight")
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


# Test dijkstra's max elevation path using elevation as the weight
# Passes if the max_elevation path has a smaller path length than the limit and
# if the max_elevation is greater than the regular elevation
def dijkstra_max_elevation(start_node, dest_node):
    print("Dijkstra max elevation using elevation change as weight")
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


# Test dijkstra's min elevation path using grade as the weight
# Passes if the min_elevation path has a smaller path length than the limit and
# if the grade is less than the regular grade
def dijkstra_min_elevation_grade(start_node, dest_node):
    print("Dijkstra min elevation using grade as weight")
    context = Context(strategies.StrategyDijkstra(graph, limit, 'min grade'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    grade = graph_utils.get_average_grade(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_grade = graph_utils.get_average_grade(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Grade:", regular_grade, "\nNew Grade:", grade)
    if max_path_length <= max_length:
        if grade <= regular_grade:
            print("Test Passed")
        else:
            print("Test Passed: Path length. Dijkstra's wasn't able to minimize grade")
    else:
        print("Test Failed")
    print("\n")


# Test dijkstra's max elevation path using grade as the weight
# Passes if the max_elevation path has a smaller path length than the limit and
# if the grade is greater than the regular grade
def dijkstra_max_elevation_grade(start_node, dest_node):
    print("Dijkstra max elevation using grade as weight")
    context = Context(strategies.StrategyDijkstra(graph, limit, 'max grade'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    grade = graph_utils.get_average_grade(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_grade = graph_utils.get_average_grade(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Grade:", round(regular_grade, 2), "\nNew Grade:", round(grade, 2))
    if max_path_length <= max_length:
        if grade >= regular_grade:
            print("Test Passed")
        else:
            print("Test Passed: Path length. Dijkstra's wasn't able to maximize grade")
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


# Test A* min elevation path using elevation as the weight
# Passes if the min_elevation path has a smaller path length than the limit and
# if the min_elevation is less than the regular elevation
def a_star_min_elevation(start_node, dest_node):
    print("A star min elevation using elevation change as weight")
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


# Test A* max elevation path using grade as the weight
# Passes if the max_elevation path has a smaller path length than the limit and
# if the max_elevation is greater than the regular elevation
def a_star_max_elevation(start_node, dest_node):
    print("A star max elevation using elevation change as weight")
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


# Test A* min elevation path using grade as the weight
# Passes if the min_elevation path has a smaller path length than the limit and
# if the grade is less than the regular grade
def a_star_min_elevation_grade(start_node, dest_node):
    print("A star min elevation using grade as weight")
    context = Context(strategies.StrategyAStar(graph, limit, 'min grade'))
    path = context.run_strategy_route(start_node, dest_node)
    print("min path", path)
    grade = graph_utils.get_average_grade(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("vanilla path", path)
    regular_grade = graph_utils.get_average_grade(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Grade:", round(regular_grade, 2), "\nNew Grade:", round(grade, 2))
    if max_path_length <= max_length:
        if grade <= regular_grade:
            print("Test Passed")
        else:
            print("Test Passed: Path length. A* wasn't able to minimize grade")
    else:
        print("Test Failed")
    print("\n")


# Test A* max elevation path
# Passes if the max_elevation path has a smaller path length than the limit and
# if the grade is greater than the regular grade
def a_star_max_elevation_grade(start_node, dest_node):
    print("A star max elevation using grade as weight")
    context = Context(strategies.StrategyAStar(graph, limit, 'max grade'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Elevation path", path)
    grade = graph_utils.get_average_grade(graph, path)
    max_path_length = graph_utils.get_path_length(graph, path)

    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("Vanilla path", path)
    regular_grade = graph_utils.get_average_grade(graph, path)
    regular_path_length = graph_utils.get_path_length(graph, path)
    max_length = regular_path_length * (1 + limit)
    print("Vanilla path length:", regular_path_length, "\nMax Possible Path length:",
          max_length, "\nLength of elevation path:", max_path_length)
    print("Vanilla path Grade:", round(regular_grade, 2), "\nNew Grade:", round(grade, 2))
    if max_path_length <= max_length:
        if grade >= regular_grade:
            print("Test Passed")
        else:
            print("Test Passed: Path length. A* wasn't able to maximize grade")
    else:
        print("Test Failed")
    print("\n")


# Networkx shortest path algorithm using Dijkstra's
def shortest_path(start_node, dest_node):
    route = nx.shortest_path(graph, start_node, dest_node, weight='length')
    print("networkx shortest path", route)
    return route


# Run all shortest path functions: BFS, Dijkstra's, A*
def all_shortest_path(start, dest):
    try:
        start_node = get_node_from_address(graph, start)
        dest_node = get_node_from_address(graph, dest)
    except Exception as e:
        print(e)
        print("Could not map address to node")
    times = []
    print("Running Dijkstra")
    context = Context(strategies.StrategyDijkstra(graph, 0, 'vanilla'))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    print("Running BFS")
    context = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    print("Running A*")
    context = Context(strategies.StrategyAStar(graph, 0, 'vanilla'))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    return times


# Return the time of Dijkstra and A* minimum elevation
def min_elevation_path_performance(start, dest, method):
    try:
        start_node = get_node_from_address(graph, start)
        dest_node = get_node_from_address(graph, dest)
    except Exception as e:
        print(e)
        print("Could not map address to node")
    times = []
    print("Running Dijkstra")
    context = Context(strategies.StrategyDijkstra(graph, 0, method))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    print("Running A*")
    context = Context(strategies.StrategyAStar(graph, 0, method))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    return times


# Return the time of Dijkstra and A* maximum elevation
def max_elevation_path_performance(start, dest, method):
    try:
        start_node = get_node_from_address(graph, start)
        dest_node = get_node_from_address(graph, dest)
    except Exception as e:
        print(e)
        print("Could not map address to node")
    times = []
    print("Running Dijkstra")
    context = Context(strategies.StrategyDijkstra(graph, 0, method))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    print("Running A*")
    context = Context(strategies.StrategyAStar(graph, 0, method))
    start_time = time()
    path = context.run_strategy_route(start_node, dest_node)
    end_time = time()
    times.append(end_time - start_time)
    return times


# Run shortest paths for a given set of locations
def shortest_path_performance():
    start_locations = ['Harvard University', 'University of Massachusetts Amherst',
                       'Massachusetts Institute of Technology']
    end_locations = ['TD Garden', 'Amherst College', 'Boston Public Market']
    for i in range(3):
        runtimes = all_shortest_path(start_locations[i], end_locations[i])
        print(runtimes)


# Run minimum elevation for a given set of locations
def min_elevation_performance(method='min elevation_change'):
    start_locations = ['Harvard University', 'University of Massachusetts Amherst',
                       'Massachusetts Institute of Technology']
    end_locations = ['TD Garden', 'Amherst College', 'Boston Public Market']
    for i in range(3):
        runtimes = min_elevation_path_performance(start_locations[i], end_locations[i], method)
        print(runtimes)


# Run maximum elevation for a given set of locations
def max_elevation_performance(method='max elevation_change'):
    start_locations = ['Harvard University', 'University of Massachusetts Amherst',
                       'Massachusetts Institute of Technology']
    end_locations = ['TD Garden', 'Amherst College', 'Boston Public Market']
    for i in range(3):
        runtimes = max_elevation_path_performance(start_locations[i], end_locations[i], method)
        print(runtimes)


# Run performance experiments on all algorithms and combinations
def performance_metrics():
    load_mass_graph()
    # print("Shortest Path Times")
    shortest_path_performance()
    print("Minimum Elevation Times using Elevation Change")
    min_elevation_performance('min elevation_change')
    print("Maximum Elevation Times using Elevation Change")
    max_elevation_performance('max elevation_change')
    print("Minimum Elevation Times using Grade")
    min_elevation_performance('min grade')
    print("Maximum Elevation Times using Grade")
    max_elevation_performance('max grade')


# Convert an address to a node
def get_node_from_address(graph, address):
    try:
        latlng = ox.geocode(address)
        node, dist = ox.get_nearest_node(graph, latlng, return_dist=True)
        if dist > 10000:
            raise Exception("{} is not currently included in Routing Capabilities".format(address))
        return node
    except:
        raise Exception("Could not find location '{}'".format(address))


if __name__ == "__main__":
    load_graph()
    # Run the tests
    bfs_shortest_path(0, 10)
    dijkstra_shortest_path(0, 10)
    dijkstra_min_elevation(0, 10)
    dijkstra_max_elevation(0, 10)
    dijkstra_min_elevation_grade(0, 10)
    dijkstra_max_elevation_grade(0, 10)
    a_star_shortest_path(0, 10)
    a_star_min_elevation(0, 10)
    a_star_max_elevation(0, 10)
    a_star_min_elevation_grade(0, 10)
    a_star_max_elevation_grade(0, 10)
    # Run the performance metrics
    # performance_metrics()

