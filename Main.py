# Sprite classes for platform game
import pygame as pg
from Settings import *
from Classes import *

g = Game()
while g.running:
    g.start_game()

pg.quit()