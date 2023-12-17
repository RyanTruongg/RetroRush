import pygame
from sys import exit
from level import Level
import settings

pygame.init()
screen = pygame.display.set_mode(
    (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

level = Level(level_map=settings.LEVEL_MAP)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    # image = pygame.image.load(
    #     'Asset Packs 1-3 (final)\Asset Pack-V1\Sprite Sheets\Character Idle 48x48.png'
    # )
    # rect = image.get_rect(topleft=(0, 0))
    # rect.width = 48
    # subimage = pygame.transform.scale_by(image.subsurface(rect), 2)
    # screen.blit(subimage, (0, 0))
    level.run()

    pygame.display.update()
    clock.tick(60)
