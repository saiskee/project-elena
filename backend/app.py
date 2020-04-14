from flask import Flask, request
import json
import osmnx as ox
import pickle as pkl
from context import Context
import strategies

app = Flask(__name__)

# Load Cached Graphs from Memory
print("Loading Graphs")
infile = open("./data/cached_graphs/amherst_graph_no_elevation_drive.pkl", 'rb')
amherst_graph = pkl.load(infile)

infile = open("./data/amherst_graph_elevation_drive_projected.pkl", 'rb')
amherst_projected = pkl.load(infile)
g_nodes = ox.graph_to_gdfs(amherst_graph, edges=False)


@app.route('/route', methods=['POST'])
def route():
    """
	request.data: {
		start: "Start Addres Lane"
		destination: "Dest"
		goal: "Max/ Min"
		limit: "##"
		algorithm: "ucs/astar/bfs/..."
	}
	"""
    data = json.loads(request.data)
    start_node = ox.get_nearest_node(data.start)
    dest_node = ox.get_nearest_node(data.destination)
    algorithm = data.algorithm

    return get_route(start_node, end_node, algorithm)

def get_route(start_node, dest_node, algorithm='astar',name='Route', color = (255,0,0)):

    if algorithm == 'astar':
        context = Context(strategies.StrategyAStar(amherst_graph, amherst_projected, g_nodes))
        path = context.run_strategy_route(start_node, end_node)
    if algorithm == 'ucs':
        context.strategy = strategies.StrategyUCS(amherst_graph, amherst_projected, g_nodes)
        path = context.run_strategy_route(start_node, end_node)

    path = [[lng, lat] for [lat, lng] in path]
    return { path: path, name: name, color: color }
    
    

def get_route_(start_lat, start_long, end_lat, end_long):  # common out this line and uncomment the above lines to run with flask
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
