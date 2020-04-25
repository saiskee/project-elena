from flask import Flask, request, render_template
import json
import osmnx as ox
import networkx as nx
import pickle as pkl
from context import Context
import strategies

app = Flask(__name__)
graphs = {}
modes = [("drive", graphs)] #, ("walk", graphs), ("bike", graphs)] 


def load_graph(method, graphs):
    with open("data/massachusetts_{}.pkl".format(method), 'rb') as infile:
        _graph = pkl.load(infile)
        graphs[method] = _graph
        print('Loaded {} graph'.format(method))


# Load Cached Graphs from Memory
print("Loading Graphs")
for mode in modes:
    load_graph(mode[0], mode[1])


print("Cached Graphs Loaded!")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", token="Hello elena")


@app.route('/route', methods=['POST'])
def route():
    """
	request.data: {
		start: "Start Address Lane"
		dest: "Dest"
		goal: "Minimize Elevation Gain / Maximize Elevation Gain"
		limit: "##"
		algorithm: "ucs/astar/bfs/..."
        method: "drive" / walk / bike
	}
	"""
    data = json.loads(request.data)
    print(data)
    # Get Lat Long of Address from Nominatim Geocoding API
    start_latlng = ox.geocode(data['start'])
    dest_latlng = ox.geocode(data['dest'])

    graph = graphs[data['method']]
    goal = data['goal']
    start_node = ox.get_nearest_node(graph, start_latlng)
    dest_node = ox.get_nearest_node(graph, dest_latlng)
    
    algorithm = data['algorithm']
    limit = float(data['limit'])/100
    return get_route(graph, start_node, dest_node, algorithm, limit=limit, goal=goal)


def get_route(graph, start_node, dest_node, algorithm='AStar', name='Route', color=(255, 0, 0),
              limit=0, goal='Minimize Elevation Gain'):
    if goal.startswith('Min'):
        method = 'min'
    elif goal.startswith('Max'):
        method = 'max'
    else:
        method = 'vanilla'

    if algorithm == 'Breadth First Search':
        context = Context(strategies.StrategyBFS(graph, limit, method))
        path = context.run_strategy_route(start_node, dest_node)
    
    elif algorithm == 'Dijkstra':
        context = Context(strategies.StrategyDijkstra(graph, limit, method))
        path = context.run_strategy_route(start_node, dest_node)

    elif algorithm == 'AStar':
        context = Context(strategies.StrategyAStar(graph, limit, method))
        path = context.run_strategy_route(start_node, dest_node)

    # elif algorithm == 'Networkx Dijkstra':
    #     context = Context(strategies.StrategyDijkstra(graph))
    #     path = context.run_strategy_route(start_node, dest_node, weight='length')

    print(path)
    final_path = []
    for i in range(len(path)-1):
        nodeId = path[i]
        nextNode = path[i+1]
        x = graph.nodes[nodeId]['x']
        y = graph.nodes[nodeId]['y']
        edge = graph[nodeId][nextNode][0]
        grade = 0
        if 'grade' in edge:
            grade = edge['grade']
        final_path.append((x,y,grade))
    # path = [[massachusetts_graph.nodes[nodeId]['x'], massachusetts_graph.nodes[nodeId]['y'], massachusetts_graph.nodes[nodeId]['elevation']] for nodeId in path]
    return {'path': final_path, 'name': name, 'color': color}
    

def other_get_route(start_lat, start_long, end_lat, end_long):  # common out this line and uncomment the above lines to run with flask
    start_node = ox.get_nearest_node(graphs['drive'], (start_lat, start_long))
    end_node = ox.get_nearest_node(graphs['drive'], (end_lat, end_long))
    print("Set Strategy to Dijkstra.")
    context = Context(strategies.StrategyDijkstra(graphs['drive']))
    path = context.run_strategy_route(start_node, end_node)
    print_path(path)


def print_path(path):
    return_path = []
    for node in path:
        # should x and y be flipped????
        lat = graphs['drive'].nodes[node]["x"]
        lng = graphs['drive'].nodes[node]["y"]
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
    # other_get_route(start_lat, start_long, end_lat, end_long)
    start_node = ox.get_nearest_node(graphs['drive'], (start_lat, start_long))
    end_node = ox.get_nearest_node(graphs['drive'], (end_lat, end_long))

    # get_route(graphs['drive'], start_node, end_node, algorithm='Breadth First Search', name='Route', color=(255, 0, 0), limit=0,
    #           goal='Vanilla')

