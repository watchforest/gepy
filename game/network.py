from .node import Node
from .edge import Edge
import pygame

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y, name, message, size):
        node = Node(x, y, name, message, size)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.edges.append(edge)

    def draw(self, screen, color):
        # Ensure the color is valid
        if isinstance(color, str):
            color = pygame.Color(color)  # Convert color string to pygame.Color
        elif not isinstance(color, pygame.Color) and not isinstance(color, tuple):
            color = (255, 255, 255)  # Default to white if color is invalid

        for edge in self.edges:
            edge.draw(screen, color)
        for node in self.nodes:
            node.draw(screen, color)
