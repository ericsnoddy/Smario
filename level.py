import pygame

from settings import TILESIZE
from support import import_csv_layout, import_cut_graphics
from tiles import StaticTile

class Level:
    def __init__(self, win, level_data):
        # general setup
        self.win = win
        self.world_shift = -3

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

    def create_tile_group(self, layout, type):

        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surf = terrain_tile_list[int(val)]
                        sprite = StaticTile(TILESIZE, x, y, tile_surf)
                        sprite_group.add(sprite)

        return sprite_group

    def run(self):
        # run the entire game/level
        self.terrain_sprites.draw(self.win)
        self.terrain_sprites.update(self.world_shift)