# Some global declarations and settings
# Game settings
from pygame import font
font.init()
import os

title = "Platformer"
width = 960
height = 640
fps = 60
project_path = os.path.dirname(os.path.realpath(__file__))


# define colors and fonts
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
font1 = font.SysFont(None, 48)
tile_size = 32

# Player settings
player_acceleration = 0.5
player_friction = -0.12
