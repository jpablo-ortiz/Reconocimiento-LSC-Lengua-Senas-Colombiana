import abc
from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R


class LandmarkInfo(metaclass=abc.ABCMeta):
    def __init__(self, points, connections, name, landmark, has_visibility):
        self.POINTS = points
        self.CONNECTIONS = connections
        self.name = name
        self.landmark = landmark
        self.has_visibility = has_visibility
        self.was_fixed = False

    def get_from_vector(self, vector: list):
        landmarks = [l for i, l in enumerate(self.landmark) if self.POINTS.has_value(i)]
        for l, v in zip(landmarks, vector):
            l.x = v[0]
            l.y = v[1]
            l.z = v[2]
        return self

    def get_fixed_landmark(self, discard_porcentage=0.0):
        # Discard the landmarks that are not used in this project.
        if not self.was_fixed:
            landmarks = [l for i, l in enumerate(self.landmark) if self.POINTS.has_value(i)]
        else:
            landmarks = self.landmark
        # Search the min and max values of the landmarks on x, y and z axis.
        xmin, xmax, ymin, ymax, zmin, zmax = 0, 0, 0, 0, 0, 0

        for i, landmark in enumerate(landmarks):
            # Take advantage of the "for" and apply the discard_porcentage on the landmarks results.
            if self._visibility_verification(landmark, discard_porcentage):
                landmark.x = 0
                landmark.y = 0
                landmark.z = 0
                landmark.visibility = 0
                continue

            if i == 0:
                xmin = xmax = landmark.x
                ymin = ymax = landmark.y
                zmin = zmax = landmark.z
            else:
                xmin = min(xmin, landmark.x)
                xmax = max(xmax, landmark.x)
                ymin = min(ymin, landmark.y)
                ymax = max(ymax, landmark.y)
                zmin = min(zmin, landmark.z)
                zmax = max(zmax, landmark.z)

        if (xmin == 0 and xmax == 0) or (ymin == 0 and ymax == 0) or (zmin == 0 and zmax == 0):
            return landmarks

        # Normalize the landmarks to the range [0, 1].
        for r in landmarks:
            r.z = (r.z - zmin) / (zmax - zmin)
            r.x = (r.x - xmin) / (xmax - xmin)
            r.y = (r.y - ymin) / (ymax - ymin)

        return landmarks

    def get_unprocessed_coordenates(self, fix_points=True, discard_porcentage=0.0):
        landmark = self.get_fixed_landmark(discard_porcentage) if fix_points else self.landmark
        if self.has_visibility:
            return np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in landmark]).flatten()
        else:
            return np.array([[lm.x, lm.y, lm.z] for lm in landmark]).flatten()

    def plot_landmark(self, landmark=None, elevation=10, azimuth=10, discard_porcentage=0.0):
        landmarks = self.get_fixed_landmark() if landmark is None else landmark

        # Plot configurations
        fig = plt.figure(figsize=(10, 5))
        ax = plt.axes(projection="3d")

        ax.view_init(elev=elevation, azim=azimuth)
        ax.set_xlabel("z")
        ax.set_ylabel("x")
        ax.set_zlabel("y")
        ax.set_title(self.name)

        # Plot points (landmarks)
        plotted_landmarks = {}
        for idx, landmark in enumerate(landmarks):
            if self._visibility_verification(landmark, discard_porcentage):
                continue

            ax.scatter3D(
                xs=[-landmark.z],
                ys=[landmark.x],
                zs=[-landmark.y],
            )
            plotted_landmarks[idx] = (-landmark.z, landmark.x, -landmark.y)
            plotted_landmarks[idx] = (-landmark.z, landmark.x, -landmark.y)

        num_landmarks = len(landmarks)
        # Draws the connections if the start and end landmarks are both visible.
        for connection in self.CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                raise ValueError(
                    f"Landmark index is out of range. Invalid connection "
                    f"from landmark #{start_idx} to landmark #{end_idx}."
                )
            if start_idx in plotted_landmarks and end_idx in plotted_landmarks:
                landmark_pair = [
                    plotted_landmarks[start_idx],
                    plotted_landmarks[end_idx],
                ]
                ax.plot3D(
                    xs=[landmark_pair[0][0], landmark_pair[1][0]],
                    ys=[landmark_pair[0][1], landmark_pair[1][1]],
                    zs=[landmark_pair[0][2], landmark_pair[1][2]],
                )
        # plt.show()
        return plt

    def _visibility_verification(self, landmark, discard_porcentage):
        if self.has_visibility:
            return landmark.visibility < discard_porcentage
        else:
            return False

    def _rotate_points(self, vector_3d, rotation_degrees=90, rotation_axis=[True, False, False]):
        """
        Rotate a vector around a given axis.

        Parameters
        ----------
        vector_3d : list
            Vector to rotate.
        rotation_degrees : float
            Rotation angle in degrees.
        rotation_axis : list of bools [x, y, z]
            Axis to rotate around.
        """
        rotation_radians = np.radians(rotation_degrees)
        rotation_axis = np.array(rotation_axis)

        rotation_vector = rotation_radians * rotation_axis
        rotation = R.from_rotvec(rotation_vector)
        rotated_vec = rotation.apply(vector_3d)
        return rotated_vec

    def data_aug_coords(
        self,
        x_max_rotation=30,
        y_max_rotation=45,
        z_max_rotation=20,
        axies_to_rotate=["x", "y", "z"],
        cant_rotations_per_axis=[3, 3, 3],
    ) -> list:
        """
        Data augmentation for coordinates.

        Parameters
        ----------
        x_max_rotation : int, optional
            Max rotation for x axis, by default 30
        y_max_rotation : int, optional
            Max rotation for y axis, by default 45
        z_max_rotation : int, optional
            Max rotation for z axis, by default 30
        axies_to_rotate : list, optional
            List of axies to rotate, by default ["x", "y", "z"].
                e.g. ["x", "y"] will rotate only x and y axis
        cant_rotations_per_axis : list, optional
            List of rotations per axis, by default [3, 3, 3]
            This rotatios will be combined between them.
                e.g. [4, 2, 2] will rotate 4 times x axis, 2 times y axis and 2 times z axis.
                Resulting in 4 * 2 * 2 = 16 rotations.
        """

        if not all([a in ["x", "y", "z"] for a in axies_to_rotate]):
            raise ValueError("The axies to rotate must be 'x' and/or 'y' and/or 'z'")

        list_of_vectors = [[r.x, r.y, r.z] for r in self.get_fixed_landmark()]

        new_list_of_vectors = [list_of_vectors]

        if "x" in axies_to_rotate:
            # Create a list of rotations on x
            x_rotations = np.linspace(-x_max_rotation, x_max_rotation, cant_rotations_per_axis[0])

            # Sort min to max with abs(). (It's because we're rotating around the original coordenate)
            # To improve this data augmentation, we need 3 principal photos (front camera, a liitle bit left (aprox 20 degrees), a little bit right (aprox 20 degrees))
            # Example:
            # Original: [-30, -20, -10, 0, 10, 20, 30]
            # Sorted: [0, -10, 10, -20, 20, -30, 30]
            x_rotations = sorted(x_rotations, key=lambda x: abs(x))

            # Rotate each list_of_vector of the new_list_of_vectors
            tem_list_of_vectors = []
            for lov in new_list_of_vectors:
                for x in x_rotations:
                    new_vector = [self._rotate_points(v, x, [True, False, False]) for v in lov]
                    tem_list_of_vectors.append(new_vector)
            new_list_of_vectors = tem_list_of_vectors

        if "y" in axies_to_rotate:
            # Create a list of rotations on y
            y_rotations = np.linspace(-y_max_rotation, y_max_rotation, cant_rotations_per_axis[1])

            # Sort min to max with abs(). (It's because we're rotating around the original coordenate)
            y_rotations = sorted(y_rotations, key=lambda x: abs(x))

            # Rotate each list_of_vector of the new_list_of_vectors
            tem_list_of_vectors = []
            for lov in new_list_of_vectors:
                for y in y_rotations:
                    new_vector = [self._rotate_points(v, y, [False, True, False]) for v in lov]
                    tem_list_of_vectors.append(new_vector)
            new_list_of_vectors = tem_list_of_vectors

        if "z" in axies_to_rotate:
            # Create a list of rotations on z
            z_rotations = np.linspace(-z_max_rotation, z_max_rotation, cant_rotations_per_axis[2])

            # Sort min to max with abs(). (It's because we're rotating around the original coordenate)
            z_rotations = sorted(z_rotations, key=lambda x: abs(x))

            # Rotate each list_of_vector of the new_list_of_vectors
            tem_list_of_vectors = []
            for lov in new_list_of_vectors:
                for z in z_rotations:
                    new_vector = [self._rotate_points(v, z, [False, False, True]) for v in lov]
                    tem_list_of_vectors.append(new_vector)
            new_list_of_vectors = tem_list_of_vectors

        # Convert all the vectors to landmarks_info
        new_landmarks_info = []
        for list_of_vector in new_list_of_vectors:
            temp_landmarks_info = deepcopy(self)
            temp_landmarks_info.get_from_vector(list_of_vector)
            new_landmarks_info.append(temp_landmarks_info)

        return new_landmarks_info
