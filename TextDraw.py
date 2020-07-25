# TextDraw.py
# A place to test

import pygame, sys

width, height = 800, 600

txtBuffer = []

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TextDraw")
clock = pygame.time.Clock()

while True:
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
					for c in txtBuffer:
						print(txtBuffer)
				except:
					print(txtBuffer)
			elif event.key == pygame.K_RETURN:
				txtBuffer.append('\n')
				print(txtBuffer)
			elif event.key == pygame.K_LSHIFT or event == pygame.K_RSHIFT:
				# TODO: do shift
				pass
			elif event.key == pygame.K_CAPSLOCK:
				# TODO: always do shift
				pass
			else:
				if 32 <= event.key <= 126 or event.key == pygame.K_TAB:
					txtBuffer.append(chr(event.key))
					for c in txtBuffer:
						print(txtBuffer)