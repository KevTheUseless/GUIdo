# TextDraw.py
# A place to test

import pygame, sys

def wrap(txtBuffer, w = 80):
	lines = []
	temp = ""
	for i in range(len(txtBuffer)):
		if txtBuffer[i] == '\n' or (i != 0 and i % w == 0):
			lines.append(temp)
			temp = ""
		else:
			temp += txtBuffer[i]
	lines.append(temp)
	return lines

def drawTxt(screen, lines, y = 0):
	for line in lines:
		img = raster.render(line, True, (255, 255, 255))
		screen.blit(img, (0, y))
		y += 16


width, height = 800, 600

txtBuffer = []
# ↓ Magic! ↓
caps = { '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z' }

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TextDraw")
clock = pygame.time.Clock()

raster = pygame.font.Font("res/vga936.fon", 32)

shift = False
capsLock = False

while True:
	screen.fill((0, 0, 0))
	drawTxt(screen, wrap(txtBuffer))
	pygame.display.update()
	clock.tick(50)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				try:
					txtBuffer.pop()
				except:
					pass
			elif event.key == pygame.K_RETURN:
				txtBuffer.append('\n')
			elif event.key == pygame.K_TAB:
				for i in range(4):
					txtBuffer.append(' ')
			elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				shift = True
			elif event.key == pygame.K_CAPSLOCK:
				capsLock = 1 - capsLock
			else:
				if 32 <= event.key <= 126:
					# ↓ Also magic! ↓
					if (event.key == 39 or 44 <= event.key <= 57 or event.key == 59 or event.key == 61 or event.key == 96 or 91 <= event.key <= 93) and shift:
						txtBuffer.append(caps[chr(event.key)])
					elif 97 <= event.key <= 122 and (shift or capsLock):
						txtBuffer.append(caps[chr(event.key)])
					else:
						txtBuffer.append(chr(event.key))
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				shift = False
			elif event.key == pygame.K_CAPSLOCK:
				capsLock = 1 - capsLock