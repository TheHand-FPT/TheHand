import os
import random
import time
from typing import Callable

import pygame as pg

import thehand as th


class GestureSprite:
    __slots__ = ("image", "rect", "speed", "gesture", "spawn_time")

    def __init__(self, image: pg.Surface, x: int, y: int, speed: float, gesture: str):
        self.image = image
        self.rect = image.get_rect(centerx=x, y=y)
        self.speed = speed
        self.gesture = gesture
        self.spawn_time = time.time()


class MagicGestureScene(th.Scene):
    """Falling-gesture gameplay scene.

    Rules implemented from user's spec:
    - Use all files in data/imgs/Gestures_4x4
    - Map file name: '01_index.png' -> gesture key 'index' -> detector is_hand_index
    - Spawn rate starts 0.5/sec, increases by +1/sec every 2 minutes
    - Fall speed starts 50 px/s, increases 10% every minute
    - Spawn x is random across screen width with 50px padding each side
    - Ground Y is bottom of main character rect
    - One detection match removes the sprite, +10 score
    - If sprite hits ground: -1 life, red flash + small shake, play sounds
    - Start with 5 lives, show HUD top-left (lives above score)
    - Game over UI with CONTINUE and RESTART buttons
    """

    def __init__(self, state: th.State, store: th.Store, name: str):
        super().__init__(state, store, name)

        # surfaces and fonts
        self.screen = getattr(self.store, "screen", pg.display.get_surface()) or pg.Surface(self.state.window_size)
        self.font_lives = getattr(self.store, "font_text_32", pg.font.SysFont("Arial", 32))
        self.font_score = getattr(self.store, "font_text_24", pg.font.SysFont("Arial", 24))

        # background and main character
        bg_path = th.asset_path("imgs", "mgs_background.jpg")
        try:
            self.bg_img = pg.image.load(bg_path).convert()
            self.bg_img = pg.transform.scale(self.bg_img, self.screen.get_size())
        except Exception:
            self.bg_img = pg.Surface(self.screen.get_size())
            self.bg_img.fill(th.COLOR_MOCHA_BASE if hasattr(th, "COLOR_MOCHA_BASE") else (30, 30, 46))

        # main character
        char_path = th.asset_path("imgs", "mgs_main_character.png")
        try:
            char_img = pg.image.load(char_path).convert_alpha()
            # The character image already has no background; keep it simple and fast
            cw = int(self.screen.get_width() * 0.10)
            ch = int(char_img.get_height() * (cw / max(1, char_img.get_width())))
            self.char_img = pg.transform.smoothscale(char_img, (cw, ch))
        except Exception:
            self.char_img = pg.Surface((50, 50), pg.SRCALPHA)
            self.char_img.fill((255, 0, 0, 180))

        self.char_rect = self.char_img.get_rect(centerx=self.screen.get_width() // 2)
        # Ground y defined relative to character bottom
        self.ground_y = self.screen.get_height() - int(self.char_img.get_height() * 0.9)
        self.char_rect.bottom = self.ground_y

        # Gameplay parameters
        self.spawn_per_second = 0.5
        self.base_fall_speed = 200.0
        self.max_sprites = 6
        self.lives = 5
        self.score = 0

        self.sprites: list[GestureSprite] = []
        self._last_spawn = time.time()
        self._start_time = time.time()
        self._last_update = time.time()

        # load gesture images & mapping
        self.gesture_images: list[tuple[str, pg.Surface]] = []
        gestures_dir = os.path.join("data", "imgs", "Gestures_4x4")
        if os.path.isdir(gestures_dir):
            for fname in sorted(os.listdir(gestures_dir)):
                if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                full = os.path.join(gestures_dir, fname)
                try:
                    img = pg.image.load(full).convert_alpha()
                    name = os.path.splitext(fname)[0]
                    gesture_key = name.split("_")[-1] if "_" in name else name
                    self.gesture_images.append((gesture_key, img))
                except Exception:
                    continue

        # sounds
        self.sound_score = self._load_sound("audio/score.mp3")
        self.sound_hit = self._load_sound("audio/roblox-death.mp3")
        self.sound_last = self._load_sound("audio/gta-v-death.mp3")

        # visual feedback timers
        self._red_flash_timer = 0.0
        self._shake_timer = 0.0

        self._game_over = False
        self._buttons = {}

        # debug
        self._debug = True
        self.done = False

    def _load_sound(self, rel: str):
        try:
            parts = rel.split("/", 1)
            if len(parts) == 2:
                p = th.asset_path(parts[0], parts[1])
            else:
                p = th.asset_path("audio", rel)
            return pg.mixer.Sound(p)
        except Exception:
            return None

    def _spawn_sprite(self):
        if self._game_over:
            return
        if not self.gesture_images or len(self.sprites) >= self.max_sprites:
            return
        key, img = random.choice(self.gesture_images)
        x = random.randint(50, max(50, self.screen.get_width() - 50))
        y = -img.get_height() // 2
        sprite = GestureSprite(img, x, y, self.base_fall_speed, key)
        self.sprites.append(sprite)

    def _increase_difficulty(self, elapsed: float):
        extra = int(elapsed // 30)
        self.spawn_per_second = 0.5 + extra * 1.0
        speed_multiplier = 1.0 * (1.1 ** int(elapsed // 10))
        self.current_fall_speed = self.base_fall_speed * speed_multiplier

    def _on_hand_result(self, result) -> None:
        if self._game_over:
            return
        if not result:
            return
        hand_landmarks_list = getattr(result, "hand_landmarks", None) or getattr(result, "hand_world_landmarks", None)
        if not hand_landmarks_list:
            return

        for sprite in list(self.sprites):
            for landmarks in hand_landmarks_list:
                func_name = f"is_hand_{sprite.gesture}"
                detector: Callable | None = getattr(th, func_name, None)
                if callable(detector):
                    try:
                        ok = detector(landmarks)
                    except Exception:
                        ok = False
                    if ok:
                        self._on_sprite_matched(sprite)
                        th.print_inline(f"Matched: {sprite.gesture}")
                        return

    def _on_sprite_matched(self, sprite: GestureSprite):
        try:
            self.sprites.remove(sprite)
        except ValueError:
            pass
        self.score += 10
        if self.sound_score:
            try:
                self.sound_score.play()
            except Exception:
                pass

    def _on_sprite_hit_ground(self, sprite: GestureSprite):
        try:
            self.sprites.remove(sprite)
        except ValueError:
            pass
        # Decrease lives but don't go below zero
        self.lives = max(0, self.lives - 1)
        self._red_flash_timer = 0.1
        self._shake_timer = 0.1
        if self.lives <= 0:
            if self.sound_last:
                try:
                    self.sound_last.play()
                except Exception:
                    pass
            self._game_over = True
            # freeze vision input for this scene and unregister callback
            try:
                self.state.set_scene_hand_callback(None)
            except Exception:
                pass
            self.state.hand_running = False
        else:
            if self.sound_hit:
                try:
                    self.sound_hit.play()
                except Exception:
                    pass

    def setup(self) -> None:
        # register to receive hand callbacks for scene
        self.state.set_scene_hand_callback(self._on_hand_result)
        self.state.hand_running = True

        self._start_time = time.time()
        self._last_spawn = time.time()
        self._last_update = time.time()
        self.sprites.clear()
        self.lives = 5
        self.score = 0
        self._game_over = False

    def handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1 and self.sprites:
                    self._on_sprite_matched(self.sprites[0])
                elif event.key == pg.K_d:
                    self.state.hand_running = not self.state.hand_running
                elif event.key == pg.K_s:
                    self._spawn_sprite()
            elif event.type == pg.MOUSEBUTTONDOWN and self._game_over:
                mx, my = event.pos
                for name, rect in self._buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == "continue":
                            self.done = True
                        elif name == "restart":
                            self.setup()

    def update(self) -> None:
        now = time.time()
        dt = now - self._last_update
        self._last_update = now
        elapsed = now - self._start_time
        self._increase_difficulty(elapsed)

        # If game over, freeze gameplay (no spawn, no movement)
        if self._game_over:
            return

        if self.spawn_per_second > 0:
            interval = 1.0 / max(0.001, self.spawn_per_second)
            if now - self._last_spawn >= interval:
                self._spawn_sprite()
                self._last_spawn = now

        current_speed = getattr(self, "current_fall_speed", self.base_fall_speed)
        for sprite in list(self.sprites):
            sprite.rect.y += int(current_speed * dt)
            if sprite.rect.bottom >= self.ground_y:
                self._on_sprite_hit_ground(sprite)

        if self._red_flash_timer > 0:
            self._red_flash_timer = max(0.0, self._red_flash_timer - dt)
        if self._shake_timer > 0:
            self._shake_timer = max(0.0, self._shake_timer - dt)

    def render(self) -> None:
        # camera shake
        offset_x = offset_y = 0
        if self._shake_timer > 0:
            offset_x = random.randint(-6, 6)
            offset_y = random.randint(-4, 4)

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg_img, (offset_x, offset_y))

        for sprite in self.sprites:
            self.screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

        self.screen.blit(self.char_img, (self.char_rect.x + offset_x, self.char_rect.y + offset_y))

        lives_text = f"Lives: {self.lives}"
        score_text = f"Score: {self.score}"
        lives_surf = self.font_lives.render(lives_text, True, (255, 255, 255))
        score_surf = self.font_score.render(score_text, True, (255, 255, 255))
        self.screen.blit(lives_surf, (10, 10))
        self.screen.blit(score_surf, (10, 10 + lives_surf.get_height() + 4))

        if self._red_flash_timer > 0:
            flash = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
            flash.fill((180, 0, 0, int(255 * (self._red_flash_timer / 0.1))))
            self.screen.blit(flash, (0, 0))

        if self._game_over:
            overlay = pg.Surface(self.screen.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(220)
            self.screen.blit(overlay, (0, 0))
            go_font = pg.font.SysFont(None, 96)
            small = pg.font.SysFont(None, 48)
            go_surf = go_font.render("GAME OVER", True, (220, 30, 30))
            score_surf2 = small.render(f"Score: {self.score}", True, (255, 255, 255))
            cx = self.screen.get_width() // 2
            self.screen.blit(go_surf, go_surf.get_rect(center=(cx, self.screen.get_height() // 2 - 40)))
            self.screen.blit(score_surf2, score_surf2.get_rect(center=(cx, self.screen.get_height() // 2 + 20)))

            btn_w, btn_h = 220, 56
            bx = cx - btn_w - 12
            by = self.screen.get_height() // 2 + 100
            rect_continue = pg.Rect(bx, by, btn_w, btn_h)
            rect_restart = pg.Rect(cx + 12, by, btn_w, btn_h)
            self._buttons = {"continue": rect_continue, "restart": rect_restart}
            pg.draw.rect(self.screen, (50, 50, 50), rect_continue)
            pg.draw.rect(self.screen, (50, 50, 50), rect_restart)
            tt = small.render("CONTINUE", True, (255, 255, 255))
            tr = small.render("RESTART", True, (255, 255, 255))
            self.screen.blit(tt, tt.get_rect(center=rect_continue.center))
            self.screen.blit(tr, tr.get_rect(center=rect_restart.center))
