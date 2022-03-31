import pygame
import random

from utils import settings
from utils import util

from game_objects.base.tile import Tile
from game_objects.weapon import Weapon
from game_objects.magic import Magic
from game_objects.player import Player
from game_objects.enemy import Enemy

from animation.animation_player import AnimationPlayer

from user_interface.heads_up_display import HeadsUpDisplay
from user_interface.upgrade_menu import UpgradeMenu
from user_interface.game_over_interface import GameOverInterface
from user_interface.title_screen_interface import TitleScreenInterface
from user_interface.level_complete_interface import LevelCompleteInterface
from orchestration.y_sort_camera_group import YSortCameraGroup

class Level:
    """* Level Class is essentially the game engine, it is responsible for:
    * Insanitating game objects:
            * level map Tile sprites
            * Player 
            * Enemy's 
    * Managing player and monster intergations
    * Managing player and weapon integrations
    * Managing different sprite groups
    * insanitating anamations
    * Running the main game update loop
    """
    def __init__(self) -> None:
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.level_nbr = 1
        self.max_nbr_levels = settings.NBR_OF_LEVELS
        self.is_level_complete = False
        self.new_player = True
        self.player:Player = None
        self.is_game_running = False
        self.is_upgrade_menu_active = False
        self.is_game_over = False
        
        # main sound
        self.main_sound = pygame.mixer.Sound(open(settings.MAIN_AUDIO_FILE))
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=-1)

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
   
        # Attack Sprites
        self.attack_sprites =  pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        # sprite setup
        # Creates monsters, tiles and player
        self.__create_level_map()

        self.current_attack = None
        # particles
        self.anamation_player = AnimationPlayer()
        self.magic = Magic(self.anamation_player)
        
        # User Interface
        self.heads_up_display = HeadsUpDisplay()
        self.title_screen_ui = TitleScreenInterface(self.activate_level)
        self.upgrade_menu = UpgradeMenu(self.player)
        self.level_complete_ui = LevelCompleteInterface(self.rebuild_level)
        self.game_over_display = GameOverInterface(self.rebuild_level)


        
    def __create_level_map(self):
        """* Load the Tile CSV Layouts
        * load the Tile Graphics
        * Build the x & y position
        * Create the Entity Sprites
        * Create the Tile Sprites (Map objects)
        """
        layouts = {
            'boundary': util.import_csv_layout("assets/map/map_FloorBlocks.csv"),
            'grass': util.import_csv_layout("assets/map/map_Grass.csv"),
            'object': util.import_csv_layout("assets/map/map_Objects.csv"),
            'entities': util.import_csv_layout("assets/map/map_Entities.csv"),
        }
        graphics = {
            'grass': util.import_folder_images("assets/graphics/Grass"),
            'objects': util.import_folder_images("assets/graphics/objects")
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * settings.TILESIZE
                        y = row_index * settings.TILESIZE
                        # Build Map Sprites
                        if style == 'entities':
                            self.__create_entity_sprites(col,(x,y))
                        else:                            
                            self.__create_tile_sprites(style, col, (x,y), graphics)
                        
    def __create_tile_sprites(self, style, id, pos:tuple, graphics):
        """Insanities the Tile object with each different type of sprite in its desired position.

        Args:
            style (str): 'boundary', 'grass', or 'object'
            id (str): the sprites allocated id from the csv layout
            pos (tuple): x and y position 
            graphics (dict): Dictionary of tile graphics
        """
        if style == 'boundary':
            Tile(pos,[self.obstacle_sprites],'invisible')
        
        if style == 'grass':
            rand_grass_img = random.choice(graphics['grass'])
            Tile(
                pos,
                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                'grass',
                rand_grass_img
            )
        
        if style == 'object':
            # Select the object graphics at the corresponding index
            surf = graphics['objects'][int(id)]
            Tile(pos,[self.visible_sprites, self.obstacle_sprites],'object', surf)

    def __create_entity_sprites(self, id, pos:tuple):
        """* Create the Player if the id matches it Tile Id
            * Instantiate the player object
        * Else Create the monsters
            * Instantiate the Enemy Object

        Args:
            id (str): Id form the tiled csv layour
            pos (tuple): X and Y position
        """
        if id == "394": # player 
            if self.player and not self.new_player:
                # Store progress
                stats = self.player.stats
                health = self.player.health
                energy = self.player.energy
                exp = self.player.exp
                # Kill and create
                self.player.kill()
                self.__create_player(pos)
                # repopulate progress
                self.player.stats = stats
                self.player.health = health
                self.player.energy = energy
                self.player.exp = exp
            else:
                self.__create_player(pos)
            # re initalise upgrade menu
            self.upgrade_menu = UpgradeMenu(self.player)

        else:
            monster_name = settings.monster_id_mapping.get(id)
            if monster_name is not None:
                Enemy(
                    monster_name,
                    pos,
                    [self.visible_sprites, self.attackable_sprites, self.enemy_sprites],
                    self.obstacle_sprites,
                    self.level_nbr - 1,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_xp
                )
    def __create_player(self, pos:tuple):
        self.player = Player(
            pos,
            [self.visible_sprites, self.attackable_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_magic
        )

    ####################################### Player Integration Methods #############################################################                         
    def create_attack(self):
        """Instantiate Weapon to current_attack
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
            self.magic.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        
    def destroy_attack(self):
        """Remove The Attack Graphic
        """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    ####################################### Enemy Integration Methods #############################################################                         
    def __detect_player_attacks(self):
        """Detect collisions between attack sprites and attackable sprites 
        """
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    self.__damage_collided_attackable_sprites(attack_sprite, collision_sprites)

    def __damage_collided_attackable_sprites(self,attack_sprite, collision_sprites):
        """* if grass, create grass anamation
        * else if not player, call get_damage 

        Args:
            attack_sprite (pygame.sprite.Sprite): Attack sprite
            collision_sprites (list(pygame.sprite.Sprite)): Sprites collied with Attack Sprite 
        """
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
        """Inflict damage on the player
        * updates player vulnerability, hurt time for damager timer.
        * calls create_particles for attack type anamation. 

        Args:
            amount (int or float): amount of damage to inflict
            attack_type (str): type of attack for particle animation
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
        """Increase players experience by an amount

        Args:
            amount (int or float): amount to increase exp by
        """
        self.player.exp += amount

    ####################################### UI Methods #############################################################                         
    def toggle_upgrade_menu(self):
        """Pause the game
        """
        self.is_upgrade_menu_active = not self.is_upgrade_menu_active

    def check_game_over(self):
        """Pause the game
        """
        if self.player.health <= 0:
            self.game_over_display.title_font_color = settings.GAME_OVER_TEXT_COLOR
            self.is_game_over = not self.is_game_over
        if len(self.enemy_sprites) == 0 and self.level_nbr == self.max_nbr_levels:
            self.game_over_display.title = 'You Won'
            self.game_over_display.title_font_color = settings.GAME_WON_TEXT_COLOR
            self.is_game_over = not self.is_game_over

        if len(self.enemy_sprites) == 0 and self.level_nbr < self.max_nbr_levels:
            self.is_level_complete = True

    def activate_level(self):
        self.is_game_running = True

    def rebuild_level(self):
        """Kill all sprites, rebuild
        """
        self.new_player = self.player.health <= 0
        # clear sprites
        for sprite in self.visible_sprites:
            if sprite.sprite_type != 'player':
                sprite.kill()
        for sprite in self.obstacle_sprites:
            if sprite.sprite_type != 'player':
                sprite.kill()
        for sprite in self.attack_sprites:
            if sprite.sprite_type != 'player':
                sprite.kill()
        for sprite in self.attackable_sprites:
            if sprite.sprite_type != 'player':
                sprite.kill()
        if self.new_player:
            self.player.kill()        
            self.level_nbr = 1

        if self.is_level_complete:
            # increase level after level complete rebuild
            self.level_nbr += 1    
        
        self.__create_level_map()
        self.main_sound.play(loops=-1)

        self.is_game_over = False
        self.is_level_complete = False    

    ####################################### Game Loop #############################################################                         
    def run(self):
        """Update and draw the sprites to the game
        """ 
        self.visible_sprites.custom_draw(self.player)
        self.heads_up_display.display(self.player, self.level_nbr)
        if not self.is_game_running:
            # Title Screen
            self.title_screen_ui.display()
        elif self.is_level_complete:
            self.level_complete_ui.display()
        elif self.is_game_over:
            # Game Over 
            self.main_sound.stop()
            self.game_over_display.display()
        elif self.is_upgrade_menu_active:
            # Upgrade screen
            self.upgrade_menu.display()
        else:
            # run the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.__detect_player_attacks()
            self.check_game_over()

