import pygame
from Settings import *

class Map:
    def __init__(self):
        self.grid = [  
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def has_wall_at(self, x, y)->bool: ##This uses pixel coords, so you'll have to divide by tilesize to get the grid coords
        return self.grid[int(y // TILESIZE)][int(x // TILESIZE)]
     
    def draw_map(self,screen):
        for y in range(len(self.grid)): ##Rows are Y, Cols are X
            for x in range(len(self.grid[0])):
                tile_x = x * TILESIZE
                tile_y = y * TILESIZE

                if self.grid[y][x] == 0:
                    pygame.draw.rect(screen, (255,255,255),( tile_x, tile_y,TILESIZE - 1 ,TILESIZE - 1))
                elif self.grid[y][x] == 1:
                    pygame.draw.rect(screen, (40,40,40), (tile_x, tile_y, TILESIZE - 1,TILESIZE - 1))
