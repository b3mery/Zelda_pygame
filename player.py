from pyclbr import Function
import pygame

from entity import Entity 
import settings
import utils


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
                 create_magic:Function  
                ):
        super().__init__(groups)
        self.image = pygame.image.load('assets/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

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


        # Stats
        self.stats = {
            'health': 100,
            'energy':60,
            'attack': 10,
            'magic': 4,
            'speed': 5
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

    def __import_player_assets(self):
        """Import player graphic assets from player sub folders
        """
        character_path = "assets/graphics/player/"
        self.animations = {
            # Movement 
            'up' : [],
            'down': [],
            'left': [],
            'right': [],
            # idle
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            # Attack
            'right_attack': [],
            'left_attack': [],
            'up_attack' : [],
            'down_attack': []
        } 
        for animation_state in self.animations.keys():
            folder_path = f"{character_path}/{animation_state}"
            self.animations[animation_state] = utils.import_folder(folder_path)

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
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # Horizontal Inputs
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
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
        if keys[pygame.K_SPACE]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
    
    def __switch_weapon_input(self):
        """* Check for switch weapon input
        * Check if can switch
        * Update can_switch
        * Update weapon_index
        """
        keys = pygame.key.get_pressed()
        # Switch Weapon        
        if keys[pygame.K_q] and self.can_switch_weapon:
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
        if keys[pygame.K_LCTRL]:
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
        if keys[pygame.K_e] and self.can_switch_magic:
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
        """_summary_
        """
        current_time = pygame.time.get_ticks()
        
        # Player Attack Cool Down
        if (self.is_attacking and current_time - self.attack_time >= self.attack_cooldown ):
            self.is_attacking = False
            self.destroy_attack()

        # Switch Weapons cool down
        if (not self.can_switch_weapon and current_time - self.weapon_switch_time >= self.switch_duration_cooldown ):
            self.can_switch_weapon = True
        
        # Switch Magic cool down
        if (not self.can_switch_magic and current_time - self.magic_switch_time >= self.switch_duration_cooldown ):
            self.can_switch_magic = True

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

    def update(self):
        """Update the game screen
        """
        self.__check_for_input()
        self.__set_status()
        self.__animate()
        self.__cooldowns()
        self.move(self.speed)    