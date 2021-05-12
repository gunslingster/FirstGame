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
        
    def update(self):
        # Gravity
        self.acc = vec(0,0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.5
        if keys[pg.K_LEFT]:
            self.acc.x = -0.5
        
        # Friction
        self.acc.x += self.vel.x * player_friction
        
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # wrap around the sides of the screen
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.bg = pg.transform.scale(pg.image.load('jungle_bg.png'), (width,height))
        self.running = True
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        p1 = Platform(0, height - 40, width, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(width / 2 - 50, height * 3 / 4, 100, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        self.run()
        
    def update(self):
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0
            self.player.rect.midbottom = self.player.pos
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    def draw(self):
        self.screen.blit(self.bg, (0,0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(fps)
                
        


    