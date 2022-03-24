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
