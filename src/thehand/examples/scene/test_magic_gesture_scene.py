import pygame as pg

import thehand as th
from thehand.game.scenes.level.Magic_gesture_scene import MagicGestureScene


def main():
    pg.init()
    state = th.State()
    screen = pg.display.set_mode(state.window_size)
    clock = pg.time.Clock()
    store = th.Store()
    # make store.screen available for scene convenience
    store.screen = screen

    # New constructor: (state, store, name)
    scene = MagicGestureScene(state, store, "magic_gesture")
    scene.setup()
    running = True
    while running and not scene.done:
        state.events = pg.event.get()
        scene.handle_events()
        scene.update()
        scene.render()
        clock.tick(state.FPS)
    pg.quit()


if __name__ == "__main__":
    main()
