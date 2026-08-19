"""
Launch configuration.
"""

import numpy as np


def launch_velocity(
    speed_mps,
    angle_deg,
):
    """
    Initial velocity.

    The launch angle is measured upward
    from the horizontal X direction.
    """

    angle = np.radians(
        angle_deg
    )

    vx = (
        speed_mps
        * np.cos(angle)
    )

    vz = (
        speed_mps
        * np.sin(angle)
    )

    return np.array(
        [
            vx,
            0.0,
            vz,
        ],
        dtype=float,
    )


def launch_attitude(
    angle_deg,
):
    """
    Initial aircraft attitude.

    Returns:

        [roll, pitch, yaw]

    in radians.
    """

    pitch = np.radians(
        angle_deg
    )

    return np.array(
        [
            0.0,
            pitch,
            0.0,
        ],
        dtype=float,
    )