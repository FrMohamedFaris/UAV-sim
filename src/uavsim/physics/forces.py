import numpy as np

from .constants import GRAVITY


def gravity_force(
    mass: float,
):

    return np.array(
        [
            0.0,
            0.0,
            -mass * GRAVITY,
        ]
    )


def net_force(
    mass: float,
    thrust: np.ndarray,
    aerodynamic_force: np.ndarray,
):

    return (
        thrust
        +
        aerodynamic_force
        +
        gravity_force(mass)
    )