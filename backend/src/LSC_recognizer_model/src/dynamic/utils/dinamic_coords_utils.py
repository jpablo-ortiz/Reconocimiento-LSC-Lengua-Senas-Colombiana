import os
from unicodedata import normalize

import numpy as np
from LSC_recognizer_model.src.dinamic.utils.video_utils import (
    change_fps_of_video,
    predict_video_seconds_dict,
    save_video_change_fps,
)


def generate_npy_files_from_video(
    filename,
    holistic,
    save_path_numpy: str = "",
    save_path_video_detection_draw: str = "",
    fps_expected=20,
):
    save_videos = save_path_video_detection_draw != ""
    save_results = save_path_numpy != ""

    try:
        # Process the video
        dict_seconds, width, height = change_fps_of_video(filename=filename, fps_expected=fps_expected)

        video_coords = predict_video_seconds_dict(
            holistic=holistic,
            seconds=dict_seconds,
            fps=fps_expected,
            used_parts=["pose", "right_hand", "left_hand", "face"],
        )

        # Get names of file
        signal_name = filename.split("/")[-2]  # Get the name of the signal
        video_name = filename.split("/")[-1]  # Get the name of the image
        video_name = video_name.split(".")[0]  # Remove the extension of the image
        video_name = video_name.split("_")[0]  # Remove the state of the image ej: 10_notprocessed.mp4

        # Delete from the name some characters that can cause problems
        trans_tab = dict.fromkeys(map(ord, "\u0301\u0308"), None)
        signal_name = normalize("NFKC", normalize("NFKD", signal_name).translate(trans_tab))
        video_name = normalize("NFKC", normalize("NFKD", video_name).translate(trans_tab))

        if save_videos:
            save_path = f"{save_path_video_detection_draw}/{signal_name}"
            save_video_change_fps(
                seconds_dict=dict_seconds,
                fps=fps_expected,
                save_path=save_path,
                video_name=video_name,
                width=width,
                height=height,
            )

        if save_results:
            array_to_save = np.array(video_coords, dtype=object)
            save_coordenates(
                coordenates=array_to_save,
                path=save_path_numpy,
                signal_name=signal_name,
                name=video_name,
            )

        return video_coords

    except Exception as error:
        print(f"Error con el video {filename}: {error}")
        return None


def save_coordenates(coordenates, path, signal_name, name):
    # Create folder if not exists
    folder = path + "/" + signal_name
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save coordenates
    with open(f"{path}/{signal_name}/{name}.npy", "wb") as f:
        np.save(f, coordenates)
