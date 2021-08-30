import pygame
import constants as c
import bullet
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super(Hero, self).__init__()
        self.hero_surface = c.hero_surface
        self.rect = self.hero_surface[0].get_rect()
        self.rect.centerx = c.SCREEN_WIDTH//2
        self.rect.y = c.SCREEN_HEIGHT
        self.speed = 10

        self.myfires = pygame.sprite.Group()
    def update(self,ticks):
        self.image = self.hero_surface[ticks//(c.animate_cycle//2)]
    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT]-offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN]-offset[pygame.K_UP]
        if x < 0:
            self.rect.left = 0
        elif x > c.SCREEN_WIDTH - self.rect.width:
            self.rect.left = c.SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
        if y <0:
            self.rect.top= 0
        elif y > c.SCREEN_HEIGHT - self.rect.height:
            self.rect.top = c.SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y
    def fire(self, isSuperBullet,isSuperBulletNotStop):
        c.sounds['bullet'].play()
        if isSuperBulletNotStop or isSuperBullet:
            # 同时射五发
            self.myfires.add(bullet.Super_bullet(self.rect.midtop))
            self.myfires.add(bullet.Super_bullet((self.rect.centerx - 33, self.rect.centery)))
            self.myfires.add(bullet.Super_bullet((self.rect.centerx - 58, self.rect.centery)))
            self.myfires.add(bullet.Super_bullet((self.rect.centerx + 30, self.rect.centery)))
            self.myfires.add(bullet.Super_bullet((self.rect.centerx + 55, self.rect.centery)))
        else:
            self.myfires.add(bullet.Bullet(self.rect.midtop))