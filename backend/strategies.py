import heapq
import math
from abstract_strategy import RoutingStrategy
from priority_queue import PriorityQueue


class StrategyUCS(RoutingStrategy):
    def __init__(self, flat_graph, projected_graph, g_nodes):
        super().__init__(flat_graph, projected_graph, g_nodes)

    def get_route(self, start, goal):

        print("Start: ", start, "End:", goal);
        # UCS uses priority queue, priority is the cumulative cost (smaller cost)
        queue = PriorityQueue()

        # expands initial node
        graph = self._projected_graph

        # get the keys of all successors of initial node
        neighbors = graph.neighbors(start)

        visited = [start]

        # adds the keys of successors in priority queue
        for neighbor in neighbors:
            weight = self.get_edge_weight(start, neighbor)
            # each item of queue is a tuple (key, cumulative_cost)
            if neighbor not in visited:
                queue.insert(([start, neighbor], weight), weight)

        reached_goal, cumulative_cost_goal, complete_path = False, -1, []
        while not queue.is_empty():
            # remove item off queue
            path, cost_node = queue.remove()
            current_node = path[-1]
            visited.append(current_node)
            if current_node == goal:
                reached_goal, cumulative_cost_goal, complete_path = True, cost_node, path
                break

            # get all successors of key_current_node
            current_neighbors = graph.neighbors(current_node)

            if current_neighbors:  # checks if contains successors
                # insert all successors of key_current_node in the queue
                for current_neighbor in current_neighbors:
                    if current_neighbor not in visited:
                        cumulative_cost = self.get_edge_weight(current_node, current_neighbor) + cost_node
                        new_path = list(path)
                        new_path.append(current_neighbor)
                        queue.insert((new_path, cumulative_cost), cumulative_cost)

        if reached_goal:
            print('\nReached goal! Cost: %s\n' % cumulative_cost_goal)
            return complete_path
        else:
            print('\nUnfulfilled goal.\n')
            return complete_path

    # Function to calculate weights of edges based on distance between nodes
    def get_edge_weight(self, node1, node2):
        lat1 = self._g_nodes.loc[node1].x
        lon1 = self._g_nodes.loc[node1].y
        lat2 = self._g_nodes.loc[node2].x
        lon2 = self._g_nodes.loc[node2].y

        return math.sqrt(math.pow(lat2 - lat1, 2) + math.pow(lon2 - lon1, 2))


class StrategyBFS(RoutingStrategy):
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
