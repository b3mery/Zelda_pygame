import pygame 
import settings

class Tile(pygame.sprite.Sprite):
    """Tile Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((settings.TILESIZE,settings.TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            # Adjust y position
            y = pos[1] - settings.TILESIZE
            self.rect = self.image.get_rect(topleft = (pos[0], y))
        else:    
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)