import pygame
import random
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE = (50, 120, 220)
YELLOW = (240, 200, 0)
ORANGE = (255, 140, 0)
ROAD_COLOR = (50, 50, 50)
LANE_LINE = (200, 200, 200)

SCREEN_W = 700
SCREEN_H = 600
ROAD_LEFT = 150
ROAD_RIGHT = 550
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
NUM_LANES = 3
LANE_WIDTH = ROAD_WIDTH // NUM_LANES

CAR_W = 40
CAR_H = 70

COIN_COLORS = {1: YELLOW, 3: ORANGE, 5: (200, 50, 200)}
POWERUP_COLORS = {"nitro": ORANGE, "shield": BLUE, "repair": GREEN}
POWERUP_SYMBOLS = {"nitro": "N", "shield": "S", "repair": "R"}

DIFFICULTY_SETTINGS = {
    "easy":   {"base_speed": 4, "traffic_interval": 120, "obstacle_interval": 180},
    "medium": {"base_speed": 6, "traffic_interval": 80,  "obstacle_interval": 120},
    "hard":   {"base_speed": 9, "traffic_interval": 50,  "obstacle_interval": 80},
}

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  120, 220),
    "green":  (50,  200, 80),
    "yellow": (240, 200, 0),
}


def lane_x(lane):
    """Return center x of a lane (0-indexed)."""
    return ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2


