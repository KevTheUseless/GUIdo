# BinEditor.py
# Binary editor for pixel art that supports undo & redo
# Might need to use that later on

import pygame, sys

width, height = 800, 600
mx, my = 0, 0

def drawGrid():
	for i in range(n + 1):
		pygame.draw.line(screen, (170, 170, 170), (50, 50 + 30 * i), (30 * (n + 1.7), 50 + 30 * i), 10)
	for i in range(n + 1):
		pygame.draw.line(screen, (170, 170, 170), (50 + 30 * i, 50), (50 + 30 * i, 30 * (n + 1.7)), 10)

def checkBorders():
	try:
		for i in range(len(squares)):
			if pygame.Rect(squares[i][0], squares[i][1], 30, 30).collidepoint(mx, my):  
				flagList[i] = 1 - flagList[i]
				undo.append(i)
	except:
		return

def calc():
	numStr = ""
	for i in range(n):
		for j in range(n):
			numStr += str(flagList[n * j + i])
		strList[i] = hex(int(numStr, 2))[2:]
		numStr = ""

def saveFile():
	fileName = input("File to save to: ")
	f = open(fileName, "w")
	for s in strList:
		f.write(s + ' ')
	f.close()

n = 8

squares = []
for i in range(55, 30 * (n + 1), 30):
	for j in range(55, 30 * (n + 1), 30):
		squares.append([i, j])
strList = [""] * n

print(squares)

flagList = [0] * n * n
print(flagList)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Binary Color Editor")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
undo = []
redo = []
over = False

while True:
	screen.fill((0, 0, 0))
	drawGrid()
	checkBorders()
	calc()
	mx, my = 0, 0
	for i in range(len(flagList)):
		if flagList[i]:
			pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(squares[i][0] + 1, squares[i][1] + 1, 20, 20), 0)
	for i in range(len(strList)):
		img = font.render(strList[i], True, (0, 0, 255))
		screen.blit(img, (30 * (n + 1) + 45, 55 + 30.5 * i))
	pygame.display.update()
	clock.tick(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if over:
					redo = []
				print(event.pos)
				mx, my = event.pos
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				saveFile()
			elif event.key == pygame.K_z:
				if len(undo) != 0:
					lastOp = undo.pop()
					redo.append(lastOp)
					flagList[lastOp] = 1 - flagList[lastOp]
					over = True
			elif event.key == pygame.K_y:
				if len(redo) != 0:
					prevOp = redo.pop()
					undo.append(prevOp)
					flagList[prevOp] = 1 - flagList[prevOp]
					over = True
			elif event.key == pygame.K_0:
				flagList = [0] * n * n