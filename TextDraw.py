# TextDraw.py
# Pixel art using hex codes

import pygame, sys

width, height = 800, 600

def drawByte(screen, data, colorList, x0, y0, dw, scale):
	for dy in range(len(data)):
		line = data[dy]
		for dx in range(dw):
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

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TextDraw")
brickColorList = [(64, 64, 64), (255, 127, 80)]
grassColorList = [(0, 50, 0), (0, 120, 0)]
clock = pygame.time.Clock()

grassPic = pygame.Surface((32, 32))
brickPic = pygame.Surface((32, 32))
brickPic = process(convert("brick.bmp"), brickColorList, 8, 4)
grassPic = process(convert("grass.bmp"), grassColorList, 8, 4)

while True:
	screen.blit(grassPic, (100, 100))
	screen.blit(brickPic, (200, 100))
	pygame.display.update()
	clock.tick(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()