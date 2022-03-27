import pygame
from src.utils import settings
from src.game_objects.player import Player

class MenuItem:
    """_summary_
    """
    def __init__(self, left, top, width, height, index, font) -> None:
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
    
    def __display_names(self, surface, name, cost, selected:bool):
        """_summary_

        Args:
            surface (_type_): _description_
            name (_type_): _description_
            cost (_type_): _description_
            selected (_type_): _description_
        """
        color = settings.TEXT_COLOR_SELECTED if selected else settings.TEXT_COLOR

        # title
        title_surf = self.font.render(name,False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        # cost
        cost_surf = self.font.render(str(int(cost)),False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0, -20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
    
    def trigger(self, player:Player):
        """_summary_

        Args:
            player (Player): _description_
        """
        upgrade_attribute = list(player.stats.keys())[self.index]
        upgrade_cost = player.upgrade_cost[upgrade_attribute]
        current_stat = player.stats[upgrade_attribute]
        stat_max = player.max_stats[upgrade_attribute] 
        if player.exp >= upgrade_cost and current_stat < stat_max:
            # decrease exp
            player.exp -= player.upgrade_cost[upgrade_attribute]
            # upgrade
            player.stats[upgrade_attribute] *= 1.2
            # incrase cost
            player.upgrade_cost[upgrade_attribute] *= 1.4

            # limit upgrade to max stat
            if player.stats[upgrade_attribute] > stat_max:
                player.stats[upgrade_attribute] = stat_max

            if upgrade_attribute == 'health':
                player.health = player.stats['health']

            if upgrade_attribute == 'energy':
                player.energy =  player.stats['energy']



    def __display_bar(self, surface, value, max_value, selected):
        # drawing setup
        color = settings.BAR_COLOR_SELECTED if selected else settings.BAR_COLOR
        top = self.rect.midtop + pygame.math.Vector2(0,60) 
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)

        # bar setup
        full_height = bottom[1] - top[1] # subtract y axis
        relative_number = (value / max_value) * full_height 
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # Draw
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)



    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface,settings.UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface,settings.UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface,settings.UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface,settings.UI_BORDER_COLOR, self.rect, 4)
        self.__display_names(surface, name, cost, self.index == selection_num)
        self.__display_bar(surface, value, max_value, self.index == selection_num)
