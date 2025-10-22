from typing import Callable

import pygame as pg

from .configs import DEFAULT_WINDOW_SIZE
from .types import FaceResultCallback, HandResultCallback, PoseResultCallback, SrResultCallback


class State:
    def __init__(self) -> None:
        self.debug_mode = False

        self.window_size = DEFAULT_WINDOW_SIZE
        self.display_flag = pg.FULLSCREEN

        self.FPS: int = 60
        self.vision_FPS: int = 10

        self.now = pg.time.get_ticks()
        self.dt: int = 1000 // self.FPS
        self.events: list[pg.event.Event] = []
        self.cursor = pg.SYSTEM_CURSOR_ARROW

        self.sr_running = False
        self.face_running = False
        self.hand_running = False
        self.pose_running = False

        self.get_speech_volume: Callable[[], float] = lambda: -1

        self.sr_callback: SrResultCallback | None = None
        self.scene_sr_callback: SrResultCallback | None = None

        self.hand_callback: HandResultCallback | None = None
        self.scene_hand_callback: HandResultCallback | None = None

        self.face_callback: FaceResultCallback | None = None
        self.scene_face_callback: FaceResultCallback | None = None

        self.pose_callback: PoseResultCallback | None = None
        self.scene_pose_callback: PoseResultCallback | None = None

    def set_sr_callback(self, sr_callback: SrResultCallback) -> None:
        self.sr_callback = sr_callback

    def set_scene_sr_callback(self, sr_callback: SrResultCallback) -> None:
        self.scene_sr_callback = sr_callback

    def set_hand_callback(self, hand_callback: HandResultCallback) -> None:
        self.hand_callback = hand_callback

    def set_scene_hand_callback(self, hand_callback: HandResultCallback) -> None:
        self.scene_hand_callback = hand_callback

    def set_face_callback(self, face_callback: FaceResultCallback) -> None:
        self.face_callback = face_callback

    def set_scene_face_callback(self, face_callback: FaceResultCallback) -> None:
        self.scene_face_callback = face_callback

    def set_pose_callback(self, pose_callback: PoseResultCallback) -> None:
        self.pose_callback = pose_callback

    def set_scene_pose_callback(self, pose_callback: PoseResultCallback) -> None:
        self.scene_pose_callback = pose_callback
