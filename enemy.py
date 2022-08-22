import pygame
from random import randint
from tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'graphics/enemy/run')
        self.rect.y += size - self.image.get_height()
        self.speed = randint(2,4)

    def move(self):
        self.rect.x += self.speed

    def flip_image(self):
        # AnimatedTile.animated() loads 'fresh' images,
        # which handles our flip back to the starting direction
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.flip_image()