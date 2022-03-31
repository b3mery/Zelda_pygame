import pygame
from game_objects.player import Player

class Weapon(pygame.sprite.Sprite):
    """Weapon class for creating and animating weapon

    Extends:
        pygame (pygame.sprite.Sprite)
    """
    def __init__(self, groups, player:Player) -> None:
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.player = player
        self.direction = player.status.split('_')[0]
        self.__get_weapon_graphic()
        self.__place_weapon()

    def __get_weapon_graphic(self):
        # Graphics
        full_path = f"assets/graphics/weapons/{self.player.weapon}/{self.direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

    def __place_weapon(self):
        """Place the Weapon on the game screen based on players direction
        """
        if self.direction == 'right':
            self.rect = self.image.get_rect(
                midleft = self.player.rect.midright + pygame.math.Vector2(0,16) 
            )
        elif self.direction == 'left':
            self.rect = self.image.get_rect(
                midright = self.player.rect.midleft + pygame.math.Vector2(0,16)
            )
        elif self.direction == 'down':
            self.rect = self.image.get_rect(
                midtop = self.player.rect.midbottom + pygame.math.Vector2(-10,0)
                )
        else: # direction == 'up':
            self.rect = self.image.get_rect(
                midbottom = self.player.rect.midtop + pygame.math.Vector2(-10,0)
            )
