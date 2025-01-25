import pygame
import random
import pygame.math
from os import path

#[Settings]
img_dir = path.join(path.dirname(__file__), 'img')
WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT * 3/4
        self.speedx = 0
        self.speedy = 0

        self.run_speed = 0
        self.bubble_speed = -3
        self.acceleration = 0.1
        self.up_acceleration = 0.1
        self.gravity = 0.4

        self.health = 1

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx += self.acceleration * (-self.run_speed - self.speedx)
        if keystate[pygame.K_RIGHT]:
            self.speedx += self.acceleration * ( self.run_speed - self.speedx)
        if not keystate[pygame.K_LEFT] and not keystate[pygame.K_RIGHT]:
            self.speedx += self.acceleration * (                - self.speedx)

        
        if keystate[pygame.K_UP]:
            self.speedy += self.up_acceleration * (self.bubble_speed - self.speedy)
            global is_started
            is_started = True
        elif is_started: self.speedy += self.gravity
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        is_hit = pygame.sprite.spritecollide(self, mobs, False)
        if is_hit: self.health -= 1
        if self.health == 0: pygame.quit()

        for i in pygame.sprite.spritecollide(self, winds, False):
            if not i.push_speedx == 0: self.speedx += 0.2 * (i.push_speedx - self.speedx)
            if not i.push_speedy == 0: self.speedy += 0.2 * (i.push_speedy - self.speedy)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -10
        self.speedy = 4
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

        self.speedx = random.randrange(-3, 3)
        self.speedy = -10

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

        self.speedx *= 0.98
        self.speedy *= 0.98
        
        for i in pygame.sprite.spritecollide(self, winds, False):
            if not i.push_speedx == 0: self.speedx += 0.2 * (i.push_speedx - self.speedx)
            if not i.push_speedy == 0: self.speedy += 0.2 * (i.push_speedy - self.speedy)

class Wind(pygame.sprite.Sprite):
    def __init__(self, push_speedx = 5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 60))
        self.image.fill(DARK_GRAY)

        self.rect = self.image.get_rect()
        self.x = WIDTH/2
        self.y = -30
        
        self.speedy = 4
        self.push_speedx = push_speedx
        self.push_speedy = 0

    def update(self):
        self.rect.y += self.speedy
        

is_started = False

all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
winds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mob_spawn_index = 0
mob_spawns = [0.5, 2, 2, 2.9, 3.1, 3.3, 3.5, 5.6, 5.7, 5.8, 5.9, 6, 6.1, 6.2]

wind_spawn_index = 0

runtime = 0

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    if is_started:
        runtime += clock.get_time() / 1000
    else:
        decoy = 0
    
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    back_sprites.update()
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    # print(mob_spawn_index)
    while mob_spawn_index < len(mob_spawns) and runtime > mob_spawns[mob_spawn_index]:
        mob_spawn_index += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    while runtime > 1.2 * wind_spawn_index:
        wind_spawn_index += 1

        push_speedx = 5
        if wind_spawn_index % 2 == 0: push_speedx = -5
        w = Wind(push_speedx)
        back_sprites.add(w)
        winds.add(w)

    # Draw / render
    screen.fill(BLACK)
    back_sprites.draw(screen)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
