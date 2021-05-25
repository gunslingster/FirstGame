import pygame as pg
pg.init()

class Button():
    def __init__(self, size, pos, content, outline=False):
        self.size = size
        self.pos = pos
        self.content = content
        self.outline = outline
        self.clicked = False

    def draw(self):
        pass

    def action(self):
        pass

    def update(self):
        pass

class TileButton(Button):
    def __init__(self, pos, tile):
        self.pos = pos
        self.tile = tile
        self.rect = self.tile.get_rect()
        self.rect.topleft = self.pos
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.tile,self.rect)

    def action(self):
        if self.clicked:
            self.clicked = False
            return self.tile

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True
                    print('click')
