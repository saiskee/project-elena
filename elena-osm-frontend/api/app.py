from flask import Flask, request
import time
import json
# import pyroutelib3
import numpy as np
import osmnx as ox
import time
import elevation
import pickle as pkl
import threading
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

# Load Cached Graphs from Memory
print("Loading Graphs")
infile = open("../../amherst_graph_no_elevation_drive.pkl", 'rb')
amherst_graph = pkl.load(infile)

infile = open("../../amherst_graph_elevation_drive_projected.pkl", 'rb')
amherst_projected = pkl.load(infile)
g_nodes = ox.graph_to_gdfs(amherst_graph, edges=False)

app = Flask(__name__)

# Performs a Breadth-First search from the Starting Node to the Goal node
def bfs(graph, start, goal):
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

# Performs an AStar search, using Manhattan distance as a heuristic
def AStar(graph, start, end):
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

        if(node == end):
            return backtrack(start, end, map)

        neighbors = graph.neighbors(node)

        for n in neighbors:
            if n not in visited:
                total_cost = path_cost + manhat(node, n) + manhat(n, end)
                heapq.heappush(queue, (total_cost, n, path_cost + manhat(node, n)))
                map[n] = node

    return

# Function for calculating Manhattan Distance
def manhat(start, end):
    start_x, start_y = get_coordinates(start)
    end_x, end_y = get_coordinates(end)

    return math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

# Function for backtracking for AStar
def backtrack(start, end, map):
    path = []
    node = end
    while node in map.keys() and node != None:
        path.append(node)
        node = map[node]

    path.reverse()
    return path

# Get latitude and longitude for a node
def get_coordinates(id):

    g_nodes[['x', 'y']]

    lat = g_nodes.loc[id].x
    lon = g_nodes.loc[id].y

    return [lat, lon]

@app.route('/test', methods=['POST'])
def get_route():

    data = json.loads(request.data)

    start_lat = data[0]["lat"]
    start_long = data[0]["lng"]

    end_lat = data[1]["lat"]
    end_long = data[1]["lng"]

    start_node = ox.get_nearest_node(amherst_graph, (start_lat, start_long))
    end_node = ox.get_nearest_node(amherst_graph, (end_lat, end_long))
    path = AStar(amherst_projected, start_node, end_node)

    return_path = []

    for node in path:
        lat = amherst_projected.nodes[node]["lat"]
        lng = amherst_projected.nodes[node]["lon"]
        return_path.append({'lat': lat, 'lng': lng})
    
    return {"nodes": return_path}
