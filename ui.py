import pygame
from player import Player
import settings

class UI:
    """User Interface Heads up Display
    Draws the Stats and Weapon/Magic to the game screen
    """
    def __init__(self) -> None:       
        # General Info:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # Bar Setup
        self.health_bar_rect = pygame.Rect(10,10,settings.HEALTH_BAR_WIDTH,settings.BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,settings.ENERGY_BAR_WIDTH,settings.BAR_HEIGHT)

        # Weapon Graphics
        self.weapon_graphics = []
        self.__build_weapon_graphics()

    def __build_weapon_graphics(self):
        """* Selects weapon graphic pass from weapons data dict.
        * Insanities a pygame.image from the path
        * stores image in self.weapon_graphics list
        
        """
        for weapon in settings.weapon_data.values():
            path = weapon['graphic']
            img = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(img)

    def __show_bar(self, cur_amount, max_amount, bg_rect:pygame.Rect, color):
        """Draw a Rect Bar to display stats

        Args:
            cur_amount (int): current stat amount
            max_amount (int): max stat amount
            bg_rect (pygame.Rect): instantiated background rect
            color (str): color code
        """
        # Draw background 
        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, bg_rect)

        # convert stat to pixels
        ratio = cur_amount / max_amount
        cur_width = bg_rect.width * ratio
        cur_rect = bg_rect.copy()
        cur_rect.width = cur_width

        # Draw bar
        pygame.draw.rect(self.display_surface, color, cur_rect)
        # Draw border 
        pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, bg_rect, 3)

    def __show_exp(self, exp:int):
        """Draw experience points to game screen

        Args:
            exp (int): experience points
        """
        exp = str(int(exp))
        exp_desc = f"EXP: {exp}"
        # build display
        text_surf = self.font.render(exp_desc, False, settings.TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x,y))

        # display on game screen
        # background
        pygame.draw.rect(self.display_surface,settings.UI_BG_COLOR, text_rect.inflate(20,20))
        # contents
        self.display_surface.blit(text_surf, text_rect)
        # border
        pygame.draw.rect(self.display_surface,settings.UI_BORDER_COLOR, text_rect.inflate(20,20),3)

    def __selection_box(self, left, top, has_switched:bool):
        """Draw game item selection box

        Args:
            left (int): left position 
            top (int): top position
            has_switched (bool): if player is switching

        Returns:
            pygame.Rect: Rect of the selection box created
        """
        bg_rect = pygame.Rect(left, top, settings.ITEM_BOX_SIZE, settings.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def __weapon_overlay(self, weapon_index:int, has_switched:bool):
        """Draw current selected weapon to the Game Screen

        Args:
            weapon_index (int): Selected Weapon Index
            has_switched (bool): If the user has just switched weapons
        """
        bg_rect = self.__selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def display(self, player:Player):
        """Draw UI Items to the Game Screen

        Args:
            player (Player): Insanitated Player Object
        """
        self.__show_bar(player.health,player.stats['health'],self.health_bar_rect, settings.HEALTH_COLOR)
        self.__show_bar(player.energy,player.stats['energy'],self.energy_bar_rect, settings.ENERGY_COLOR)
        self.__show_exp(player.exp)
        self.__weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.__selection_box(80, 630, False) # Magic