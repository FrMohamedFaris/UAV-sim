"""
UAV-Sim CFD Stage 6B

D2Q9 LBM stability test.

IMPORTANT:

There is no drone in this test.

We are testing whether the fluid solver
can maintain a stable uniform flow.
"""

from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.domain import (
    CFDDomain,
)

from uavsim.cfd.lbm import (
    D2Q9,
)


def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 6B — D2Q9 LBM TEST")
    print("=" * 70)

    # ========================================================
    # CONFIG
    # ========================================================

    config = CFDConfig()

    config.validate()

    # ========================================================
    # DOMAIN
    # ========================================================

    domain = CFDDomain(

        width=config.domain_width,

        height=config.domain_height,

        nx=config.nx,

        ny=config.ny,
    )

    domain.summary()

    # ========================================================
    # SOLVER
    # ========================================================

    print()
    print("[1] Creating D2Q9 solver...")

    lbm = D2Q9(

        nx=config.nx,

        ny=config.ny,

        u0=config.u0,

        viscosity=config.viscosity,
    )

    print(
        f"tau   = {lbm.tau:.6f}"
    )

    print(
        f"omega = {lbm.omega:.6f}"
    )

    print(
        f"u0    = {lbm.u0:.6f}"
    )

    # ========================================================
    # SIMULATION
    # ========================================================

    print()
    print("[2] Running LBM...")

    checkpoints = 10

    interval = max(
        1,
        config.steps
        // checkpoints,
    )

    for step in range(
        config.steps
    ):

        lbm.step()

        if (
            step % interval == 0
            or
            step == config.steps - 1
        ):

            d = (
                lbm.diagnostics()
            )

            print(
                f"step={d['step']:5d} "
                f"| "
                f"rho="
                f"{d['rho_min']:.5f}"
                f"–"
                f"{d['rho_max']:.5f}"
                f" | "
                f"max|u|="
                f"{d['max_velocity']:.6f}"
                f" | "
                f"Mach="
                f"{d['mach']:.6f}"
            )

    # ========================================================
    # FINAL CHECKS
    # ========================================================

    print()
    print("[3] Final validation...")

    d = (
        lbm.diagnostics()
    )

    assert d[
        "rho_min"
    ] > 0.0

    assert d[
        "rho_max"
    ] < 2.0

    assert d[
        "max_velocity"
    ] < 0.15

    assert d[
        "max_velocity"
    ] == d[
        "max_velocity"
    ]

    print()
    print(
        "✓ Density stable"
    )

    print(
        "✓ Velocity stable"
    )

    print(
        "✓ No NaN / Inf"
    )

    print()
    print("=" * 70)
    print("STAGE 6B COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()