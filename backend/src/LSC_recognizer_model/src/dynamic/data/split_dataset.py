import math
from math import floor

import numpy as np
import tensorflow as tf
from LSC_recognizer_model.src.coordenates.utils.sign_utils import get_classes, get_filepaths
from LSC_recognizer_model.src.dinamic.utils.dinamic_coords_utils import generate_npy_files_from_video
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
        self.extension = "mp4" if self.is_path_raw_image else "npy"

    def get_splited_files(
        self,
        save_path_numpy: str = "",
        save_path_image_detection_draw: str = "",
    ):
        save_images = save_path_image_detection_draw != ""

        if self.is_path_raw_numpy:
            if save_images:
                raise Exception("No se puede guardar imagenes cuando el path_raw_numpy esta definido")
            save_images = False

        # Create the object
        holistic = HolisticDetector()

        filenames = get_filepaths(self.path, self.extension)
        if self.extension == "mp4":
            filenames = get_filepaths(self.path, "m4v") + filenames  # m4v

        # Get the respective label
        classes = self.get_classes()
        dict_classes = {_class: _label for _label, _class in classes}
        labels = [dict_classes[filename.split("/")[-2]] for filename in filenames]
        labels_dataset = tf.keras.utils.to_categorical(labels).astype(int)

        dataset_numpy = []
        dict_labels_dataset = {}

        list_of_error_videos = []
        list_of_correct_videos = []

        # Create a tuple of numpy array (x) and labels (y) (y is a one-hot encoded vector) (from filenames and labels)
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
                video_coords = generate_npy_files_from_video(
                    filename=filename,
                    holistic=holistic,
                    save_path_numpy=save_path_numpy,
                    save_path_video_detection_draw=save_path_image_detection_draw,
                    fps_expected=20,
                )

                if video_coords is None:
                    list_of_error_videos.append(filename)
                else:
                    list_of_correct_videos.append(filename)

                # Save the dataset (x, y)
                dataset_numpy.append((video_coords, label_hot))

                # Dict with the labels
                if label in dict_labels_dataset:
                    dict_labels_dataset[label].append((video_coords, label_hot))
                else:
                    dict_labels_dataset[label] = [(video_coords, label_hot)]

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

        return train, test, validation, (list_of_error_videos, list_of_correct_videos)

    def get_classes(self):
        if self.classes is None:
            self.classes = get_classes(self.path)
        return self.classes

    def get_recomend_steps_per_epoch(self, batch_size=32):
        if self.steps_per_epoch is None:
            filenames = get_filepaths(self.path, self.extension)
            self.steps_per_epoch = math.ceil(len(filenames) / batch_size)
        return self.steps_per_epoch
