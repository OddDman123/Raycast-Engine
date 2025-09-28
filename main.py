from Settings import *
from Map import Map
from Player import Player
from RayCaster import Raycaster
from Isaac import Isaac
import pygame

pygame.init()
pygame.font.init() # Initialize the font module
pygame.mixer.init()

## Window created by pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

wall_texture = pygame.image.load('textures/bricks.png')
wall_texture.convert_alpha()

map = Map()
player = Player(map)
raycaster = Raycaster(player,map)
isaac = Isaac(player, map)
clock = pygame.time.Clock()


font = pygame.font.SysFont('Arial', 8)

minimap_size = 5
minimap_x = WINDOW_WIDTH - (5 * COLS) - 10
minimap_y = 10


# pygame.event.set_grab(True)  # Locks the mouse to the window
# pygame.mouse.set_visible(False) # Hides the mouse cursor

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEWHEEL:
            FOV += event.y * (math.pi / 180)
            raycaster.change_FOV(FOV)

    # pygame.mouse.set_pos(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    
    delta_time = clock.tick(FPS) / 1000

    ## Debug text, a lot for now. Will downsize the code later
    fps_text = "FPS: " + str(int(clock.get_fps()))
    fov_text = "FOV: " + str(round(FOV / (math.pi / 180)))
    text_to_display = fps_text + "\n" + fov_text


    screen.fill((0,0,0)) ##Always reset the screen to one color
    
    ##Update all objects
    player.update_player(delta_time)
    raycaster.castAllRays()
    isaac.update()
    ## Draw all objects, what gets drawn last stays on top

    raycaster.drawAllRays(screen, wall_texture)

    isaac.draw_isaac(screen)
    
    map.draw_map(screen, minimap_x, minimap_y, minimap_size)
    isaac.draw_minimap_isaac(screen, minimap_x, minimap_y, minimap_size)
    player.draw_mini_player(screen, minimap_x, minimap_y, minimap_size)

    player._draw_gun(screen)

    for i,line in enumerate(text_to_display.split('\n')):
        txt_surf = font.render(line, True, (255,255,255))
        txt_rect = txt_surf.get_rect()
        txt_rect.topleft = (8, 8 + i * (txt_rect.h + 4))
        screen.blit(txt_surf,txt_rect)
        

    pygame.display.update() ##When ever you draw onto the screen remember to update the window to display everything