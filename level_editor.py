import pygame as pg
import csv
import os
import math
vec = pg.math.Vector2
pg.init()

# Setting up the window
width = 1280
height = 640
screen = pg.display.set_mode((width,height))

# Setting some basic colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

path = 'C:/Users/sabrahams/Desktop/pygame/FirstGame/Assets/Tiles'

def get_tile_images(tile_size):
    #tile_directory = input('Enter tile directory: ')
    tile_directory = path
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
        
class MapEditor():
    def __init__(self, map_width=30, map_height=20, map_size = 3, tile_size=32, tiles=None, bg=None):
        self.map_width = map_width
        self.map_height = map_height
        self.map_size = map_size
        self.tile_size = tile_size
        self.tiles = tiles
        self.bg = pg.transform.scale
        self.create_level()
        self.tile_clicked = None

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
    
    def create_level(self):
        self.level = pg.Surface((self.map_width*self.tile_size*self.map_size, self.map_height*self.tile_size))
        self.level_info = []
        cols = self.map_width*self.map_size
        rows = self.map_height
        for i in range(rows):
            self.level_info.append([0]*cols)
        
            
def main():
    running = True
    test = get_tile_images(32)
    m = MapEditor(tiles=test)
    m.generate_ui()
    m.create_level()
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
