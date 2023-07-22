import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.setting
        self.image = pygame.image.load('adi.png')
        self.rect = self.image.get_rect()

        self.scale_factor = 0.3 # Фактор масштабирования
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * self.scale_factor), int(self.rect.height * self.scale_factor)))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update(self):
        self.x += (self.settings.line_speed*self.settings.fleet_direction)
        self.rect.x = self.x 
    