"""
Time integration for UAV flight dynamics.
"""

import numpy as np

from .constants import GRAVITY


def integrate(
    state,
    thrust,
    aerodynamic_force,
    dt,
):

    # --------------------------------------------------------
    # Gravity
    # --------------------------------------------------------

    gravity = np.array(
        [
            0.0,
            0.0,
            -state.mass * GRAVITY,
        ],
        dtype=float,
    )

    # --------------------------------------------------------
    # Total force
    # --------------------------------------------------------

    total_force = (
        thrust
        +
        aerodynamic_force
        +
        gravity
    )

    # --------------------------------------------------------
    # Newton's second law
    #
    # F = ma
    # a = F/m
    # --------------------------------------------------------

    acceleration = (
        total_force
        / state.mass
    )

    # --------------------------------------------------------
    # Semi-implicit Euler integration
    # --------------------------------------------------------

    state.velocity += (
        acceleration
        * dt
    )

    state.position += (
        state.velocity
        * dt
    )

    return state