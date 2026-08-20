"""
UAV-Sim
=======

Public command-line entry point.

Users do NOT need to know the internal CFD modules.

Run:

    python main.py

The program will:

    1. Ask for simulation parameters
    2. Load UAV boundary
    3. Transform geometry
    4. Create CFD body mask
    5. Run D2Q9 LBM
    6. Calculate physical reference values
    7. Render CFD result
    8. Save output
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

# ============================================================
# PROJECT PATH
# ============================================================

ROOT = Path(__file__).resolve().parent

SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# ============================================================
# UAV-Sim INTERNAL MODULES
# ============================================================

from uavsim.cfd.config import CFDConfig
from uavsim.cfd.domain import CFDDomain
from uavsim.cfd.lbm import D2Q9
from uavsim.cfd.body_mask import BodyMask
from uavsim.cfd.boundary_loader import BoundaryLoader
from uavsim.cfd.geometry_scale import normalize_boundary
from uavsim.cfd.geometry_transform import rotate
from uavsim.cfd.physical import PhysicalCondition
from uavsim.cfd.visualization import plot_cfd


# ============================================================
# PATHS
# ============================================================

DEFAULT_BOUNDARY = (
    ROOT
    / "assets"
    / "aircraft"
    / "boundary.csv"
)

OUTPUT_DIR = (
    ROOT
    / "output"
    / "results"
)


# ============================================================
# TERMINAL UI
# ============================================================

def header():

    print()

    print("=" * 70)
    print("UAV-SIM")
    print("STATIC UAV CFD")
    print("=" * 70)

    print()

    print(
        "CAD-derived UAV geometry → "
        "LBM CFD → velocity/vorticity visualization"
    )

    print()


def ask_string(
    label,
    default,
):

    value = input(
        f"{label} [{default}]: "
    ).strip()

    if not value:
        return str(default)

    return value


def ask_float(
    label,
    default,
):

    while True:

        value = input(
            f"{label} [{default}]: "
        ).strip()

        if not value:

            return float(default)

        try:

            return float(value)

        except ValueError:

            print(
                "Please enter a valid number."
            )


def ask_int(
    label,
    default,
):

    while True:

        value = input(
            f"{label} [{default}]: "
        ).strip()

        if not value:

            return int(default)

        try:

            return int(value)

        except ValueError:

            print(
                "Please enter a valid integer."
            )


# ============================================================
# USER INPUT
# ============================================================

def get_inputs():

    print("=" * 70)
    print("SIMULATION INPUT")
    print("=" * 70)

    boundary_file = Path(
        ask_string(
            "UAV boundary CSV",
            DEFAULT_BOUNDARY,
        )
    )

    speed_kmh = ask_float(
        "Airspeed (km/h)",
        180.0,
    )

    aoa_deg = ask_float(
        "Angle of attack (deg)",
        0.0,
    )

    nx = ask_int(
        "CFD width",
        400,
    )

    ny = ask_int(
        "CFD height",
        200,
    )

    steps = ask_int(
        "Simulation steps",
        3000,
    )

    characteristic_length = ask_float(
        "Characteristic length (m)",
        0.33,
    )

    lattice_velocity = ask_float(
        "LBM lattice velocity",
        0.03,
    )

    viscosity = ask_float(
        "LBM viscosity",
        0.03,
    )

    print()

    return {
        "boundary_file": boundary_file,
        "speed_kmh": speed_kmh,
        "aoa_deg": aoa_deg,
        "nx": nx,
        "ny": ny,
        "steps": steps,
        "characteristic_length": (
            characteristic_length
        ),
        "lattice_velocity": (
            lattice_velocity
        ),
        "viscosity": viscosity,
    }


# ============================================================
# SIMULATION
# ============================================================

def run_simulation(params):

    boundary_file = (
        params["boundary_file"]
    )

    speed_kmh = (
        params["speed_kmh"]
    )

    aoa_deg = (
        params["aoa_deg"]
    )

    nx = params["nx"]
    ny = params["ny"]

    steps = params["steps"]

    characteristic_length = (
        params["characteristic_length"]
    )

    u0 = (
        params["lattice_velocity"]
    )

    viscosity = (
        params["viscosity"]
    )

    # ========================================================
    # VALIDATE GEOMETRY
    # ========================================================

    if not boundary_file.exists():

        raise FileNotFoundError(
            "\nUAV boundary file not found:\n"
            f"{boundary_file}\n\n"
            "Put your boundary CSV in:\n"
            "assets/aircraft/boundary.csv"
        )

    # ========================================================
    # CONFIG
    # ========================================================

    config = CFDConfig(

        domain_width=20.0,

        domain_height=10.0,

        nx=nx,

        ny=ny,

        u0=u0,

        viscosity=viscosity,

        steps=steps,

        speed_kmh=speed_kmh,

        characteristic_length_m=(
            characteristic_length
        ),
    )

    config.validate()

    # ========================================================
    # PHYSICAL CONDITION
    # ========================================================

    print()
    print("=" * 70)
    print("[1/6] PHYSICAL FLIGHT CONDITION")
    print("=" * 70)

    physical = PhysicalCondition(

        speed_kmh=speed_kmh,

        characteristic_length_m=(
            characteristic_length
        ),

        air_density=(
            config.air_density
        ),

        dynamic_viscosity=(
            config.air_dynamic_viscosity
        ),

        lattice_velocity=u0,

        lattice_length=(
            nx * 0.35
        ),
    )

    physical.summary()

    # ========================================================
    # DOMAIN
    # ========================================================

    print()
    print("=" * 70)
    print("[2/6] CREATING CFD DOMAIN")
    print("=" * 70)

    domain = CFDDomain(

        width=config.domain_width,

        height=config.domain_height,

        nx=nx,

        ny=ny,
    )

    # ========================================================
    # LOAD BOUNDARY
    # ========================================================

    print()
    print("=" * 70)
    print("[3/6] LOADING UAV GEOMETRY")
    print("=" * 70)

    loader = BoundaryLoader(
        boundary_file
    )

    points = loader.load()

    print(
        f"Boundary points: "
        f"{len(points)}"
    )

    # ========================================================
    # ROTATE
    # ========================================================

    points = rotate(
        points,
        angle_deg=aoa_deg,
    )

    # ========================================================
    # SCALE
    # ========================================================

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
    # BODY MASK
    # ========================================================

    print()
    print("=" * 70)
    print("[4/6] CREATING UAV CFD BODY")
    print("=" * 70)

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
    # LBM
    # ========================================================

    print()
    print("=" * 70)
    print("[5/6] RUNNING LBM CFD")
    print("=" * 70)

    lbm = D2Q9(

        nx=nx,

        ny=ny,

        u0=u0,

        viscosity=viscosity,
    )

    print(
        f"tau   = {lbm.tau:.6f}"
    )

    print(
        f"omega = {lbm.omega:.6f}"
    )

    print()

    for step in range(
        steps
    ):

        lbm.step(
            solid_mask=solid_mask
        )

        if (
            step % max(
                1,
                steps // 10
            ) == 0
            or
            step == steps - 1
        ):

            speed = (
                lbm.speed(
                    solid_mask
                )
            )

            fluid = (
                speed[
                    ~solid_mask
                ]
            )

            print(
                f"[CFD] "
                f"{step + 1:5d}/{steps} "
                f"| max={fluid.max():.6f} "
                f"| mean={fluid.mean():.6f}"
            )

    # ========================================================
    # OUTPUT
    # ========================================================

    print()
    print("=" * 70)
    print("[6/6] RENDERING RESULT")
    print("=" * 70)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    image_file = (
        OUTPUT_DIR
        / "uav_cfd.png"
    )

    data_file = (
        OUTPUT_DIR
        / "simulation.json"
    )

    plot_cfd(

        domain=domain,

        lbm=lbm,

        solid_mask=solid_mask,

        body_points=points,

        aoa_deg=aoa_deg,

        physical_speed_kmh=speed_kmh,

        show_vectors=True,

        show_airflow=True,

        show_vorticity=True,

        save_path=image_file,
    )

    # ========================================================
    # SAVE METADATA
    # ========================================================

    result = {

        "simulation": {

            "speed_kmh": speed_kmh,

            "speed_ms": (
                physical.speed_ms
            ),

            "aoa_deg": aoa_deg,

            "characteristic_length_m": (
                characteristic_length
            ),

            "reynolds": (
                physical.reynolds
            ),

            "mach": (
                physical.mach
            ),
        },

        "lbm": {

            "nx": nx,

            "ny": ny,

            "steps": steps,

            "u0": u0,

            "viscosity": viscosity,

            "tau": lbm.tau,

            "omega": lbm.omega,
        },

        "geometry": {

            "boundary_points": (
                len(points)
            ),

            "solid_cells": (
                body.solid_cells
            ),

            "solid_fraction": (
                body.solid_fraction
            ),
        },

        "output": {

            "image": str(
                image_file
            ),

        },
    }

    with open(
        data_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            result,
            file,
            indent=2,
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)

    print()

    print(
        f"Speed       : "
        f"{speed_kmh:.1f} km/h"
    )

    print(
        f"Velocity    : "
        f"{physical.speed_ms:.2f} m/s"
    )

    print(
        f"AoA         : "
        f"{aoa_deg:+.1f}°"
    )

    print(
        f"Reynolds    : "
        f"{physical.reynolds:.3e}"
    )

    print(
        f"Mach        : "
        f"{physical.mach:.4f}"
    )

    print()

    print(
        "Output:"
    )

    print(
        f"  Image : {image_file}"
    )

    print(
        f"  Data  : {data_file}"
    )

    print()

    return {
        "image": image_file,
        "data": data_file,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    header()

    try:

        params = get_inputs()

        run_simulation(
            params
        )

        print()
        print(
            "✓ UAV-Sim finished successfully."
        )

    except KeyboardInterrupt:

        print()
        print(
            "Simulation cancelled."
        )

        sys.exit(1)

    except Exception as exc:

        print()
        print("=" * 70)
        print("SIMULATION FAILED")
        print("=" * 70)

        print()
        print(
            str(exc)
        )

        print()

        sys.exit(1)

    finally:

        plt.close("all")


if __name__ == "__main__":

    main()