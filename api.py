from flask import Flask
from flask import request
import json
import numpy as np
import osmnx as ox
import time
import pickle as pkl
import threading
import networkx as nx
import matplotlib.pyplot as plt
import json
import heapq
import math
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST', 'GET'])
def find_route():
    data = request.get_json(force=True)
    print(data)

    start = data["start"]
    end = data["end"]
    optimization = data["opt"]
    delta = data["delta"]

    return find_route(start, end, optimization, delta)


def find_route(start, end, optimization, delta):
    G = build_graph(start, end)

    start_node = ox.get_nearest_node(G, (start[0], start[1]))
    end_node = ox.get_nearest_node(G, (end[0], end[1]))

    path = bfs(G, start_node, end_node)

    route = []

    for p in path:
        route.append(get_coordinates(G, p))

    print(route)


    info = {
        "name": "Route 1",
		"color": [255, 0, 0],
        "path": route
    }

    with open('./data.json', 'w') as f:
        json.dump(info, f)

    return info


def build_graph2():
    G = ox.graph_from_place({'state': 'Massachusetts', 'country': 'USA'})
    print(G.number_of_nodes())

    pkl.dump(G, open("mass_graph.pkl", "wb"))


def build_graph(start, end):
    dist = int(haversine(start, end) * 2)

    # G = ox.graph_from_point((start[0], start[1]), distance=dist, network_type='walk')

    infile = open("mass_graph.pkl", 'rb')
    G = pkl.load(infile)

    print(G.number_of_nodes())

    return G


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


# returns distance in meters
def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_coordinates(G, id):
    nodes = ox.graph_to_gdfs(G, edges=False)
    nodes[['x', 'y']]

    lat = nodes.loc[id].x
    lon = nodes.loc[id].y

    return [lat, lon]


def test():
    data = json.loads(
        '''{   "delta": 50,   "end": [     42.351049, -71.105828  ],   "opt": "max",   "start": [     42.373767, -71.118941   ] }''')

    start = data["start"]
    end = data["end"]
    optimization = data["opt"]
    delta = 1 + data["delta"] * 0.01

    find_route(start, end, optimization, delta)
    # build_graph2()


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    print(chr(27) + "[2J")

    test()