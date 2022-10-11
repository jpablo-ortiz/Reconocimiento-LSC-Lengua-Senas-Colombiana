import os
from glob import glob
from math import floor

import tensorflow as tf

# ===========================================================
# PATH CONSTANTS
# ===========================================================

PATH_RAW_DATA = "../../data/raw/Signs"
PATH_PROCESSED_DATA = "../../data/processed/Signs"

# ===========================================================
# SPLIT DATASET Class
# ===========================================================


class SplitDataset:
    def __init__(
        self,
        path=PATH_RAW_DATA,
        defined_dataset=None,
        porcentage_train=0.8,
        porcentage_test=0.1,
        porcentage_validation=0.1,
    ):
        # It is recommended that the defined_dataset be "clean", without any transformation,
        # optimizations as batching, prefetching, cache, shuffle, etc.
        self.path = path
        self.defined_dataset = defined_dataset
        self.porcentage_train = porcentage_train
        self.porcentage_test = porcentage_test
        self.porcentage_validation = porcentage_validation
        self.have_dataset = False
        self.classes = None

    def get_datasets(self):
        dataset = self.defined_dataset

        if dataset is None:
            # Get the filename (with path) of each image
            filenames = glob(self.path + "/*/*.jpg")
            # Transdorm all \\ to / to avoid errors when extract labels
            filenames = [filename.replace("\\", "/") for filename in filenames]

            # Get the respective label
            classes = self.get_classes()
            dict_classes = {_class: _label for _label, _class in classes}
            labels = [dict_classes[filename.split("/")[-2]] for filename in filenames]

            # Create a dataset of images (x) and labels (y) (y = a one_hot tensor) (from filenames and labels)
            filenames_dataset = tf.data.Dataset.from_tensor_slices(filenames)  # .take(1)
            images_dataset = filenames_dataset.map(
                self._decode_image, num_parallel_calls=tf.data.experimental.AUTOTUNE
            )

            labels_dataset = tf.keras.utils.to_categorical(labels)  # To one hot vector
            labels_dataset = tf.data.Dataset.from_tensor_slices(labels_dataset)

            dataset = tf.data.Dataset.zip((images_dataset, labels_dataset))
            # dataset = dataset.repeat(self.num_new_images_per_image)
        else:
            self.have_dataset = True

        # Shuffle the dataset before split
        buffer_size = int(100 * len(dataset))
        dataset = dataset.shuffle(buffer_size=buffer_size)

        # Calculate the number of images for each dataset
        len_dataset = len(dataset)
        len_train = floor(len_dataset * self.porcentage_train)
        len_test = floor(len_dataset * self.porcentage_test)
        len_validation = floor(len_dataset * self.porcentage_validation)

        leaftover_data = len_dataset - (len_train + len_test + len_validation)
        len_validation += leaftover_data

        # Split the dataset in train, test and validation
        dataset_train = dataset.take(len_train)
        dataset_test = dataset.skip(len_train).take(len_test)
        dataset_validation = dataset.skip(
            len_train + len_test
        )  # .take(len_validation) # Take is not necessary, only take the rest of the dataset

        return dataset_train, dataset_test, dataset_validation

    def get_classes(self):
        if self.have_dataset:
            print(
                "Advertencia: se ingresó un dataset previamente creado, por lo cual las clases que se obtienen del path pueden no ser las correctas"
            )
        if self.classes is None:
            # Get the classes from the folders names in the path
            classes = os.listdir(self.path)
            # All folders that begin with '.' are ignored
            classes = [_class for _class in classes if _class[0] != "."]
            self.classes = [(_label, _class) for _label, _class in enumerate(classes)]
        return self.classes

    def _decode_image(self, filename):
        image = tf.io.read_file(filename)
        image = tf.image.decode_jpeg(image, channels=3)
        return image
