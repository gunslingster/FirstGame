import pygame as pg
import os
from Settings import *

pg.init()
width = 1000
height = 1000
screen = pg.display.set_mode((width,height))
test_map = 'Assets/Maps/map_01.txt'

screen.fill((0,0,0))
class Tile():
    def __init__(self, image, tile_size):
        self.image = pg.transform.scale(pg.image.load(image), (tile_size,tile_size))
        self.tile_size = tile_size
        self.rect = self.image.get_rect()
    
    def draw(self, screen, pos):
        screen.blit(self.image, pos)

class Map():
    def __init__(self, map_file, width, height):
        self.map_file = map_file
        self.width = width
        self.height = height
        self.map = self.process_map()
        self.tile_size = self.width // len(self.map[0])
        self.tile = Tile('Assets/Tiles/Tile_02.png', self.tile_size)

    def process_map(self):
        f = open(self.map_file, 'r+')
        lines = [[int(char) for char in list(line.replace('\n', ''))] for line in f.readlines()]
        return lines

    def generate_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 1:
                    self.tile.draw(screen, (j*self.tile.tile_size, i*self.tile.tile_size))

test = Map(test_map, 1000, 1000)
test.generate_map()
pg.display.flip()


