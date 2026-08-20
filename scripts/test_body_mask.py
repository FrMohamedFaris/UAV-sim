"""
UAV-Sim CFD Stage 6C

Test the CFD body-mask system using
a simple UAV-like polygon.

This test does NOT use the CAD model yet.
"""


import numpy as np
import matplotlib.pyplot as plt

from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.domain import (
    CFDDomain,
)

from uavsim.cfd.body_mask import (
    BodyMask,
)


def create_test_uav():

    # --------------------------------------------------------
    # UAV-like 2D profile.
    #
    # X = forward
    # Y = vertical/cross-flow
    # --------------------------------------------------------

    points = np.array(
        [
            [5.0, 5.0],
            [6.5, 5.8],
            [9.0, 6.2],
            [12.0, 6.0],
            [14.0, 5.4],
            [12.0, 5.0],
            [14.0, 4.6],
            [12.0, 4.0],
            [9.0, 3.8],
            [6.5, 4.2],
        ],
        dtype=float,
    )

    return points


def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 6C — BODY MASK TEST")
    print("=" * 70)

    # ========================================================
    # DOMAIN
    # ========================================================

    config = CFDConfig()

    config.validate()

    domain = CFDDomain(
        width=config.domain_width,
        height=config.domain_height,
        nx=config.nx,
        ny=config.ny,
    )

    # ========================================================
    # BODY
    # ========================================================

    points = create_test_uav()

    # ========================================================
    # MASK
    # ========================================================

    body = BodyMask(
        domain
    )

    mask = body.from_polygon(
        points
    )

    body.summary()

    # ========================================================
    # VALIDATION
    # ========================================================

    assert mask.dtype == bool

    assert body.solid_cells > 0

    assert body.fluid_cells > 0

    assert (
        body.solid_cells
        <
        body.mask.size
    )

    print()
    print(
        "✓ Mask contains solid cells"
    )

    print(
        "✓ Mask contains fluid cells"
    )

    print(
        "✓ Mask is boolean"
    )

    # ========================================================
    # VISUALIZATION
    # ========================================================

    plt.figure(
        figsize=(14, 6)
    )

    plt.imshow(
        mask,
        origin="lower",
        extent=[
            0,
            domain.width,
            0,
            domain.height,
        ],
        aspect="equal",
    )

    plt.plot(
        points[:, 0],
        points[:, 1],
        linewidth=2,
    )

    plt.xlabel(
        "X — Flow direction"
    )

    plt.ylabel(
        "Y — Cross-flow direction"
    )

    plt.title(
        "Stage 6C — UAV CFD Solid Mask"
    )

    plt.grid(
        True,
        alpha=0.25,
    )

    plt.tight_layout()

    plt.show()

    print()
    print("=" * 70)
    print("STAGE 6C MASK TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()