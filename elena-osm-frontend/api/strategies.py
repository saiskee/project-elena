import heapq
import math
from abstract_strategy import RoutingStrategy


class StrategyUCS(RoutingStrategy):
    def __init__(self, flat_graph, projected_graph, g_nodes):
        super().__init__(flat_graph, projected_graph, g_nodes)

    def get_route(self, start, goal):
        graph = self._projected_graph
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


class StrategyAStar(RoutingStrategy):
    def __init__(self, flat_graph, projected_graph, g_nodes):
        super().__init__(flat_graph, projected_graph, g_nodes)

    def get_route(self, start, goal):
        graph = self._projected_graph
        visited = set()
        queue = []
        map = {}
        cost = 0
        path_cost = 0

        map[start] = None
        heapq.heappush(queue, (cost, start, path_cost))

        while queue:
            cost, node, path_cost = heapq.heappop(queue)
            visited.add(node)
            if node == goal:
                return self.backtrack(start, goal, map)

            neighbors = graph.neighbors(node)

            for n in neighbors:
                if n not in visited:
                    total_cost = path_cost + self.manhat(node, n) + self.manhat(n, goal)
                    heapq.heappush(queue, (total_cost, n, path_cost + self.manhat(node, n)))
                    map[n] = node
        return

    # Function for calculating Manhattan Distance
    def manhat(self, start, goal):
        start_x, start_y = self.get_coordinates(start)
        end_x, end_y = self.get_coordinates(goal)

        return math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)

    # Function for backtracking for AStar
    def backtrack(self, start, end, map):
        path = []
        node = end
        while node in map.keys() and node is not None:
            path.append(node)
            node = map[node]

        path.reverse()
        return path

    # Get latitude and longitude for a node
    def get_coordinates(self, id):

        self._g_nodes[['x', 'y']]

        lat = self._g_nodes.loc[id].x
        lon = self._g_nodes.loc[id].y
        return [lat, lon]


class StrategyDijkstra(RoutingStrategy):
    def __init__(self, flat_graph, projected_graph, g_nodes):
        super().__init__(flat_graph, projected_graph, g_nodes)

    def get_route(self, graph, start, goal):
        pass


