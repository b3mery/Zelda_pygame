import pygame

import settings
from tile import Tile
from player import Player
from debug import debug

class Level:
    """Level Class - builds and updates game level
    """
    def __init__(self) -> None:
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()
        

    def create_map(self):
        """Create the map loading spties
        """
        for row_index, row in enumerate(settings.WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * settings.TILESIZE
                y = row_index * settings.TILESIZE
                # x = obstacle sprite, p = player sprite
                if col == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites])

    def run(self):
        """Update and draw the sprites to the game
        """
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)