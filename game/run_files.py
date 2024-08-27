import pygame
import sys
from game.network import Network
from game.player import Player
from game.create_network import load_gexf_to_network
from game.camera import Camera
import game.colors as colors

def game_loop(screen, WIDTH, HEIGHT, clock, FPS):
    # Initialize the network and player
    G = 'assets/network/fully_connected_15_nodes.gexf'
    network = Network()
    load_gexf_to_network(G, network)

    player = Player(network.nodes[0], colors.RED)

    # Initialize the camera
    camera = Camera(WIDTH * 2, HEIGHT * 2)  # Assuming a large enough map

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Update camera position
        camera.update(player)

        screen.fill(colors.BLACK)
        network.draw(screen, camera.apply_offset())
        screen.blit(player.image, camera.apply(player))
        player.draw_message(screen, camera.apply_offset())
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Import these here if running directly, not required if run from start_screen.py
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    FPS = 60

    game_loop(screen, WIDTH, HEIGHT, clock, FPS)
