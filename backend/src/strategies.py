import heapq
import math
from backend.src.abstract_strategy import RoutingStrategy
from backend.src.priority_queue import PriorityQueue
import backend.src.graph_utils as graph_utils
import networkx as nx

# Used in Dijkstra
from itertools import count


class StrategyBFS(RoutingStrategy):
    def __init__(self, graph, limit, method):
        self.graph = graph
        self.limit = limit
        self.method = method

    def get_route(self, source, goal):
        if self.method == 'vanilla':
            return self.vanilla_shortest_path(source, goal)
        if self.method == 'min':
            return self.minimum_elevation(source, goal)
        else:
            return self.maximum_elevation(source, goal)

    def vanilla_shortest_path(self, start, goal, edge_weight='length'):
        graph = self.graph
        explored = []

        queue = [[start]]

        if start == goal:
            return [goal]

        # keeps looping until all possible paths have been checked
        while queue:
            path = queue.pop(0)
            node = path[-1]

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

    def maximum_elevation(self, source, goal, edge_weight='elevation_change'):
        # print("calling maximizing elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)

        max_path = []
        length_allowance = max_path_length - shortest_path_length
        for i in range(0, len(shortest_path) - 1):

            cur_node = shortest_path[i]
            next_node = shortest_path[i + 1]
            min_distance = graph[cur_node][next_node][0]['length']
            allowance = length_allowance * (min_distance / shortest_path_length)

            highest_elevation = -1
            best_path = []
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

    def minimum_elevation(self, source, goal, edge_weight='elevation_change'):
        # print("calling minimum elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length + shortest_path_length * self.limit

        least_elevation = self.vanilla_shortest_path(source, goal, edge_weight='elevation_change')
        least_elevation_length = graph_utils.get_path_length(graph, least_elevation)

        if least_elevation_length > max_path_length:
            length = len(least_elevation)
            for i in range(2, length):
                node = least_elevation[-i]
                path_length_to_node = graph_utils.get_path_length(graph, least_elevation[:-i + 1])
                node_to_goal_shortest = self.vanilla_shortest_path(node, goal)
                new_path_length = graph_utils.get_path_length(graph, node_to_goal_shortest)
                if path_length_to_node + new_path_length <= max_path_length:
                    return least_elevation[:-i] + node_to_goal_shortest
        else:
            return least_elevation


class StrategyDijkstra(RoutingStrategy):
    # Assume Limit is some percentage of the shortest path [0,1]
    def __init__(self, graph, limit, method):
        self.graph = graph
        self.limit = limit
        self.method = method

    def get_route(self, source, goal):
        if self.method == 'vanilla':
            return self.vanilla_shortest_path(source, goal)
        if self.method == 'min':
            return self.minimum_elevation(source, goal)
        else:
            return self.maximum_elevation(source, goal)

    def vanilla_shortest_path(self, source, goal, edge_weight='length'):
        # print("calling vanilla shortest path")
        graph = self.graph
        weight = weight_function(graph, edge_weight)
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
                if edge_weight == "elevation_change":
                    cost = max(0, weight(v, u, e))
                else:
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

    def maximum_elevation(self, source, goal, edge_weight='elevation_change'):
        # print("calling maximizing elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)

        max_path = []
        length_allowance = max_path_length - shortest_path_length
        for i in range(0, len(shortest_path) - 1):

            cur_node = shortest_path[i]
            next_node = shortest_path[i + 1]
            min_distance = graph[cur_node][next_node][0]['length']
            allowance = length_allowance * (min_distance / shortest_path_length)

            highest_elevation = -1
            best_path = []
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

    def minimum_elevation(self, source, goal, edge_weight='elevation_change'):
        # print("calling minimum elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length + shortest_path_length * self.limit

        least_elevation = self.vanilla_shortest_path(source, goal, edge_weight='elevation_change')
        least_elevation_length = graph_utils.get_path_length(graph, least_elevation)

        if least_elevation_length > max_path_length:
            length = len(least_elevation)
            for i in range(2, length):
                node = least_elevation[-i]
                path_length_to_node = graph_utils.get_path_length(graph, least_elevation[:-i + 1])
                node_to_goal_shortest = self.vanilla_shortest_path(node, goal)
                new_path_length = graph_utils.get_path_length(graph, node_to_goal_shortest)
                if path_length_to_node + new_path_length <= max_path_length:
                    return least_elevation[:-i] + node_to_goal_shortest
        else:
            return least_elevation


class StrategyAStar(RoutingStrategy):
    def __init__(self, graph, limit, method):
        self.graph = graph
        self.limit = limit
        self.method = method

    def get_route(self, source, goal):
        if self.method == 'vanilla':
            return self.vanilla_shortest_path(source, goal)
        if self.method == 'min':
            return self.minimum_elevation(source, goal)
        else:
            return self.maximum_elevation(source, goal)

    def vanilla_shortest_path(self, source, goal, edge_weight='length'):
        push = heapq.heappush
        pop = heapq.heappop

        graph = self.graph
        successor_graph = graph._succ if graph.is_directed() else graph._adj

        weight = weight_function(graph, edge_weight)
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

    def maximum_elevation(self, source, goal, edge_weight='elevation_change'):
        # print("calling maximizing elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length * (1 + self.limit)

        max_path = []
        length_allowance = max_path_length - shortest_path_length
        for i in range(0, len(shortest_path) - 1):

            cur_node = shortest_path[i]
            next_node = shortest_path[i + 1]
            min_distance = graph[cur_node][next_node][0]['length']
            allowance = length_allowance * (min_distance / shortest_path_length)

            highest_elevation = -1
            best_path = []
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

    def minimum_elevation(self, source, goal, edge_weight='elevation_change'):
        # print("calling minimum elevation")
        graph = self.graph

        shortest_path = self.vanilla_shortest_path(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length + shortest_path_length * self.limit

        least_elevation = self.vanilla_shortest_path(source, goal, edge_weight='elevation_change')
        least_elevation_length = graph_utils.get_path_length(graph, least_elevation)

        if least_elevation_length > max_path_length:
            length = len(least_elevation)
            for i in range(2, length):
                node = least_elevation[-i]
                path_length_to_node = graph_utils.get_path_length(graph, least_elevation[:-i + 1])
                node_to_goal_shortest = self.vanilla_shortest_path(node, goal)
                new_path_length = graph_utils.get_path_length(graph, node_to_goal_shortest)
                if path_length_to_node + new_path_length <= max_path_length:
                    return least_elevation[:-i] + node_to_goal_shortest
        else:
            return least_elevation

    def manhat(self, start, goal):
        amherst_graph = self.graph
        start_x, start_y = amherst_graph.nodes[start]['x'], amherst_graph.nodes[start]['y']
        end_x, end_y = amherst_graph.nodes[goal]['x'], amherst_graph.nodes[goal]['y']
        # return 0 # Dijkstra, essentially
        return ((end_x - start_x) ** 2 + (end_y - start_y) ** 2)**0.5


def weight_function(graph, weight='length'):
    if weight == 'length':
        def weight_(source, dest, edge_data):
            return min(attr.get(weight, 1) for attr in edge_data.values())
    elif weight =='elevation_change':
        def weight_(source, dest, edge_data):
            return max(0, min(attr.get(weight, 1) for attr in edge_data.values()))
    return weight_
