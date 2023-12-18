import pygame
from sys import exit
import settings

pygame.init()
screen = pygame.display.set_mode(
    (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

from level import Level

level = Level(level_map=settings.LEVEL_MAP)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    level.run()

    pygame.display.update()
    clock.tick(60)
