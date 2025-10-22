import thehand as th


class EmptyScene(th.Scene):
    def __init__(self, state: th.State, store: th.Store, name: str):
        super().__init__(state, store, name)

    def setup(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return
