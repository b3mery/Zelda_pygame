import pygame
from user_interface.base.menu_base import MenuBase 

from utils import settings

class TitleMenuInterfaceBase(MenuBase):
    """Base Class for Drawinging Title and Options to the game screen
    """
    def __init__(self) -> None:
        super().__init__()
        # General Setup:
        self.display_surface = pygame.display.get_surface()
        self.title = ''
        self.title_font_color = settings.UI_FONT  
        self.attribute_names:list = []
        self.title_font = pygame.font.Font(settings.UI_FONT, settings.TITLE_FONT_SIZE)
        
        self.height = self.display_surface.get_size()[1] * 0.10
        self.width = self.display_surface.get_size()[0] * 0.15
        self.create_menu_items()
        
    def __draw_title(self):
        title_surf = self.title_font.render(self.title,False, self.title_font_color, settings.TITLE_BG_COLOR)
        x = self.display_surface.get_size()[0] * 0.5
        y = self.display_surface.get_size()[1] * 0.3

        title_rect = title_surf.get_rect(midtop = (x,y))
        # title_rect.inflate(0,250)
        self.display_surface.blit(title_surf, title_rect)

    def create_menu_items(self):
        """Create item (buttons) from self.item list
        """
        self.item_list = []

        for item in range(len(self.attribute_names)):
            # horizontal
            full_width = self.display_surface.get_size()[0] 
            increment = full_width // len(self.attribute_names)
            left = (item * increment) + (increment - self.width) // 2 
            # vertical
            top = self.display_surface.get_size()[1] * 0.6 
            # create object:
            item_box = pygame.Rect(left, top, self.width, self.height)
            self.item_list.append(item_box)

    def __draw_selection_box(self, item_box, name:str, selected:bool):
        bg_color = settings.UPGRADE_BG_COLOR_SELECTED if selected else settings.UI_BG_COLOR
        border_coldor = settings.UI_BORDER_COLOR_ACTIVE if selected else settings.UI_BORDER_COLOR
        text_color = settings.TEXT_COLOR_SELECTED if selected else settings.TEXT_COLOR
        # create box        
        pygame.draw.rect(self.display_surface,bg_color, item_box)
        pygame.draw.rect(self.display_surface,border_coldor, item_box, 4)

        # Create label
        label_surf = self.font.render(name, False, text_color)
        label_rect = label_surf.get_rect(center = item_box.center)
        self.display_surface.blit(label_surf, label_rect)

    def __display_selection_box(self):
         for index, item_box in enumerate(self.item_list):
            item_name = self.attribute_names[index]
            self.__draw_selection_box(item_box, item_name, self.selection_index == index) 

    def display(self):
        super().display()
        self.__draw_title()
        self.__display_selection_box()
       
