"""
Atmosphere and wind field.

The wind field can use either:

1. Constant wind
2. Time-varying wind profile
"""

import numpy as np


class WindField:

    def __init__(
        self,
        velocity=(0.0, 0.0, 0.0),
        profile=None,
    ):

        self.velocity = np.asarray(
            velocity,
            dtype=float,
        )

        self.profile = profile

    def velocity_at(
        self,
        position,
        time,
    ):

        if self.profile is not None:

            return np.asarray(
                self.profile.velocity(
                    time
                ),
                dtype=float,
            )

        return self.velocity.copy()


def relative_air_velocity(
    drone_velocity,
    wind_velocity,
):

    return (
        np.asarray(
            drone_velocity,
            dtype=float,
        )
        -
        np.asarray(
            wind_velocity,
            dtype=float,
        )
    )


def speed_kmh(
    velocity,
):

    return (
        np.linalg.norm(
            velocity
        )
        * 3.6
    )