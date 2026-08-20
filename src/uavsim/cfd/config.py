"""
CFD configuration.

Stage 6A contains only domain and
numerical stability parameters.

Physical UAV parameters will be added
in later stages.
"""


from dataclasses import dataclass


@dataclass
class CFDConfig:


    # ========================================================
    # PHYSICAL FLIGHT CONDITION
    # ========================================================

    speed_kmh: float = 180.0

    characteristic_length_m: float = 0.33

    air_density: float = 1.225

    air_dynamic_viscosity: float = 1.81e-5

    # --------------------------------------------------------
    # Domain
    # --------------------------------------------------------

    domain_width: float = 20.0

    domain_height: float = 10.0

    nx: int = 400

    ny: int = 200

    # --------------------------------------------------------
    # LBM
    # --------------------------------------------------------

    # Lattice velocity.

    u0: float = 0.03

    # Kinematic viscosity in lattice units.

    viscosity: float = 0.03

    # --------------------------------------------------------
    # Simulation
    # --------------------------------------------------------

    steps: int = 2000

    # Frames will later use this.

    output_interval: int = 10

    # --------------------------------------------------------
    # Stability
    # --------------------------------------------------------

    max_velocity: float = 0.12

    density_min: float = 0.5

    density_max: float = 1.5

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate(self):

        if self.u0 <= 0:
            raise ValueError(
                "u0 must be > 0"
            )

        if self.u0 >= self.max_velocity:
            raise ValueError(
                "u0 must be below "
                "max_velocity"
            )

        if self.viscosity <= 0:
            raise ValueError(
                "viscosity must be > 0"
            )

        if self.nx < 20:
            raise ValueError(
                "nx is too small"
            )

        if self.ny < 20:
            raise ValueError(
                "ny is too small"
            )

        if self.steps <= 0:
            raise ValueError(
                "steps must be > 0"
            )

        if (
            self.density_min
            <= 0
        ):

            raise ValueError(
                "density_min must be > 0"
            )

        if (
            self.density_min
            >= self.density_max
        ):

            raise ValueError(
                "Invalid density limits"
            )
