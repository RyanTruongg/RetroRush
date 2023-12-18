import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, location: tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface(32, 64)
        self.image.fill('Red')
        self.rect = self.image.get_rect(center=location)
