"""
Stage 6C

Load the actual UAV boundary generated
from the STEP model and convert it into
a CFD solid mask.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.domain import (
    CFDDomain,
)

from uavsim.cfd.boundary_loader import (
    BoundaryLoader,
)

from uavsim.cfd.geometry_scale import (
    normalize_boundary,
)

from uavsim.cfd.body_mask import (
    BodyMask,
)

from uavsim.cfd.geometry_transform import (
    rotate,
)

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

BOUNDARY_FILE = (
    PROJECT_ROOT
    / "assets"
    / "aircraft"
    / "boundary.csv"
)


def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 6C — REAL UAV CFD MASK")
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

    # ========================================================
    # LOAD
    # ========================================================

    print()
    print(
        "[1] Loading UAV boundary..."
    )

    loader = BoundaryLoader(
        BOUNDARY_FILE
    )

    points = loader.load()
    print()
    print(
        "[2] Rotating UAV for forward flight..."
    )

    points = rotate(
        points,
        angle_deg=-90.0,
    )
    print(
        f"Boundary points: "
        f"{len(points)}"
    )

    # ========================================================
    # NORMALIZE
    # ========================================================

    print()
    print(
        "[3] Scaling UAV into CFD domain..."
    )

    scaled = normalize_boundary(

        points,

        domain_width=domain.width,

        domain_height=domain.height,

        body_width_fraction=0.35,

        body_height_fraction=0.35,

        center=True,
    )

    # ========================================================
    # MASK
    # ========================================================

    print()
    print(
        "[3] Creating CFD solid mask..."
    )

    body = BodyMask(
        domain
    )

    mask = body.from_polygon(
        scaled
    )

    body.summary()

    # ========================================================
    # VISUALIZE
    # ========================================================

    print()
    print(
        "[4] Visualizing..."
    )

    plt.figure(
        figsize=(16, 6)
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
        scaled[:, 0],
        scaled[:, 1],
        linewidth=2,
    )

    plt.xlabel(
        "X — Flow direction"
    )

    plt.ylabel(
        "Y — Cross-flow direction"
    )

    plt.title(
        "UAV-Sim — Real UAV CFD Boundary"
    )

    plt.grid(
        True,
        alpha=0.25,
    )

    plt.tight_layout()

    plt.show()

    print()
    print("=" * 70)
    print("REAL UAV MASK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()