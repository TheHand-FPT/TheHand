from thehand.game import TheHandGame


def main():
    game = TheHandGame()

    game.state.debug_mode = True

    game.init()
    game.run()


if __name__ == "__main__":
    main()
