import pygame
import sys
from config import WIDTH, HEIGHT, BLACK, FPS
from game.network import Network
from game.player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Network Node Game")
    clock = pygame.time.Clock()

    network = Network()
    player = Player(network.add_node(100, 100))

    node2 = network.add_node(300, 100)
    network.add_edge(player.node, node2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Game logic here
        # Example: Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.move_to_node(node2)

        screen.fill(BLACK)
        network.draw(screen)
        player.draw(screen, WHITE)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
