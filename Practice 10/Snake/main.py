import pygame, random, sys
from pygame.locals import *

W, H = 600, 400
BLOCK = 20
FPS = 60 

# Список цветов для уровней (добавь сколько хочешь)
LEVEL_COLORS = [
    (46, 204, 113),  # Зеленый (Ур 1)
    (52, 152, 219),  # Синий (Ур 2)
    (155, 89, 182),  # Фиолетовый (Ур 3)
    (241, 196, 15),  # Желтый (Ур 4)
    (230, 126, 34),  # Оранжевый (Ур 5)
    (26, 188, 156),  # Бирюзовый (Ур 6)
    (255, 255, 255)  # Белый (Ур 7+)
]

COLOR_BG = (20, 25, 30)
COLOR_HEAD = (200, 100, 96)   
COLOR_FOOD = (231, 76, 60)  
COLOR_TEXT = (236, 240, 241)

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20, bold=True)

def get_random_food(snake):
    while True:
        x = random.randrange(0, W, BLOCK)
        y = random.randrange(0, H, BLOCK)
        if [x, y] not in snake:
            return x, y

def game():
    snake = [[100, 100], [80, 100], [60, 100]]
    dx, dy = BLOCK, 0
    next_dx, next_dy = dx, dy 
    food = get_random_food(snake)
    
    score = 0
    level = 1
    # Текущий цвет змейки (берем первый из списка)
    current_snake_color = LEVEL_COLORS[0]
    
    step_delay = 120
    last_step_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        screen.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w and dy == 0: next_dx, next_dy = 0, -BLOCK
                if event.key == K_s and dy == 0: next_dx, next_dy = 0, BLOCK
                if event.key == K_a and dx == 0: next_dx, next_dy = -BLOCK, 0
                if event.key == K_d and dx == 0: next_dx, next_dy = BLOCK, 0

        # Логика движения по таймеру
        if current_time - last_step_time > step_delay:
            dx, dy = next_dx, next_dy 
            new_head = [snake[0][0] + dx, snake[0][1] + dy]

            if (new_head[0] < 0 or new_head[0] >= W or 
                new_head[1] < 0 or new_head[1] >= H or 
                new_head in snake):
                return 

            snake.insert(0, new_head)

            if new_head == list(food):
                score += 1
                food = get_random_food(snake)
                if score % 5 == 0:
                    level += 1
                    step_delay = max(50, step_delay - 20) 
                    
                    # МЕНЯЕМ ЦВЕТ ПРИ РОСТЕ УРОВНЯ
                    # Используем остаток от деления (%), чтобы не выйти за пределы списка цветов
                    color_index = (level - 1) % len(LEVEL_COLORS)
                    current_snake_color = LEVEL_COLORS[color_index]
            else:
                snake.pop()
            
            last_step_time = current_time

        # Отрисовка
        pygame.draw.circle(screen, COLOR_FOOD, (food[0] + BLOCK//2, food[1] + BLOCK//2), BLOCK//2 - 2)

        for i, seg in enumerate(snake):
            # Голова остается своего цвета, а тело использует current_snake_color
            color = COLOR_HEAD if i == 0 else current_snake_color
            pygame.draw.rect(screen, color, [seg[0], seg[1], BLOCK-2, BLOCK-2])

        info = font.render(f"SCORE: {score}  LEVEL: {level}", True, COLOR_TEXT)
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(FPS) 

game()