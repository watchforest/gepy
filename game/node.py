import pygame

class Node:
    def __init__(self, x, y, name, message=""):
        self.x = x
        self.y = y
        self.name = name
        self.message = message  # Message associated with the node
        self.neighbors = {}  # Dictionary to hold neighboring nodes

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), 10)

    # def add_neighbor(self, direction, node):
    #     self.neighbors[direction] = node
