import enum
from typing import Type, Union

from models.coord_signal import Coords, CoordSignal
from utils.landmarks.landmarks_info import LandmarkInfo

CANT_OLD_LANDMARKS_POSE = 33 * 4
CANT_LANDMARKS_POSE = 25 * 4


class OldPoseLandmark(enum.IntEnum):
    """The original 33 pose landmarks."""

    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    # The following landmark is not used in this proyect.
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class PoseLandmark(enum.IntEnum):
    """The 25 pose landmarks modified to de original"""

    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class PoseInfo(LandmarkInfo):
    def __init__(
        self,
        results: Union[Type[tuple], CoordSignal],
    ):
        if isinstance(results, Type):
            landmarks = results.pose_landmarks
        elif isinstance(results, CoordSignal):
            landmarks = results.pose
        else:
            raise TypeError("los resultados deben ser NormalizedLandmarkList (Mediapipe) o CoordSignal")

        if landmarks is None:
            landmarks = [Coords.empty()] * int(CANT_LANDMARKS_POSE / 4)
        elif landmarks is not None and isinstance(results, Type):
            landmarks = landmarks.landmark

        super().__init__(
            landmark=landmarks,
            points=PoseLandmark,
            connections=self._pose_connections(),
            name="pose",
            has_visibility=True,
        )

    def _pose_connections(self, old_connections=False):
        # fmt: off
        OLD_POSE_CONNECTIONS = frozenset(
            [
                (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5),
                (5, 6), (6, 8), (9, 10), (11, 12), (11, 13),
                (13, 15), (15, 17), (15, 19), (15, 21), (17, 19), 
                (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
                (18, 20), (11, 23), (12, 24), (23, 24), (23, 25),
                (24, 26), (25, 27), (26, 28), (27, 29), (28, 30),
                (29, 31), (30, 32), (27, 31), (28, 32),
            ]
        )
        # Pose connections (from, to) without the landmarks that are not used in this project.
        CONNECTIONS = frozenset( 
            [
                (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5),
                (5, 6), (6, 8), (9, 10), (11, 12), (11, 13),
                (13, 15), (15, 17), (15, 19), (15, 21), (17, 19), 
                (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
                (18, 20), (11, 23), (12, 24), (23, 24)
            ]
        )
        # fmt: on

        if old_connections:
            return OLD_POSE_CONNECTIONS
        else:
            return CONNECTIONS
