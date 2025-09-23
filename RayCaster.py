import pygame
from Settings import *
from Ray import Ray
from Map import Map

class Raycaster:
    def __init__(self, player, map):
        self.rays = []
        self.player = player
        self.map = map

    def castAllRays(self):
        self.rays = []
        ray_angle = (self.player.rotation_angle - FOV / 2)
        for i in range(NUM_RAYS):
            ray = Ray(ray_angle,self.player,self.map)
            ray.cast()
            self.rays.append(ray)

            ray_angle += FOV / (NUM_RAYS - 1)  

    def drawAllRays(self, screen):
        counter = 0
        
        for ray in self.rays:
            # ray.draw_ray(screen)

            line_height = (32 / ray.distance) * 415

            draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
            draw_end = line_height

            pygame.draw.rect(screen, (0,255,0), (counter * RES, draw_begin, RES, draw_end))
            
            counter += 1
    
    