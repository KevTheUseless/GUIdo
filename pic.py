import pygame, sys, random

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