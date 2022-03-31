import pygame 

from game_objects.player import Player
from user_interface.base.menu_base import MenuBase
from user_interface.base.upgrade_menu_item import UpgradeMenuItem
from utils import settings

class UpgradeMenu(MenuBase):
    """Play Stats Upgrade Menu Interface
    Extends: MenuBase
    """
    def __init__(self, player:Player) -> None:
        # General Setup:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

    def trigger(self):
        self.item_list[self.selection_index].trigger_upgrade(self.player)

    def create_items(self):
        """Create Item Stats
        """
        self.item_list = []

        for index, item in enumerate(range(len(self.attribute_names))):
            # horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // len(self.attribute_names)
            left = (item * increment) + (increment - self.width) // 2 
            # vertical
            top = self.display_surface.get_size()[1] * 0.1 # 10percent of y axis
            # create object:
            item = UpgradeMenuItem(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        """Display Stats to Screen
        """
        super().display()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


