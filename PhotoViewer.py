from pic import *

class PhotoViewer(object):
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Photo Viewer")
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
	def addButton(self, name, picFile, x, y, guideID):
		b = Button(name, picFile, x, y, guideID)
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
			btn.mouse_move(pos)

class Button(object):
	def __init__(self, name, picFile, x, y, guideID):
		self.name = name
		self.img = pygame.image.load(picFile)
		self.img.set_colorkey((0, 255, 0))
		self.w, self.h = self.img.get_width() // 3, self.img.get_height()
		self.x, self.y = x, y
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.status = 0
		self.guideID = guideID
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y),
					(self.status * self.rect.w, 0,
					 self.rect.w, self.rect.h))
	def mouseDown(self, pos, button):
		if self.rect.collidepoint(pos):
			self.status = 2
	def mouseUp(self, pos, button):
		self.status = 0
		if not self.rect.collidepoint(pos):
			return
		if self.name == 'U':
			framework.guideList[self.guideID].pic.draw(framework.screen, 1, framework.speed)
		if self.name == 'D':
			framework.guideList[self.guideID].pic.draw(framework.screen, 2, framework.speed)
		if self.name == 'L':
			framework.guideList[self.guideID].pic.draw(framework.screen, 3, framework.speed)
		if self.name == 'R':
			framework.guideList[self.guideID].pic.draw(framework.screen, 4, framework.speed)
		framework.guideID = self.guideID

	def mouse_move(self, pos):
		if self.rect.collidepoint(pos):
			self.status = 1
		else: self.status = 0

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

framework = PhotoViewer()
g01 = Guide("res/xian01.jpg")
framework.guideID = g01.id
framework.addGuide(g01)
g02 = Guide("res/xian02.jpg")
framework.addGuide(g02)
g03 = Guide("res/xian03.jpg")
framework.addGuide(g03)
g04 = Guide("res/xian04.jpg")
framework.addGuide(g04)
g01.addButton('U', "res/button/btn_up.bmp", width // 2 - 35, 20, g02.id)
g01.addButton('L', "res/button/btn_left.bmp", 20, height // 2 - 35, g03.id)
g01.addButton('R', "res/button/btn_right.bmp", width - 100, height // 2 - 35, g04.id)
g02.addButton('D', "res/button/btn_down.bmp", width // 2 - 35, height - 100, g01.id)
g03.addButton('R', "res/button/btn_right.bmp", width - 100, height // 2 - 35, g01.id)
g04.addButton('L', "res/button/btn_left.bmp", 20, height // 2 - 35, g01.id)
g01.addTxt("How are you?", framework.font32, 487, 407, (0, 255, 0), (580, 439, 26, 38))

g05 = Guide("res/profilePic.jpg")
framework.addGuide(g05)
g01.addSecret((521, 233, 24, 28), g05.id)
g05.addSecret((521, 110, 30, 30), g01.id)

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
