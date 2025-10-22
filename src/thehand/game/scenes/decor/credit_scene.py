import pygame as pg

import thehand as th


class CreditScene(th.Scene):
    def __init__(self, state: th.State, store: th.Store, name: str):
        super().__init__(state, store, name)

    def setup(self):
        self.bg_color = (20, 20, 20)
        self.text_color = (255, 255, 255)

        self.lines = [
            "CREDITS",
            "",
            "A product by TheHand Corporation",
            "",
            "Nguyễn Thế Anh",
            "Trần Đức Thịnh",
            "Châm Duy Khoát",
            "Hoàng Minh Nhất",
            "Đinh Duy Khương",
            "",
            "",
            "Thank you for playing the game!",
            "",
            "Press ESC or SPACE to exit",
        ]

    def handle_events(self):
        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_SPACE):
                    pg.event.post(th.create_quit_event())

    def update(self):
        pass

    def render(self):
        self.store.screen.fill(self.bg_color)

        y = 150
        for line in self.lines:
            text_surface = self.store.font_text_24.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.store.screen.get_width() / 2, y))
            self.store.screen.blit(text_surface, text_rect)
            y += 40

        pg.display.flip()
