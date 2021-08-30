import pygame
from random import randint
import constants as c

# 提供超级子弹的补给
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self):
        super(BulletSupply, self).__init__()
        self.height = c.SCREEN_HEIGHT
        self.image = c.images['ufo1']
        self.rect = self.image.get_rect()
        self.rect.topleft = [randint(0, (c.SCREEN_WIDTH - self.rect.width)),
                                -self.rect.height]

        self.speed = 3
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
    # 定义移动的方法
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active=False

    def reset(self):
        self.active = True
        self.rect.topleft = [randint(0, (c.SCREEN_WIDTH - self.rect.width)),
                                -self.rect.height]

# 提供炸弹的补给
class BombSupply(pygame.sprite.Sprite):
    def __init__(self):
        super(BombSupply, self).__init__()
        self.height = c.SCREEN_HEIGHT
        self.image = c.images['ufo2']
        self.rect = self.image.get_rect()
        self.rect.topleft = [randint(0, (c.SCREEN_WIDTH - self.rect.width)),
                             -self.rect.height]
        self.speed = 3
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
    # 定义移动的方法
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active=False

    def reset(self):
        self.active = True
        self.rect.topleft = [randint(0, (c.SCREEN_WIDTH - self.rect.width)),
                                -self.rect.height]