import pygame

from settings import TILESIZE, HEIGHT, WIDTH
from support import import_csv_layout, import_cut_graphics
from tiles import Tile, StaticTile, Crate, Coin, Palm
from player import Player
from enemy import Enemy
from decoration import Sky, Water, Clouds

class Level:
    def __init__(self, win, level_data):
        # general setup
        self.win = win
        self.world_shift = 0

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # crate setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # coin setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palm setup
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # background palm setup
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # background palm setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        # sky, clouds, etc
        self.sky = Sky(8)
        self.water = Water(HEIGHT - 25)
        self.clouds = Clouds(400, 20)

    def player_setup(self, layout):

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if val == '0':
                    sprite = Player((x, y))
                    self.player.add(sprite)
                if val == '1':
                    hat_surf = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(TILESIZE, x, y, hat_surf)
                    self.goal.add(sprite)

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
                        
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surf = grass_tile_list[int(val)]
                        sprite = StaticTile(TILESIZE, x, y, tile_surf)

                    if type == 'crates':
                        sprite = Crate(TILESIZE, x, y)

                    if type == 'coins':
                        if val == '0': sprite = Coin(TILESIZE, x, y, 'graphics/coins/gold')
                        if val == '1': sprite = Coin(TILESIZE, x, y, 'graphics/coins/silver')

                    if type == 'fg palms':
                        if val == '0': sprite = Palm(TILESIZE, x, y, 'graphics/terrain/palm_small', 38)
                        if val == '1': sprite = Palm(TILESIZE, x, y, 'graphics/terrain/palm_large', 64)               
           
                    if type == 'bg palms':
                        sprite = Palm(TILESIZE, x, y, 'graphics/terrain/palm_bg', 64)  

                    if type == 'enemies':
                        sprite = Enemy(TILESIZE, x, y) 
                      
                    if type == 'constraints':  
                        sprite = Tile(TILESIZE, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_bounce(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def autoscroll(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < WIDTH // 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - WIDTH // 4 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def handle_horizontal_collision(self, obstacle_groups):

        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in obstacle_groups:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right

    def handle_vertical_collision(self, obstacle_groups):

        player = self.player.sprite
        player.apply_gravity()

        for sprite in obstacle_groups:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # cancel out gravity                  
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom

    # run the entire game/level
    def run(self):

        # sky
        self.sky.draw(self.win)

        # clouds (3rd arg is to lag the clouds from the foreground)
        self.clouds.draw(self.win, self.world_shift, 1)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.win)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.win)

        # water
        self.water.draw(self.win, self.world_shift)

        # crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.win)

        # enemies     
        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.win)
        self.constraint_sprites.update(self.world_shift)   # enemy constraints are not drawn
        self.enemy_bounce()   # reverse enemy direction on collision with constraint

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.win)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.win)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.win)
        self.player.update()
        self.handle_horizontal_collision(self.terrain_sprites)
        self.handle_vertical_collision(self.terrain_sprites)
        self.player.draw(self.win)
        self.autoscroll()

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.win)