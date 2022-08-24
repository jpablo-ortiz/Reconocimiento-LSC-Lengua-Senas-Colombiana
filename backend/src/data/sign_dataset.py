import math
import os
import random
from abc import ABCMeta, abstractmethod
from glob import glob

import tensorflow as tf

# Different types of datasets pipelines of sign images
# - SignDataset() -> tf.data.Dataset
#   - tf.data.Dataset.from_tensor_slices (with direct io)
#   - tf.data.Dataset.list_files
# - SignDatasetImageDatasetFromDirectory() -> tf.keras.preprocessing.image_dataset_from_directory
# - SignDatasetImageDataGenerator() ->tf.keras.preprocessing.image.ImageDataGenerator

# ===========================================================
# Abstract class for sign datasets
# ===========================================================


class SignDatasetAbstract(metaclass=ABCMeta):
    def __init__(self, path='../../data/raw/Signs', img_height=256, img_width=256, batch_size=32,
                 shuffle=True, random_seed=None, optimizers=True, normalize_images=True, grayscale=False,
                 use_cache=True, cache_dir=''):
        self.path = path
        self.img_height = img_height
        self.img_width = img_width
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.random_seed = random_seed
        self.optimizers = optimizers
        self.normalize_images = normalize_images
        self.grayscale = grayscale
        self.use_cache = use_cache
        self.cache_dir = cache_dir

    def _configure_for_performance(self, dataset: tf.data.Dataset):
        # dataset.repeat() will repeat the dataset indefinitely to prevent errors when running out of data.
        # This is why it is VERY IMPORTANT to set the steps_per_epoch parameter of the model.fit() method
        dataset = dataset.repeat()

        # Improve performance by cache and prefetching some batches (to allow batches use batch_size)
        # https://www.tensorflow.org/guide/data_performance

        # There are 3 different cases for cache usage:
        # 1. cache() -> When the size of the dataset does not exceed the available RAM memory, otherwise...
        # 2. cache(filename) -> Save the cache to a file on the disk memory. This method fills up a lot
        #    of disk memory, and it's so slow on the firts epoch, but improve a lot the following epochs.
        # 3. If the above conditions are not met, don't use cache()

        if self.use_cache:  # Cache the dataset to avoid re-reading the files
            if self.cache_dir != '':
                dataset = dataset.cache(self.cache_dir)
            else:
                dataset = dataset.cache()

        # Optimize the use of gpu and cpu
        dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        return dataset

    def get_recomend_steps_per_epoch(self):
        # Variable to put on model.fit(steps_per_epoch=?)
        if self.steps_per_epoch is None:
            filenames = glob(self.path + '/*/*.jpg')
            self.steps_per_epoch = math.ceil(len(filenames) / self.batch_size)
        return self.steps_per_epoch

    # -----------------------------------------------------------
    # Abstract methods for sign datasets
    # -----------------------------------------------------------

    @abstractmethod
    def get_dataset(self) -> tf.data.Dataset:
        pass

    # -----------------------------------------------------------
    # Static methods for sign datasets
    # -----------------------------------------------------------

    def denormalize_image(dataset: tf.data.Dataset):
        def denormalization(image, label):
            return image * 255.0, label
        return dataset.map(denormalization, num_parallel_calls=tf.data.experimental.AUTOTUNE)

    def normalize_image(dataset: tf.data.Dataset):
        def normalization(image, label):
            return image / 255.0, label
        return dataset.map(normalization, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    

# ===========================================================
# Class for sign datasets inherited from SignDatasetAbstract
# ===========================================================


class SignDataset(SignDatasetAbstract):
    def __init__(self, path='../../data/raw/Señas', img_height=256, img_width=256, batch_size=32,
                 shuffle=True, random_seed=None, optimizers=True, normalize_images=True, grayscale=False,
                 use_cache=True, cache_dir='', fastest_version=True, resize_images=True):
        super().__init__(path, img_height, img_width, batch_size, shuffle, random_seed,
                         optimizers, normalize_images, grayscale, use_cache, cache_dir)

        self.fastest_version = fastest_version
        self.resize_images = resize_images

        self.classes = None
        self.steps_per_epoch = None

    def get_dataset(self) -> tf.data.Dataset:
        dataset = None

        # Get the filename (with path) of each image
        filenames = glob(self.path + '/*/*.jpg')
        if self.shuffle:
            self._shuffle_filenames(filenames)

        # Process the dataset generator
        if self.fastest_version:
            dataset = self._get_dataset_from_tensor_slices_version(filenames)
        else:
            dataset = self._get_dataset_list_files_version(filenames)

        if self.optimizers:
            # Perform shuffle, batch, repeat and prefetch
            dataset = self._configure_for_performance(dataset)

        return dataset

    # tf.data.Dataset.from_tensor_slices (with direct io)
    def _get_dataset_from_tensor_slices_version(self, filenames):
        # Get the respective label
        classes = self.get_classes()
        dict_classes = {_class: _label for _label, _class in classes}
        labels = [dict_classes[filename.split('/')[-2]] for filename in filenames]

        # Create a dataset of images (x) and labels (y) (y = a one_hot tensor) (from filenames and labels)
        filenames_dataset = tf.data.Dataset.from_tensor_slices(filenames)
        images_dataset = filenames_dataset.map(
            self._decode_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        labels_dataset = tf.keras.utils.to_categorical(labels)  # To one hot vector
        labels_dataset = tf.data.Dataset.from_tensor_slices(labels_dataset)
        dataset = tf.data.Dataset.zip((images_dataset, labels_dataset))  # Zip the two datasets

        return dataset

    def _get_dataset_list_files_version(self, filenames):  # tf.data.Dataset.list_files
        def get_label(file_path):
            # Get classes from the folders names in the path
            classes = self.get_classes()
            classes = [_class for i, _class in classes]

            # Divide the path into parts
            part = tf.strings.split(file_path, os.path.sep)
            part = part[-2]
            one_hot = part == classes
            # To one hot vector
            to_number = tf.argmax(one_hot)
            label = tf.one_hot(to_number, len(classes))
            return label

        def process_path(file_path):
            label = y = get_label(file_path)
            image = x = self._decode_image(file_path)
            return x, y

        # Create a dataset of images (x) and labels (y) (y = a one_hot tensor)
        dataset = tf.data.Dataset.list_files(file_pattern=filenames, shuffle=self.shuffle)
        dataset = dataset.map(process_path, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        return dataset

    def get_classes(self):
        if self.classes is None:
            # Get the classes from the folders names in the path
            classes = os.listdir(self.path)
            # All folders that begin with '.' are ignored
            classes = [_class for _class in classes if _class[0] != '.']
            self.classes = [(_label, _class) for _label, _class in enumerate(classes)]
        return self.classes

    # -------------------------------------------------------------------------------
    # Auxiliar methods
    # -------------------------------------------------------------------------------

    def _configure_for_performance(self, dataset: tf.data.Dataset):
        # Configure options for the dataset
        if self.shuffle:
            dataset = dataset.shuffle(buffer_size=1000, reshuffle_each_iteration=True)
        dataset = dataset.batch(self.batch_size)

        # Configure extra options to improve the performance
        dataset = super()._configure_for_performance(dataset)

        return dataset

    def _shuffle_filenames(self, filenames):
        if self.random_seed is not None:
            random.Random(self.random_seed).shuffle(filenames)
        else:
            random.shuffle(filenames)

    def _decode_image(self, filename):
        image = tf.io.read_file(filename)
        image = tf.image.decode_jpeg(image, channels=3)
        if self.grayscale:
            image = tf.image.rgb_to_grayscale(image)
        if self.resize_images:
            image = tf.image.resize(image, [self.img_height, self.img_width])
        if self.normalize_images:
            image = image / 255.0
        return image


class SignDatasetImageDatasetFromDirectory(SignDatasetAbstract):
    def __init__(self, path='../../data/raw/Señas', img_height=256, img_width=256, batch_size=32,
                 shuffle=True, random_seed=None, optimizers=True, normalize_images=True, grayscale=False,
                 use_cache=True, cache_dir='', crop_to_aspect_ratio=False):
        super().__init__(path, img_height, img_width, batch_size, shuffle, random_seed,
                         optimizers, normalize_images, grayscale, use_cache, cache_dir)

        self.crop_to_aspect_ratio = crop_to_aspect_ratio

        self.classes = None
        self.steps_per_epoch = None

    def get_dataset(self) -> tf.data.Dataset:
        dataset = tf.keras.utils.image_dataset_from_directory(
            self.path,
            labels='inferred',
            label_mode='categorical',
            color_mode='grayscale' if self.grayscale else 'rgb',
            batch_size=self.batch_size if self.optimizers else None,
            image_size=(self.img_height, self.img_width),
            shuffle=self.shuffle,  # reshuffle_each_iteration=False compared with other techniques
            seed=self.random_seed,
            interpolation='bilinear',
            crop_to_aspect_ratio=self.crop_to_aspect_ratio,
        )

        if self.normalize_images:
            dataset = SignDatasetAbstract.normalize_image(dataset)

        if self.optimizers:
            # Perform shuffle, batch, repeat and prefetch
            dataset = self._configure_for_performance(dataset)

        self.dataset = dataset
        return self.dataset

    def get_classes(self) -> list:
        if self.classes is None:
            self.classes = self.dataset.class_names
        return self.classes

    # -------------------------------------------------------------------------------
    # Auxiliar methods
    # -------------------------------------------------------------------------------

    def _configure_for_performance(self, dataset: tf.data.Dataset):
        # Configure options for the dataset
        if self.shuffle:
            dataset = dataset.shuffle(buffer_size=1000, reshuffle_each_iteration=True)

        # Configure extra options to improve the performance
        dataset = super()._configure_for_performance(dataset)

        return dataset

