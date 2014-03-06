import sys, pygame
pygame.init()

width = 640
height = 480

screen = pygame.display.set_mode((640,480))

#background = pygame.image.load("background.png")
#backgroundrect = pygame.Rect(0,0,1,1)

cody = pygame.image.load("codyinthebox.png")
codyrect = cody.get_rect()
codyrect = codyrect.move(250,150)

#pipe dimensions: ~65x205
uppipe = pygame.image.load("uppipe.png")
uppiperect = uppipe.get_rect()
uppiperect = uppiperect.move(640,400)

downpipe = pygame.image.load("downpipe.png")
downpiperect = downpipe.get_rect()
downpiperect = downpiperect.move(640,-20)

gate = pygame.Rect(652,225,1,175)

black = 0, 0, 0
speed = [0,0]
counter = 0

while 1:

	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_SPACE:
				speed = [0,-4]

	#move things
	codyrect = codyrect.move(speed)
	downpiperect = downpiperect.move(-1,0)
	uppiperect = uppiperect.move(-1,0)
	gate = gate.move(-1,0)

	#gravity simulation
	if counter % 8 == 0:
		speed[1] = speed[1] + 1

	#max fall speed
	if speed[1] > 4:
		speed[1] = 5

	#collision checking
	if codyrect.bottom > height:
		speed[1] = 0
	if codyrect.top < 0:
		speed[1] = 0
		codyrect = codyrect.move(0,1)

	#drawing
	screen.fill(black)
	screen.blit(cody, codyrect)
	screen.blit(downpipe, downpiperect)
	screen.blit(uppipe, uppiperect)
	#screen.blit(background, backgroundrect)
	pygame.display.flip()

	#game timers
	pygame.time.wait(8)
	if counter > 10000:
		counter = 0
	else:
		counter += 1 