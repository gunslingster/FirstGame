import pygame as pg
pg.init()

class Button(pg.sprite.Sprite):
    def __init__(self, size, pos, image = None, text = None, font =  pg.font.SysFont(None, 48)):
        super().__init__()
        self.size = size
        if image:
            self.image = pg.transform.scale(pg.image.load(image), (size))
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
        if text:
            self.text = text
            self.textsurface = font.render(text, False, (255,0,0))
            self.rect = self.textsurface.get_rect()
            self.rect.topleft = self.pos
        self.pressed = False

    def action(self):
        pass

    def update(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= mouse_pos[1] <= self.pos[1] + self.size[1]:
                    self.pressed = True
                    self.action()
