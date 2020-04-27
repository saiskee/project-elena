from flask import Flask, request, render_template
import json
import osmnx as ox
import networkx as nx
import pickle as pkl
from context import Context
import strategies

app = Flask(__name__)
graphs = {}
modes = [("drive", graphs), ("walk", graphs), ("bike", graphs)]


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

    graph = graphs[data['method']]
    goal = data['goal']
    algorithm = data['algorithm']

    # Get Lat Long of Address from Nominatim Geocoding API
    try:
        start_node = get_node_from_address(graph, data['start'])
        dest_node = get_node_from_address(graph, data['dest'])
    except Exception as e:
        return str(e), 501

    limit = float(data['limit'])/100
    return get_route(graph, start_node, dest_node, algorithm, limit=limit, goal=goal)


def get_route(graph, start_node, dest_node, algorithm='AStar', limit=0, goal='Minimize Elevation Gain'):
    print("Setting up right algorithm object")
    if len(goal.split()) > 1:
        weight = goal.split()[1]
        if weight.startswith('Elevation'):
            weight = 'elevation_change'
        else:
            weight = 'grade'
    if goal.startswith('Min'):
        method = 'min ' + weight
    elif goal.startswith('Max'):
        method = 'max ' + weight
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

    elif algorithm == 'Networkx Dijkstra':
        path = nx.shortest_path(start_node, dest_node, weight='length')

    print(path)
    path, path_data = prep_path(graph, path)
    return {'path': path, 'path_data': path_data}


def get_node_from_address(graph, address):
    try:
        latlng = ox.geocode(address)
        node, dist = ox.get_nearest_node(graph, latlng, return_dist=True)
        if dist > 10000:
            raise Exception("{} is not currently included in Routing Capabilities".format(address))
        return node
    except:
        raise Exception("Could not find location '{}'".format(address))


def prep_path(graph, path):
    final_path = []
    lengths_and_elevations = []
    for i in range(len(path)-1):
        nodeId = path[i]
        nextNode = path[i+1]
        x = graph.nodes[nodeId]['x']
        y = graph.nodes[nodeId]['y']
        elevation = graph.nodes[nodeId]['elevation']
        edge = graph[nodeId][nextNode][0]
        length = 0
        if 'length' in edge:
            length = edge['length']
        grade = 0
        if 'grade' in edge:
            grade = max(0, edge['grade'])
        final_path.append((x, y))
        lengths_and_elevations.append({'length': length, 'elevation': elevation, 'grade': grade})
    # Add Last Node
    lastNode = graph.nodes[nextNode]
    final_path.append((lastNode['x'], lastNode['y']))
    lengths_and_elevations.append({'length': 0, 'elevation': lastNode['elevation']})
    return final_path, lengths_and_elevations

# if __name__ == "__main__":
#     # amherst books
#     start_lat = 42.375801
#     start_long = -72.519547
#     # CS building
#     end_lat = 42.395611
#     end_long = -72.531612
#     # other_get_route(start_lat, start_long, end_lat, end_long)
#     start_node = ox.get_nearest_node(graphs['drive'], (start_lat, start_long))
#     end_node = ox.get_nearest_node(graphs['drive'], (end_lat, end_long))
#     print("Calling get_route from {} to {}".format(start_node, end_node))
#     get_route(graphs['drive'], start_node, end_node, algorithm='Dijkstra', name='Route', color=(255, 0, 0), limit=0,
#               goal='Min')

# harvard to TD garden

