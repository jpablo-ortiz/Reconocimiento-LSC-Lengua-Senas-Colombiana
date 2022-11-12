import math
import os
import random
from abc import ABCMeta, abstractmethod
from glob import glob

import tensorflow as tf

# Different types of datasets pipelines of sign images
# - SignDataset() ->tf.data.Dataset
#   - tf.data.Dataset.from_tensor_slices (with direct io)
#   - tf.data.Dataset.list_files
# - SignDatasetImageDatasetFromDirectory() -> tf.keras.preprocessing.image_dataset_from_directory
# - SignDatasetImageDataGenerator() =>tf.keras.preprocessing.image.ImageDataGenerator

# ===========================================================
# PATH CONSTANTS
# ===========================================================

PATH_RAW_DATA = "../../data/raw/Signs"
PATH_PROCESSED_DATA = "../../data/processed/Signs"

# ===========================================================
# Abstract class for sign datasets
# ===========================================================


class SignDatasetAbstract(metaclass=ABCMeta):
    def __init__(
        self,
        path=PATH_RAW_DATA,
        img_height=256,
        img_width=256,
        batch_size=32,
        shuffle=True,
        random_seed=None,
        optimizers=True,
        normalize_images=True,
        grayscale=False,
        use_cache=True,
        disable_repeate=False,
        defined_dataset=None,
    ):
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
        self.defined_dataset = defined_dataset
        self.disable_repeate = disable_repeate

    def _configure_for_performance(self, dataset: tf.data.Dataset):
        # Improve performance by cache and prefetching some batches (to allow batches use batch_size)
        # https://www.tensorflow.org/guide/data_performance

        # If you use cache, depending on the size of the dataset, you can saturate the RAM memory.
        # This cause that the system goes slow or freeze, but if you wait the system will recover.
        # The chache affects the performance of the first epoch, but improves the performance of the
        # following epochs.

        if self.use_cache:  # Cache the dataset to avoid re-reading the files
            dataset = dataset.cache()

        # Optimize the use of gpu and cpu
        dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

        return dataset

    def get_recomend_steps_per_epoch(self):
        # Variable to put on model.fit(steps_per_epoch=?)
        if self.steps_per_epoch is None:
            filenames = glob(self.path + "/*/*.jpg")
            self.steps_per_epoch = math.floor(len(filenames) / self.batch_size)
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

        return dataset.map(denormalization, num_parallel_calls=tf.dat3a.experimental.AUTOTUNE)

    def normalize_image(dataset: tf.data.Dataset):
        def normalization(image, label):
            return image / 255.0, label

        return dataset.map(normalization, num_parallel_calls=tf.data.experimental.AUTOTUNE)

    def load_dataset(path="../data/processed_tfdataset"):
        return tf.data.experimental.load(path)


# ===========================================================
# Class for sign datasets inherited from SignDatasetAbstract
# ===========================================================


class SignDataset(SignDatasetAbstract):
    def __init__(
        self,
        path=PATH_RAW_DATA,
        img_height=256,
        img_width=256,
        batch_size=32,
        shuffle=True,
        random_seed=None,
        optimizers=True,
        normalize_images=True,
        grayscale=False,
        use_cache=True,
        fastest_version=True,
        resize_images=True,
        disable_repeate=False,
        defined_dataset=None,
    ):
        super().__init__(
            path,
            img_height,
            img_width,
            batch_size,
            shuffle,
            random_seed,
            optimizers,
            normalize_images,
            grayscale,
            use_cache,
            disable_repeate,
            defined_dataset,
        )

        self.fastest_version = fastest_version
        self.resize_images = resize_images

        self.classes = None
        self.steps_per_epoch = None
        self.have_dataset = False

    def get_dataset(self) -> tf.data.Dataset:
        dataset = self.defined_dataset

        if dataset is None:
            # Get the filename (with path) of each image
            filenames = glob(self.path + "/*/*.jpg")
            # Transform all \\ to / to avoid errors when extract labels
            filenames = [filename.replace("\\", "/") for filename in filenames]
            if self.shuffle:
                self._shuffle_filenames(filenames)

            # Process the dataset generator
            if self.fastest_version:
                dataset = self._get_dataset_from_tensor_slices_version(filenames)
            else:
                dataset = self._get_dataset_list_files_version(filenames)
        else:
            self.have_dataset = True

        # If is defined_dataset apply previous transformations
        if self.defined_dataset is not None:
            # Resize image
            if self.resize_images:
                dataset = dataset.map(
                    lambda x, y: (
                        tf.cast(tf.image.resize(x, [self.img_height, self.img_width]), tf.uint8),
                        y,
                    ),
                    num_parallel_calls=tf.data.experimental.AUTOTUNE,
                )

            # Apply normalization (Allways at the end)
            if self.normalize_images and dataset.element_spec[0].dtype != tf.float32:
                dataset = dataset.map(
                    lambda x, y: (tf.cast(x, tf.float32) / 255.0, y),
                    num_parallel_calls=tf.data.experimental.AUTOTUNE,
                )

        if self.optimizers:
            # Perform shuffle, batch, repeat and prefetch
            dataset = self._configure_for_performance(dataset)

        return dataset

    # tf.data.Dataset.from_tensor_slices (with direct io)
    def _get_dataset_from_tensor_slices_version(self, filenames):
        # Get the respective label
        classes = self.get_classes()
        dict_classes = {_class: _label for _label, _class in classes}
        labels = [dict_classes[filename.split("/")[-2]] for filename in filenames]

        # Create a dataset of images (x) and labels (y) (y = a one_hot tensor) (from filenames and labels)
        filenames_dataset = tf.data.Dataset.from_tensor_slices(filenames)
        images_dataset = filenames_dataset.map(
            self._decode_image, num_parallel_calls=tf.data.experimental.AUTOTUNE
        )
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

        # dataset.repeat() will repeat the dataset indefinitely to prevent errors when running out of data.
        # This is why it is VERY IMPORTANT to set the steps_per_epoch parameter of the model.fit() method
        if not self.disable_repeate:
            dataset = dataset.repeat()

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
            image = tf.image.per_image_standardization(image)
        return image


