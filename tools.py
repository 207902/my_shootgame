import os,pygame
import constants as c
class Startup():
	def __init__(self):
		pass
class Draw_text():
    def __init__(self,screen):
        self.bomb_image = c.images['bomb']
        self.life_image = pygame.transform.scale(c.images['hero1'],(50,50))
        self.bomb_rect = self.bomb_image.get_rect()
        self.life_rect = self.life_image.get_rect()
        self.bomb_font = c.bomb_font

        self.score_font = c.score_font
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
    def update(self, bomb_num,life_num, score):
        self.bomb_num = bomb_num
        # bomb
        self.bomb_text=self.bomb_font.render("x %d" % self.bomb_num, True, 'WHITE')
        self.text_rect=self.bomb_text.get_rect()
        self.screen.blit(self.bomb_image, (10, self.screen_rect.height - 10 - self.text_rect.height))
        self.screen.blit(self.bomb_text, (20+self.bomb_rect.width, self.screen_rect.height-5-self.text_rect.height))
        # 绘制生命数量
        for i in range(life_num):
            self.screen.blit(self.life_image, (self.screen_rect.width - (i+1)*self.life_rect.width, 
                                               self.screen_rect.height- self.life_rect.height))
        life_text = self.score_font.render("Infinite x ", True, 'WHITE')
        self.screen.blit(life_text, (self.screen_rect.width - 3*self.life_rect.width-life_text.get_rect().width, 
                                    self.screen_rect.height-40))
        # 绘制分数
        score_text = self.score_font.render("Score : %s" % str(score), True, 'WHITE')
        self.screen.blit(score_text, (10, 5))
'''

private functions
'''
def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    sounds = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            sounds[name] = pygame.mixer.Sound(os.path.join(directory, fx))
            sounds[name].set_volume(0.2)
    return sounds

def read_pack_file(directory):
	file = open(os.path.join(directory,'image/shoot.pack'),'r')
	lines = file.readlines()
	index = 1
	list={}
	for line in lines:
		if index>5:
			i = (index-5) % 7
			if i == 1:
				name = line.strip()
			elif i ==3:
				begin = line.find(":")
				str = line[begin+1:].strip('\n').split(',')
				x,y = int(str[0]),int(str[1])
			elif i== 4:
				begin = line.find(":")
				str = line[begin+1:].strip('\n').split(',')
				width,height = int(str[0]),int(str[1])
			elif i==5:
				list[name]=[(x,y),(width,height)]			
		index += 1
    #file.close()
	return list

def load_all_images(directory):
	#self.directory=directory
	list=read_pack_file(directory)
	images={}
	shoot_img = pygame.image.load('resources/image/shoot.png')
	for name, value in list.items():
		images[name]=shoot_img.subsurface(pygame.Rect(value))
	return images