import pygame as pg
from typing import Optional, Tuple

import thehand as th


class HintScene(th.Scene):
    """Scene that shows a static background and a single hint line at the bottom corner.

    Accepts optional `background_path` (image file) and `hint_text`.
    """

    def __init__(
        self,
        name: str,
        state: th.State,
        store: th.Store,
        background_path: Optional[str] = None,
        hint_text: str = "Hãy sử dụng tay của bạn để di chuyển",
        text_color: Tuple[int, int, int] = (240, 240, 240),
        align: str = "left",
    ) -> None:
        super().__init__(name, state, store)
        self.background_path = background_path
        self.hint_text = hint_text
        self.text_color = text_color
        self.align = align if align in ("left", "right") else "left"

        self.background: Optional[pg.Surface] = None

    def setup(self) -> None:
        """Load and scale background image if provided."""
        if self.background_path:
            try:
                img = pg.image.load(self.background_path)
                self.background = pg.transform.scale(img, self.store.screen.get_size()).convert()
            except Exception as e:
                print(f"[HintScene] Không thể tải background: {e}")
                self.background = None

        self.have_setup = True

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.done = True

    def update(self) -> None:
        pass

    def render(self) -> None:
        screen = self.store.screen
        screen.fill((25, 25, 25))

        if self.background:
            screen.blit(self.background, (0, 0))

        # draw bottom-corner hint text
        font = getattr(self.store, "font_text_24", None)
        if font is None:
            font = pg.font.SysFont(None, 24)

        text_surface = font.render(self.hint_text, True, self.text_color)
        text_rect = text_surface.get_rect()
        padding = 10
        if self.align == "left":
            text_rect.bottomleft = (padding, screen.get_height() - padding)
        else:
            text_rect.bottomright = (screen.get_width() - padding, screen.get_height() - padding)

        screen.blit(text_surface, text_rect)

        pg.display.flip()
