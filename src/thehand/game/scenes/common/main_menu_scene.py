import time
from threading import Thread

import pygame as pg
from PIL import Image

import thehand as th


class MainMenuScene(th.Scene):
    def __init__(self, state: th.State, store: th.Store, name: str):
        super().__init__(state, store, name)

        self.bg_frames = []
        self.bg_frame_idx = 0
        self.bg_frame_timer = 0
        self.bg_frame_delay = 100

        try:
            gif_path = th.asset_path("imgs", "menu_background.gif")
            pil_img = Image.open(gif_path)
            for frame in range(0, pil_img.n_frames):
                pil_img.seek(frame)
                frame_img = pil_img.convert("RGBA")
                raw_str = frame_img.tobytes()
                size = frame_img.size
                pg_img = pg.image.frombytes(raw_str, size, "RGBA")
                self.bg_frames.append(pg_img)
        except Exception:
            self.bg_frames = []

        # Button setup
        self.button_font = self.store.font_pixel_36
        self.start_btn_rect = pg.Rect(0, 0, 260, 70)
        self.quit_btn_rect = pg.Rect(0, 0, 260, 70)
        w, h = self.state.window_size
        self.start_btn_rect.center = (w // 2, h // 2 + 60)
        self.quit_btn_rect.center = (w // 2, h // 2 + 150)

        # Button effect state
        self.active_btn = None  # 'start' or 'quit'
        self.active_btn_time = 0

        # Speech recognition
        self.last_spoken = ""

        self._start_button_pressed = False

    def setup(self):
        self.state.set_scene_sr_callback(self._sr_callback)

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.start_btn_rect.collidepoint(mx, my):
                    self._press_start_button()
                elif self.quit_btn_rect.collidepoint(mx, my):
                    self._press_quit_button()

    def update(self):
        now = pg.time.get_ticks()

        if self.bg_frames:
            if now - self.bg_frame_timer > self.bg_frame_delay:
                self.bg_frame_idx = (self.bg_frame_idx + 1) % len(self.bg_frames)
                self.bg_frame_timer = now

        # Reset button effect after 0.5s
        if self.active_btn and now - self.active_btn_time > 500:
            self.active_btn = None

    def render(self):
        if self.bg_frames:
            bg = pg.transform.scale(self.bg_frames[self.bg_frame_idx], self.state.window_size)
            self.store.screen.blit(bg, (0, 0))
        else:
            self.store.screen.fill((25, 25, 25))

        self._draw_button(self.start_btn_rect, "START", active=(self.active_btn == "start"))

        self._draw_button(self.quit_btn_rect, "QUIT", active=(self.active_btn == "quit"))

        # Draw last spoken text as subtitle
        if self.last_spoken:
            subtitle_surf = self.store.font_text_32.render(self.last_spoken, True, (255, 255, 0))
            subtitle_rect = subtitle_surf.get_rect(
                center=(
                    self.store.screen.get_width() // 2,
                    self.store.screen.get_height() - 60,
                )
            )
            self.store.screen.blit(subtitle_surf, subtitle_rect)

    def _sr_callback(self, text):
        if not text:
            return

        self.last_spoken = text
        t = text.lower()

        if "start" in t:
            self._press_start_button()
        elif "quit" in t:
            self._press_quit_button()

    def _draw_button(self, rect, text, active=False):
        bg_color = th.COLOR_MOCHA_TEXT
        border_color = th.COLOR_MOCHA_CRUST
        txt_color = th.COLOR_MOCHA_CRUST

        if active:
            bg_color, border_color, txt_color = (
                border_color,
                bg_color,
                th.COLOR_MOCHA_TEXT,
            )
            rect = rect.copy()

        pg.draw.rect(self.store.screen, bg_color, rect)
        pg.draw.rect(self.store.screen, border_color, rect, 4)

        txt_surf = self.button_font.render(text, True, txt_color)
        txt_rect = txt_surf.get_rect(center=rect.center)

        self.store.screen.blit(txt_surf, txt_rect)

    def _activate_button(self, btn_name):
        self.active_btn = btn_name
        self.active_btn_time = pg.time.get_ticks()

    def _delayed_next_scene(self):
        def next_scene():
            time.sleep(1)
            pg.event.post(th.create_next_scene_event())

        Thread(target=next_scene, daemon=True).start()

    def _delayed_quit(self):
        def quit():
            time.sleep(1.5)
            pg.event.post(th.create_quit_event())

        Thread(target=quit, daemon=True).start()

    def _press_start_button(self):
        if self._start_button_pressed:
            return

        self.store.sounds["button_launch"].play()
        self._start_button_pressed = True
        self._activate_button("start")
        self._delayed_next_scene()

    def _press_quit_button(self):
        self.store.sounds["green_screen"].play()
        self._activate_button("quit")
        self._delayed_quit()
