import pygame

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Initialize
pygame.init()

# Define screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Variable to keep game running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Create a surface and pass in a tuple containing its length and width
    surf = pygame.Surface((50, 50))

    # Give the surface a color to separate it from the background
    surf.fill((0, 0, 0))
    rect = surf.get_rect()

    # Put the center of surf at the center of the display
    surf_center = (
        (SCREEN_WIDTH - surf.get_width())/2,
        (SCREEN_HEIGHT - surf.get_height())/2
    )

    # This line says "Draw surf onto the screen at the center"
    screen.blit(surf, surf_center)
    pygame.display.flip()
