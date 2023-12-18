import os
import pygame
import json


def bulk_import(path: str):
    surfs: list[pygame.Surface] = []
    for _, __, files in os.walk(path):
        for file in files:
            surfs.append(pygame.image.load(path + '/' + file))

    return surfs


def split_from(path: str, width: int, scaleFactor: int = 1):
    surfs: list[pygame.Surface] = []
    origin = pygame.image.load(path)
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


def read_level_map_data(level: int):
    map_path = f'levels/level_{level}/map.tmj'
    f = open(map_path, "r")
    map_data = json.load(f)

    layer = map_data['layers'][0]
    width = layer['width']
    height = layer['height']

    layer_data = layer['data']
    layer2d = []
    for r in range(height):
        row = []
        for c in range(width):
            row.append(layer_data[r * width + c] - 1)
        layer2d.append(row)
    return layer2d
