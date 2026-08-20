"""
UAV-Sim CFD
Stage 6F - Physical Flight Scaling

Converts physical UAV flight conditions into
useful aerodynamic reference quantities.

IMPORTANT
---------
LBM lattice velocity is NOT physical velocity.

Example:

    180 km/h = 50 m/s

may be represented numerically by:

    lattice_velocity = 0.03

The mapping is kept explicit so that the
simulation does not confuse physical units
with lattice units.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PhysicalCondition:
    """
    Physical flight condition.

    Parameters
    ----------
    speed_kmh:
        Physical UAV airspeed in km/h.

    characteristic_length_m:
        Reference aerodynamic length in metres.

    air_density:
        Air density in kg/m^3.

    dynamic_viscosity:
        Dynamic viscosity in Pa.s.

    lattice_velocity:
        Numerical LBM reference velocity.

    lattice_length:
        Characteristic body length measured
        in lattice cells.
    """

    # ========================================================
    # PHYSICAL FLIGHT CONDITION
    # ========================================================

    speed_kmh: float = 180.0

    characteristic_length_m: float = 0.33

    # Standard sea-level approximation.

    air_density: float = 1.225

    dynamic_viscosity: float = 1.81e-5

    # ========================================================
    # NUMERICAL LBM REFERENCE
    # ========================================================

    lattice_velocity: float = 0.03

    lattice_length: float = 140.0

    # ========================================================
    # SPEED
    # ========================================================

    @property
    def speed_ms(self) -> float:
        """
        Convert km/h to m/s.
        """

        return self.speed_kmh / 3.6

    # ========================================================
    # REYNOLDS NUMBER
    # ========================================================

    @property
    def reynolds(self) -> float:
        """
        Reynolds number:

            Re = rho * V * L / mu
        """

        if (
            self.air_density <= 0.0
            or self.dynamic_viscosity <= 0.0
            or self.characteristic_length_m <= 0.0
        ):
            raise ValueError(
                "Air density, viscosity and "
                "characteristic length must be > 0."
            )

        return (
            self.air_density
            * self.speed_ms
            * self.characteristic_length_m
            / self.dynamic_viscosity
        )

    # ========================================================
    # MACH NUMBER
    # ========================================================

    @property
    def mach(self) -> float:
        """
        Approximate Mach number.

        Uses 340.3 m/s as the reference
        speed of sound.
        """

        speed_of_sound = 340.3

        return self.speed_ms / speed_of_sound

    # ========================================================
    # LBM VISCOSITY
    # ========================================================

    @property
    def lattice_viscosity_for_re(self) -> float:
        """
        Estimate lattice viscosity corresponding
        to the selected Reynolds number.

        This is a reference calculation only.

        Do NOT automatically use this value in the
        current BGK solver at high Reynolds number,
        because tau approaching 0.5 can become unstable.
        """

        if self.reynolds <= 0.0:

            raise ValueError(
                "Reynolds number must be > 0."
            )

        return (
            self.lattice_velocity
            * self.lattice_length
            / self.reynolds
        )

    # ========================================================
    # LBM TAU
    # ========================================================

    @property
    def lattice_tau_for_re(self) -> float:
        """
        Calculate theoretical BGK relaxation time:

            nu = cs^2 * (tau - 0.5)

        therefore:

            tau = 0.5 + nu / cs^2

        This is reported for analysis only.
        """

        cs2 = 1.0 / 3.0

        nu = (
            self.lattice_viscosity_for_re
        )

        return (
            0.5
            +
            nu / cs2
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self) -> None:

        print()
        print("=" * 70)
        print("PHYSICAL FLIGHT CONDITION")
        print("=" * 70)

        print(
            f"Speed                 : "
            f"{self.speed_kmh:.2f} km/h"
        )

        print(
            f"Speed                 : "
            f"{self.speed_ms:.3f} m/s"
        )

        print(
            f"Characteristic length : "
            f"{self.characteristic_length_m:.3f} m"
        )

        print(
            f"Air density           : "
            f"{self.air_density:.4f} kg/m^3"
        )

        print(
            f"Dynamic viscosity     : "
            f"{self.dynamic_viscosity:.4e} Pa.s"
        )

        print(
            f"Reynolds number       : "
            f"{self.reynolds:.4e}"
        )

        print(
            f"Mach number           : "
            f"{self.mach:.5f}"
        )

        print()
        print("LBM NUMERICAL REFERENCE")
        print("-" * 70)

        print(
            f"Lattice velocity      : "
            f"{self.lattice_velocity:.6f}"
        )

        print(
            f"Lattice body length   : "
            f"{self.lattice_length:.2f} cells"
        )

        print(
            f"Theoretical lattice nu: "
            f"{self.lattice_viscosity_for_re:.8f}"
        )

        print(
            f"Theoretical LBM tau   : "
            f"{self.lattice_tau_for_re:.8f}"
        )

        print()
        print(
            "NOTE: The theoretical tau is not "
            "automatically applied to the current solver."
        )

        print("=" * 70)