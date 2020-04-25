def get_path_length(graph, path):
    length = 0
    for i in range(len(path)-1):
        length += graph[path[i]][path[i+1]][0]['length']
    return length

def get_path_elevation(graph, path):
    elevation = 0
    for i in range(len(path)-1):
        elevation += max(0, graph.nodes[path[i]]['elevation'] - graph.nodes[path[i+1]]['elevation'])
    return elevation