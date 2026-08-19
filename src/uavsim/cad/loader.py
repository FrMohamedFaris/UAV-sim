"""
UAV-Sim
CAD STEP loader.

STEP
  ↓
CadQuery / OpenCascade
  ↓
CAD shape
"""


from pathlib import Path

import cadquery as cq


class STEPModel:

    def __init__(self, path):

        self.path = Path(path)

        self.shape = None

    def load(self):

        if not self.path.exists():

            raise FileNotFoundError(
                f"\nSTEP file not found:\n"
                f"{self.path}"
            )

        print()
        print("=" * 70)
        print("LOADING UAV CAD")
        print("=" * 70)

        print(
            f"STEP:\n{self.path}"
        )

        self.shape = cq.importers.importStep(
            str(self.path)
        )

        print(
            "✓ STEP loaded successfully"
        )

        return self.shape