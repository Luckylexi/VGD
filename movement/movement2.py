import pygame
pygame.init()

window = pygame.display.set_mode((360,740))

pygame.display.set_caption("movement")

path = pygame.image.load('path.png')
walking = [pygame.image.load('rightfoot.png'), pygame.image.load('leftfoot.png')]
rightfoot = pygame.image.load('rightfoot.png')
leftfoot = pygame.image.load('leftfoot.png')


x = 140
y = 480
y2 = 0
width = 64
height = 64
walking = False
color = (0,255,0)
mov = 10
count = 0

def gameDisplay():
		global count
		window.blit(path, (0,y2))
		window.blit(rightfoot, (x,y))
		pygame.display.update()
				


#main
run = True
while run:
		pygame.time.delay(100)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			y2 -= mov

				
		gameDisplay()
				
pygame.quit
