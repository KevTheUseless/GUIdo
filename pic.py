import pygame, sys, random

width, height = 1024, 768

class Pic(object):
	def __init__(self, fileName):
		img = pygame.image.load(fileName)
		self.img = pygame.transform.scale(img, (width, height))
		self.x, self.y = 0, 0
		self.w, self.h = self.img.get_size()
	def draw(self, screen, effectNum = 0, speed = 5):
		if effectNum == 1:
			for x in range(-width, 0, speed):
				screen.blit(self.img, (x, 0))
				pygame.display.update()
		if effectNum == 2:
			for x in range(0, width, speed):
				screen.blit(self.img, (x, 0), (x, 0, speed, self.h))
				pygame.display.update()
		if effectNum == 3:
			oldImg = screen.copy()
			for x in range(-width, 0, speed):
				screen.blit(self.img, (x, 0))
				screen.blit(oldImg, (x + width, 0))
				pygame.display.update()
		screen.blit(self.img, (self.x, self.y), (0, 0, self.w, self.h))
		pygame.draw.rect(screen, (0, 255, 0), (0, 0, speed * 8, 8), 0)
	def filter(self, screen, filterNum):
		if filterNum == 1:				#Grayscale
			for y in range(self.h):
				for x in range(self.w):
					r0, g0, b0, alpha = self.img.get_at((x, y))
					grayscale = int((r0 + g0 + b0) / 3)
					r, g, b = grayscale, grayscale, grayscale
					screen.set_at((x, y), (r, g, b))
				pygame.display.update()
		elif filterNum == 2:			#Kaleidoscope
			img0 = pygame.transform.scale(self.img, (width, height))
			img1 = pygame.Surface((width, height))
			n = self.w
			a = int(self.w / 2)
			for y in range(a):
				for x in range(y, a):
					img1.set_at((x, y), img0.get_at((x, y)))
					img1.set_at((y, x), img0.get_at((x, y)))
					img1.set_at((n - 1 - x, y), img0.get_at((x, y)))
					img1.set_at((n - 1 - y, x), img0.get_at((x, y)))
			for y in range(a - 1):
				for x in range(n):
					img1.set_at((x, n - 1 - y), img1.get_at((x, y)))
			screen = pygame.transform.scale(img1, (width, height))
			self.img = screen.copy()
		elif filterNum == 3:			#Inverted
			for y in range(self.h):
				for x in range(self.w):
					r0, g0, b0, alpha = self.img.get_at((x, y))
					c = (255 - r0, 255 - g0, 255 - b0)
					screen.set_at((x, y), c)
				pygame.display.update()
		elif filterNum == 4:			#Black & white ONLY
			for y in range(self.h):
				for x in range(self.w):
					r0, g0, b0, alpha = self.img.get_at((x, y))
					grayscale = int((r0 + g0 + b0) / 3)
					c = (grayscale // 128 * 128, grayscale // 128 * 128, grayscale // 128 * 128)
					screen.set_at((x, y), c)
				pygame.display.update()
		elif filterNum == 5:			#Oil painting
			n = 5
			grid = [[0] * n] * n
			for y in range(n // 2, self.h - n // 2):
				for x in range(n // 2, self.w - n // 2):
					self.getPixelGrid(x, y, n, grid)
					x1 = random.randint(0, n - 1)
					y1 = random.randint(0, n - 1)
					screen.set_at((x, y), grid[x1][y1])
				pygame.display.update()
		elif filterNum == 6:			#Pencil sketch
			n = 5
			grid = [[0] * n] * n
			for y in range(n // 2, self.h - n // 2):
				for x in range(n // 2, self.w - n // 2):
					self.getPixelGrid(x, y, n, grid)
					x1 = random.randint(0, n - 1)
					y1 = random.randint(0, n - 1)
					c1 = grid[y1][x1]
					grayscale = (c1[0] + c1[1] + c1[2]) // 3 // 32 * 32
					c = (grayscale, grayscale, grayscale)
					screen.set_at((x, y), c)
				pygame.display.update()
		elif filterNum == 7:			#Carving
			d = 128
			n = 5
			grid = [[0] * n] * n
			for y in range(n // 2, self.h - n // 2):
				for x in range(n // 2, self.w - n // 2):
					self.getPixelGrid(x, y, n, grid)
					c0 = self.img.get_at((x, y))
					c1 = grid[0][0]
					r = (c1[0] - c0[0]) + d
					if r > 255:
						r = 255
					if r < 0:
						r = 0
					g = (c1[1] - c0[1]) + d
					if g > 255:
						g = 255
					if g < 0:
						g = 0
					b = (c1[2] - c0[2]) + d
					if b > 255:
						b = 255
					if b < 0:
						b = 0
					grayscale = max(r, g, b)
					c = (grayscale, grayscale, grayscale)
					screen.set_at((x, y), c)
				pygame.display.update()
		self.img = screen.copy()
	def getPixelGrid(self, x0, y0, sideLen, pixelGrid):
		n = sideLen // 2
		for y in range(-n, n + 1):
			for x in range(-n, n + 1):
				pixelGrid[y + n][x + n] = self.img.get_at((x + x0, y + y0))