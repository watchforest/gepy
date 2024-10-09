import pygame
from game.button import Button
from game.config import WIDTH, HEIGHT, BLACK, WHITE
from game.styles import game_font

class PauseMenu:
    def __init__(self, resume_action, settings_action, exit_action):
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = HEIGHT // 2 - (3 * button_height + 2 * button_spacing) // 2

        self.resume_button = Button("Resume", WIDTH // 2 - button_width // 2, start_y, button_width, button_height, resume_action)
        self.settings_button = Button("Settings", WIDTH // 2 - button_width // 2, start_y + button_height + button_spacing, button_width, button_height, settings_action)
        self.exit_button = Button("Exit", WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, exit_action)
        self.buttons = [self.resume_button, self.settings_button, self.exit_button]
        self.font = game_font(74)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_for_input(mouse_pos)

    def draw(self, screen):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # black with 50% opacity
        screen.blit(overlay, (0, 0))

        # Draw "Paused" text
        paused_text = self.font.render("Paused", True, WHITE)
        screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 4))

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)