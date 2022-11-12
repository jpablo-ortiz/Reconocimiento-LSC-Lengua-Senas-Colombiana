import time
from datetime import datetime

import numpy as np
import tensorflow as tf

from models.model_variables import ModelVariables, TrainingState
from repositories.model_repository import ModelRepository


class SaveResultsOnDatabaseCallback(tf.keras.callbacks.Callback):
    def __init__(
        self,
        model_repository: ModelRepository,
        epochs: int,
        model_variables: ModelVariables,
        evaluate_val: str = "val_loss",
    ):
        super(SaveResultsOnDatabaseCallback, self).__init__()
        self.model_variables = model_variables
        self.timer = 0
        self.mean = 0
        self.timer_per_epoch = []
        self.model_repository = model_repository
        self.epochs = epochs
        self.evaluate_val = evaluate_val

    def on_train_begin(self, logs=None):
        self.model_variables.training_state = TrainingState.STARTED
        self.model_repository.update(self.model_variables)

    def on_epoch_begin(self, epoch, logs=None):
        self.timer = time.perf_counter()

    def on_epoch_end(self, epoch, logs=None):
        self.timer_per_epoch.append(time.perf_counter() - self.timer)
        self.mean = np.mean(self.timer_per_epoch[-25:])

        # Regular clear of timers to "avoid" memory overflow (its not really a problem, but it is a good practice)
        if len(self.timer_per_epoch) > 50:
            self.timer_per_epoch = self.timer_per_epoch[-25:]

        self.model_variables.loss = logs.get("loss")
        self.model_variables.accuracy = logs.get("accuracy")

        if self.evaluate_val == "val_loss":
            if epoch < 3 or logs.get("val_loss") < self.model_variables.val_loss:
                self.model_variables.val_loss = logs.get("val_loss")
                self.model_variables.val_accuracy = logs.get("val_accuracy")
        elif self.evaluate_val == "val_accuracy":
            if logs.get("val_accuracy") > self.model_variables.val_accuracy:
                self.model_variables.val_loss = logs.get("val_loss")
                self.model_variables.val_accuracy = logs.get("val_accuracy")

        self.model_variables.epoch = epoch
        self.model_variables.mean_time_execution = self.mean
        self.model_variables.training_state = TrainingState.PROCESSING

        self.model_repository.update(self.model_variables)

    def on_train_end(self, logs=None):
        if self.model_variables.epoch == self.epochs - 1:
            self.model_variables.training_state = TrainingState.FINISHED
        else:
            self.model_variables.training_state = TrainingState.ERROR
        self.model_variables.end_time = datetime.now()

        self.model_repository.update(self.model_variables)
