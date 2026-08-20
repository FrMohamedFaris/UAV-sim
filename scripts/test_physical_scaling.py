from uavsim.cfd.physical import (
    PhysicalCondition,
)


def main():

    condition = PhysicalCondition(
        speed_kmh=180.0,

        characteristic_length_m=0.33,

        lattice_velocity=0.03,

        lattice_length=140.0,
    )

    condition.summary()


if __name__ == "__main__":
    main()