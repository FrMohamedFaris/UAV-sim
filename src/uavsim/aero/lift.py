"""
Simplified aerodynamic lift model.

Lift:

    L = 0.5 * rho * V^2 * S * CL

Stage 3 uses a simple CL model.

Later we can replace it with:
    - airfoil lookup
    - CFD-generated coefficients
    - aircraft-specific coefficient tables
"""

import numpy as np


class LiftModel:

    def __init__(
        self,
        reference_area,
        lift_coefficient=0.4,
        air_density=1.225,
    ):

        self.reference_area = float(
            reference_area
        )

        self.lift_coefficient = float(
            lift_coefficient
        )

        self.air_density = float(
            air_density
        )

    def calculate(
        self,
        relative_velocity,
    ):

        velocity = np.asarray(
            relative_velocity,
            dtype=float,
        )

        speed = np.linalg.norm(
            velocity
        )

        if speed < 1e-9:

            return np.zeros(
                3,
                dtype=float,
            )

        dynamic_pressure = (
            0.5
            * self.air_density
            * speed**2
        )

        lift_magnitude = (
            dynamic_pressure
            * self.reference_area
            * self.lift_coefficient
        )

        # ----------------------------------------------------
        # Stage 3 approximation:
        #
        # Lift acts approximately in +Z world direction.
        #
        # We will later calculate the actual lift direction
        # from the aircraft velocity and body orientation.
        # ----------------------------------------------------

        return np.array(
            [
                0.0,
                0.0,
                lift_magnitude,
            ],
            dtype=float,
        )