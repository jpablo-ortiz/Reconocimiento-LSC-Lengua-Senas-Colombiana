import math
from math import floor

import numpy as np
import tensorflow as tf

from LSC_recognizer_model.src.utils.sign_utils import (
    generate_npy_files_from_image,
    get_classes,
    get_filepaths,
)
from utils.holistic.holistic_detector import HolisticDetector


class SplitDataset:
    def __init__(
        self,
        porcentage_train=0.8,
        porcentage_test=0.1,
        porcentage_validation=0.1,
        path_raw_image="",
        path_numpy="",
    ):
        self.is_path_raw_image = path_raw_image != ""
        self.is_path_numpy = path_numpy != ""
        self.porcentage_train = porcentage_train
        self.porcentage_test = porcentage_test
        self.porcentage_validation = porcentage_validation
        self.classes = None
        self.steps_per_epoch = None

        self.path = path_raw_image if self.is_path_raw_image else path_numpy
        self.extension = "jpg" if self.is_path_raw_image else "npy"

    def get_splited_files(
        self,
        save_path_numpy: str = "",
        save_path_image_detection_draw: str = "",
        image_single_aug=None,
        image_separated_aug=None,
        cant_rotations_per_axie_data_aug=[0, 0, 0],
        x_max_rotation=30,
        y_max_rotation=45,
        z_max_rotation=20,
    ):
        if image_separated_aug is None:
            image_separated_aug = []

        save_images = save_path_image_detection_draw != ""

        if self.is_path_numpy:
            if save_images:
                raise Exception("No se puede guardar imagenes cuando el path_numpy esta definido")
            save_images = False

        # Create the object
        holistic = HolisticDetector()
        filenames = get_filepaths(self.path, self.extension)

        # Get the respective label
        classes = self.get_classes()
        dict_classes = {_class: _label for _label, _class in classes}
        labels = [dict_classes[filename.split("/")[-2]] for filename in filenames]
        labels_dataset = tf.keras.utils.to_categorical(labels).astype(int)

        dataset_numpy = []
        dict_labels_dataset = {}

        list_of_failed_images = []
        list_of_error_images = []
        list_of_correct_images = []

        # Create a tuple of numpy array (x) and labels (y) (y is a one-hot encoded vector) (from filenames and labels)
        for filename, label_hot, label in zip(filenames, labels_dataset, labels):
            if self.is_path_numpy:
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
                list_landmarks_per_new_coord = generate_npy_files_from_image(
                    filename=filename,
                    holistic=holistic,
                    save_path_numpy=save_path_numpy,
                    save_path_image_detection_draw=save_path_image_detection_draw,
                    image_single_aug=image_single_aug,
                    image_separated_aug=image_separated_aug,
                    cant_rotations_per_axie_data_aug=cant_rotations_per_axie_data_aug,
                    x_max_rotation=x_max_rotation,
                    y_max_rotation=y_max_rotation,
                    z_max_rotation=z_max_rotation,
                )

                if len(list_landmarks_per_new_coord) == 0:
                    list_of_failed_images.append(filename)
                elif list_landmarks_per_new_coord is None:
                    list_of_error_images.append(filename)
                else:
                    list_of_correct_images.append(filename)

                for pose, right_hand, left_hand, face in list_landmarks_per_new_coord:
                    # Save the dataset (x, y)
                    dataset_numpy.append(((pose, right_hand, left_hand, face), label_hot))

                    # Dict with the labels
                    if label in dict_labels_dataset:
                        dict_labels_dataset[label].append(((pose, right_hand, left_hand, face), label_hot))
                    else:
                        dict_labels_dataset[label] = [((pose, right_hand, left_hand, face), label_hot)]

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

        return train, test, validation, (list_of_failed_images, list_of_error_images, list_of_correct_images)

    def get_classes(self):
        if self.classes is None:
            self.classes = get_classes(self.path)
        return self.classes

    def get_recomend_steps_per_epoch(self, batch_size=32):
        if self.steps_per_epoch is None:
            filenames = get_filepaths(self.path, self.extension)
            self.steps_per_epoch = math.floor(len(filenames) / batch_size)
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
