import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrainingState(enum.IntEnum):
    CREATED = 0
    STARTED = 1
    PROCESSING = 2
    FINISHED = 3
    ERROR = 4

    @classmethod
    def has_value(cls, value):
        return value in range(5)


class ModelVariables(BaseModel):
    id: Optional[str]
    name: str  # 1-Modelo_99.9%_2022-10-25_23:39:20
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
    trained_signals: dict[str, str] = None

    class Config:
        arbitrary_types_allowed = True
