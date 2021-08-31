#-*- coding: utf-8 -*-
import pygame ,os
from pygame.sprite import Group
from pygame.locals import * 
from sys import exit  
from random import randint, choice
#自文件导入
import constants as c
from  myplane import Hero
#import bullet
import enemy
import tools
import supply
#字典对移动的控制
offset = {pygame.K_LEFT:0,
          pygame.K_RIGHT:0,
          pygame.K_UP:0,
          pygame.K_DOWN:0}

screen=c.screen
background = c.background
#导入音效文件
sounds = c.sounds 
# 载入资源图片
images = c.images
# 标志是否暂停游戏
paused = False
paused_image = c.pause_nor_image
paused_rect=paused_image.get_rect()
paused_rect.topleft=(c.SCREEN_WIDTH - paused_rect.width - 10,10)
# 生成敌方精灵组
enemy_down_group = Group()
enemyPlanes = Group()
smallEnemyPlanes = Group()
mediumEnemyPlanes = Group()
bigEnemyPlanes = Group()
enemy_group=[smallEnemyPlanes,
             mediumEnemyPlanes,
             bigEnemyPlanes,
             enemyPlanes]

#基本计数
bomb_num = c.bomb_num
life_num = c.life_num
score = 0
#事件定义
SUPPLY_TIME=USEREVENT
# 超级子弹定时器
SUPER_BULLET_TIME = USEREVENT + 1
# 复活时无敌的计时器
IS_NOT_DEAD_TIME=USEREVENT+2
# 标志是否使用超级子弹
isSuperBullet = False
# 不会停下的超级子弹
isSuperBulletNotStop = False
# 设置是否处于无敌(不会死)状态
isNotDead=False
isHoldFire=False
#print(paused_rect,c.paused_blank.get_rect())
def set_paused(paused):	
    if paused:
        pygame.time.set_timer(SUPPLY_TIME, 0)
        pygame.mixer.music.pause()
        pygame.mixer.pause()
        paused_image = c.resume_nor_image            
    else:
        pygame.time.set_timer(SUPPLY_TIME, 10*1000)
        pygame.mixer.music.unpause()
        pygame.mixer.unpause()
        paused_image = c.resume_nor_image
        paused_image = c.pause_nor_image
    return paused_image
def inc_speed(target, inc):
    for plane in target:
        plane.speed+=inc
