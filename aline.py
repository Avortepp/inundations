import sys
from time import sleep
import pygame
from game_stats import GameStats
from setting import Settings 
from ship import Ship
from bullet import Bullet
from  line import Alien

class AlienInvasion:
    def __init__(self):
       pygame.init()
       self.setting = Settings()
       self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
       self.setting.screen_width = self.screen.get_rect().width
       self.setting.screen_height = self.screen.get_rect().height
       pygame.display.set_caption("Alien Invasion")
       self.stats = GameStats(self)

       self.background = pygame.image.load(self.setting.background_image).convert()  
       self.ship = Ship(self)
       self.bullets = pygame.sprite.Group()
       self.line = pygame.sprite.Group()
       self._create_fleet()

    def run_game(self):

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_line()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))
            self._update_screen()
    def _update_line(self):
          self._check_fleet_edges()
          self.line.update()
          if pygame.sprite.spritecollideany(self.ship, self.line):
                self._ship_hit()
          self._check_line_bottom()
    def _check_fleet_edges(self):
            for aline in self.line.sprites():
                if aline.check_edges():
                    self._change_fleet_direction()
                    break  
    def _change_fleet_direction(self):
            for alien in self.line.sprites():
                alien.rect.y += self.setting.fleet_drop_speed
            self.setting.fleet_direction *= -1    

            
    def _check_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    def _check_keydown_events(self, event):
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_LEFT:
                         self.ship.moving_left = True
                    elif event.key == pygame.K_UP:
                         self.ship.moving_up = True
                    elif event.key == pygame.K_DOWN:
                         self.ship.moving_down = True
                    elif event.key == pygame.K_q:
                          sys.exit()
                    elif event.key == pygame.K_SPACE:
                          self._fire_bullet()
    def _check_keyup_events(self, event):
                        if event.key == pygame.K_RIGHT:
                              self.ship.moving_right = False
                        elif event.key == pygame.K_LEFT:
                             self.ship.moving_left = False
                        elif event.key == pygame.K_UP:
                            self.ship.moving_up = False
                        elif event.key == pygame.K_DOWN:
                             self.ship.moving_down = False
    def _fire_bullet(self):
        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
            collision = pygame.sprite.groupcollide(self.bullets, self.line, True,True)
            if not self.line:
              self.bullets.empty()
              self._create_fleet()
           
    def _update_screen(self):
            self.screen.blit(self.background, (0, 0))  # Рисование изображения фона
            #self.screen.fill(self.setting.bg_color)
            #self.screen.fill(self.setting.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.line.draw(self.screen)
 
            pygame.display.flip()
    
    def _create_fleet(self):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            ship_height = self.ship.rect.height
            available_space_x = self.setting.screen_width - (2 * alien_width)
            available_space_y = self.setting.screen_height - ship_height - (2 * alien_height)
            number_aliens_x = available_space_x // (2 * alien_width)
            number_rows = available_space_y // (2 * alien_height)
            for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                    self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.line.add(alien)
    def _ship_hit(self):
          if self.stats.ships_left > 0:
                self.stats.ships_left -= 1
                self.line.empty()
                self.bullets.empty()
                self._create_fleet()
                self.ship.center_ship()
                sleep(0.5)
          else:
                self.stats.game_active = False
    def _check_line_bottom(self):
          screen_rect = self.screen.get_rect()
          for alien in self.line.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                      self._ship_hit()
                      break


                
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

