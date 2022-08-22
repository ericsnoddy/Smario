import pygame
from os import walk, path
from csv import reader

from settings import TILESIZE

def import_folder(img_path):
    image_surf_list = []
    for _, __, image_files in walk(img_path):
        for image in image_files:
            full_path = path.join(img_path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf_list.append(image_surf)
    return image_surf_list

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
            new_surf = pygame.Surface((TILESIZE, TILESIZE), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            cut_tiles.append(new_surf)

    return cut_tiles