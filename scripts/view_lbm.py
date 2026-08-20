"""
UAV-Sim CFD Stage 6B

Visualize the LBM velocity magnitude.
"""

import matplotlib.pyplot as plt

from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.lbm import (
    D2Q9,
)


def main():

    config = CFDConfig()

    config.validate()

    lbm = D2Q9(

        nx=config.nx,

        ny=config.ny,

        u0=config.u0,

        viscosity=config.viscosity,
    )

    # Run the flow.

    for _ in range(
        500
    ):

        lbm.step()

    speed = (
        lbm.speed()
    )

    plt.figure(
        figsize=(14, 6)
    )

    plt.imshow(
        speed,
        origin="lower",
        aspect="auto",
        extent=[
            0,
            config.domain_width,
            0,
            config.domain_height,
        ],
    )

    plt.xlabel(
        "X — Flow direction"
    )

    plt.ylabel(
        "Y — Cross-flow direction"
    )

    plt.title(
        "D2Q9 LBM Velocity Magnitude"
    )

    plt.colorbar(
        label="Lattice velocity"
    )

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    main()