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

    def draw(self, screen, color, camera_offset):
        for edge in self.edges:
            start_pos = (edge.node1.x + camera_offset.x, edge.node1.y + camera_offset.y)
            end_pos = (edge.node2.x + camera_offset.x, edge.node2.y + camera_offset.y)
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

        for node in self.nodes:
            node_rect = pygame.Rect(node.x + camera_offset.x, node.y + camera_offset.y, node.size, node.size)
            pygame.draw.rect(screen, color, node_rect)
