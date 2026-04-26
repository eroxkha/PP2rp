import pygame, random, sys
from pygame.locals import *

pygame.init()
W, H = 400, 600
screen = pygame.display.set_mode((W, H))
FPS = 60
clock = pygame.time.Clock()

# Загрузка ресурсов
try:
    # Загружаем изображения
    bg = pygame.image.load("image/road.png")
    bg = pygame.transform.scale(bg, (W, H))
    coin_img = pygame.image.load("image/coin.png")
    # Загружаем звуки
    pygame.mixer.music.load("background_music.mp3") # Фоновая музыка
    pygame.mixer.music.play(-1) # Зациклить
    coin_sound = pygame.mixer.Sound("coin_pickup.mp3") # Звук монеты
except:
    print("Файлы ресурсов не найдены. Используются заглушки.")

# Глобальные переменные
COIN_SCORE = 0
SPEED = 5
bg_y = 0 # Для анимации дороги

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try: self.image = pygame.transform.scale(pygame.image.load("image/player_car.png"), (75, 120))
        except: self.image = pygame.Surface((75, 120)); self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(200, 520))
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and self.rect.left > 40: self.rect.move_ip(-5, 0)
        if keys[K_d] and self.rect.right < W - 40: self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try: self.image = pygame.transform.scale(pygame.image.load("image/enemy_car.png"), (75, 120))
        except: self.image = pygame.Surface((75, 120)); self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.randint(60, W-60), -100))
    
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > H:
            self.rect.center = (random.randint(60, W-60), -100)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choices([1, 5], weights=[80, 20])[0]
        size = 30 if self.weight == 1 else 50
        try: self.image = pygame.transform.scale(coin_img, (size, size))
        except: self.image = pygame.Surface((size, size)); self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect(center=(random.randint(60, W-60), -50))

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > H: self.reset()

    def reset(self):
        self.__init__()

P1, E1, C1 = Player(), Enemy(), Coin()
enemies, coins = pygame.sprite.Group(E1), pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); sys.exit()

    # --- АНИМАЦИЯ ДОРОГИ ---
    # Рисуем две картинки дороги друг за другом
    try:
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - H))
        bg_y += 3 # Скорость прокрутки дороги
        if bg_y >= H: bg_y = 0
    except:
        screen.fill((50, 50, 50)) # Если нет картинки дороги

    # Отрисовка и логика
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)
        sprite.move()

    # СБОР МОНЕТ
    if pygame.sprite.spritecollideany(P1, coins):
        for c in coins:
            COIN_SCORE += c.weight
            try: coin_sound.play() # Звук при подборе
            except: pass
            c.reset()
            if COIN_SCORE % 5 == 0: SPEED += 1

    # ГЕЙМОВЕР
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        pygame.quit(); sys.exit()

    # Статистика
    inf = pygame.font.SysFont("Verdana", 20).render(f"Coins: {COIN_SCORE} Spd: {SPEED}", True, (0, 0, 0))
    screen.blit(inf, (15, 15))
    
    pygame.display.flip()
    clock.tick(FPS)