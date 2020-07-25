# kernel.py
# Core of our OS

import pygame, sys, random
from enum import Enum

width, height = 1024, 768

def lineWrap(txt, w):
	processed = []
	temp = ""
	for i in range(txt.__len__()):
		if i != 0 and i % w == 0:
			processed.append(framework.raster.render(temp, True, (0, 0, 0)))
			temp = ""
		temp += txt[i]
	processed.append(framework.raster.render(temp, True, (0, 0, 0)))
	return processed

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
		self.raster = pygame.font.Font("res/vga936.fon", 32)
		self.speed = 5
		self.mousePos = (0, 0)
		self.apps = []
		self.appID = 0
		self.dialogs = []
		self.dialogID = 0
	def launch(self):
		for app in self.apps:
			app.draw(self.screen)
		for dialog in self.dialogs:
			try:
				dialog.draw(self.screen)
			except:
				pass
		pygame.display.update()
		self.clock.tick(50)
	def addApp(self, app):
		app.appID = len(self.apps)
		self.apps.append(app)
	def addDialog(self, dialog):
		dialog.dialogID = len(self.dialogs)
		dialog.closeBtn = Secret((dialog.x + 357, dialog.y + 6, 17, 16), dialog.dialogID)
		self.dialogs.append(dialog)
	# TODO: Add KEYUP/KEYDOWN support
	def keyUp(self, key):
		return
	def keyDown(self, key):
		return
	def mouseDown(self, pos, button):
		self.apps[self.appID].mouseDown(pos, button)
		try:
			self.dialogs[self.dialogID].mouseDown(pos, button)
		except:
			pass
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

class Secret:
	def __init__(self, rect, dialogID):
		self.rect = pygame.Rect(rect)
		self.dialogID = dialogID
	def mouseDown(self, pos, button):
		if self.rect.collidepoint(pos):
			framework.dialogs.pop(len(framework.dialogs) - 1)
			print(len(framework.dialogs) - 1)

class DlgStatus(Enum):
	INFO = 0
	WARNING = 1
	ERROR = 2

class Dialog:
	def __init__(self, title, content, status = DlgStatus.INFO):
		self.img = pygame.image.load("res/dialog/dialog.png")
		self.icon = pygame.image.load("res/dialog/" + str(status) + ".bmp")
		self.icon.set_colorkey((255, 255, 255))
		self.title = framework.raster.render(title, True, (255, 255, 255))
		self.content = lineWrap(content, 35)
		self.dialogID = 0
		self.w, self.h = self.img.get_size()
		self.x, self.y = 322, 284
		self.closeBtn = None
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))
		screen.blit(self.title, (self.x + 10, self.y + 6))
		screen.blit(self.icon, (self.x + 30, self.y + 90))
		for i in range(len(self.content)):
			screen.blit(self.content[i], (self.x + 80, self.y + 35 + i * 16))
	def mouseDown(self, pos, button):
		self.closeBtn.mouseDown(pos, button)

framework = Kernel()
bg = App("res/clouds.jpg")
term = App("res/term.jpg")
framework.appID = bg.appID
framework.addApp(bg)
framework.addApp(term)
framework.addDialog(Dialog("Hey there!", "Welcome to our OS emulator! As you can see, line wrap is working perfectly here. Now we just need some art for the icons."))
framework.addDialog(Dialog("Hi!", "Another one"))
bg.addButton(Button('U', "res/button/txt_btn.bmp", width // 2 - 35, 20, term.appID, font=framework.raster, content="TERMINAL"))
term.addButton(Button('D', "res/button/txt_btn.bmp", width // 2 - 35, 20, bg.appID, font=framework.raster, content="CLOSE"))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			framework.keyDown(event.key)
			print(event.key)
		elif event.type == pygame.KEYUP:
			framework.keyUp(event.key)
			print(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN:
			framework.mouseDown(event.pos, event.button)
		elif event.type == pygame.MOUSEBUTTONUP:
			framework.mouseUp(event.pos, event.button)
		elif event.type == pygame.MOUSEMOTION:
			framework.mouseMotion(event.pos)
	framework.launch()