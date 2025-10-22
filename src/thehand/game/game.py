from threading import Thread

import pygame as pg

import thehand as th
from thehand.game.configs import GAME_NAME
from thehand.game.scenes import (
    CreditScene,
    HintScene,
    MagicGestureScene,
    MainMenuScene,
    MlrsScene,
    PacmanScene,
    RpsScene,
    SplashScene,
)


class TheHandGame:
    def __init__(self) -> None:
        pg.init()
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption(GAME_NAME)

        self.state = th.State()
        self.state.set_sr_callback(self._sr_callback)
        self.state.set_hand_callback(self._hand_callback)
        self.state.set_face_callback(self._face_callback)
        self.state.set_pose_callback(self._pose_callback)

        self.store = th.Store()

        self.clock = pg.Clock()
        self.vision_clock = pg.Clock()

        self.scene_manager: th.SceneManager | None = None

        self.sr: th.SpeechRecognition | None = None

        self.camera: th.Camera | None = None
        self.face: th.FaceLandmarker | None = None
        self.hand: th.HandLandmarker | None = None
        self.pose: th.PoseLandmarker | None = None

    def init(self) -> None:
        self.store.screen = pg.display.set_mode(self.state.window_size, self.state.display_flag)

        self.scene_manager = th.SceneManager(self.state, self.store)

        self.sr = th.SpeechRecognition(self.state)
        self.state.get_speech_volume = self.sr.get_speech_volume

        self.camera = th.Camera()
        self.face = th.FaceLandmarker(self.state)
        self.hand = th.HandLandmarker(self.state)
        self.pose = th.PoseLandmarker(self.state)

        self._setup_scenes()

    def run(self) -> None:
        if not self.scene_manager:
            raise TypeError("SceneManager is not initialized")

        sr_thread = Thread(target=self.sr.run, daemon=True)
        sr_thread.start()

        vision_thread = Thread(target=self._run_vision, daemon=True)
        vision_thread.start()

        while True:
            self.state.now = pg.time.get_ticks()
            self._handle_events()
            self.scene_manager()
            self.state.dt = self.clock.tick(self.state.FPS)

    def quit(self) -> None:
        self.sr.stop()
        self.state.hand_running = False
        self.state.face_running = False
        self.state.pose_running = False
        pg.quit()

        print("\n\n\n" + " QUIT GAME ".center(80, "="))
        print("\n\n" + " Thank you for playing our game! ".center(80, "=") + "\n\n")

        exit(0)

    def _create_and_add_scenes(self) -> None:
        # Magic gesture scene should run first
        self.magic_scene = MagicGestureScene(self.state, self.store, "magic_gesture")
        self.scene_manager += self.magic_scene

        self.splash_scene = SplashScene(self.state, self.store, "splash")
        self.scene_manager += self.splash_scene

        self.main_menu_scene = MainMenuScene(self.state, self.store, "main_menu")
        self.scene_manager += self.main_menu_scene

        self.hint_pacman_scene = HintScene(
            self.state,
            self.store,
            "hint_pacman",
            self.store.imgs["pacman_bg"],
            self.store.sounds["pacman_start"],
            "Reach 10000 score to win!",
        )
        self.scene_manager += self.hint_pacman_scene

        self.pacman_scene = PacmanScene(self.state, self.store, "pacman")
        self.scene_manager += self.pacman_scene

        self.hint_mlrs_scene = HintScene(
            self.state,
            self.store,
            "hint_mlrs",
            self.store.imgs["flying_comets"],
            self.store.sounds["fire_in_the_hole"],
            "Like comets in the sky...",
        )
        self.scene_manager += self.hint_mlrs_scene

        self.mlrs_scene = MlrsScene(self.state, self.store, "mlrs")
        self.scene_manager += self.mlrs_scene

        self.hint_magic_scene = HintScene(
            self.state,
            self.store,
            "hint_magic",
            self.store.imgs["majik"],
            self.store.sounds["magic_spells"],
            "The true magic is your hand.",
        )
        self.scene_manager += self.hint_magic_scene

        self.magic_scene = MagicGestureScene(self.state, self.store, "magic")
        self.scene_manager += self.magic_scene

        self.hint_rps_scene = HintScene(
            self.state,
            self.store,
            "hint_rps",
            self.store.imgs["rps"],
            self.store.sounds["error"],
            "",
        )
        self.scene_manager += self.hint_rps_scene

        self.rps_scene = RpsScene(self.state, self.store, "rps")
        self.scene_manager += self.rps_scene

        self.credit_scene = CreditScene(self.state, self.store, "credit")
        self.scene_manager += self.credit_scene

    def _setup_scenes(self) -> None:
        self._create_and_add_scenes()

        # chain existing scenes as before
        (
            self.splash_scene
            >> self.main_menu_scene
            >> self.hint_pacman_scene
            >> self.pacman_scene
            >> self.hint_mlrs_scene
            >> self.mlrs_scene
            >> self.hint_magic_scene
            >> self.magic_scene
            >> self.hint_rps_scene
            >> self.rps_scene
            >> self.credit_scene
        )

        # set initial scene to magic gesture
        self.scene_manager << self.splash_scene

    def _sr_callback(self, text: str) -> None:
        th.print_inline(text)

        if self.state.scene_sr_callback:
            self.state.scene_sr_callback(text)

    def _hand_callback(self, hand: th.HandLandmarkerResult) -> None:
        if self.state.scene_hand_callback:
            self.state.scene_hand_callback(hand)

    def _face_callback(self, face: th.FaceLandmarkerResult) -> None:
        if self.state.scene_face_callback:
            self.state.scene_face_callback(face)

    def _pose_callback(self, pose: th.PoseLandmarkerResult) -> None:
        if self.state.scene_pose_callback:
            self.state.scene_pose_callback(pose)

    def _run_vision(self) -> None:
        if not self.face:
            raise TypeError("FaceLandmarker is not initialized")
        if not self.hand:
            raise TypeError("HandLandmarker is not initialized")
        if not self.pose:
            raise TypeError("PoseLandmarker is not initialized")

        while True:
            image = self.camera.read()

            if image is None:
                continue

            if self.state.hand_running:
                self.hand(image)

            if self.state.face_running:
                self.face(image)

            if self.state.pose_running:
                self.pose(image)

            self.vision_clock.tick(self.state.vision_FPS)

    def _next_scene(self) -> None:
        success = self.scene_manager.next()
        if not success:
            print("Failed to get next scene. Quitting.")
            self.quit()

    def _change_scene(self, scene: str) -> None:
        success = self.scene_manager.set_current(scene)
        if not success:
            print(f"Failed to change to '{scene}' scene. Quitting.")
            self.quit()

    def _handle_events(self) -> None:
        self.state.events = pg.event.get()

        for event in self.state.events:
            if event.type == pg.QUIT:
                self.quit()

            if event.type == th.THEHAND_EVENT:
                if event.code == th.C_NEXT_SCENE:
                    self._next_scene()
                if event.code == th.C_CHANGE_SCENE:
                    self._change_scene(event.value)

        if self.state.debug_mode:
            self._debug_handle_events()

    def _debug_handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    self._next_scene()


def main():
    game = TheHandGame()

    game.state.debug_mode = True
    game.state.window_size = (1280, 720)
    game.state.display_flag = pg.SHOWN

    game.init()
    game.run()


if __name__ == "__main__":
    main()
