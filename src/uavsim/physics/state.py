"""
UAV state.

World coordinates:

X = forward
Y = right
Z = up

Attitude:

roll  = radians
pitch = radians
yaw   = radians
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class UAVState:

    position: np.ndarray

    velocity: np.ndarray

    attitude: np.ndarray

    angular_velocity: np.ndarray

    mass: float

    @classmethod
    def initial(
        cls,
        mass,
        position=(0.0, 0.0, 0.0),
        velocity=(0.0, 0.0, 0.0),
        attitude=(0.0, 0.0, 0.0),
    ):

        return cls(

            position=np.asarray(
                position,
                dtype=float,
            ),

            velocity=np.asarray(
                velocity,
                dtype=float,
            ),

            attitude=np.asarray(
                attitude,
                dtype=float,
            ),

            angular_velocity=np.zeros(
                3,
                dtype=float,
            ),

            mass=float(
                mass
            ),
        )