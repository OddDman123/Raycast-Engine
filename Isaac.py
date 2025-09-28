from Settings import *
from Map import *
import pygame
import math

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0:
        angle = (2 * math.pi) + angle
    return angle

class Isaac():
    def __init__(self, i_player, i_map):
        self.x = 48
        self.y = 48

        self.player = i_player
        self.map = i_map
        
        self.rotation_angle = 90 * (math.pi / 180)

        self.sprite = pygame.image.load('textures/angry_isaac.png').convert_alpha()
        self.rah = pygame.mixer.Sound('audio/isaac-rah.wav')
        self.rah.set_volume(25)
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            self.rah.play()

    def draw_minimap_isaac(self, screen, m_posx, m_posy, mini_map_size):
        mX = m_posx + (self.x * (mini_map_size / TILESIZE))
        mY = m_posy + (self.y * (mini_map_size / TILESIZE))
        radius = 2
        pygame.draw.circle(screen, (0,200,200), (mX, mY), radius)



    def draw_isaac(self, screen : pygame.Surface):
        # mouse = pygame.mouse.get_pos()
        # sprite_size = (self.sprite.get_width(), self.sprite.get_height())

        # scaling_y = self.sprite.get_height() * abs((mouse[1] - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT / 2)
        # scaling_x = self.sprite.get_width() * abs((mouse[1] - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT / 2)

        # scaled_isaac = pygame.transform.scale(self.sprite,(scaling_x, scaling_y))

        # screen.blit(scaled_isaac, (mouse[0] - scaling_x / 2, mouse[1] - scaling_y / 2))

        # draw_begin = (WINDOW_HEIGHT / 2) - (self.sprite.get_height() / 2)

        # nx = self.x - self.player.x
        # ny = self.x - self.player.y

        # nx = nx * math.cos(self.player.rotation_angle) - ny * math.sin(self.player.rotation_angle)
        # ny = nx * math.sin(self.player.rotation_angle) + ny * math.cos(self.player.rotation_angle)

        # maxfov = (WINDOW_WIDTH / 2) / math.tan(FOV / 2)
        # screen_x = nx * (maxfov / ny)
        # sprite_height = WALLHEIGHT * (maxfov / ny)
        
        # scaling_y = self.sprite.get_height() * abs((sprite_height - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT / 2)
        # scaling_x = self.sprite.get_width() * abs((sprite_height - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT / 2)

        # scaled_isaac = pygame.transform.scale(self.sprite,(scaling_x, scaling_y))
        
        # # draw_begin = (WINDOW_HEIGHT / 2) - (sprite_height / 2)
        
        # screen.blit(scaled_isaac, (screen_x , sprite_height))

        sprite_x = float(self.x - self.player.x)
        sprite_y = float(self.y - self.player.y)
        planeX = self.player.planeX
        planeY = self.player.planeY
        dirx = math.cos(self.player.rotation_angle)
        diry = math.sin(self.player.rotation_angle)
        h = WINDOW_HEIGHT
        w = WINDOW_WIDTH

        invDet = 1.0 / (planeX * diry - dirx * planeY)
        
        transformX = invDet * (diry * sprite_x - dirx * sprite_y)
        transformY = invDet * (-planeY * sprite_x + planeX * sprite_y)

        # print(dirx, diry, invDet, transformX, transformY)

        spriteScreenX = int((w / 2) * (1 + transformX / transformY))

        spriteHeight = abs(int(self.sprite.get_height() / (transformY))) #using 'transformY' instead of the real distance prevents fisheye
        #calculate lowest and highest pixel to fill in current stripe
        drawStartY = -spriteHeight / 2 + h / 2
        if(drawStartY < 0): 
            drawStartY = 0
        drawEndY = spriteHeight / 2 + h / 2
        if(drawEndY >= h):
            drawEndY = h - 1
        
        spriteWidth = abs( int (self.sprite.get_height() / (transformY)))
        drawStartX = -spriteWidth / 2 + spriteScreenX
        if(drawStartX < 0):
            drawStartX = 0
        drawEndX = spriteWidth / 2 + spriteScreenX
        if (drawEndX >= w):
            drawEndX = w - 1

        # scaling_y = self.sprite.get_height() * abs((transformY - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT / 2)
        # scaling_x = self.sprite.get_width() * abs((transformY - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT / 2)
        # scaled_isaac = pygame.transform.scale(self.sprite,(scaling_x, scaling_y))
        # print(scaling_x, scaling_y)
        # for strip in range(int(round(drawStartX)), int(round(drawEndX))):
        #     texX = int((256 * (strip - (-spriteWidth / 2 + spriteScreenX)) * 4 / spriteWidth) / 256)
        #         #the conditions in the if are:
        #         ##1) it's in front of camera plane so you don't see things behind you
        #         ##2) it's on the surface (left)
        #         ##3) it's on the surface (right)
        #         ##4) ZBuffer, with perpendicular distance
        #     if(transformY > 0 and strip > 0 and strip < w): #and transformY < zBuffer[stripe]):
        screen.blit(pygame.transform.scale(self.sprite, (spriteWidth , spriteHeight)), (spriteScreenX, drawEndY))
        # scaled_isaac = pygame.transform.scale(self.sprite, (spriteWidth, spriteHeight))

        # screen.blit(scaled_isaac, (spriteScreenX, drawStartY))






    

        
        