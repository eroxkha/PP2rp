import pygame, random, sys
from pygame.locals import *

# --- НАСТРОЙКИ ---
W, H = 800, 500
BLOCK = 25
FPS = 60

# Цвета
COLOR_BG = (15, 15, 20)
COLOR_UI = (236, 240, 241)
SNAKE_COLORS = [(46, 204, 113), (52, 152, 219), (155, 89, 182), (241, 196, 15)]

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Arial", 50, bold=True)
font_small = pygame.font.SysFont("Arial", 25, bold=True)

def get_random_food(snake):
    while True:
        x = random.randrange(BLOCK, W - BLOCK, BLOCK)
        y = random.randrange(BLOCK, H - BLOCK, BLOCK)
        if [x, y] not in snake: return x, y

def show_menu():
    """Главное меню: выбор сложности"""
    while True:
        screen.fill(COLOR_BG)
        title = font_big.render("SNAKE PRO", True, COLOR_UI)
        screen.blit(title, (W//2 - 130, H//4))
        
        hint = font_small.render("Choose Difficulty:", True, (150, 150, 150))
        screen.blit(hint, (W//2 - 100, H//2 - 40))

        # Кнопки выбора
        draw_btn("1 - EASY", W//2 - 150, H//2)
        draw_btn("2 - MEDIUM", W//2 - 150, H//2 + 50)
        draw_btn("3 - HARD", W//2 - 150, H//2 + 100)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1: return 250 # Задержка для Easy
                if event.key == K_2: return 150 # Medium
                if event.key == K_3: return 80  # Hard

def draw_btn(txt, x, y):
    t = font_small.render(txt, True, (46, 204, 113))
    screen.blit(t, (x, y))

def game(start_delay):
    snake = [[W//2, H//2], [W//2-BLOCK, H//2], [W//2-2*BLOCK, H//2]]
    dx, dy = BLOCK, 0
    next_dx, next_dy = dx, dy
    food = get_random_food(snake)
    
    score = 0
    step_delay = start_delay
    last_step = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        
        # 1. Мгновенный ввод
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key in [K_w, K_UP] and dy == 0: next_dx, next_dy = 0, -BLOCK
                if event.key in [K_s, K_DOWN] and dy == 0: next_dx, next_dy = 0, BLOCK
                if event.key in [K_a, K_LEFT] and dx == 0: next_dx, next_dy = -BLOCK, 0
                if event.key in [K_d, K_RIGHT] and dx == 0: next_dx, next_dy = BLOCK, 0

        # 2. Логика шага
        if now - last_step > step_delay:
            dx, dy = next_dx, next_dy
            head = [snake[0][0] + dx, snake[0][1] + dy]

            if head[0] < 0 or head[0] >= W or head[1] < 0 or head[1] >= H or head in snake:
                return # Проиграл — выходим в меню

            snake.insert(0, head)
            if head == list(food):
                score += 1
                food = get_random_food(snake)
                step_delay = max(50, step_delay - 2) # Плавное ускорение
            else:
                snake.pop()
            last_step = now

        # 3. Отрисовка
        screen.fill(COLOR_BG)
        # Еда
        pygame.draw.rect(screen, (255, 50, 80), (food[0]+2, food[1]+2, BLOCK-4, BLOCK-4), border_radius=5)
        # Змейка
        for i, seg in enumerate(snake):
            color = (255, 255, 255) if i == 0 else SNAKE_COLORS[score % 4]
            pygame.draw.rect(screen, color, (seg[0]+1, seg[1]+1, BLOCK-2, BLOCK-2), border_radius=4)
        
        score_txt = font_small.render(f"SCORE: {score}", True, COLOR_UI)
        screen.blit(score_txt, (20, 20))
        
        pygame.display.flip()
        clock.tick(FPS)

# Вечный цикл: Меню -> Игра -> Меню
while True:
    difficulty = show_menu()
    game(difficulty)