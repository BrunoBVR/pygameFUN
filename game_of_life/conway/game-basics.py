import pygame

pygame.init()

WIDTH = 960
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or(
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            quit()

    # White background
    screen.fill((255, 255, 255))
    pygame.display.update()

    # Draw rectangle on screen
    # INPUTS ---> (canvas, color,[x,y, width-of-rect, height-of rect])
    # Here, x,y are the top left corner of rectangle
    pygame.draw.rect(screen, (25,25,112), [(WIDTH/2) - 50, (HEIGHT/2) - 50, 100, 100])
    pygame.display.update()
    clock.tick(60)
