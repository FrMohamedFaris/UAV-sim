"""
Stage 6A test.

Creates a CFD computational domain
and verifies its dimensions.
"""


from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.domain import (
    CFDDomain,
)


def main():

    print()
    print("=" * 70)
    print("UAV-SIM")
    print("STAGE 6A — CFD DOMAIN TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    config = CFDConfig()

    config.validate()

    # --------------------------------------------------------
    # Domain
    # --------------------------------------------------------

    domain = CFDDomain(

        width=config.domain_width,

        height=config.domain_height,

        nx=config.nx,

        ny=config.ny,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    domain.summary()

    # --------------------------------------------------------
    # Coordinate checks
    # --------------------------------------------------------

    print()
    print("[CHECKS]")

    print(
        "X minimum:",
        domain.x.min(),
    )

    print(
        "X maximum:",
        domain.x.max(),
    )

    print(
        "Y minimum:",
        domain.y.min(),
    )

    print(
        "Y maximum:",
        domain.y.max(),
    )

    print(
        "X shape:",
        domain.X.shape,
    )

    print(
        "Y shape:",
        domain.Y.shape,
    )

    # --------------------------------------------------------
    # Assertions
    # --------------------------------------------------------

    assert domain.X.shape == (
        config.ny,
        config.nx,
    )

    assert domain.Y.shape == (
        config.ny,
        config.nx,
    )

    assert domain.cell_count == (
        config.nx
        * config.ny
    )

    assert domain.dx > 0

    assert domain.dy > 0

    print()
    print(
        "✓ ALL DOMAIN CHECKS PASSED"
    )

    print()
    print("=" * 70)
    print("STAGE 6A COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()