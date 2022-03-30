import pygame

class ParticleEffect(pygame.sprite.Sprite):
    """Animate Particle Effects

    Extends:
        pygame (pygame.sprite.Sprite)
    """
    def __init__(self, pos, animation_frames, groups) -> None:
        super().__init__(groups)

        self.sprite_type = 'magic'
        self.frame_index = 0
        self.anamation_speed = 0.15
        self.frames = animation_frames
        self.image = animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    
    def animate(self):
        """update self.image to match current frame
        kill is out of range i.e. list has been interated completely.
        """
        self.frame_index += self.anamation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]


    def update(self ) -> None:
        """_summary_
        """
        self.animate()