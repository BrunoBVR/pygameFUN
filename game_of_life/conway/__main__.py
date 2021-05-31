import pygame
from game_of_life import GameOfLife

pygame.init()
pygame.display.set_caption("Conway's Game of Life on pygame!")

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60

conway = GameOfLife(screen, scale=13)

# Main loop
while True:
    clock.tick(fps)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or(
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            quit()

    conway.run()
    pygame.display.update()
