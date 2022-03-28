import pygame 

from src.utils import settings

class GameOverInterface:
    """_summary_
    """
    def __init__(self) -> None:
        # General Setup:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)
    
    def draw(self, name):
        title_surf = self.font.render(name,False, 'red')
        
        x = self.display_surface.get_size()[0] * 0.5
        y = self.display_surface.get_size()[1] * 0.5

        title_rect = title_surf.get_rect(midtop = (x,y))
        self.display_surface.blit(title_surf, title_rect)

    def display(self):
        self.display_surface.fill('black')
        self.draw('Game Over')
