import pygame
import utils


class Tile(pygame.sprite.Sprite):

    TILES_SET = utils.create_tiles_set('graphics/tiles/tiles_set.png',
                                       (32, 32), 2)

    def __init__(self, position: tuple[int], index: int = 0) -> None:
        super().__init__()
        self.colliable = index != 10
        self.image = Tile.TILES_SET[index]
        self.rect = self.image.get_rect(topleft=position)

    def update(self, world_shift: int):
        self.rect.x += world_shift
