import pygame
import settings
from tile import Tile
from player import Player


class Level(pygame.sprite.Sprite):

    def __init__(self, level_map: list[list]) -> None:
        super().__init__()
        self.display = pygame.display.get_surface()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.world_shift = 0
        for row_idx, row in enumerate(level_map):
            for col_idx, col in enumerate(row):
                x = col_idx * settings.TILE_SIZE
                y = row_idx * settings.TILE_SIZE

                if row_idx == 10 and col_idx == 1:
                    self.player_group.add(Player((x, y), self.display))

                self.tiles_group.add(
                    Tile((x, y), int(level_map[row_idx][col_idx])))

    def scroll_x(self):
        player = self.get_player_sprite()
        left_border = settings.SCREEN_WIDTH // 4
        right_border = settings.SCREEN_WIDTH - (settings.SCREEN_WIDTH // 4)
        if player.hit_box_rect.x >= right_border and player.direction.x > 0:
            self.world_shift = -5
            player.speed = 0
        elif player.hit_box_rect.x <= left_border and player.direction.x < 0:
            self.world_shift = 5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def get_player_sprite(self) -> Player:
        return self.player_group.sprite

    def run(self):
        self.display.fill('Black')

        self.tiles_group.update(self.world_shift)
        self.tiles_group.draw(self.display)

        self.player_group.update(sprites=self.tiles_group.sprites())
        self.player_group.draw(self.display)
        self.scroll_x()
