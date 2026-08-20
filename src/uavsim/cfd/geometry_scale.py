"""
UAV-Sim CFD Stage 6C

Geometry scaling and positioning.

The UAV is scaled into the CFD domain while
preserving its aspect ratio.

The final UAV is positioned at the CENTER
of the complete CFD domain.
"""

from __future__ import annotations

import numpy as np


def normalize_boundary(
    points,
    domain_width,
    domain_height,
    body_width_fraction=0.35,
    body_height_fraction=0.35,
    center=True,
):

    points = np.asarray(
        points,
        dtype=float,
    )

    if points.ndim != 2:
        raise ValueError(
            "Expected boundary shape (N, 2)"
        )

    if points.shape[1] != 2:
        raise ValueError(
            "Boundary must contain X,Y"
        )

    if len(points) < 3:
        raise ValueError(
            "Boundary requires at least 3 points"
        )

    # ========================================================
    # ORIGINAL BOUNDS
    # ========================================================

    xmin = np.min(
        points[:, 0]
    )

    xmax = np.max(
        points[:, 0]
    )

    ymin = np.min(
        points[:, 1]
    )

    ymax = np.max(
        points[:, 1]
    )

    width = xmax - xmin
    height = ymax - ymin

    if width <= 0:
        raise ValueError(
            "Boundary width is zero"
        )

    if height <= 0:
        raise ValueError(
            "Boundary height is zero"
        )

    # ========================================================
    # REMOVE ORIGINAL OFFSET
    # ========================================================

    normalized = (
        points
        -
        np.array(
            [
                xmin,
                ymin,
            ],
            dtype=float,
        )
    )

    # ========================================================
    # TARGET SIZE
    # ========================================================

    target_width = (
        domain_width
        *
        body_width_fraction
    )

    target_height = (
        domain_height
        *
        body_height_fraction
    )

    # ========================================================
    # PRESERVE ASPECT RATIO
    # ========================================================

    scale_x = (
        target_width
        /
        width
    )

    scale_y = (
        target_height
        /
        height
    )

    scale = min(
        scale_x,
        scale_y,
    )

    normalized *= scale

    # ========================================================
    # ACTUAL SCALED SIZE
    # ========================================================

    scaled_width = (
        np.max(
            normalized[:, 0]
        )
        -
        np.min(
            normalized[:, 0]
        )
    )

    scaled_height = (
        np.max(
            normalized[:, 1]
        )
        -
        np.min(
            normalized[:, 1]
        )
    )

    # ========================================================
    # CENTER BODY IN CFD DOMAIN
    # ========================================================

    if center:

        body_center_x = (
            np.min(
                normalized[:, 0]
            )
            +
            np.max(
                normalized[:, 0]
            )
        ) / 2.0

        body_center_y = (
            np.min(
                normalized[:, 1]
            )
            +
            np.max(
                normalized[:, 1]
            )
        ) / 2.0

        domain_center_x = (
            domain_width / 2.0
        )

        domain_center_y = (
            domain_height / 2.0
        )

        normalized[:, 0] += (
            domain_center_x
            -
            body_center_x
        )

        normalized[:, 1] += (
            domain_center_y
            -
            body_center_y
        )

    # ========================================================
    # DIAGNOSTICS
    # ========================================================

    print()
    print("=" * 70)
    print("UAV GEOMETRY NORMALIZATION")
    print("=" * 70)

    print(
        f"Original width  : {width:.4f}"
    )

    print(
        f"Original height : {height:.4f}"
    )

    print(
        f"Scale factor    : {scale:.6f}"
    )

    print(
        f"CFD width       : {scaled_width:.4f}"
    )

    print(
        f"CFD height      : {scaled_height:.4f}"
    )

    print(
        f"Domain center   : "
        f"({domain_width / 2:.3f}, "
        f"{domain_height / 2:.3f})"
    )

    print("=" * 70)

    return normalized