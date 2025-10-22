from mediapipe.tasks.python.components.containers.landmark import (
    Landmark,
    NormalizedLandmark,
)

from .utils import (
    calculate_angle_2d,
    calculate_angle_3d,
    calculate_distance,
    normalized_landmarks_to_coordinates,
)


def get_hand_position_on_screen(
    normalized_landmarks: list[NormalizedLandmark],
    screen_width: int,
    screen_height: int,
) -> None | tuple[float, float]:
    coordinates = normalized_landmarks_to_coordinates(normalized_landmarks, screen_width, screen_height)

    if coordinates[9]:
        return coordinates[9][0], coordinates[9][1]  # ty: ignore[invalid-return-type]

    return None


def is_hand_palm(landmarks: list[Landmark]) -> bool:
    return (
        is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_open(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_like(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_horizontal(landmarks)
        and is_hand_horizontal_up(landmarks)
        and is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_dislike(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_horizontal(landmarks)
        and is_hand_horizontal_down(landmarks)
        and is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_point(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_fuck(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_open(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_index(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_v(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_three(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_open(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_gun(landmarks: list[Landmark]) -> bool:
    distance_8_12 = calculate_distance(landmarks[8], landmarks[12])
    distance_5_9 = calculate_distance(landmarks[5], landmarks[9])

    return (
        distance_8_12 * 0.7 < distance_5_9
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_four(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_open(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_spider(landmarks: list[Landmark]) -> bool:
    return (
        is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_promise(landmarks: list[Landmark]) -> bool:
    return (
        not is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_call(landmarks: list[Landmark]) -> bool:
    return (
        is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_v_capture(landmarks: list[Landmark]) -> bool:
    angle_4_5_8 = calculate_angle_3d(landmarks[4], landmarks[5], landmarks[8])
    return (
        int(angle_4_5_8) in range(75, 135)
        and is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_ok(landmarks: list[Landmark]) -> bool:
    distance_4_8 = calculate_distance(landmarks[4], landmarks[8])
    distance_3_4 = calculate_distance(landmarks[3], landmarks[4])

    return (
        distance_4_8 < distance_3_4 * 1.3
        and is_middle_open(landmarks)
        and is_ring_open(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_punch(landmarks: list[Landmark]) -> bool:
    return (
        is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_vertical(landmarks: list[Landmark]) -> bool:
    angle_0_9 = calculate_angle_2d(landmarks[0], landmarks[9])
    return (int(angle_0_9) in range(45, 135)) or (angle_0_9 in range(-135, -45))


def is_hand_vertical_up(landmarks: list[Landmark]) -> bool:
    angle_0_9 = calculate_angle_2d(landmarks[0], landmarks[9])
    return int(angle_0_9) in range(-135, -45)


def is_hand_vertical_down(landmarks: list[Landmark]) -> bool:
    angle_0_9 = calculate_angle_2d(landmarks[0], landmarks[9])
    return int(angle_0_9) in range(45, 135)


def is_hand_horizontal(landmarks: list[Landmark]) -> bool:
    angle_5_17 = calculate_angle_2d(landmarks[5], landmarks[17])
    return (int(angle_5_17) in range(45, 135)) or (int(angle_5_17) in range(-135, -45))


def is_hand_horizontal_up(landmarks: list[Landmark]) -> bool:
    angle_5_17 = calculate_angle_2d(landmarks[5], landmarks[17])
    return int(angle_5_17) in range(45, 135)


def is_hand_horizontal_down(landmarks: list[Landmark]) -> bool:
    angle_5_17 = calculate_angle_2d(landmarks[5], landmarks[17])
    return int(angle_5_17) in range(-135, -45)


def is_thumb_open(landmarks: list[Landmark]) -> bool:
    angle_4_3_2 = calculate_angle_3d(landmarks[4], landmarks[3], landmarks[2])
    angle_4_2_0 = calculate_angle_3d(landmarks[4], landmarks[2], landmarks[0])
    return angle_4_3_2 > 150 and angle_4_2_0 > 150


def is_thumb_close(landmarks: list[Landmark]) -> bool:
    angle_4_3_2 = calculate_angle_3d(landmarks[4], landmarks[3], landmarks[2])
    angle_4_2_0 = calculate_angle_3d(landmarks[4], landmarks[2], landmarks[0])
    return angle_4_3_2 < 135 or angle_4_2_0 < 135


def is_index_open(landmarks: list[Landmark]) -> bool:
    angle_8_6_5 = calculate_angle_3d(landmarks[8], landmarks[6], landmarks[5])
    return angle_8_6_5 > 135


def is_index_close(landmarks: list[Landmark]) -> bool:
    distance_0_8 = calculate_distance(landmarks[0], landmarks[8])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_8 * 0.8 < distance_0_9


def is_middle_open(landmarks: list[Landmark]) -> bool:
    angle_12_10_9 = calculate_angle_3d(landmarks[12], landmarks[10], landmarks[9])
    return angle_12_10_9 > 135


def is_middle_close(landmarks: list[Landmark]) -> bool:
    distance_0_12 = calculate_distance(landmarks[0], landmarks[12])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_12 * 0.8 < distance_0_9


def is_ring_open(landmarks: list[Landmark]) -> bool:
    angle_16_14_13 = calculate_angle_3d(landmarks[16], landmarks[14], landmarks[13])
    return angle_16_14_13 > 135


def is_ring_close(landmarks: list[Landmark]) -> bool:
    distance_0_16 = calculate_distance(landmarks[0], landmarks[16])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_16 * 0.8 < distance_0_9


def is_pinky_open(landmarks: list[Landmark]) -> bool:
    angle_20_18_17 = calculate_angle_3d(landmarks[20], landmarks[18], landmarks[17])
    return angle_20_18_17 > 135


def is_pinky_close(landmarks: list[Landmark]) -> bool:
    distance_0_20 = calculate_distance(landmarks[0], landmarks[20])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_20 * 0.8 < distance_0_9
