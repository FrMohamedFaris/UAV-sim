"""
Convert CadQuery/OpenCascade geometry
into a PyVista mesh.
"""

import numpy as np

import pyvista as pv


class CADMesher:

    def __init__(
        self,
        shape,
        tolerance=0.1,
    ):

        self.shape = shape

        self.tolerance = tolerance

    def mesh(self):

        print()
        print(
            "[CAD] Creating visualization mesh..."
        )

        # CadQuery tessellation
        vertices, triangles = (
            self.shape.val()
            .tessellate(
                self.tolerance
            )
        )

        points = np.array(
            [
                (
                    vertex.x,
                    vertex.y,
                    vertex.z,
                )
                for vertex in vertices
            ],
            dtype=float,
        )

        faces = []

        for triangle in triangles:

            faces.extend(
                [
                    3,
                    triangle[0],
                    triangle[1],
                    triangle[2],
                ]
            )

        faces = np.asarray(
            faces,
            dtype=np.int64,
        )

        mesh = pv.PolyData(
            points,
            faces,
        )

        print(
            "✓ Mesh generated"
        )

        print(
            f"Vertices : "
            f"{len(points)}"
        )

        print(
            f"Triangles: "
            f"{len(triangles)}"
        )

        return mesh