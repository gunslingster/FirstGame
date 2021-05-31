# This will be a game class to help organize the code
import pygame as pg
import random
from Settings import *
from Button import *
from utils import *
vec = pg.math.Vector2

tiles, tile_mapping, index_mapping = get_tile_images(32)

class Tile(pg.sprite.Sprite):
    def __init__(self, tile_size, tile_image, pos, tile_index):
        super().__init__()
        self.tile_size = tile_size
        if isinstance(tile_image, str):
            self.image = pg.transform.scale(pg.image.load(tile_image), size)
        else:
            self.image = tile_image
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

def generate_level_tiles(level_csv):
    data = csv_to_level(level_csv)
    tiles = pg.sprite.Group()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != 0:
                tile = Tile(tile_size, tile_mapping[data[i][j]], (j*tile_size, i*tile_size), data[i][j])
                tiles.add(tile)
    return tiles

class Player(pg.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.image = pg.Surface(size)
        self.image.fill(red)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2,height/2)
        self.pos = vec(width/2,height/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.falling = False

    def jump(self, force):
        if self.falling == False:
            vy = -int(math.sqrt(2*force/5))
            self.vel.y += vy
            self.falling = True

    def update(self,blocks):
        # Gravity
        self.acc = vec(0,0.5)
        # Get input
        keys = pg.key.get_pressed()
        def updatex():
            if keys[pg.K_RIGHT]:
                self.acc.x = 0.5
            if keys[pg.K_LEFT]:
                self.acc.x = -0.5
            # Friction
            self.acc.x += self.vel.x * player_friction
            # Equations of motion
            self.vel.x += self.acc.x
            self.pos.x += self.vel.x + 0.5 * self.acc.x
            self.pos.x = self.pos.x
            self.rect.midbottom = self.pos
            hit_list = [hit for hit in blocks if self.rect.colliderect(hit.rect)]
            for hit in hit_list:
                if self.vel.x > 0:
                    self.vel.x = 0
                    self.acc.x = 0
                    self.pos.x = hit.rect.left - self.size[0]//2
                    self.rect.right = hit.rect.left
                if self.vel.x < 0:
                    self.vel.x = 0
                    self.acc.x = 0
                    self.pos.x = hit.rect.right + self.size[0]//2
                    self.rect.left = hit.rect.right
        def updatey():
            if keys[pg.K_UP]:
                self.jump(500)
            # Equations of motion
            self.vel.y += self.acc.y
            self.pos.y += math.ceil(self.vel.y + 0.5 * self.acc.y)
            self.rect.midbottom = self.pos
            hit_list = pg.sprite.spritecollide(self,blocks,False)
            for hit in hit_list:
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.acc.y = 0
                    self.pos.y = hit.rect.top
                    self.rect.bottom = self.pos.y
                    self.falling = False
                if self.vel.y < 0:
                    self.vel.y = 0
                    self.acc.y = 0
                    self.pos.y = hit.rect.bottom + self.size[1]
                    self.rect.bottom = self.pos.y
        updatex()
        updatey()

    def display_position(self):
        textsurface = font1.render('Position: ' + str(int(self.pos.x)) + ',' + str(int(self.pos.y)), False, (0, 0, 0))
        return textsurface

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Camera():
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + width//2
        y = -target.rect.y + height//2

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - width), x)
        y = max(-(self.height - height), y)
        self.camera = pg.Rect(x,y,self.width,self.height)

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.bg = pg.transform.scale(pg.image.load('Background.png'), (width,height))
        self.bgx = 0
        self.bgx2 = self.bg.get_width()
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.tiles = generate_level_tiles(level01)
        for tile in self.tiles:
            self.all_sprites.add(tile)
        self.player = Player((30,50))
        self.all_sprites.add(self.player)
        self.camera = Camera(1920,height)
        self.run()

    def update(self):
        # Update Sprites
        self.all_sprites.update(self.tiles)
        self.camera.update(self.player)

        # Update background
        self.bgx -= round_down(self.player.vel.x)  # Move both background images back
        self.bgx2 -= round_down(self.player.vel.x)

        if self.bgx < -self.bg.get_width():  # If our bg is at the -width then reset its position
            self.bgx = self.bg.get_width()

        if self.bgx2 < -self.bg.get_width():
            self.bgx2 = self.bg.get_width()

        if self.bgx > self.bg.get_width():
            self.bgx = -self.bg.get_width()

        if self.bgx2 > self.bg.get_width():
            self.bgx2 = -self.bg.get_width()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.screen.blit(self.bg, (self.bgx, 0))  # draws our first bg image
        self.screen.blit(self.bg, (self.bgx2, 0))  # draws the seconf bg image
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.player.display_position(), (0,0))
        pg.display.flip()

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(fps)

    def start_game(self):
        self.start_button = TextButton((600,400), (100,50), 'START GAME')
        while self.start_button.clicked == False:
            for event in pg.event.get():
                self.start_button.handle_event(event)
                self.screen.blit(self.bg, (0,0))
                self.start_button.draw(self.screen)
                pg.display.flip()
        self.new()
