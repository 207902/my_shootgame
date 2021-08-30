import pygame, os
import tools
projectPath=os.path.abspath('.')
directory = os.path.join(projectPath, "resources")

# 初始化游戏
pygame.init()                                      # 初始化pygame
SCREEN_SIZE = SCREEN_WIDTH,SCREEN_HEIGHT=(480,750)# 定义窗口的分辨率
screen = pygame.display.set_mode(SCREEN_SIZE)     # 初始化窗口
pygame.display.set_caption('飞机大战外卖员')       # 设置窗口标题
# 载入背景图
background = pygame.image.load(os.path.join(directory,'image/background.png'))
images = tools.load_all_images(directory)
#背景音乐加载
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(directory,'sound/game_music.ogg'))
pygame.mixer.music.set_volume(0.1)
sounds = tools.load_all_sfx(os.path.join(directory,'sound'))
# font
bomb_font = pygame.font.Font(os.path.join(directory,'font/font.ttf'), 48)
score_font = pygame.font.Font(os.path.join(directory,'font/font.ttf'), 24)
#画面帧率
frame_rate = 60
animate_cycle = 30 
#生命管理
life_num = 3 
bomb_num = 3
medium_enemy_energy = 10
big_enemy_energy =20
enemy_num_lv1=[10,4, 2]#敌人数量'small' ,'medium','big'
#分值
small_score = 500
medium_score = 1000
big_score = 2000
#图片大小调整
hero_width =100
hero_surface = [pygame.transform.scale(images['hero1'],(hero_width,hero_width)),
				pygame.transform.scale(images['hero2'],(hero_width,hero_width))]
#动画管理
medium_enemyplane=[images['enemy2'],
                   images['enemy2']]
Big_enemyPlane=[images['enemy3_n1'],
                images['enemy3_n2']]				
enemy1_down_surface =[images['enemy1_down1'],
					  images['enemy1_down2'],
					  images['enemy1_down3'],
					  images['enemy1_down4']]
enemy2_down_surface =[images['enemy2_down1'],
					  images['enemy2_down2'],
					  images['enemy2_down3'],
					  images['enemy2_down4']]
enemy3_down_surface =[images['enemy3_down1'],
                      images['enemy3_down2'],
                      images['enemy3_down3'],
                      images['enemy3_down4'],
                      images['enemy3_down5'],
                      images['enemy3_down6']]
#暂停管理
pause_nor_image=images['game_pause_nor']
pause_pressed_image=images['game_pause_pressed']
resume_nor_image=pygame.image.load(os.path.join(directory,'image/resume_nor.png')).convert_alpha()
resume_pressed_image=pygame.image.load(os.path.join(directory,'image/resume_pressed.png')).convert_alpha()
pause_rect=pause_nor_image.get_rect()
#paused_blank=shoot_img.subsurface([(673, 0), (60, 45)])
