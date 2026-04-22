import pygame
from player import MusicPlayer

pygame.init()
screen = pygame.display.set_mode((400, 200))
player = MusicPlayer("music/sample_tracks/")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: player.play()
            if event.key == pygame.K_s: player.stop()
            if event.key == pygame.K_n: player.next()
            if event.key == pygame.K_b: player.prev()

    screen.fill((50, 50, 50))
    pygame.display.flip()
pygame.quit()