import cv2
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult

import thehand as th

detection_result = None

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)


def result_callback(result: HandLandmarkerResult):
    global detection_result
    detection_result = result

    if result.hand_world_landmarks:
        # print_inline(f"{len(result.hand_world_landmarks)} hand detected")
        if len(result.hand_world_landmarks) > 0:
            hand_landmarks = result.hand_world_landmarks

            for i, landmarks in enumerate(hand_landmarks):
                if len(landmarks) < 21:
                    continue

                # pos = th.get_hand_position_on_screen(result.hand_landmarks[i], 1980, 1080)
                # print(pos)

                res = th.is_hand_three(landmarks)
                print(res)


def draw(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]
        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend(
            [landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks]
        )
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style(),
        )

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(
            annotated_image,
            f"{handedness[0].category_name}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA,
        )

    return annotated_image


def main():
    state = th.State()
    state.hand_callback = result_callback

    camera = th.Camera()
    hand = th.HandLandmarker(state)

    while True:
        image = camera.read()

        if image is None:
            continue

        hand(image)

        if not detection_result:
            continue

        annotated_image = draw(image, detection_result)

        cv2.imshow("Hand", annotated_image)
        if cv2.waitKey(50) == 27:
            break


if __name__ == "__main__":
    main()
