# This will be a game class to help organize the code
import pygame as pg
import random
from Settings import *
import os
import math
vec = pg.math.Vector2

def round_down(num):
    if num < 0:
        return math.ceil(num)
    else:
        return math.floor(num)

class Button(pg.sprite.Sprite):
    def __init__(self, pos=(100,100), size=(100,40), text='BUTTON', color=red, font=font1):
        super().__init__()
        self.pos = pos
        self.size = size
        self.text = text
        self.color = color
        self.font = font
        self.textsurface = font.render(text, False, color)
        self.rect = self.textsurface.get_rect()
        self.rect.center = self.pos
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.textsurface, self.rect.topleft)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True

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
        self.platforms = pg.sprite.Group()
        self.player = Player((30,50))
        self.all_sprites.add(self.player)
        p1 = Platform(0, height - 40, width, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(width / 2 - 50, height * 3 / 4, 100, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        p3 = Platform(900, height-90,30,50)
        self.all_sprites.add(p3)
        self.platforms.add(p3)
        self.camera = Camera(width,height)
        self.run()

    def update(self):
        # Update Sprites
        self.all_sprites.update(self.platforms)
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
        start_button = Button(text='START GAME', pos=(600,400))
        while start_button.clicked == False:
            self.screen.blit(self.bg, (0,0))
            start_button.draw(self.screen)
            start_button.events()
            pg.display.flip()
        self.new()









