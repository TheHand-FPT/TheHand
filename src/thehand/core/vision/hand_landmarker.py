import time

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

from thehand.core.configs import HAND_LANDMARKER_MODEL, NUM_HAND_DETECTED
from thehand.core.state import State


class HandLandmarker:
    def __init__(self, state: State) -> None:
        self.state = state

        base_options = BaseOptions(model_asset_path=HAND_LANDMARKER_MODEL)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=NUM_HAND_DETECTED,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self._mediapipe_result_callback,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(options)

    def __call__(self, image) -> None:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        self._landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

    def _mediapipe_result_callback(self, result: vision.HandLandmarkerResult, _, timestamp_ms: int) -> None:
        if self.state.hand_callback:
            self.state.hand_callback(result)
