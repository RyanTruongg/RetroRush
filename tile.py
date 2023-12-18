import pygame
import utils


class Tile(pygame.sprite.Sprite):
    TILES_SET = utils.create_tiles_set('graphics/tiles/tiles_set.png',
                                       (32, 32), 2)

    def __init__(self, position: tuple[int], index: int = 0) -> None:
        super().__init__()
        self.colliable = index > -1

        if index == -1:
            self.image = pygame.Surface((64, 64))
            self.image.fill('Black')
        else:
            self.image = Tile.TILES_SET[index]
        self.rect = self.image.get_rect(topleft=position)
