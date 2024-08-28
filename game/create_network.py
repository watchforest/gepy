import pandas as pd
import networkx as nx
from game.network import Network

def load_gexf_to_network(gexf_file_path, network, scale=10000):
    # Load the GEXF file
    graph = nx.read_gexf(gexf_file_path)
    pos = nx.spring_layout(graph)
    weighted_degrees = dict(graph.degree(weight='weight'))
    # Create a dictionary to map node IDs to Node objects
    node_dict = {}

    # Add nodes to the network
    for g_node, (x, y) in pos.items():
        x = x * scale + 600  # Scale up the x position
        y = y * scale + 550  # Scale up the y position
        name = g_node  # Use label if available, otherwise the node ID
        message = ' '
        # Extract the node weight, defaulting to 1 if not present
        node_weight = weighted_degrees[g_node]*5
        #print(f"Adding node with x={x}, y={y}, name={name}, weight={node_weight}")
        # Add the node to the network
        node = network.add_node(x, y, name, message, node_weight)
        node_dict[g_node] = node

    # Add edges to the network and set neighbors
    for source, target in graph.edges():
        node1 = node_dict[source]
        node2 = node_dict[target]
        network.add_edge(node1, node2)

        # Only add the closest node in each direction
        def add_neighbor_if_closer(node1, node2, direction1, direction2):
            if direction1 not in node1.neighbors or (
                (node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2
            ) < (
                (node1.neighbors[direction1].x - node1.x) ** 2 + (node1.neighbors[direction1].y - node1.y) ** 2
            ):
                node1.add_neighbor(direction1, node2)
                node2.add_neighbor(direction2, node1)

        for source, target in graph.edges():
            node1 = node_dict[source]
            node2 = node_dict[target]
            network.add_edge(node1, node2)

            if node1 != node2:
                dx = node2.x - node1.x
                dy = node2.y - node1.y

                # Primary Directions
                if dx > 0 and abs(dy) <= abs(dx):  # Mostly right
                    add_neighbor_if_closer(node1, node2, 'right', 'left')
                elif dx < 0 and abs(dy) <= abs(dx):  # Mostly left
                    add_neighbor_if_closer(node1, node2, 'left', 'right')
                if dy > 0 and abs(dx) <= abs(dy):  # Mostly down
                    add_neighbor_if_closer(node1, node2, 'down', 'up')
                elif dy < 0 and abs(dx) <= abs(dy):  # Mostly up
                    add_neighbor_if_closer(node1, node2, 'up', 'down')

                # Diagonal Directions
                if dx > 0 and dy < 0:  # Up-right
                    add_neighbor_if_closer(node1, node2, 'up-right', 'down-left')
                elif dx > 0 and dy > 0:  # Down-right
                    add_neighbor_if_closer(node1, node2, 'down-right', 'up-left')
                elif dx < 0 and dy < 0:  # Up-left
                    add_neighbor_if_closer(node1, node2, 'up-left', 'down-right')
                elif dx < 0 and dy > 0:  # Down-left
                    add_neighbor_if_closer(node1, node2, 'down-left', 'up-right')

def create_network(gexf_file_path):
    # Initialize the network
    network = Network()

    # Load data into the network from the GEXF file
    G = gexf_file_path
    load_gexf_to_network(G, network)

    return network
