from pyclbr import Function
import pygame

from game_objects.base.entity import Entity 
from utils import settings
from utils import util

class Player(Entity):
    """Player Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self, 
                 pos:tuple,
                 groups:list,
                 obstacle_sprites:pygame.sprite.Group,
                 create_attack:Function,
                 destroy_attack:Function,
                 create_magic:Function,  
                ):
        super().__init__(groups)
        self.sprite_type = 'player'
        
        self.image = pygame.image.load('assets/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(settings.HITBOX_OFFSET[self.sprite_type])

        # Graphics Set up
        self.__import_player_assets()
        self.status = 'down'
      
        # Movement
        self.obstacle_sprites = obstacle_sprites
        # Attack timer
        self.is_attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        # Weapon and magic switch
        self.switch_duration_cooldown = 200
        
        # Weapons
        # Weapon methods
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        # Weapon Attributes
        self.weapon_index = 0
        self.weapon = list(settings.weapon_data.keys())[self.weapon_index]
        # Weapon Timer
        self.can_switch_weapon = True
        self.weapon_switch_time = None

        # Magic
        # Magic methods
        self.create_magic = create_magic
        # self.destroy_magic = destroy_magic        
        # Magic Attributes
        self.magic_index = 0
        self.magic = list(settings.magic_data.keys())[self.magic_index]
        # Magic Timer
        self.can_switch_magic = True
        self.magic_switch_time = True

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.vulnerability_cooldown_duration = 500

        self.weapon_attack_sound = pygame.mixer.Sound('assets/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.40)

        # Stats
        self.stats = settings.player_stats
        self.max_stats = settings.player_max_stats
        self.upgrade_cost = settings.player_upgrade_cost
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.resistance = 1
        self.exp = 0

    def __import_player_assets(self):
        """Import player graphic assets from player sub folders
        """
        character_path = "assets/graphics/player/"
        self.animations =settings.player_animations
        for animation_state in self.animations.keys():
            folder_path = f"{character_path}/{animation_state}"
            self.animations[animation_state] = util.import_folder_images(folder_path)

    def __check_for_input(self):
        """Check for keyboard input"""
        if self.is_attacking:
            return None
        self.__movement_input()
        self.__attack_input()
        self.__magic_input()
        self.__switch_weapon_input()
        self.__switch_magic_input()


    def __movement_input(self):
        """* Check for keyboard movement input.
        * Update direction
        * Update Status
        """
        keys = pygame.key.get_pressed()
        # Vertical Inputs
        if keys[settings.UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[settings.DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # Horizontal Inputs
        if keys[settings.RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[settings.LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def __attack_input(self):
        """* Check for attack keyboard inputs
        * Update is_attacking
        * create_attack
        """
        keys = pygame.key.get_pressed()
        # Attack Input:
        if keys[settings.ATTACK]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.weapon_attack_sound.play()
    
    def __switch_weapon_input(self):
        """* Check for switch weapon input
        * Check if can switch
        * Update can_switch
        * Update weapon_index
        """
        keys = pygame.key.get_pressed()
        # Switch Weapon        
        if keys[settings.SWAP_WEAPON] and self.can_switch_weapon:
            # q to change weapon
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index += 1
            # Reset index for out of range
            if self.weapon_index > len(settings.weapon_data.keys()) - 1:
                self.weapon_index = 0
            self.weapon = list(settings.weapon_data.keys())[self.weapon_index]
    
    def __magic_input(self):
        """* Check for magic keyboard inputs
        * Update is_attacking
        * create_magic
        """
        keys = pygame.key.get_pressed()
        # Magic Input
        if keys[settings.MAGIC]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            style = list(settings.magic_data.keys())[self.magic_index]
            strength = list(settings.magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            cost = list(settings.magic_data.values())[self.magic_index]['cost']
            self.create_magic(style, strength, cost)
    
    def __switch_magic_input(self):
        """* Check for switch magic input
        * Check if can switch
        * Update can_switch
        * Update magic_index
        """       
        keys = pygame.key.get_pressed()
        # Switch Magic
        if keys[settings.SWAP_MAGIC] and self.can_switch_magic:
            # e to change magic
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            self.magic_index += 1
            # Reset index for out of range
            if self.magic_index > len(settings.magic_data.keys()) - 1:
                self.magic_index = 0
            self.magic = list(settings.magic_data.keys())[self.magic_index]

    def __set_status(self):
        """Calculate the player.status based on direction and attacking
        """
        # idle status:
        if self.direction.x == 0  and self.direction.y == 0 and 'idle' not in self.status and not 'attack' in self.status:
            self.status = self.status + '_idle'
        
        # Attack status:
        if self.is_attacking:
            self.direction.x = 0 
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack') 
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def __cooldowns(self):
        """Method for tracking player cooldowns
        """
        current_time = pygame.time.get_ticks()
        
        # Player Attack Cool Down
        if (self.is_attacking and current_time - self.attack_time >= (self.attack_cooldown + settings.weapon_data[self.weapon]['cooldown']) ):
            self.is_attacking = False
            self.destroy_attack()

        # Switch Weapons cool down
        if (not self.can_switch_weapon and current_time - self.weapon_switch_time >= self.switch_duration_cooldown ):
            self.can_switch_weapon = True
        
        # Switch Magic cool down
        if (not self.can_switch_magic and current_time - self.magic_switch_time >= self.switch_duration_cooldown ):
            self.can_switch_magic = True

        # Invincibility
        if not self.vulnerable and  current_time - self.hurt_time >= self.vulnerability_cooldown_duration:
            self.vulnerable = True

    def __animate(self):
        """Animate the Game Object
        """
        anamation = self.animations[self.status]
        self.frame_index += self.anamation_speed

        if self.frame_index >= len(anamation):
            self.frame_index = 0

        # set the image
        self.image = anamation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable: 
            # Flicker 0 -255
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else: 
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        """
        Returns:
            float: sum of base damage + assigned weapon strength 
        """
        base_damage  = self.stats['attack']
        weapon_damage = settings.weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        """
        Returns:
            float: sum of base damage + assigned magic strength 
        """
        base_damage  = self.stats['attack']
        spell_damage = settings.magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index:int):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index:int):
        return list(self.upgrade_cost.values())[index]

    def __energy_recovery(self):
        """Recovery then player energy by x amount over time
        """
        max_energy = self.stats['energy']
        if self.energy < max_energy:
            # Recovery energy * magic stats
            self.energy += 0.01 * self.stats['magic']
            if self.energy > max_energy:
                self.energy = max_energy
    

    def update(self):
        """Update the game screen
        """
        self.__check_for_input()
        self.__set_status()
        self.__animate()
        self.__cooldowns()
        self.move(self.stats['speed'])
        self.__energy_recovery()    