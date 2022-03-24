import pygame 
import settings

class Tile(pygame.sprite.Sprite):
    """Tile Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
