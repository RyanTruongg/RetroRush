import os
import pygame
import json
import settings


def split_from(path: str, width: int, scaleFactor: int = 1):
    surfs: list[pygame.Surface] = []
    origin = pygame.image.load(path).convert_alpha()
    rect = origin.get_rect()
    rect.width = width
    for i in range(origin.get_width() // width):
        frame_rect = rect.copy()
        frame_rect.x += width * i
        surfs.append(
            pygame.transform.scale_by(origin.subsurface(frame_rect),
                                      scaleFactor))
    return surfs


def scale_all_by(surfaces: list[pygame.Surface], factor: int):
    return map(lambda s: pygame.transform.scale_by(s, factor), surfaces)


def create_tiles_set(path: str, size: tuple[int, int], scaleFactor: int):
    tile_width = size[0]
    tile_height = size[1]

    surfs = []
    origin = pygame.image.load(path).convert()
    sized_rect = origin.get_rect()
    sized_rect.width = tile_width
    sized_rect.height = tile_height
    for y in range(origin.get_height() // tile_height):
        for x in range(origin.get_width() // tile_width):
            tile_rect = sized_rect.copy()
            tile_rect.x += tile_width * x
            tile_rect.y += tile_height * y
            tile_rect = origin.subsurface(tile_rect)
            surfs.append(tile_rect)
    surfs = list(scale_all_by(surfs, scaleFactor))
    return surfs


def convert_to_2d_tiled_map(arr: list, rows: int, cols: int):
    _2d_arrays = []
    for cur_row in range(rows):
        row = []
        for cur_col in range(cols):
            row.append(arr[cur_row * cols + cur_col] - 1)
        _2d_arrays.append(row)
    return _2d_arrays


class LevelData():

    def __init__(self, level_number: int) -> None:
        map_path = f'levels/level_{level_number}/map.tmj'
        f = open(map_path, "r")
        map_data = json.load(f)
        f.close()

        self.cols = int(map_data['width'])
        self.rows = int(map_data['height'])

        ground_layer = list(
            filter(lambda x: x['name'] == 'ground', map_data['layers']))[0]
        self.ground_layer_2d = convert_to_2d_tiled_map(ground_layer['data'],
                                                       self.rows, self.cols)

        player_layer = list(
            filter(lambda x: x['name'] == 'player', map_data['layers']))[0]
        self.entity_layer_2d = convert_to_2d_tiled_map(player_layer['data'],
                                                       self.rows, self.cols)

    def get_screen_width(self):
        return self.cols * settings.TILE_SIZE

    def get_screen_height(self):
        return self.rows * settings.TILE_SIZE
