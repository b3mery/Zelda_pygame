import pygame
from utils import settings
from game_objects.player import Player

class UpgradeMenuItem():
    """Base Menu Item for each Stat Item
    """
    def __init__(self, left, top, width, height, index, font) -> None:
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
    
    def __display_names(self, surface, name, cost, value, max_value, selected:bool):
        """Draw the Names to game screen

        Args:
            surface (pygame.display_suraface): the game surface
            name (str): name of stat
            cost (int or float): cost of the stat
            selected (bool): currently selected 
        """
        color = settings.TEXT_COLOR_SELECTED if selected else settings.TEXT_COLOR

        # title
       
        title_surf = self.font.render(name,False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))
        
        stat = f"{int(value)}/{int(max_value)}" 
        stat_surf = self.font.render(stat,False, color)
        stat_rect = stat_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 40))
        # cost
        cost_str = f"cost: {int(cost)}"
        cost_surf = self.font.render(cost_str,False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0, -20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(stat_surf, stat_rect)
        surface.blit(cost_surf, cost_rect)

    def __display_bar(self, surface, value, max_value, selected):
        """Draw stat bar """
        # drawing setup
        color = settings.BAR_COLOR_SELECTED if selected else settings.BAR_COLOR
        top = self.rect.midtop + pygame.math.Vector2(0,80) 
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)

        # bar setup
        full_height = bottom[1] - top[1] # subtract y axis
        relative_number = (value / max_value) * full_height 
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # Draw
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    
    def trigger_upgrade(self, player:Player):
        """Trigger Selection, upgrade each stat if allowed

        Args:
            player (Player): Insanitated Player Object
        """
        upgrade_attribute = list(player.stats.keys())[self.index]
        upgrade_cost = player.upgrade_cost[upgrade_attribute]
        current_stat = player.stats[upgrade_attribute]
        stat_max = player.max_stats[upgrade_attribute] 
        print(stat_max)
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

    def display(self, surface, selection_num, name, value, max_value, cost):
        """Display Items on screen"""
        if self.index == selection_num:
            pygame.draw.rect(surface,settings.UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface,settings.UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface,settings.UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface,settings.UI_BORDER_COLOR, self.rect, 4)
        self.__display_names(surface, name, cost, value, max_value, self.index == selection_num)
        self.__display_bar(surface, value, max_value, self.index == selection_num)
