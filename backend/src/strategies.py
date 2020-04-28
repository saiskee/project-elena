import heapq
from abstract_strategy import RoutingStrategy
import graph_utils
import networkx as nx
from itertools import count


class StrategyBFS(RoutingStrategy):
    """
    A class used to represent a BFS path finding strategy

    ...

    Attributes
    ----------
    graph : nx.multidigraph
       a formatted string to print out what the animal says
    limit : int
       the multiply factor on the path length
    method : str
       the type of shortest path algorithm to run

    Methods
    -------
    get_route(source, goal)
       calls the appropriate routing algorithm
    vanilla_shortest_path(start, goal, edge_weight)
       calculate the shortest path
    """
    def __init__(self, graph, limit, method):
        super().__init__(graph, limit, method)

    def get_route(self, source, goal):
        """Gets the route that is set by the "method" parameter.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path

        Returns
        ------
        list of nodes that form the discovered path
        """

        return self.vanilla_shortest_path(source, goal)

    def vanilla_shortest_path(self, source, goal, edge_weight='length'):
        """Gets the shortest path given by BFS algorithm.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path
        edge_weight : string, optional
            defaults to 'length'

        Returns
        ------
        list of nodes that form the discovered path
        """
        graph = self.graph
        explored = []

        # start the BFS queue
        queue = [[source]]

        # return if start node is the end node
        if source == goal:
            return [goal]

        # keeps looping until all possible paths have been checked
        while queue:
            path = queue.pop(0)
            node = path[-1]
            # add neighboring nodes if they haven't been explored
            if node not in explored:
                neighbors = graph.neighbors(node)
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    if neighbor == goal:
                        return new_path
                explored.append(node)
        # Return empty list if path doesn't exist
        return []


