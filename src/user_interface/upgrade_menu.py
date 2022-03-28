import pygame 

from src.game_objects.player import Player
from src.user_interface.base.menu_base import MenuBase
from src.user_interface.menu_item import MenuItem
from src.utils import settings

class UpgradeMenu(MenuBase):
    """_summary_
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
        """_summary_
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
            item = MenuItem(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        """_summary_
        """
        super().display()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


