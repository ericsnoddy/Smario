import pygame
from pygame.locals import *
from os import path

from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, win_surf, create_jump_particles_func):
        super().__init__()

        # animation
        self._import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # sprite attrs
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # dust particles
        self._import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.win = win_surf
        self.create_jump_particles_func = create_jump_particles_func

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 0.6
        self.jump_speed = -16

        # status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
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
            self.create_jump_particles_func(self.rect.midbottom)

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

        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index > len(self.animations[self.status]):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # get rectangles
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def animate_dust(self):

        if self.status == 'run' and self.on_ground:

            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0            
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.win.blit(dust_particle, pos)    
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.win.blit(flipped_dust_particle,pos)

    def _import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')

    def _import_player_assets(self):
        folder_path = 'graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = path.join(folder_path, animation)
            self.animations[animation] = import_folder(full_path)

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.animate_dust()


    
