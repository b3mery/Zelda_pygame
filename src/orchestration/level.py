from unittest.mock import MagicProxy
import pygame
import random
from src.game_objects.base.magic import MagicPlayer


from src.utils import settings
from src.utils import util

from src.game_objects.base.tile import Tile
from src.game_objects.base.weapon import Weapon
from src.game_objects.player import Player
from src.game_objects.enemy import Enemy
from src.animation.animation_player import AnimationPlayer
from src.game_objects.base.magic import MagicPlayer
from src.user_interface.heads_up_display import HeadsUpDisplay
from src.user_interface.upgrade_menu import UpgradeMenu
from src.orchestration.y_sort_camera_group import YSortCameraGroup

# animation 
class Level:
    """Level Class - builds and updates game level
    """
    def __init__(self) -> None:
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack Sprites
        self.current_attack = None
        self.attack_sprites =  pygame.sprite.Group()
        self.attackable_sprites =  pygame.sprite.Group()
        # sprite setup
        # Creates monsters, tiles and player
        self.create_map()

        # User Interface
        self.ui = HeadsUpDisplay()
        self.upgrade = UpgradeMenu(self.player)

        # particles
        self.anamation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.anamation_player)

        
    def create_map(self):
        """Create the map loading spties
        """
        layouts = {
            'boundary': util.import_csv_layout("assets/map/map_FloorBlocks.csv"),
            'grass': util.import_csv_layout("assets/map/map_Grass.csv"),
            'object': util.import_csv_layout("assets/map/map_Objects.csv"),
            'entities': util.import_csv_layout("assets/map/map_Entities.csv"),
        }
        graphics = {
            'grass': util.import_folder("assets/graphics/Grass"),
            'objects': util.import_folder("assets/graphics/objects")
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
                            Tile(
                                (x,y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                rand_grass_img
                            )
                        
                        if style == 'object':
                            # Select the object graphics at the corresponding index
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'object', surf)
                        
                        if style == 'entities':
                            if col == "394": # player 
                                self.player = Player(
                                        (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic
                                    )
                            else:
                                monster_name = settings.monster_id_mapping.get(col)
                                if monster_name is not None:
                                    Enemy(
                                        monster_name,
                                        (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_xp
                                    )
                            
    def create_attack(self):
        """Create the Attack
        """
        self.current_attack = Weapon([self.visible_sprites, self.attack_sprites], self.player)
    
    def create_magic(self, style, strength, cost):
        """create players magic spell

        Args:
            style (str): Type of spell ('heal' or 'flame')
            strength (int): power of the spell
            cost (int): cost of using the spell
        """
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        
    def destroy_attack(self):
        """Remove The Attack Graphic
        """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """Attack 
        """
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offest = pygame.math.Vector2(0,50)
                            for _ in range(random.randint(3,6)):
                                self.anamation_player.create_grass_particles(pos-offest,[self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type != 'player':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
    
    def damage_player(self, amount, attack_type):
        """_summary_

        Args:
            amount (_type_): _description_
            attack_type (_type_): _description_
        """
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.anamation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
    
    def trigger_death_particles(self, pos:tuple, particle_type:str):
        """Triggers anamation of death particles

        Args:
            pos (tuple): (x,y) position
            particle_type (str): name of particle animation
        """
        self.anamation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused


    def run(self):
        """Update and draw the sprites to the game
        """
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