class SignDatasetImageDatasetFromDirectory(SignDatasetAbstract):
    def __init__(
        self,
        path=PATH_RAW_DATA,
        img_height=256,
        img_width=256,
        batch_size=32,
        shuffle=True,
        random_seed=None,
        optimizers=True,
        normalize_images=True,
        grayscale=False,
        use_cache=True,
        crop_to_aspect_ratio=False,
    ):
        super().__init__(
            path,
            img_height,
            img_width,
            batch_size,
            shuffle,
            random_seed,
            optimizers,
            normalize_images,
            grayscale,
            use_cache,
        )

        self.crop_to_aspect_ratio = crop_to_aspect_ratio

        self.classes = None
        self.steps_per_epoch = None

    def get_dataset(self) -> tf.data.Dataset:
        dataset = tf.keras.utils.image_dataset_from_directory(
            self.path,
            labels="inferred",
            label_mode="categorical",
            color_mode="grayscale" if self.grayscale else "rgb",
            batch_size=self.batch_size if self.optimizers else None,
            image_size=(self.img_height, self.img_width),
            shuffle=self.shuffle,  # reshuffle_each_iteration=False compared with other techniques
            seed=self.random_seed,
            interpolation="bilinear",
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

        # dataset.repeat() will repeat the dataset indefinitely to prevent errors when running out of data.
        # This is why it is VERY IMPORTANT to set the steps_per_epoch parameter of the model.fit() method
        if not self.disable_repeate:
            dataset = dataset.repeat()

        return dataset


class SignDatasetImageDataGenerator(SignDatasetAbstract):
    def __init__(
        self,
        path=PATH_RAW_DATA,
        img_height=256,
        img_width=256,
        batch_size=32,
        shuffle=True,
        random_seed=None,
        optimizers=True,
        normalize_images=True,
        grayscale=False,
        crop_to_aspect_ratio=False,
        data_aug_save_dir=None,
        data_aug_save_prefix="",
        use_cache=True,
        data_aug_save_format="jpg",
        image_data_generator: tf.keras.preprocessing.image.ImageDataGenerator = None,
    ):
        super().__init__(
            path,
            img_height,
            img_width,
            batch_size,
            shuffle,
            random_seed,
            optimizers,
            normalize_images,
            grayscale,
            use_cache,
        )

        self.crop_to_aspect_ratio = crop_to_aspect_ratio
        self.data_aug_save_dir = data_aug_save_dir
        self.data_aug_save_prefix = data_aug_save_prefix
        self.data_aug_save_format = data_aug_save_format

        if image_data_generator is None:
            self.image_data_generator = tf.keras.preprocessing.image.ImageDataGenerator()
        else:
            self.image_data_generator = image_data_generator

        self.dataset = None
        self.classes = None
        self.steps_per_epoch = None

    def get_dataset(self) -> tf.data.Dataset:
        if self.normalize_images:
            self.image_data_generator.rescale = 1.0 / 255

        dataset = self.image_data_generator.flow_from_directory(
            self.path,
            classes=None,
            class_mode="categorical",
            color_mode="grayscale" if self.grayscale else "rgb",
            batch_size=self.batch_size if self.optimizers else None,
            target_size=(self.img_height, self.img_width),
            shuffle=self.shuffle,
            seed=self.random_seed,
            interpolation="nearest",
            keep_aspect_ratio=self.crop_to_aspect_ratio,
            save_to_dir=self.data_aug_save_dir,
            save_prefix=self.data_aug_save_prefix,
            save_format=self.data_aug_save_format,
        )

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

        return dataset
