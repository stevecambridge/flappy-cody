import sys, pygame, random
pygame.init()

width = 640
height = 480

screen = pygame.display.set_mode((640,480))

#object classes
class Cody(pygame.sprite.Sprite):

	#constructor
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("codyinthebox.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(250,150)

class Downpipe(pygame.sprite.Sprite):

	#constructor
	def __init__(self, randFactor):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("downpipe.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(640,0-randFactor)

class Uppipe(pygame.sprite.Sprite):

	#constructor
	def __init__(self, randFactor):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("uppipe.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(640,400-randFactor)

class Gate(pygame.sprite.Sprite):

	#constructor
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(672,0,1,480)

class Background(pygame.sprite.Sprite):

	#constructor
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("background.png")
		self.rect = pygame.Rect(0,0,1,1)

#instantiate pieces for testing
cody = Cody()
background = Background()

player = pygame.sprite.Group(cody)
pipes = pygame.sprite.Group()
scenery = pygame.sprite.Group(background)

black = 0, 0, 0
speed = [0,0]
grav_counter = 0
pipe_counter = 0

#main game loop
running = True
while running:

	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_SPACE:
				speed = [0,-4]
				grav_counter = 0
			elif event.key == pygame.K_ESC:
				sys.exit()

	#move things
	cody.rect = cody.rect.move(speed)
	for Downpipe in pipes:
		Downpipe.rect = Downpipe.rect.move(-1,0)
	for Uppipe in pipes:
		Uppipe.rect = Uppipe.rect.move(-1,0)
	#gate.rect = gate.rect.move(-1,0)

	#gravity simulation w/ max fall speed
	if grav_counter % 8 == 0:
		speed[1] = speed[1] + 1
	if speed[1] > 4:
		speed[1] = 5

	#collision checking
	if cody.rect.bottom > height:
		speed[1] = 0
	if cody.rect.top < 0:
		speed[1] = 0
		cody.rect = cody.rect.move(0,1)
	#GAMEOVER
	for Uppipe in pipes:
		if pygame.sprite.collide_rect(cody, Uppipe):
			running = False
	for Downpipe in pipes:
		if pygame.sprite.collide_rect(cody, Downpipe):
			running = False

	#drawing
	#screen.fill(black)
	scenery.draw(screen)
	pipes.draw(screen)
	player.draw(screen)
	pygame.display.flip()

	#pipe deletion
	for Downpipe in pipes:
		if Downpipe.rect.right < 0:
			Downpipe.kill()
	for Uppipe in pipes:
		if Uppipe.rect.right < 0:
			Downpipe.kill()


	#game timers
	pygame.time.wait(0)
	if grav_counter > 100:
		grav_counter = 0
	else:
		grav_counter += 1

	if pipe_counter == 10:
		x = random.randint(0,100)
		pipes.add(Uppipe(x))
		pipes.add(Downpipe(x))
		pipe_counter = 0
	else:
		pipe_counter += 1