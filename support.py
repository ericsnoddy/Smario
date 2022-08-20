import pygame
from csv import reader

from settings import TILESIZE

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / TILESIZE)
    tile_num_y = int(surface.get_height() / TILESIZE)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surf = pygame.Surface((TILESIZE, TILESIZE))
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            cut_tiles.append(new_surf)

    return cut_tiles