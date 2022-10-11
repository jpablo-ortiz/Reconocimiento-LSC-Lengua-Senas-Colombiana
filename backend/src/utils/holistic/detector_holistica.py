from math import floor
from typing import Type, Union

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions import holistic
from models.coord_signal import CoordSignal
from utils.landmarks.face_info import FaceInfo
from utils.landmarks.hand_info import CANT_LANDMARKS_HAND, Hand, HandInfo
from utils.landmarks.pose_info import CANT_OLD_LANDMARKS_POSE, PoseInfo


class DetectorHolistica:

    # =============================================================
    # =================== Funciones Principales ===================
    # =============================================================

    def __init__(
        self,
        modo_estatico=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1,
        use_hands=True,
        use_face=True,
        use_pose=True,
    ):

        self.use_hands = use_hands
        self.use_face = use_face
        self.use_pose = use_pose

        self.modo_estatico = modo_estatico  # Creamos el objeto y el tendra su propia variable
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.dibujo = mp.solutions.drawing_utils
        self.estilo_dibujo: mp.python.solutions.drawing_styles = mp.solutions.drawing_styles

        # Creamos los objetos que detectaran las manos y las dibujaran
        self.mpholistic: holistic = mp.solutions.holistic
        self.holistic: holistic.Holistic = self.mpholistic.Holistic(
            static_image_mode=self.modo_estatico,
            model_complexity=self.model_complexity,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

    # Funcion para detectar y dibujar la mano con sus componentes
    def detectar_holistica(self, fotograma) -> Type[tuple]:
        # Realizamos la predicción holistica (manos, rostro y pose)
        fotograma = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        fotograma.flags.writeable = False

        self.resultados = self.holistic.process(fotograma)

        fotograma.flags.writeable = True
        fotograma = cv2.cvtColor(fotograma, cv2.COLOR_RGB2BGR)

        return self.resultados

    def dibujar_prediccion(self, fotograma, resultados=None):
        if resultados is None:
            resultados = self.resultados

        fotograma = fotograma.copy()

        # -------------------- Pose connections --------------------
        self.dibujo.draw_landmarks(
            image=fotograma,
            landmark_list=self.resultados.pose_landmarks,
            connections=self.mpholistic.POSE_CONNECTIONS,
            landmark_drawing_spec=self.estilo_dibujo.DrawingSpec(
                color=(75, 50, 121), thickness=1, circle_radius=2
            ),
            connection_drawing_spec=self.estilo_dibujo.DrawingSpec(
                color=(75, 50, 121), thickness=2, circle_radius=2
            ),
        )

        # -------------------- Face connections --------------------
        self.dibujo.draw_landmarks(
            image=fotograma,
            landmark_list=self.resultados.face_landmarks,
            connections=self.mpholistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.estilo_dibujo.get_default_face_mesh_tesselation_style()
            # landmark_drawing_spec=mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
            # connection_drawing_spec=mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
        )
        self.dibujo.draw_landmarks(
            image=fotograma,
            landmark_list=self.resultados.face_landmarks,
            connections=self.mpholistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.estilo_dibujo.get_default_face_mesh_contours_style(),
        )

        # -------------------- Hand connections --------------------
        self.dibujo.draw_landmarks(
            image=fotograma,
            landmark_list=self.resultados.left_hand_landmarks,
            connections=self.mpholistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.dibujo.DrawingSpec(color=(115, 22, 76), thickness=2, circle_radius=4),
            connection_drawing_spec=self.dibujo.DrawingSpec(
                color=(115, 44, 250), thickness=2, circle_radius=2
            ),
        )
        self.dibujo.draw_landmarks(
            image=fotograma,
            landmark_list=self.resultados.right_hand_landmarks,
            connections=self.mpholistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.dibujo.DrawingSpec(color=(250, 117, 66), thickness=2, circle_radius=4),
            connection_drawing_spec=self.dibujo.DrawingSpec(
                color=(250, 66, 230), thickness=2, circle_radius=2
            ),
        )

        return fotograma

    def probability_visualizer(self, results, classes, fotograma):
        fotograma = fotograma.copy()
        colors = [
            (255, 0, 0),
            (255, 20, 0),
            (255, 40, 0),
            (255, 60, 0),
            (255, 80, 0),
            (255, 100, 0),
            (255, 120, 0),
            (255, 140, 0),
            (255, 160, 0),
            (255, 180, 0),
            (255, 200, 0),
            (255, 220, 0),
            (255, 240, 0),
            (255, 255, 0),
            (240, 255, 0),
            (220, 255, 0),
            (200, 255, 0),
            (180, 255, 0),
            (160, 255, 0),
            (140, 255, 0),
            (120, 255, 0),
        ]

        # ordenate the results with the order of the actions
        new_res = []
        for _, action in classes:
            for i in range(len(results)):
                if action == results[i][0]:
                    new_res.append(results[i])
                    break

        # draw the results
        for num, result in enumerate(new_res):
            probability = result[1]
            action = result[0]
            prob = probability / 100

            # given a probability, we can the corresponding color
            color = colors[floor((probability * len(colors)) / 100) - 1]
            cv2.rectangle(fotograma, (0, 60 + num * 30), (int(prob * 100 * 2), 90 + num * 30), color, -1)
            cv2.putText(
                fotograma,
                action,
                (0, 85 + num * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
        return fotograma

    def get_info_objects_of_landmarks(self, resultado: Union[Type[tuple], CoordSignal] = None):
        if resultado is None:
            resultado = self.resultados

        pose = PoseInfo(resultado)
        right_hand = HandInfo(resultado, Hand.RIGHT)
        left_hand = HandInfo(resultado, Hand.LEFT)
        face = FaceInfo(resultado)

        return pose, right_hand, left_hand, face

    def get_unprocessed_coordenates(self, resultado: Union[Type[tuple], CoordSignal] = None):
        if resultado is None:
            resultado = self.resultados

        pose, right_hand, left_hand, face = self.get_info_objects_of_landmarks(resultado)

        pose = pose.get_unprocessed_coordenates()
        right_hand = right_hand.get_unprocessed_coordenates()
        left_hand = left_hand.get_unprocessed_coordenates()
        face = face.get_unprocessed_coordenates()

        return pose, right_hand, left_hand, face

    def get_coordenates(
        self,
        resultado: Union[Type[tuple], CoordSignal] = None,
        used_parts=["pose", "right_hand", "left_hand", "face"],
    ):
        if resultado is None:
            resultado = self.resultados

        pose, right_hand, left_hand, face = self.get_unprocessed_coordenates(resultado)

        X_dataset = []

        if "pose" in used_parts:
            X_dataset.append(pose)

        if "right_hand" in used_parts:
            X_dataset.append(right_hand)

        if "left_hand" in used_parts:
            X_dataset.append(left_hand)

        if "face" in used_parts:
            X_dataset.append(face)

        X_dataset = np.array(np.concatenate(X_dataset), dtype=np.float32)

        return X_dataset

    def get_aug_info_objects_of_landmarks(
        self,
        resultado: Union[Type[tuple], CoordSignal] = None,
        used_parts=["pose", "right_hand", "left_hand", "face"],
        x_max_rotation: int = 30,
        y_max_rotation: int = 45,
        z_max_rotation: int = 20,
        axies_to_rotate=["x", "y", "z"],
        cant_rotations_per_axis=[3, 3, 3],
    ):
        if resultado is None:
            resultado = self.resultados

        # Get object of landmarks info
        pose_info, right_hand_info, left_hand_info, face_info = self.get_info_objects_of_landmarks(resultado)

        # Do coords data augmentation
        if "pose" in used_parts:
            new_poses_info = [pose_info] + pose_info.data_aug_coords(
                x_max_rotation=x_max_rotation,
                y_max_rotation=y_max_rotation,
                z_max_rotation=z_max_rotation,
                axies_to_rotate=axies_to_rotate,
                cant_rotations_per_axis=cant_rotations_per_axis,
            )
        else:
            new_poses_info = [pose_info]

        if "right_hand" in used_parts:
            new_right_hands_info = [right_hand_info] + right_hand_info.data_aug_coords(
                x_max_rotation=x_max_rotation,
                y_max_rotation=y_max_rotation,
                z_max_rotation=z_max_rotation,
                axies_to_rotate=axies_to_rotate,
                cant_rotations_per_axis=cant_rotations_per_axis,
            )
        else:
            new_right_hands_info = [right_hand_info]

        if "left_hand" in used_parts:
            new_left_hands_info = [left_hand_info] + left_hand_info.data_aug_coords(
                x_max_rotation=x_max_rotation,
                y_max_rotation=y_max_rotation,
                z_max_rotation=z_max_rotation,
                axies_to_rotate=axies_to_rotate,
                cant_rotations_per_axis=cant_rotations_per_axis,
            )
        else:
            new_left_hands_info = [left_hand_info]

        if "face" in used_parts:
            new_faces_info = [face_info] + face_info.data_aug_coords(
                x_max_rotation=x_max_rotation,
                y_max_rotation=y_max_rotation,
                z_max_rotation=z_max_rotation,
                axies_to_rotate=axies_to_rotate,
                cant_rotations_per_axis=cant_rotations_per_axis,
            )
        else:
            new_faces_info = [face_info]

        return new_poses_info, new_right_hands_info, new_left_hands_info, new_faces_info

    def get_unproccesed_coordenates_data_aug(
        self,
        resultado: Union[Type[tuple], CoordSignal] = None,
        used_parts=["pose", "right_hand", "left_hand", "face"],
        x_max_rotation: int = 30,
        y_max_rotation: int = 45,
        z_max_rotation: int = 20,
        axies_to_rotate=["x", "y", "z"],
        cant_rotations_per_axis=[3, 3, 3],
    ):
        if resultado is None:
            resultado = self.resultados

        (
            new_poses_info,
            new_right_hands_info,
            new_left_hands_info,
            new_faces_info,
        ) = self.get_aug_info_objects_of_landmarks(
            resultado=resultado,
            used_parts=used_parts,
            x_max_rotation=x_max_rotation,
            y_max_rotation=y_max_rotation,
            z_max_rotation=z_max_rotation,
            axies_to_rotate=axies_to_rotate,
            cant_rotations_per_axis=cant_rotations_per_axis,
        )

        new_poses = [pose.get_unprocessed_coordenates() for pose in new_poses_info]
        new_right_hands = [right_hand.get_unprocessed_coordenates() for right_hand in new_right_hands_info]
        new_left_hands = [left_hand.get_unprocessed_coordenates() for left_hand in new_left_hands_info]
        new_faces = [face.get_unprocessed_coordenates() for face in new_faces_info]

        return new_poses, new_right_hands, new_left_hands, new_faces

    def get_coordenates_aug(
        self,
        resultado: Union[Type[tuple], CoordSignal] = None,
        used_parts=["pose", "right_hand", "left_hand", "face"],
        x_max_rotation: int = 30,
        y_max_rotation: int = 45,
        z_max_rotation: int = 20,
        axies_to_rotate=["x", "y", "z"],
        cant_rotations_per_axis=[3, 3, 3],
    ):
        if resultado is None:
            resultado = self.resultados

        (
            new_poses_info,
            new_right_hands_info,
            new_left_hands_info,
            new_faces_info,
        ) = self.get_unproccesed_coordenates_data_aug(
            resultado=resultado,
            used_parts=used_parts,
            x_max_rotation=x_max_rotation,
            y_max_rotation=y_max_rotation,
            z_max_rotation=z_max_rotation,
            axies_to_rotate=axies_to_rotate,
            cant_rotations_per_axis=cant_rotations_per_axis,
        )

        unprocessed_coords = []
        for p, rh, lh, f in zip(new_poses_info, new_right_hands_info, new_left_hands_info, new_faces_info):
            X_dataset = []

            if "pose" in used_parts:
                X_dataset.append(p)

            if "right_hand" in used_parts:
                X_dataset.append(rh)

            if "left_hand" in used_parts:
                X_dataset.append(lh)

            if "face" in used_parts:
                X_dataset.append(f)

            # TODO: if not works change dtype=object
            X_dataset = np.array(np.concatenate(X_dataset), dtype=np.float32)
            unprocessed_coords.append(X_dataset)

        return unprocessed_coords
