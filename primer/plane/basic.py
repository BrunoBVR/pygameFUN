# Simple pygame program
# Creates a window, fill background with white
# Draws a circle in the middle

import pygame
pygame.init()

# Set up drawing window
screen = pygame.display.set_mode([500,500])

# Run until user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background with white
    screen.fill((255, 255, 255))

    # Draw solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250,250), 75)

    # Flip the display: updates the contents of the display to the screen.
    # Without this call, nothing appears in the window!
    pygame.display.flip()

# Done!
pygame.quit()
