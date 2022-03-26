import pygame

import settings 
from entity import Entity

import utils

class Enemy(Entity):
    """_summary_

    Args:
        Entity (pygame.sprite.Sprite): _description_
    """
    def __init__(self, monster_name:str, pos:tuple, groups) -> None:
        super().__init__(groups)
        # General Setup
        self.sprite_type = 'enemy'

        # Graphic Setup
        self.__import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def __import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': [] }
        main_path = f'assets/graphics/monsters/{monster_name}/'
        for anamation in self.animations.keys(): 
            self.animations[anamation] = utils.import_folder(main_path + anamation)
    
