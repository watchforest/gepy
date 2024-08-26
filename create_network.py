import pandas as pd
import networkx as nx
from game.network import Network

G = 'assets/network/fully_connected_15_nodes.gexf'
df = pd.read_csv('assets/network/TestNetwork.csv')

def load_gexf_to_network(gexf_file_path, network):
    # Load the GEXF file
    graph = nx.read_gexf(gexf_file_path)

    # Create a dictionary to map node IDs to Node objects
    node_dict = {}

    # Add nodes to the network
    for node_id, data in graph.nodes(data=True):
        x = data['x']
        y = data['y']
        name = data.get('Id', node_id)  # Use label if available, otherwise the node ID
        message = 'TEST'
        print(f"Adding node with x={x}, y={y}, name={name}")
        node = network.add_node(x, y, name, message)
        node_dict[node_id] = node

    # Add edges to the network
    for source, target in graph.edges():
        node1 = node_dict[source]
        node2 = node_dict[target]
        network.add_edge(node1, node2)

# Usage
network = Network()
load_gexf_to_network(G, network)


