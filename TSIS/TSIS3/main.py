import pygame
import sys

from racer import GameSession, SCREEN_W, SCREEN_H
from ui import (draw_main_menu, draw_settings_screen, draw_game_over,
                draw_leaderboard_screen, draw_hud)
from persistence import (load_leaderboard, add_to_leaderboard,
                         load_settings, save_settings)

FPS = 60

# States
STATE_MENU = "menu"
STATE_USERNAME = "username"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "gameover"
STATE_LEADERBOARD = "leaderboard"
STATE_SETTINGS = "settings"

# Инициализация звукового движка
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3") 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("RACER")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 52, bold=True)
    font = pygame.font.SysFont("Arial", 26)
    font_small = pygame.font.SysFont("Arial", 16)
    font_input = pygame.font.SysFont("Arial", 30)

    settings = load_settings()
    leaderboard = load_leaderboard()

    state = STATE_MENU
    game = None
    username = ""
    username_input = ""

    # Key repeat for smooth car movement
    key_cooldown = 0
    KEY_DELAY = 12  # frames between lane changes

    while True:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---- MAIN MENU ----
            if state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_main_menu(screen, font_big, font, mouse_pos)
                    if btns["Play"].collidepoint(mouse_pos):
                        state = STATE_USERNAME
                        username_input = ""
                    elif btns["Leaderboard"].collidepoint(mouse_pos):
                        leaderboard = load_leaderboard()
                        state = STATE_LEADERBOARD
                    elif btns["Settings"].collidepoint(mouse_pos):
                        state = STATE_SETTINGS
                    elif btns["Quit"].collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            # ---- USERNAME ENTRY ----
            elif state == STATE_USERNAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username_input.strip():
                        username = username_input.strip()
                        game = GameSession(settings)
                        state = STATE_PLAYING
                    elif event.key == pygame.K_BACKSPACE:
                        username_input = username_input[:-1]
                    else:
                        if len(username_input) < 16 and event.unicode.isprintable():
                            username_input += event.unicode

            # ---- PLAYING ----
            elif state == STATE_PLAYING:
                pass  # Input handled below with key polling

            # ---- GAME OVER ----
            elif state == STATE_GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_game_over(screen, font_big, font,
                                         game.score, game.distance,
                                         game.coins_collected, mouse_pos)
                    if btns["retry"].collidepoint(mouse_pos):
                        game = GameSession(settings)
                        state = STATE_PLAYING
                    elif btns["menu"].collidepoint(mouse_pos):
                        state = STATE_MENU

            # ---- LEADERBOARD ----
            elif state == STATE_LEADERBOARD:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_leaderboard_screen(screen, font_big, font,
                                                   leaderboard, mouse_pos)
                    if btns["back"].collidepoint(mouse_pos):
                        state = STATE_MENU

            # ---- SETTINGS ----
            elif state == STATE_SETTINGS:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_settings_screen(screen, font_big, font,
                                                settings, mouse_pos)
                    if btns["sound"].collidepoint(mouse_pos):
                        settings["sound"] = not settings["sound"]
                        save_settings(settings)
                    for cname, crect in btns["colors"].items():
                        if crect.collidepoint(mouse_pos):
                            settings["car_color"] = cname
                            save_settings(settings)
                    for dname, drect in btns["diffs"].items():
                        if drect.collidepoint(mouse_pos):
                            settings["difficulty"] = dname
                            save_settings(settings)
                    if btns["back"].collidepoint(mouse_pos):
                        state = STATE_MENU

        # ---- GAME UPDATE (key polling) ----
        if state == STATE_PLAYING and game:
            keys = pygame.key.get_pressed()

            key_cooldown = max(0, key_cooldown - 1)
            if key_cooldown == 0:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    game.player.move(-1)
                    key_cooldown = KEY_DELAY
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    game.player.move(1)
                    key_cooldown = KEY_DELAY

            game.update(keys, dt)

            if not game.alive:
                leaderboard = add_to_leaderboard(username, game.score, game.distance)
                state = STATE_GAME_OVER
            elif game.finished:
                leaderboard = add_to_leaderboard(username, game.score, game.distance)
                state = STATE_GAME_OVER

        # ---- DRAWING ----
        screen.fill((30, 30, 30))

        if state == STATE_MENU:
            draw_main_menu(screen, font_big, font, mouse_pos)

        elif state == STATE_USERNAME:
            screen.fill((20, 20, 40))
            title = font_big.render("Enter Your Name", True, (240, 200, 0))
            screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 160))

            box = pygame.Rect(200, 270, 300, 50)
            pygame.draw.rect(screen, (60, 60, 80), box, border_radius=6)
            pygame.draw.rect(screen, (200, 200, 200), box, 2, border_radius=6)
            name_surf = font_input.render(username_input + "|", True, (255, 255, 255))
            screen.blit(name_surf, (box.x + 10, box.y + 10))

            hint = font_small.render("Press ENTER to start", True, (160, 160, 160))
            screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 340))

        elif state == STATE_PLAYING and game:
            game.draw(screen, font_small)
            draw_hud(screen, font_small, game.score, game.distance,
                     game.coins_collected, game.active_powerup,
                     game.powerup_timer if game.active_powerup == "nitro" else 0,
                     GameSession.TOTAL_DISTANCE)

        elif state == STATE_GAME_OVER and game:
            game.draw(screen, font_small)
            draw_game_over(screen, font_big, font, game.score,
                           game.distance, game.coins_collected, mouse_pos)

        elif state == STATE_LEADERBOARD:
            draw_leaderboard_screen(screen, font_big, font, leaderboard, mouse_pos)

        elif state == STATE_SETTINGS:
            draw_settings_screen(screen, font_big, font, settings, mouse_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()