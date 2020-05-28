import pygame, sys

ORIGIN_ALT, SCALE = 5700, 0.15
X_MAX, Y_MAX = 1401, 1401
width, height = 1400, 640

def convertCoords(z):
	return height - (z - ORIGIN_ALT) * SCALE

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Qomolangma v2.0")
screen.fill((0, 0, 0))

ascFile = open("Qomolangma.asc", 'r')
ascList = ascFile.readlines()
ascFile.close()

maxList, minList = [0] * X_MAX, [height] * X_MAX
dataList = []

#PROGRESS BAR#
progressBar = 0

for dataStr in ascList:
	dataStr = dataStr.strip('\n')
	line = []
	for s in dataStr.split():
		line.append(eval(s))
	dataList.append(line)
	progressBar += 1
	pygame.draw.rect(screen, (0, 255, 0), (0, 250, 800, 100), 2)
	pygame.draw.rect(screen, (0, 255, 0), (0, 250, int(progressBar / X_MAX * 800), 100), 0)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
#END OF PROGRESS BAR#

screen.fill((0, 0, 0))

for y in range(Y_MAX):
	x0, z0 = 0, dataList[y][X_MAX - 1]
	for x in range(X_MAX):
		z = dataList[y][X_MAX - 1 - x]
		flag = 0
		if z < minList[x]:
			minList[x], flag = z, 1
		if z > maxList[x]:
			maxList[x], flag = z, 1
		if flag == 1 and abs(z - z0) < 100:
			pygame.draw.line(screen, (240, 240, 240), \
							 (x0, convertCoords(z0)), \
							 (x, convertCoords(z)), 1)
		x0, z0 = x, z
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
