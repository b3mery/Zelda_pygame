import pygame

import settings 
import utils
from player import Player
from entity import Entity


class Enemy(Entity):
    """_summary_

    Args:
        Entity (pygame.sprite.Sprite): _description_
    """
    def __init__(self, monster_name:str, pos:tuple, groups, obstacle_sprites) -> None:
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

    def __import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': [] }
        main_path = f'assets/graphics/monsters/{monster_name}/'
        for anamation in self.animations.keys(): 
            self.animations[anamation] = utils.import_folder(main_path + anamation)
    
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

        if distance <= self.attack_radius:
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
            print('attack')
        if self.status == 'move':
            self.direction = self.__get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def animate(self):
        """Animate the Game Object
        """
        anamation = self.animations[self.status]
        self.frame_index += self.anamation_speed
        if self.frame_index >= len(anamation):
            self.frame_index = 0

        # set the image
        self.image = anamation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()

    def enemy_update(self, player:Player) -> None:
        """_summary_

        Args:
            player (Player): _description_
        """
        self.__set_status(player)
        self.__actions(player)