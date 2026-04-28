import pygame
import sys
from game import Game, load_settings, save_settings
from db import init_db, get_or_create_player, save_session, get_top10, get_personal_best
from config import *


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 22)


def draw_button(surface, text, rect, color=DARK_GRAY, hover=False):
    col = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)) if hover else color
    pygame.draw.rect(surface, col, rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=6)
    txt = font.render(text, True, WHITE)
    tx = rect[0] + (rect[2] - txt.get_width()) // 2
    ty = rect[1] + (rect[3] - txt.get_height()) // 2
    surface.blit(txt, (tx, ty))


def is_hover(rect):
    mx, my = pygame.mouse.get_pos()
    return pygame.Rect(rect).collidepoint(mx, my)


def main_menu():
    username = ""
    input_active = True

    btn_play = (200, 280, 200, 40)
    btn_lb = (200, 340, 200, 40)
    btn_settings = (200, 400, 200, 40)
    btn_quit = (200, 460, 200, 40)

    while True:
        screen.fill(BLACK)

        title = big_font.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # username input
        name_label = font.render("Username:", True, WHITE)
        screen.blit(name_label, (170, 190))
        input_rect = pygame.Rect(170, 215, 260, 36)
        pygame.draw.rect(screen, DARK_GRAY, input_rect)
        pygame.draw.rect(screen, GREEN if input_active else GRAY, input_rect, 2)
        uname_txt = font.render(username + ("|" if input_active else ""), True, WHITE)
        screen.blit(uname_txt, (input_rect.x + 5, input_rect.y + 7))

        draw_button(screen, "Play", btn_play, hover=is_hover(btn_play))
        draw_button(screen, "Leaderboard", btn_lb, hover=is_hover(btn_lb))
        draw_button(screen, "Settings", btn_settings, hover=is_hover(btn_settings))
        draw_button(screen, "Quit", btn_quit, hover=is_hover(btn_quit))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(btn_play).collidepoint(event.pos):
                    if username.strip():
                        return 'play', username.strip()
                elif pygame.Rect(btn_lb).collidepoint(event.pos):
                    return 'leaderboard', username.strip()
                elif pygame.Rect(btn_settings).collidepoint(event.pos):
                    return 'settings', username.strip()
                elif pygame.Rect(btn_quit).collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if username.strip():
                            return 'play', username.strip()
                    elif len(username) < 20:
                        username += event.unicode

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    rows = get_top10()
    btn_back = (220, 540, 160, 40)

    while True:
        screen.fill(BLACK)
        title = big_font.render("LEADERBOARD", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        headers = ["#", "Name", "Score", "Level", "Date"]
        col_x = [20, 60, 200, 280, 360]

        for i, h in enumerate(headers):
            htxt = small_font.render(h, True, GRAY)
            screen.blit(htxt, (col_x[i], 75))
        pygame.draw.line(screen, GRAY, (10, 95), (590, 95))

        for idx, row in enumerate(rows):
            uname, score, level, played_at = row
            date_str = played_at.strftime("%m/%d %H:%M") if played_at else "-"
            vals = [str(idx + 1), uname[:12], str(score), str(level), date_str]
            color = YELLOW if idx == 0 else WHITE
            for i, v in enumerate(vals):
                vtxt = small_font.render(v, True, color)
                screen.blit(vtxt, (col_x[i], 105 + idx * 28))

        draw_button(screen, "Back", btn_back, hover=is_hover(btn_back))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(btn_back).collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    settings = load_settings()

    btn_grid = (200, 200, 200, 40)
    btn_sound = (200, 260, 200, 40)
    btn_color_r = (200, 320, 60, 40)
    btn_color_g = (280, 320, 60, 40)
    btn_color_b = (360, 320, 60, 40)
    btn_save = (200, 420, 200, 40)

    color_options = [
        (0, 200, 0), (0, 0, 200), (255, 165, 0),
        (200, 0, 200), (0, 200, 200), (255, 255, 255)
    ]
    current_color_idx = 0
    # find closest
    for i, c in enumerate(color_options):
        if list(c) == settings['snake_color']:
            current_color_idx = i
            break

    while True:
        screen.fill(BLACK)
        title = big_font.render("SETTINGS", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        # grid
        grid_status = "ON" if settings['grid'] else "OFF"
        draw_button(screen, f"Grid: {grid_status}", btn_grid, hover=is_hover(btn_grid))

        # sound
        sound_status = "ON" if settings['sound'] else "OFF"
        draw_button(screen, f"Sound: {sound_status}", btn_sound, hover=is_hover(btn_sound))

        # snake color
        color_label = font.render("Snake Color:", True, WHITE)
        screen.blit(color_label, (170, 300))
        for i, c in enumerate(color_options):
            cx = 200 + i * 40
            rect = (cx, 320, 32, 32)
            pygame.draw.rect(screen, c, rect)
            if i == current_color_idx:
                pygame.draw.rect(screen, WHITE, rect, 3)

        draw_button(screen, "Save & Back", btn_save, hover=is_hover(btn_save))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(btn_grid).collidepoint(event.pos):
                    settings['grid'] = not settings['grid']
                elif pygame.Rect(btn_sound).collidepoint(event.pos):
                    settings['sound'] = not settings['sound']
                elif pygame.Rect(btn_save).collidepoint(event.pos):
                    settings['snake_color'] = list(color_options[current_color_idx])
                    save_settings(settings)
                    return
                else:
                    for i, c in enumerate(color_options):
                        cx = 200 + i * 40
                        rect = pygame.Rect(cx, 320, 32, 32)
                        if rect.collidepoint(event.pos):
                            current_color_idx = i

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(score, level, personal_best):
    btn_retry = (150, 380, 140, 40)
    btn_menu = (320, 380, 140, 40)

    while True:
        screen.fill(BLACK)

        title = big_font.render("GAME OVER", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        score_txt = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, 210))

        lvl_txt = font.render(f"Level reached: {level}", True, WHITE)
        screen.blit(lvl_txt, (SCREEN_WIDTH // 2 - lvl_txt.get_width() // 2, 250))

        best_txt = font.render(f"Personal best: {personal_best}", True, YELLOW)
        screen.blit(best_txt, (SCREEN_WIDTH // 2 - best_txt.get_width() // 2, 290))

        if score > personal_best:
            new_txt = font.render("NEW BEST!", True, GREEN)
            screen.blit(new_txt, (SCREEN_WIDTH // 2 - new_txt.get_width() // 2, 330))

        draw_button(screen, "Retry", btn_retry, hover=is_hover(btn_retry))
        draw_button(screen, "Main Menu", btn_menu, hover=is_hover(btn_menu))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(btn_retry).collidepoint(event.pos):
                    return 'retry'
                elif pygame.Rect(btn_menu).collidepoint(event.pos):
                    return 'menu'

        pygame.display.flip()
        clock.tick(60)


def run_game(username, player_id, personal_best):
    game = Game(username, player_id, personal_best)
    move_timer = 0

    while True:
        dt = clock.tick(60)
        move_timer += dt

        speed = game.get_current_speed()
        move_interval = 1000 // speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return game.score, game.level
                game.handle_input(event)

        if move_timer >= move_interval:
            move_timer = 0
            result = game.update()
            if result == 'game_over':
                return game.score, game.level

        game.draw(screen)
        pygame.display.flip()


def main():
    init_db()

    username = ""
    player_id = None

    while True:
        action, uname = main_menu()

        if action == 'leaderboard':
            leaderboard_screen()
            continue

        if action == 'settings':
            settings_screen()
            continue

        if action == 'play':
            username = uname
            player_id = get_or_create_player(username)
            if not player_id:
                player_id = None

        while True:
            personal_best = get_personal_best(player_id) if player_id else 0
            score, level = run_game(username, player_id, personal_best)

            if player_id:
                save_session(player_id, score, level)
                new_best = get_personal_best(player_id)
            else:
                new_best = max(personal_best, score)

            choice = game_over_screen(score, level, new_best)
            if choice == 'menu':
                break
            # else retry


if __name__ == '__main__':
    main()