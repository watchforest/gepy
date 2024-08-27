import pandas as pd
import networkx as nx
from game.network import Network

def load_gexf_to_network(gexf_file_path, network, scale=10):
    # Load the GEXF file
    graph = nx.read_gexf(gexf_file_path)

    # Create a dictionary to map node IDs to Node objects
    node_dict = {}

    # Add nodes to the network
    for node_id, data in graph.nodes(data=True):
        x = data['x'] * scale  # Scale up the x position
        y = data['y'] * scale  # Scale up the y position
        name = data.get('Id', node_id)  # Use label if available, otherwise the node ID
        message = 'TEST'
        print(f"Adding node with x={x}, y={y}, name={name}")
        node = network.add_node(x, y, name, message)
        node_dict[node_id] = node

    # Add edges to the network and set neighbors
    for source, target in graph.edges():
        node1 = node_dict[source]
        node2 = node_dict[target]
        network.add_edge(node1, node2)

        # Only add the closest node in each direction
        if node1.x < node2.x:  # Right direction
            if 'right' not in node1.neighbors or (node2.x - node1.x) < (node1.neighbors['right'].x - node1.x):
                node1.add_neighbor('right', node2)
                node2.add_neighbor('left', node1)
        elif node1.y < node2.y:  # Down direction
            if 'down' not in node1.neighbors or (node2.y - node1.y) < (node1.neighbors['down'].y - node1.y):
                node1.add_neighbor('down', node2)
                node2.add_neighbor('up', node1)

def create_network():
    # Initialize the network
    network = Network()
    
    # Load data into the network from the GEXF file
    G = 'assets/network/fully_connected_15_nodes.gexf'
    load_gexf_to_network(G, network)
    
    return network
