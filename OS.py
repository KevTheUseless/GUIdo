from pic import *

class OSEmu(object):
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Windows 95 Simulated")
		self.clock = pygame.time.Clock()
		self.font32 = pygame.font.Font("res/segoeui.ttf", 32)
		self.speed = 5
		self.mousePos = (0, 0)
		self.guideList = []
		self.guideID = 0
	def launch(self):
		for guide in self.guideList:
			guide.draw(self.screen)
		pygame.display.update()
		self.clock.tick(50)
	def addGuide(self, guide):
		guide.id = len(self.guideList)
		self.guideList.append(guide)
	def keyUp(self, key):
		return
	def keyDown(self, key):
		return
	def mouseDown(self, pos, button):
		self.guideList[self.guideID].mouseDown(pos, button)
		print(event.pos)
	def mouseUp(self, pos, button):
		self.guideList[self.guideID].mouseUp(pos, button)
	def mouseMotion(self, pos):
		self.guideList[self.guideID].mouseMotion(pos)

class Guide(object):
	def __init__(self, picName):
		self.pic = Pic(picName)
		self.id = 0
		self.btnList = []
		self.txtList = []
		self.secretList = []
	def draw(self, screen):
		if framework.guideID != self.id:
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
	def addSecret(self, rect, guideID):
		secret = Secret(rect, guideID)
		self.secretList.append(secret)
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

class Button(object):
	def __init__(self, name, picFile, x, y, guideID, **txt):
		self.name = name
		self.img = pygame.image.load(picFile).convert()
		#self.img.set_colorkey(pygame.Color(0, 255, 0))
		self.w, self.h = self.img.get_width() // 3, self.img.get_height()
		self.x, self.y = x, y
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.status = 0
		self.guideID = guideID

		self.txt = txt
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y),
					(self.status * self.rect.w, 0,
					 self.rect.w, self.rect.h))
		if self.txt:
			screen.blit(self.txt['font'].render(self.txt['content'], True, (0,0,0)), (self.x + 10, self.y + 30))
	def mouseDown(self, pos, button):
		if self.rect.collidepoint(pos):
			self.status = 2
	def mouseUp(self, pos, button):
		self.status = 0
		if not self.rect.collidepoint(pos):
			return
		if self.name == 'U':
			framework.guideList[self.guideID].pic.draw(framework.screen, framework.speed)
		if self.name == 'D':
			framework.guideList[self.guideID].pic.draw(framework.screen, framework.speed)
		if self.name == 'L':
			framework.guideList[self.guideID].pic.draw(framework.screen, framework.speed)
		if self.name == 'R':
			framework.guideList[self.guideID].pic.draw(framework.screen, framework.speed)
		framework.guideID = self.guideID

	def mouseMove(self, pos):
		if self.rect.collidepoint(pos):
			self.status = 1
		else:
			self.status = 0

class Txt(object):
	def __init__(self, txt, font, x, y, c, rect):
		self.txt = txt
		self.img = font.render(txt, True, c)
		self.x, self.y = x, y
		self.c = c
		self.rect = pygame.Rect(rect)
	def draw(self, screen):
		if self.rect.collidepoint(framework.mousePos):
			screen.blit(self.img, (self.x, self.y))
		
class Secret(object):
	def __init__(self, rect, guideID):
		self.rect = pygame.Rect(rect)
		self.guideID = guideID
	def mouseDown(self, pos, button):
		if self.rect.collidepoint(pos):
			framework.guideList[self.guideID].pic.draw(framework.screen, 1, framework.speed)
			framework.guideID = self.guideID

framework = OSEmu()
bg = Guide("res/clouds.jpg")
framework.guideID = bg.id
framework.addGuide(bg)
bg.addButton(Button('', "res/button/txt_btn.bmp", width // 2 - 35, 20, bg.id, font=framework.font32, content="hello"))


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