class StrategyDijkstra(RoutingStrategy):
    """
    A class used to represent a BFS path finding strategy

    ...

    Attributes
    ----------
    graph : nx.multidigraph
       a formatted string to print out what the animal says
    limit : int
       the multiply factor on the path length
    method : str
       the type of shortest path algorithm to run

    Methods
    -------
    get_route(source, goal)
       calls the appropriate routing algorithm
    vanilla_shortest_path(start, goal, edge_weight)
       calculate the shortest path
    maximum_elevation(start, goal)
       calculate the shortest path while maximizing elevation
    minimum_elevation(start, goal, weight)
       calculate the shortest path while minimizing elevation
    """
    # Assume Limit is some percentage of the shortest path [0,1]
    def __init__(self, graph, limit, method):
        super().__init__(graph, limit, method)

    def get_route(self, source, goal):
        """Gets the route that is set by the "method" parameter.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path

        Returns
        ------
        list of nodes that form the discovered path
        """

        if self.method == 'vanilla':
            return self.vanilla_shortest_path(source, goal)
        elif self.method.startswith('min'):
            weight = self.method.split()[1]
            return self.minimum_elevation(source, goal, weight)
        elif self.method.startswith('max'):
            return self.maximum_elevation(source, goal)

    def vanilla_shortest_path(self, source, goal, edge_weight='length'):
        """Gets the shortest path given by Dijkstra's algorithm.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path
        edge_weight : string, optional
            defaults to 'length'

        Returns
        ------
        list of nodes that form the discovered path
        """
        # print("calling vanilla shortest path")
        graph = self.graph
        weight = graph_utils.weight_function(graph, edge_weight)
        paths = {source: [source]}
        successor_graph = graph._succ if graph.is_directed() else graph._adj

        push = heapq.heappush
        pop = heapq.heappop
        dist = {}  # Dictionary of Final distances
        seen = {}
        c = count()
        queue = []

        if source not in graph:
            return []  # Figure out way to handle exceptions properly
        seen[source] = 0
        push(queue, (0, next(c), source))
        while queue:
            d, _, v = pop(queue)
            if v in dist:
                continue  # already searched this node
            dist[v] = d
            if v == goal:
                break
            for u, e in successor_graph[v].items():
                cost = weight(v, u, e) + 1
                if cost is None:
                    continue

                vu_dist = dist[v] + cost
                if u in dist:
                    if vu_dist < dist[u]:
                        pass  # Contradictory paths found, negative weights?
                elif u not in seen or vu_dist < seen[u]:
                    seen[u] = vu_dist
                    push(queue, (vu_dist, next(c), u))
                    paths[u] = paths[v] + [u]
        return paths[goal]

    def maximum_elevation(self, source, goal):
        """Gets the shortest path within a path length limit, optimizing for maximum elevation.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path

        Returns
        ------
        list of nodes that form the discovered path
        """

        # print("calling maximizing elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)
        max_path = []
        length_allowance = max_path_length - shortest_path_length
        if length_allowance < 15:
            return shortest_path

        # Iterate through each pair of nodes and find a subpath that can maximize elevation within a path
        # length constraint
        for i in range(0, len(shortest_path) - 1):
            cur_node = shortest_path[i]
            next_node = shortest_path[i + 1]
            min_distance = graph[cur_node][next_node][0]['length']
            allowance = length_allowance * (min_distance / shortest_path_length)
            highest_elevation = -1
            best_path = []

            # find all paths from cur_node to next_node and get the path length and elevation, add to original path
            for path in nx.all_simple_paths(graph, cur_node, next_node, cutoff=5):
                path_elevation = graph_utils.get_path_elevation(graph, path)
                path_length = graph_utils.get_path_length(graph, path)

                if path_elevation > highest_elevation:
                    if path_length <= allowance + min_distance:
                        highest_elevation = path_elevation
                        best_path = path

            best_path_length = graph_utils.get_path_length(graph, best_path)
            length_allowance -= (best_path_length - min_distance)

            for j in best_path[:-1]:
                max_path.append(j)
        max_path.append(goal)
        return max_path

    def minimum_elevation(self, source, goal, weight):
        """Gets the shortest path within a path length limit, optimizing for minimum elevation.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path
        weight : string
            type of weight to use
        Returns
        ------
        list of nodes that form the discovered path
        """

        # print("calling minimum elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)
        if (self.limit < 0.05):
            return shortest_path
        # calculate the smallest elevation path using elevation/grade
        least_elevation = self.vanilla_shortest_path(source, goal, edge_weight=weight)
        least_elevation_length = graph_utils.get_path_length(graph, least_elevation)

        # if the path with smallest elevation is longer than the maximum allowed path, go through each node
        # and find the shortest path from the end to the beginning, thereby optimizing for elevation and path length
        if least_elevation_length > max_path_length:
            length = len(least_elevation)
            for i in range(2, length+1):
                node = least_elevation[-i]
                path_length_to_node = graph_utils.get_path_length(graph, least_elevation[:-i + 1])
                node_to_goal_shortest = self.vanilla_shortest_path(node, goal)
                new_path_length = graph_utils.get_path_length(graph, node_to_goal_shortest)
                if path_length_to_node + new_path_length <= max_path_length:
                    return least_elevation[:-i] + node_to_goal_shortest
        else:
            return least_elevation


