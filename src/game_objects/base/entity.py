"""Base Entity Game Object
"""
import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    """_summary_

    Args:
        pygame (_type_): _description_
    """
    def __init__(self, groups) -> None:
        super().__init__(groups)
        # Graphics
        self.frame_index = 0
        self.anamation_speed = 0.15
        # Movement
        self.direction = pygame.math.Vector2()

    def move(self,speed):
        """Move the Player"""
        # Check vector length and normalize
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.check_collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.check_collisions('vertical')
        self.rect.center = self.hitbox.center

    def check_collisions(self, direction:str):
        """Check collisions

        Args:
            direction (str): horizontal or vertical
        """
        if direction == 'horizontal':
            self.check_horizontal_collisions()

        if direction == 'vertical':
            self.check_vertical_collisions()

    def check_horizontal_collisions(self):
        """Check Sprite collisions on x Axis
        """
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0: # moving right
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0: # moving left
                    self.hitbox.left = sprite.hitbox.right

    def check_vertical_collisions(self):
        """Check for sprite collisions on the y Axis
        """
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0: # moving down
                    self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0: # moving moving up
                    self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        # sign wave
        value = sin(pygame.time.get_ticks())
        if value >= 0:
           return 255
        else: 
           return 0