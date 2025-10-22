import pygame as pg

import thehand as th


class RPSScene(th.Scene):
    def __init__(self, state: th.State, store: th.Store, name: str):
        super().__init__(state, store, name)

        self.player_surface = pg.Surface((self.store.screen.get_width(), self.store.screen.get_height() / 2))
        self.machine_surface = pg.Surface((self.store.screen.get_width(), self.store.screen.get_height() / 2))

        self.player_surface.fill(th.COLOR_MOCHA_BLUE)
        self.machine_surface.fill(th.COLOR_MOCHA_RED)

    def setup(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        pass

    def render(self):
        self.store.screen.blit(self.machine_surface, (0, 0))
        self.store.screen.blit(self.player_surface, (0, self.store.screen.get_height() / 2))
