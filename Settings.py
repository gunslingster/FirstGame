# Some global declarations and settings
# Game settings
from pygame import font
font.init()

title = "Platformer"
width = 1200
height = 800 
fps = 60
project_path = '/home/gunslingster/Desktop/python_projects/pygame_projects/first_game/FirstGame'


# define colors and fonts
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
font1 = font.SysFont(None, 48)

# Player settings
player_acceleration = 0.5
player_friction = -0.12

