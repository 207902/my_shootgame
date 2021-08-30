import pygame
import constants as c
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_init_pos):
        super(Bullet, self).__init__()
        self.image= c.images['bullet1']
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 8
    def update(self):
        self.rect.top -= self.speed
        if self.rect.top < - self.rect.height:
            self.kill()

class Super_bullet(Bullet):
    def __init__(self, bullet_init_pos):
        super(Super_bullet,self).__init__(bullet_init_pos)
        self.image =c.images['bullet2']
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 20