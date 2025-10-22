import pygame as pg

import thehand as th


class HintScene(th.Scene):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        name: str,
        background: pg.Surface | None = None,
        sound: pg.mixer.Sound | None = None,
        text: str = "",
        text_color: tuple[int, int, int] = th.COLOR_MOCHA_TEXT,
        align: str = "left",
    ) -> None:
        super().__init__(state, store, name)

        self.background = background
        self.sound = sound
        self.text = text
        self.text_color = text_color
        self.align = align if align in ("left", "right") else "left"

    def setup(self) -> None:
        if self.background:
            self.background = pg.transform.scale(self.background, self.state.window_size).convert()

        if self.sound:
            self.sound.play()

        self._start_timer = self.state.now

    def handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.KEYDOWN and event.key in (pg.K_ESCAPE, pg.K_RETURN):
                pg.event.post(th.create_next_scene_event())

    def update(self) -> None:
        if self.state.now - self._start_timer > 5000:
            pg.event.post(th.create_next_scene_event())

    def render(self) -> None:
        screen = self.store.screen
        screen.fill(th.COLOR_MOCHA_CRUST)

        if self.background:
            screen.blit(self.background, (0, 0))

        font = self.store.font_text_32

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        padding = 60
        if self.align == "left":
            text_rect.bottomleft = (padding, screen.get_height() - padding)
        else:
            text_rect.bottomright = (screen.get_width() - padding, screen.get_height() - padding)

        screen.blit(text_surface, text_rect)
