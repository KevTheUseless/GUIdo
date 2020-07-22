# kernel.py
# Core of our OS

import pygame, sys, random
from enum import Enum

width, height = 1024, 768

def drawByte(screen, data, colorList, x0, y0, dw, scale):
	for dy in range(dw):
		line = data[dy]
		for dx in range(len(data)):
			c = colorList[line & 1]
			tx = x0 + (dw - dx - 1) * scale
			ty = y0 + dy * scale
			if scale > 1:
				pygame.draw.rect(screen, c, (tx, ty, scale, scale), 0)
			else:
				screen.set_at((tx, ty), c)
			line >>= 1
	return

def convert(fileName):
	try:
		f = open(fileName, "r")
		dataList = f.readline().split()
		f.close()
	except:
		print("File not found!")
		pygame.quit()
		sys.exit()
	converted = []
	for i in dataList:
		converted.append(int(i, 16))
	return converted

def process(data, colorList, dw, scale):
	img = pygame.Surface((dw * scale, dw * scale))
	drawByte(img, data, colorList, 0, 0, dw, scale)
	return img

class Pic(object):
	def __init__(self, fileName):
		img = pygame.image.load(fileName)
		self.img = pygame.transform.scale(img, (width, height))
		self.x, self.y = 0, 0
		self.w, self.h = self.img.get_size()
	def draw(self, screen, speed = 5):
		screen.blit(self.img, (self.x, self.y), (0, 0, self.w, self.h))
		pygame.draw.rect(screen, (0, 255, 0), (0, 0, speed * 8, 8), 0)
	def getPixelGrid(self, x0, y0, sideLen, pixelGrid):
		n = sideLen // 2
		for y in range(-n, n + 1):
			for x in range(-n, n + 1):
				pixelGrid[y + n][x + n] = self.img.get_at((x + x0, y + y0))

class Kernel:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Windows 95 Simulated")
		self.clock = pygame.time.Clock()
		self.font32 = pygame.font.Font("res/segoeui.ttf", 32)
		self.speed = 5
		self.mousePos = (0, 0)
		self.apps = []
		self.appID = 0
	def launch(self):
		for app in self.apps:
			app.draw(self.screen)
		pygame.display.update()
		self.clock.tick(50)
	def addApp(self, app):
		app.appID = len(self.apps)
		self.apps.append(app)
	# TODO: Add KEYUP/KEYDOWN support
	def keyUp(self, key):
		return
	def keyDown(self, key):
		return
	def mouseDown(self, pos, button):
		self.apps[self.appID].mouseDown(pos, button)
		print(event.pos)
	def mouseUp(self, pos, button):
		self.apps[self.appID].mouseUp(pos, button)
	def mouseMotion(self, pos):
		self.apps[self.appID].mouseMotion(pos)

class App:
	def __init__(self, picName):
		self.pic = Pic(picName)
		self.appID = 0
		self.btnList = []
		self.txtList = []
		self.secretList = []
	def draw(self, screen):
		if framework.appID != self.appID:
			return
		screen.blit(self.pic.img, (0, 0))
		for button in self.btnList:
			button.draw(screen)
		for txt in self.txtList:
			txt.draw(screen)
	def addButton(self, b):
		self.btnList.append(b)
	def addTxt(self, txt, font, x, y, c, rect):
		t = Txt(txt, font, x, y, c, rect)
		self.txtList.append(t)
	def mouseDown(self, pos, button):
		for btn in self.btnList:
			btn.mouseDown(pos, button)
		for secret in self.secretList:
			secret.mouseDown(pos, button)
	def mouseUp(self, pos, button):
		for button in self.btnList:
			button.mouseUp(pos, button)
	def mouseMotion(self, pos):
		framework.mousePos = pos
		for btn in self.btnList:
			btn.mouseMove(pos)
	def keyUp(self, button):
		framework.keyUp(button)
	def keyDown(self, button):
		framework.keyDown(button)

class Button:
	def __init__(self, name, picFile, x, y, appID, **txt):
		self.name = name
		self.img = pygame.image.load(picFile).convert()
#		self.img.set_colorkey(pygame.Color(0, 255, 0))
		self.w, self.h = self.img.get_width() // 3, self.img.get_height()
		self.x, self.y = x, y
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.status = 0
		self.appID = appID
		self.txt = txt
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y),
					(self.status * self.rect.w, 0,
					 self.rect.w, self.rect.h))
		if self.txt:
			screen.blit(self.txt["font"].render(self.txt["content"], True, (0,0,0)), \
			            (self.x + self.w // 2 - 4 * len(self.txt["content"]), self.y + self.h // 2 - 8))
	def mouseDown(self, pos, button):
		if self.rect.collidepoint(pos):
			self.status = 2
	def mouseUp(self, pos, button):
		self.status = 0
		if not self.rect.collidepoint(pos):
			return
		if self.name == 'U':
			framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
		if self.name == 'D':
			framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
		if self.name == 'L':
			framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
		if self.name == 'R':
			framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
		framework.appID = self.appID

	def mouseMove(self, pos):
		if self.rect.collidepoint(pos):
			self.status = 1
		else:
			self.status = 0

class Txt:
	def __init__(self, txt, font, x, y, c, rect):
		self.txt = txt
		self.img = font.render(txt, True, c)
		self.x, self.y = x, y
		self.c = c
		self.rect = pygame.Rect(rect)
	def draw(self, screen):
		if self.rect.collidepoint(framework.mousePos):
			screen.blit(self.img, (self.x, self.y))

class DlgStatus(Enum):
	INFO = 0
	WARNING = 1
	ERROR = 2

class Dialog(object):
	def __init__(self, title, content, scale, status = DlgStatus.INFO):
		self.title = title
		self.icon = pygame.image.load("res/dialog/" + str(status) + ".png")
		self.content = content
		self.scale = scale
	def draw(self, screen):
		pass

framework = Kernel()
bg = App("res/clouds.jpg")
term = App("res/term.jpg")
framework.appID = bg.appID
framework.addApp(bg)
framework.addApp(term)
raster = pygame.font.Font("res/vga936.fon", 32)
bg.addButton(Button('U', "res/button/txt_btn.bmp", width // 2 - 35, 20, term.appID, font=raster, content="TERMINAL"))
term.addButton(Button('D', "res/button/txt_btn.bmp", width // 2 - 35, 20, bg.appID, font=raster, content="CLOSE"))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			framework.keyDown(event.key)
		elif event.type == pygame.KEYUP:
			framework.keyUp(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN:
			framework.mouseDown(event.pos, event.button)
		elif event.type == pygame.MOUSEBUTTONUP:
			framework.mouseUp(event.pos, event.button)
		elif event.type == pygame.MOUSEMOTION:
			framework.mouseMotion(event.pos)
	framework.launch()