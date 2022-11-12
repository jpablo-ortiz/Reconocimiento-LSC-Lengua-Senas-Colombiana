import enum
from typing import Type, Union

from models.coord_signal import CoordSignal, CoordsWithouthVisibility
from utils.landmarks.landmarks_info import LandmarkInfo

CANT_LANDMARKS_HAND = 21 * 3


class HandLandmark(enum.IntEnum):
    """The 21 hand landmarks."""

    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Hand(enum.IntEnum):
    """The 2 hands."""

    LEFT = 0
    RIGHT = 1

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class HandInfo(LandmarkInfo):
    def __init__(
        self,
        results: Union[Type, CoordSignal],
        hand: Hand = Hand.RIGHT,
    ):
        if isinstance(results, Type):
            landmarks = results.right_hand_landmarks if hand == Hand.RIGHT else results.left_hand_landmarks
        elif isinstance(results, CoordSignal):
            landmarks = results.rightHand if hand == Hand.RIGHT else results.leftHand
        else:
            raise TypeError("los resultados deben ser NormalizedLandmarkList (Mediapipe) o CoordSignal")

        if landmarks is None:
            landmarks = [CoordsWithouthVisibility.empty()] * int(CANT_LANDMARKS_HAND / 3)
        elif landmarks is not None and isinstance(results, Type):
            landmarks = landmarks.landmark

        super().__init__(
            landmark=landmarks,
            points=HandLandmark,
            connections=self._hand_connections(),
            name="left_hand" if hand == Hand.LEFT else "right_hand",
            has_visibility=False,
        )

    def _hand_connections(self):
        # fmt: off
        HAND_PALM_CONNECTIONS = ((0, 1), (0, 5), (9, 13), (13, 17), (5, 9), (0, 17))
        HAND_THUMB_CONNECTIONS = ((1, 2), (2, 3), (3, 4))
        HAND_INDEX_FINGER_CONNECTIONS = ((5, 6), (6, 7), (7, 8))
        HAND_MIDDLE_FINGER_CONNECTIONS = ((9, 10), (10, 11), (11, 12))
        HAND_RING_FINGER_CONNECTIONS = ((13, 14), (14, 15), (15, 16))
        HAND_PINKY_FINGER_CONNECTIONS = ((17, 18), (18, 19), (19, 20))

        return frozenset().union(*[
            HAND_PALM_CONNECTIONS, HAND_THUMB_CONNECTIONS,
            HAND_INDEX_FINGER_CONNECTIONS, HAND_MIDDLE_FINGER_CONNECTIONS,
            HAND_RING_FINGER_CONNECTIONS, HAND_PINKY_FINGER_CONNECTIONS
        ])
        # fmt: on
