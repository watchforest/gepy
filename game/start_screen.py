import pygame
import sys
import os
from create_network import create_network  # Import from create_network module
from game.player import Player  # Import Player class from player module
from game.camera import Camera  # Import Camera class from camera module

# Initialize Pygame
pygame.init()

# Define constants
# Setup the display in fullscreen mode without window borders
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
WIDTH, HEIGHT = screen.get_size()  # Get the actual screen size in fullscreen mode
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()
FPS = 60

# Define colors
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color('#DAD6C1')

# Load the custom font for the title
font_path = os.path.join('assets', 'font', 'Pastor of Muppets.TTF')
title_font = pygame.font.Font(font_path, 200)  # Adjust the size as needed

# Setup font for button rendering
button_font = pygame.font.Font(None, 74)  # Button font

# Load the image for the start screen (Make sure to place the image in the correct directory)
image_path = os.path.join('assets', 'images', 'start_screen_image.png')
start_screen_image = pygame.image.load(image_path).convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (600, 600))  # Adjust size as needed

# Button class to handle the buttons
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK  # Button color is initially BLACK
        self.text_color = WHITE  # Text color is initially WHITE
        self.hovered = False
        self.action = action
        self.font = pygame.font.Font(font_path, 74)  # Use the same font as the title

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, WHITE, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color if not self.hovered else BLACK)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.action:
                self.action()
        else:
            self.hovered = False

def game_loop():
    # Initialize network and player
    network = create_network()
    player = Player(network.nodes[0], pygame.Color(255, 0, 0))  # Using red color for player

    # Initialize camera
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
        camera_offset = camera.apply_offset()

        screen.fill(BLACK)
        network.draw(screen, camera_offset)
        screen.blit(player.image, player.rect.move(camera_offset))
        player.draw_message(screen, camera_offset)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def start_screen():
    def start_new_game():
        game_loop()

    start_button = Button("Start", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75, start_new_game)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)  # Set background color to the specified hex color
        title_surface = title_font.render("SYNDESI", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))  # Move title up

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if start_button.check_for_input(mouse_position):
                    start_button.action()  # Trigger the start game action

        mouse_position = pygame.mouse.get_pos()
        start_button.check_for_input(mouse_position)

        start_button.draw(screen)

        # Draw the image on the right side of the screen
        screen.blit(start_screen_image, (WIDTH - start_screen_image.get_width() - 50, HEIGHT // 2 - start_screen_image.get_height() // 4))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_screen()
