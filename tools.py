import os,pygame
from sys import exit
import constants as c
class Startup():
	def __init__(self):
		self.screen = c.screen
		self.screen_rect = self.screen.get_rect()
		self.copyright=c.bg_images['shoot_copyright']
		self.copyright_rect = self.copyright.get_rect()
		self.copyright_rect.centerx=self.screen_rect.centerx
		self.copyright_rect.y=20
		self.game_loading=c.bg_images['game_loading1']
		self.loading_rect = self.game_loading.get_rect()
		self.loading_rect.centerx = self.screen_rect.centerx
		self.loading_rect.y= 300
		self.num =1
		self.animate_tick=0
		self.font=pygame.font.Font(os.path.join(c.directory,'font/kumo.ttf'), 24)
		self.big_font=pygame.font.Font(os.path.join(c.directory,'font/kumo.ttf'), 36)
		self.text1='ENTER to start this fun game'
		self.text2='N:无敌   V:全屏炸弹  B:超级子弹  空格: 炸弹'
		self.text3='P:暂停   H:停火     M:静音        Q: 退出'
		self.text4='Last, Good Luck!'
		
	def update(self):
		clock=pygame.time.Clock()
		clock.tick(60)
		if self.animate_tick % 30 == 0:
			self.game_loading=c.bg_images['game_loading'+str(self.num)]
			if self.num < 4:
				self.num += 1
			else:
				self.num = 1
			self.screen.blit(c.bg_images['background'],(0,0))
			self.screen.blit(self.game_loading,self.loading_rect)
			self.screen.blit(self.copyright,self.copyright_rect)
			pygame.draw.rect(self.screen,'green',(0,390,c.SCREEN_WIDTH,200),3)
			txt1=self.big_font.render(self.text1,True, 'blue')
			txt2=self.font.render(self.text2,True, 'black')
			txt3=self.font.render(self.text3,True, 'black')
			txt4=self.big_font.render(self.text4,True, 'red')
			txt=[txt1,txt2,txt3,txt4]
			for i in range(4):
				rect = txt[i].get_rect()
				rect.centerx = self.screen_rect.centerx
				rect.y = 400+45*i
				self.screen.blit(txt[i],rect)
			#self.screen.blit(c.bg_images['btn_finish'],(0,400))
			pygame.display.update()
			
	def wait_for_press(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						return
					elif event.key == pygame.K_q:
						pygame.quit()
						exit()
			if self.animate_tick < 300: 
				self.animate_tick += 1
			else:
				self.animate_tick =0
			self.update()

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

def read_pack_file(file_path):
	file = open(file_path,'r')
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

def load_all_images(directory,file_name):
	pack= os.path.join(directory,'image/'+file_name+'.pack')
	img_name=os.path.join(directory,'image/'+file_name+'.png')
	list=read_pack_file(pack)
	images={}
	shoot_img = pygame.image.load(img_name)
	for name, value in list.items():
		images[name]=shoot_img.subsurface(pygame.Rect(value))
	return images