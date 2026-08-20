"""
UAV-Sim CFD Stage 6A

Computational domain for the LBM solver.

Coordinate system:

X -> flow direction
Y -> cross-flow direction

The domain is intentionally 2D for Stage 6.

The UAV/body will be introduced in Stage 6C.

Domain:

    inlet                         outlet
      │                              │
      ▼                              ▼

      ┌──────────────────────────────┐
      │                              │
      │                              │
      │          CFD DOMAIN          │
      │                              │
      │                              │
      └──────────────────────────────┘

X = streamwise direction
Y = transverse direction
"""


from dataclasses import dataclass

import numpy as np


@dataclass
class CFDDomain:

    # Physical dimensions
    width: float
    height: float

    # Grid resolution
    nx: int
    ny: int

    def __post_init__(self):

        if self.width <= 0:
            raise ValueError(
                "Domain width must be > 0"
            )

        if self.height <= 0:
            raise ValueError(
                "Domain height must be > 0"
            )

        if self.nx < 10:
            raise ValueError(
                "nx must be >= 10"
            )

        if self.ny < 10:
            raise ValueError(
                "ny must be >= 10"
            )

        # ----------------------------------------------------
        # Grid spacing
        # ----------------------------------------------------

        self.dx = (
            self.width
            / (self.nx - 1)
        )

        self.dy = (
            self.height
            / (self.ny - 1)
        )

        # ----------------------------------------------------
        # Coordinates
        # ----------------------------------------------------

        self.x = np.linspace(
            0.0,
            self.width,
            self.nx,
        )

        self.y = np.linspace(
            0.0,
            self.height,
            self.ny,
        )

        self.X, self.Y = np.meshgrid(
            self.x,
            self.y,
        )

    # ========================================================
    # SHAPE
    # ========================================================

    @property
    def shape(self):

        return (
            self.ny,
            self.nx,
        )

    # ========================================================
    # CENTER
    # ========================================================

    @property
    def center(self):

        return (
            self.width / 2.0,
            self.height / 2.0,
        )

    # ========================================================
    # TOTAL CELLS
    # ========================================================

    @property
    def cell_count(self):

        return (
            self.nx
            * self.ny
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):

        print()
        print("=" * 70)
        print("CFD COMPUTATIONAL DOMAIN")
        print("=" * 70)

        print(
            f"Width       : "
            f"{self.width:.3f}"
        )

        print(
            f"Height      : "
            f"{self.height:.3f}"
        )

        print(
            f"Resolution  : "
            f"{self.nx} x {self.ny}"
        )

        print(
            f"Grid spacing: "
            f"dx={self.dx:.6f}, "
            f"dy={self.dy:.6f}"
        )

        print(
            f"Cells       : "
            f"{self.cell_count:,}"
        )

        print(
            f"Center      : "
            f"({self.center[0]:.3f}, "
            f"{self.center[1]:.3f})"
        )

        print("=" * 70)