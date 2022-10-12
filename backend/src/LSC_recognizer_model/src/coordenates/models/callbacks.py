import time
from datetime import datetime

import numpy as np
import tensorflow as tf
from repositories.callback_repository import CallbackRepository

from models.callback_variables import CallbackVariables, TrainingState


class SaveResultsOnDatabaseCallback(tf.keras.callbacks.Callback):
    def __init__(self, callback_repository: CallbackRepository, epochs: int):
        super(SaveResultsOnDatabaseCallback, self).__init__()
        self.callback_variables = None
        self.timer = 0
        self.mean = 0
        self.timer_per_epoch = []
        self.callback_repository = callback_repository
        self.epochs = epochs

    def on_train_begin(self, logs=None):
        self.callback_variables = CallbackVariables(
            loss=0.0,
            val_loss=0.0,
            accuracy=0.0,
            val_accuracy=0.0,
            mean_time_execution=0.0,
            epoch=0,
            cant_epochs=self.epochs,
            training_state=TrainingState.START,
            begin_time=datetime.now(),
            end_time=datetime.now(),
        )
        id = self.callback_repository.create(self.callback_variables)
        self.callback_variables.id = id

    def on_epoch_begin(self, epoch, logs=None):
        self.timer = time.perf_counter()

    def on_epoch_end(self, epoch, logs=None):
        self.timer_per_epoch.append(time.perf_counter() - self.timer)
        self.mean = np.mean(self.timer_per_epoch[-25:])

        # Regular clear of timers to "avoid" memory overflow (its not really a problem, but it is a good practice)
        if len(self.timer_per_epoch) > 50:
            self.timer_per_epoch = self.timer_per_epoch[25:]

        self.callback_variables.loss = logs.get("loss")
        self.callback_variables.val_loss = logs.get("val_loss")
        self.callback_variables.accuracy = logs.get("accuracy")
        self.callback_variables.val_accuracy = logs.get("val_accuracy")
        self.callback_variables.epoch = epoch
        self.callback_variables.mean_time_execution = self.mean
        self.callback_variables.training_state = TrainingState.PROCESSING

        self.callback_repository.update(self.callback_variables)

    def on_train_end(self, logs=None):
        if self.callback_variables.epoch == self.epochs - 1:
            self.callback_variables.training_state = TrainingState.FINISHED
        else:
            self.callback_variables.training_state = TrainingState.ERROR
        self.callback_variables.end_time = datetime.now()

        self.callback_repository.update(self.callback_variables)
