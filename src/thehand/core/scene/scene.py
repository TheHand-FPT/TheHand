from abc import ABC, abstractmethod

from thehand.core.state import State
from thehand.core.store import Store


class Scene(ABC):
    def __init__(
        self,
        state: State,
        store: Store,
        name: str,
    ) -> None:
        self.state = state
        self.store = store
        self.name = name

        self.next_scene: str = ""

        self._have_setup = False

    def __rshift__(self, other: "Scene") -> "Scene":
        self.next_scene = other.name
        return other

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError

    def _setup(self) -> None:
        self.setup()
        self._have_setup = True
