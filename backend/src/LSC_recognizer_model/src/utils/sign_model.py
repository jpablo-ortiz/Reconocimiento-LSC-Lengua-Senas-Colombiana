import os

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix


class SignModel:
    def __init__(
        self,
        model,
        path_to_load_weights: str = "",
        dataset_train=None,
        dataset_validation=None,
        X_train=None,
        Y_train=None,
        X_validation=None,
        Y_validation=None,
    ):
        self.trained_model = False
        self.have_validation = False

        self.model = model

        # Verifications
        self.is_loaded_weights = path_to_load_weights != ""
        self.is_dataset = dataset_train is not None
        self.is_XY = X_train is not None and Y_train is not None

        if not self.is_dataset and not self.is_XY and not self.is_loaded_weights:
            raise Exception("Se debe proveer un dataset_train o X_train e Y_train o path_to_load_weights")

        if self.is_loaded_weights:
            self.path_to_load_weights = path_to_load_weights
            self.model.load_weights(self.path_to_load_weights)

        if self.is_dataset:
            if dataset_validation is not None:
                self.dataset_validation = dataset_validation
                self.have_validation = True
            else:
                if X_validation is not None and Y_validation is not None:
                    raise Exception("Se debe proveer un dataset_validation cuando se provee un dataset_train")
            self.dataset_train = dataset_train

        elif self.is_XY:
            if X_validation is not None and Y_validation is not None:
                self.X_validation = X_validation
                self.Y_validation = Y_validation
                self.have_validation = True
            else:
                if dataset_validation is not None:
                    raise Exception(
                        "Se debe proveer un X_validation e Y_validation cuando se provee un X_train e Y_train"
                    )
            self.X_train = X_train
            self.Y_train = Y_train

    def train_model(
        self,
        epochs: int = 100,
        optimizer: str = "Adam",
        loss: str = "mean_squared_error",
        metrics: list = ["accuracy"],
        callbacks: list = None,
        steps_per_epoch=None,
        verbose: int = 1,
    ):
        if not self.is_dataset and not self.is_XY:
            raise Exception("Se debe proveer un dataset_train o X_train e Y_train en el constructor (init)")

        if self.is_loaded_weights:
            print(
                "El modelo se cargo con pesos predeterminados, el entrenamiento continuara en la última mejor epoch"
            )

        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

        val = None
        if self.have_validation:
            if self.is_dataset:
                val = self.dataset_validation
            elif self.is_XY:
                val = (self.X_validation, self.Y_validation)

        self.history = self.model.fit(
            x=self.X_train if self.is_XY else self.dataset_train,
            y=self.Y_train if self.is_XY else None,
            validation_data=val,
            epochs=epochs,
            #steps_per_epoch=steps_per_epoch,
            callbacks=callbacks,
            use_multiprocessing=False,
            class_weight=None,
            workers=1,
            verbose=verbose,

        )

        self.trained_model = True

    def load_model_weights(self, path_to_load_weights: str):
        self.is_loaded_weights = True
        self.model.load_weights(path_to_load_weights)

    def save_plot_results(self, X_test, Y_test, path_to_save: str):
        if not self.trained_model:
            raise Exception("Se debe entrenar el modelo antes de guardar las gráficas de resultados")

        if not os.path.exists(f"{path_to_save}/report"):
            os.mkdir(f"{path_to_save}/report")

        plot_acc_los = self.get_plot_acc_loss()
        plot_acc_los.savefig(f"{path_to_save}/report/results.png")
        plot_acc_los.savefig(f"{path_to_save}/report/results.svg")

        plot_confusion_matrix, _ = self.get_plot_confusion_matrix(X_test, Y_test)
        plot_confusion_matrix.savefig(f"{path_to_save}/report/confusion_matrix.png")
        plot_confusion_matrix.savefig(f"{path_to_save}/report/confusion_matrix.svg")

        return plot_acc_los, plot_confusion_matrix

    def get_plot_acc_loss(self):

        if not self.trained_model:
            raise Exception("The model is not trained")
        else:
            history = self.history
            plt.figure(figsize=(12, 5))
            plt.suptitle("Optimizer : Adam", fontsize=10)

            plt.subplot(1, 2, 1)
            plt.ylabel("Loss", fontsize=16)
            # plt.xlabel("Epoch", fontsize=14)
            plt.plot(history.history["loss"], label="Training Loss")
            plt.plot(history.history["val_loss"], label="Validation Loss")
            # Show a point on the best epoch
            plt.plot(
                np.argmin(history.history["val_loss"]),
                np.min(history.history["val_loss"]),
                marker="x",
                color="r",
                label="best model",
            )
            plt.title(
                "Best epoch: {} with loss: {:.3f}".format(
                    np.argmin(history.history["val_loss"]),
                    np.min(history.history["val_loss"]),
                )
            )
            plt.legend(loc="upper right")

            plt.subplot(1, 2, 2)
            plt.ylabel("Accuracy", fontsize=16)
            # plt.xlabel("Epoch", fontsize=14)
            plt.plot(history.history["accuracy"], label="Training Accuracy")
            plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
            # Show a point and the value on the best epoch
            plt.plot(
                np.argmax(history.history["val_accuracy"]),
                np.max(history.history["val_accuracy"]),
                marker="x",
                color="r",
                label="best model",
            )
            plt.title(
                "Best epoch: {} with accuracy: {:.1f}%".format(
                    np.argmax(history.history["val_accuracy"]),
                    np.max(history.history["val_accuracy"]) * 100,
                )
            )
            plt.legend(loc="lower right")

            # plt.show()
            return plt

    def get_plot_confusion_matrix(self, X_test, Y_test):
        if not self.trained_model and not self.is_loaded_weights:
            raise Exception("El modelo no ha sido entrenado o ha sido cargado con pesos predeterminados")

        ytrue = np.argmax(Y_test, axis=1).tolist()

        yhat = self.model.predict(X_test)
        yhat = np.argmax(yhat, axis=1).tolist()

        cm = confusion_matrix(ytrue, yhat)
        plt.figure(figsize=(10, 10))
        sns.heatmap(cm, annot=True, fmt="d")
        plt.title("Confusion matrix")
        plt.ylabel("True label")
        plt.xlabel("Predicted label")

        return plt, accuracy_score(ytrue, yhat)

    def get_prediction(self, keypoints, classes: list[tuple[int, str]], all_results: bool = True):
        if not self.trained_model and not self.is_loaded_weights:
            raise Exception("El modelo no ha sido entrenado o ha sido cargado con pesos predeterminados")
        keypoints = np.expand_dims(keypoints, axis=0)
        results = self.model.predict(keypoints, verbose=0)[0]
        if not all_results:
            result = np.argmax(results)
            return classes[result]
        else:
            all_results: list = []
            for num, prob in enumerate(results):
                probability = int(prob * 100)
                all_results.append((classes[num][1], probability))

            # Sort highest probability to lowest
            return sorted(all_results, key=lambda x: x[1], reverse=True)
