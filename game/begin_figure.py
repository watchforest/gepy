import pygame

class BeginFigure:
    def __init__(self, image_path, position, screen):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (600, 600))  # Adjust size as needed
        self.position = position
        self.screen = screen
        self.alpha = 0  # Start with fully transparent
        self.text = "Welcome to GE.PY!!! Press a key to begin"
        self.displayed_text = ""
        self.text_index = 0
        self.typing_speed = 1  # Control the speed of the text appearing
        self.typing_counter = 0
        self.font = pygame.font.Font(None, 36)
        self.bubble_width = 300
        self.bubble_height = 150
        self.button_font = pygame.font.Font(None, 48)
        self.button_color = (255, 0, 0)
        self.button_hover_color = (200, 0, 0)
        self.button_text_color = (255, 255, 255)
        self.button_rect = pygame.Rect(position[0] + 50, position[1] + 250, 200, 50)
        self.show_button = False

    def fade_in(self, speed=14):
        """Gradually increase the alpha value to fade in the image."""
        if self.alpha < 255:
            self.alpha += speed
            self.image.set_alpha(self.alpha)

    def update_text(self):
        """Update the text display to simulate typing."""
        if self.text_index < len(self.text):
            self.typing_counter += 1
            if self.typing_counter % self.typing_speed == 0:
                self.displayed_text += self.text[self.text_index]
                self.text_index += 1
        else:
            self.show_button = True  # Show the button when typing is complete

    def draw_speech_bubble(self):
        """Draw a speech bubble connected to the image."""
        bubble_x = self.position[0] + self.image.get_width() // 2 - self.bubble_width // 2
        bubble_y = self.position[1] - self.bubble_height - 10
        pygame.draw.rect(self.screen, (255, 255, 255), (bubble_x, bubble_y, self.bubble_width, self.bubble_height), 0)
        pygame.draw.rect(self.screen, (0, 0, 0), (bubble_x, bubble_y, self.bubble_width, self.bubble_height), 2)

        # Draw the text inside the bubble with word wrapping
        lines = []
        words = self.displayed_text.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            text_width, text_height = self.font.size(test_line)
            if text_width < self.bubble_width - 20:  # Adjust for padding inside the bubble
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  # Add the last line

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (bubble_x + 10, bubble_y + 10 + i * text_height))

    def draw(self):
        """Draw the image and speech bubble on the screen."""
        self.fade_in()  # Apply the fade-in effect
        self.screen.blit(self.image, self.position)

        if self.alpha >= 255:
            self.update_text()  # Start typing text after image is fully displayed
            self.draw_speech_bubble()  # Draw the speech bubble and the text
