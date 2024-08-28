from .node import Node
from .edge import Edge
import pygame
from pygame import gfxdraw
from game.styles import NODE_COLOR

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y, name, message, size, cluster):
        node = Node(x, y, name, message, size, cluster)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.edges.append(edge)

    def draw(self, screen, color, camera):
        for edge in self.edges:
            start_pos = camera.apply(pygame.Rect(edge.node1.x, edge.node1.y, 0, 0)).topleft
            end_pos = camera.apply(pygame.Rect(edge.node2.x, edge.node2.y, 0, 0)).topleft
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

        for node in self.nodes:
            node_center = camera.apply(pygame.Rect(node.x, node.y, 0, 0)).center
            pygame.draw.circle(screen, NODE_COLOR[node.cluster], node_center, node.size)

