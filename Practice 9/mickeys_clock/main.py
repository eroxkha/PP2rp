import pygame
import datetime
from clock import rotate_hand

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


#mickey_hand = pygame.image.load("images/mickey_hand.png").convert_alpha()
mickey_hand = pygame.image.load("images/mickey_hand.png").convert() 
WHITE = (255, 255, 255)
GRAY = (247, 247, 247)
mickey_hand.set_colorkey(WHITE) 
mickey_hand = pygame.transform.scale(mickey_hand, (150, 350))


bg_image = pygame.image.load("images/main-clock.png").convert()
bg_image = pygame.transform.scale(bg_image, (W, H))


center = (W // 2, H // 2)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))
    
    now = datetime.datetime.now()
    sec_angle = -now.second * 6
    min_angle = -now.minute * 6

    
    rotate_hand(screen, mickey_hand, center, min_angle) # Минуты
    rotate_hand(screen, mickey_hand, center, sec_angle) # Секунды 
    # НЕ ЗАБУДЬ ПОМЕНЯТЬ руку на стрелку 

    pygame.display.flip()
    clock.tick(60)
pygame.quit()