"""
Plot UAV launch trajectory.
"""

import matplotlib.pyplot as plt
import numpy as np

from uavsim.simulation.scenario import (
    run_flight,
)


def main():

    # --------------------------------------------------------
    # Run simulation
    # --------------------------------------------------------

    history = run_flight(

        mass=1.5,

        launch_speed=20.0,

        launch_angle=70.0,

        wind_speed=5.0,

        reference_area=0.15,

        drag_coefficient=0.8,

        max_thrust=30.0,

        throttle=0.65,

        simulation_time=10.0,

        dt=0.01,
    )

    # --------------------------------------------------------
    # Extract position
    # --------------------------------------------------------

    positions = np.array(
        [
            item["position"]
            for item in history
        ]
    )

    # --------------------------------------------------------
    # X-Z trajectory
    # --------------------------------------------------------

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        positions[:, 0],
        positions[:, 2],
        linewidth=2,
    )

    plt.xlabel(
        "Distance X (m)"
    )

    plt.ylabel(
        "Altitude Z (m)"
    )

    plt.title(
        "UAV Launch Trajectory"
    )

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.axis(
        "equal"
    )

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    main()