import pygame
from game.styles import NODE_COLOR

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.surface = None

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
            pygame.draw.circle(self.surface, NODE_COLOR[self.cluster], 
                             (self.size + 10, self.size + 10), self.size + 10)
            font = pygame.font.Font(None, 24)
            name_surface = font.render(self.name, True, pygame.Color('white'))
            self.surface.blit(name_surface, (self.size + 12, self.size - 12))

        def draw(self, surface, offset_x, offset_y):
            if self.surface is None:
                self.render_surface()
            surface.blit(self.surface, (int(self.x - self.size - 10 + offset_x), 
                                      int(self.y - self.size - 10 + offset_y)))

        def add_neighbor(self, node):
            direction = self.get_direction(node)
            self.neighbors[direction] = node

        def get_direction(self, other_node):
            dx = other_node.x - self.x
            dy = other_node.y - self.y
            
            # Determine the primary direction based on the larger component
            if abs(dx) > abs(dy):
                return 'right' if dx > 0 else 'left'
            else:
                return 'down' if dy > 0 else 'up'

    def add_node(self, x, y, name, message, size, cluster):
        node = self.Node(x, y, name, message, size, cluster)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        # Add the edge to the edges list
        self.edges.append((node1, node2))
        
        # Set up bidirectional neighbors
        node1.add_neighbor(node2)
        node2.add_neighbor(node1)

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def render_to_surface(self, width, height):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw edges
        for node1, node2 in self.edges:
            pygame.draw.line(self.surface, pygame.Color('gray'),
                           (int(node1.x), int(node1.y)),
                           (int(node2.x), int(node2.y)), 2)
        
        # Draw nodes
        for node in self.nodes:
            node.draw(self.surface, 0, 0)

    def draw(self, screen, camera):
        if self.surface:
            screen.blit(self.surface, (camera.x, camera.y))
