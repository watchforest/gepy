import pygame

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def draw(self, screen, color):
        pygame.draw.line(screen, color, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 2)
