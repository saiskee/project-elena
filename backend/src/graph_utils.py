def get_path_length(graph, path):
    """
                   Calculates the path length of a given path.

                   Parameters:
                   -----------
                   graph: networkx Graph
                       The graph to perform the routing algorithm on.
                   path: [networkx Node]
                       The array of nodes produced by the routing function.

                   Returns:
                   --------
                       length: The length of the path.
    """
    length = 0
    for i in range(len(path)-1):
        length += graph[path[i]][path[i+1]][0]['length']
    return length


def get_path_elevation(graph, path):
    """
                       Calculates the elevation of a given path.

                       Parameters:
                       -----------
                       graph: networkx Graph
                           The graph to perform the routing algorithm on.
                       path: [networkx Node]
                           The array of nodes produced by the routing function.

                       Returns:
                       --------
                           elevation: The elevation of the path.
    """
    elevation = 0
    for i in range(len(path)-1):
        elevation += max(0, graph.nodes[path[i+1]]['elevation'] - graph.nodes[path[i]]['elevation'])
    return elevation


def weight_function(graph, weight='length'):
    """
                       Returns a weight function given a weight type

                       Parameters:
                       -----------
                       graph: networkx Graph
                           The graph to perform the routing algorithm on.
                       weight: String
                           The type of weight to use. ex: length, grade, elevation_change

                       Returns:
                       --------
                           def: The weight function.
           """
    if weight == 'length':
        def weight_(source, dest, edge_data):
            return min(attr.get(weight, 1) for attr in edge_data.values())
    elif weight == 'grade':
        def weight_(source, dest, edge_data):
            try:
                return max(0, edge_data['grade'])
            except:
                return 0
    elif weight == 'elevation_change':
        def weight_(source, dest, edge_data):
            try:
                elevation_diff = graph.nodes[dest]['elevation'] - graph.nodes[source]['elevation']
                return max(elevation_diff, 0)
            except:
                print("elevation not found: ", source, dest)
                return 0
    return weight_


def get_average_grade(graph, path):
    """
                       Calculates the average grade of the given path

                       Parameters:
                       -----------
                       graph: networkx Graph
                           The graph to perform the routing algorithm on.
                       path: [networkx Node]
                           The array of nodes produced by the routing function.

                       Returns:
                       --------
                           avg_grade: The average grade of the path.
    """
    avg_grade = 0
    for i in range(len(path) - 1):
        avg_grade += max(0, graph[path[i]][path[i+1]][0]['grade'])
    return avg_grade / (len(path) - 1)
