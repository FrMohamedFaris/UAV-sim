"""
UAV simulation engine.

Stage 3:

UAV state
    ↓
Wind
    ↓
Relative airflow
    ↓
Aerodynamics
    ↓
Thrust
    ↓
Gravity
    ↓
Motion
"""

import numpy as np

from uavsim.physics.integrator import (
    integrate,
)


class SimulationEngine:

    def __init__(
        self,
        state,
        propulsion,
        aerodynamic_model,
        wind_field,
        dt=0.01,
    ):

        self.state = state

        self.propulsion = propulsion

        self.aerodynamic_model = (
            aerodynamic_model
        )

        self.wind_field = wind_field

        self.dt = float(
            dt
        )

        self.time = 0.0

    def step(
        self,
        throttle,
    ):

        # ----------------------------------------------------
        # WIND
        # ----------------------------------------------------

        wind = (
            self.wind_field.velocity_at(
                self.state.position,
                self.time,
            )
        )

        # ----------------------------------------------------
        # RELATIVE AIRFLOW
        # ----------------------------------------------------

        relative_velocity = (
            self.state.velocity
            -
            wind
        )

        # ----------------------------------------------------
        # AERODYNAMICS
        # ----------------------------------------------------

        aero = (
            self.aerodynamic_model.calculate(
                relative_velocity
            )
        )

        aerodynamic_force = (
            aero["force"]
        )

        # ----------------------------------------------------
        # PROPULSION
        # ----------------------------------------------------

        thrust = (
            self.propulsion.thrust(
                throttle,
                self.state.attitude,
            )
        )

        # ----------------------------------------------------
        # INTEGRATE
        # ----------------------------------------------------

        integrate(
            self.state,
            thrust,
            aerodynamic_force,
            self.dt,
        )

        self.time += self.dt

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        return {

            "time":
                self.time,

            "position":
                self.state.position.copy(),

            "velocity":
                self.state.velocity.copy(),

            "attitude":
                self.state.attitude.copy(),

            "wind":
                wind.copy(),

            "relative_velocity":
                relative_velocity.copy(),

            "thrust":
                thrust.copy(),

            "aerodynamic_force":
                aerodynamic_force.copy(),

            "lift":
                aero["lift"],

            "drag":
                aero["drag"],

            "dynamic_pressure":
                aero[
                    "dynamic_pressure"
                ],
        }