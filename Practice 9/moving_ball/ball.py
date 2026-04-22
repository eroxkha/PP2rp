import pygame

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BALL_RADIUS = 25
STEP = 20

def move_ball(x, y, key):
    if key == pygame.K_UP and y - STEP - BALL_RADIUS >= 0:
        y -= STEP
    elif key == pygame.K_DOWN and y + STEP + BALL_RADIUS <= HEIGHT:
        y += STEP
    elif key == pygame.K_LEFT and x - STEP - BALL_RADIUS >= 0:
        x -= STEP
    elif key == pygame.K_RIGHT and x + STEP + BALL_RADIUS <= WIDTH:
        x += STEP
    return x, y