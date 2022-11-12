import os
import random
from datetime import datetime

import cv2
from keras.callbacks import ModelCheckpoint, TensorBoard

from controllers.signal_controller import SignalController
from LSC_recognizer_model.src.coordenates.data.split_dataset import SplitDataset
from LSC_recognizer_model.src.coordenates.models.callbacks import SaveResultsOnDatabaseCallback
from LSC_recognizer_model.src.utils.sign_model import SignModel
from LSC_recognizer_model.src.utils.sign_utils import generate_npy_files_from_image, get_filepaths
from models.model_variables import ModelVariables, TrainingState
from repositories.model_repository import ModelRepository, ModelRepositoryTinyDB
from settings import INPUT, PATH_MODELS, PATH_NUMPY_COORDS, PATH_RAW_SIGNS, neuronal_network
from utils.holistic.holistic_detector import HolisticDetector


class ModelController:
    def __init__(self, model_repository: ModelRepository, signal_controller: SignalController):
        self.model_repository = model_repository
        self.signal_controller = signal_controller

    def get_training_info(self, id_training: int):
        return self.model_repository.get_training_info(id_training)

    def get_training_info_actual(self):
        return self.model_repository.get_training_info_actual()

    def process_images_not_processed(self):
        # -----------------------------------------------
        # Data augmentation Functions to apply to the images
        # -----------------------------------------------
        def single_aug(image):
            image = cv2.flip(image, 1)
            return image

        def rotation(image, angle):
            angle = int(random.uniform(-angle, angle))
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((int(w / 2), int(h / 2)), angle, 1)
            image = cv2.warpAffine(image, M, (w, h))
            return image

        def zoom(img, value):
            def fill(img, h, w):
                img = cv2.resize(img, (h, w), cv2.INTER_CUBIC)
                return img

            if value > 1 or value < 0:
                print("Value for zoom should be less than 1 and greater than 0")
                return img

            value = random.uniform(value, 1)
            h, w = img.shape[:2]
            h_taken = int(value * h)
            w_taken = int(value * w)
            h_start = random.randint(0, h - h_taken)
            w_start = random.randint(0, w - w_taken)
            img = img[h_start : h_start + h_taken, w_start : w_start + w_taken, :]
            img = fill(img, h, w)
            return img

        image_single_aug = (1, single_aug)
        image_separated_aug = [
            (3, lambda image: rotation(image, 10)),
            (3, lambda image: zoom(image, 0.5)),
        ]

        # -----------------------------------------------
        # Process all notprocessed and error images
        # -----------------------------------------------
        holistic = HolisticDetector()

        list_of_failed_images = []
        list_of_error_images = []
        list_of_correct_images = []

        filenames = get_filepaths(PATH_RAW_SIGNS, "jpg")

        for filename in filenames:
            # If the image is not processed or failed, process it
            if "notprocessed" in filename or "error" in filename:
                list_landmarks_per_new_coord = generate_npy_files_from_image(
                    filename=filename,
                    holistic=holistic,
                    save_path_numpy=PATH_NUMPY_COORDS,
                    # save_path_image_detection_draw = PATH_PREDICTED_IMG,
                    image_single_aug=image_single_aug,
                    image_separated_aug=image_separated_aug,
                    # TODO: When the data augmentation is tested, use cant_rotations_per_axie_data_aug
                    # cant_rotations_per_axie_data_aug=[2, 2, 2]
                    x_max_rotation=25,
                    y_max_rotation=40,
                    z_max_rotation=20,
                )

                if len(list_landmarks_per_new_coord) == 0:
                    list_of_failed_images.append(filename)
                elif list_landmarks_per_new_coord is None:
                    list_of_error_images.append(filename)
                else:
                    list_of_correct_images.append(filename)

        for correct_image in list_of_correct_images:
            temp_name_image = correct_image.replace("notprocessed", "processed")
            temp_name_image = temp_name_image.replace("error", "processed")
            os.rename(correct_image, temp_name_image)
        for failed_image in list_of_failed_images:
            temp_name_image = failed_image.replace("notprocessed", "failed")
            temp_name_image = temp_name_image.replace("error", "failed")
            os.rename(failed_image, temp_name_image)
        for error_image in list_of_error_images:
            temp_name_image = error_image.replace("notprocessed", "error")
            os.rename(error_image, temp_name_image)

        # Before processing the images, we can verify that all signs are processed
        self.signal_controller.update_all_signals_to_processed()

    async def train_model(self, epoch: int, callback_variable: ModelVariables):
        try:
            signals_with_unprocessed_images = self.signal_controller.get_signals_with_unprocessed_images()

            if len(signals_with_unprocessed_images) > 0:
                print("Processing images...")
                self.process_images_not_processed()

            _ = self.train_model_process(epoch, callback_variable)
        except Exception:
            callback_variable.training_state = TrainingState.ERROR
            self.callback_update(callback_variable)

    def train_model_process(self, epochs: int, model_variables: ModelVariables):
        # -----------------------------------------------
        # Split Dataset Layer (Train, Test, Validation)
        # -----------------------------------------------

        print("Loading dataset...")
        split_dataset = SplitDataset(path_numpy=PATH_NUMPY_COORDS)
        train, test, validation, _ = split_dataset.get_splited_files()

        # FIX data
        print("Fixing data...")
        X_train, Y_train = split_dataset.get_only_specific_parts_and_fix(
            train, used_parts=["pose", "left_hand", "right_hand"]
        )
        X_test, Y_test = split_dataset.get_only_specific_parts_and_fix(
            test, used_parts=["pose", "left_hand", "right_hand"]
        )
        X_validation, Y_validation = split_dataset.get_only_specific_parts_and_fix(
            validation, used_parts=["pose", "left_hand", "right_hand"]
        )

        # -----------------------------------------------
        # Model Layer
        # -----------------------------------------------

        # 1. Create Model layer and define hyperparameters
        steps_per_epoch = split_dataset.get_recomend_steps_per_epoch()
        classes = split_dataset.get_classes()
        model_variables.trained_signals = {str(c[0]): c[1] for c in classes}

        modelo = SignModel(
            model=neuronal_network(INPUT, len(classes)),
            dataset_train=None,
            dataset_validation=None,
            X_train=X_train,
            Y_train=Y_train,
            X_validation=X_validation,
            Y_validation=Y_validation,
        )

        # 2. Define callbacks
        PATH_CHECKPOINTS_SAVE = os.path.join(PATH_MODELS, model_variables.name)
        print("Saving checkpoints in: ", PATH_CHECKPOINTS_SAVE)
        monitor_value = "val_loss"
        mode = "min" if monitor_value == "val_loss" else "max"

        # ============ TensorBoard ============
        # To open tensorboard: tensorboard --logdir=. on the folder where the logs are.
        log_dir = f"{PATH_CHECKPOINTS_SAVE}/logs"
        tb_callback = TensorBoard(log_dir=log_dir)

        # ============ Checkpoints ============
        model_dir = f"{PATH_CHECKPOINTS_SAVE}/weights.hdf5"
        checkpoint = ModelCheckpoint(
            filepath=model_dir, monitor=monitor_value, verbose=1, save_best_only=True, mode=mode
        )

        # ========== Callbacks list ============
        callbacks_list = [
            checkpoint,
            tb_callback,
            SaveResultsOnDatabaseCallback(ModelRepositoryTinyDB(), epochs, model_variables, monitor_value)
        ]

        # 3. Train model

        print("Training model...")
        modelo.train_model(
            epochs=epochs,
            optimizer="Adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"],
            callbacks=callbacks_list,
            steps_per_epoch=steps_per_epoch,
            verbose=1,
        )

        # 4. Save plots of the training
        plot_acc_los, plot_confusion_matrix = modelo.save_plot_results(
            X_test=X_test, Y_test=Y_test, path_to_save=PATH_CHECKPOINTS_SAVE
        )

    def callback_training_creation(self, epochs: int):
        today = datetime.now()
        num_model = self.model_repository.get_next_model_number()

        model_variables = ModelVariables(
            name=f"{num_model}-Modelo_{today.strftime('%Y-%m-%d_%H-%M-%S')}",
            loss=0.0,
            val_loss=0.0,
            accuracy=0.0,
            val_accuracy=0.0,
            mean_time_execution=0.0,
            epoch=0,
            cant_epochs=epochs,
            training_state=TrainingState.CREATED,
            begin_time=datetime.now(),
            end_time=datetime.now(),
        )
        id = self.model_repository.create(model_variables)
        model_variables.id = id

        return model_variables

    def callback_update(self, model_variables: ModelVariables):
        self.model_repository.update(model_variables)

    def get_actual_model(self) -> ModelVariables:
        return self.model_repository.get_actual_model()

    def get_checkpoint_path(self) -> str:
        return os.path.join(PATH_MODELS, self.get_actual_model().name)
