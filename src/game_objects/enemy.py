from pyclbr import Function
import pygame

from utils import settings 
from utils import util
from game_objects.player import Player
from game_objects.base.entity import Entity


class Enemy(Entity):
    """Enemy Game Object Class

    Extends:
        Entity (pygame.sprite.Sprite): Base Game Object Class
    """
    def __init__(self, monster_name:str, pos:tuple, groups, obstacle_sprites,level_nbr, damage_player:Function, trigger_death_particles:Function, add_exp:Function) -> None:
        super().__init__(groups)
        # General Setup
        self.sprite_type = 'enemy'
        self.level_upgrade_factor = level_nbr * settings.LEVEL_INCREASE_PERCENT
        # Graphic Setup
        self.__import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        
        # Stats
        self.monster_name = monster_name
        monster_info = settings.monster_data[self.monster_name]
        self.health = monster_info['health']  
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        self.__upgrade_stats_for_level()

        # Player Interaction
        self.can_attack = True
        self.attack_cooldown_duration = 800
        self.attack_time = None
        # Player Interaction Functions
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # Invincibility
        self.vulnerable = True
        self.hurt_time = None
        self.vulnerability_cooldown_duration = 300
        # sounds
        self.hit_sound = pygame.mixer.Sound('assets/audio/hit.wav')
        self.death_sound = pygame.mixer.Sound('assets/audio/death.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.3)

    def __upgrade_stats_for_level(self):
        self.health += self.health * self.level_upgrade_factor
        self.exp += self.exp * self.level_upgrade_factor
        self.speed += self.speed * self.level_upgrade_factor
        self.attack_damage += self.attack_damage * self.level_upgrade_factor

    def __import_graphics(self, monster_name):
        """Import the monster graphics from the monsters folder

        Args:
            monster_name (str): monster name corresponding to the monster folder
        """
        self.animations = {'idle': [], 'move': [], 'attack': [] }
        main_path = f'assets/graphics/monsters/{monster_name}/'
        for anamation in self.animations.keys(): 
            self.animations[anamation] = util.import_folder_images(main_path + anamation)
    
    def __get_player_distance_direction(self,player:Player):
        """Apply vector maths on Enemy Vector and Player Vector to calculate
        then enemy distance and direction from the player

        Args:
            player (Player): Insanitated Player Object

        Returns:
            tuple: (distance, direction)
        """
        enemy_vect = pygame.math.Vector2(self.rect.center)
        player_vect = pygame.math.Vector2(player.rect.center)
        # convert vector into distance
        distance = (player_vect - enemy_vect).magnitude() 
        
        if distance > 0:
            # Normalize verctor difference to calc direction
            direction = (player_vect - enemy_vect).normalize() 
        else:
            # if 0, player and enemy are already together
            direction = pygame.math.Vector2()
        
        return (distance, direction)

    def __set_status(self, player:Player):
        """Check the Distance from the Player, update Status

        Args:
            player (Player): Insanitated Player object
        """
        distance = self.__get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def __actions(self, player:Player):
        """Check status, complete an actions (attack, move, idle)

        Args:
            player (Player): Insanitated Player object
        """
        if self.status == 'attack':
            # if self.status != 'attack':
                # Reset anamation 
                # self.frame_index = 0
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()

        if self.status == 'move':
            self.direction = self.__get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def __animate(self):
        """Animate the Game Object
        """
        anamation = self.animations[self.status]
        self.frame_index += self.anamation_speed
        if self.frame_index >= len(anamation):
            # play the full  
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = anamation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # Flicker 
        if not self.vulnerable: 
            # Flicker 0 -255
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else: 
            self.image.set_alpha(255)
    
    def __cooldowns(self):
        """Cool down timer methods 
        """
        current_time = pygame.time.get_ticks()
        
        # Attack Cool Down
        if (not self.can_attack and current_time - self.attack_time >= self.attack_cooldown_duration ):
            self.can_attack = True
        
        # Invincibility cool down
        if not self.vulnerable and current_time - self.hurt_time >= self.vulnerability_cooldown_duration:
            self.vulnerable = True

    def get_damage(self, player:Player, attack_type):
        """Calculate the damage inflicted by player

        Args:
            player (Player): Instanitated Player object
            attack_type (str): 'weapon' or 'magic'
        """
        if self.vulnerable:
            self.hit_sound.play()
            # Update Direction 
            self.direction = self.__get_player_distance_direction(player)[1]
            
            # Update Timer
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()
            
            # Weapon Attack Types:
            if attack_type == 'weapon': 
                self.health -= player.get_full_weapon_damage()
            else: 
                # magic damage
                self.health -= player.get_full_magic_damage()
            
    def hit_reaction(self):
        """Move the enemy back if they have been hit
        """
        if not self.vulnerable:
            self.direction *=  -self.resistance
    
    def __check_death(self):
        """Check if health is less than or equal to 0,
        kill sprite
        """
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def update(self) -> None:
        """Extends pygame update, updates the game screen
        """
        self.hit_reaction()
        self.move(self.speed)
        self.__animate()
        self.__cooldowns()
        self.__check_death()

    def enemy_update(self, player:Player) -> None:
        """Custom Update Game screen method for player interactions

        Args:
            player (Player): Insanitated Player Object
        """
        self.__set_status(player)
        self.__actions(player)