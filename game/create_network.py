import networkx as nx
import pygame
from game.network import Network
import random

def create_network(source, width, height):
    if isinstance(source, str):  # If source is a file path
        G = nx.read_gexf(source)
    else:  # If source is not a string, assume it's the number of nodes for a random graph
        G = nx.gnm_random_graph(source, source * 2)  # Creates a random graph

    # Create a Network object
    network = Network()

    # Get the positions of the nodes
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # Scale the positions to fit the desired width and height
    x_values, y_values = zip(*pos.values())
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    
    scale_x = (width - 100) / (x_max - x_min)
    scale_y = (height - 100) / (y_max - y_min)
    scale = min(scale_x, scale_y)

    # Add nodes
    for node_id, (x, y) in pos.items():
        scaled_x = (x - x_min) * scale + 50
        scaled_y = (y - y_min) * scale + 50
        cluster = random.randint(0, 5)  # Random cluster for color variety
        node = network.add_node(scaled_x, scaled_y, str(node_id), "", 10, cluster)

    # Add edges
    for edge in G.edges():
        node1 = network.get_node_by_name(str(edge[0]))
        node2 = network.get_node_by_name(str(edge[1]))
        if node1 and node2:
            network.add_edge(node1, node2)

    # Render the network to a surface
    network.render_to_surface(width, height)
    
    return network
