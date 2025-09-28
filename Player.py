import pygame
import math
from Map import Map
from Settings import *

class Player:
    def __init__(self, new_map):
        self.x = COLS * TILESIZE / 2
        self.y = ROWS * TILESIZE / 2
        # self.radius = 5

        self.turnDirection = 0
        self.walkDirection = 0
        self.strafeDirection = 0

        self.rotation_angle = 90 * (math.pi / 180)
        self.planeX = 0.0
        self.planeY = 0.66

        self.map = new_map

        ## Player Stats
        self.use_mouse : bool = False
        self.mouse_sens = 0.03
        self.move_speed = 100
        self.rotation_speed = 200 * (math.pi / 180)

        ## Gun
        self.gun_frames = []
        for i in range(9):
            frame = pygame.image.load(f"duke_nukem_shotgun/duke_nukem_shotgun_{i}.png").convert_alpha()
            self.gun_frames.append(frame)


    def update_player(self, delta : float):
        self.movenment(delta)
        # print(self.)


    def movenment(self, delta : float):
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
        
        if self.turnDirection == 1:
            if self.use_mouse:
                self.rotation_angle += self.turnDirection * self.rotation_speed * delta * self.mouse_sens
            else:
                self.rotation_angle += self.turnDirection * self.rotation_speed * delta
                oldplanX = self.planeX
                self.planeX = self.planeX * math.cos(-self.rotation_speed * delta) - self.planeY * math.sin(-self.rotation_speed * delta)
                self.planeY = oldplanX * math.sin(-self.rotation_speed * delta) + self.planeY * math.cos(-self.rotation_speed * delta)
        elif self.turnDirection == -1:
            if self.use_mouse:
                self.rotation_angle += self.turnDirection * self.rotation_speed * delta * self.mouse_sens
            else:
                self.rotation_angle += self.turnDirection * self.rotation_speed * delta
                oldplanX = self.planeX
                self.planeX = self.planeX * math.cos(self.rotation_speed * delta) - self.planeY * math.sin(self.rotation_speed * delta)
                self.planeY = oldplanX * math.sin(self.rotation_speed * delta) + self.planeY * math.cos(self.rotation_speed * delta)


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
        
    def draw_mini_player(self,screen, pos_x, pos_y, minimap_size):
        size = minimap_size / TILESIZE
        player_mini_x = pos_x + (self.x * size)
        player_mini_y = pos_y + (self.y * size)
        radius = 2
        pygame.draw.circle(screen, (0,255,40), (player_mini_x, player_mini_y), radius)

        pygame.draw.line(screen,(255, 0, 0), (player_mini_x, player_mini_y), (player_mini_x + math.cos(self.rotation_angle) * radius, player_mini_y + math.sin(self.rotation_angle) * radius))
    
    def _draw_gun(self, screen):
        w = (WINDOW_WIDTH / 2) - self.gun_frames[0].get_width()
        h = (WINDOW_WIDTH / 2) + self.gun_frames[0].get_height()
        pygame.transform.scale 
        screen.blit(pygame.transform.scale(self.gun_frames[0], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)), (180, WINDOW_HEIGHT / 2))