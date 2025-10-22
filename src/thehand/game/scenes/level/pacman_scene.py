import random

import pygame as pg
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult

import thehand as th


class Collectible(pg.sprite.Sprite):
    def __init__(self, image_path, pos, points, size=(50, 50)):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=pos)
        self.points = points


class Apple(Collectible):
    def __init__(self, pos):
        size_points = random.choices([(50, 1), (80, 10), (120, 50), (150, 200), (300, 1000)], [50, 20, 10, 5, 1])
        size = size_points[0][0]
        points = size_points[0][1]
        super().__init__(th.asset_path("imgs", "apple.png"), pos, points, (size, size))


class Strawberry(Collectible):
    def __init__(self, pos):
        size_points = random.choices(
            [(50, 5), (80, 50), (120, 100), (150, 500), (300, 2000)],
            [50, 20, 10, 5, 1],
        )
        size = size_points[0][0]
        points = size_points[0][1] * 2
        super().__init__(th.asset_path("imgs", "strawberry.png"), pos, points, (size, size))


class Ghost(pg.sprite.Sprite):
    def __init__(self, store: th.Store, pos, speed=2, size=(70, 70)):
        super().__init__()

        self.store = store

        ghost_images = ["ghost_blinky", "ghost_blue", "ghost_clyde", "ghost_inky", "ghost_pinky"]

        self.image = self.store.imgs[random.choice(ghost_images)].convert_alpha()
        self.image = pg.transform.scale(self.image, size)

        self.rect = self.image.get_rect(center=pos)

        self.speed = speed
        self.direction = random.choice(["horizontal", "vertical"])
        self.points_loss = 500

    def update(self):
        if self.direction == "horizontal":
            self.rect.x += self.speed
            if self.rect.left < 0 or self.rect.right > self.store.screen.get_width():
                self.speed *= -1
        else:
            self.rect.y += self.speed
            if self.rect.top < 0 or self.rect.bottom > self.store.screen.get_height():
                self.speed *= -1


class Toast(th.Entity):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        pos: tuple[int, int],
        size: tuple[int, int],
        text: str,
        duration: int = 3000,
        font: pg.font.Font | None = None,
        color: tuple[int, int, int] = th.COLOR_MOCHA_TEXT,
        bg_color: tuple[int, int, int] = th.COLOR_MOCHA_BASE,
        bg_opacity: float = 0.8,
    ) -> None:
        super().__init__(state, store)

        self.pos = pos
        self.size = size
        self.text = text
        self.duration = duration
        self.font = self.store.font_text_24 if font is None else font
        self.color = color
        self.bg_color = bg_color
        self.bg_opacity = bg_opacity

        self.alpha = 0
        self.scale = 0.5
        self.animation_state = "HIDDEN"  # HIDDEN, FADE_IN, VISIBLE, FADE_OUT
        self.start_time = 0

    def setup(self) -> None:
        pass

    def handle_events(self) -> None:
        pass

    def update(self) -> None:
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if self.animation_state == "FADE_IN":
            if elapsed_time < 500:
                self.alpha = int((elapsed_time / 500) * 255 * self.bg_opacity)
                self.scale = 0.5 + (elapsed_time / 500) * 0.5
            else:
                self.alpha = int(255 * self.bg_opacity)
                self.scale = 1.0
                self.animation_state = "VISIBLE"
                self.start_time = current_time
        elif self.animation_state == "VISIBLE":
            if elapsed_time > self.duration:
                self.animation_state = "FADE_OUT"
                self.start_time = current_time
        elif self.animation_state == "FADE_OUT":
            if elapsed_time < 500:
                self.alpha = int((1 - (elapsed_time / 500)) * 255 * self.bg_opacity)
                self.scale = 1.0 - (elapsed_time / 500) * 0.5
            else:
                self.alpha = 0
                self.scale = 0.5
                self.animation_state = "HIDDEN"

    def render(self) -> None:
        if self.animation_state != "HIDDEN":
            scaled_width = int(self.size[0] * self.scale)
            scaled_height = int(self.size[1] * self.scale)

            bg_surface = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)
            bg_surface.fill(self.bg_color)
            bg_surface.set_alpha(self.alpha)

            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
            bg_surface.blit(text_surface, text_rect)

            scaled_bg = pg.transform.scale(bg_surface, (scaled_width, scaled_height))
            rect = scaled_bg.get_rect(center=self.pos)

            self.store.screen.blit(scaled_bg, rect)

    def show(self) -> None:
        self.animation_state = "FADE_IN"
        self.start_time = pg.time.get_ticks()


