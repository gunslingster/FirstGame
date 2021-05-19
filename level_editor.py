import pygame as pg
import csv
import os
pg.init()

# Setting up the window
width = 1200
height = 800
screen = pg.display.set_mode((width,height))

# Setting some basic colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

def get_tile_images(tile_size):
    tile_directory = input('Enter tile directory: ')
    tile_images = []
    for tile_image in os.listdir(tile_directory):
        print(tile_image)
        tile = pg.transform.scale(pg.image.load(os.path.join(tile_directory, tile_image)), (tile_size,tile_size))
        tile_images.append(tile)
    return tile_images

class MapEditor():
    def __init__(self, map_width=1000, map_height=1000, tile_size=32, tile_images=None, background_image=None):
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.tile_images = tile_images
        self.background_image = background_image

    def generate_ui(self):
        self.ui_width = self.tile_size * 10
        self.ui_height = height
        self.ui_image = pg.Surface((width,height))
        self.ui_image.fill(red)
        self.ui_image.set_colorkey(white)

    def display_ui(self):
        screen.blit(self.ui_image, (width - self.ui_width, 0))

m = MapEditor()
m.generate_ui()
m.display_ui()
pg.display.flip()

