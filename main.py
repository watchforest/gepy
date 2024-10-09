import pygame
import sys
from game.start_screen import start_screen
from game.config import WIDTH, HEIGHT, TITLE


def main():
    # Initialize Pygame
    pygame.init()

    # Setup the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.display.set_caption(TITLE)

    # Setup clock for controlling game speed
    clock = pygame.time.Clock()

    # Start the game
    start_screen(screen, clock)

    # Quit game when start_screen returns
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()