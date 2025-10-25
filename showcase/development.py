from thehand.game import TheHandGame

import pygame as pg


def main():
    game = TheHandGame()

    game.state.debug_mode = True
    game.state.window_size = (1024, 640)
    game.state.display_flag = pg.SHOWN

    game.init()
    game.run()


if __name__ == "__main__":
    main()
