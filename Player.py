import pygame
import math
from Settings import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = 5

        self.turnDirection = 0
        self.walkDirection = 0
        self.strafeDirection = 0

        self.rotation_angle = -90 * (math.pi / 180)

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
        # wall_check_x = self.x + math.cos(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed
        # wall_check_y = self.y + math.sine(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed

        self.x += self.walkDirection * math.cos(self.rotation_angle) * self.move_speed * delta 
        self.y += self.walkDirection * math.sin(self.rotation_angle) * self.move_speed * delta 
        self.x += self.strafeDirection * math.cos(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed * delta
        self.y += self.strafeDirection * math.sin(self.rotation_angle + (90 * math.pi / 180)) * self.move_speed * delta
            

    def move_player(self, x, y):
        self.x += x
        self.y += y
    def draw_player(self,screen):
        pygame.draw.circle(screen, (0,255,40), (self.x,self.y), self.radius)

        pygame.draw.line(screen,(255, 0, 0), (self.x, self.y), (self.x + math.cos(self.rotation_angle) * 50, self.y + math.sin(self.rotation_angle) * 50))