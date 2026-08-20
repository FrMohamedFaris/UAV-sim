"""
UAV-Sim CFD Stage 6B
D2Q9 Lattice Boltzmann Method

This is a minimal, CPU-based LBM solver.

Coordinate system:

X -> flow direction
Y -> cross-flow direction

D2Q9 lattice:

             2
             ↑
         5   │   6
           \ │ /
        3 ←  0  → 1
           / │ \
         7   │   8
             ↓
             4

The implementation is intentionally simple and
explicit so numerical stability can be inspected.
"""

import numpy as np


class D2Q9:

    # ========================================================
    # D2Q9 VELOCITY DIRECTIONS
    # ========================================================

    CX = np.array(
        [
            0,
            1,
            0,
            -1,
            0,
            1,
            -1,
            -1,
            1,
        ],
        dtype=np.int32,
    )

    CY = np.array(
        [
            0,
            0,
            1,
            0,
            -1,
            1,
            1,
            -1,
            -1,
        ],
        dtype=np.int32,
    )

    # ========================================================
    # D2Q9 WEIGHTS
    # ========================================================

    W = np.array(
        [
            4.0 / 9.0,
            1.0 / 9.0,
            1.0 / 9.0,
            1.0 / 9.0,
            1.0 / 9.0,
            1.0 / 36.0,
            1.0 / 36.0,
            1.0 / 36.0,
            1.0 / 36.0,
        ],
        dtype=np.float64,
    )

    # Opposite directions.
    OPPOSITE = np.array(
        [
            0,
            3,
            4,
            1,
            2,
            7,
            8,
            5,
            6,
        ],
        dtype=np.int32,
    )

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        nx,
        ny,
        u0=0.05,
        viscosity=0.02,
        rho0=1.0,
    ):

        self.nx = int(nx)
        self.ny = int(ny)

        self.u0 = float(u0)

        self.viscosity = float(
            viscosity
        )

        self.rho0 = float(
            rho0
        )

        if self.nx < 10:
            raise ValueError(
                "nx must be >= 10"
            )

        if self.ny < 10:
            raise ValueError(
                "ny must be >= 10"
            )

        if self.u0 <= 0.0:
            raise ValueError(
                "u0 must be > 0"
            )

        if self.u0 >= 0.15:
            raise ValueError(
                "u0 is too large for "
                "this stable test solver"
            )

        if self.viscosity <= 0.0:
            raise ValueError(
                "viscosity must be > 0"
            )

        # ====================================================
        # LBM SPEED OF SOUND
        # ====================================================

        self.cs2 = 1.0 / 3.0

        # ====================================================
        # RELAXATION TIME
        # ====================================================

        self.tau = (
            0.5
            +
            self.viscosity
            / self.cs2
        )

        # Relaxation frequency.

        self.omega = (
            1.0
            / self.tau
        )

        if self.tau <= 0.5:
            raise ValueError(
                "Invalid tau. "
                "tau must be > 0.5"
            )

        if self.omega <= 0.0:
            raise ValueError(
                "Invalid omega"
            )

        if self.omega >= 2.0:
            raise ValueError(
                "omega must be < 2"
            )

        # ====================================================
        # MACROSCOPIC FIELDS
        # ====================================================

        self.rho = np.full(
            (
                self.ny,
                self.nx,
            ),
            self.rho0,
            dtype=np.float64,
        )

        self.ux = np.full(
            (
                self.ny,
                self.nx,
            ),
            self.u0,
            dtype=np.float64,
        )

        self.uy = np.zeros(
            (
                self.ny,
                self.nx,
            ),
            dtype=np.float64,
        )

        # ====================================================
        # DISTRIBUTION FUNCTION
        # ====================================================

        self.f = np.zeros(
            (
                9,
                self.ny,
                self.nx,
            ),
            dtype=np.float64,
        )

        self.feq = np.zeros_like(
            self.f
        )

        # Initialize equilibrium.

        self.f[:] = (
            self.equilibrium(
                self.rho,
                self.ux,
                self.uy,
            )
        )

        # Simulation counter.

        self.step_number = 0

    # ========================================================
    # EQUILIBRIUM DISTRIBUTION
    # ========================================================

    def equilibrium(
        self,
        rho,
        ux,
        uy,
    ):

        usq = (
            ux * ux
            +
            uy * uy
        )

        feq = np.empty(
            (
                9,
                self.ny,
                self.nx,
            ),
            dtype=np.float64,
        )

        for i in range(9):

            cu = (
                self.CX[i] * ux
                +
                self.CY[i] * uy
            )

            feq[i] = (
                self.W[i]
                * rho
                *
                (
                    1.0
                    +
                    3.0 * cu
                    +
                    4.5 * cu * cu
                    -
                    1.5 * usq
                )
            )

        return feq

    # ========================================================
    # MACROSCOPIC VARIABLES
    # ========================================================

    def update_macroscopic(self):

        self.rho = np.sum(
            self.f,
            axis=0,
        )

        # Avoid division by zero.

        rho_safe = np.maximum(
            self.rho,
            1e-12,
        )

        self.ux = (
            np.sum(
                self.f
                * self.CX[
                    :,
                    None,
                    None,
                ],
                axis=0,
            )
            / rho_safe
        )

        self.uy = (
            np.sum(
                self.f
                * self.CY[
                    :,
                    None,
                    None,
                ],
                axis=0,
            )
            / rho_safe
        )

    # ========================================================
    # COLLISION
    # ========================================================

    def collide(self):

        self.feq = (
            self.equilibrium(
                self.rho,
                self.ux,
                self.uy,
            )
        )

        # Standard BGK relaxation.
        #
        # The smaller inlet velocity and higher viscosity
        # used in Stage 6D keep this within a stable regime.

        self.f += (
                self.omega
                *
                (
                        self.feq
                        -
                        self.f
                )
        )

    # ========================================================
    # STREAMING
    # ========================================================

    def stream(self):

        streamed = np.empty_like(
            self.f
        )

        for i in range(9):

            streamed[i] = np.roll(
                self.f[i],
                shift=(
                    self.CY[i],
                    self.CX[i],
                ),
                axis=(
                    0,
                    1,
                ),
            )

        self.f = streamed

    # ========================================================
    # SIMPLE BOUNDARIES
    # ========================================================

    def apply_boundaries(self):

        # ----------------------------------------------------
        # Top / bottom bounce-back
        # ----------------------------------------------------

        # Bottom wall.

        self.f[2, 0, :] = (
            self.f[4, 0, :]
        )

        self.f[5, 0, :] = (
            self.f[7, 0, :]
        )

        self.f[6, 0, :] = (
            self.f[8, 0, :]
        )

        # Top wall.

        self.f[4, -1, :] = (
            self.f[2, -1, :]
        )

        self.f[7, -1, :] = (
            self.f[5, -1, :]
        )

        self.f[8, -1, :] = (
            self.f[6, -1, :]
        )

        # ----------------------------------------------------
        # Inlet
        # ----------------------------------------------------

        # Keep a simple equilibrium inlet.

        rho_in = np.ones(
            self.ny,
            dtype=np.float64,
        )

        ux_in = np.full(
            self.ny,
            self.u0,
            dtype=np.float64,
        )

        uy_in = np.zeros(
            self.ny,
            dtype=np.float64,
        )

        inlet = self.equilibrium(
            rho_in[:, None],
            ux_in[:, None],
            uy_in[:, None],
        )

        self.f[:, :, 0] = (
            inlet[:, :, 0]
        )

        # ----------------------------------------------------
        # Outlet
        # ----------------------------------------------------

        # Simple zero-gradient outlet.

        self.f[:, :, -1] = (
            self.f[:, :, -2]
        )

    # ========================================================
    # ONE TIME STEP
    # ========================================================

    def step(
        self,
        solid_mask=None,
    ):

        # ----------------------------------------------------
        # 1. Macroscopic variables
        # ----------------------------------------------------

        self.update_macroscopic()

        # ----------------------------------------------------
        # 2. Collision
        # ----------------------------------------------------

        self.collide()

        # ----------------------------------------------------
        # 3. Streaming
        # ----------------------------------------------------

        self.stream()

        # ----------------------------------------------------
        # 4. Outer CFD boundaries
        # ----------------------------------------------------

        self.apply_boundaries()

        # ----------------------------------------------------
        # 5. UAV solid boundary
        # ----------------------------------------------------

        if solid_mask is not None:

            self.apply_body_boundary(
                solid_mask
            )

        # ----------------------------------------------------
        # 6. Recalculate macroscopic fields
        # ----------------------------------------------------

        self.update_macroscopic()

        # ----------------------------------------------------
        # 7. Force UAV velocity to zero
        # ----------------------------------------------------

        if solid_mask is not None:

            self.ux[solid_mask] = 0.0
            self.uy[solid_mask] = 0.0

        # ----------------------------------------------------
        # 8. Step counter
        # ----------------------------------------------------

        self.step_number += 1

        # ----------------------------------------------------
        # 9. Stability
        # ----------------------------------------------------

        self.check_stability()
    # ========================================================
    # SOLID BODY BOUNCE-BACK
    # ========================================================

    def apply_body_boundary(
            self,
            solid_mask,
    ):
        """
        Apply a stable solid-body boundary.

        True  -> solid UAV
        False -> fluid
        """

        if solid_mask.shape != (
                self.ny,
                self.nx,
        ):
            raise ValueError(
                "solid_mask shape must be "
                f"({self.ny}, {self.nx})"
            )

        # --------------------------------------------------------
        # Bounce-back
        # --------------------------------------------------------

        old_f = self.f.copy()

        for i in range(9):
            opposite = self.OPPOSITE[i]

            self.f[
                opposite,
                solid_mask,
            ] = old_f[
                i,
                solid_mask,
            ]

        # --------------------------------------------------------
        # Force zero velocity inside the body.
        # --------------------------------------------------------

        self.ux[
            solid_mask
        ] = 0.0

        self.uy[
            solid_mask
        ] = 0.0

        # --------------------------------------------------------
        # Keep density inside the solid well behaved.
        # --------------------------------------------------------

        self.rho[
            solid_mask
        ] = 1.0


    # ========================================================
    # SPEED
    # ========================================================

    def speed(
            self,
            solid_mask=None,
    ):

        speed = np.sqrt(
            self.ux * self.ux
            +
            self.uy * self.uy
        )

        if solid_mask is not None:
            speed = speed.copy()

            speed[
                solid_mask
            ] = 0.0

        return speed

    # ========================================================
    # MACH-LIKE NUMBER
    # ========================================================

    def lattice_mach(
            self,
            solid_mask=None,
    ):

        velocity = self.speed(
            solid_mask
        )

        return (
                velocity
                /
                np.sqrt(self.cs2)
        )

    # ========================================================
    # STABILITY CHECK
    # ========================================================

    def check_stability(
        self,
        max_velocity=0.15,
        rho_min=0.5,
        rho_max=1.5,
    ):

        if not np.all(
            np.isfinite(
                self.f
            )
        ):

            raise RuntimeError(
                "LBM divergence: "
                "distribution contains "
                "NaN or Inf"
            )

        if not np.all(
            np.isfinite(
                self.rho
            )
        ):

            raise RuntimeError(
                "LBM divergence: "
                "density contains "
                "NaN or Inf"
            )

        if not np.all(
            np.isfinite(
                self.ux
            )
        ):

            raise RuntimeError(
                "LBM divergence: "
                "ux contains "
                "NaN or Inf"
            )

        if not np.all(
            np.isfinite(
                self.uy
            )
        ):

            raise RuntimeError(
                "LBM divergence: "
                "uy contains "
                "NaN or Inf"
            )

        max_u = np.max(
            self.speed()
        )

        if max_u > max_velocity:

            raise RuntimeError(
                "LBM divergence: "
                f"max|u|={max_u:.6f} "
                f"> {max_velocity:.6f}"
            )

        min_rho = np.min(
            self.rho
        )

        max_rho = np.max(
            self.rho
        )

        if (
            min_rho < rho_min
            or
            max_rho > rho_max
        ):

            raise RuntimeError(
                "LBM density became "
                f"unstable: "
                f"{min_rho:.6f} "
                f"to "
                f"{max_rho:.6f}"
            )

    # ========================================================
    # DIAGNOSTICS
    # ========================================================

    def diagnostics(self):

        speed = self.speed()

        return {

            "step":
                self.step_number,

            "rho_min":
                float(
                    np.min(
                        self.rho
                    )
                ),

            "rho_max":
                float(
                    np.max(
                        self.rho
                    )
                ),

            "rho_mean":
                float(
                    np.mean(
                        self.rho
                    )
                ),

            "max_velocity":
                float(
                    np.max(
                        speed
                    )
                ),

            "mean_velocity":
                float(
                    np.mean(
                        speed
                    )
                ),

            "mach":
                float(
                    np.max(
                        self.lattice_mach()
                    )
                ),
        }