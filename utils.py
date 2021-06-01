import pygame as pg
from Settings import *
import os
import csv
import math

pg.init()

def round_down(num):
    if num < 0:
        return math.ceil(num)
    else:
        return math.floor(num)

def csv_to_level(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = [list(map(int ,row)) for row in data]
    return data

def draw_grid(surface, spacing=32, color=red):
    for i in range(surface.get_width()):
        pg.draw.line(surface, color, (i*spacing, 0), (i*spacing, surface.get_height()))
    for i in range(surface.get_height()):
        pg.draw.line(surface, color, (0, i*spacing), (surface.get_width(), i*spacing))

def get_tile_images(tile_size):
    #tile_directory = input('Enter tile directory: ')
    tile_directory = os.path.join(project_path, 'Assets/Tiles')
    tile_images = []
    tile_mapping = {}
    for tile_image in os.listdir(tile_directory):
        tile_index = int(tile_image[-6:-4])
        tile = pg.transform.scale(pg.image.load(os.path.join(tile_directory, tile_image)), (tile_size,tile_size))
        tile_images.append(tile)
        tile_mapping[tile_index] = tile
    blank = pg.Surface((tile_size, tile_size))
    tile_images.append(blank)
    tile_mapping[0] = blank
    index_mapping = {v:k for k,v in tile_mapping.items()}
    return tile_images, tile_mapping, index_mapping

def level_to_csv(level, level_name):
    with open(level_name + '.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(level)
