import pygame as pg

import thehand as th


class Page(th.Entity):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        name: str,
        sr_callback: th.SrResultCallback | None = None,
        background: pg.Surface | None = None,
        text: str | None = None,
        sound: pg.Sound | None = None,
        duration: int = 3000,
        depend_on_sound: bool = False,
        infinity: bool = False,
    ) -> None:
        super().__init__(state, store)

        self.name = name
        self.sr_callback = sr_callback

        self.background = background
        if self.background:
            self.background = pg.transform.smoothscale(self.background, self.state.window_size)

        self.text = text

        self.box_height = self.state.window_size[1] // 6
        if self.text:
            self.text_bg_sur = pg.Surface((int(self.state.window_size[0]), self.box_height)).convert()
            self.text_bg_sur.fill(th.COLOR_MOCHA_BASE)
            self.text_bg_sur.set_alpha(int(0.3 * 255))
            self.text_bg_rect = self.text_bg_sur.get_rect(
                center=(self.state.window_size[0] // 2, self.state.window_size[1] - self.box_height // 2)
            )

        self.sound = sound
        self.channel = None
        self.duration = duration
        self.depend_on_sound = depend_on_sound
        self.infinity = infinity

    def setup(self) -> None:
        if self.sound:
            self.channel = self.sound.play()

    def handle_events(self) -> None:
        return

    def update(self) -> None:
        return

    def render(self) -> None:
        if self.background:
            self.store.screen.blit(self.background, (0, 0))
        if self.text:
            self.text_sur = self.store.font_text_24.render(self.text, True, th.COLOR_MOCHA_TEXT)
            self.text_rect = self.text_sur.get_rect(
                center=(self.state.window_size[0] // 2, self.state.window_size[1] - self.box_height // 2)
            )

            self.store.screen.blit(self.text_bg_sur, self.text_bg_rect)
            self.store.screen.blit(self.text_sur, self.text_rect)


class NovelScene(th.Scene):
    def __init__(self, name: str, state: th.State, store: th.Store, pages: list[Page]):
        super().__init__(state, store, name)

        self.pages = pages
        self.current_page_index = 0

        self._page_timer = 0

    def setup(self):
        self.set_current_page(0)

    def handle_events(self):
        return

    def update(self):
        page = self.pages[self.current_page_index]

        if page.infinity:
            return

        if page.depend_on_sound:
            if not page.channel or not page.channel.get_busy():
                self.next_page()
        else:
            if self.state.now - self._page_timer > self.pages[self.current_page_index].duration:
                self.next_page()

    def render(self):
        self.pages[self.current_page_index].render()

    def set_current_page(self, index: int):
        if index >= len(self.pages):
            return

        self.current_page_index = index

        self.pages[index].setup()
        self._page_timer = self.state.now
        self.state.set_scene_sr_callback(self.pages[index].sr_callback)

    def next_page(self):
        self.set_current_page(self.current_page_index + 1)
