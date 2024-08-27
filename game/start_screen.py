import pygame
import sys
import os
import game.colors as colors
from game.create_network import create_network  # Import from create_network module
from game.player import Player  # Import Player class from player module
from game.camera import Camera  # Import Camera class from camera module

# Initialize Pygame
pygame.init()

# Define constants
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()
FPS = 60

# Determine the base directory of the project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
font_path = os.path.join(base_dir, 'assets', 'font', 'Pastor of Muppets.TTF')

# Load the title font
title_font = pygame.font.Font(font_path, 200)

# Setup font for button rendering
button_font = pygame.font.Font(None, 74)

# Load the image for the start screen
image_path = os.path.join(base_dir, 'assets', 'images', 'start_screen_image.png')
start_screen_image = pygame.image.load(image_path).convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (600, 600))

# Button class to handle the buttons
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = colors.WHITE  # Button color is initially WHITE
        self.text_color = colors.BLACK  # Text color is initially BLACK
        self.hovered = False
        self.action = action
        self.font = pygame.font.Font(font_path, 74)

    def draw(self, surface):
        # Change button color on hover
        pygame.draw.rect(surface, colors.BLACK if self.hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color if not self.hovered else colors.WHITE)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.action:
                self.action()
        else:
            self.hovered = False

# Game loop definition
def game_loop():
    network = create_network('assets/network/random_graph_100_nodes.gexf')
    player = Player(network.nodes[0], pygame.Color(255, 0, 0))

    # Assume the map is larger than the screen size
    map_width = 2000  # Replace with your map's width
    map_height = 2000  # Replace with your map's height

    # Initialize the camera to follow the player within the map bounds
    camera = Camera(WIDTH, HEIGHT, map_width, map_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Update the camera position to follow the player
        camera.update(player)
        camera_offset = camera.apply_offset()

        screen.fill(colors.BLACK)
        
        # Draw the network with camera offset
        network.draw(screen, colors.WHITE, camera_offset)

        # Draw the player with camera offset
        screen.blit(player.image, player.rect.move(camera_offset))
        player.draw_message(screen, camera_offset)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# Campaign menu
def campaign_menu():
    stage_buttons = [Button(f"Stage {i+1}", WIDTH // 4, HEIGHT // 5 + i * 40, 300, 50, lambda i=i: start_stage(i)) for i in range(3)]

    running = True
    while running:
        screen.fill(colors.BLACK)
        title_surface = title_font.render("Campaign", True, colors.WHITE)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in stage_buttons:
                    button.check_for_input(mouse_position)

        mouse_position = pygame.mouse.get_pos()
        for button in stage_buttons:
            button.check_for_input(mouse_position)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def start_stage(stage_number):
    print(f"Starting stage {stage_number + 1}...")

def upload_files():
    print("Uploading files...")

def run_files():
    print("Running files...")

# Start screen
def start_screen():
    start_button = Button("Start", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75, game_loop)
    #levels_button = Button("Levels", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75, campaign_menu)
   # upload_button = Button("Upload Files", WIDTH // 4 - 150, HEIGHT // 2 + 300, 300, 75, upload_files)
    #run_button = Button("Run Files", WIDTH // 4 - 150, HEIGHT // 2 + 400, 300, 75, run_files)
    exit_button = Button("Exit Game", WIDTH - 250, 50, 200, 75, lambda: (pygame.quit(), sys.exit()))

    buttons =  [start_button, exit_button] #start_button, upload_button, run_button.

    running = True
    while running:
        screen.fill(colors.BLACK)
        title_surface = title_font.render("SYNDESI", True, colors.WHITE)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_for_input(mouse_position)

        mouse_position = pygame.mouse.get_pos()
        for button in buttons:
            button.check_for_input(mouse_position)
            button.draw(screen)

        screen.blit(start_screen_image, (WIDTH - start_screen_image.get_width() - 50, HEIGHT // 2 - start_screen_image.get_height() // 4))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_screen()
