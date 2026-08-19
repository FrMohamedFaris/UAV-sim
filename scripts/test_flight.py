"""
Stage 2 flight physics test.
"""

import numpy as np

from uavsim.simulation.scenario import (
    run_flight,
)


def main():

    print()
    print("=" * 80)
    print("UAV-SIM — STAGE 2")
    print("=" * 80)

    # --------------------------------------------------------
    # Parameters
    # --------------------------------------------------------

    MASS = 1.5

    LAUNCH_SPEED = 20.0

    LAUNCH_ANGLE = 30.0

    WIND_SPEED = 5.0

    REFERENCE_AREA = 0.15

    DRAG_COEFFICIENT = 0.8

    MAX_THRUST = 30.0

    THROTTLE = 0.65

    SIMULATION_TIME = 10.0

    DT = 0.01

    # --------------------------------------------------------
    # Print configuration
    # --------------------------------------------------------

    print(
        f"\nMass          : "
        f"{MASS:.2f} kg"
    )

    print(
        f"Launch speed  : "
        f"{LAUNCH_SPEED:.2f} m/s"
    )

    print(
        f"Launch angle  : "
        f"{LAUNCH_ANGLE:.2f} deg"
    )

    print(
        f"Wind speed    : "
        f"{WIND_SPEED:.2f} m/s"
    )

    print(
        f"Max thrust    : "
        f"{MAX_THRUST:.2f} N"
    )

    print()

    # --------------------------------------------------------
    # Run simulation
    # --------------------------------------------------------

    history = run_flight(
        mass=MASS,
        launch_speed=LAUNCH_SPEED,
        launch_angle=LAUNCH_ANGLE,
        wind_speed=WIND_SPEED,
        reference_area=REFERENCE_AREA,
        drag_coefficient=DRAG_COEFFICIENT,
        max_thrust=MAX_THRUST,
        throttle=THROTTLE,
        simulation_time=SIMULATION_TIME,
        dt=DT,
    )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    for i, result in enumerate(history):

        if i % 100 != 0:
            continue

        position = result[
            "position"
        ]

        velocity = result[
            "velocity"
        ]

        speed = np.linalg.norm(
            velocity
        )

        print(
            f"t={result['time']:6.2f} s | "
            f"x={position[0]:8.2f} m | "
            f"y={position[1]:8.2f} m | "
            f"z={position[2]:8.2f} m | "
            f"speed={speed:7.2f} m/s"
        )

    print()
    print("=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)

    final = history[-1]

    print(
        "\nFinal position:",
        final["position"],
    )

    print(
        "Final velocity:",
        final["velocity"],
    )

    print(
        "Final speed:",
        np.linalg.norm(
            final["velocity"]
        ),
    )


if __name__ == "__main__":
    main()