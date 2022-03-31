import pygame, sys
from user_interface.base.title_menu_base import TitleMenuInterfaceBase

from utils import settings

class TitleScreenInterface(TitleMenuInterfaceBase):
    """Title Screen Interface responsible for Play or Quit interactions
    Extends: TitleMenuInterfaceBase
    """
    def __init__(self, activate_level) -> None:
        super().__init__()
        # self.display_surface = pygame.display.get_surface()
        self.title = settings.GAME_TITLE
        self.title_font_color = settings.TITLE_TEXT_COLOR
        self.attribute_names = ['play', 'quit']

        self.create_menu_items()
        self.activate_level = activate_level

    def trigger(self):
        selection = self.attribute_names[self.selection_index]
        if selection == 'play':
            self.activate_level()

        if selection == 'quit':
            pygame.quit()
            sys.exit() 

    def display(self):
        super().display()
       
