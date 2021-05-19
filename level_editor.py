import pygame as pg
import csv
import os
import math
vec = pg.math.Vector2
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
        tile = pg.transform.scale(pg.image.load(os.path.join(tile_directory, tile_image)), (tile_size,tile_size))
        tile_images.append(tile)
    return tile_images

class Tile():
    def __init__(self, tile_size, tile_image, pos):
        self.tile_size = tile_size
        self.image = tile_image
        self.tile_pos = pos
        self.real_pos = (pos[0]*self.tile_size, pos[1]*tile_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.real_pos
    
class Platform(pg.sprite.Sprite):
    """Form a platform by joining tiles together.
    The platform can only be made up a single type of tile.
    Size the the number of tiles.
    The platform can have a velocity."""
    def __init__(self, tile, size, pos, vel):
        super().__init__()
        self.tile = tile
        self.tile_size = self.tile.get_width()
        self.size = size
        self.image = pg.Surface((self.tile_size*size, self.tile_size))
        self.fill_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.pos = vec(pos)
        self.vel = vec(vel)
        
    def fill_image(self):
         for i in range(self.size):
             self.image.blit(self.tile, (i*self.tile_size, 0))
        
class MapEditor():
    def __init__(self, map_width=1000, map_height=1000, tile_size=32, tiles=None, background_image=None):
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.tiles = tiles
        self.background_image = background_image

    def generate_ui(self):
        self.ui_width = self.tile_size * 11
        self.ui_height = height
        self.ui_image = pg.Surface((width,height))
        self.ui_image.fill(red)
        self.ui_image.set_colorkey(white)
        self.tile_cols = 5
        self.tile_rows = math.ceil(len(self.tiles)/5)

    def display_ui(self):
        screen.blit(self.ui_image, (width - self.ui_width, 0))
        count = 0
        for i in range(self.tile_rows):
            for j in range(1,11,2):
                if count < len(self.tiles):
                    self.ui_image.blit(self.tiles[count], (j*self.tile_size, i*self.tile_size))
                    count += 1
                else:
                    break

def main():
    running = True
    test = get_tile_images(32)
    m = MapEditor(tiles=test)
    m.generate_ui()
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        screen.fill(black)
        m.display_ui()
        pg.display.flip()

main()
pg.quit()
