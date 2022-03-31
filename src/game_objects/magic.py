import pygame
import random

from animation.animation_player import AnimationPlayer
from game_objects.player import Player

from utils import settings

class Magic:
    """Generate Plaer Magic
    """
    def __init__(self, animation_player:AnimationPlayer) -> None:
        self.animation_player = animation_player
        self.sounds ={
            'heal': pygame.mixer.Sound('assets/audio/heal.wav'),
            'flame': pygame.mixer.Sound('assets/audio/flame.wav')
        }


    def heal(self,player:Player, strength:int, cost:int, groups:list):
        """* If player has enough energy and player health is less than max:
            * Reduce player energy
            * increase player health by strength
                * if health goes beyond max, set at max
            * Generate aura animation
            * Generate health animation

        Args:
            player (Player): _description_
            strength (int): _description_
            cost (int): _description_
            groups (list): _description_
        """
        player_max_health = player.stats['health']
        if player.energy >= cost and player.health < player_max_health: 
            self.sounds['heal'].play()
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
        """* If player has enough energy:
            * Reduce player energy
            * Calculate player direction
            * Generate Flame animations

        Args:
            player (Player): Insanitated Player Object
            cost (int): cost of flame spell
            groups (list): sprite groups
        """
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()
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