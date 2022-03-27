import pygame 

from src.game_objects.player import Player
from src.utils import settings

class Upgrade:
    """_summary_
    """
    def __init__(self, player:Player) -> None:
        # General Setup:
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nbr = len(self.player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # Selection System:
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.selection_cooldown_duration = 300

    def input(self):
        """_summary_
        """
        keys = pygame.key.get_pressed()
        if not self.can_move:
            return None

        if keys[pygame.K_RIGHT] and self.selection_index < (self.attribute_nbr -1):
            self.selection_index += 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        
        if keys[pygame.K_LEFT] and self.selection_index >= 1:
            self.selection_index -= 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            
        if keys[pygame.K_SPACE]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.item_list[self.selection_index].trigger(self.player)


    def __cooldowns(self):
        """_summary_
        """
        current_time = pygame.time.get_ticks()
        if not self.can_move and current_time - self.selection_time >= self.selection_cooldown_duration:
            self.can_move = True

    def create_items(self):
        """_summary_
        """
        self.item_list = []

        for index, item in enumerate(range(self.attribute_nbr)):
            # horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nbr
            left = (item * increment) + (increment - self.width) // 2 
            # vertical
            top = self.display_surface.get_size()[1] * 0.1 # 10percent of y axis
            # create object:
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        """_summary_
        """
        # self.display_surface.fill('black')
        self.input()
        self.__cooldowns()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)



class Item:
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
