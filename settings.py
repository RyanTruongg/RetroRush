import csv


def load_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


LEVEL_MAP = load_csv('levels\\level_1_ground.csv')
TILE_SIZE = 64
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DEBUG = True
