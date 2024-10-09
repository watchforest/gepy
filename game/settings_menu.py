import pygame
from game.button import Button
from game.config import WIDTH, HEIGHT, BLACK, WHITE
from game.styles import game_font


class SettingsMenu:
    def __init__(self, back_action):
        self.font = game_font(48)
        self.title_font = game_font(74)

        # Create sliders for volume control
        self.music_volume = 50
        self.sfx_volume = 50

        # Create a back button
        self.back_button = Button("Back", WIDTH // 2 - 100, HEIGHT - 100, 200, 50, back_action)

        # Initialize Pygame mixer
        pygame.mixer.init()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.back_button.check_for_input(mouse_pos)

            # Check if user is adjusting volume sliders
            self.adjust_volume(mouse_pos)

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button held down
                mouse_pos = pygame.mouse.get_pos()
                self.adjust_volume(mouse_pos)

    def adjust_volume(self, mouse_pos):
        music_slider_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 50, WIDTH // 2, 20)
        sfx_slider_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 20)

        if music_slider_rect.collidepoint(mouse_pos):
            self.music_volume = (mouse_pos[0] - music_slider_rect.x) / music_slider_rect.width * 100
            pygame.mixer.music.set_volume(self.music_volume / 100)
        elif sfx_slider_rect.collidepoint(mouse_pos):
            self.sfx_volume = (mouse_pos[0] - sfx_slider_rect.x) / sfx_slider_rect.width * 100
            pygame.mixer.Channel(0).set_volume(self.sfx_volume / 100)

    def draw(self, screen):
        screen.fill(BLACK)

        # Draw title
        title_text = self.title_font.render("Settings", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Draw volume sliders
        self.draw_slider(screen, "Music Volume", self.music_volume, HEIGHT // 2 - 50)
        self.draw_slider(screen, "SFX Volume", self.sfx_volume, HEIGHT // 2 + 50)

        # Draw back button
        self.back_button.draw(screen)

    def draw_slider(self, screen, label, value, y_pos):
        label_text = self.font.render(label, True, WHITE)
        screen.blit(label_text, (WIDTH // 4 - label_text.get_width() - 20, y_pos))

        pygame.draw.rect(screen, WHITE, (WIDTH // 4, y_pos, WIDTH // 2, 20), 2)
        pygame.draw.rect(screen, WHITE, (WIDTH // 4, y_pos, WIDTH // 2 * value / 100, 20))

        value_text = self.font.render(f"{int(value)}%", True, WHITE)
        screen.blit(value_text, (WIDTH * 3 // 4 + 20, y_pos))

    def save_settings(self):
        # Here you would implement saving settings to a file
        pass

    def load_settings(self):
        # Here you would implement loading settings from a file
        pass