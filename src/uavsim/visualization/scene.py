"""
UAV-Sim 3D visualization.
"""

import numpy as np
import pyvista as pv

from uavsim.visualization.airflow import (
    AirflowVisualizer,
)

from uavsim.visualization.hud import (
    SimulationHUD,
)


class UAVScene:

    def __init__(
        self,
        window_size=(1400, 900),
    ):

        self.plotter = pv.Plotter(
            window_size=window_size
        )

        self.plotter.set_background(
            "white"
        )

        self.aircraft_actor = None

        self.base_mesh = None

        # ----------------------------------------------------
        # Airflow
        # ----------------------------------------------------

        self.airflow = (
            AirflowVisualizer(
                self.plotter
            )
        )

        # ----------------------------------------------------
        # HUD
        # ----------------------------------------------------

        self.hud = (
            SimulationHUD(
                self.plotter
            )
        )

    # ========================================================
    # AIRCRAFT
    # ========================================================

    def add_aircraft(
        self,
        mesh,
    ):

        self.base_mesh = mesh.copy()

        center = np.array(
            self.base_mesh.center,
            dtype=float,
        )

        self.base_mesh.translate(
            -center,
            inplace=True,
        )

        self.aircraft_actor = (
            self.plotter.add_mesh(
                self.base_mesh,
                name="uav",
                smooth_shading=True,
                show_edges=False,
                reset_camera=False,
            )
        )

    # ========================================================
    # UPDATE AIRCRAFT
    # ========================================================

    def update_aircraft(
        self,
        position,
        attitude,
    ):

        if self.aircraft_actor is None:
            return

        position = np.asarray(
            position,
            dtype=float,
        )

        roll, pitch, yaw = attitude

        Rx = np.array([
            [1, 0, 0],
            [
                0,
                np.cos(roll),
                -np.sin(roll),
            ],
            [
                0,
                np.sin(roll),
                np.cos(roll),
            ],
        ])

        Ry = np.array([
            [
                np.cos(pitch),
                0,
                np.sin(pitch),
            ],
            [
                0,
                1,
                0,
            ],
            [
                -np.sin(pitch),
                0,
                np.cos(pitch),
            ],
        ])

        Rz = np.array([
            [
                np.cos(yaw),
                -np.sin(yaw),
                0,
            ],
            [
                np.sin(yaw),
                np.cos(yaw),
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ])

        rotation = (
            Rz
            @ Ry
            @ Rx
        )

        transform = np.eye(
            4,
            dtype=float,
        )

        transform[:3, :3] = rotation

        transform[:3, 3] = position

        self.aircraft_actor.user_matrix = (
            transform
        )

    # ========================================================
    # AXES
    # ========================================================

    def add_axes(self):

        self.plotter.add_axes(
            line_width=2,
            labels_off=False,
        )

    # ========================================================
    # GROUND
    # ========================================================

    def add_ground(
        self,
        size=500,
    ):

        ground = pv.Plane(
            center=(
                0.0,
                0.0,
                0.0,
            ),
            direction=(
                0.0,
                0.0,
                1.0,
            ),
            i_size=size,
            j_size=size,
            i_resolution=1,
            j_resolution=1,
        )

        self.plotter.add_mesh(
            ground,
            opacity=0.15,
            show_edges=False,
            name="ground",
        )

    # ========================================================
    # WIND
    # ========================================================

    def add_wind(
        self,
        bounds,
        wind_velocity,
        spacing=8.0,
    ):

        return self.airflow.create_wind_field(
            bounds=bounds,
            wind_velocity=wind_velocity,
            spacing=spacing,
        )

    # ========================================================
    # HUD
    # ========================================================

    def update_hud(
        self,
        frame,
    ):

        self.hud.update(
            frame
        )

    # ========================================================
    # CAMERA
    # ========================================================

    def fit_camera(self):

        self.plotter.reset_camera()

    # ========================================================
    # SHOW
    # ========================================================

    def show(
        self,
        **kwargs,
    ):

        self.plotter.show(
            **kwargs
        )