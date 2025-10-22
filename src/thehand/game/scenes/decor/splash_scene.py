import pygame as pg

import thehand as th


class SplashScene(th.Scene):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        name: str,
        icon_ratio: float = 0.3,
    ):
        super().__init__(state, store, name)

        self.image = None
        self.image_rect = None

        self.icon_ratio = icon_ratio

        self.alpha = 0
        self.scale = 0.8
        self.animation_speed = 2
        self.zoom_speed = 0.005

        self.duration = 3500
        self.start_time = pg.time.get_ticks()

    def setup(self):
        self.store.sounds["windows_xp_startup"].play()
        original_image = self.store.imgs["thehand_icon"].convert_alpha()
        new_height = self.store.screen.get_height() * self.icon_ratio
        aspect_ratio = original_image.get_width() / original_image.get_height()
        new_width = new_height * aspect_ratio
        self.image = pg.transform.smoothscale(original_image, (new_width, new_height))
        self.image_rect = self.image.get_rect(center=self.store.screen.get_rect().center)

    def handle_events(self):
        return

    def update(self):
        if self.alpha < 255:
            self.alpha += self.animation_speed
            self.alpha = min(self.alpha, 255)

        if self.scale < 1.0:
            self.scale += self.zoom_speed
            self.scale = min(self.scale, 1.0)

        if self.state.now - self.start_time > self.duration:
            pg.event.post(th.create_next_scene_event())

    def render(self):
        self.store.screen.fill(th.COLOR_MOCHA_CRUST)

        if self.image:
            scaled_image = pg.transform.smoothscale_by(self.image, self.scale)
            scaled_image.set_alpha(self.alpha)
            scaled_rect = scaled_image.get_rect(center=self.image_rect.center)
            self.store.screen.blit(scaled_image, scaled_rect)