class PacmanScene(th.Scene):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        name: str,
    ):
        super().__init__(state, store, name)

        self.pacman_images = {
            "right": pg.image.load(th.asset_path("imgs", "pacman_right.png")).convert_alpha(),
            "left": pg.image.load(th.asset_path("imgs", "pacman_left.png")).convert_alpha(),
            "up": pg.image.load(th.asset_path("imgs", "pacman_up.png")).convert_alpha(),
            "down": pg.image.load(th.asset_path("imgs", "pacman_down.png")).convert_alpha(),
            "close_right": pg.image.load(th.asset_path("imgs", "pacman_close_right.png")).convert_alpha(),
            "close_left": pg.image.load(th.asset_path("imgs", "pacman_close_left.png")).convert_alpha(),
            "close_up": pg.image.load(th.asset_path("imgs", "pacman_close_up.png")).convert_alpha(),
            "close_down": pg.image.load(th.asset_path("imgs", "pacman_close_down.png")).convert_alpha(),
        }
        for key, img in self.pacman_images.items():
            self.pacman_images[key] = pg.transform.scale(img, (70, 70))

        self.pacman_image = self.pacman_images["right"]
        self.scaled_pacman = self.pacman_image
        self.pacman_direction = "right"

        self.pacman_pos = pg.Vector2(self.store.screen.get_width() / 2, self.store.screen.get_height() / 2)
        self.pacman_target_pos = pg.Vector2(self.store.screen.get_width() / 2, self.store.screen.get_height() / 2)
        self.easing = 0.1

        self.score = 0
        self.collectibles = pg.sprite.Group()
        self._spawn_margin = int(0.3 * self.state.window_size[1])
        self._spawn_initial_collectibles()

        self.toasts: list[Toast] = []

        self.background = self.store.imgs["pacman_bg_gray"].convert()

        self.eat_0_buffer = None
        self.eat_1_buffer = None
        self.eat_2_buffer = None

    def setup(self):
        self.state.hand_running = True
        self.state.set_scene_hand_callback(self._hand_callback)

    def handle_events(self):
        for event in self.state.events:
            if event.type == th.THEHAND_EVENT:
                if event.code == th.C_VECTOR:
                    self.pacman_target_pos.x = event.value[0]
                    self.pacman_target_pos.y = event.value[1]

    def update(self):
        if self.score > 10000:
            return

        velocity = pg.Vector2(
            (self.pacman_target_pos.x - self.pacman_pos.x),
            (self.pacman_target_pos.y - self.pacman_pos.y),
        )

        if velocity.magnitude_squared() > 1:
            if abs(velocity.x) > abs(velocity.y):
                self.pacman_direction = "right" if velocity.x > 0 else "left"
            else:
                self.pacman_direction = "down" if velocity.y > 0 else "up"

        self.pacman_pos.x += velocity.x * self.easing
        self.pacman_pos.y += velocity.y * self.easing

        state = "close_" if (self.state.now // 500) % 2 == 0 else ""
        self.pacman_image = self.pacman_images[state + self.pacman_direction]

        scale_factor = 2 * min(self.score, 10000) / 10000 + 1
        self.scaled_pacman = pg.transform.scale_by(self.pacman_image, scale_factor)

        pacman_sprite = pg.sprite.Sprite()
        pacman_sprite.rect = self.scaled_pacman.get_rect(center=self.pacman_pos)

        collided_collectibles = pg.sprite.spritecollide(pacman_sprite, self.collectibles, True)
        for collectible in collided_collectibles:
            self.score += collectible.points

            if not self.eat_0_buffer or not self.eat_0_buffer.get_busy():
                self.eat_0_buffer = pg.mixer.Sound.play(self.store.sounds["munch"])
            if self.score > 2000 and self.score < 5000:
                if random.random() < 0.5:
                    if not self.eat_1_buffer or not self.eat_1_buffer.get_busy():
                        self.eat_1_buffer = pg.mixer.Sound.play(self.store.sounds["heavy_eating"])
            elif self.score > 5000:
                if random.random() < 0.2:
                    if self.score < 7500:
                        self.store.sounds["auughhh"].set_volume(0.5)
                    else:
                        self.store.sounds["auughhh"].set_volume(1)
                    if not self.eat_2_buffer or not self.eat_2_buffer.get_busy():
                        self.eat_2_buffer = pg.mixer.Sound.play(self.store.sounds["auughhh"])

            toast = Toast(
                self.state,
                self.store,
                (collectible.rect.centerx, collectible.rect.centery),
                (100, 50),
                f"+ {collectible.points}",
                1000,
                color=th.COLOR_MOCHA_BASE,
                bg_color=th.COLOR_MOCHA_RED,
            )
            toast.show()
            self.toasts.append(toast)
            self._spawn_collectible(type(collectible))

        for toast in self.toasts:
            toast.update()
        self.toasts = [toast for toast in self.toasts if toast.animation_state != "HIDDEN"]

    def render(self):
        self.store.screen.blit(self.background, (0, 0))

        self.collectibles.draw(self.store.screen)

        self.store.screen.blit(self.scaled_pacman, self.pacman_image.get_rect(center=self.pacman_pos))

        score_text = self.store.font_display_48.render(str(self.score), True, th.COLOR_MOCHA_TEXT)
        self.store.screen.blit(score_text, (60, 60))

        for toast in self.toasts:
            toast.render()

        if self.score > 10000:
            board_size = (self.state.window_size[0] / 2, self.state.window_size[1] / 2)
            board = pg.Surface(board_size, pg.SRCALPHA)
            board.fill((0, 0, 0, 178))

            # Image
            image = self.store.imgs["pacman_right"].convert_alpha()
            image = pg.transform.scale(image, (board_size[1] * 0.5, board_size[1] * 0.5))
            image_rect = image.get_rect(center=(board_size[0] / 2, board_size[1] / 2 - 50))
            board.blit(image, image_rect)

            # Text
            font = self.store.font_pixel_36
            text = font.render("Ok, you win.", True, (255, 255, 255))
            text_rect = text.get_rect(center=(board_size[0] / 2, board_size[1] / 2 + 100))
            board.blit(text, text_rect)

            board_rect = board.get_rect(center=(self.state.window_size[0] / 2, self.state.window_size[1] / 2))
            self.store.screen.blit(board, board_rect)

    def _hand_callback(self, result: HandLandmarkerResult) -> None:
        if not result.hand_world_landmarks or len(result.hand_world_landmarks) <= 0:
            return

        hand_landmarks = result.hand_landmarks

        for i, normalized_landmarks in enumerate(hand_landmarks):
            if len(normalized_landmarks) < 21:
                continue

            pos = th.get_hand_position_on_screen(
                normalized_landmarks,
                self.state.window_size[0],
                self.state.window_size[1],
            )

            if pos is None:
                continue

            pg.event.post(th.create_vector_event(pos))

    def _spawn_collectible(self, collectible_type):
        pos = (
            random.randint(self._spawn_margin, self.state.window_size[0] - self._spawn_margin),
            random.randint(self._spawn_margin, self.state.window_size[1] - self._spawn_margin),
        )
        collectible = collectible_type(pos)
        self.collectibles.add(collectible)

    def _spawn_initial_collectibles(self):
        for _ in range(5):
            self._spawn_collectible(Apple)
        for _ in range(2):
            self._spawn_collectible(Strawberry)
