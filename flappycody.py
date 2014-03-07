import sys, pygame, random
pygame.init()
myfont = pygame.font.SysFont("monospace", 15, True, False)


#misc data
black = 0, 0, 0
speed = [0,0]
grav_counter = 0
pipe_counter = 0
width = 640
height = 480
score = 0

#screen init
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

#initialzize cody and background
cody = Cody()
background = Background()

#groups
player = pygame.sprite.Group(cody)
pipes_group = pygame.sprite.Group()
scenery = pygame.sprite.Group(background)
gates = pygame.sprite.Group()

#main game loop
running = True
while running:

	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_SPACE:
				speed = [0,-5]
				grav_counter = 0
			elif event.key == pygame.K_ESC:
				sys.exit()

	#move things
	cody.rect = cody.rect.move(speed)
	for x in pipes_group:
		x.rect = x.rect.move(-1,0)
	for x in pipes_group:
		x.rect = x.rect.move(-1,0)
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
	for x in pipes_group:
		if pygame.sprite.collide_rect(cody, x):
			running = False
	#scoring
	for y in gates:
		if pygame.sprite.collide_rect(cody, y):
			y.kill()
			gates.remove(y)
			score = score + 1

	#drawing
	#screen.fill(black)
	scenery.draw(screen)
	pipes_group.draw(screen)
	player.draw(screen)
	pygame.display.flip()
	label = myfont.render("TEXT HERE", 1, (235,25,150))
	screen.blit(label, (100, 100))

	#pipe deletion
	for x in pipes_group:
		if x.rect.right < 0:
			x.kill()
			pipes_group.remove(x)
	for y in gates:
		if y.rect.right < 0:
			y.kill()
			gates.remove(y)

	#game timers
	if grav_counter > 100:
		grav_counter = 0
	else:
		grav_counter += 1

	if pipe_counter == 120 :
		x = random.randint(0,130)
		u = Uppipe(x)
		d = Downpipe(x)
		pipes_group.add(u)
		pipes_group.add(d)
		pipe_counter = 0
		g = Gate()
		gates.add(g)
	else:
		pipe_counter += 1

	pygame.time.wait(0)