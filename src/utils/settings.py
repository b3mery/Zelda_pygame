import pygame
GAME_TITLE = 'Zelda: A Link To The Py'

############################################### Game Setup #####################################################################
WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': (-10, -26),
    'object': (0,-64),
    'grass': (0,-10),
    'invisible': (0,0)
}

NBR_OF_LEVELS = 5
LEVEL_INCREASE_PERCENT = 0.10

MAIN_AUDIO_FILE = 'assets/audio/main.ogg'

############################################### Keyboard Input ################################################################
UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT

OK = pygame.K_RALT 

ATTACK = pygame.K_SPACE
MAGIC = pygame.K_LALT

MENU = pygame.K_m

SWAP_WEAPON = pygame.K_LCTRL
SWAP_MAGIC = pygame.K_LSHIFT

############################################### Display #######################################################################
# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'assets/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
TEXT_COLOR_SELECTED = '#111111'

# Title 
TITLE_FONT_SIZE = 40
TITLE_BG_COLOR = '#4D96FF' 
# Game over
GAME_OVER_TEXT_COLOR = '#d11500'
GAME_WON_TEXT_COLOR = '#6BCB77'
# Title Screen
TITLE_TEXT_COLOR = '#FFD93D'
 
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
 
# upgrade menu
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

####################################### Player Attributes #################################################################
# Stats
player_stats = {
    'health': 100,
    'energy':60,
    'attack': 10,
    'magic': 4,
    'speed': 5,
}
player_max_stats = {
    'health': 300, 
    'energy': 140, 
    'attack': 20, 
    'magic' : 10,
    'speed': 10
}
player_upgrade_cost = {
    'health': 100,
    'energy': 100, 
    'attack': 100, 
    'magic' : 100, 
    'speed': 100
}

player_animations = {
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

######################################### Player Weapons #############################################################
# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'assets/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'assets/graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'assets/graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'assets/graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'assets/graphics/weapons/sai/full.png'}}

# magic
magic_data = {
    'flame': {'strength': 5,'cost': 20,'graphic':'assets/graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20,'cost': 10,'graphic':'assets/graphics/particles/heal/heal.png'}}

####################################### Enemies #########################################################################

# enemy
monster_id_mapping = {
    '390': 'bamboo',
    '391': 'spirit',
    '392': 'raccoon',
    '393' : 'squid'
}

monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'assets/audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'assets/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300} }