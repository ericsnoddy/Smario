import pygame
from pygame.locals import *
from os import path

from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # animation
        self.animations = {}
        self._import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # sprite attrs
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect( topleft = pos )

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.6
        self.jump_speed = -16

        # status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = True
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        
    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False
        

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def get_status(self):
        # if player not moving and not jumping/falling
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.animations[self.status]):
            self.frame_index = 0

    def _import_player_assets(self):
        folder_path = 'graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = path.join(folder_path, animation)
            self.animations[animation] = import_folder(full_path)

    def update(self):
        self.get_input()


    
