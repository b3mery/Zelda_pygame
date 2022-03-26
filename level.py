import pygame
import random
from enemy import Enemy

import settings
import utils
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from y_sort_camera_group import YSortCameraGroup

class Level:
    """Level Class - builds and updates game level
    """
    def __init__(self) -> None:
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack Sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # User Interface
        self.ui = UI()
        
    def create_map(self):
        """Create the map loading spties
        """
        layouts = {
            'boundary': utils.import_csv_layout("assets/map/map_FloorBlocks.csv"),
            'grass': utils.import_csv_layout("assets/map/map_Grass.csv"),
            'object': utils.import_csv_layout("assets/map/map_Objects.csv"),
            'entities': utils.import_csv_layout("assets/map/map_Entities.csv"),
        }
        graphics = {
            'grass': utils.import_folder("assets/graphics/Grass"),
            'objects': utils.import_folder("assets/graphics/objects")
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * settings.TILESIZE
                        y = row_index * settings.TILESIZE
                        # Build Map Sprites
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        
                        if style == 'grass':
                            rand_grass_img = random.choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'grass', rand_grass_img)
                        
                        if style == 'object':
                            # Select the object graphics at the corresponding index
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'object', surf)
                        
                        if style == 'entities':
                            if col == "394": # player 
                                self.player = Player(
                                        (x,y),
                                        [self.visible_sprites],
                                        self.obstacle_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic
                                    )
                            else:
                                monster_name = settings.monster_id_mapping.get(col)
                                if monster_name is not None:
                                    Enemy(monster_name, (x,y), [self.visible_sprites] )
                            


    def create_attack(self):
        """Create the Attack
        """
        self.current_attack = Weapon([self.visible_sprites], self.player)
    
    def destroy_attack(self):
        """Remove The Attack Graphic
        """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        print(style)
        print(cost)
        print(strength)

    def run(self):
        """Update and draw the sprites to the game
        """
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

