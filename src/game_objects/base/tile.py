import pygame 
from utils import settings

class Tile(pygame.sprite.Sprite):
    """Tile Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((settings.TILESIZE,settings.TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.__place_sprite(pos)
            
    def __place_sprite(self,pos):
        """* Adjust the postion of specifc sprite types,
        * place sprite at pos
        * Adjust hitbox of spite

        Args:
            pos (tuple): (x, y) x and y positions
        """
        if self.sprite_type == 'object':
            # Objects are double tilesize, adjust Y for placement
            self.rect = self.image.get_rect(topleft = (pos[0],  pos[1] - settings.TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        
        self.hitbox = self.rect.inflate(settings.HITBOX_OFFSET[self.sprite_type])
