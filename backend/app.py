from flask import Flask, request
import json
import osmnx as ox
import pickle as pkl
from context import Context
import strategies

app = Flask(__name__)

# Load Cached Graphs from Memory
print("Loading Graphs")
infile = open("../../cached_graphs/amherst_graph_no_elevation_drive.pkl", 'rb')
amherst_graph = pkl.load(infile)

infile = open("../../cached_graphs/amherst_graph_elevation_drive_projected.pkl", 'rb')
amherst_projected = pkl.load(infile)
g_nodes = ox.graph_to_gdfs(amherst_graph, edges=False)


# @app.route('/test', methods=['POST'])
# def get_route():
    # data = json.loads(request.data)

    # start_lat = data[0]["lat"]
    # start_long = data[0]["lng"]
    #
    # end_lat = data[1]["lat"]
    # end_long = data[1]["lng"]

def get_route(start_lat, start_long, end_lat, end_long):  # common out this line and uncomment the above lines to run with flask
    start_node = ox.get_nearest_node(amherst_graph, (start_lat, start_long))
    end_node = ox.get_nearest_node(amherst_graph, (end_lat, end_long))
    print("Set Strategy to A*.")
    context = Context(strategies.StrategyAStar(amherst_graph, amherst_projected, g_nodes))
    path = context.run_strategy_route(start_node, end_node)
    print_path(path)
    print("Set Strategy to UCS.")
    context.strategy = strategies.StrategyUCS(amherst_graph, amherst_projected, g_nodes)
    path = context.run_strategy_route(start_node, end_node)
    print_path(path)


def print_path(path):
    return_path = []
    for node in path:
        lat = amherst_projected.nodes[node]["lat"]
        lng = amherst_projected.nodes[node]["lon"]
        return_path.append({'lat': lat, 'lng': lng})
    print(return_path)
    return {"nodes": return_path}


if __name__ == "__main__":
    print("Calling get_route")
    # amherst books
    start_lat = 42.375801
    start_long = -72.519547
    # CS building
    end_lat = 42.395611
    end_long = -72.531612
    get_route(start_lat, start_long, end_lat, end_long)
