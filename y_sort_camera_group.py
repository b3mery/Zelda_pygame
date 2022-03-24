import pygame
from player import Player

class YSortCameraGroup(pygame.sprite.Group):
    """Custom Sprite Group for Camera and Overlap
    Sprites with higher y pos are on top
    """
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player:Player):
        """Draw sprites to game screen

        Args:
            player (Player): Insanitated Player Object
        """
        # get player offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw Sprites in Sorted Y order.
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)