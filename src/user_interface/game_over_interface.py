import pygame, sys
from user_interface.base.title_menu_base import TitleMenuInterfaceBase
from utils import settings

class GameOverInterface(TitleMenuInterfaceBase):
    """Game Over user interface for restarting or quitting the game
    Extends: TitleMenuInterfaceBase
    """
    def __init__(self, rebuild) -> None:
        super().__init__()
        self.title = 'Game Over'
        self.title_font_color = settings.GAME_OVER_TEXT_COLOR  
        self.attribute_names = ['try again', 'quit']

        self.create_menu_items()
        self.rebuild = rebuild

    def trigger(self):
        selection = self.attribute_names[self.selection_index]
        if selection == 'try again':
            self.rebuild()

        if selection == 'quit':
            pygame.quit()
            sys.exit() 

    def display(self):
        super().display()
       
