import pygame 

from src.game_objects.player import Player
from src.user_interface.menu_item import MenuItem
from src.utils import settings

class UpgradeMenu:
    """_summary_
    """
    def __init__(self, player:Player) -> None:
        # General Setup:
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nbr = len(self.player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # Selection System:
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.selection_cooldown_duration = 300

    def input(self):
        """_summary_
        """
        keys = pygame.key.get_pressed()
        if not self.can_move:
            return None

        if keys[pygame.K_RIGHT] and self.selection_index < (self.attribute_nbr -1):
            self.selection_index += 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        
        if keys[pygame.K_LEFT] and self.selection_index >= 1:
            self.selection_index -= 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            
        if keys[pygame.K_SPACE]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.item_list[self.selection_index].trigger(self.player)


    def __cooldowns(self):
        """_summary_
        """
        current_time = pygame.time.get_ticks()
        if not self.can_move and current_time - self.selection_time >= self.selection_cooldown_duration:
            self.can_move = True

    def create_items(self):
        """_summary_
        """
        self.item_list = []

        for index, item in enumerate(range(self.attribute_nbr)):
            # horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nbr
            left = (item * increment) + (increment - self.width) // 2 
            # vertical
            top = self.display_surface.get_size()[1] * 0.1 # 10percent of y axis
            # create object:
            item = MenuItem(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        """_summary_
        """
        # self.display_surface.fill('black')
        self.input()
        self.__cooldowns()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


