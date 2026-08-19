"""
Simple UAV flight profile.

This controls the aircraft attitude
through the mission.

This is NOT yet a full autopilot.

It is a deterministic test profile
for validating the simulator.
"""

import numpy as np


class FlightProfile:

    def __init__(
        self,

        launch_pitch_deg=30.0,

        cruise_pitch_deg=5.0,

        descent_pitch_deg=-8.0,
    ):

        self.launch_pitch = np.radians(
            launch_pitch_deg
        )

        self.cruise_pitch = np.radians(
            cruise_pitch_deg
        )

        self.descent_pitch = np.radians(
            descent_pitch_deg
        )

    def attitude(
        self,
        time,
    ):

        # ----------------------------------------------------
        # LAUNCH
        # ----------------------------------------------------

        if time < 2.0:

            progress = (
                time / 2.0
            )

            pitch = (
                self.launch_pitch
                * (1.0 - progress)
                +
                self.cruise_pitch
                * progress
            )

        # ----------------------------------------------------
        # CRUISE
        # ----------------------------------------------------

        elif time < 6.0:

            pitch = (
                self.cruise_pitch
            )

        # ----------------------------------------------------
        # DESCENT
        # ----------------------------------------------------

        elif time < 8.0:

            progress = (
                (time - 6.0)
                / 2.0
            )

            pitch = (
                self.cruise_pitch
                * (1.0 - progress)
                +
                self.descent_pitch
                * progress
            )

        # ----------------------------------------------------
        # LANDING
        # ----------------------------------------------------

        else:

            pitch = (
                self.descent_pitch
            )

        return np.array(
            [
                0.0,
                pitch,
                0.0,
            ],
            dtype=float,
        )