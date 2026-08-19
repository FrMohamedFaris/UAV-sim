"""
Simulation HUD.
"""



import numpy as np


class SimulationHUD:

    def __init__(
        self,
        plotter,
    ):

        self.plotter = plotter

        self.text_actor = None

    def update(
        self,
        frame,
    ):

        position = frame[
            "position"
        ]

        velocity = frame[
            "velocity"
        ]

        wind = frame[
            "wind"
        ]

        attitude = frame[
            "attitude"
        ]

        speed = (
            np.linalg.norm(
                velocity
            )
            * 3.6
        )

        wind_speed = (
            np.linalg.norm(
                wind
            )
            * 3.6
        )

        pitch = (
            np.degrees(
                attitude[1]
            )
        )

        text = (
            f"UAV SIMULATION\n"
            f"\n"
            f"TIME     : "
            f"{frame['time']:6.2f} s\n"
            f"SPEED    : "
            f"{speed:6.1f} km/h\n"
            f"WIND     : "
            f"{wind_speed:6.1f} km/h\n"
            f"ALTITUDE : "
            f"{position[2]:6.1f} m\n"
            f"X        : "
            f"{position[0]:6.1f} m\n"
            f"Y        : "
            f"{position[1]:6.1f} m\n"
            f"PITCH    : "
            f"{pitch:6.1f} deg\n"
            f"LIFT     : "
            f"{frame['lift']:6.1f} N\n"
            f"DRAG     : "
            f"{frame['drag']:6.1f} N"
        )

        self.plotter.add_text(
            text,
            position="upper_left",
            name="hud",
            font_size=12,
        )