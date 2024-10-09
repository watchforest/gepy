import pygame
import game.styles as colors
from game.styles import game_font
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = colors.WHITE  # Button color is initially WHITE
        self.text_color = colors.BLACK  # Text color is initially BLACK
        self.hovered = False
        self.action = action
        self.font = game_font(74)

    def draw(self, surface):
        # Change button color on hover
        pygame.draw.rect(surface, colors.BLACK if self.hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color if not self.hovered else colors.WHITE)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2+20))

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.action:
                self.action()
        else:
            self.hovered = False