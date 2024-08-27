import pygame
import sys
from game.network import Network
from game.player import Player
from game.create_network import load_gexf_to_network
from game.start_screen import start_screen
import game.colors as colors

# Initialize Pygame
pygame.init()

# Define constants
# Setup the display in fullscreen mode without window borders
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
WIDTH, HEIGHT = screen.get_size()  # Get the actual screen size in fullscreen mode
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()
FPS = 60

# Setup font for text rendering
font = pygame.font.Font(None, 36)

# Start screen function
start_screen()

# After the start screen is done, initialize the network and player
G = 'assets/network/fully_connected_15_nodes.gexf'
network = Network()
load_gexf_to_network(G, network)

# Initialize the player at the starting node
player = Player(network.nodes[0], colors.RED)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill(colors.BLACK)
    network.draw(screen, colors.WHITE)
    screen.blit(player.image, player.rect)
    player.draw_message(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
