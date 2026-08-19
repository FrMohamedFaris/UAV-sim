import numpy as np

from uavsim.physics.state import UAVState
from uavsim.flight.launch import launch_velocity
from uavsim.physics.integrator import integrate_state


# ============================================================
# USER INPUT
# ============================================================

MASS = 1.5

LAUNCH_SPEED = 20.0

LAUNCH_ANGLE = 30.0

SIMULATION_TIME = 10.0

DT = 0.01


# ============================================================
# INITIAL STATE
# ============================================================

velocity = launch_velocity(
    LAUNCH_SPEED,
    LAUNCH_ANGLE,
)


state = UAVState.initial(
    mass=MASS,
    position=(
        0.0,
        0.0,
        0.0,
    ),
    velocity=velocity,
)


# ============================================================
# SIMULATION
# ============================================================

time = 0.0

while time <= SIMULATION_TIME:

    thrust = np.array(
        [
            0.0,
            0.0,
            0.0,
        ]
    )

    aerodynamic_force = np.array(
        [
            0.0,
            0.0,
            0.0,
        ]
    )

    integrate_state(
        state,
        thrust,
        aerodynamic_force,
        DT,
    )

    print(
        f"{time:6.2f}s | "
        f"x={state.position[0]:8.3f} | "
        f"z={state.position[2]:8.3f} | "
        f"V={np.linalg.norm(state.velocity):8.3f}"
    )

    time += DT