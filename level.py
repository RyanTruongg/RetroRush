import pygame
import settings
import utils
from tile import Tile
from player import Player
import enemy


class Level(pygame.sprite.Sprite):

    def __init__(self, level_number: int) -> None:
        super().__init__()
        self.display = pygame.display.get_surface()
        self.level_data = utils.LevelData(level_number)
        self.level_surf = pygame.surface.Surface(
            (self.level_data.get_screen_width(),
             self.level_data.get_screen_height()))

        self.tiles_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()

        for r in range(self.level_data.rows):
            for c in range(self.level_data.cols):
                screenx = c * settings.TILE_SIZE
                screeny = r * settings.TILE_SIZE
                tile_id = int(self.level_data.ground_layer_2d[r][c])
                self.tiles_group.add(Tile((screenx, screeny), tile_id))

                if int(self.level_data.entity_layer_2d[r][c]) == 15:
                    self.player_group.add(Player((screenx, screeny)))
                if int(self.level_data.entity_layer_2d[r][c]) == 16:
                    self.enemy_group.add(enemy.Enemy((screenx, screeny)))

        self.offsety = settings.CENTER_Y - self.player_group.sprite.hit_box_rect.y

    def get_player_sprite(self) -> Player:
        return self.player_group.sprite

    def run(self):
        self.level_surf.fill('Black')

        self.tiles_group.update()
        self.player_group.update(collidable_sprites=self.tiles_group.sprites(),
                                 enemy_sprites=self.enemy_group.sprites())
        self.enemy_group.update(collidable_sprites=self.tiles_group.sprites())

        self.tiles_group.draw(self.level_surf)
        self.enemy_group.draw(self.level_surf)
        self.player_group.draw(self.level_surf)

        if settings.DEBUG:
            pygame.draw.rect(
                self.level_surf,
                'Red',
                self.player_group.sprite.rect,
                width=1,
            )
            pygame.draw.rect(
                self.level_surf,
                'Green',
                self.player_group.sprite.hit_box_rect,
                width=1,
            )
            pygame.draw.rect(
                self.level_surf,
                'Blue',
                self.player_group.sprite.attack_hit_box_rect,
                width=1,
            )

        offsetx = settings.CENTER_X - self.player_group.sprite.hit_box_rect.x
        offsetx = min(offsetx, 0)
        offsetx = max(offsetx,
                      -(self.level_surf.get_width() - settings.SCREEN_WIDTH))

        self.display.fill('Black')
        self.display.blit(self.level_surf, (offsetx, self.offsety))
