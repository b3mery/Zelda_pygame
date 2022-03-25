from numpy import character
import pygame
from debug import debug 
import settings
import utils

class Player(pygame.sprite.Sprite):
    """Player Game Object Class

    Extends: pygame (pygame.sprite.Sprite)
    """
    def __init__(self,pos,groups, obstacle_sprites:pygame.sprite.Group):
        super().__init__(groups)
        self.image = pygame.image.load('assets/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

        # Graphics Set up
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.anamation_speed = 0.15
        
        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5 
        self.is_attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        """Import player graphic assets from player sub folders
        """
        character_path = "assets/graphics/player/"
        self.animations = {
            # Movement 
            'up' : [],
            'down': [],
            'left': [],
            'right': [],
            # idle
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            # Attack
            'right_attack': [],
            'left_attack': [],
            'up_attack' : [],
            'down_attack': []
        } 
        for animation_state in self.animations.keys():
            folder_path = f"{character_path}/{animation_state}"
            self.animations[animation_state] = utils.import_folder(folder_path)

    def input(self):
        """Monitor for keybaord input"""
        if self.is_attacking:
            return None
        keys = pygame.key.get_pressed()

        # Vertical Inputs
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # Horizontal Inputs
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
    
        # Attack Input:
        if keys[pygame.K_SPACE]:
            self.is_attacking = True
            self. attack_time = pygame.time.get_ticks()

        # Magic Input
        if keys[pygame.K_LCTRL]:
            self.is_attacking = True
            self. attack_time = pygame.time.get_ticks()
            print('Magic')

    def get_status(self):
        """Calculate the player.status based on direction and attacking
        """
        # idle status:
        if self.direction.x == 0  and self.direction.y == 0 and 'idle' not in self.status and not 'attack' in self.status:
            self.status = self.status + '_idle'
        
        # Attack status:
        if self.is_attacking:
            self.direction.x = 0 
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack') 
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self,speed):
        """Move the Player"""
        # Check vector length and normalize
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.check_collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.check_collisions('vertical')
        self.rect.center = self.hitbox.center

    def check_collisions(self, direction:str):
        """Check collisions

        Args:
            direction (str): horizontal or vertical
        """
        if direction == 'horizontal':
            self.check_horizontal_collisions()

        if direction == 'vertical':
            self.check_vertical_collisions()

    def check_horizontal_collisions(self):
        """Check Sprite collisions on x Axis
        """
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0: # moving right
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0: # moving left
                    self.hitbox.left = sprite.hitbox.right

    def check_vertical_collisions(self):
        """Check for sprite collisions on the y Axis
        """
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0: # moving down
                    self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0: # moving moving up
                    self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        """_summary_
        """
        current_time = pygame.time.get_ticks()
        if (self.is_attacking and current_time - self.attack_time >= self.attack_cooldown ):
            self.is_attacking = False

    def animate(self):
        """_summary_
        """
        anamation = self.animations[self.status]
        self.frame_index += self.anamation_speed

        if self.frame_index >= len(anamation):
            self.frame_index = 0

        # set the image
        self.image = anamation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        """Update the game screen
        """
        self.input()
        self.get_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)
        debug(self.status)
    