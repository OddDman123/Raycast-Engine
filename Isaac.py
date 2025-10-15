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



    def draw_isaac(self, screen : pygame.Surface, zbuffer : list):
        ##Method 2
        sprite_x = float(self.x - self.player.x)
        sprite_y = float(self.y - self.player.y)

        dirx = math.cos(self.player.rotation_angle)
        diry = math.sin(self.player.rotation_angle)
        fov = 0.60  # Or adjust for desired FOV
        planeX = -diry * fov
        planeY = dirx * fov
        scale_factor = 20.0
        h = WINDOW_HEIGHT
        w = WINDOW_WIDTH

        invDet = 1.0 / (planeX * diry - dirx * planeY)
        
        transformX = invDet * (diry * sprite_x - dirx * sprite_y)
        transformY = invDet * (-planeY * sprite_x + planeX * sprite_y)

        spriteScreenX = int((w / 2) * (1 + transformX / transformY))

        if transformY <= 0:
            return
        spriteHeight = abs(int(self.sprite.get_height() * scale_factor / (transformY))) #using 'transformY' instead of the real distance prevents fisheye
        
       

        drawEndY = int(min(WINDOW_HEIGHT - 1, spriteHeight / 2 + WINDOW_HEIGHT / 2))
        if(drawEndY >= h):
            drawEndY = h - 1
        drawStartY = drawEndY - spriteHeight


        spriteWidth = abs( int (self.sprite.get_width() * scale_factor/ (transformY)))

        drawStartX = int(-spriteWidth / 2 + spriteScreenX)
        if(drawStartX < 0):
            drawStartX = 0
        drawEndX = int(spriteWidth / 2 + spriteScreenX)
        if (drawEndX >= w):
            drawEndX = w - 1


        # screen.blit(pygame.transform.scale(self.sprite, (spriteWidth , spriteHeight)), (spriteScreenX, drawStartY))

        
        sprite_texture = self.sprite.convert_alpha()
        texture_width = self.sprite.get_width()
        texture_height = self.sprite.get_height()

        for stripe in range(drawStartX, drawEndX):

            # Draw sprite pixel/column
            if (0 <= stripe < WINDOW_WIDTH and transformY > 0 and transformY < zbuffer[stripe]):
                # Texture X coordinate (clamped)
                texX = int((stripe - (-spriteWidth / 2 + spriteScreenX)) * texture_width / spriteWidth)
                texX = max(0, min(texture_width - 1, texX))

                # Create a 1px wide vertical strip surface
                strip_height = drawEndY - drawStartY
                if strip_height <= 0:
                    continue  # skip degenerate strips

                vertical_strip = pygame.Surface((1, strip_height), pygame.SRCALPHA)

                for y in range(strip_height):
                    screen_y = y + drawStartY  # actual Y position on screen
                    d = screen_y * 256 - WINDOW_HEIGHT * 128 + spriteHeight * 128
                    texY = int((d * texture_height) / spriteHeight / 256)
                    texY = max(0, min(texture_height - 1, texY))

                    # Get the pixel from the sprite texture
                    color = sprite_texture.get_at((texX, texY))

                    # Skip transparent pixels
                    if color.a != 0:
                        vertical_strip.set_at((0, y), color)

                # Draw the strip at the current screen position
                screen.blit(vertical_strip, (stripe, drawStartY))











    

        
        