import pygame
import datetime
import sys
from tools import flood_fill

# Настройки окна
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KBTU Paint Pro")

# Цвета интерфейса
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)

# Холст
canvas = pygame.Surface((950, 750))
canvas.fill(WHITE)

# Состояние
active_color = BLACK
brush_size = 5
tool = 'pencil'
drawing = False
last_pos = None  
start_pos = None 

# Шрифты
font = pygame.font.SysFont("Verdana", 16)
input_text = ""
text_pos = None

# Область палитры
palette_rect = pygame.Rect(20, 50, 160, 150)

def draw_palette():
    for i in range(160):
        for j in range(150):
            c = pygame.Color(0)
            c.hsva = (i * (360/160), 100, 100 - (j * (100/150)), 100)
            screen.set_at((20 + i, 50 + j), c)
    pygame.draw.rect(screen, BLACK, palette_rect, 2)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, 200, HEIGHT))
    
    # Палитра
    screen.blit(font.render("Pick Color:", True, BLACK), (20, 25))
    draw_palette()
    
    # Текущий цвет (превью)
    pygame.draw.rect(screen, active_color, (20, 210, 160, 30))
    pygame.draw.rect(screen, BLACK, (20, 210, 160, 30), 2)

    # Кнопки инструментов
    y_start = 260
    tools = ['pencil', 'line', 'rect', 'circle', 'fill', 'text', 'eraser']
    for i, t in enumerate(tools):
        rect = pygame.Rect(20, y_start + i * 40, 160, 35)
        color = (100, 100, 100) if tool == t else WHITE
        pygame.draw.rect(screen, color, rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=5)
        label = font.render(t.capitalize(), True, WHITE if tool == t else BLACK)
        screen.blit(label, (35, y_start + 7 + i * 40))

    # Кнопки размеров
    y_start = 560
    for i, s in enumerate([2, 5, 10, 20]):
        rect = pygame.Rect(20 + i * 42, y_start, 38, 38)
        color = (100, 100, 100) if brush_size == s else WHITE
        pygame.draw.rect(screen, color, rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=5)
        screen.blit(font.render(str(s), True, WHITE if brush_size == s else BLACK), (20 + i * 42 + 10, y_start + 10))

# Главный цикл
running = True
while running:
    screen.fill((240, 240, 240))
    screen.blit(canvas, (220, 25))
    
    m_pos = pygame.mouse.get_pos()
    adj_x, adj_y = m_pos[0] - 220, m_pos[1] - 25

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if palette_rect.collidepoint(m_pos):
                rel_x, rel_y = m_pos[0] - 20, m_pos[1] - 50
                temp_c = pygame.Color(0)
                temp_c.hsva = (rel_x * (360/160), 100, 100 - (rel_y * (100/150)), 100)
                active_color = temp_c
            
            elif m_pos[0] < 200:
                # Инструменты
                for i, t in enumerate(['pencil', 'line', 'rect', 'circle', 'fill', 'text', 'eraser']):
                    if pygame.Rect(20, 260 + i * 40, 160, 35).collidepoint(m_pos):
                        tool = t
                # Размеры
                for i, s in enumerate([2, 5, 10, 20]):
                    if pygame.Rect(20 + i * 42, 560, 38, 38).collidepoint(m_pos):
                        brush_size = s
            
            elif 0 <= adj_x < 950 and 0 <= adj_y < 750:
                if tool == 'fill':
                    flood_fill(canvas, adj_x, adj_y, active_color)
                elif tool == 'text':
                    text_pos = (adj_x, adj_y)
                    input_text = ""
                else:
                    drawing = True
                    start_pos = (adj_x, adj_y)
                    last_pos = (adj_x, adj_y)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool == 'line':
                    pygame.draw.line(canvas, active_color, start_pos, (adj_x, adj_y), brush_size)
                elif tool == 'rect':
                    r = pygame.Rect(min(start_pos[0], adj_x), min(start_pos[1], adj_y), 
                                    abs(adj_x - start_pos[0]), abs(adj_y - start_pos[1]))
                    pygame.draw.rect(canvas, active_color, r, brush_size)
                elif tool == 'circle':
                    r_val = int(((start_pos[0]-adj_x)**2 + (start_pos[1]-adj_y)**2)**0.5)
                    pygame.draw.circle(canvas, active_color, start_pos, r_val, brush_size)
                drawing = False
                last_pos = None

        if event.type == pygame.MOUSEMOTION:
            if drawing and 0 <= adj_x < 950 and 0 <= adj_y < 750:
                if tool == 'pencil':
                    pygame.draw.line(canvas, active_color, last_pos, (adj_x, adj_y), brush_size)
                    pygame.draw.circle(canvas, active_color, (adj_x, adj_y), brush_size // 2)
                    last_pos = (adj_x, adj_y)
                elif tool == 'eraser':
                    pygame.draw.line(canvas, WHITE, last_pos, (adj_x, adj_y), brush_size * 2)
                    pygame.draw.circle(canvas, WHITE, (adj_x, adj_y), brush_size)
                    last_pos = (adj_x, adj_y)

        if event.type == pygame.KEYDOWN and tool == 'text' and text_pos:
            if event.key == pygame.K_RETURN:
                canvas.blit(font.render(input_text, True, active_color), text_pos)
                text_pos = None
            elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE: text_pos = None
            else: input_text += event.unicode

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            fname = f"drawing_{datetime.datetime.now().strftime('%H%M%S')}.png"
            pygame.image.save(canvas, fname)
            print(f"Saved: {fname}")
    if drawing and tool in ['line', 'rect', 'circle']:
        canvas_origin = (220, 25)
        s_p = (start_pos[0] + 220, start_pos[1] + 25)
        if tool == 'line':
            pygame.draw.line(screen, active_color, s_p, m_pos, brush_size)
        elif tool == 'rect':
            r_p = pygame.Rect(min(s_p[0], m_pos[0]), min(s_p[1], m_pos[1]), 
                              abs(m_pos[0] - s_p[0]), abs(m_pos[1] - s_p[1]))
            pygame.draw.rect(screen, active_color, r_p, brush_size)
        elif tool == 'circle':
            r_val = int(((s_p[0]-m_pos[0])**2 + (s_p[1]-m_pos[1])**2)**0.5)
            pygame.draw.circle(screen, active_color, s_p, r_val, brush_size)

    if tool == 'text' and text_pos:
        screen.blit(font.render(input_text + "|", True, active_color), (text_pos[0]+220, text_pos[1]+25))

    draw_ui()
    pygame.display.flip()

pygame.quit()