from Settings import *
from Map import Map
from Player import Player
from RayCaster import Raycaster
import pygame

## Window created by pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

wall_texture = pygame.image.load('bricks.png')
wall_texture.convert()

map = Map()
player = Player(map)
raycaster = Raycaster(player,map)

clock = pygame.time.Clock()

pygame.font.init() # Initialize the font module
font = pygame.font.SysFont('Arial', 16)

minimap_x = 10
minimap_y = 10
minimap_size = 5

# pygame.event.set_grab(True)  # Locks the mouse to the window
# pygame.mouse.set_visible(False) # Hides the mouse cursor

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # pygame.mouse.set_pos(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    delta_time = clock.tick(FPS) / 1000

    text_to_display = "FPS: " + str(int(clock.get_fps()))
    text_surface = font.render(text_to_display,True,(255,255,255))
    text_rect = text_surface.get_rect()

    screen.fill((0,0,0)) ##Always reset the screen to one color
    
    ##Update all objects
    player.update_player(1.0)
    raycaster.castAllRays()

    ## Draw all objects, what gets drawn last stays on top

    raycaster.drawAllRays(screen, wall_texture)

    map.draw_map(screen, minimap_x, minimap_y, minimap_size)
    player.draw_player(screen, minimap_x, minimap_y, minimap_size)
    screen.blit(text_surface,text_rect)
    

    pygame.display.update() ##When ever you draw onto the screen remember to update the window to display everything