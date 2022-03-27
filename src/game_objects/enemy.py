from pyclbr import Function
import pygame

from src.utils import settings 
from src.utils import util
from src.game_objects.player import Player
from src.game_objects.base.entity import Entity


class Enemy(Entity):
    """_summary_

    Args:
        Entity (pygame.sprite.Sprite): _description_
    """
    def __init__(self, monster_name:str, pos:tuple, groups, obstacle_sprites, damage_player:Function) -> None:
        super().__init__(groups)
        # General Setup
        self.sprite_type = 'enemy'

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

        # Player Interaction
        self.can_attack = True
        self.attack_cooldown_duration = 800
        self.attack_time = None

        self.damage_player = damage_player

        # Invincibility
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_cooldown_duration = 300

    def __import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': [] }
        main_path = f'assets/graphics/monsters/{monster_name}/'
        for anamation in self.animations.keys(): 
            self.animations[anamation] = util.import_folder(main_path + anamation)
    
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
            player (Player): _description_
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
            if self.status != 'attack':
                # Reset anamation 
                self.frame_index = 0
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            
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
        """_summary_
        """
        current_time = pygame.time.get_ticks()
        
        # Attack Cool Down
        if (not self.can_attack and current_time - self.attack_time >= self.attack_cooldown_duration ):
            self.can_attack = True
        
        # Invinciblity cool down
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_cooldown_duration:
            self.vulnerable = True

    def get_damage(self, player:Player, attack_type):
        """_summary_

        Args:
            player (Player): _description_
            attack_type (_type_): _description_
        """
        if self.vulnerable:
            # Update Direction 
            self.direction = self.__get_player_distance_direction(player)[1]
            
            # Update Timer
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            
            # Weapon Attack Types:
            if attack_type == 'weapon': 
                self.health -= player.get_full_weapon_damage()
            else: 
                # magic damage
                pass
            
    
    def __hit_reaction(self):
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

    def update(self) -> None:
        """_summary_
        """
        self.__hit_reaction()
        self.move(self.speed)
        self.__animate()
        self.__cooldowns()
        self.__check_death()

    def enemy_update(self, player:Player) -> None:
        """_summary_

        Args:
            player (Player): _description_
        """
        self.__set_status(player)
        self.__actions(player)