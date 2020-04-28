from flask import Flask, request, render_template
import json
import osmnx as ox
import networkx as nx
import pickle as pkl
from context import Context
import strategies
import webbrowser

app = Flask(__name__)
graphs = {}
modes = [("drive", graphs), ("walk", graphs), ("bike", graphs)]


def load_graph(method, graphs):
    """
    Loads MA graphs for specified method into memory.

    Parameters:
    -----------
    method: string
        The specific graph to load. ex: drive, bike, walk
    graphs: {string:graph}
        Map that stores the graphs with the method as the key.

    Returns:
    --------
        Nothing
    """
    with open("data/massachusetts_{}.pkl".format(method), 'rb') as infile:
        _graph = pkl.load(infile)
        graphs[method] = _graph
        print('Loaded {} graph'.format(method))


# Load Cached Graphs from Memory
print("Loading Graphs")
for mode in modes:
    load_graph(mode[0], mode[1])


print("Cached Graphs Loaded!")

webbrowser.open('http://localhost:5000', new=2)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", token="Hello elena")


@app.route('/route', methods=['POST'])
def route():
    """
        Receives requests from front end and extracts data to run the routing function.

        Parameters:
        -----------
        request: Request
            The HTTP Post request with data in the form:
                start: "Start Address Lane"
                dest: "Dest"
                goal: "Minimize Elevation Gain / Maximize Elevation Gain"
                limit: "##"
                algorithm: "ucs/astar/bfs/..."
                method: "drive" / walk / bike

        Returns:
        --------
            Result of get_route function
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
        print(e)
        return str(e), 501

    limit = float(data['limit'])/100
    return get_route(graph, start_node, dest_node, algorithm, limit=limit, goal=goal)


def get_route(graph, start_node, dest_node, algorithm='AStar', limit=0, goal='Minimize Elevation Gain'):
    """
            Receives requests from front end and extracts data to run the routing function.

            Parameters:
            -----------
            graph: networkx Graph
                The graph to perform the routing algorithm on.
            start_node: networkx Node
                The starting node for the graph.
            dest_node: networkx Node
                The destination node for the graph.
            algorithm: String
                The algorithm to run. ex: AStar, Breadth First Search, Dijkstra
            limit: Float
                The percentage that the generated path can deviate from the shortest path.
            goal: String
                The objective of the route. ex: Minimize Elevation Gain, Maximize Elevation Gain

            Returns:
            --------
                {'path': [[long, lat]], 'path_data': [{elevation, length, grade}]}
    """
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


    print(path)
    path, path_data = prep_path(graph, path)
    return {'path': path, 'path_data': path_data}


# Convert an address to a node
def get_node_from_address(graph, address):
    """
                Converts a string address to the closest node on a graph.

                Parameters:
                -----------
                graph: networkx Graph
                    The graph to perform the look up.
                address: String
                    The address to convert to a node.

                Returns:
                --------
                    node: The closest node to the address given.
     """
    try:
        latlng = ox.geocode(address)
        node, dist = ox.get_nearest_node(graph, latlng, return_dist=True)
        if dist > 10000:
            raise Exception("{} is not currently included in Routing Capabilities".format(address))
        return node
    except:
        raise Exception("Could not find location '{}'".format(address))


def prep_path(graph, path):
    """
                Converts the path of nodes to data that can be sent back to the front end.

                Parameters:
                -----------
                graph: networkx Graph
                    The graph to perform the routing algorithm on.
                path: [networkx Node]
                    The array of nodes produced by the routing function.

                Returns:
                --------
                    final_path: [[long, lat]]
                    lengths_and_elevations: [{elevation, length, grade}]}
    """
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


# Code to run backend on its own
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
