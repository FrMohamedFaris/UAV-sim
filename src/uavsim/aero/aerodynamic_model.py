"""
Combined aerodynamic force model.

Stage 3:

relative airflow
      ↓
dynamic pressure
      ↓
lift + drag
      ↓
total aerodynamic force
"""

import numpy as np

from uavsim.aero.lift import (
    LiftModel,
)


class AerodynamicModel:

    def __init__(
        self,
        reference_area,
        drag_coefficient=0.8,
        lift_coefficient=0.4,
        air_density=1.225,
    ):

        self.reference_area = float(
            reference_area
        )

        self.drag_coefficient = float(
            drag_coefficient
        )

        self.lift_coefficient = float(
            lift_coefficient
        )

        self.air_density = float(
            air_density
        )

        self.lift_model = LiftModel(
            reference_area=(
                reference_area
            ),
            lift_coefficient=(
                lift_coefficient
            ),
            air_density=(
                air_density
            ),
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

            return {
                "force": np.zeros(
                    3,
                    dtype=float,
                ),

                "lift": 0.0,

                "drag": 0.0,

                "speed": 0.0,
            }

        # ----------------------------------------------------
        # Dynamic pressure
        # ----------------------------------------------------

        q = (
            0.5
            * self.air_density
            * speed**2
        )

        # ----------------------------------------------------
        # Drag
        # ----------------------------------------------------

        drag_magnitude = (
            q
            * self.reference_area
            * self.drag_coefficient
        )

        velocity_direction = (
            velocity
            / speed
        )

        drag_force = (
            -velocity_direction
            * drag_magnitude
        )

        # ----------------------------------------------------
        # Lift
        # ----------------------------------------------------

        lift_force = (
            self.lift_model.calculate(
                velocity
            )
        )

        lift_magnitude = np.linalg.norm(
            lift_force
        )

        # ----------------------------------------------------
        # Total
        # ----------------------------------------------------

        total_force = (
            drag_force
            +
            lift_force
        )

        return {
            "force": total_force,

            "lift_force": lift_force,

            "drag_force": drag_force,

            "lift": lift_magnitude,

            "drag": drag_magnitude,

            "speed": speed,

            "dynamic_pressure": q,
        }