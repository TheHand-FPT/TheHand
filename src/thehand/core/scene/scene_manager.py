import time

import pygame as pg

from thehand.core.state import State
from thehand.core.store import Store

from .scene import Scene


class SceneManager:
    def __init__(self, state: State, store: Store) -> None:
        self._state = state
        self._store = store

        self.scenes: dict[str, Scene] = {}

        self._current_scene: Scene | None = None

    def __call__(self) -> None:
        if not self._current_scene:
            print("Current scene empty")
            time.sleep(0.2)
            return

        if not self._current_scene._have_setup:
            self._current_scene._setup()
        self._current_scene.handle_events()
        self._current_scene.update()
        self._current_scene.render()
        pg.display.flip()

    def __add__(self, scene: Scene) -> "SceneManager":
        self.scenes[scene.name] = scene
        return self

    def __lshift__(self, scene: Scene) -> None:
        self.set_current(scene.name)

    def set_current(self, scene: str) -> bool:
        if not self.scenes.get(scene):
            return False

        self._current_scene = self.scenes[scene]
        return True

    def next(self) -> bool:
        if not self._current_scene or not self._current_scene.next_scene:
            return False

        return self.set_current(self._current_scene.next_scene)
