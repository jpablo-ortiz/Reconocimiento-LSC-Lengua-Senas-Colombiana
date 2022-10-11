import os
from glob import glob

import tensorflow as tf

# ===========================================================
# PATH CONSTANTS
# ===========================================================

PATH_RAW_DATA = "../../data/raw/Signs"
PATH_PROCESSED_DATA = "../../data/processed/Signs"
PATH_PROCCESSED_TFDATASET = "../../data/processed_tfdataset/Signs"

# ===========================================================
# DATA AUGMENTATION Class
# ===========================================================


class DataAug:
    def __init__(
        self,
        path=PATH_RAW_DATA,
        normalize_images=True,
        grayscale=False,
        img_height=256,
        img_width=256,
        resize_images=False,
        single_transformations=[],
        general_transformation=None,
        separeted_transformations=[],
        defined_dataset=None,
    ):

        self.resize_images = resize_images
        self.path = path
        self.img_height = img_height
        self.img_width = img_width
        self.normalize_images = normalize_images
        self.grayscale = grayscale

        self.classes = None
        self.have_dataset = False
        self.single_transformations = single_transformations
        self.general_transformation = general_transformation
        self.separeted_transformations = separeted_transformations
        self.defined_dataset = defined_dataset

    # PRINCIPAL FUNCTION
    def generate_data_aug(self) -> tf.data.Dataset:

        dataset = self.defined_dataset

        if dataset is None:
            # Get the filename (with path) of each image
            filenames = glob(self.path + "/*/*.jpg")
            # Transform all \\ to / to avoid errors when extract labels
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

        combined_dataset = dataset

        if len(self.single_transformations) > 0:
            for cant_repetitions, transformation in self.single_transformations:
                transformed_datasets = []
                for _ in range(cant_repetitions):
                    temp = dataset.map(transformation, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                    transformed_datasets.append(temp)

                for temp in transformed_datasets:
                    combined_dataset = combined_dataset.concatenate(temp)

        if len(self.separeted_transformations) > 0:
            separated_datasets = []
            for cant_repetitions, transformation in self.separeted_transformations:
                for _ in range(cant_repetitions):
                    temp = dataset.map(transformation, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                    separated_datasets.append(temp)

            for ds in separated_datasets:
                combined_dataset = combined_dataset.concatenate(ds)

        dataset = combined_dataset

        if self.general_transformation is not None:
            combined_dataset = combined_dataset.map(
                self.general_transformation, num_parallel_calls=tf.data.experimental.AUTOTUNE
            )

        if self.normalize_images:
            combined_dataset = combined_dataset.map(
                lambda x, y: (tf.cast(x, tf.float32), y), num_parallel_calls=tf.data.experimental.AUTOTUNE
            )
        else:
            combined_dataset = combined_dataset.map(
                lambda x, y: (tf.cast(x, tf.uint8), y), num_parallel_calls=tf.data.experimental.AUTOTUNE
            )

        return combined_dataset

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

    def get_class_of_label(self, one_hot_label):
        classes = self.get_classes()
        return classes[one_hot_label.argmax()][1]

    def get_x_samples(self, dataset: tf.data.Dataset, samples=10, random=False, named_labels=True):
        temp = dataset
        if random:
            temp = temp.shuffle(buffer_size=1000, reshuffle_each_iteration=False)
        temp = list(temp.take(samples).as_numpy_iterator())
        # Is a list of tuples (image, label)
        # divided in two lists (images, labels)
        images, labels = list(zip(*temp))

        if named_labels:
            labels = [self.get_class_of_label(lbl) for lbl in labels]

        return list(images), list(labels)

    def save_dataset_jpg(self, dataset: tf.data.Dataset, path_to_save=PATH_PROCESSED_DATA, debug=False):
        counter = 1

        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        # Create the folders of the classes if they don't exist
        classes = self.get_classes()
        for _class in classes:
            class_path = os.path.join(path_to_save, _class[1])
            if not os.path.exists(class_path):
                os.makedirs(class_path)

        def encode(image, label, counter):
            # Denormalize image
            if isinstance(image, float):
                image = image * 255.0
            image = tf.cast(image, tf.uint8)
            image = tf.image.encode_jpeg(image, optimize_size=True, chroma_downsampling=False)
            # save image
            with tf.io.gfile.GFile(path_to_save + "/" + str(label) + "/" + str(counter) + ".jpg", "wb") as f:
                f.write(image.numpy())

        for image, label in dataset:
            if debug:
                print(counter)
            label = tf.argmax(label)
            label = classes[label][1]
            encode(image, label, counter)
            counter += 1

    def _save_dataset_optimized(self, dataset: tf.data.Dataset, path_to_save=PATH_PROCCESSED_TFDATASET):
        tf.data.experimental.save(dataset, path_to_save)

    # -------------------------------------------------------------------------------
    # Auxiliar methods
    # -------------------------------------------------------------------------------

    def _decode_image(self, filename):
        image = tf.io.read_file(filename)
        image = tf.image.decode_jpeg(image, channels=3)

        # Resize image
        if self.resize_images:
            image = tf.image.resize(image, [self.img_height, self.img_width])

        # Apply normalization (Allways at the end)
        if self.normalize_images:
            image = tf.image.per_image_standardization(image)

        return image

    def _apply_data_augmentation(self, image, label):
        return image, label
