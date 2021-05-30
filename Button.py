import pygame as pg
pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)


class Button():
    def __init__(
            self,
            pos,
            size,
            outline=True,
            outline_normal=BLACK,
            outline_hover=LIGHTGRAY,
            outline_pressed=RED):
        self.pos = pos
        self.size = size
        self.outline = outline
        if self.outline:
            self.outline_normal = outline_normal
            self.outline_hover = outline_hover
            self.outline_pressed = outline_pressed
        self.pressed = False  # is the button currently pushed down?
        self.clicked = False  # Was the button completely clicked?
        self.hover = False  # is the mouse currently hovering over the button?
        # was the last mouse down event over the mouse button? (Used to track
        # clicks.)
        self.lastMouseDownOverButton = False

    def handle_event(self, event):
        if event.type not in [
                pg.MOUSEMOTION,
                pg.MOUSEBUTTONDOWN,
                pg.MOUSEBUTTONUP]:
            pass
        else:
            mouse_pos = event.pos
            if not self.hover and self.rect.collidepoint(mouse_pos):
                self.hover = True
            if self.hover and not self.rect.collidepoint(mouse_pos):
                self.hover = False
            if self.hover and event.type == pg.MOUSEBUTTONDOWN:
                self.pressed = True
                self.lastMouseDownOverButton = True
            if not self.hover and event.type == pg.MOUSEBUTTONDOWN:
                self.lastMouseDownOverButton = False
                self.clicked = False
            if self.hover and event.type == pg.MOUSEBUTTONUP and self.lastMouseDownOverButton:
                self.clicked = True
                self.pressed = False
            if not self.hover and event.type == pg.MOUSEBUTTONUP and self.lastMouseDownOverButton:
                self.clicked = False
            if self.pressed and not self.rect.collidepoint(mouse_pos):
                self.pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        if self.outline:
            if self.pressed:
                pg.draw.rect(screen, self.outline_pressed, self.rect, 1)
            elif self.hover:
                pg.draw.rect(screen, self.outline_hover, self.rect, 1)
            else:
                pg.draw.rect(screen, self.outline_normal, self.rect, 1)


class ImageButton(Button):
    def __init__(
            self,
            pos,
            size,
            image,
            outline=True,
            outline_normal=BLACK,
            outline_hover=LIGHTGRAY,
            outline_pressed=RED):
        super().__init__(
            pos,
            size,
            outline,
            outline_normal,
            outline_hover,
            outline_pressed)
        if isinstance(image, str):
            self.image = pg.transform.scale(pg.image.load(image), self.size)
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos


class TextButton(Button):
    def __init__(
            self,
            pos,
            size,
            text,
            font=pg.font.SysFont(
                None,
                48),
            font_color=RED,
            bg_color=GREEN,
            outline=True,
            outline_normal=BLACK,
            outline_hover=LIGHTGRAY,
            outline_pressed=RED):
        super().__init__(
            pos,
            size,
            outline,
            outline_normal,
            outline_hover,
            outline_pressed)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.bg_color = bg_color
        self.image = pg.Surface(self.size)
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.textbox = self.font.render(text, True, font_color)
        self.image.blit(
            self.textbox,
            (self.rect.center[0] -
             pg.Surface.get_width(
                self.textbox) //
                2,
                self.rect.center[1] -
                pg.Surface.get_height(
                self.textbox) //
                2))
        self.rect.topleft = self.pos


def test():
    tile = '/home/gunslingster/Desktop/python_projects/pygame_projects/FirstGame/Assets/Tiles/Tile_02.png'
    b = ImageButton((500, 500), (32, 32), tile)
    t = TextButton((800, 500), (100, 100), 'Start')
    screen = pg.display.set_mode((1200, 800))
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                b.handle_event(event)
                t.handle_event(event)
        b.draw(screen)
        t.draw(screen)
        pg.display.flip()


#test()
#pg.quit()
