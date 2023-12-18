import pygame
import settings
from tile import Tile
from player import Player


class Level(pygame.sprite.Sprite):

    def __init__(self, level_map: list[list]) -> None:
        super().__init__()
        self.display = pygame.display.get_surface()
        self.ground_surf = pygame.surface.Surface(
            (len(level_map[0]) * settings.TILE_SIZE,
             len(level_map) * settings.TILE_SIZE))

        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()

        for row_idx, row in enumerate(level_map):
            for col_idx, _ in enumerate(row):
                x = col_idx * settings.TILE_SIZE
                y = row_idx * settings.TILE_SIZE

                self.tiles_group.add(
                    Tile((x, y), int(level_map[row_idx][col_idx])))

                if row_idx == 13 and col_idx == 4:
                    self.player_group.add(Player((x, y)))

        self.offsety = settings.CENTER_Y - self.player_group.sprite.hit_box_rect.y

    def get_player_sprite(self) -> Player:
        return self.player_group.sprite

    def run(self):
        self.ground_surf.fill('Black')

        self.tiles_group.update()
        self.tiles_group.draw(self.ground_surf)

        self.player_group.update(sprites=self.tiles_group.sprites())
        self.player_group.draw(self.ground_surf)

        if settings.DEBUG:
            pygame.draw.rect(
                self.ground_surf,
                'Red',
                self.player_group.sprite.rect,
                width=1,
            )
            pygame.draw.rect(
                self.ground_surf,
                'Green',
                self.player_group.sprite.hit_box_rect,
                width=1,
            )

        offsetx = settings.CENTER_X - self.player_group.sprite.hit_box_rect.x

        self.display.fill('Black')
        self.display.blit(self.ground_surf, (offsetx, self.offsety))
