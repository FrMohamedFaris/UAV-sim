"""
UAV-Sim Stage 5
3D UAV + Wind + HUD + MP4 recording
"""

from pathlib import Path

import numpy as np

from uavsim.cad.loader import STEPModel
from uavsim.cad.mesh import CADMesher

from uavsim.simulation.scenario import run_flight

from uavsim.visualization.scene import UAVScene


# ============================================================
# PROJECT
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


STEP_FILE = (
    PROJECT_ROOT
    / "assets"
    / "aircraft"
    / "model1.step"
)


VIDEO_DIR = (
    PROJECT_ROOT
    / "output"
    / "videos"
)


VIDEO_FILE = (
    VIDEO_DIR
    / "uav_stage5.mp4"
)


# ============================================================
# VIDEO SETTINGS
# ============================================================

FPS = 30

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720


# ============================================================
# SIMULATION
# ============================================================

def create_simulation():

    return run_flight(

        mass=1.5,

        launch_speed=20.0,

        launch_angle=30.0,

        wind_speed=5.0,

        wind_direction_deg=0.0,

        wind_gust=2.0,

        reference_area=0.15,

        drag_coefficient=0.8,

        lift_coefficient=0.4,

        max_thrust=30.0,

        throttle=0.65,

        simulation_time=10.0,

        dt=1.0 / FPS,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 5 — UAV + WIND + MP4")
    print("=" * 70)

    VIDEO_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # LOAD CAD
    # ========================================================

    print()
    print("[1] Loading CAD...")

    model = STEPModel(
        STEP_FILE
    )

    shape = model.load()

    # ========================================================
    # CREATE MESH
    # ========================================================

    print()
    print("[2] Creating CAD mesh...")

    mesher = CADMesher(
        shape,
        tolerance=0.1,
    )

    mesh = mesher.mesh()

    # ========================================================
    # SIMULATION
    # ========================================================

    print()
    print("[3] Running flight simulation...")

    history = create_simulation()

    print(
        f"✓ Simulation frames: "
        f"{len(history)}"
    )

    # ========================================================
    # CREATE SCENE
    # ========================================================

    print()
    print("[4] Creating 3D scene...")

    scene = UAVScene(
        window_size=(
            VIDEO_WIDTH,
            VIDEO_HEIGHT,
        )
    )

    scene.add_aircraft(
        mesh
    )

    scene.add_axes()

    scene.add_ground(
        size=500
    )

    # ========================================================
    # WIND
    # ========================================================

    scene.add_wind(

        bounds=(
            -100,
            300,
            -100,
            100,
            -20,
            100,
        ),

        wind_velocity=(
            5.0,
            0.0,
            0.0,
        ),

        spacing=15.0,
    )

    # ========================================================
    # CAMERA
    # ========================================================

    scene.fit_camera()

    # ========================================================
    # OPEN WINDOW
    # ========================================================

    print()
    print("[5] Opening renderer...")

    scene.plotter.show(
        auto_close=False,
        interactive_update=True,
    )

    # ========================================================
    # START MP4
    # ========================================================

    print()
    print("[6] Opening MP4 writer...")

    scene.plotter.open_movie(
        str(VIDEO_FILE),
        framerate=FPS,
    )

    print()
    print(
        f"Video:"
        f"\n{VIDEO_FILE}"
    )

    # ========================================================
    # RENDER FRAMES
    # ========================================================

    print()
    print("[7] Rendering video...")
    print()

    total_frames = len(
        history
    )

    for frame_number, frame in enumerate(
        history
    ):

        # ----------------------------------------------------
        # UAV state
        # ----------------------------------------------------

        position = frame[
            "position"
        ]

        attitude = frame[
            "attitude"
        ]

        # ----------------------------------------------------
        # Update UAV
        # ----------------------------------------------------

        scene.update_aircraft(

            position=position,

            attitude=attitude,
        )

        # ----------------------------------------------------
        # Update HUD
        # ----------------------------------------------------

        scene.update_hud(
            frame
        )

        # ----------------------------------------------------
        # Render
        # ----------------------------------------------------

        scene.plotter.render()

        # ----------------------------------------------------
        # Write frame
        # ----------------------------------------------------

        scene.plotter.write_frame()

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        if (
            frame_number % FPS == 0
            or
            frame_number == total_frames - 1
        ):

            percent = (
                (
                    frame_number + 1
                )
                /
                total_frames
                * 100.0
            )

            print(
                f"\r"
                f"Frame "
                f"{frame_number + 1:04d}"
                f"/"
                f"{total_frames:04d}"
                f"  "
                f"{percent:6.1f}%",
                end="",
                flush=True,
            )

    print()

    # ========================================================
    # CLOSE VIDEO
    # ========================================================

    scene.plotter.close()

    print()
    print("=" * 70)
    print("VIDEO COMPLETE")
    print("=" * 70)

    print()
    print(
        f"Saved to:"
        f"\n{VIDEO_FILE}"
    )

    print()
    print(
        "FPS       :",
        FPS,
    )

    print(
        "Resolution:",
        f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
    )

    print(
        "Duration  :",
        f"{len(history) / FPS:.2f} seconds",
    )


if __name__ == "__main__":

    main()