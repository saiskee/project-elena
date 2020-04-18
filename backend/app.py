from flask import Flask, request, render_template
import json
import osmnx as ox
import networkx as nx
import pickle as pkl
from context import Context
import strategies

app = Flask(__name__)

mode = "drive" # "drive", "walk", "cycle"

# Load Cached Graphs from Memory
print("Loading Graph")
with open("./data/massachusetts_{}.pkl".format(mode), 'rb') as infile:
    massachusetts_graph = pkl.load(infile)

print("Cached Graphs Loaded!")

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", token="Hello elena")

@app.route('/route', methods=['POST'])
def route():
    """
	request.data: {
		start: "Start Addres Lane"
		dest: "Dest"
		goal: "Max/ Min"
		limit: "##"
		algorithm: "ucs/astar/bfs/..."
	}
	"""
    data = json.loads(request.data)
    print(data)
    # Get Lat Long of Address from Nominatim Geocoding API
    start_latlng = ox.geocode(data['start'])
    dest_latlng = ox.geocode(data['dest'])

    start_node = ox.get_nearest_node(massachusetts_graph, start_latlng)
    dest_node = ox.get_nearest_node(massachusetts_graph, dest_latlng)
    
    algorithm = data['algorithm']

    return get_route(start_node, dest_node, algorithm)


def get_route(start_node, dest_node, algorithm='astar',name='Route', color = (255,0,0)):

    # if algorithm == 'AStar (Old)':
    #     context = Context(strategies.StrategyAStarOld(massachusetts_graph))
    #     path = context.run_strategy_route(start_node, dest_node)
    
    # if algorithm == 'Uniform Cost Search':
    #     context = Context(strategies.StrategyUCS(massachusetts_graph))
    #     path = context.run_strategy_route(start_node, dest_node)
    
    if algorithm == 'Breadth First Search':
        context = Context(strategies.StrategyBFS(massachusetts_graph))
        path = context.run_strategy_route(start_node, dest_node)
    
    elif algorithm == 'Dijkstra':
        context = Context(strategies.StrategyDijkstra(massachusetts_graph))
        path = context.run_strategy_route(start_node, dest_node)

    elif algorithm == 'AStar':
        context = Context(strategies.StrategyAStar(massachusetts_graph))
        path = context.run_strategy_route(start_node, dest_node)
        # path = nx.astar_path(amherst_graph, start_node, dest_node, weight='length', heuristic=manhat)
    
    elif algorithm == 'Networkx Dijkstra':
        path = nx.shortest_path(massachusetts_graph, start_node, dest_node, weight='length')
    print(path)
    final_path = []
    for i in range(len(path)-1):
        nodeId = path[i]
        nextNode = path[i+1]
        x = massachusetts_graph.nodes[nodeId]['x']
        y = massachusetts_graph.nodes[nodeId]['y']
        edge = massachusetts_graph[nodeId][nextNode][0]
        grade = 0
        if 'grade' in edge:
            grade = edge['grade']
        final_path.append((x,y,grade))
    # path = [[massachusetts_graph.nodes[nodeId]['x'], massachusetts_graph.nodes[nodeId]['y'], massachusetts_graph.nodes[nodeId]['elevation']] for nodeId in path]
    return { 'path': final_path, 'name': name, 'color': color }
    
    

# def get_route_(start_lat, start_long, end_lat, end_long):  # common out this line and uncomment the above lines to run with flask
#     start_node = ox.get_nearest_node(amherst_graph, (start_lat, start_long))
#     end_node = ox.get_nearest_node(amherst_graph, (end_lat, end_long))
#     print("Set Strategy to A*.")
#     context = Context(strategies.StrategyAStar(amherst_graph, amherst_projected, g_nodes))
#     path = context.run_strategy_route(start_node, end_node)
#     print_path(path)
#     print("Set Strategy to UCS.")
#     context.strategy = strategies.StrategyUCS(amherst_graph, amherst_projected, g_nodes)
#     path = context.run_strategy_route(start_node, end_node)
#     print_path(path)


# def print_path(path):
#     return_path = []
#     for node in path:
#         lat = amherst_projected.nodes[node]["lat"]
#         lng = amherst_projected.nodes[node]["lon"]
#         return_path.append({'lat': lat, 'lng': lng})
#     print(return_path)
#     return {"nodes": return_path}


# if __name__ == "__main__":
#     print("Calling get_route")
#     # amherst books
#     start_lat = 42.375801
#     start_long = -72.519547
#     # CS building
#     end_lat = 42.395611
#     end_long = -72.531612
#     get_route(start_lat, start_long, end_lat, end_long)
