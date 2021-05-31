import pygame

import random

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT
)

# Setup for sounds. Defaults are ok
pygame.mixer.init()


# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Define screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define fps
fps = 60

# Define Player object by extending the pygame.sprite.Sprite class
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.frame = 0
        self.last_update = 0
        self.sprites = [pygame.image.load('dragon/PNG/small/frame-1.png'),
                        pygame.image.load('dragon/PNG/small/frame-2.png'),
                        pygame.image.load('dragon/PNG/small/frame-3.png'),
                        pygame.image.load('dragon/PNG/small/frame-4.png')]
        # self.surf = pygame.image.load("jet.png").convert()
        self.surf = self.sprites[self.frame].convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(0,SCREEN_HEIGHT/2)
        )

    # Update frame
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.frame = (self.frame +1)%len(self.sprites)
            self.surf = self.sprites[self.frame].convert_alpha()

    # Move the sprite based on keypressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            # move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            # move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define enemy object by extending pygame.sprite.Sprite class
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite class
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    # Move the cloud with constant speed
    # Remove cloud when it passes the left edge of screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right <= 0:
            self.kill()

# Define bullet object by extending pygame.sprite.Sprite class
class Bullet(pygame.sprite.Sprite):
    BULLET_SPEED = 5
    def __init__(self, position):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("FireSmall.png").convert_alpha() # Transparent image file
        self.rect = self.surf.get_rect(
            center = position
        )

    # Move the bullet with constant speed
    # Remove bullet when it passes the right edge of screen
    def update(self):
        self.rect.move_ip(self.BULLET_SPEED, 0)
        if self.rect.left >= SCREEN_WIDTH:
            self.kill()

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Create a custom event for adding an enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)   # In miliseconds (so this adds cloud every 1s)

# Instantiate player. Right now, this is just a rectangle
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - bullets is used for position updates and collision detection
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# all_sprites.add(player)

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.ogg")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound source: Jon Fincher
# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
hit_sound = pygame.mixer.Sound("hit.wav")

# Variable to keep game running
running = True
last_update = 0

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == pygame.QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            ):
                running=False

        # Add new enemy?
        if event.type == ADDENEMY:
            # Create the new enemy and add it to the sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add new cloud?
        if event.type == ADDCLOUD:
            # Create new cloud and add it to the sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # Shooting
        if (event.type == KEYDOWN and event.key == K_SPACE):
            new_bullet = Bullet(player.rect.center)
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)

    # Get all keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy and clouds positions
    enemies.update()
    clouds.update()
    bullets.update()

    # Fill the screen with sky-blue
    screen.fill((135, 206, 250))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    player.animate()
    screen.blit(player.surf, player.rect)   # Keep this out of loop to keep jet on top of clouds

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        # Stop any moving sounds and play collision sound
        # move_up_sound.stop()
        # move_down_sound.stop()
        collision_sound.play()

        # Stop the loop
        running = False

    # Check if bullet hits an enemy
    for shot in bullets:
        if pygame.sprite.spritecollide(shot, enemies, True):
            shot.kill()
            hit_sound.play()

    # Update the display
    pygame.display.flip()

    # Ensure to maintain a 30 fps rate
    clock.tick(fps)

# At this point, we are done! We can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
