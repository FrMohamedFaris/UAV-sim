"""
Wind profile for UAV simulation.

The wind can vary with time.

This is still a simplified model.
The later CFD solver will calculate
the actual spatial airflow field.
"""

import numpy as np


class WindProfile:

    def __init__(
        self,
        base_speed=10.0,
        direction_deg=0.0,
        gust_amplitude=0.0,
        gust_frequency=0.2,
    ):

        self.base_speed = float(
            base_speed
        )

        self.direction_deg = float(
            direction_deg
        )

        self.gust_amplitude = float(
            gust_amplitude
        )

        self.gust_frequency = float(
            gust_frequency
        )

    def velocity(
        self,
        time,
    ):

        direction = np.radians(
            self.direction_deg
        )

        # ----------------------------------------------------
        # Base wind
        # ----------------------------------------------------

        base = np.array(
            [
                np.cos(direction),
                np.sin(direction),
                0.0,
            ],
            dtype=float,
        )

        # ----------------------------------------------------
        # Gust
        # ----------------------------------------------------

        gust = (
            self.gust_amplitude
            *
            np.sin(
                2.0
                * np.pi
                * self.gust_frequency
                * time
            )
        )

        return (
            base
            *
            (
                self.base_speed
                + gust
            )
        )