import pygame

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



    def flame(self):
        pass