class PlayerCar:
    def __init__(self, color_name="red"):
        self.lane = 1
        self.x = lane_x(1)
        self.y = SCREEN_H - 120
        self.color = CAR_COLORS.get(color_name, RED)
        self.target_x = self.x
        self.speed_bonus = 0  # nitro extra speed

    def move(self, direction):
        new_lane = self.lane + direction
        if 0 <= new_lane < NUM_LANES:
            self.lane = new_lane
            self.target_x = lane_x(self.lane)

    def update(self):
        # Smooth slide
        if abs(self.x - self.target_x) > 2:
            self.x += (self.target_x - self.x) * 0.2
        else:
            self.x = self.target_x

    def get_rect(self):
        return pygame.Rect(self.x - CAR_W // 2, self.y - CAR_H // 2, CAR_W, CAR_H)

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        # Windshield
        pygame.draw.rect(surface, (150, 220, 255),
                         (r.x + 6, r.y + 8, r.w - 12, 18), border_radius=3)
        # Wheels
        for wx, wy in [(r.x - 4, r.y + 8), (r.x + r.w - 8, r.y + 8),
                       (r.x - 4, r.y + r.h - 22), (r.x + r.w - 8, r.y + r.h - 22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 12, 14), border_radius=3)


class TrafficCar:
    COLORS = [(180, 60, 60), (60, 60, 180), (60, 160, 60),
              (180, 120, 60), (120, 60, 180)]

    def __init__(self, lane, speed):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = -CAR_H
        self.speed = speed
        self.color = random.choice(self.COLORS)

    def update(self, scroll_speed):
        self.y += scroll_speed + self.speed

    def get_rect(self):
        return pygame.Rect(self.x - CAR_W // 2, self.y - CAR_H // 2, CAR_W, CAR_H)

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        pygame.draw.rect(surface, (150, 220, 255),
                         (r.x + 6, r.y + r.h - 26, r.w - 12, 18), border_radius=3)
        for wx, wy in [(r.x - 4, r.y + 8), (r.x + r.w - 8, r.y + 8),
                       (r.x - 4, r.y + r.h - 22), (r.x + r.w - 8, r.y + r.h - 22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 12, 14), border_radius=3)

    def off_screen(self):
        return self.y > SCREEN_H + CAR_H


class Obstacle:
    TYPES = [
        {"name": "oil",     "color": (40, 40, 80),   "w": 50, "h": 30},
        {"name": "barrier", "color": (220, 80, 0),   "w": 40, "h": 20},
        {"name": "pothole", "color": (0, 0, 0),   "w": 35, "h": 25},
    ]

    def __init__(self, lane):
        t = random.choice(self.TYPES)
        self.name = t["name"]
        self.color = t["color"]
        self.w = t["w"]
        self.h = t["h"]
        self.x = lane_x(lane)
        self.y = -40

    def update(self, scroll_speed):
        self.y += scroll_speed

    def get_rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)

    def draw(self, surface):
        r = self.get_rect()
        if self.name == "oil":
            pygame.draw.ellipse(surface, self.color, r)
            # Sheen
            pygame.draw.ellipse(surface, (60, 60, 120),
                                (r.x + 5, r.y + 5, r.w - 10, r.h - 10))
        elif self.name == "pothole":
            pygame.draw.ellipse(surface, self.color, r)
        else:
            pygame.draw.rect(surface, self.color, r, border_radius=4)
            pygame.draw.rect(surface, (255, 200, 0), r, 2, border_radius=4)

    def off_screen(self):
        return self.y > SCREEN_H + 50


class Coin:
    def __init__(self, lane):
        weights = [60, 30, 10]
        values = [1, 3, 5]
        self.value = random.choices(values, weights=weights)[0]
        self.x = lane_x(lane)
        self.y = -20
        self.radius = 20

    def update(self, scroll_speed):
        self.y += scroll_speed

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, surface, font_small):
        color = COIN_COLORS.get(self.value, YELLOW)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        txt = font_small.render(str(self.value), True, BLACK)
        surface.blit(txt, (int(self.x) - txt.get_width() // 2,
                           int(self.y) - txt.get_height() // 2))

    def off_screen(self):
        return self.y > SCREEN_H + 30


class PowerUp:
    def __init__(self, lane):
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.x = lane_x(lane)
        self.y = -25
        self.radius = 16
        self.lifetime = 8.0  # seconds before disappearing

    def update(self, scroll_speed, dt):
        self.y += scroll_speed
        self.lifetime -= dt

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, surface, font_small):
        col = POWERUP_COLORS[self.kind]
        pygame.draw.circle(surface, col, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        sym = font_small.render(POWERUP_SYMBOLS[self.kind], True, WHITE)
        surface.blit(sym, (int(self.x) - sym.get_width() // 2,
                           int(self.y) - sym.get_height() // 2))

    def expired(self):
        return self.lifetime <= 0 or self.y > SCREEN_H + 30


class NitroStrip:
    """A speed boost strip on the road — road event."""
    def __init__(self, lane):
        self.x = lane_x(lane)
        self.y = -30
        self.w = LANE_WIDTH - 10
        self.h = 20

    def update(self, scroll_speed):
        self.y += scroll_speed

    def get_rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y, self.w, self.h)

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, ORANGE, r, border_radius=3)
        for i in range(3):
            cx = r.x + 10 + i * (r.w // 3)
            pygame.draw.polygon(surface, YELLOW, [
                (cx, r.y + 3), (cx + 8, r.y + r.h // 2), (cx, r.y + r.h - 3)
            ])

    def off_screen(self):
        return self.y > SCREEN_H + 40


class RoadScroller:
    def __init__(self):
        self.offset = 0
        self.lane_dash_h = 40
        self.lane_dash_gap = 30

    def update(self, speed):
        self.offset = (self.offset + speed) % (self.lane_dash_h + self.lane_dash_gap)

    def draw(self, surface):
        # Road background
        pygame.draw.rect(surface, ROAD_COLOR,
                         (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_H))
        # Side curbs
        pygame.draw.rect(surface, (200, 200, 200), (ROAD_LEFT - 8, 0, 8, SCREEN_H))
        pygame.draw.rect(surface, (200, 200, 200), (ROAD_RIGHT, 0, 8, SCREEN_H))

        # Lane dashes
        for lane in range(1, NUM_LANES):
            lx = ROAD_LEFT + lane * LANE_WIDTH
            y = -self.lane_dash_h + self.offset
            while y < SCREEN_H:
                pygame.draw.rect(surface, LANE_LINE, (lx - 2, y, 4, self.lane_dash_h))
                y += self.lane_dash_h + self.lane_dash_gap


class GameSession:
    TOTAL_DISTANCE = 3000  # meters to finish

    def __init__(self, settings):
        self.settings = settings
        diff = settings.get("difficulty", "medium")
        ds = DIFFICULTY_SETTINGS[diff]
        self.base_speed = ds["base_speed"]
        self.traffic_interval = ds["traffic_interval"]
        self.obstacle_interval = ds["obstacle_interval"]

        self.player = PlayerCar(settings.get("car_color", "red"))
        self.road = RoadScroller()

        self.scroll_speed = self.base_speed
        self.distance = 0.0
        self.score = 0
        self.coins_collected = 0

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.nitro_strips = []

        self.active_powerup = None
        self.powerup_timer = 0.0
        self.shielded = False

        self.frame = 0
        self.alive = True
        self.finished = False

        # Timers
        self.traffic_timer = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.powerup_spawn_timer = 0
        self.nitro_strip_timer = 0

    def _safe_lane(self, exclude_lane=None):
        lanes = list(range(NUM_LANES))
        if exclude_lane is not None:
            lanes = [l for l in lanes if l != exclude_lane]
        return random.choice(lanes) if lanes else random.randint(0, NUM_LANES - 1)

    def _spawn_traffic(self):
        lane = random.randint(0, NUM_LANES - 1)
        # Don't spawn right on top of player if same lane and car near top
        if lane == self.player.lane:
            lane = (lane + 1) % NUM_LANES
        speed_bonus = min(self.frame // 500, 4)
        car = TrafficCar(lane, random.uniform(0.5, 1.5 + speed_bonus * 0.3))
        self.traffic.append(car)

    def _spawn_obstacle(self):
        lane = random.randint(0, NUM_LANES - 1)
        self.obstacles.append(Obstacle(lane))

    def _spawn_coin(self):
        lane = random.randint(0, NUM_LANES - 1)
        self.coins.append(Coin(lane))

    def _spawn_powerup(self):
        lane = random.randint(0, NUM_LANES - 1)
        self.powerups.append(PowerUp(lane))

    def _spawn_nitro_strip(self):
        lane = random.randint(0, NUM_LANES - 1)
        self.nitro_strips.append(NitroStrip(lane))

    def activate_powerup(self, kind):
        self.active_powerup = kind
        if kind == "nitro":
            self.powerup_timer = 4.0
        elif kind == "shield":
            self.powerup_timer = -1  # until hit
            self.shielded = True
        elif kind == "repair":
            self.powerup_timer = 0  # instant
            # Repair clears one random obstacle if any
            if self.obstacles:
                self.obstacles.pop(0)
            self.active_powerup = None

    def update(self, keys, dt):
        if not self.alive or self.finished:
            return

        self.frame += 1

        # Difficulty scaling — speed up over time
        self.scroll_speed = self.base_speed + min(self.frame // 300, 6)

        # Nitro speed bonus
        nitro_extra = 4 if self.active_powerup == "nitro" else 0
        effective_speed = self.scroll_speed + nitro_extra

        self.road.update(effective_speed)
        self.player.update()

        # Distance (1 unit = roughly 1 meter)
        self.distance += effective_speed * 0.05
        if self.distance >= self.TOTAL_DISTANCE:
            self.finished = True
            self.score += 500  # finish bonus
            return

        # Spawn timers — get faster with difficulty scaling
        density_factor = max(0.5, 1.0 - self.frame / 3000)
        self.traffic_timer += 1
        if self.traffic_timer >= self.traffic_interval * density_factor:
            self._spawn_traffic()
            self.traffic_timer = 0

        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_interval * density_factor:
            self._spawn_obstacle()
            self.obstacle_timer = 0

        self.coin_timer += 1
        if self.coin_timer >= 60:
            self._spawn_coin()
            self.coin_timer = 0

        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= 300:
            if not self.powerups:  # only one on screen at a time
                self._spawn_powerup()
            self.powerup_spawn_timer = 0

        self.nitro_strip_timer += 1
        if self.nitro_strip_timer >= 400:
            self._spawn_nitro_strip()
            self.nitro_strip_timer = 0

        # Update all objects
        player_rect = self.player.get_rect()

        for tc in self.traffic[:]:
            tc.update(effective_speed)
            if tc.off_screen():
                self.traffic.remove(tc)
                self.score += 5  # survived a car
            elif tc.get_rect().colliderect(player_rect):
                if self.shielded:
                    self.shielded = False
                    self.active_powerup = None
                    self.traffic.remove(tc)
                else:
                    self.alive = False
                    return

        for obs in self.obstacles[:]:
            obs.update(effective_speed)
            if obs.off_screen():
                self.obstacles.remove(obs)
            elif obs.get_rect().colliderect(player_rect):
                if self.shielded:
                    self.shielded = False
                    self.active_powerup = None
                    self.obstacles.remove(obs)
                else:
                    self.alive = False
                    return

        for coin in self.coins[:]:
            coin.update(effective_speed)
            if coin.off_screen():
                self.coins.remove(coin)
            elif coin.get_rect().colliderect(player_rect):
                self.coins_collected += coin.value
                self.score += coin.value * 10
                self.coins.remove(coin)

        for pu in self.powerups[:]:
            pu.update(effective_speed, dt)
            if pu.expired():
                self.powerups.remove(pu)
            elif pu.get_rect().colliderect(player_rect):
                self.activate_powerup(pu.kind)
                self.powerups.remove(pu)

        for ns in self.nitro_strips[:]:
            ns.update(effective_speed)
            if ns.off_screen():
                self.nitro_strips.remove(ns)
            elif ns.get_rect().colliderect(player_rect):
                # Temporary mini-boost if no nitro already
                if self.active_powerup != "nitro":
                    self.activate_powerup("nitro")
                self.nitro_strips.remove(ns)

        # Power-up countdown
        if self.active_powerup == "nitro":
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                self.active_powerup = None

        # Score from distance
        self.score = (self.coins_collected * 10) + int(self.distance)

    def draw(self, surface, font_small):
        self.road.draw(surface)

        for ns in self.nitro_strips:
            ns.draw(surface)
        for obs in self.obstacles:
            obs.draw(surface)
        for tc in self.traffic:
            tc.draw(surface)
        for coin in self.coins:
            coin.draw(surface, font_small)
        for pu in self.powerups:
            pu.draw(surface, font_small)

        self.player.draw(surface)

        # Shield visual
        if self.shielded:
            pr = self.player.get_rect()
            pygame.draw.ellipse(surface, (*BLUE, 0), pr.inflate(14, 14), 3)
            pygame.draw.ellipse(surface, BLUE, pr.inflate(14, 14), 3)