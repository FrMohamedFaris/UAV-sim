"""
Load a 2D UAV boundary CSV.

Expected format:

Point_ID,Y,Z

The loader converts this to:

X,Y

where:

X <- CSV Y
Y <- CSV Z
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

import csv


class BoundaryLoader:

    def __init__(
        self,
        filename,
    ):

        self.filename = Path(
            filename
        )

    def load(self):

        if not self.filename.exists():

            raise FileNotFoundError(
                f"\nBoundary CSV not found:\n"
                f"{self.filename}"
            )

        points = []

        with open(
            self.filename,
            "r",
            newline="",
        ) as file:

            reader = csv.DictReader(
                file
            )

            required = {
                "Y",
                "Z",
            }

            if not required.issubset(
                reader.fieldnames or []
            ):

                raise ValueError(
                    "CSV must contain "
                    "Y and Z columns."
                )

            for row in reader:

                try:

                    x = float(
                        row["Y"]
                    )

                    y = float(
                        row["Z"]
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    continue

                points.append(
                    [
                        x,
                        y,
                    ]
                )

        points = np.asarray(
            points,
            dtype=float,
        )

        if len(points) < 3:

            raise ValueError(
                "Boundary contains fewer "
                "than 3 valid points."
            )

        return points