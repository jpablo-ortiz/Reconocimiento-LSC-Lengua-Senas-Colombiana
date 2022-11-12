import os
from glob import glob
from unicodedata import normalize

import cv2
import numpy as np


def generate_npy_files_from_image(
    filename,
    holistic,
    save_path_numpy: str = "",
    save_path_image_detection_draw: str = "",
    image_single_aug=None,
    image_separated_aug=None,
    cant_rotations_per_axie_data_aug=[0, 0, 0],
    x_max_rotation=30,
    y_max_rotation=45,
    z_max_rotation=20,
):
    save_images = save_path_image_detection_draw != ""
    save_results = save_path_numpy != ""

    count_image = 0
    list_landmarks_per_new_coord = []
    try:
        # Load the image
        frame = cv2.imread(filename)

        # Do data augmentation and iterate over the generated images
        new_frames = [frame]

        # Single image augmentation
        if image_single_aug is not None:
            transformation = image_single_aug[1]
            for _ in range(image_single_aug[0]):
                new_frames.append(transformation(frame))

        # Separated image augmentation
        temp_frames = [f for f in new_frames]
        if len(image_separated_aug) > 0:
            for cant_repetitions, transformation in image_separated_aug:
                for _ in range(cant_repetitions):
                    for image in temp_frames:
                        new_frames.append(transformation(image))

        # Convert all images to numpy array
        for frame_iter in new_frames:
            # Process the image
            results = holistic.detect_holistic(frame_iter)

            # Simple verification to see if there is even a hand in the image
            # if results.left_hand_landmarks is not None or results.right_hand_landmarks is not None:
            if results.left_hand_landmarks is not None or results.right_hand_landmarks is not None:
                signal_name = filename.split("/")[-2]  # Get the name of the signal
                name_image = filename.split("/")[-1]  # Get the name of the image
                name_image = name_image.split(".")[0]  # Remove the extension of the image
                name_image = name_image.split("_")[
                    0
                ]  # Remove the state of the image ej: 10_notprocessed.jpg -> 10

                # Delete from the name some characters that can cause problems
                trans_tab = dict.fromkeys(map(ord, "\u0301\u0308"), None)
                signal_name = normalize("NFKC", normalize("NFKD", signal_name).translate(trans_tab))
                name_image = normalize("NFKC", normalize("NFKD", name_image).translate(trans_tab))

                # Save the image
                if save_images:
                    name_image_iter = f"{name_image}-{count_image}"
                    image_pred = holistic.draw_prediction(frame_iter, results)
                    save_image_prediction_draw(
                        image_pred,
                        save_path_image_detection_draw,
                        signal_name,
                        name_image_iter,
                    )

                if all(
                    [
                        cant_rotations_per_axie == 0
                        for cant_rotations_per_axie in cant_rotations_per_axie_data_aug
                    ]
                ):
                    new_pose, new_right_hand, new_left_hand, new_face = holistic.get_unprocessed_coordenates(
                        results
                    )
                    new_poses = [new_pose]
                    new_right_hands = [new_right_hand]
                    new_left_hands = [new_left_hand]
                    new_faces = [new_face]
                else:
                    # Get all
                    (
                        new_poses,
                        new_right_hands,
                        new_left_hands,
                        new_faces,
                    ) = holistic.get_unproccesed_coordenates_data_aug(
                        result=results,
                        # used_parts = used_parts,
                        x_max_rotation=x_max_rotation,
                        y_max_rotation=y_max_rotation,
                        z_max_rotation=z_max_rotation,
                        axies_to_rotate=["x", "y", "z"],
                        cant_rotations_per_axis=cant_rotations_per_axie_data_aug,
                    )

                for pose, right_hand, left_hand, face in zip(
                    new_poses, new_right_hands, new_left_hands, new_faces
                ):
                    # Save all the new coords data augmentation
                    if save_results:
                        array_to_save = np.array([pose, right_hand, left_hand, face], dtype=object)

                        name_image_iter = f"{name_image}-{count_image}"
                        count_image += 1

                        save_coordenates(array_to_save, save_path_numpy, signal_name, name_image_iter)

                    list_landmarks_per_new_coord.append((pose, right_hand, left_hand, face))
            else:
                print(f"En la imagen {filename} no se pudo detectar ambas manos")

        return list_landmarks_per_new_coord
    except Exception as error:
        print(f"Error con la imagen {filename}: {error}")
        return None


def save_coordenates(coordenates, path, signal_name, name):
    # Create folder if not exists
    folder = path + "/" + signal_name
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save coordenates
    with open(f"{path}/{signal_name}/{name}.npy", "wb") as f:
        np.save(f, coordenates)


def save_image_prediction_draw(image_pred, path, signal_name, name):
    # Create folder if not exists
    folder = path + "/" + signal_name
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save image
    cv2.imwrite(f"{path}/{signal_name}/{name}.jpg", image_pred)


def get_classes(path):
    # Get the classes from the folders names in the path
    classes = os.listdir(path)
    # All folders that begin with '.' are ignored
    classes = [_class for _class in classes if _class[0] != "."]
    classes = [(_label, _class) for _label, _class in enumerate(classes)]
    return classes


def get_filepaths(path, extension):
    # Get the filename (with path) of each image
    filenames = glob(path + f"/*/*.{extension}")
    # Transform all \\ to / to avoid errors when extract labels
    filenames = [filename.replace("\\", "/") for filename in filenames]
    return filenames
