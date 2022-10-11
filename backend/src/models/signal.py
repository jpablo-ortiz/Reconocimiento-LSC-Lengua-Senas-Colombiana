from typing import List, Optional

from pydantic import BaseModel


class Signal(BaseModel):
    name: str
    photos: List[str]  # Photos on base64
    counter: Optional[int] = 0
    new_signal: Optional[bool] = False
