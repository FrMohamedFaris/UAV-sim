"""
UAV propulsion model.

Body coordinate system:

        +Z
         ↑
         │
         │
         UAV
         ───────→ +X

Thrust is initially along +Z in body coordinates.

The attitude rotates this vector into world coordinates.
"""

import numpy as np

from uavsim.physics.rotation import (
    body_to_world,
)


class Propulsion:

    def __init__(
        self,
        max_thrust,
    ):

        self.max_thrust = float(
            max_thrust
        )

    def thrust(
        self,
        throttle,
        attitude,
    ):

        throttle = np.clip(
            throttle,
            0.0,
            1.0,
        )

        magnitude = (
            throttle
            * self.max_thrust
        )

        # ----------------------------------------------------
        # Thrust in UAV body coordinates
        # ----------------------------------------------------

        thrust_body = np.array(
            [
                0.0,
                0.0,
                magnitude,
            ],
            dtype=float,
        )

        # ----------------------------------------------------
        # Rotate into world coordinates
        # ----------------------------------------------------

        thrust_world = body_to_world(
            thrust_body,
            attitude,
        )

        return thrust_world