# kernel.py
# Core of our OS

import pygame, sys, random, io
from math import *
from contextlib import redirect_stdout

from enum import Enum

from ls import ls
from rm import rm
from pwd import pwd
from cat import cat
from calc import calc

width, height = 1024, 768

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
		pygame.display.set_caption("Winnux 58")
		self.clock = pygame.time.Clock()
		self.raster = pygame.font.Font("res/Perfect_DOS_VGA_437.ttf", 15)
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
	def keyUp(self, key):
		self.apps[self.appID].keyUp(key)
	def keyDown(self, key):
		self.apps[self.appID].keyDown(key)
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
		self.tooltipList = []
		self.txtField = TxtField(0, 0, 0, 0)
		self.txtFieldEnabled = False
		self.canvas = pygame.Surface((width, height - 60))
		self.canvasEnabled = False
		self.secretList = []
	def draw(self, screen):
		if framework.appID != self.appID:
			return
		screen.blit(self.pic.img, (0, 0))
		for button in self.btnList:
			button.draw(screen)
		for tooltip in self.tooltipList:
			tooltip.draw(screen)
		if self.txtFieldEnabled:
			self.txtField.content = self.txtField.wrap(self.txtField.txtBuffer)
			self.txtField.content = self.txtField.content[-self.txtField.h:]
			self.txtField.draw(screen, self.txtField.content)
		if self.canvasEnabled:
			framework.screen.blit(self.canvas, (0, 60))
	def addButton(self, b):
		self.btnList.append(b)
	def addTooltip(self, txt, font, x, y, c, rect):
		tt = Tooltip(txt, font, x, y, c, rect)
		self.txtList.append(tt)
	def enableTxtField(self, x, y, w, h, placeholder = "/# "):
		if self.canvasEnabled:
			print("Only one of either the text field or the canvas can be enabled in an App.")
			return
		self.txtFieldEnabled = True
		self.txtField.x, self.txtField.y = x, y
		self.txtField.w, self.txtField.h = w, h
		self.txtField.placeholder = placeholder
	def enableCanvas(self):
		if self.txtFieldEnabled:
			print("Only one of either the text field or the canvas can be enabled in an App.")
			return
		self.canvasEnabled = True
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
	def keyUp(self, key):
		if self.txtFieldEnabled:
			self.txtField.keyUp(key)
	def keyDown(self, key):
		if self.txtFieldEnabled:
			self.txtField.keyDown(key)
		if self.canvasEnabled:
			if self.appID == snake.appID:
				pass

class Button:
	def __init__(self, picFile, x, y, appID, **txt):
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
		framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
		framework.appID = self.appID
	def mouseMove(self, pos):
		if self.rect.collidepoint(pos):
			self.status = 1
		else:
			self.status = 0

class Tooltip:
	def __init__(self, txt, font, x, y, c, rect):
		self.txt = txt
		self.img = font.render(txt, True, c)
		self.x, self.y = x, y
		self.c = c
		self.rect = pygame.Rect(rect)
	def draw(self, screen):
		if self.rect.collidepoint(framework.mousePos):
			screen.blit(self.img, (self.x, self.y))

