import pygame as pg
pg.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKGRAY = (64,64,64)
GRAY = (128,128,128)
LIGHTGRAY = (212,208,200)

class Button():
    def __init__(self, pos, size):
        pass
    
    def handle_event(self, event):
        pass
    
    def draw(self, screen):
        pass
    
class ImageButton(Button):
    def __init__(self, pos, size, image, outline=True, outline_normal = BLACK, outline_hover = LIGHTGRAY, outline_pressed = RED):
        self.pos = pos
        self.size = size
        if type(image) == str:
            self.image = pg.transform.scale(pg.image.load(image), size)
        else:
            self.image = image
        
        self.outline = outline
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        if self.outline:
            self.outline_normal = outline_normal
            self.outline_hover = outline_hover
            self.outline_pressed = outline_pressed
        
        self.pressed = False # is the button currently pushed down?
        self.clicked = False # Was the button completely clicked? 
        self.hover = False  # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False # was the last mouse down event over the mouse button? (Used to track clicks.)
    
    def handle_event(self, event):
        if event.type not in [pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
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
            if self.hover and event.type == pg.MOUSEBUTTONUP and self.lastMouseDownOverButton == True:
                self.clicked = True
                self.pressed = False
            if not self.hover and event.type == pg.MOUSEBUTTONUP and self.lastMouseDownOverButton == True:
                self.clicked = False
            if self.pressed  and not self.rect.collidepoint(mouse_pos):
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
                
def test():
    tile = 'C:/Users/sabrahams/Desktop/pygame/FirstGame/Assets/Tiles/Tile_02.png'
    b = ImageButton((500,500), (32,32), tile)
    screen = pg.display.set_mode((1200,800))
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                b.handle_event(event)
                b.draw(screen)
                pg.display.flip()

test()
pg.quit()
                
            
                
                
        
            
                
            
        
        
            
        
            
        
        