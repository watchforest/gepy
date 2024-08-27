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

    def draw(self, screen, color, camera):
        # Draw edges
        for edge in self.edges:
            start_pos = camera.apply(pygame.Rect(edge.node1.x, edge.node1.y, 0, 0)).topleft
            end_pos = camera.apply(pygame.Rect(edge.node2.x, edge.node2.y, 0, 0)).topleft
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

        # Draw nodes as simple rectangles or circles
        for node in self.nodes:
            node_rect = pygame.Rect(node.x, node.y, node.size, node.size)
            pygame.draw.rect(screen, color, camera.apply(node_rect))
