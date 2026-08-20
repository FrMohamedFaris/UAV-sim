"""
UAV-Sim CFD geometry transformations.
"""

from __future__ import annotations

import numpy as np


def rotate(
    points,
    angle_deg,
):

    points = np.asarray(
        points,
        dtype=float,
    )

    angle = np.deg2rad(
        angle_deg
    )

    c = np.cos(angle)
    s = np.sin(angle)

    rotation_matrix = np.array(
        [
            [c, -s],
            [s, c],
        ]
    )

    center = np.mean(
        points,
        axis=0,
    )

    centered = (
        points
        -
        center
    )

    rotated = (
        centered
        @
        rotation_matrix.T
    )

    rotated += center

    return rotated