#初始界面
game_init=tools.Startup()
game_init.wait_for_press()
#text
text_draw = tools.Draw_text(screen)
#画面帧率
clock = pygame.time.Clock()
ticks = 0
#玩家创建,碰撞组
hero =  Hero()
# 天降百宝箱,每30秒发放一个补给包，分别是炸弹和超级子弹
bulletSupply=supply.BulletSupply()
bombSupply=supply.BombSupply()
pygame.time.set_timer(SUPPLY_TIME, 10*1000)
pygame.mixer.music.play(-1)
# 事件循环(main loop)
while True:
    
    clock.tick(c.frame_rate)
    ticks += 1
    if ticks >= c.animate_cycle:
        ticks=0         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_q:
                exit()
            if event.key == K_p:
                paused = not paused
                paused_image=set_paused(paused)
            elif event.key == K_b:
                isSuperBulletNotStop = not isSuperBulletNotStop
            elif event.key == K_n:
                isNotDead = not isNotDead
            elif event.key == K_h:
                isHoldFire = not isHoldFire
            elif event.key in [K_SPACE, K_v]:
                bomb_trigger=False
                if event.key == K_v:
                    bomb_trigger=True
                if not bomb_trigger and bomb_num:
                    bomb_num -= 1
                    bomb_trigger=True
                if bomb_trigger:
                    if not paused:
                        sounds['use_bomb'].play()
                        # 清屏中的敌机
                        for plane in enemyPlanes:
                            if plane.rect.bottom > 0:
                               score += plane.score
                               plane.kill()
        # 控制方向
            elif event.key in offset:
                if not paused:
                    offset[event.key] = 3
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0
        elif event.type == MOUSEBUTTONDOWN:
            if event.button==1 and paused_rect.collidepoint(event.pos):
                paused = not paused
                paused_image=set_paused(paused)
                
        elif event.type == MOUSEMOTION:
            if paused_rect.collidepoint(event.pos):
                if paused:
                    paused_image = c.resume_pressed_image
                else:
                    paused_image = c.pause_pressed_image
            else:
                if paused:
                    paused_image = c.resume_nor_image
                else:
                    paused_image = c.pause_nor_image
                    
        elif event.type == SUPPLY_TIME:
            sounds['supply'].play()
            if choice([True,False]):
                bulletSupply.reset()
            else:
                bombSupply.reset()

        elif event.type == SUPER_BULLET_TIME:
            isSuperBullet=False
            pygame.time.set_timer(SUPER_BULLET_TIME, 0)

        elif event.type == IS_NOT_DEAD_TIME:
            isNotDead = False
            pygame.time.set_timer(IS_NOT_DEAD_TIME, 0)
    if paused:
        pygame.draw.rect(screen,(200,200,200),paused_rect)
        #screen.blit(background,paused_rect)
        screen.blit(paused_image,paused_rect)
        pygame.display.update()
    else:
        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制动画
        hero.update(ticks)
        hero.move(offset)
        #绘制子弹
        if not isHoldFire:
            if ticks % 10 == 0 :
                hero.fire(isSuperBullet,isSuperBulletNotStop)
            hero.myfires.update()
            hero.myfires.draw(screen)
        
        #绘制敌机,控制密度
        if ticks % 30 == 0:
            for i in range(3):
                diff=c.enemy_num_lv1[i]-len(enemy_group[i])
                if diff>0:
                    for e in range(diff):
                        if i==0:
                            enemyplane = enemy.SmallEnemyPlane()
                        elif i==1:
                            enemyplane = enemy.MediumEnemyPlane()
                        elif i==2:
                            enemyplane = enemy.BigEnemyPlane()
                        #enemyplane = enemy_class[i]
                        enemy_group[i].add(enemyplane)
                        enemy_group[3].add(enemyplane)
     
        screen.blit(hero.image, hero.rect)
        bigEnemyPlanes.update(screen, ticks)
        mediumEnemyPlanes.update(screen,ticks)
        smallEnemyPlanes.update(screen,ticks)


        #检测碰撞
        enemy_down_group.add(pygame.sprite.groupcollide(enemyPlanes,
                                                         hero.myfires, False, True))
        for plane in enemy_down_group:
            if plane in mediumEnemyPlanes or plane in bigEnemyPlanes:
                plane.hit=True
                plane.energy -= 1
                enemy_down_group.remove(plane)
            else:
                plane.active = False
            if (not plane.active) and plane.count:
                score += plane.score
                plane.count = False
        # 检测我方飞机是否被撞
        hero_down = pygame.sprite.spritecollide(hero, enemyPlanes, False, pygame.sprite.collide_mask)
        if hero_down:
            if not isNotDead:
                sounds['me_down'].play()
                hero.kill()
                hero= Hero()
                if life_num>0:
                    life_num -= 1
            for e in hero_down:
                score += e.score
                e.kill()
        # 绘制炸弹补给并检测是否获得
        if bombSupply.active:
            bombSupply.move()
            screen.blit(bombSupply.image,bombSupply.rect)
            if pygame.sprite.collide_mask(bombSupply,hero):
                sounds['get_bomb'].play()
                bomb_num += 1
                bombSupply.active = False

        # 绘制超级子弹补给并检测是否获得
        if bulletSupply.active:
            bulletSupply.move()
            screen.blit(bulletSupply.image, bulletSupply.rect)
            if pygame.sprite.collide_mask(bulletSupply, hero):
                sounds['get_bullet'].play()
                # 发射超级子弹
                isSuperBullet=True
                pygame.time.set_timer(SUPER_BULLET_TIME, 10*1000)
                bulletSupply.active = False 
        # 绘制全屏炸弹数量
        text_draw.update(bomb_num,life_num, score)          
        # 更新屏幕
        screen.blit(paused_image,paused_rect)
        pygame.display.update()
        