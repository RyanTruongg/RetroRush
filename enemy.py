import pygame
import entity


class Enemy(entity.Entity):

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.image = pygame.Surface((32, 64))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center=position)

    def update(self, collidable_sprites: list[pygame.sprite.Sprite]) -> None:
        super().update(collidable_sprites)
        self.rect = self.image.get_rect(center=self.hit_box_rect.center)
