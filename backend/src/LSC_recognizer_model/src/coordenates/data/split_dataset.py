import math
import multiprocessing as mp
import os
from glob import glob
from math import floor
from unicodedata import normalize

import cv2
import numpy as np
import tensorflow as tf
from utils.holistic.holistic_detector import HolisticDetector


class SplitDataset:
    def __init__(
        self,
        porcentage_train=0.8,
        porcentage_test=0.1,
        porcentage_validation=0.1,
        path_raw_image="",
        path_raw_numpy="",
    ):
        self.is_path_raw_image = path_raw_image != ""
        self.is_path_raw_numpy = path_raw_numpy != ""
        self.porcentage_train = porcentage_train
        self.porcentage_test = porcentage_test
        self.porcentage_validation = porcentage_validation
        self.classes = None
        self.steps_per_epoch = None

        self.path = path_raw_image if self.is_path_raw_image else path_raw_numpy
        self.extension = "jpg" if self.is_path_raw_image else "npy"

    def get_splited_files(
        self,
        save_path_numpy: str = "",
        save_path_image_detection_draw: str = "",
        image_single_aug=None,
        image_separated_aug=None,
        execute_in_parallel=False,
        cant_rotations_per_axie_data_aug=[0, 0, 0],
        x_max_rotation=30,
        y_max_rotation=45,
        z_max_rotation=20,
    ):
        if image_separated_aug is None:
            image_separated_aug = []

        save_results = save_path_numpy != ""
        save_images = save_path_image_detection_draw != ""

        if self.is_path_raw_numpy:
            if save_images:
                raise Exception("No se puede guardar imagenes cuando el path_raw_numpy esta definido")
            save_images = False

        count_image = 0

        # Create the object
        holistica = HolisticDetector()

        filenames = self.get_filepaths()

        # Get the respective label
        classes = self.get_classes()
        dict_classes = {_class: _label for _label, _class in classes}
        labels = [dict_classes[filename.split("/")[-2]] for filename in filenames]

        labels_dataset = tf.keras.utils.to_categorical(labels).astype(int)

        if execute_in_parallel:
            num_workers = mp.cpu_count() - 2
            pool = mp.Pool(num_workers)

        # Create a tuple of numpy array (x) and labels (y) (y is a one-hot encoded vector) (from filenames and labels)
        dataset_numpy = []
        dict_labels_dataset = {}
        for filename, label_hot, label in zip(filenames, labels_dataset, labels):
            if self.is_path_raw_numpy:
                try:
                    # Load the image
                    array = np.load(filename, allow_pickle=True)
                    array = array.tolist()

                    # Save the dataset (x, y)
                    dataset_numpy.append((array, label_hot))

                    # Dict with the labels
                    if label in dict_labels_dataset:
                        dict_labels_dataset[label].append((array, label_hot))
                    else:
                        dict_labels_dataset[label] = [(array, label_hot)]

                except Exception as error:
                    print(f"Error con el archivo {filename}: {error}")
            else:  # self.is_path_raw_image:
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
                    for fotograma in new_frames:
                        # Process the image
                        results = holistica.detect_holistic(fotograma)

                        # Simple verification to see if there is even a hand in the image
                        # if results.left_hand_landmarks is not None or results.right_hand_landmarks is not None:
                        if (
                            results.left_hand_landmarks is not None
                            or results.right_hand_landmarks is not None
                        ):
                            signal_name = filename.split("/")[-2]
                            name_image = filename.split("/")[-1].split(".")[0]

                            # Delete from the name some characters that can cause problems
                            trans_tab = dict.fromkeys(map(ord, "\u0301\u0308"), None)
                            signal_name = normalize(
                                "NFKC", normalize("NFKD", signal_name).translate(trans_tab)
                            )
                            name_image = normalize("NFKC", normalize("NFKD", name_image).translate(trans_tab))

                            # Save the image
                            if save_images:
                                name_image_iter = f"{count_image}-{signal_name}-({name_image})"
                                count_image += 1
                                image_pred = holistica.draw_prediction(fotograma, results)
                                self.save_image_prediction_draw(
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
                                (
                                    new_pose,
                                    new_right_hand,
                                    new_left_hand,
                                    new_face,
                                ) = holistica.get_unprocessed_coordenates(results)
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
                                ) = holistica.get_unproccesed_coordenates_data_aug(
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
                                    array_to_save = np.array(
                                        [pose, right_hand, left_hand, face], dtype=object
                                    )

                                    name_image_iter = f"{count_image}-{signal_name}-({name_image})"
                                    count_image += 1

                                    if execute_in_parallel:
                                        pool.apply_async(
                                            self.save_coordenates,
                                            args=(
                                                array_to_save,
                                                save_path_numpy,
                                                signal_name,
                                                name_image_iter,
                                            ),
                                        )
                                    else:
                                        self.save_coordenates(
                                            array_to_save, save_path_numpy, signal_name, name_image_iter
                                        )

                                # Save the dataset (x, y)
                                dataset_numpy.append(((pose, right_hand, left_hand, face), label_hot))

                                # Dict with the labels
                                if label in dict_labels_dataset:
                                    dict_labels_dataset[label].append(
                                        ((pose, right_hand, left_hand, face), label_hot)
                                    )
                                else:
                                    dict_labels_dataset[label] = [
                                        ((pose, right_hand, left_hand, face), label_hot)
                                    ]
                except Exception as error:
                    print(f"Error con la imagen {filename}: {error}")
        if execute_in_parallel:
            pool.close()
            pool.join()

        train, test, validation = [], [], []

        # Get equilibrated division
        for label, array in dict_labels_dataset.items():
            # Calculate the number of elements for each dataset
            len_dataset = len(array)
            len_train = floor(len_dataset * self.porcentage_train)
            len_test = floor(len_dataset * self.porcentage_test)
            # len_validation = floor(len_dataset * self.porcentage_validation)

            # Shuffle the dataset
            np.random.shuffle(array)

            # Split the dataset
            train.extend(array[:len_train])
            test.extend(array[len_train : len_train + len_test])
            validation.extend(array[len_train + len_test :])

        # Shuffle the dataset
        np.random.shuffle(train)
        np.random.shuffle(test)
        np.random.shuffle(validation)

        return train, test, validation

    def get_classes(self):
        if self.classes is None:
            # Get the classes from the folders names in the path
            classes = os.listdir(self.path)
            # All folders that begin with '.' are ignored
            classes = [_class for _class in classes if _class[0] != "."]
            self.classes = [(_label, _class) for _label, _class in enumerate(classes)]
        return self.classes

    def get_filepaths(self):
        # Get the filename (with path) of each image
        filenames = glob(self.path + f"/*/*.{self.extension}")
        # Transform all \\ to / to avoid errors when extract labels
        filenames = [filename.replace("\\", "/") for filename in filenames]
        return filenames

    def save_coordenates(self, coordenates, path, signal_name, name):
        # Create folder if not exists
        folder = path + "/" + signal_name
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save coordenates
        with open(f"{path}/{signal_name}/{name}.npy", "wb") as f:
            np.save(f, coordenates)

    def save_image_prediction_draw(self, image_pred, path, signal_name, name):
        # Create folder if not exists
        folder = path + "/" + signal_name
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save image
        cv2.imwrite(f"{path}/{signal_name}/{name}.jpg", image_pred)

    def get_recomend_steps_per_epoch(self, batch_size=32):
        if self.steps_per_epoch is None:
            filenames = glob(self.path + f"/*/*.{self.extension}")
            self.steps_per_epoch = math.ceil(len(filenames) / batch_size)
        return self.steps_per_epoch

    def get_only_specific_parts_and_fix(
        self, dataset, used_parts=["pose", "right_hand", "left_hand", "face"]
    ):
        x_dataset, y_dataset = zip(*dataset)

        used_parts_position = []
        if "pose" in used_parts:
            used_parts_position.append(0)
        if "right_hand" in used_parts:
            used_parts_position.append(1)
        if "left_hand" in used_parts:
            used_parts_position.append(2)
        if "face" in used_parts:
            used_parts_position.append(3)

        x_dataset_temp = []
        for x in x_dataset:
            x_dataset_temp.append(np.concatenate([x[i] for i in used_parts_position]))

        x_dataset = np.array(x_dataset_temp, dtype=np.float32)
        y_dataset = np.array(y_dataset, dtype=np.float32)

        return x_dataset, y_dataset
