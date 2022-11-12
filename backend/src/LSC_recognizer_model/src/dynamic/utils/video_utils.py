from math import ceil, floor

import cv2
import numpy as np

from utils.holistic.holistic_detector import HolisticDetector
from utils.landmarks.face_info import CANT_LANDMARKS_FACE
from utils.landmarks.hand_info import CANT_LANDMARKS_HAND
from utils.landmarks.pose_info import CANT_LANDMARKS_POSE


def change_fps_of_video(filename: str, fps_expected: int) -> tuple[dict, str, int, int]:
    """Function to change the fps of a video returning a dictionary with the seconds and the frames of each second

    Args:
        filename (str): path of the video
        fps_expected (int): fps that you want to have
            IMPORTANT: the fps_expected must be minor or equal to the original fps

    Returns:
        tuple[dict, str, int, int]: dictionary with the seconds and the frames of each second, video_name, width, height
    """

    # Read video
    video = cv2.VideoCapture(filename)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # Convert a video to fps_expected video

    # Divide each second by actual fps
    seconds = {}
    for i in range(total_frames):
        actual_second = floor(i / fps)
        ret, frame = video.read()
        if actual_second in seconds:
            seconds[actual_second].append(frame)
        else:
            seconds[actual_second] = [frame]

    # Delete frames to transform each second from fps to fps_expected
    if fps > fps_expected:
        for second in seconds:
            frames = seconds[second]
            if len(frames) < int(fps):
                cant_frames = ceil(
                    (len(frames) / fps) * fps_expected
                )  # Quantity of frames that will be on 1 second
                cant_frames_to_delete = len(frames) - cant_frames
                for i in range(cant_frames_to_delete):
                    frame_to_delete = i * ceil(len(frames) / cant_frames)
                    if frame_to_delete < len(frames):
                        del frames[frame_to_delete]
            else:
                for i in range(len(frames)):
                    if i % (len(frames) / fps_expected) != 0:
                        del frames[i]

    video.release()

    return seconds, width, height


def save_video_change_fps(seconds_dict, fps, video_name, save_path, width, height):
    extension = video_name.split(".")[-1]
    video_name = video_name.split(".")[0]
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*extension)
    full_path = f"{save_path}/{video_name}_{fps}fps.mp4"
    out = cv2.VideoWriter(full_path, fourcc, fps, (width, height))

    for second in seconds_dict:
        for frame in seconds_dict[second]:
            out.write(frame)

    out.release()


def predict_video_seconds_dict(
    seconds,
    fps,
    holistic=None,
    draw_landmarks_on_video=False,
    cv2_view_video=False,
    used_parts=["pose", "right_hand", "left_hand", "face"],
):
    if holistic is None:
        holistic = HolisticDetector()

    video_coords = []

    for second in seconds:
        for i, frame in enumerate(seconds[second]):
            # Make detections
            results = holistic.detect_holistic(frame)

            # Draw landmarks
            if draw_landmarks_on_video:
                frame = holistic.draw_prediction(frame, results)
                seconds[second][i] = frame

            pose, right_hand, left_hand, face = holistic.get_unprocessed_coordenates(results)
            # coords = get_only_specific_parts_and_fix_individual(
            #    parts=[pose, right_hand, left_hand, face],
            #    used_parts=used_parts,
            # )
            coords = [pose, right_hand, left_hand, face]
            video_coords.append(coords)

            if cv2_view_video:
                cv2.imshow("frame", frame)
                milliseconds_to_wait = int(100 / fps)
                if cv2.waitKey(milliseconds_to_wait) & 0xFF == ord("q"):
                    break

    # video_coords = np.array(video_coords)  # (total_frames, all_coords)

    if cv2_view_video:
        cv2.destroyAllWindows()

    return video_coords


def get_only_specific_parts_and_fix_video(
    dataset, used_parts=["pose", "right_hand", "left_hand", "face"], max_total_fps_video=100
):
    if len(dataset) == 0:
        return np.array([]), np.array([])

    x_dataset, y_dataset = zip(*dataset)

    used_parts_position = []
    zeros_parts = [
        np.zeros(CANT_LANDMARKS_POSE),
        np.zeros(CANT_LANDMARKS_HAND),
        np.zeros(CANT_LANDMARKS_HAND),
        np.zeros(CANT_LANDMARKS_FACE),
    ]

    if "pose" in used_parts:
        used_parts_position.append(0)
    if "right_hand" in used_parts:
        used_parts_position.append(1)
    if "left_hand" in used_parts:
        used_parts_position.append(2)
    if "face" in used_parts:
        used_parts_position.append(3)

    x_dataset_temp = []
    for video in x_dataset:
        sequence_temp = []
        # Get only the used parts
        for frame in video:
            sequence_temp.append(np.concatenate([frame[i] for i in used_parts_position]))

        to_fix = sequence_temp[-1]

        # Complete the frames with the final frame
        if len(video) < max_total_fps_video:
            for _ in range(max_total_fps_video - len(video)):
                sequence_temp.append(to_fix)
        elif len(video) > max_total_fps_video:
            sequence_temp = sequence_temp[:max_total_fps_video]

        # if len(video) < max_total_fps_video:
        #    for _ in range(max_total_fps_video - len(video)):
        #        sequence_temp.append(np.concatenate([zeros_parts[i] for i in used_parts_position]))

        # Append the video to the dataset
        x_dataset_temp.append(sequence_temp)

    x_dataset = np.array(x_dataset_temp, dtype=np.float32)
    y_dataset = np.array(y_dataset, dtype=np.float32)

    return x_dataset, y_dataset
