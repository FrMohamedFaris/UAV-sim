"""
UAV flight simulation scenario.

Stage 5:

UAV
 ↓
Wind profile
 ↓
Relative airflow
 ↓
Aerodynamic forces
 ↓
Flight dynamics
"""

from uavsim.physics.state import (
    UAVState,
)

from uavsim.flight.launch import (
    launch_velocity,
    launch_attitude,
)

from uavsim.flight.profile import (
    FlightProfile,
)

from uavsim.physics.propulsion import (
    Propulsion,
)

from uavsim.aero.aerodynamic_model import (
    AerodynamicModel,
)

from uavsim.aero.atmosphere import (
    WindField,
)

from uavsim.aero.wind_profile import (
    WindProfile,
)

from uavsim.simulation.engine import (
    SimulationEngine,
)


def run_flight(

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

    dt=0.02,
):

    # ========================================================
    # INITIAL VELOCITY
    # ========================================================

    velocity = launch_velocity(
        launch_speed,
        launch_angle,
    )

    # ========================================================
    # INITIAL ATTITUDE
    # ========================================================

    attitude = launch_attitude(
        launch_angle
    )

    # ========================================================
    # STATE
    # ========================================================

    state = UAVState.initial(

        mass=mass,

        position=(
            0.0,
            0.0,
            0.0,
        ),

        velocity=velocity,

        attitude=attitude,
    )

    # ========================================================
    # PROPULSION
    # ========================================================

    propulsion = Propulsion(
        max_thrust=max_thrust
    )

    # ========================================================
    # AERODYNAMICS
    # ========================================================

    aerodynamics = AerodynamicModel(

        reference_area=(
            reference_area
        ),

        drag_coefficient=(
            drag_coefficient
        ),

        lift_coefficient=(
            lift_coefficient
        ),

        air_density=1.225,
    )

    # ========================================================
    # WIND PROFILE
    # ========================================================

    profile = WindProfile(

        base_speed=wind_speed,

        direction_deg=(
            wind_direction_deg
        ),

        gust_amplitude=wind_gust,

        gust_frequency=0.2,
    )

    wind = WindField(
        profile=profile
    )

    # ========================================================
    # FLIGHT PROFILE
    # ========================================================

    flight_profile = (
        FlightProfile(

            launch_pitch_deg=(
                launch_angle
            ),

            cruise_pitch_deg=5.0,

            descent_pitch_deg=-8.0,
        )
    )

    # ========================================================
    # ENGINE
    # ========================================================

    engine = SimulationEngine(

        state=state,

        propulsion=propulsion,

        aerodynamic_model=(
            aerodynamics
        ),

        wind_field=wind,

        dt=dt,
    )

    # ========================================================
    # SIMULATION
    # ========================================================

    steps = int(
        simulation_time / dt
    )

    history = []

    for _ in range(steps):

        # ----------------------------------------------------
        # Flight attitude
        # ----------------------------------------------------

        engine.state.attitude = (
            flight_profile.attitude(
                engine.time
            )
        )

        # ----------------------------------------------------
        # Physics
        # ----------------------------------------------------

        result = engine.step(
            throttle
        )

        history.append(
            result
        )

    return history