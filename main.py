import pygame, sys
from src.utils import settings
from src.orchestration.level import Level
    
class Game:
    """Game Class"""
    def __init__(self) -> None:
        # General Setup
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))

        pygame.display.set_caption(f'Zelda Py 🔺')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        """PyGame Game Loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                # Toogle Menu    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_upgrade_menu()
                              
            self.screen.fill(settings.WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(settings.FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
    