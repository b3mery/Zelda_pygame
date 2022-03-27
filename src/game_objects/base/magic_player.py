import pygame
import random

from src.animation.animation_player import AnimationPlayer
from src.game_objects.player import Player

from src.utils import settings

class MagicPlayer:
    """_summary_
    """
    def __init__(self, animation_player:AnimationPlayer) -> None:
        self.animation_player = animation_player


    def heal(self,player:Player, strength:int, cost:int, groups:list):
        """_summary_

        Args:
            player (Player): _description_
            strength (int): _description_
            cost (int): _description_
            groups (list): _description_
        """
        player_max_health = player.stats['health']
        if player.energy >= cost: #and player.health < player_max_health: 
            player.health += strength
            player.energy -= cost
            # if health has gone over max, set to max
            if player.health >= player_max_health:
                player.health = player_max_health
            
            # span particles:
            self.animation_player.create_particles('aura', player.rect.center, groups)
            offset = pygame.math.Vector2(0,-60)
            self.animation_player.create_particles('heal', player.rect.center + offset, groups)



    def flame(self, player:Player, cost:int, groups:list):
        """_summary_

        Args:
            player (Player): _description_
            cost (int): _description_
            groups (list): _description_
        """
        if player.energy >= cost:
            player.energy -= cost

            direction = self.__get_direction(player.status.split('_')[0])

            for i in range(1,6):
                # Horizontal
                if direction.x:
                    offset_x = ((direction.x * i) * settings.TILESIZE)
                    x = player.rect.centerx + offset_x + random.randint(-settings.TILESIZE // 3, settings.TILESIZE // 3)
                    y = player.rect.centery + random.randint(-settings.TILESIZE // 3, settings.TILESIZE // 3)
                # Vertical
                else:
                    offset_y = ((direction.y * i) * settings.TILESIZE)
                    x = player.rect.centerx + random.randint(-settings.TILESIZE // 3, settings.TILESIZE // 3)
                    y = player.rect.centery + offset_y + random.randint(-settings.TILESIZE // 3, settings.TILESIZE // 3)
                
                self.animation_player.create_particles('flame', (x,y), groups)

    def __get_direction(self, status:str):
        """Calculate the direction the player is facing

        Args:
            status (str): left,right,up, or down

        Returns:
            pygame.math.Vector2: Vector representing direction
        """
        if status == 'right':
            direction = pygame.math.Vector2(1,0)
        elif status == 'left':
            direction = pygame.math.Vector2(-1,0)
        elif status == 'down':
            direction = pygame.math.Vector2(0,1)
        else: # status == 'up':
            direction = pygame.math.Vector2(0,-1)

        return direction