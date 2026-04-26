import pygame, sys, random
from pygame.locals import *

# 1. Инициализация и настройки
pygame.init()
W, H = 300, 600  # Ширина совпадает с размером окна
FPS = 60
COIN_SCORE = 0

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer Practice 10")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 20)

# Попытка загрузить звук, если файла нет - игра не вылетит
try:
    honk_sound = pygame.mixer.Sound("honk.mp3")
except:
    honk_sound = None

# 2. Классы объектов
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            img = pygame.image.load("image/player_car.png")
            self.image = pygame.transform.scale(img, (75, 150))
        except:
            self.image = pygame.Surface((75, 150))
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(150, 525))
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and self.rect.left > 0: self.rect.move_ip(-5, 0)
        if keys[K_d] and self.rect.right < W: self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            img = pygame.image.load("image/enemy_car.png")
            self.image = pygame.transform.scale(img, (75, 150))
        except:
            self.image = pygame.Surface((75, 150))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.randint(40, W-40), -100))
        self.speed = 5
        self.score = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > H:
            self.score += 10
            self.rect.center = (random.randint(40, W-40), -100)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            img = pygame.image.load("image/coin.png")
            self.image = pygame.transform.scale(img, (40, 40))
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 215, 0)) # Желтый квадрат, если нет картинки
        self.rect = self.image.get_rect(center=(random.randint(40, W-40), -50))

    def move(self):
        self.rect.move_ip(0, 5) # Скорость монетки
        if self.rect.top > H:
            self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, W-40), -50)

# 3. Фон (упрощенная прокрутка)
try:
    bg_img = pygame.image.load("image/proad.png")
    bg_img = pygame.transform.scale(bg_img, (W, H))
except:
    bg_img = pygame.Surface((W, H))
    bg_img.fill((100, 100, 100))
bg_y = 0

# 4. Создание объектов и групп
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# 5. Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # --- ЛОГИКА ДВИЖЕНИЯ ---
    bg_y += 2
    if bg_y >= H: bg_y = 0
    
    for entity in all_sprites:
        entity.move()

    # --- ПРОВЕРКА СТОЛКНОВЕНИЙ ---
    # Сбор монет
    if pygame.sprite.spritecollide(P1, coins, False):
        COIN_SCORE += 1
        C1.reset() # Монетка исчезает и появляется сверху

    # Авария
    if pygame.sprite.spritecollideany(P1, enemies):
        if honk_sound: honk_sound.play()
        screen.fill((200, 0, 0))
        final_txt = font_small.render(f"Game Over! Coins: {COIN_SCORE}", True, (255,255,255))
        screen.blit(final_txt, (30, H//2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # --- ОТРИСОВКА (Важен порядок слоев!) ---
    # 1. Фон
    screen.blit(bg_img, (0, bg_y))
    screen.blit(bg_img, (0, bg_y - H))
    
    # 2. Все объекты (Машины и Монетки)
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # 3. Текст счета (поверх всего)
    txt_coins = font_small.render(f"Coins: {COIN_SCORE}", True, (0, 0, 0))
    txt_score = font_small.render(f"Score: {E1.score}", True, (0, 0, 0))
    screen.blit(txt_coins, (10, 10))
    screen.blit(txt_score, (W - 110, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()