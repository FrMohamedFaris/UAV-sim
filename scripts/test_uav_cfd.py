"""
UAV-Sim
Stage 6F - Physical UAV CFD

Pipeline:

    boundary.csv
          ↓
    geometry rotation
          ↓
    geometry scaling
          ↓
    CFD body mask
          ↓
    physical flight condition
          ↓
    D2Q9 LBM
          ↓
    UAV bounce-back
          ↓
    velocity field
          ↓
    vorticity
          ↓
    CFD visualization
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.domain import (
    CFDDomain,
)

from uavsim.cfd.lbm import (
    D2Q9,
)

from uavsim.cfd.body_mask import (
    BodyMask,
)

from uavsim.cfd.boundary_loader import (
    BoundaryLoader,
)

from uavsim.cfd.geometry_scale import (
    normalize_boundary,
)

from uavsim.cfd.geometry_transform import (
    rotate,
)

from uavsim.cfd.physical import (
    PhysicalCondition,
)

from uavsim.cfd.visualization import (
    plot_cfd,
)


# ============================================================
# PROJECT PATH
# ============================================================

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


# ============================================================
# FLIGHT CONDITION
# ============================================================

AOA_DEG = 90.0

SPEED_KMH = 180.0

CHARACTERISTIC_LENGTH_M = 0.33


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 6F - PHYSICAL UAV CFD")
    print("=" * 70)

    # ========================================================
    # CONFIGURATION
    # ========================================================

    print()
    print("[1] Loading CFD configuration...")

    config = CFDConfig()

    config.speed_kmh = (
        SPEED_KMH
    )

    config.characteristic_length_m = (
        CHARACTERISTIC_LENGTH_M
    )

    config.validate()

    # ========================================================
    # PHYSICAL CONDITION
    # ========================================================

    print()
    print("[2] Creating physical flight condition...")

    physical = PhysicalCondition(

        speed_kmh=SPEED_KMH,

        characteristic_length_m=(
            CHARACTERISTIC_LENGTH_M
        ),

        air_density=(
            config.air_density
        ),

        dynamic_viscosity=(
            config.air_dynamic_viscosity
        ),

        lattice_velocity=(
            config.u0
        ),

        lattice_length=(
            config.nx * 0.35
        ),
    )

    physical.summary()

    # ========================================================
    # CFD DOMAIN
    # ========================================================

    print()
    print("[3] Creating CFD domain...")

    domain = CFDDomain(

        width=config.domain_width,

        height=config.domain_height,

        nx=config.nx,

        ny=config.ny,
    )

    domain.summary()

    # ========================================================
    # LOAD UAV BOUNDARY
    # ========================================================

    print()
    print("[4] Loading UAV boundary...")

    if not BOUNDARY_FILE.exists():

        raise FileNotFoundError(
            "\nUAV boundary not found:\n"
            f"{BOUNDARY_FILE}\n\n"
            "Copy your boundary.csv into:\n"
            "assets/aircraft/boundary.csv"
        )

    loader = BoundaryLoader(
        BOUNDARY_FILE
    )

    points = loader.load()

    print(
        f"Boundary points: "
        f"{len(points)}"
    )

    # ========================================================
    # ROTATE UAV
    # ========================================================

    print()
    print(
        f"[5] Rotating UAV "
        f"AoA={AOA_DEG:+.2f}°..."
    )

    points = rotate(
        points,
        angle_deg=AOA_DEG,
    )

    # ========================================================
    # SCALE / CENTER
    # ========================================================

    print()
    print(
        "[6] Scaling and centering UAV..."
    )

    points = normalize_boundary(

        points,

        domain_width=(
            domain.width
        ),

        domain_height=(
            domain.height
        ),

        body_width_fraction=0.35,

        body_height_fraction=0.35,

        center=True,
    )

    # ========================================================
    # CREATE BODY MASK
    # ========================================================

    print()
    print(
        "[7] Creating UAV solid mask..."
    )

    body = BodyMask(
        domain
    )

    solid_mask = (
        body.from_polygon(
            points
        )
    )

    body.summary()

    # ========================================================
    # CREATE LBM
    # ========================================================

    print()
    print(
        "[8] Creating D2Q9 LBM solver..."
    )

    lbm = D2Q9(

        nx=config.nx,

        ny=config.ny,

        u0=config.u0,

        viscosity=config.viscosity,
    )

    print(
        f"tau   = "
        f"{lbm.tau:.6f}"
    )

    print(
        f"omega = "
        f"{lbm.omega:.6f}"
    )

    print(
        f"LBM u0 = "
        f"{config.u0:.6f}"
    )

    print(
        f"Physical speed = "
        f"{SPEED_KMH:.1f} km/h"
    )

    # ========================================================
    # RUN CFD
    # ========================================================

    print()
    print(
        "[9] Running UAV CFD..."
    )

    for step in range(
        config.steps
    ):

        lbm.step(
            solid_mask=solid_mask
        )

        if (
            step % config.output_interval == 0
            or
            step == config.steps - 1
        ):

            speed = (
                lbm.speed(
                    solid_mask
                )
            )

            fluid_speed = (
                speed[
                    ~solid_mask
                ]
            )

            print(
                f"step={step:5d} "
                f"| "
                f"max|u|="
                f"{fluid_speed.max():.6f} "
                f"| "
                f"mean|u|="
                f"{fluid_speed.mean():.6f}"
            )

    # ========================================================
    # OUTPUT DIRECTORY
    # ========================================================

    print()
    print(
        "[10] Preparing output..."
    )

    output_dir = (
        PROJECT_ROOT
        / "output"
        / "cfd"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir
        / "uav_cfd_stage6f.png"
    )

    # ========================================================
    # RENDER
    # ========================================================

    print()
    print(
        "[11] Rendering CFD result..."
    )

    plot_cfd(

        domain=domain,

        lbm=lbm,

        solid_mask=solid_mask,

        body_points=points,

        aoa_deg=AOA_DEG,

        physical_speed_kmh=SPEED_KMH,

        show_vectors=True,

        show_airflow=True,

        show_vorticity=True,

        save_path=output_file,
    )

    # ========================================================
    # SHOW
    # ========================================================

    plt.show()

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 70)
    print("STAGE 6F COMPLETE")
    print("=" * 70)

    print()
    print(
        "Physical condition:"
    )

    print(
        f"  Speed : "
        f"{SPEED_KMH:.1f} km/h"
    )

    print(
        f"  Speed : "
        f"{physical.speed_ms:.2f} m/s"
    )

    print(
        f"  AoA   : "
        f"{AOA_DEG:+.1f}°"
    )

    print(
        f"  Re    : "
        f"{physical.reynolds:.3e}"
    )

    print()
    print(
        f"Output:\n"
        f"{output_file}"
    )


if __name__ == "__main__":

    main()