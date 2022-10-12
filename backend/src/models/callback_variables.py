import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrainingState(enum.IntEnum):
    START = 0
    PROCESSING = 1
    FINISHED = 2
    ERROR = 3

    @classmethod
    def has_value(cls, value):
        return value in range(4)


class CallbackVariables(BaseModel):
    id: Optional[str]
    loss: float
    val_loss: float
    accuracy: float
    val_accuracy: float
    mean_time_execution: float
    epoch: int
    cant_epochs: int
    training_state: TrainingState
    begin_time: datetime = None
    end_time: datetime = None

    class Config:
        arbitrary_types_allowed = True
