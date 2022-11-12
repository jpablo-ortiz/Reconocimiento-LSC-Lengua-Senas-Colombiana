from typing import List, Optional

from pydantic import BaseModel


# --------------------------------------------
# Request Models
# --------------------------------------------
class RequestSignal(BaseModel):
    name: str
    images: List[str]  # List of images on base64


# --------------------------------------------
# Models
# --------------------------------------------


class Image(BaseModel):
    image: Optional[str]  # Photo on base64
    name: str
    processed_image: bool = False  # If the image has been processed or not


class Signal(BaseModel):
    name: str
    images: Optional[List[Image]]
    processed_signal: bool = False  # If the signal has been processed or not