class TxtField:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.pwd = '/'
		self.placeholder = '%s# ' % self.pwd
		self.txtBuffer = []
		self.content = []
		self.caps = { '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z' }
		self.shift, self.capsLock = False, False
		self.raster = pygame.font.Font("res/Perfect_DOS_VGA_437.ttf", 28)
	def wrap(self, txtBuffer):
		lines = []
		temp = self.placeholder
		for i in range(len(txtBuffer)):
			if txtBuffer[i] == '\n':
				lines.append(temp)
				temp = self.placeholder
			elif txtBuffer[i] == '\r':
				temp = ''
				lines.append('')
			elif (i != 0 and i % self.w == 0):
				lines.append(temp)
				temp = ""
			else:
				temp += txtBuffer[i]
		lines.append(temp)
		return lines
	def draw(self, screen, lines, c = (255, 255, 255), y = 0):
		for line in lines:
			img = self.raster.render(line, True, c)
			screen.blit(img, (0, y))
			y += 30

	def exec_cmd(self, on_scr):
		cmd = on_scr.split()
		main = cmd.pop()
		output = io.StringIO()
		with redirect_stdout(output):
			exec("%s('%s', %s)" % (main, self.pwd, str(cmd)))
		self.txtBuffer.append(output.getvalue())

	def keyUp(self, key):
		if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
			self.shift = False
		elif key == pygame.K_CAPSLOCK:
			self.capsLock = 1 - self.capsLock
	def keyDown(self, key):
		if key == pygame.K_BACKSPACE:
			if (self.txtBuffer and self.txtBuffer[-1] != '\n') or not self.txtBuffer:
				try:
					self.txtBuffer.pop()
				except:
					pass
		elif key == pygame.K_RETURN:
			cmd = ''
			i = -1
			while len(self.txtBuffer) > -i-1 and self.txtBuffer[i] != '\n':
				cmd = self.txtBuffer[i] + cmd
				i -= 1
			self.txtBuffer.append('\r')
			self.exec_cmd(cmd)
			self.txtBuffer.append('\n')
		elif key == pygame.K_TAB:
			for i in range(4):
				self.txtBuffer.append(' ')
		elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
			self.shift = True
		elif key == pygame.K_CAPSLOCK:
			self.capsLock = 1 - self.capsLock
		else:
			if 32 <= key <= 126:
				if (key == 39 or 44 <= key <= 57 or key == 59 or key == 61 or key == 96 or 91 <= key <= 93) and self.shift:
					self.txtBuffer.append(self.caps[chr(key)])
				elif 97 <= event.key <= 122 and (self.shift or self.capsLock):
					self.txtBuffer.append(self.caps[chr(key)])
				else:
					self.txtBuffer.append(chr(key))

class Secret:
	def __init__(self, rect, dialogID):
		self.rect = pygame.Rect(rect)
		self.dialogID = dialogID
	def mouseDown(self, pos, button):
		if self.rect.collidepoint(pos):
			framework.dialogs.pop()

class DlgStatus(Enum):
	INFO = 0
	WARNING = 1
	ERROR = 2

class Dialog:
	def __init__(self, title, content, status=DlgStatus.INFO):
		self.img = pygame.image.load("res/dialog/dialog.png")
		self.icon = pygame.transform.scale(pygame.image.load("res/dialog/" + str(status) + ".bmp"), (32, 32))
		self.icon.set_colorkey((255, 0, 255))
		self.raster = pygame.font.Font("res/Perfect_DOS_VGA_437.ttf", 16)
		self.title = self.raster.render(title, True, (255, 255, 255))
		self.content = self.wrap(content, 35)
		self.dialogID = 0
		self.w, self.h = self.img.get_size()
		self.x, self.y = 322, 284
		self.closeBtn = None
	def wrap(self, txt, w):
		processed = []
		temp = ""
		for i in range(txt.__len__()):
			if i != 0 and i % w == 0:
				processed.append(self.raster.render(temp, True, (0, 0, 0)))
				temp = ""
			temp += txt[i]
		processed.append(self.raster.render(temp, True, (0, 0, 0)))
		return processed
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
term = App("res/blank.jpg")
snake = App("res/blank.jpg")
framework.appID = bg.appID
framework.addApp(bg)
framework.addApp(term)
framework.addDialog(Dialog("Hey there!", "Welcome to Winnux 58!"))
bg.addButton(Button("res/button/txt_btn.bmp", width // 2 - 35, 20, term.appID, font=framework.raster, content="TERMINAL"))
term.addButton(Button("res/button/txt_btn.bmp", width // 2 - 35, 20, bg.appID, font=framework.raster, content="CLOSE"))
term.enableTxtField(0, 0, 80, 20)

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
