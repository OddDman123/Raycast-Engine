import pygame
from Settings import *
from Ray import Ray
from Map import Map

class Raycaster:
    def __init__(self, player, map):
        self.rays = []
        self.player = player
        self.map = map
        self.fov = FOV
        self.zbuffer = [0] * WINDOW_WIDTH

    def get_z_buffer(self) -> list:
        return self.zbuffer
    
    def castAllRays(self):
        self.rays = []
        # ray_angle = (self.player.rotation_angle - self.fov / 2)
        xx = -(WINDOW_WIDTH / 2)
        maxfov = (WINDOW_WIDTH / 2) / math.tan(self.fov / 2)
        
        for i in range(NUM_RAYS):
            ray_angle = self.player.rotation_angle + math.atan(xx / maxfov) #* 0.0174533) * 57.2958

            ray = Ray(ray_angle,self.player,self.map)
            ray.cast()
            self.rays.append(ray)

            self.zbuffer[i] = ray.distance
            
            # ray_angle += self.fov / (NUM_RAYS - 1)
            xx += (WINDOW_WIDTH / NUM_RAYS)  

    def change_FOV(self, new_FOV):
        self.fov = new_FOV

    def drawAllRays(self, screen, texture):
        counter = 0
        
        for ray in self.rays:
            # ray.draw_ray(screen)
            maxfov = (WINDOW_WIDTH / 2) / math.tan(self.fov / 2)

            

            if ray.distance > 0:
                line_height = (maxfov / ray.distance) * WALLHEIGHT
                # was line_height = (ceiling_height / ray_distance) * 415 (415 being distance to projected plane)
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
            scaled_texture_slice.fill((ray.color, ray.color, ray.color), special_flags=pygame.BLEND_RGBA_MULT)

            screen.blit(scaled_texture_slice, (counter * RES, draw_begin))

            #pygame.draw.rect(screen, (0,255,0), (counter * RES, draw_begin, RES, draw_end))
            
            counter += 1
    
    