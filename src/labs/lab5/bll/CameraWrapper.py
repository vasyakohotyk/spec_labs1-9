import math

import numpy as np
from OpenGL.GLU import gluLookAt

from labs.lab5.dal.Camera import CameraData


class Camera:
    """
    Class representing a camera with various transformation capabilities.
    """

    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        if data:
            self.data = data

    @classmethod
    def create(
        cls,
        position,
        target,
        up_vector,
        pitch=0,
        yaw=-90.0,
        fovy=45.0,
        aspect=1.77,
        z_near=0.1,
        z_far=100.0,
    ):
        data = CameraData(
            position=np.array(position, dtype=np.float32),
            target=np.array(target, dtype=np.float32),
            up_vector=np.array(up_vector, dtype=np.float32),
            pitch=pitch,
            yaw=yaw,
            fovy=fovy,
            aspect=aspect,
            z_near=z_near,
            z_far=z_far,
        )
        instance = cls(data)
        return instance

    def apply_transformations(self):
        gluLookAt(
            self.data.position[0],
            self.data.position[1],
            self.data.position[2],
            self.data.target[0],
            self.data.target[1],
            self.data.target[2],
            self.data.up_vector[0],
            self.data.up_vector[1],
            self.data.up_vector[2],
        )

    def rotate(self, dx, dy, dz=0):
        self.data.yaw -= dy
        self.data.pitch += dx
        # Limit the pitch to avoid flipping the camera
        self.data.pitch = max(-89.0, min(89.0, self.data.pitch))

        # Calculate new direction vector based on yaw and pitch
        direction = np.array(
            [
                math.cos(math.radians(self.data.yaw))
                * math.cos(math.radians(self.data.pitch)),
                math.sin(math.radians(self.data.pitch)),
                math.sin(math.radians(self.data.yaw))
                * math.cos(math.radians(self.data.pitch)),
            ],
            dtype=np.float32,
        )

        # Update the target position
        self.data.target = self.data.position + direction

    def translate(self, x, y, z):
        translation_vector = np.array([x, y, z], dtype=np.float32)
        self.data.position += translation_vector
        self.data.target += translation_vector

    def update_fovy(self, delta_fovy=0):
        self.data.fovy = max(10, min(170, self.data.fovy + delta_fovy))

    def update_aspect(self, delta_aspect):
        if not delta_aspect:
            return
        self.data.aspect = delta_aspect
        self.data.aspect = max(
            0.1, min(5, delta_aspect)
        )  # Ensures aspect ratio within plausible boundaries

    def update_z_near(self, delta_z_near):
        self.data.z_near = max(
            0.01, min(5.0, self.data.z_near + delta_z_near)
        )  # Clamps the near clip plane distance

    def update_z_far(self, delta_z_far):
        self.data.z_far = max(
            3.0, min(1000.0, self.data.z_far + delta_z_far)
        )  # Clamps the far clip plane distance

    def get_perspective(self):
        return self.data.fovy, self.data.aspect, self.data.z_near, self.data.z_far
