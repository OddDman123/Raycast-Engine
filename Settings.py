import math

TILESIZE : int = 32
ROWS : int = 10
COLS : int = 15

WINDOW_WIDTH = COLS * TILESIZE
WINDOW_HEIGHT = ROWS * TILESIZE

##Need to convert Degrees to Radians
FOV = 60 * (math.pi / 180)

RES = 1
NUM_RAYS = WINDOW_WIDTH // RES

FPS = 60

# Dist_to_projected_plane = (WINDOW_WIDTH / 2) / math.tan(FOV / 2) == 415 in this case
