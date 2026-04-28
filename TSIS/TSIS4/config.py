SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

FPS = 10

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
DARK_RED = (120, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
ORANGE = (255, 165, 0)
PURPLE = (160, 0, 160)
CYAN = (0, 200, 200)

FOOD_POINTS = {
    'normal': 1,
    'bonus': 3,
    'poison': 0
}

FOOD_TIMER = 5000  # ms, for disappearing food
POWERUP_FIELD_TIMER = 8000  # ms on field before disappear
POWERUP_EFFECT_TIMER = 5000  # ms effect lasts

FOOD_COLORS = {
    'normal': RED,
    'bonus': YELLOW,
    'poison': DARK_RED
}

POWERUP_COLORS = {
    'speed': ORANGE,
    'slow': CYAN,
    'shield': PURPLE
}

LEVEL_UP_FOOD = 5  # food to eat per level
SPEED_PER_LEVEL = 1

DB_CONFIG = {
    'host': 'localhost',
    'database': 'snake_game',
    'user': 'eroxkha',
    'password': 'Rerokha01',
    'port': 5432
}