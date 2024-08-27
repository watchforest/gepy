import pygame

class Node:
    def __init__(self, x, y, name, message, size):
        self.x = x
        self.y = y
        self.name = name
        self.message = message
        self.size = int(size)
        self.neighbors = {}


    def draw(self, surface, color):
        pygame.draw.circle(surface, color, (self.x, self.y), self.size+10)  # Draw the node
        font = pygame.font.Font(None, 24)
        name_surface = font.render(self.name, True, pygame.Color('white'))
        surface.blit(name_surface, (self.x + 12, self.y - 12))  # Draw the node's name

    def add_neighbor(self, direction, node):
        self.neighbors[direction] = node
