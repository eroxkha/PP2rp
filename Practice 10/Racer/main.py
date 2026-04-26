import pygame
from pygame.locals import *
import random

pygame.init()
W, H = 400, 600
COIN_SCORE = 0 
font_small = pygame.font.SysFont("Verdana", 20)
screen = pygame.display.set_mode((400, 600))
coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, (0, 0, 0))
screen.blit(coin_text, (W - 150, 10))

class player_car(pygame.sprite.Sprite):
    def __init__(self,path="image\player_car.png"):
        super().__init__()
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image,(75,150))
        self.rect = self.image.get_rect()
        self.rect.center = (47,525)
    
    def move(self):
        button = pygame.key.get_pressed()

        if button[K_a]:
            self.rect.centerx -= 3
        elif button[K_d]:
            self.rect.centerx += 3
        # boundary condition for the position of the car
        if self.rect.centerx < 47:
            self.rect.centerx = 47
        if self.rect.centerx > 253:
            self.rect.centerx = 253

    


class opposing_car(pygame.sprite.Sprite):
    def __init__(self,path = "image\enemy_car.png"):
        super().__init__()
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image,(75,150))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47,253),75)
        self.speed = 5
        self.score = 0
    
    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 675:
            self.rect.centery = -75
            self.rect.centerx = random.randint(47,253)
            self.score += 10

import random


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            img = pygame.image.load("image/coin.png")
            self.image = pygame.transform.scale(img, (100, 100))
        except:
            self.image = pygame.Surface((100, 100))
            self.image.fill((255, 215, 0)) # Желтый квадрат, если нет картинки
        self.rect = self.image.get_rect(center=(random.randint(40, W-40), -50))

    def move(self):
        self.rect.move_ip(0, 5) # Скорость монетки
        if self.rect.top > H:
            self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, W-40), -50)


class background_loading:
    def __init__(self, path = "image/road.png"):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image,(400,600))
        rect1 = self.image.get_rect()
        rect2 = self.image.get_rect()
        rect2.centery += 300
        rect3 = self.image.get_rect()
        rect3.centery += 600
        self.rectangles = []
        self.rectangles.append(rect1)
        self.rectangles.append(rect2)
        self.rectangles.append(rect3)


    def draw(self):
        for rectangle in self.rectangles:
            screen.blit(self.image,rectangle)
    
    def move(self):
        for rectangle in self.rectangles:
            rectangle.centery+=2
            if rectangle.centery>750:
                rectangle.centery = -150



    

player = player_car()
opponent = opposing_car()

cars = pygame.sprite.Group()
cars.add(player)
cars.add(opponent)

opponents = pygame.sprite.Group()
opponents.add(opponent)

honk_sound = pygame.mixer.Sound("honk.mp3")

running = True



background = background_loading()

enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group() 

P1 = player_car()
E1 = opposing_car()
C1 = Coin()

enemies.add(E1)
coins.add(C1)

all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

C1 = Coin()
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites.add(C1) 

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    background.move()
    background.draw()

    

    for car in cars:
        screen.blit(car.image,car.rect)
        car.move()
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += 1
    for coin in coins:
        coin.rect.top = 0
        coin.rect.center = (random.randint(40, W-40), 0)


    if pygame.sprite.spritecollideany(player,opponents):
        screen.fill((125,50,50))
        font = pygame.font.SysFont("open dyslexic",18)
        text = font.render("Your final score is: " + str(opponent.score),True,(0,255,255))
        rect = text.get_rect()
        rect.center = (150,300)
        honk_sound.play()
        screen.blit(text,rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
    
    coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, (0, 0, 0))
    screen.blit(coin_text, (W - 150, 10))
    
    pygame.time.Clock().tick(60)
    pygame.display.flip()
 