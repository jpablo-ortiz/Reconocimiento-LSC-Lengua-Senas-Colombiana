from typing import List, Optional

from pydantic import BaseModel


class Coords(BaseModel):
    x: float
    y: float
    z: float
    visibility: float

    # Get empty coords
    @classmethod
    def empty(cls):
        return cls(x=0.0, y=0.0, z=0.0, visibility=0.0)


class CoordsWithouthVisibility(BaseModel):
    x: float
    y: float
    z: float

    # Get empty coords
    @classmethod
    def empty(cls):
        return cls(x=0.0, y=0.0, z=0.0)


class CoordSignal(BaseModel):
    pose: Optional[List[Coords]]
    leftHand: Optional[List[CoordsWithouthVisibility]]
    rightHand: Optional[List[CoordsWithouthVisibility]]
    ea: Optional[List[Coords]]
    face: Optional[List[CoordsWithouthVisibility]]
