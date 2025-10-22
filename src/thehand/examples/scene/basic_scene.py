import pygame as pg

import thehand as th


class BasicScene(th.Scene):
    def __init__(
        self,
        name: str,
        state: th.State,
        store: th.Store,
    ):
        super().__init__(state, store, name)

        self.image = None
        self.image_rect = None

        self.icon_ratio = 0.3

        self.alpha = 0
        self.animation_speed = 2

        self.start_time = pg.time.get_ticks()

    def setup(self):
        original_image = pg.image.load(th.asset_path("imgs", "thehand_icon.png")).convert_alpha()

        new_height = self.store.screen.get_height() * self.icon_ratio
        aspect_ratio = original_image.get_width() / original_image.get_height()
        new_width = new_height * aspect_ratio

        self.image = pg.transform.smoothscale(original_image, (new_width, new_height))
        self.image_rect = self.image.get_rect(center=self.store.screen.get_rect().center)

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("Space!")

    def update(self):
        self.alpha += self.animation_speed
        if self.alpha > 255:
            self.animation_speed = -self.animation_speed
            self.alpha = 255
        if self.alpha < 0:
            self.animation_speed = -self.animation_speed
            self.alpha = 0

    def render(self):
        self.store.screen.fill(th.COLOR_MOCHA_BASE)

        if self.image:
            self.image.set_alpha(self.alpha)
            self.store.screen.blit(self.image, self.image_rect)
