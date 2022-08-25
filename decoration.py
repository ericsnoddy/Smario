import pygame
from random import choice, randint

from settings import TILESIZE, WIDTH, VTILES, LWIDTH
from support import import_folder
from tiles import AnimatedTile, StaticTile

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (WIDTH, TILESIZE))
        self.middle = pygame.transform.scale(self.middle, (WIDTH, TILESIZE))
        self.bottom = pygame.transform.scale(self.bottom, (WIDTH, TILESIZE))

    def draw(self, surf):
        for row in range(VTILES):
            y = row * TILESIZE
            if row < self.horizon:
                surf.blit(self.top, (0, y))
            elif row == self.horizon:
                surf.blit(self.middle, (0, y))
            else:
                surf.blit(self.bottom, (0, y))

class Water:
    def __init__(self, top):
        water_start = -WIDTH
        WATER_TILE_WIDTH = 192
        EXTEND_TILES = 8
        tiles = int((LWIDTH + WIDTH) / WATER_TILE_WIDTH) + EXTEND_TILES
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tiles):
            x = tile * WATER_TILE_WIDTH + water_start
            y = top
            sprite = AnimatedTile(WATER_TILE_WIDTH, x, y, 'graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surf, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surf)

class Clouds:
    def __init__(self, horizon, cloud_count):
        cloud_surfs = import_folder('graphics/decoration/clouds')
        min_x = -WIDTH
        max_x = LWIDTH + WIDTH
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_count):
            cloud = choice(cloud_surfs)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surf, shift, lag):
        if shift + lag > 0: shift = shift + lag
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surf)