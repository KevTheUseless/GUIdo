# TextDraw.py
# Pixel art using hex codes

import pygame, sys

width, height = 800, 600

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

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TextDraw")
clock = pygame.time.Clock()

letterColorList = [(0, 0, 0), (255, 255, 255)]
upper = []
lower = []
for i in range(26):
	name = i + ord('A')
	upper.append(process(convert("res/charset/upper/" + chr(name) + ".bmp"), letterColorList, 8, 2))
	name = i + ord('a')
	lower.append(process(convert("res/charset/lower/" + chr(name) + ".bmp"), letterColorList, 8, 2))

while True:
	for i in range(26):
		screen.blit(upper[i], (10 + i * 16, 100))
		screen.blit(lower[i], (10 + i * 16, 116))
	pygame.display.update()
	clock.tick(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()