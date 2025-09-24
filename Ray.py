import math
import pygame
from Settings import *
from Map import Map

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0:
        angle = (2 * math.pi) + angle
    return angle

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

class Ray: 
    def __init__(self, angle, player, map):
        self.ray_angle = normalizeAngle(angle)
        self.player = player
        self.map = map

        self.is_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.ray_angle < 0.5 * math.pi or self.ray_angle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

        self.distance = 0
        self.verticle = False
        self.color = 255

    def cast(self):
        ## Check Horizontol collisions
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0
        
        ##Find First intersection
        first_intersection_x = None
        first_intersection_y = None

        if self.is_facing_up:
            first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) - 0.01
        elif self.is_facing_down:
            first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) + TILESIZE

        first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(self.ray_angle)

        next_horizontal_x = first_intersection_x
        next_horizontal_y = first_intersection_y
        
        xa = 0
        ya = 0

        if self.is_facing_up:
            ya = -TILESIZE
        elif self.is_facing_down: ##While you could do an else here, it's easier to read this way, and the extra check is minimal in terms of performace
            ya = TILESIZE
        
        xa = ya / math.tan(self.ray_angle)

        while (next_horizontal_x < WINDOW_WIDTH and next_horizontal_x >= 0 and 
               next_horizontal_y < WINDOW_HEIGHT and next_horizontal_y >= 0):
            
            if self.map.has_wall_at(next_horizontal_x,next_horizontal_y):
                found_horizontal_wall = True
                horizontal_hit_x = next_horizontal_x
                horizontal_hit_y = next_horizontal_y
                break
            else:
                next_horizontal_x += xa
                next_horizontal_y += ya

       ##Verticle Checking

        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        if self.is_facing_right:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) + TILESIZE
        elif self.is_facing_left:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) - 0.01
        
        first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(self.ray_angle)

        next_vertical_x = first_intersection_x
        next_vertical_y = first_intersection_y

        if self.is_facing_right:
            xa = TILESIZE
        elif self.is_facing_left:
            xa = -TILESIZE
        
        ya = xa * math.tan(self.ray_angle)

        while (next_vertical_x <= WINDOW_WIDTH and next_vertical_x >= 0 and 
               next_vertical_y <= WINDOW_HEIGHT and next_vertical_y >= 0):
            
            if self.map.has_wall_at(next_vertical_x, next_vertical_y):
                found_vertical_wall = True
                vertical_hit_x = next_vertical_x
                vertical_hit_y = next_vertical_y
                break
            else:
                next_vertical_x += xa
                next_vertical_y += ya
        
        ##distance calc
        horizontal_dist : float = 0
        vertical_dist : float = 0
        
        if found_horizontal_wall:
            horizontal_dist = distance_between(self.player.x, self.player.y, horizontal_hit_x, horizontal_hit_y)
        else:
            horizontal_dist = 9999
        
        if found_vertical_wall:
            vertical_dist = distance_between(self.player.x, self.player.y, vertical_hit_x, vertical_hit_y)
            
        else:
            vertical_dist = 9999

        ##compare distances
        if horizontal_dist < vertical_dist:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_dist
            self.color = 160
        elif vertical_dist < horizontal_dist:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y
            self.verticle = True
            self.distance = vertical_dist
            self.color = 150

        self.color *= (LIGHTLEVEL / self.distance)
        if self.color > 255:
            self.color = 255
        self.distance *= math.cos(self.player.rotation_angle - self.ray_angle)

    def draw_ray(self, screen):
        pygame.draw.line(screen, (255,255,0), (self.player.x, self.player.y), (self.wall_hit_x, self.wall_hit_y))
                                                                      