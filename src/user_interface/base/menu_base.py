import pygame 

from utils import settings
class MenuBase:
    """Base Menu UI Class for keyboard selection 
    """
    def __init__(self) -> None:
        # General Setup:
        self.display_surface = pygame.display.get_surface()
        self.attribute_names:list = []
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # Selection System:
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.selection_cooldown_duration = 300

    def input(self):
        """Keyboard input 
        """
        keys = pygame.key.get_pressed()
        if not self.can_move:
            return None

        if keys[settings.RIGHT] and self.selection_index < (len(self.attribute_names) -1):
            self.selection_index += 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        
        if keys[settings.LEFT] and self.selection_index >= 1:
            self.selection_index -= 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            
        if keys[settings.OK]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.trigger()


    def cooldowns(self):
        """Keyboard selection cooldown method
        """
        current_time = pygame.time.get_ticks()
        if not self.can_move and current_time - self.selection_time >= self.selection_cooldown_duration:
            self.can_move = True

    def trigger(self):
        """Override Method
        Used to select an item
        """
        print(f"Selected item index: {self.selection_index}, attribute: {self.attribute_names[self.selection_index]}. If your're seeing this, methodd needs to be overridden")


    def display(self):
        """Update Input and Cooldowns
        """
        self.input()
        self.cooldowns()
