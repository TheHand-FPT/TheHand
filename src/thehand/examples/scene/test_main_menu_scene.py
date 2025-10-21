import pygame as pg

import thehand as th


def main():
    pg.init()

    clock = pg.time.Clock()

    state = th.State()
    store = th.Store()
    sr = th.SpeechRecognition(state)

    store.screen = pg.display.set_mode(state.window_size)

    scene = th.MainMenuScene("MainMenu", state, store, sr)

    scene.setup()

    while not scene.done:
        state.events = pg.event.get()

        scene.handle_events()
        scene.update()
        scene.render()

        clock.tick(state.FPS)

    pg.quit()


if __name__ == "__main__":
    main()
