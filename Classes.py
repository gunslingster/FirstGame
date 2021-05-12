# This will be a game class to help organize the code
import pygame as pg
import random
from Settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((30,50))
        self.image.fill(red)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2,height/2)
        self.pos = vec(width/2,height/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()
        
    def update(self):
        self.all_sprites.update()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
                
        


    