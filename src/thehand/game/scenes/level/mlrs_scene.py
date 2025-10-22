import random

import pygame as pg

import thehand as th
from thehand.game.scenes.common import NovelScene, Page


class MlrsScene(NovelScene):
    def __init__(self, state: th.State, store: th.Store, name: str):
        scripts = {
            "welcome": "Welcome back, Commander.",
            "defeated": "Our frontline forces have been defeated.",
            "rocket": "But don't worry. Our rocket system are ready to\npushing them back to the held!",
            "fire": 'You just need to say "FIRE!!!".',
            "easy": "Easy, right?",
            "weldone": "Weldone Commander.",
        }

        pages = [
            Page(
                state,
                store,
                "welcome",
                None,
                store.imgs["mlrs_00"],
                scripts["welcome"],
                store.sounds["mlrs_00_welcome"],
                depend_on_sound=True,
            ),
            Page(
                state,
                store,
                "defeated",
                None,
                store.imgs["mlrs_00"],
                scripts["defeated"],
                store.sounds["mlrs_01_defeated"],
                depend_on_sound=True,
            ),
            Page(
                state,
                store,
                "rocket",
                None,
                store.imgs["mlrs_00"],
                scripts["rocket"],
                store.sounds["mlrs_02_rocket"],
                depend_on_sound=True,
            ),
            Page(
                state,
                store,
                "fire",
                None,
                store.imgs["mlrs_00"],
                scripts["fire"],
                store.sounds["mlrs_03_fire"],
                depend_on_sound=True,
            ),
            Page(
                state,
                store,
                "easy",
                None,
                store.imgs["mlrs_00"],
                scripts["easy"],
                store.sounds["mlrs_04_easy"],
                depend_on_sound=True,
            ),
            Page(
                state,
                store,
                "wait",
                self._fire_callback,
                store.imgs["mlrs_00"],
                'Nói đi. Nói "Firrreeee!!!" ý.',
                infinity=True,
            ),
            Page(
                state,
                store,
                "launch",
                None,
                store.imgs["mlrs_01"],
                None,
                store.sounds["mlrs_05_launch"],
                duration=3000,
            ),
            Page(
                state,
                store,
                "weldone",
                None,
                store.imgs["mlrs_01"],
                scripts["weldone"],
                store.sounds["mlrs_06_weldone"],
                3000,
            ),
        ]

        super().__init__(name, state, store, pages)

    def setup(self):
        super().setup()

        self.store.sounds["ambient_rain"].set_volume(2)
        self.store.sounds["ambient_rain"].play()
        self.state.set_scene_sr_callback(self._sr_callback)

    def handle_events(self):
        super().handle_events()

        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.next_page()

    def update(self):
        super().update()

    def render(self):
        super().render()

    def _fire_callback(self, text: str):
        if "fire" in text.lower():
            speech_volume = self.state.get_speech_volume()
            if speech_volume > 0.04:
                self.next_page()
            else:
                self.pages[self.current_page_index].text = "Nói nhỏ quá..."
        elif text:
            self.pages[self.current_page_index].text = "." * random.randrange(3, 9)

    def _sr_callback(self, text: str):
        th.print_inline(text)

        if self.pages[self.current_page_index].sr_callback:
            self.pages[self.current_page_index].sr_callback(text)
