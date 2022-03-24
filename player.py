import pygame 
import settings

class Player(pygame.sprite.Sprite):
    """Player Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self,pos,groups, obstacle_sprites:pygame.sprite.Group):
        super().__init__(groups)
        self.image = pygame.image.load('assets/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5 

        self.obstacle_sprites = obstacle_sprites

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

        self.rect.x += self.direction.x * speed
        self.check_collisions('horizontal')
        self.rect.y += self.direction.y * speed
        self.check_collisions('vertical')

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
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0: # moving right
                    self.rect.right = sprite.rect.left
                if self.direction.x < 0: # moving left
                    self.rect.left = sprite.rect.right

    def check_vertical_collisions(self):
        """Check for sprite collisions on the y Axis
        """
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0: # moving down
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0: # moving moving up
                    self.rect.top = sprite.rect.bottom

    def update(self):
        """Update the game screen
        """
        self.input()
        self.move(self.speed)
    