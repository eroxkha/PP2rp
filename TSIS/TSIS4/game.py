import pygame
import random
import json
import os
from config import *


def load_settings():
    default = {
        'snake_color': list(GREEN),
        'grid': True,
        'sound': False
    }
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r') as f:
                data = json.load(f)
                default.update(data)
        except:
            pass
    return default


def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)


class Food:
    def __init__(self, ftype, pos):
        self.ftype = ftype  # 'normal', 'bonus', 'poison'
        self.pos = pos
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        # bonus food disappears after timer
        if self.ftype == 'bonus':
            return pygame.time.get_ticks() - self.spawn_time > FOOD_TIMER
        return False

    def draw(self, surface):
        color = FOOD_COLORS.get(self.ftype, RED)
        x = self.pos[0] * CELL_SIZE
        y = self.pos[1] * CELL_SIZE
        pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))


class PowerUp:
    def __init__(self, ptype, pos):
        self.ptype = ptype  # 'speed', 'slow', 'shield'
        self.pos = pos
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > POWERUP_FIELD_TIMER

    def draw(self, surface):
        color = POWERUP_COLORS.get(self.ptype, BLUE)
        x = self.pos[0] * CELL_SIZE
        y = self.pos[1] * CELL_SIZE
        pygame.draw.rect(surface, color, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        pygame.draw.rect(surface, WHITE, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 2)


class Snake:
    def __init__(self, color):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.color = color
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_dir(self, new_dir):
        # dont allow going backwards
        if (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        self.direction = new_dir

    def get_head(self):
        return self.body[0]

    def draw(self, surface):
        for i, seg in enumerate(self.body):
            x = seg[0] * CELL_SIZE
            y = seg[1] * CELL_SIZE
            color = self.color if i > 0 else tuple(min(255, c + 60) for c in self.color)
            pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)


class Game:
    def __init__(self, username, player_id, personal_best):
        self.settings = load_settings()
        self.snake = Snake(tuple(self.settings['snake_color']))
        self.username = username
        self.player_id = player_id
        self.personal_best = personal_best

        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.speed = FPS

        self.foods = []
        self.powerup = None
        self.obstacles = []

        self.active_effect = None  # ('speed'/'slow', end_time)
        self.shield = False

        self.spawn_food('normal')
        self.spawn_poison()

        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 36)

    def get_occupied(self):
        occupied = set()
        for s in self.snake.body:
            occupied.add(s)
        for f in self.foods:
            occupied.add(f.pos)
        if self.powerup:
            occupied.add(self.powerup.pos)
        for o in self.obstacles:
            occupied.add(o)
        return occupied

    def random_free_pos(self):
        occupied = self.get_occupied()
        attempts = 0
        while attempts < 200:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in occupied:
                return pos
            attempts += 1
        return None

    def spawn_food(self, ftype):
        pos = self.random_free_pos()
        if pos:
            self.foods.append(Food(ftype, pos))

    def spawn_poison(self):
        pos = self.random_free_pos()
        if pos:
            self.foods.append(Food('poison', pos))

    def spawn_powerup(self):
        if self.powerup is not None:
            return
        ptype = random.choice(['speed', 'slow', 'shield'])
        pos = self.random_free_pos()
        if pos:
            self.powerup = PowerUp(ptype, pos)

    def spawn_obstacles(self):
        # place 3 + level random obstacles, make sure snake head not trapped
        count = 3 + self.level
        head = self.snake.get_head()
        occupied = self.get_occupied()
        # safe zone around head
        safe = set()
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                safe.add((head[0] + dx, head[1] + dy))

        new_obs = []
        attempts = 0
        while len(new_obs) < count and attempts < 500:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in occupied and pos not in safe and pos not in new_obs:
                new_obs.append(pos)
            attempts += 1
        self.obstacles.extend(new_obs)

    def level_up(self):
        self.level += 1
        self.food_eaten = 0
        self.speed = FPS + SPEED_PER_LEVEL * (self.level - 1)
        if self.level >= 3:
            self.spawn_obstacles()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake.change_dir((0, -1))
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake.change_dir((0, 1))
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake.change_dir((-1, 0))
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake.change_dir((1, 0))

    def get_current_speed(self):
        now = pygame.time.get_ticks()
        if self.active_effect:
            etype, end_time = self.active_effect
            if now < end_time:
                if etype == 'speed':
                    return self.speed + 4
                elif etype == 'slow':
                    return max(1, self.speed - 4)
            else:
                self.active_effect = None
        return self.speed

    def update(self):
        # expire foods
        to_remove = []
        for f in self.foods:
            if f.is_expired():
                to_remove.append(f)
        for f in to_remove:
            self.foods.remove(f)

        # expire powerup on field
        if self.powerup and self.powerup.is_expired():
            self.powerup = None

        # maybe spawn powerup
        if self.powerup is None and random.random() < 0.005:
            self.spawn_powerup()

        self.snake.move()
        head = self.snake.get_head()

        # wall collision
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            if self.shield:
                self.shield = False
                # bounce back by putting head inside
                bx = max(0, min(GRID_WIDTH - 1, head[0]))
                by = max(0, min(GRID_HEIGHT - 1, head[1]))
                self.snake.body[0] = (bx, by)
            else:
                return 'game_over'

        # self collision
        if head in self.snake.body[1:]:
            if self.shield:
                self.shield = False
            else:
                return 'game_over'

        # obstacle collision
        if head in self.obstacles:
            if self.shield:
                self.shield = False
            else:
                return 'game_over'

        # food collision
        eaten_food = None
        for f in self.foods:
            if f.pos == head:
                eaten_food = f
                break

        if eaten_food:
            self.foods.remove(eaten_food)
            if eaten_food.ftype == 'poison':
                # shorten by 2
                if len(self.snake.body) <= 2:
                    return 'game_over'
                self.snake.body = self.snake.body[:-2]
                self.spawn_poison()
            else:
                pts = FOOD_POINTS.get(eaten_food.ftype, 1)
                self.score += pts
                self.food_eaten += 1
                self.snake.grow = True
                # respawn food
                if eaten_food.ftype == 'normal':
                    self.spawn_food('normal')
                    if random.random() < 0.3:
                        self.spawn_food('bonus')
                elif eaten_food.ftype == 'bonus':
                    pass  # bonus don't auto respawn
                if self.food_eaten >= LEVEL_UP_FOOD:
                    self.level_up()

        # powerup collision
        if self.powerup and self.powerup.pos == head:
            ptype = self.powerup.ptype
            self.powerup = None
            if ptype == 'shield':
                self.shield = True
            else:
                end_time = pygame.time.get_ticks() + POWERUP_EFFECT_TIMER
                self.active_effect = (ptype, end_time)

        return 'running'

    def draw(self, surface):
        surface.fill(DARK_GRAY)

        # grid
        if self.settings.get('grid', True):
            for x in range(0, SCREEN_WIDTH, CELL_SIZE):
                pygame.draw.line(surface, (70, 70, 70), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
                pygame.draw.line(surface, (70, 70, 70), (0, y), (SCREEN_WIDTH, y))

        # obstacles
        for obs in self.obstacles:
            ox = obs[0] * CELL_SIZE
            oy = obs[1] * CELL_SIZE
            pygame.draw.rect(surface, GRAY, (ox, oy, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, BLACK, (ox, oy, CELL_SIZE, CELL_SIZE), 1)

        for f in self.foods:
            f.draw(surface)

        if self.powerup:
            self.powerup.draw(surface)

        self.snake.draw(surface)

        # HUD
        score_txt = self.font.render(f"Score: {self.score}  Level: {self.level}  Best: {self.personal_best}", True, WHITE)
        surface.blit(score_txt, (5, 5))

        # active effects
        now = pygame.time.get_ticks()
        if self.active_effect:
            etype, end_time = self.active_effect
            remaining = max(0, (end_time - now) // 1000)
            eff_txt = self.font.render(f"Effect: {etype} ({remaining}s)", True, YELLOW)
            surface.blit(eff_txt, (5, 25))

        if self.shield:
            shield_txt = self.font.render("SHIELD ACTIVE", True, PURPLE)
            surface.blit(shield_txt, (5, 45))