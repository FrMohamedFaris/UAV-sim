"""
3D airflow visualization.

This is a visualization layer.

It does NOT replace the CFD solver.

It shows the wind vector and will
later be replaced/augmented by the
LBM velocity field.
"""

import numpy as np

import pyvista as pv


class AirflowVisualizer:

    def __init__(
        self,
        plotter,
    ):

        self.plotter = plotter

        self.actor = None

    def create_wind_field(
        self,
        bounds,
        wind_velocity,
        spacing=8.0,
    ):

        xmin, xmax, ymin, ymax, zmin, zmax = (
            bounds
        )

        x = np.arange(
            xmin,
            xmax + spacing,
            spacing,
        )

        y = np.arange(
            ymin,
            ymax + spacing,
            spacing,
        )

        z = np.arange(
            zmin,
            zmax + spacing,
            spacing,
        )

        grid = pv.StructuredGrid()

        X, Y, Z = np.meshgrid(
            x,
            y,
            z,
            indexing="ij",
        )

        grid.points = np.column_stack(
            [
                X.ravel(),
                Y.ravel(),
                Z.ravel(),
            ]
        )

        grid.dimensions = (
            len(x),
            len(y),
            len(z),
        )

        velocity = np.tile(
            np.asarray(
                wind_velocity,
                dtype=float,
            ),
            (
                len(grid.points),
                1,
            ),
        )

        grid["velocity"] = velocity

        arrows = grid.glyph(
            orient="velocity",
            scale=False,
            factor=1.5,
        )

        self.actor = (
            self.plotter.add_mesh(
                arrows,
                name="wind",
                opacity=0.35,
            )
        )

        return grid