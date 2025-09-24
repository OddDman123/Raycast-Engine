import pygame
import math
from Map import Map
from Settings import *

class Player:
    def __init__(self, new_map):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        # self.radius = 5

        self.turnDirection = 0
        self.walkDirection = 0
        self.strafeDirection = 0

        self.rotation_angle = -90 * (math.pi / 180)
        
        self.map = new_map

        ## Player Stats
        self.use_mouse : bool = False
        self.mouse_sens = 0.03
        self.move_speed = 2.5
        self.rotation_speed = 5 * (math.pi / 180)

    def update_player(self, delta : float):
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()

        self.turnDirection = 0
        self.walkDirection = 0
        self.strafeDirection = 0

        if self.use_mouse:
            if mouse_rel[0]:
                self.turnDirection = mouse_rel[0]
        else:
            if keys[pygame.K_RIGHT]:
                self.turnDirection = 1
            elif keys[pygame.K_LEFT]:
                self.turnDirection = -1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.walkDirection = 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.walkDirection = -1
        if keys[pygame.K_a]:
            self.strafeDirection = -1
        if keys[pygame.K_d]:
            self.strafeDirection = 1
        
        if self.use_mouse:
            self.rotation_angle += self.turnDirection * self.rotation_speed * delta * self.mouse_sens
        else:
            self.rotation_angle += self.turnDirection * self.rotation_speed * delta

        if self.walkDirection:
            if not self.map.has_wall_at(self.x + self.walkDirection * math.cos(self.rotation_angle) * self.move_speed * delta, self.y):
                self.x += self.walkDirection * math.cos(self.rotation_angle) * self.move_speed * delta
            if not self.map.has_wall_at(self.x, self.y + self.walkDirection * math.sin(self.rotation_angle) * self.move_speed * delta):
                self.y += self.walkDirection * math.sin(self.rotation_angle) * self.move_speed * delta
        
        if self.strafeDirection:
            if not self.map.has_wall_at(self.x + self.strafeDirection * math.cos(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed * delta, self.y):
                self.x += self.strafeDirection * math.cos(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed * delta
            if not self.map.has_wall_at(self.x, self.y + self.strafeDirection * math.sin(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed * delta):
                self.y += self.strafeDirection * math.sin(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed * delta


    def draw_player(self,screen, pos_x, pos_y, minimap_size):
        size = minimap_size / TILESIZE
        player_mini_x = pos_x + (self.x * size)
        player_mini_y = pos_y + (self.y * size)
        radius = 2
        pygame.draw.circle(screen, (0,255,40), (player_mini_x, player_mini_y), radius)

        pygame.draw.line(screen,(255, 0, 0), (player_mini_x, player_mini_y), (player_mini_x + math.cos(self.rotation_angle) * radius, player_mini_y + math.sin(self.rotation_angle) * radius))