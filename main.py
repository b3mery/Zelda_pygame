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

        # main sound
        self.main_sound = pygame.mixer.Sound(open('assets/audio/main.ogg'))
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=1)

    def run(self):
        """PyGame Game Loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                              
            self.screen.fill(settings.WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(settings.FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
    