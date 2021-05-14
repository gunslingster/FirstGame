import pygame
import os
from Settings import *

pygame.init()
width = 1000
height = 1000
screen = pygame.display.set_mode((width,height))
screen.fill((0,0,0))

class Map():
    def __init__(self, map_file, width, height):
        self.map_file = map_file
        self.width = width
        self.height = height
        self.map = self.process_map()
        self.tile_size = self.width // len(self.map[0])

    def process_map(self):
        f = open(self.map_file, 'r+')
        lines = [[int(char) for char in list(line.replace('\n', ''))] for line in f.readlines()]
        return lines

    def generate_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 1:
                    tile_rect = pygame.Rect(j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size)
                    pygame.draw.rect(screen, (0,255,0), tile_rect)


test = Map(os.path.join(project_path, "maps/maps.txt"), 1000, 1000)
mymap = test.process_map()
test.generate_map()
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
print(mymap)
main()
pygame.quit()


