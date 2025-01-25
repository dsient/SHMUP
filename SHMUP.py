import pygame
import random
from os import path

# [Settings]
img_dir = path.join(path.dirname(__file__), 'img')
WIDTH = 480
HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)

# Initialize pygame and create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

# Load background
background = pygame.image.load(path.join(img_dir, 'space.jpg')).convert()
background_rect = background.get_rect()

# Load all game graphics
player_img = pygame.image.load(path.join(img_dir, "ship1.png")).convert()
player_img = pygame.transform.scale(player_img, (50, 38))  # Scale to desired size
player_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_dir, "bubble.png")).convert()
#bullet_img.set_colorkey(BLACK)  # Remove background from the bullet sprite

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT * 3/4
        self.speedx = 0
<<<<<<< Updated upstream
        self.acceleration = 0.2
        self.health = 1 

=======
        self.speedy = 0

        self.run_speed = 0
        self.bubble_speed = -3
        self.acceleration = 0.1
        self.up_acceleration = 0.1
        self.gravity = 0.4

        self.health = 1
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
=======
        self.rect.y = -10
        self.speedy = 4
        self.speedx = 0
>>>>>>> Stashed changes

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.image = pygame.Surface((random.randint(20, 50), random.randint(20, 50)))


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
        # Kill the bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

<<<<<<< Updated upstream
# Sprite groups
=======
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

>>>>>>> Stashed changes
all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
winds = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player and mobs
player = Player()
all_sprites.add(player)
<<<<<<< Updated upstream
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
=======

mob_spawn_index = 0
mob_spawns = [0.5, 2, 2, 2.9, 3.1, 3.3, 3.5, 5.6, 5.7, 5.8, 5.9, 6, 6.1, 6.2]

wind_spawn_index = 0

runtime = 0
>>>>>>> Stashed changes

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)

<<<<<<< Updated upstream
=======
    if is_started:
        runtime += clock.get_time() / 1000
    else:
        decoy = 0
    
>>>>>>> Stashed changes
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    back_sprites.update()
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    while runtime > 1.2 * wind_spawn_index:
        wind_spawn_index += 1

<<<<<<< Updated upstream
    # Check if a mob hits the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        player.health -= 1  # Reduce health only once
        for mob in hits:  # Optional: Reset the positions of mobs that collided
            mob.rect.x = random.randrange(WIDTH - mob.rect.width)
            mob.rect.y = random.randrange(-100, -40)
            mob.speedy = random.randrange(1, 8)
        if player.health <= 0:
            running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
=======
        push_speedx = 5
        if wind_spawn_index % 2 == 0: push_speedx = -5
        w = Wind(push_speedx)
        back_sprites.add(w)
        winds.add(w)

    # Draw / render
    screen.fill(BLACK)
    back_sprites.draw(screen)
>>>>>>> Stashed changes
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

pygame.quit()
