import pygame as pg
import csv
from Button import *
from Settings import *
from utils import *
vec = pg.math.Vector2
pg.init()

# Setting up the window
width = 1312 # 32 * 41
height = 640 # 32 * 20
screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()

# Setting some basic colors
black = (0,0,0)
white = (255,255,255)
gray = (205,205,205)
red = (255,0,0)
green = (0,255,0)

tiles, tile_mapping, index_mapping = get_tile_images(32)

class Level():
    def __init__(self, level_width=960, level_height=640, tile_size=32, level_data=None):
        self.tile_size = tile_size
        if level_data is not None:
            self.level_width = len(level_data[0])*self.tile_size
            self.level_height = len(level_data)*self.tile_size
            self.data = level_data
        else:
            self.level_width = level_width
            self.level_height = level_height
            self.data = [[0]*(self.level_width//tile_size) for i in range(self.level_height//tile_size)]
        self.image = pg.Surface((self.level_width, self.level_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

    def add_tile(self, tile_index, index):
        self.data[index[1]][index[0]] = tile_index

    def del_tile(self, index):
        self.data[index[1]][index[0]] = 0

    def draw(self):
        for i in range(self.level_height//self.tile_size):
            for j in range(self.level_width//self.tile_size):
                self.image.blit(tile_mapping[self.data[i][j]], (j*self.tile_size, i*self.tile_size))
        draw_grid(self.image)



class MapEditor():
    def __init__(self, tiles):
        self.running = True
        self.tiles = tiles
        self.tile_size = self.tiles[0].get_width()
        self.bg = pg.transform.scale(pg.image.load('Background.png'), (960, 640))
        self.setup()
        self.level = Level()

    def setup(self):
        # There will be two screens
        # One screen is for the ui with all the butoons
        # The other screen is to add tiles and edit the map
        self.ui_screen = pg.Surface((352, 640))
        self.ui_screen.fill(LIGHTGRAY)
        self.editor_screen = pg.Surface((960, 640))
        self.tile_buttons = []
        self.tile_clicked = None
        self.tile_index = 0
        self.scroll = 0
        # Will have 5 tiles per row
        rows = len(self.tiles)//5 + 1
        count = 0
        for i in range(rows+1):
            for j in range(1,11,2):
                if count < len(self.tiles):
                    tile_button = ImageButton((960+j*self.tile_size,i*self.tile_size), (self.tile_size,self.tile_size), self.tiles[count])
                    self.tile_buttons.append(tile_button)
                    count += 1
                else:
                    break
        self.save_button = TextButton((960+3*self.tile_size, 13*self.tile_size), (5*self.tile_size, 1*self.tile_size), 'SAVE LEVEL')
        self.load_button = TextButton((960+3*self.tile_size, 15*self.tile_size), (5*self.tile_size, 1*self.tile_size), 'LOAD LEVEL')
        self.new_button = TextButton((960+3*self.tile_size, 17*self.tile_size), (5*self.tile_size, 1*self.tile_size), 'NEW LEVEL')

    def draw(self):
        screen.blit(self.ui_screen, (960,0))
        self.level.draw()
        self.editor_screen.blit(self.level.image, self.level.rect)
        screen.blit(self.editor_screen, (0,0))
        for button in self.tile_buttons:
            button.draw(screen)
        self.save_button.draw(screen)
        self.load_button.draw(screen)
        self.new_button.draw(screen)

    def new_level(self):
        level_width = int(input('Enter level width: '))
        level_height =int(input('Enter level height: '))
        self.level = Level(level_width, level_height, self.tile_size)

    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    if self.level.rect.right <= self.editor_screen.get_width():
                        pass
                    else:
                        self.scroll += 1
                        self.level.rect.left -= 1*self.tile_size
                if event.key == pg.K_LEFT:
                    if self.level.rect.left + 1 > 0:
                        pass
                    else:
                        self.scroll -= 1
                        self.level.rect.left += 1*self.tile_size
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.editor_screen.get_rect().collidepoint(event.pos):
                    if self.tile_clicked is not None:
                        tile_pos = (event.pos[0]//self.tile_size + self.scroll, event.pos[1]//self.tile_size)
                        self.level.add_tile(index_mapping[self.tile_clicked], tile_pos)
            if event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[0]:
                if self.editor_screen.get_rect().collidepoint(event.pos):
                    if self.tile_clicked is not None:
                        tile_pos = (event.pos[0]//self.tile_size + self.scroll, event.pos[1]//self.tile_size)
                        self.level.add_tile(index_mapping[self.tile_clicked], tile_pos)
            for button in self.tile_buttons:
                button.handle_event(event)
                if button.clicked:
                    self.tile_clicked = button.image
            self.save_button.handle_event(event)
            self.load_button.handle_event(event)
            self.new_button.handle_event(event)
            if self.save_button.clicked:
                level_name = input('Enter level name: ')
                level_to_csv(self.level.data, level_name)
                self.running = False
            if self.load_button.clicked:
                level_directory = input('Enter csv directory: ')
                data = csv_to_level(level_directory)
                self.level = Level(level_data=data)
                self.load_button.clicked = False
            if self.new_button.clicked:
                self.new_level()
                self.new_button.clicked = False



def test():
    m = MapEditor(tiles)
    while m.running:
        m.events()
        m.draw()
        pg.display.flip()
        clock.tick(30)
test()
pg.quit()
