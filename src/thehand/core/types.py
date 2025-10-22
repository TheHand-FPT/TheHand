from typing import Any, Callable, TypedDict

from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarkerResult
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

type SrResultCallback = Callable[[str], None]

type FaceResultCallback = Callable[[FaceLandmarkerResult], None]
type HandResultCallback = Callable[[HandLandmarkerResult], None]
type PoseResultCallback = Callable[[PoseLandmarkerResult], None]


class TheHandEventData(TypedDict):
    code: int
    value: Any
    seed: int
