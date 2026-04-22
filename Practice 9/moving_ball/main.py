import pygame
from ball import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

x, y = WIDTH // 2, HEIGHT // 2
running = True

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            x, y = move_ball(x, y, event.key)

    pygame.draw.circle(screen, RED, (x, y), BALL_RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()