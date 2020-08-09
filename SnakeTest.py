import pygame, sys, random

width, height = 1024, 708

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Winnux 58")
clock = pygame.time.Clock()
raster = pygame.font.Font("res/Perfect_DOS_VGA_437.ttf", 15)

class SnakeGame(object):
	def __init__(self):
		self.tileWidth = 32
		self.snakeLen = 1
		self.snakePos = []
		self.direction = 0
		self.speedX = (1, 0, -1, 0)
		self.speedY = (0, 1, 0, -1)
		self.sx, self.sy = 0, 0
		self.ix, self.iy = random.randint(0, 19), random.randint(0, 14)
		self.lost = 0
	def draw(self, canvas):
		if self.lost == 1:
		for pos in self.snakePos[-self.snakeLen:]:
			pygame.draw.rect(canvas, (60, 110, 5), (pos[0] * self.tileWidth, pos[1] * self.tileWidth, self.tileWidth, self.tileWidth))
		pygame.draw.rect(canvas, (190, 30, 50), (self.ix * self.tileWidth, self.iy * self.tileWidth, self.tileWidth, self.tileWidth))
	def move(self):
		if self.lost == 1:
			return
		self.sx = (self.sx + self.speedX[self.direction]) % 20
		self.sy = (self.sy + self.speedY[self.direction]) % 15
		if (self.sx, self.sy) in self.snakePos[-self.snakeLen:]:
			self.lost = 1
		self.snakePos.append((self.sx, self.sy))
		if self.sx == self.ix and self.sy == self.iy:
			self.ix, self.iy = random.randint(0, 20), random.randint(0, 15)
			self.snakeLen += 1
	def keyDown(self, key):
		if key == pygame.K_UP:
			self.direction = 3
		if key == pygame.K_DOWN:
			self.direction = 1
		if key == pygame.K_LEFT:
			self.direction = 2
		if key == pygame.K_RIGHT:
			self.direction = 0
		if key == pygame.K_r and self.lost == 1:
			self.snakeLen = 1
			self.snakePos = []
			self.sx, self.sy = 0, 0
			self.ix, self.iy = random.randint(0, 20), random.randint(0, 15)
			self.lost = 0

snake = SnakeGame()
while True:
	screen.fill((0, 0, 0))
	snake.draw(screen)
	snake.move()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			snake.keyDown(event.key)
	pygame.display.update()
	clock.tick(10)