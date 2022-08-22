import pygame, sys

from settings import WIDTH, HEIGHT, FPS
from level import Level
from game_data import level_0

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smario")
clock = pygame.time.Clock()
level = Level(WIN, level_0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
    level.run()

    pygame.display.update()
    clock.tick(FPS)


