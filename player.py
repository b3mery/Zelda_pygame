import pygame 
import settings

class Player(pygame.sprite.Sprite):
    """Player Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5 

    def input(self):
        """Monitor for keybaord input"""
        keys = pygame.key.get_pressed()

        # Vertical Inputs 
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Horizontal Inputs 
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    
    def move(self,speed):
        """Move the Player"""
        # Check vector length and normalize
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed

    def update(self):
        """Update the game screen
        """
        self.input()
        self.move(self.speed)
    