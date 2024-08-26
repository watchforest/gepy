class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), 10)
