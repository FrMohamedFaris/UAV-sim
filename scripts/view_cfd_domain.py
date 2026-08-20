"""
Visualize the Stage 6A CFD domain.
"""


import matplotlib.pyplot as plt

from uavsim.cfd.config import (
    CFDConfig,
)

from uavsim.cfd.domain import (
    CFDDomain,
)


def main():
    """
    Visualize the Stage 6A CFD domain.
    """

    import matplotlib.pyplot as plt

    from uavsim.cfd.config import CFDConfig
    from uavsim.cfd.domain import CFDDomain

    def main():
        # --------------------------------------------------------
        # CFD configuration
        # --------------------------------------------------------

        config = CFDConfig()

        config.validate()

        # --------------------------------------------------------
        # Create CFD domain
        # --------------------------------------------------------

        domain = CFDDomain(

            width=config.domain_width,

            height=config.domain_height,

            nx=config.nx,

            ny=config.ny,
        )

        # --------------------------------------------------------
        # Create figure
        # --------------------------------------------------------

        plt.figure(
            figsize=(14, 6)
        )

        plt.xlim(
            0,
            domain.width
        )

        plt.ylim(
            0,
            domain.height
        )

        plt.xlabel(
            "X — Flow direction"
        )

        plt.ylabel(
            "Y — Cross-flow direction"
        )

        plt.title(
            "UAV-Sim CFD Computational Domain"
        )

        # --------------------------------------------------------
        # Draw domain boundary
        # --------------------------------------------------------

        plt.plot(
            [
                0,
                domain.width,
                domain.width,
                0,
                0,
            ],
            [
                0,
                0,
                domain.height,
                domain.height,
                0,
            ],
            linewidth=2,
        )

        # --------------------------------------------------------
        # Mark inlet
        # --------------------------------------------------------

        plt.axvline(
            0,
            linewidth=3,
            label="Inlet",
        )

        # --------------------------------------------------------
        # Mark outlet
        # --------------------------------------------------------

        plt.axvline(
            domain.width,
            linewidth=3,
            label="Outlet",
        )

        # --------------------------------------------------------
        # Mark domain center
        # --------------------------------------------------------

        cx, cy = domain.center

        plt.scatter(
            [cx],
            [cy],
            s=80,
            label="Domain center",
        )

        # --------------------------------------------------------
        # Grid
        # --------------------------------------------------------

        plt.legend()

        plt.grid(
            True,
            alpha=0.25,
        )

        # --------------------------------------------------------
        # Equal aspect ratio
        # --------------------------------------------------------

        plt.gca().set_aspect(
            "equal"
        )

        plt.tight_layout()

        # --------------------------------------------------------
        # Display
        # --------------------------------------------------------

        plt.show()

    if __name__ == "__main__":
        main()

if __name__ == "__main__":

    main()