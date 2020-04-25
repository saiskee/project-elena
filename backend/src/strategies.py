import heapq
import math
from abstract_strategy import RoutingStrategy
from priority_queue import PriorityQueue
import graph_utils

# Used in Dijkstra
from itertools import count


class StrategyBFS(RoutingStrategy):
    def __init__(self, graph):
        super().__init__(graph)

    def get_route(self, start, goal, edge_weight='length'):
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


class StrategyDijkstra(RoutingStrategy):
    def __init__(self, graph):
        super().__init__(graph)

    def get_route(self, source, goal, edge_weight='length'):
        graph = self.graph
        weight = weight_function(graph, edge_weight)

        paths = {source: [source]}

        successor_graph = graph._succ if graph.is_directed() else graph._adj

        push = heapq.heappush
        pop = heapq.heappop
        dist = {} # Dictionary of Final distances
        seen = {}
        
        c = count()
        queue = []
        if source not in graph:
            return [] # Figure out way to handle exceptions properly
        seen[source] = 0
        push(queue, (0, next(c), source))
        while queue:
            d, _, v = pop(queue)
            if v in dist:
                continue # already searched this node
            dist[v] = d
            if v == goal:
                break
            for u, e in successor_graph[v].items():
                if (edge_weight=="elevation_change"):
                    cost = max(0, weight(v, u, e))
                else:
                    cost = weight(v, u, e) + 1

                if cost is None: continue

                vu_dist = dist[v] + cost
                if u in dist:
                    if vu_dist < dist[u]:
                        pass # Contradictory paths found, negative weights?
                elif u not in seen or vu_dist < seen[u]:
                    seen[u] = vu_dist
                    push(queue, (vu_dist, next(c), u))
                    paths[u] = paths[v]+[u]
        return paths[goal]

class StrategyDijkstraWithLimit(RoutingStrategy):
     # Assume Limit is some percentage of the shortest path [0,1]
    def __init__(self, graph, limit):
        super().__init__(graph)
        self.limit = limit

   
    def get_route(self, source, goal, edge_weight='elevation_change'):
        graph = self.graph

        length_dijkstra = StrategyDijkstra(graph)
        shortest_path = length_dijkstra.get_route(source, goal)
        shortest_path_length = graph_utils.get_path_length(graph, shortest_path)
        max_path_length = shortest_path_length + shortest_path_length * self.limit

        weight = weight_function(graph, edge_weight)
        length_func = weight_function(graph, 'length')

        paths = {source: [source]}

        successor_graph = graph._succ if graph.is_directed() else graph._adj

        push = heapq.heappush
        pop = heapq.heappop
        dist = {} # Dictionary of Final Weights
        length_dict = {} # Dictionary of Lengths
        seen = {}
        
        c = count()
        queue = []
        if source not in graph:
            return [] # Figure out way to handle exceptions properly
        seen[source] = 0
        push(queue, (0, next(c), source, 0))
        while queue:
            d, _, v, dist_so_far = pop(queue)
            if v in dist:
                continue # already searched this node
            dist[v] = d
            length_dict[v] = dist_so_far

            if v == goal:
                break
            for u, e in successor_graph[v].items():
                if (edge_weight=="elevation_change"):
                    cost = max(0, weight(v, u, e))
                    length = length_func(v, u, e)
                else:
                    cost = weight(v, u, e) + 1

                if cost is None: continue

                vu_dist = dist[v] + cost
                vu_length = length_dict[v] + length
                if u in dist:
                    if vu_dist < dist[u]:
                        pass # Contradictory paths found, negative weights?
                elif (u not in seen or vu_dist < seen[u]) and vu_length <= max_path_length:
                    seen[u] = vu_dist
                    push(queue, (vu_dist, next(c), u, vu_length))
                    paths[u] = paths[v]+[u]
        return paths[goal]

class StrategyAStar(RoutingStrategy):
    def __init__(self, graph):
        super().__init__(graph)
    
    def manhat(self, start, goal):
        amherst_graph = self.graph
        start_x, start_y = amherst_graph.nodes[start]['x'], amherst_graph.nodes[start]['y']
        end_x, end_y = amherst_graph.nodes[goal]['x'], amherst_graph.nodes[goal]['y']
        # return 0 # Dijkstra, essentially
        return ((end_x - start_x) ** 2 + (end_y - start_y) ** 2)**0.5

    def get_route(self, source, goal, edge_weight='length'):
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


def weight_function(graph, weight):
    def weight_(source, dest, edge_data):
        return min(attr.get(weight, 1) for attr in edge_data.values())
    return weight_
