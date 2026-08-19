"""
UAV-Sim

Stage 1:
STEP → 3D visualization
"""

from pathlib import Path

from uavsim.cad.loader import (
    STEPModel,
)

from uavsim.cad.mesh import (
    CADMesher,
)

from uavsim.visualization.scene import (
    UAVScene,
)


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# ============================================================
# STEP FILE
# ============================================================

STEP_FILE = (
    PROJECT_ROOT
    / "assets"
    / "aircraft"
    / "model1.step"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 1 — 3D CAD VIEWER")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP
    # --------------------------------------------------------

    model = STEPModel(
        STEP_FILE
    )

    shape = model.load()

    # --------------------------------------------------------
    # MESH
    # --------------------------------------------------------

    mesher = CADMesher(
        shape,
        tolerance=0.1,
    )

    mesh = mesher.mesh()

    # --------------------------------------------------------
    # SCENE
    # --------------------------------------------------------

    scene = UAVScene()

    scene.add_aircraft(
        mesh
    )

    scene.add_axes()

    scene.add_ground(
        size=500
    )

    scene.fit_camera()

    # --------------------------------------------------------
    # SHOW
    # --------------------------------------------------------

    print()
    print(
        "Opening 3D viewer..."
    )

    scene.show()


if __name__ == "__main__":

    main()