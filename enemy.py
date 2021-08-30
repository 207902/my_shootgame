import pygame
import constants as c
from random import randint
class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyPlane, self).__init__()
        self.sounds = c.sounds
        self.images = c.images
        self.screen_height = c.SCREEN_HEIGHT
        self.active = True
        self.down_index = 0
        self.down_finished = False
        self.animate_cycle=c.animate_cycle
        self.count = True
        self.y = 0.00
    def move(self):
        if self.rect.top < self.screen_height:
            self.y = float(self.rect.top)
            self.y += self.speed
            self.rect.top =self.y
        else:
            self.kill()
class SmallEnemyPlane(EnemyPlane):
    def __init__(self):
        super(SmallEnemyPlane,self).__init__()
        self.image = self.images['enemy1']
        self.rect = self.image.get_rect()
        self.rect.topleft = [randint(0, c.SCREEN_WIDTH-self.rect.width),
                             randint(-5*self.rect.height,0)]
        self.speed = 2
        self.down_surface = c.enemy1_down_surface
        self.down_num = len(self.down_surface)-1
        self.score = c.small_score
    def update(self,screen,ticks):
        self.move()
        if self.active:
            screen.blit(self.image, self.rect)
        else: 
            if self.down_index == 0: 
                self.sounds['enemy1_down'].play()
            screen.blit(self.down_surface[self.down_index], self.rect)
            if ticks % (self.animate_cycle//2) == 0:
                if self.down_index < self.down_num:
                    self.down_index += 1
                else:  
                    self.kill()
class MediumEnemyPlane(EnemyPlane):
    def __init__(self):
        super(MediumEnemyPlane, self).__init__()
        self.sound = self.sounds['enemy2_down']
        self.image = c.images['enemy2']
        self.rect = self.image.get_rect()
        self.rect.topleft = [randint(0, c.SCREEN_WIDTH-self.rect.width),
                            randint(-2*c.SCREEN_HEIGHT,-self.rect.height)]
        self.mask = pygame.mask.from_surface(self.image)
        self.enemy_surface =c.medium_enemyplane
        self.speed = 1.2
        self.image_hit = c.images['enemy2_hit']
        self.hit = False
        self.energy = c.medium_enemy_energy
        self.full_energy=c.medium_enemy_energy
        self.down_surface = c.enemy2_down_surface
        self.down_num = len(self.down_surface)-1
        self.score = c.medium_score
    def update(self,screen,ticks):
        self.move()
        self.image = self.enemy_surface[ticks//(self.animate_cycle//2)]
        if self.active:
            if not self.hit:
                screen.blit(self.image, self.rect)
            else: 
                screen.blit(self.image_hit, self.rect)
                #血量计算
                energy_remain = self.energy / self.full_energy
                if energy_remain > 0.2:
                    energy_color = 'GREEN'
                else:
                    energy_color = 'RED'
                if self.energy == 0:
                    self.active = False
                # 绘制血槽
                pygame.draw.line(screen, 'BLACK', (self.rect.left, self.rect.top - 5),
                                         (self.rect.right, self.rect.top - 5), 2)
                # 当生命大于20%显示绿色，否则显示红色
                
                pygame.draw.line(screen, energy_color, (self.rect.left, self.rect.top - 5),
                                 (self.rect.left + self.rect.width * energy_remain, self.rect.top - 5), 2)

        else:
            if self.down_index == 0: 
                self.sounds['enemy2_down'].play()
            screen.blit(self.down_surface[self.down_index], self.rect)
            if ticks % (self.animate_cycle//2) == 0:
                if self.down_index < self.down_num:
                    self.down_index += 1
                else:  
                    self.kill()
class BigEnemyPlane(MediumEnemyPlane):
    def __init__(self):
        super(BigEnemyPlane, self).__init__()
        self.sound = self.sounds['enemy3_down']
        self.image = c.images['enemy3_n1']
        self.enemy_surface = c.Big_enemyPlane
        self.rect = self.image.get_rect()
        self.rect.topleft = [randint(0, c.SCREEN_WIDTH-self.rect.width),
                            randint(-3*c.SCREEN_HEIGHT,-c.SCREEN_HEIGHT)]
        self.hit = False
        self.image_hit = c.images['enemy3_hit']
        self.speed = 1
        self.energy = c.big_enemy_energy
        self.full_energy=c.big_enemy_energy
        self.down_surface = c.enemy3_down_surface
        self.down_num = len(self.down_surface)-1
        self.score = c.big_score