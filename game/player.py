class Player:
    def __init__(self, node):
        self.node = node
        self.x = node.x
        self.y = node.y

    def move_to_node(self, target_node):
        self.node = target_node
        self.x = target_node.x
        self.y = target_node.y

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), 15)
