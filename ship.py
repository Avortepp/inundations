import pygame
class Ship():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("korabll.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.center
        

        self.scale_factor = 0.2  # Фактор масштабирования
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * self.scale_factor), int(self.rect.height * self.scale_factor)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.center
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        if self.moving_right:
            self.rect.x += 1#self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left:
            self.rect.x -= 1 #self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        elif self.moving_up:
            self.rect.x = 1
        if self.moving_up and self.rect.top > 0:
           self.rect.y -= self.settings.ship_speed
        elif self.moving_down:
            self.rect.x = 1
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
           self.rect.y += self.settings.ship_speed
        
        self.rect.x = self.x
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)