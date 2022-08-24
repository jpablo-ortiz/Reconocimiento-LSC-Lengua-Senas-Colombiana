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
    
