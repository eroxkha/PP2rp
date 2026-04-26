import pygame, sys

# Настройки
W, H = 800, 600
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Состояния
current_color = (0, 0, 0)
brush_size = 5
drawing = False
last_pos = None

# 1. Создаем поверхность для палитры-радуги
palette_width = 250
palette_surf = pygame.Surface((palette_width, 20))
for x in range(palette_width):
    color = pygame.Color(0)
    color.hsva = (int(x / palette_width * 350), 100, 100, 100)
    pygame.draw.line(palette_surf, color, (x, 0), (x, 20))

# 2. Настройки слайдера размера
slider_x = 450  # Начало шкалы по X
slider_y = 30   # Позиция по Y
slider_w = 200  # Длина шкалы

screen.fill((255, 255, 255))

def draw_ui():
    # Панель управления
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, W, 80))
    
    # Палитра
    screen.blit(palette_surf, (20, 25))
    
    # Кнопки Черный / Ластик
    pygame.draw.rect(screen, (0, 0, 0), (280, 25, 30, 30))
    pygame.draw.rect(screen, (255, 255, 255), (320, 25, 30, 30), 2)
    
    # Индикатор цвета
    pygame.draw.rect(screen, current_color, (365, 20, 40, 40))
    pygame.draw.rect(screen, (0, 0, 0), (365, 20, 40, 40), 2)

    # --- ВИЗУАЛЬНАЯ ШКАЛА РАЗМЕРА ---
    # Рисуем треугольную линию (от тонкой к толстой)
    pygame.draw.polygon(screen, (100, 100, 100), [
        (slider_x, slider_y + 10), 
        (slider_x + slider_w, slider_y), 
        (slider_x + slider_w, slider_y + 20)
    ])
    # Ползунок (где сейчас размер)
    current_slider_pos = slider_x + (brush_size * (slider_w / 50))
    pygame.draw.line(screen, (255, 0, 0), (current_slider_pos, slider_y - 5), (current_slider_pos, slider_y + 25), 3)

    font = pygame.font.SysFont("Arial", 12, bold=True)
    screen.blit(font.render("COLOR", True, (0,0,0)), (20, 10))
    screen.blit(font.render(f"SIZE: {brush_size}", True, (0,0,0)), (slider_x, 55))
    screen.blit(font.render("C - Clear", True, (0,0,0)), (700, 30))

while True:
    m_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Клик по палитре
            if 20 <= m_pos[0] <= 20 + palette_width and 25 <= m_pos[1] <= 45:
                current_color = palette_surf.get_at((m_pos[0] - 20, 5))
            
            # Клик по черному / ластику
            elif 280 <= m_pos[0] <= 310 and 25 <= m_pos[1] <= 55: current_color = (0, 0, 0)
            elif 320 <= m_pos[0] <= 350 and 25 <= m_pos[1] <= 55: current_color = (255, 255, 255)
            
            # --- КЛИК ПО ШКАЛЕ РАЗМЕРА ---
            elif slider_x <= m_pos[0] <= slider_x + slider_w and slider_y - 5 <= m_pos[1] <= slider_y + 25:
                # Высчитываем размер пропорционально месту клика (от 1 до 50)
                relative_click = m_pos[0] - slider_x
                brush_size = int((relative_click / slider_w) * 50)
                brush_size = max(1, brush_size) # Минимум 1
            
            # Рисование
            elif m_pos[1] > 80:
                drawing = True
            
            last_pos = m_pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: screen.fill((255, 255, 255), (0, 80, W, H-80))

    # Логика рисования
    if drawing and m_pos[1] > 80:
        if last_pos:
            pygame.draw.line(screen, current_color, last_pos, m_pos, brush_size)
            pygame.draw.circle(screen, current_color, m_pos, brush_size // 2)
        last_pos = m_pos

    draw_ui()
    pygame.display.flip()
    clock.tick(120)