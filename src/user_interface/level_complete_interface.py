import pygame, sys
from src.user_interface.base.title_menu_base import TitleMenuInterfaceBase

from src.utils import settings

class LevelCompleteInterface(TitleMenuInterfaceBase):
    """_summary_
    """
    def __init__(self, rebuild) -> None:
        super().__init__()
        # self.display_surface = pygame.display.get_surface()
        self.title = "Level Complete"
        self.title_font_color = settings.TITLE_TEXT_COLOR
        self.attribute_names = ['continue', 'quit']

        self.create_menu_items()
        self.rebuild = rebuild

    def trigger(self):
        selection = self.attribute_names[self.selection_index]
        if selection == 'continue':
            self.rebuild()

        if selection == 'quit':
            pygame.quit()
            sys.exit() 

    def display(self):
        super().display()
       
