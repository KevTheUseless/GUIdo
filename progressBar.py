X_MAX = 1920

progressBar = 0
STUFF_TO_ITERATE

for STUFF_TO_ITERATE:
	#PUT STUFF HERE
	progressBar += 1
	pygame.draw.rect(screen, (0, 255, 0), (0, 250, 800, 100), 2)
	pygame.draw.rect(screen, (0, 255, 0), (0, 250, int(progressBar / X_MAX * 800), 100), 0)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()