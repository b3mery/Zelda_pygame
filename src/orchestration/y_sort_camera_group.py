import pygame
from game_objects.player import Player

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

        # Create the floor
        self.floor_surf = pygame.image.load("assets/graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft= (0,0))

    def custom_draw(self, player:Player):
        """Draw sprites to game screen

        Args:
            player (Player): Insanitated Player Object
        """
        # get player offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw the floor
        floor_offset_pos = self.floor_rect.topleft -self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw Sprites in Sorted Y order.
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
    def enemy_update(self, player:Player):
        """Update Enemy Sprites

        Args:
            player (Player): Insatiated Player Object
        """
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)