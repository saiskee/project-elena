# Source: osmnx.elevation - modified to use a different API

import math
import networkx as nx
import pandas as pd
import requests


def add_node_elevations(G, max_loc_per_batch=1000, pause_duration=0.0):  # pragma: no cover
    """
    Get the elevation (meters) of each node in the network and add it to the
    node as an attribute.

    Parameters
    ----------
    G : networkx multidigraph
    max_locations_per_batch : int
        max number of coordinate pairs to submit in each API call (if this is
        too high, the server will reject the request because its character
        limit exceeds the max)
    pause_duration : float
        time to pause between API calls

    Returns
    -------
    G : networkx multidigraph
    """

    # Dockerized open-elevation for elevation data and hosted on our own machine
    url_template = 'http://0.0.0.0:8080/api/v1/lookup'

    # make a pandas series of all the nodes' coordinates as 'lat,lng'
    # round coorindates to 5 decimal places (approx 1 meter) to be able to fit
    # in more locations per API call
#     node_points = pd.Series({node:'{:.5f},{:.5f}'.format(data['y'], data['x']) for node, data in G.nodes(data=True)})
    node_points = [{'latitude': data['y'], 'longitude': data['x']} for node, data in G.nodes(data=True)]
    print('Requesting node elevations from the API in {} calls.'.format(math.ceil(len(node_points) / max_loc_per_batch)))

    # break the series of coordinates into chunks of size max_locations_per_batch
    # API format is locations=lat,lng|lat,lng|lat,lng|lat,lng...
    results = []
    # for i in range(0, 1):
    for i in range(0, len(node_points), max_loc_per_batch):
        chunk = node_points[i: i + max_loc_per_batch]
        locations = {'locations': chunk}

        try:
            print(locations)
            response = requests.post(url_template, json=locations)
            response_json = response.json()
            print(response_json)

        except Exception as e:
            print(e)
            print('Exception: Server responded with {}: {}'.format(response.status_code, response.reason))

        # append these elevation results to the list of all results
        results.extend(response_json['results'])

    # sanity check that all our vectors have the same number of elements
    if not (len(results) == len(G.nodes()) == len(node_points)):
        raise Exception('Graph has {} nodes but we received {} results from the elevation API.'.format(len(G.nodes()), len(results)))
    else:
        print('Graph has {} nodes and we received {} results from the elevation API.'.format(len(G.nodes()), len(results)))

    # add elevation as an attribute to the nodes
    df = pd.DataFrame(node_points, columns=['node_points'])
    df['elevation'] = [result['elevation'] for result in results]
    # temp = [result['elevation'] for result in results]
    # print(temp)
    df['elevation'] = df['elevation'].round(3)  # round to millimeter
    nx.set_node_attributes(G, name='elevation', values=df['elevation'].to_dict())
    print('Added elevation data to all nodes.')

    return G