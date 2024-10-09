import pygame
from game.styles import NODE_COLOR

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []

    class Node:
        def __init__(self, x, y, name, message, size, cluster):
            self.x = x
            self.y = y
            self.name = name
            self.message = message
            self.size = size
            self.cluster = cluster
            self.neighbors = {}
            self.surface = None

        def render_surface(self):
            self.surface = pygame.Surface((self.size * 2 + 20, self.size * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(self.surface, NODE_COLOR[self.cluster], (self.size + 10, self.size + 10), self.size + 10)
            font = pygame.font.Font(None, 24)
            name_surface = font.render(self.name, True, pygame.Color('white'))
            self.surface.blit(name_surface, (self.size + 12, self.size - 12))

        def draw(self, surface, camera_offset_x, camera_offset_y):
            if self.surface is None:
                self.render_surface()
            surface.blit(self.surface, (self.x - self.size - 10 + camera_offset_x, self.y - self.size - 10 + camera_offset_y))

        def add_neighbor(self, direction, node):
            self.neighbors[direction] = node

    class Edge:
        def __init__(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

    def add_node(self, x, y, name, message, size, cluster):
        node = self.Node(x, y, name, message, size, cluster)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        edge = self.Edge(node1, node2)
        self.edges.append(edge)

    def draw(self, screen, color, camera):
        # Draw edges
        for edge in self.edges:
            start_pos = (edge.node1.x + camera.camera.x, edge.node1.y + camera.camera.y)
            end_pos = (edge.node2.x + camera.camera.x, edge.node2.y + camera.camera.y)
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

        # Draw nodes
        for node in self.nodes:
            node.draw(screen, camera.camera.x, camera.camera.y)