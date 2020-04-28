import pickle as pkl
import networkx as nx
import osmnx as ox
from time import time
from backend.src.context import Context
from backend.src import strategies
from backend.src import graph_utils


graph = None
limit = 5


def load_graph():
    """
        Loads in the test graph.

    """
    global graph
    with open("test_graph.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded test graph')


def load_mass_graph():
    """
            Loads in the Massachusetts graph.

    """
    global graph
    with open("../src/data/massachusetts_bike.pkl", 'rb') as infile:
        graph = pkl.load(infile)
        print('Loaded MASS graph')


def dijkstra_shortest_path(start_node, dest_node):
    """
            Test Dijkstra's shortest path in comparison to networkx's shortest_path.

            Parameters:
            -----------
            start_node: networkx Node
                The starting node.
            dest_node: networkx Node
                The ending node.

            Passing Criteria:
            --------
            Both path lengths must be the same.

        """
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
    """
                Test Dijkstra's min elevation path using elevation as the weight.

                Parameters:
                -----------
                start_node: networkx Node
                    The starting node.
                dest_node: networkx Node
                    The ending node.

                Passing Criteria:
                --------
                min_elevation path must have the smaller path length than the limit
                 and min_elevation is less than regular elevation.

    """
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


def dijkstra_max_elevation(start_node, dest_node):
    """
                Test Dijkstra's max elevation path using elevation as the weight.

                Parameters:
                -----------
                start_node: networkx Node
                    The starting node.
                dest_node: networkx Node
                    The ending node.

                Passing Criteria:
                --------
                max_elevation path must have the smaller path length than the limit
                 and max_elevation is greater than regular elevation.

            """
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


def dijkstra_min_elevation_grade(start_node, dest_node):
    """
                    Test Dijkstra's min elevation path using grade as the weight.

                    Parameters:
                    -----------
                    start_node: networkx Node
                        The starting node.
                    dest_node: networkx Node
                        The ending node.

                    Passing Criteria:
                    --------
                    min_elevation path must have the smaller path length than the limit
                     and grade is less than regular grade.

        """
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


def dijkstra_max_elevation_grade(start_node, dest_node):
    """
                    Test Dijkstra's max elevation path using grade as the weight.

                    Parameters:
                    -----------
                    start_node: networkx Node
                        The starting node.
                    dest_node: networkx Node
                        The ending node.

                    Passing Criteria:
                    --------
                    max_elevation path must have the smaller path length than the limit
                     and grade is greater than regular greater.

                """
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


def bfs_shortest_path(start_node, dest_node):
    """
                    Test BFS' shortest path compared to the networkx shortest_path

                    Parameters:
                    -----------
                    start_node: networkx Node
                        The starting node.
                    dest_node: networkx Node
                        The ending node.

                    Passing Criteria:
                    --------
                    Number of nodes in the BFS path is <= to the networkx path because BFS always returns the least
                     number of edges.

                """
    context = Context(strategies.StrategyBFS(graph, 0, 'vanilla'))
    path = context.run_strategy_route(start_node, dest_node)
    print("BFS shortest path", path)
    nx_shortest_path = shortest_path(start_node, dest_node)
    if len(path) <= len(nx_shortest_path):
        print("Test Passed")
    else:
        print("Test Failed")
    print("\n")


def a_star_shortest_path(start_node, dest_node):
    """
               Test AStar's shortest path in comparison to networkx's shortest_path.

               Parameters:
               -----------
               start_node: networkx Node
                   The starting node.
               dest_node: networkx Node
                   The ending node.

               Passing Criteria:
               --------
               Both path lengths must be the same.

           """
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
    """
                    Test AStar's min elevation path using elevation as the weight.

                    Parameters:
                    -----------
                    start_node: networkx Node
                        The starting node.
                    dest_node: networkx Node
                        The ending node.

                    Passing Criteria:
                    --------
                    min_elevation path must have the smaller path length than the limit
                     and min_elevation is less than regular elevation.

        """
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


def a_star_max_elevation(start_node, dest_node):
    """
                   Test AStar's max elevation path using elevation as the weight.

                   Parameters:
                   -----------
                   start_node: networkx Node
                       The starting node.
                   dest_node: networkx Node
                       The ending node.

                   Passing Criteria:
                   --------
                   max_elevation path must have the smaller path length than the limit
                    and max_elevation is greater than regular elevation.

               """
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


def a_star_min_elevation_grade(start_node, dest_node):
    """
                        Test AStar's min elevation path using grade as the weight.

                        Parameters:
                        -----------
                        start_node: networkx Node
                            The starting node.
                        dest_node: networkx Node
                            The ending node.

                        Passing Criteria:
                        --------
                        min_elevation path must have the smaller path length than the limit
                         and grade is less than regular grade.

            """
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


def a_star_max_elevation_grade(start_node, dest_node):
    """
                        Test AStar's min elevation path using grade as the weight.

                        Parameters:
                        -----------
                        start_node: networkx Node
                            The starting node.
                        dest_node: networkx Node
                            The ending node.

                        Passing Criteria:
                        --------
                        max_elevation path must have the smaller path length than the limit
                         and grade is less than regular grade.

            """
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


def shortest_path(start_node, dest_node):
    """
                        Get the shortest path route from Networkx's Dijkstra.

                        Parameters:
                        -----------
                        start_node: networkx Node
                            The starting node.
                        dest_node: networkx Node
                            The ending node.

                        Returns:
                        --------
                        route: The array of Nodes that represents the shortest path.

            """
    route = nx.shortest_path(graph, start_node, dest_node, weight='length')
    print("networkx shortest path", route)
    return route


# Run all shortest path functions: BFS, Dijkstra's, A*
def all_shortest_path(start, dest):
    """
                Run all the shortest path algorithms: BFS, Dijkstra, A*

                Parameters:
                -----------
                start: String
                    The starting address.
                dest: String
                    The ending address.

                Returns:
                --------
                times: An array of the time (as float values) it took each algorithm to run.

                """
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
    """
                    Run a performance test on the minimum elevation path of Dijkstra and A*.

                    Parameters:
                    -----------
                    start: String
                        The starting address.
                    dest: String
                        The ending address.
                    method: String
                        The method to use: Minimize Elevation Gain or Minimize Steepness.

                    Returns:
                    --------
                    times: An array of the time (as float values) it took each algorithm to run.

                    """
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


def max_elevation_path_performance(start, dest, method):
    """
                        Run a performance test on the maximum elevation path of Dijkstra and A*.

                        Parameters:
                        -----------
                        start: String
                            The starting address.
                        dest: String
                            The ending address.
                        method: String
                            The method to use: Maximize Elevation Gain or Maximize Steepness.

                        Returns:
                        --------
                        times: An array of the time (as float values) it took each algorithm to run.

                        """
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


def shortest_path_performance():
    """
        Run the shortest paths for a given set of locations.
    """
    start_locations = ['Harvard University', 'University of Massachusetts Amherst',
                       'Massachusetts Institute of Technology']
    end_locations = ['TD Garden', 'Amherst College', 'Boston Public Market']
    for i in range(3):
        runtimes = all_shortest_path(start_locations[i], end_locations[i])
        print(runtimes)


def min_elevation_performance(method='min elevation_change'):
    """
           Run the minimum elevation for a given set of locations.
    """
    start_locations = ['Harvard University', 'University of Massachusetts Amherst',
                       'Massachusetts Institute of Technology']
    end_locations = ['TD Garden', 'Amherst College', 'Boston Public Market']
    for i in range(3):
        runtimes = min_elevation_path_performance(start_locations[i], end_locations[i], method)
        print(runtimes)


def max_elevation_performance(method='max elevation_change'):
    """
           Run the maximum elevation for a given set of locations.
    """
    start_locations = ['Harvard University', 'University of Massachusetts Amherst',
                       'Massachusetts Institute of Technology']
    end_locations = ['TD Garden', 'Amherst College', 'Boston Public Market']
    for i in range(3):
        runtimes = max_elevation_path_performance(start_locations[i], end_locations[i], method)
        print(runtimes)


def performance_metrics():
    """
           Run performance experiments on all algorithms and combinations.
    """
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


def get_node_from_address(graph, address):
    """
                Converts a string address to the closest node on a graph.

                Parameters:
                -----------
                graph: networkx Graph
                    The graph to perform the look up.
                address: String
                    The address to convert to a node.

                Returns:
                --------
                    node: The closest node to the address given.
    """
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