class StrategyAStar(RoutingStrategy):
    """
    A class used to represent a BFS path finding strategy

    ...

    Attributes
    ----------
    graph : nx.multidigraph
       a formatted string to print out what the animal says
    limit : int
       the multiply factor on the path length
    method : str
       the type of shortest path algorithm to run

    Methods
    -------
    get_route(source, goal)
       calls the appropriate routing algorithm
    vanilla_shortest_path(start, goal, edge_weight)
       calculate the shortest path
    maximum_elevation(start, goal)
       calculate the shortest path while maximizing elevation
    minimum_elevation(start, goal, weight)
       calculate the shortest path while minimizing elevation
    """
    def __init__(self, graph, limit, method):
        super().__init__(graph, limit, method)

    def get_route(self, source, goal):
        """Gets the route that is set by the "method" parameter.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path

        Returns
        ------
        list of nodes that form the discovered path
        """

        if self.method == 'vanilla':
            return self.vanilla_shortest_path(source, goal)
        elif self.method.startswith('min'):
            weight = self.method.split()[1]
            return self.minimum_elevation(source, goal, weight)
        elif self.method.startswith('max'):
            return self.maximum_elevation(source, goal)

    def vanilla_shortest_path(self, source, goal, edge_weight='length'):
        """Gets the shortest path given by A* algorithm.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path
        edge_weight : string, optional
            defaults to 'length'

        Returns
        ------
        list of nodes that form the discovered path
        """
        push = heapq.heappush
        pop = heapq.heappop

        graph = self.graph
        successor_graph = graph._succ if graph.is_directed() else graph._adj

        weight = graph_utils.weight_function(graph, edge_weight)
        c = count()
        queue = [(0, next(c), source, 0, None)]

        enqueued = {}
        explored = {}

        while queue:
            _, __, curnode, dist, parent = pop(queue)

            if curnode == goal:
                path = [curnode]
                node = parent
                while node is not None:
                    path.append(node)
                    node = explored[node]
                path.reverse()
                return path

            if curnode in explored:
                if explored[curnode] is None:
                    continue

                qcost, h = enqueued[curnode]
                if qcost < dist:
                    continue

            explored[curnode] = parent

            for neighbor, w in successor_graph[curnode].items():
                ncost = dist + weight(curnode, neighbor, w)
                if neighbor in enqueued:
                    qcost, h = enqueued[neighbor]
                    if qcost <= ncost:
                        continue
                else:
                    h = self.manhat(neighbor, goal)
                enqueued[neighbor] = ncost, h
                push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    def maximum_elevation(self, source, goal):
        """Gets the shortest path within a path length limit, optimizing for maximum elevation.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path

        Returns
        ------
        list of nodes that form the discovered path
        """

        # print("calling maximizing elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)
        if (self.limit < 0.05):
            return shortest_path
        max_path = []
        length_allowance = max_path_length - shortest_path_length

        # Iterate through each pair of nodes and find a subpath that can maximize elevation within a path
        # length constraint
        for i in range(0, len(shortest_path) - 1):
            cur_node = shortest_path[i]
            next_node = shortest_path[i + 1]
            min_distance = graph[cur_node][next_node][0]['length']
            allowance = length_allowance * (min_distance / shortest_path_length)
            highest_elevation = -1
            best_path = []

            # find all paths from cur_node to next_node and get the path length and elevation, add to original path
            for path in nx.all_simple_paths(graph, cur_node, next_node, cutoff=5):
                path_elevation = graph_utils.get_path_elevation(graph, path)
                path_length = graph_utils.get_path_length(graph, path)

                if path_elevation > highest_elevation:
                    if path_length <= allowance + min_distance:
                        highest_elevation = path_elevation
                        best_path = path

            best_path_length = graph_utils.get_path_length(graph, best_path)
            length_allowance -= (best_path_length - min_distance)

            for j in best_path[:-1]:
                max_path.append(j)
        max_path.append(goal)
        return max_path

    def minimum_elevation(self, source, goal, weight):
        """Gets the shortest path within a path length limit, optimizing for minimum elevation.

        Parameters
        ----------
        source : node
            starting point node for the path
        goal : node
            destination node for the path
        weight : string
            type of weight to use
        Returns
        ------
        list of nodes that form the discovered path
        """

        # print("calling minimum elevation")
        graph = self.graph
        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)
        if (self.limit < 0.05):
            return shortest_path

        # Find the least elevation path using A* and elevation/grade as the edge weight
        least_elevation = self.vanilla_shortest_path(source, goal, edge_weight=weight)
        least_elevation_length = graph_utils.get_path_length(graph, least_elevation)

        # if the path with smallest elevation is longer than the maximum allowed path, go through each node
        # and find the shortest path from the end to the beginning, thereby optimizing for elevation and path length
        if least_elevation_length > max_path_length:
            length = len(least_elevation)
            for i in range(2, length+1):
                node = least_elevation[-i]
                path_length_to_node = graph_utils.get_path_length(graph, least_elevation[:-i + 1])
                node_to_goal_shortest = self.vanilla_shortest_path(node, goal)
                new_path_length = graph_utils.get_path_length(graph, node_to_goal_shortest)
                if path_length_to_node + new_path_length <= max_path_length:
                    return least_elevation[:-i] + node_to_goal_shortest
        else:
            return least_elevation

    def manhat(self, start, goal):
        """Calculates the manhattan distance between two nodes.

        Parameters
        ----------
        start : node
            starting point node for the path
        goal : node
            destination node for the path

        Returns
        ------
        manhattan distance, int
        """

        amherst_graph = self.graph
        start_x, start_y = amherst_graph.nodes[start]['x'], amherst_graph.nodes[start]['y']
        end_x, end_y = amherst_graph.nodes[goal]['x'], amherst_graph.nodes[goal]['y']
        # return 0 # Dijkstra, essentially
        return ((end_x - start_x) ** 2 + (end_y - start_y) ** 2)**0.5
