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

    def drawAllRays(self, screen, texture):
        counter = 0
        
        for ray in self.rays:
            # ray.draw_ray(screen)
            if ray.distance != 0:
                line_height = (32 / ray.distance) * 415
            else:
                line_height = 0

            draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
            # draw_end = line_height
            

            wall_percent = int((ray.wall_hit_x % TILESIZE)) / TILESIZE
            if ray.verticle:
                wall_percent = int((ray.wall_hit_y % TILESIZE)) / TILESIZE

            texture_x =  (texture.get_width() * wall_percent)
            
            texture_slice = texture.subsurface((texture_x, 0, 1, texture.get_height()))

            scaled_texture_slice = pygame.transform.scale(texture_slice, (RES, line_height))
            scaled_texture_slice.convert_alpha()
            scaled_texture_slice.fill((ray.color, ray.color, ray.color), special_flags=pygame.BLEND_RGBA_MIN)

            screen.blit(scaled_texture_slice, (counter * RES, draw_begin))

            #pygame.draw.rect(screen, (0,255,0), (counter * RES, draw_begin, RES, draw_end))
            
            counter += 1
    
    