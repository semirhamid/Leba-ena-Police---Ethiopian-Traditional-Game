import pygame


class Theif():
	def __init__(self, x, y):
		self.x, self.base = x + 200, y + 300
		self.run_list = []
		self.duck_list = []


		for i in range(1, 5):
			img = pygame.image.load(f'Assets/leba/{i}.png')
			img = pygame.transform.scale(img, (134, 136)) 
			self.run_list.append(img)

		for i in range(4, 6):
			img = pygame.image.load(f'Assets/leba/{i}.png')
			img = pygame.transform.scale(img, (134, 136))
			self.duck_list.append(img)

		self.dead_image = pygame.image.load(f'Assets/leba/8.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (134, 136))

		self.reset()

		self.vel = 0
		self.gravity = 1
		self.jumpHeight = 25
		self.isJumping = False

	def reset(self):
		self.index = 0
		self.image = self.run_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.bottom = self.base

		self.alive = True
		self.counter = 0

	def update(self, jump, duck):
		if self.alive:
			if not self.isJumping and jump:
				self.vel = -self.jumpHeight
				self.isJumping = True

			self.vel += self.gravity
			if self.vel >= self.jumpHeight:
				self.vel = self.jumpHeight

			self.rect.y += self.vel
			if self.rect.bottom > self.base:
				self.rect.bottom = self.base
				self.isJumping = False

			if duck:
				self.counter += 1
				if self.counter >= 6:
					self.index = (self.index + 1) % len(self.duck_list)
					self.image = self.duck_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			elif self.isJumping:
				self.index = 0
				self.counter = 0
				self.image = self.run_list[self.index]
			else:
				self.counter += 1
				if self.counter >= 4:
					self.index = (self.index + 1) % len(self.run_list)
					self.image = self.run_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

		else:
			self.image = self.dead_image

	def draw(self, win):
		win.blit(self.image, self.rect)