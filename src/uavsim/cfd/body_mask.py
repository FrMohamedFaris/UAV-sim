"""
UAV-Sim CFD Stage 6C

Converts a 2D UAV boundary into a CFD solid mask.

Mask convention:

    False = fluid
    True  = solid UAV

The CFD solver will use this mask for
bounce-back boundary conditions.
"""

from __future__ import annotations

import numpy as np


class BodyMask:

    def __init__(
        self,
        domain,
    ):

        self.domain = domain

        self.mask = np.zeros(
            domain.shape,
            dtype=bool,
        )

    # ========================================================
    # CREATE FROM POLYGON
    # ========================================================

    def from_polygon(
        self,
        points,
    ):

        points = np.asarray(
            points,
            dtype=float,
        )

        if points.ndim != 2:
            raise ValueError(
                "Polygon must have shape "
                "(N, 2)"
            )

        if points.shape[1] != 2:
            raise ValueError(
                "Polygon must contain "
                "X,Y coordinates"
            )

        if len(points) < 3:
            raise ValueError(
                "Polygon requires at least "
                "3 points"
            )

        # ----------------------------------------------------
        # Make sure polygon is closed.
        # ----------------------------------------------------

        if not np.allclose(
            points[0],
            points[-1],
        ):

            points = np.vstack(
                [
                    points,
                    points[0],
                ]
            )

        # ----------------------------------------------------
        # Point-in-polygon test
        #
        # Ray casting algorithm.
        # ----------------------------------------------------

        x = self.domain.X
        y = self.domain.Y

        inside = np.zeros(
            x.shape,
            dtype=bool,
        )

        x0 = points[:-1, 0]
        y0 = points[:-1, 1]

        x1 = points[1:, 0]
        y1 = points[1:, 1]

        for i in range(
            len(x0)
        ):

            yi = y0[i]
            yj = y1[i]

            xi = x0[i]
            xj = x1[i]

            crosses = (
                (yi > y)
                !=
                (yj > y)
            )

            denominator = (
                yj - yi
            )

            if abs(denominator) < 1e-15:
                continue

            intersection_x = (
                xi
                +
                (
                    y - yi
                )
                *
                (
                    xj - xi
                )
                /
                denominator
            )

            inside ^= (
                crosses
                &
                (
                    x
                    <
                    intersection_x
                )
            )

        self.mask = inside

        return self.mask

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):

        self.mask.fill(
            False
        )

    # ========================================================
    # SOLID CELL COUNT
    # ========================================================

    @property
    def solid_cells(self):

        return int(
            np.count_nonzero(
                self.mask
            )
        )

    # ========================================================
    # FLUID CELL COUNT
    # ========================================================

    @property
    def fluid_cells(self):

        return int(
            self.mask.size
            -
            self.solid_cells
        )

    # ========================================================
    # SOLID FRACTION
    # ========================================================

    @property
    def solid_fraction(self):

        return (
            self.solid_cells
            /
            self.mask.size
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):

        print()
        print("=" * 70)
        print("CFD BODY MASK")
        print("=" * 70)

        print(
            f"Grid cells   : "
            f"{self.mask.size:,}"
        )

        print(
            f"Solid cells  : "
            f"{self.solid_cells:,}"
        )

        print(
            f"Fluid cells  : "
            f"{self.fluid_cells:,}"
        )

        print(
            f"Solid fraction: "
            f"{self.solid_fraction:.4%}"
        )

        print("=" * 70)