import pygame as pg
import csv
import os
import math
from Button import *
vec = pg.math.Vector2
pg.init()

# Setting up the window
width = 1280
height = 640
screen = pg.display.set_mode((width,height))

# Setting some basic colors
black = (0,0,0)
white = (255,255,255)
gray = (205,205,205)
red = (255,0,0)
green = (0,255,0)

def get_tile_images(tile_size):
    tile_directory = input('Enter tile directory: ')
    tile_images = []
    for tile_image in os.listdir(tile_directory):
        print(tile_image)
        tile_index = int(tile_image[-6:-4])
        tile = pg.transform.scale(pg.image.load(os.path.join(tile_directory, tile_image)), (tile_size,tile_size))
        tile_images.append(tile)
    return tile_images

def draw_grid(surface, spacing, color):
    for i in range(surface.get_width()):
        pg.draw.line(surface, color, (i*spacing, 0), (i*spacing, height))
    for i in range(surface.get_height()):
        pg.draw.line(surface, color, (0, i*spacing), (width, i*spacing))


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
        self.generate_ui()
        self.create_level()
        self.tile_clicked = None

    def generate_ui(self):
        self.ui_width = self.tile_size * 11
        self.ui_height = height
        self.ui_screen = pg.Surface((self.ui_width,self.ui_height))
        self.editor_screen = pg.Surface((width-self.ui_width,height))
        self.editor_screen.fill(gray)
        self.ui_screen.fill(green)
        self.ui_screen.set_colorkey(white)
        self.tile_cols = 5
        self.tile_rows = math.ceil(len(self.tiles)/5)
        self.tile_buttons = []
        count = 0
        for i in range(self.tile_rows):
            for j in range(1,11,2):
                if count < len(self.tiles):
                    tile_button = ImageButton((width-self.ui_width+j*self.tile_size,i*self.tile_size), (self.tile_size, self.tile_size), self.tiles[count])
                    self.tile_buttons.append(tile_button)
                    count += 1
                else:
                    break

    def draw(self, screen):
        screen.blit(self.editor_screen, (0,0))
        screen.blit(self.ui_screen, (width-self.ui_width, 0))
        draw_grid(self.level, self.tile_size, red)
        self.editor_screen.blit(self.level, self.level_pos)
        for button in self.tile_buttons:
            button.draw(screen)

    def create_level(self):
        self.level = pg.Surface((self.map_width*self.tile_size*self.map_size, self.map_height*self.tile_size))
        self.level_rect = self.level.get_rect()
        self.level_pos = [0,0]
        self.level_info = []
        cols = self.map_width*self.map_size
        rows = self.map_height
        for i in range(rows):
            self.level_info.append([0]*cols)

    def insert_tile(self, tile, pos):
        self.level.blit(tile, pos)

def main():
    running = True
    tiles = get_tile_images(32)
    m = MapEditor(tiles=tiles)
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            for button in m.tile_buttons:
                button.handle_event(event)
                if button.clicked:
                    m.tile_clicked = button.image
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if m.editor_screen.get_rect().collidepoint(mouse_pos):
                    if m.tile_clicked is not None:
                        x = (mouse_pos[0]//m.tile_size) * m.tile_size
                        y = (mouse_pos[1]//m.tile_size) * m.tile_size
                        m.level.blit(m.tile_clicked, (x,y))
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                   m.level_pos[0] += m.tile_size
                if event.key == pg.K_RIGHT:
                   m.level_pos[0] -= m.tile_size
        screen.fill(black)
        m.draw(screen)
        pg.display.flip()

main()
pg.quit()
