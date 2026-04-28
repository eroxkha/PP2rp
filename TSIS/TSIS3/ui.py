import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (60, 60, 60)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE = (50, 120, 220)
YELLOW = (240, 200, 0)
ORANGE = (255, 140, 0)


def draw_button(surface, text, rect, font, color=DARK_GRAY, hover=False):
    bg = (100, 100, 100) if hover else color
    pygame.draw.rect(surface, bg, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    label = font.render(text, True, WHITE)
    lx = rect[0] + (rect[2] - label.get_width()) // 2
    ly = rect[1] + (rect[3] - label.get_height()) // 2
    surface.blit(label, (lx, ly))


def draw_main_menu(surface, font_big, font, mouse_pos):
    surface.fill((20, 20, 40))
    title = font_big.render("RACER", True, YELLOW)
    surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 80))

    buttons = {
        "Play":        pygame.Rect(250, 200, 200, 50),
        "Leaderboard": pygame.Rect(250, 270, 200, 50),
        "Settings":    pygame.Rect(250, 340, 200, 50),
        "Quit":        pygame.Rect(250, 410, 200, 50),
    }
    for label, rect in buttons.items():
        hover = rect.collidepoint(mouse_pos)
        draw_button(surface, label, rect, font, hover=hover)
    return buttons


def draw_settings_screen(surface, font_big, font, settings, mouse_pos):
    surface.fill((20, 30, 20))
    title = font_big.render("SETTINGS", True, GREEN)
    surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 40))

    # Sound toggle
    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    sound_rect = pygame.Rect(200, 140, 300, 50)
    draw_button(surface, sound_text, sound_rect, font,
                color=(0, 120, 0) if settings["sound"] else (120, 0, 0),
                hover=sound_rect.collidepoint(mouse_pos))

    # Car color buttons
    color_label = font.render("Car Color:", True, WHITE)
    surface.blit(color_label, (200, 215))
    colors = ["red", "blue", "green", "yellow"]
    color_rects = {}
    for i, c in enumerate(colors):
        r = pygame.Rect(200 + i * 80, 245, 70, 40)
        color_rects[c] = r
        border = 4 if settings["car_color"] == c else 2
        pygame.draw.rect(surface, _name_to_rgb(c), r, border_radius=6)
        pygame.draw.rect(surface, WHITE, r, border, border_radius=6)

    # Difficulty buttons
    diff_label = font.render("Difficulty:", True, WHITE)
    surface.blit(diff_label, (200, 315))
    diffs = ["easy", "medium", "hard"]
    diff_rects = {}
    for i, d in enumerate(diffs):
        r = pygame.Rect(200 + i * 110, 345, 100, 40)
        diff_rects[d] = r
        col = (0, 100, 0) if settings["difficulty"] == d else DARK_GRAY
        draw_button(surface, d.capitalize(), r, font, color=col,
                    hover=r.collidepoint(mouse_pos))

    back_rect = pygame.Rect(250, 430, 200, 50)
    draw_button(surface, "Back", back_rect, font, hover=back_rect.collidepoint(mouse_pos))

    return {"sound": sound_rect, "colors": color_rects, "diffs": diff_rects, "back": back_rect}


def draw_game_over(surface, font_big, font, score, distance, coins, mouse_pos):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title = font_big.render("GAME OVER", True, RED)
    surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 80))

    lines = [
        f"Score:    {score}",
        f"Distance: {int(distance)} m",
        f"Coins:    {coins}",
    ]
    for i, line in enumerate(lines):
        txt = font.render(line, True, WHITE)
        surface.blit(txt, (220, 170 + i * 45))

    retry_rect = pygame.Rect(160, 320, 180, 50)
    menu_rect = pygame.Rect(360, 320, 180, 50)
    draw_button(surface, "Retry", retry_rect, font, color=(0, 120, 0),
                hover=retry_rect.collidepoint(mouse_pos))
    draw_button(surface, "Main Menu", menu_rect, font, color=DARK_GRAY,
                hover=menu_rect.collidepoint(mouse_pos))
    return {"retry": retry_rect, "menu": menu_rect}


def draw_leaderboard_screen(surface, font_big, font, entries, mouse_pos):
    surface.fill((20, 20, 50))
    title = font_big.render("LEADERBOARD", True, YELLOW)
    surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 30))

    header = font.render(f"{'#':<4} {'Name':<16} {'Score':<10} {'Dist(m)'}", True, GRAY)
    surface.blit(header, (60, 100))
    pygame.draw.line(surface, GRAY, (60, 125), (640, 125), 1)

    for i, entry in enumerate(entries[:10]):
        color = YELLOW if i == 0 else WHITE
        line = f"{i+1:<4} {entry['name']:<16} {entry['score']:<10} {entry.get('distance', 0)}"
        txt = font.render(line, True, color)
        surface.blit(txt, (60, 135 + i * 32))

    back_rect = pygame.Rect(250, 490, 200, 50)
    draw_button(surface, "Back", back_rect, font, hover=back_rect.collidepoint(mouse_pos))
    return {"back": back_rect}


def draw_hud(surface, font, score, distance, coins, powerup, powerup_timer, total_distance):
    # Left side
    surface.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    surface.blit(font.render(f"Coins: {coins}", True, YELLOW), (10, 35))

    # Distance bar
    traveled = min(distance / total_distance, 1.0)
    bar_w = 200
    pygame.draw.rect(surface, DARK_GRAY, (200, 10, bar_w, 18), border_radius=4)
    pygame.draw.rect(surface, GREEN, (200, 10, int(bar_w * traveled), 18), border_radius=4)
    dist_txt = font.render(f"{int(distance)}/{total_distance}m", True, WHITE)
    surface.blit(dist_txt, (200, 32))

    # Power-up display
    if powerup:
        pu_colors = {"nitro": ORANGE, "shield": BLUE, "repair": GREEN}
        col = pu_colors.get(powerup, WHITE)
        pu_txt = font.render(f"{powerup.upper()} {powerup_timer:.1f}s", True, col)
        surface.blit(pu_txt, (420, 10))


def _name_to_rgb(name):
    return {"red": RED, "blue": BLUE, "green": GREEN, "yellow": YELLOW}.get(name, WHITE)