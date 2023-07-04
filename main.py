import random
import time
import pygame

from objects import Background, Ground, Police, Theif, Cactus, Cloud, Ptera, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (1280, 768 )
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.DOUBLEBUF)




clock = pygame.time.Clock()
FPS = 200

# COLORS *********************************************************************

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)


# IMAGES *********************************************************************

start_img = pygame.image.load('Assets/start_img.png')
start_img = pygame.transform.scale(start_img, (387, 220))


game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (500, 63))

replay_img = pygame.image.load('Assets/replay.png')
replay_img = pygame.transform.scale(replay_img, (60, 60))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 120

numbers_img = pygame.image.load('Assets/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))
background_img = pygame.image.load('./Assets/background.png')
background_img = pygame.transform.scale(background_img, (1440, 768))
# SOUNDS *********************************************************************

jump_fx = pygame.mixer.Sound('Sounds/jump.wav')
start = pygame.mixer.Sound('Sounds/start.wav')
murife = pygame.mixer.Sound('Sounds/murife.mp3')
checkpoint_fx = pygame.mixer.Sound('Sounds/checkPoint.wav')
count = 1
# OBJECTS & GROUPS ***********************************************************

ground = Ground()
background = Background()
theif = Theif(250, 400)
police = Police(50, 400)

cactus_group = pygame.sprite.Group()
ptera_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()

# FUNCTIONS ******************************************************************

def reset():
	global counter, SPEED, POLICESPEED, score, high_score
	win.blit(background_img, (0, 0))
	if score and score >= high_score:
		high_score = score

	counter = 0
	SPEED = 7
	POLICESPEED = 7
	score = 0
	police.x = 50

	cactus_group.empty()
	ptera_group.empty()
	cloud_group.empty()
	stars_group.empty()

	theif.reset()
	police.reset()


keys = []
GODMODE = False
DAYMODE = False
LYAGAMI = False

# VARIABLES ******************************************************************

counter = 0
enemy_time = 100
cloud_time = 250
stars_time = 150

SPEED = POLICESPEED =5
jump = False
police_jump = False
police_duck = False
duck = False

score = 0
high_score = 0
start_page = True
mouse_pos = (-1, -1)

running = True
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)

gradient_surf = pygame.Surface((WIDTH, HEIGHT))
start_time = time.time()
while running:
	jump = False
	
	police_jump = False
	win.fill(SKY_BLUE)
	# if DAYMODE:
	# 	
	# else:
	# 	win.fill(GRAY)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE :
				running = False
    
			if  event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_SPACE:
				if start_page:
					start_page = False
				elif theif.alive:
					jump = True


					# jump_fx.play()
				else:
					reset()
    
	
			if event.key == pygame.K_w:
				if start_page:
					start_page = False
				elif police.alive:
					police_jump = True
					# jump_fx.play()
				else:
					reset()

			if event.key == pygame.K_UP:
				jump = True
				# jump_fx.play()
    
			if event.key == pygame.K_w:
				police_jump = True
				# jump_fx.play()

			if event.key == pygame.K_DOWN:
				duck = True
    
			if event.key == pygame.K_s:
				police_duck = True

			key = pygame.key.name(event.key)
			keys.append(key)
			keys = keys[-7:]
			if ''.join(keys).upper() == 'GODMODE':
				GODMODE = not GODMODE

			if ''.join(keys).upper() == 'DAYMODE':
				DAYMODE = not DAYMODE

			if ''.join(keys).upper() == 'LYAGAMI':
				LYAGAMI = not LYAGAMI

			if ''.join(keys).upper() == 'SPEEDUP':
				SPEED += 2

			if ''.join(keys).upper() == 'IAMRICH':
				score += 10000

			if ''.join(keys).upper() == 'HISCORE':
				high_score = 99999

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				jump = False

			if event.key == pygame.K_DOWN:
				duck = False

			if event.key == pygame.K_w:
				police_jump = False
			
			if event.key == pygame.K_s:
				police_duck = False

		
    
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = (-1, -1)

	if start_page:
		win.fill(SKY_BLUE)  # Fill with black color
		win.blit(start_img, (500, 300))
		start.play()
		

	else:
		start.stop()
		current_time = time.time()
		if current_time - start_time >= 10:
			jump_fx.play()
			count += 1
			start_time = current_time
		if theif.alive :
			
			counter += 1
			if counter % int(enemy_time) == 0:
				if random.randint(1, 10) == 5:
					y = random.choice([85, 130])
					ptera = Ptera(WIDTH, y)
					ptera_group.add(ptera)
				else:
					type = random.randint(1, 4)
					cactus = Cactus(type)
					cactus_group.add(cactus)

			if counter % cloud_time == 0:
				y = random.randint(40, 100)
				cloud = Cloud(WIDTH, y)
				cloud_group.add(cloud)

			if counter % stars_time == 0:
				type = random.randint(1, 3)
				y = random.randint(40, 100)
				star = Star(WIDTH, y, type)
				stars_group.add(star)

			if counter % 100 == 0:
				SPEED += 0.1
				POLICESPEED += 0.1
				enemy_time -= 0.5

			if counter % 5 == 0:
				score += 1


			if not GODMODE:
				for cactus in cactus_group:
					if LYAGAMI:
						dx = cactus.rect.x - theif.rect.x
						px = cactus.rect.x - police.rect.x
						if 0 <= dx <= (70 + (score//100)):
							jump = True
						if 0 <= px <= (70 + (score//100)):
							police_jump = True


					if pygame.sprite.collide_mask(theif, cactus):
						SPEED = 0
      
						theif.alive = False

					if not theif.alive:
						if pygame.sprite.collide_mask(police, theif):
							police.alive = False
							# die_fx.play()


				for cactus in ptera_group:
					px = cactus.rect.x - police.rect.x
					if 0 <= px <= (70 + (score//100)):
						police_jump = True
					if LYAGAMI:
						dx = ptera.rect.x - theif.rect.x
						if 0 <= dx <= 70:
							if theif.rect.top <= ptera.rect.top:
								jump = True
							else:
								duck = True
						else:
							duck = False

					if pygame.sprite.collide_mask(theif, ptera):
						SPEED = 0
						theif.alive = False
						# die_fx.play()
		if police.alive :
			if pygame.sprite.collide_mask(police, theif):
				POLICESPEED = 0
				police.alive = False
				# die_fx.play()
		if not theif.alive:
			police.x += 10
		ground.update(SPEED)
		ground.draw(win)
      

		cloud_group.update(POLICESPEED-3, theif)
		cloud_group.draw(win)
		stars_group.update(POLICESPEED-3, theif)
		stars_group.draw(win)
		cactus_group.update(POLICESPEED, theif)
		cactus_group.draw(win) 
		ptera_group.update(POLICESPEED-1, theif)
		ptera_group.draw(win)
		theif.update(jump, duck)
		theif.draw(win)
		police.update(police_jump, police_duck)
		police.draw(win)

		string_score = str(score).zfill(5)
		for i, num in enumerate(string_score):
			win.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

		if high_score:
			win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score = f'{high_score}'.zfill(5)
			for i, num in enumerate(string_score):
				win.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))

		if not police.alive:
			win.blit(game_over_img, ((WIDTH //2)-250, 55))
			win.blit(replay_img, replay_rect)

			if replay_rect.collidepoint(mouse_pos):
				reset()
    

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	clock.tick(FPS)
	pygame.display.flip()

pygame.quit()