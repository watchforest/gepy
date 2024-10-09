import pygame
import os
from game.styles import game_font, base_dir

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.music = {}

    def load_image(self, name, file_name):
        if name not in self.images:
            try:
                image_path = os.path.join(base_dir, 'assets', 'images', file_name)
                image = pygame.image.load(image_path).convert_alpha()
                self.images[name] = image
            except pygame.error as e:
                print(f"Unable to load image: {file_name}")
                print(e)
                return None
        return self.images[name]

    def load_sound(self, name, file_name):
        if name not in self.sounds:
            try:
                sound_path = os.path.join(base_dir, 'assets', 'sounds', file_name)
                sound = pygame.mixer.Sound(sound_path)
                self.sounds[name] = sound
            except pygame.error as e:
                print(f"Unable to load sound: {file_name}")
                print(e)
                return None
        return self.sounds[name]

    def load_music(self, name, file_name):
        if name not in self.music:
            try:
                music_path = os.path.join(base_dir, 'assets', 'music', file_name)
                self.music[name] = music_path
            except pygame.error as e:
                print(f"Unable to load music: {file_name}")
                print(e)
                return None
        return self.music[name]

    def play_music(self, name):
        if name in self.music:
            pygame.mixer.music.load(self.music[name])
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = game_font(size)
        return self.fonts[size]

    def scale_image(self, name, scale):
        if name in self.images:
            original = self.images[name]
            scaled_size = (int(original.get_width() * scale), int(original.get_height() * scale))
            return pygame.transform.scale(original, scaled_size)
        return None