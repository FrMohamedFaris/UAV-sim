"""
3D rotation utilities.

Coordinate system:

X = forward
Y = right
Z = up

Attitude:

roll  = rotation around X
pitch = rotation around Y
yaw   = rotation around Z
"""

import numpy as np


def rotation_x(angle):
    """Rotation around X axis."""

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, c, -s],
        [0.0, s, c],
    ])


def rotation_y(angle):
    """Rotation around Y axis."""

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, 0.0, s],
        [0.0, 1.0, 0.0],
        [-s, 0.0, c],
    ])


def rotation_z(angle):
    """Rotation around Z axis."""

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, -s, 0.0],
        [s, c, 0.0],
        [0.0, 0.0, 1.0],
    ])


def rotation_matrix(
    roll,
    pitch,
    yaw,
):
    """
    Create body-to-world rotation matrix.

    Rotation order:

        roll
          ↓
        pitch
          ↓
        yaw
    """

    Rx = rotation_x(roll)
    Ry = rotation_y(pitch)
    Rz = rotation_z(yaw)

    return (
        Rz
        @ Ry
        @ Rx
    )


def body_to_world(
    vector,
    attitude,
):
    """
    Transform a vector from UAV body coordinates
    into world coordinates.
    """

    roll, pitch, yaw = attitude

    R = rotation_matrix(
        roll,
        pitch,
        yaw,
    )

    return R @ np.asarray(
        vector,
        dtype=float,
    )


def world_to_body(
    vector,
    attitude,
):
    """
    Transform a world vector into UAV body coordinates.
    """

    roll, pitch, yaw = attitude

    R = rotation_matrix(
        roll,
        pitch,
        yaw,
    )

    return R.T @ np.asarray(
        vector,
        dtype=float,
    )