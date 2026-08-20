"""
UAV-Sim Stage 6E

CFD visualization utilities.

Provides:
    - velocity magnitude
    - velocity vectors
    - vorticity
    - airflow direction
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt


def calculate_vorticity(
    ux,
    uy,
):
    """
    Calculate 2D z-vorticity:

        omega_z = dUy/dx - dUx/dy
    """

    duy_dy, duy_dx = np.gradient(
        uy
    )

    dux_dy, dux_dx = np.gradient(
        ux
    )

    return (
        duy_dx
        -
        dux_dy
    )


def plot_cfd(
    domain,
    lbm,
    solid_mask,
    body_points,
    aoa_deg=0.0,
    physical_speed_kmh=None,
    show_vectors=True,
    show_airflow=True,
    show_vorticity=True,
    save_path=None,
):
    """
    Create a complete CFD visualization.
    """

    ux = lbm.ux.copy()
    uy = lbm.uy.copy()

    # --------------------------------------------------------
    # Remove velocity inside UAV.
    # --------------------------------------------------------

    ux[solid_mask] = np.nan
    uy[solid_mask] = np.nan

    speed = np.sqrt(
        ux * ux
        +
        uy * uy
    )

    # --------------------------------------------------------
    # Vorticity
    # --------------------------------------------------------

    vorticity = calculate_vorticity(
        np.nan_to_num(ux),
        np.nan_to_num(uy),
    )

    vorticity[
        solid_mask
    ] = np.nan

    # --------------------------------------------------------
    # Coordinates
    # --------------------------------------------------------

    X = domain.X
    Y = domain.Y

    # ========================================================
    # FIGURE
    # ========================================================

    fig, ax = plt.subplots(
        figsize=(16, 8)
    )

    # ========================================================
    # VELOCITY FIELD
    # ========================================================

    image = ax.pcolormesh(
        X,
        Y,
        speed,
        shading="auto",
        cmap="turbo",
    )

    colorbar = fig.colorbar(
        image,
        ax=ax,
        pad=0.02,
    )

    if physical_speed_kmh is not None:

        colorbar.set_label(
            "Velocity / airflow"
        )

    else:

        colorbar.set_label(
            "Velocity — lattice units"
        )

    # ========================================================
    # UAV
    # ========================================================

    body_closed = np.vstack(
        [
            body_points,
            body_points[0],
        ]
    )

    ax.fill(
        body_closed[:, 0],
        body_closed[:, 1],
        color="white",
        zorder=10,
    )

    ax.plot(
        body_closed[:, 0],
        body_closed[:, 1],
        linewidth=2.5,
        zorder=11,
    )

    # ========================================================
    # VELOCITY VECTORS
    # ========================================================

    if show_vectors:

        # Don't draw every CFD cell.

        skip_x = max(
            1,
            domain.nx // 35,
        )

        skip_y = max(
            1,
            domain.ny // 18,
        )

        ax.quiver(
            X[
                ::skip_y,
                ::skip_x
            ],
            Y[
                ::skip_y,
                ::skip_x
            ],
            ux[
                ::skip_y,
                ::skip_x
            ],
            uy[
                ::skip_y,
                ::skip_x
            ],
            color="white",
            alpha=0.65,
            scale=None,
            zorder=5,
        )

    # ========================================================
    # AIRFLOW DIRECTION
    # ========================================================

    if show_airflow:

        # Large arrows along the inlet.

        arrow_y = np.linspace(
            domain.height * 0.15,
            domain.height * 0.85,
            6,
        )

        arrow_x_start = (
            domain.width * 0.025
        )

        arrow_length = (
            domain.width * 0.08
        )

        for y in arrow_y:

            ax.annotate(
                "",
                xy=(
                    arrow_x_start
                    +
                    arrow_length,
                    y,
                ),
                xytext=(
                    arrow_x_start,
                    y,
                ),
                arrowprops=dict(
                    arrowstyle="->",
                    linewidth=2.5,
                    color="white",
                ),
                zorder=20,
            )

        ax.text(
            domain.width * 0.025,
            domain.height * 0.93,
            "AIRFLOW →",
            fontsize=14,
            fontweight="bold",
            color="white",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="black",
                alpha=0.65,
            ),
            zorder=20,
        )

    # ========================================================
    # VORTICITY CONTOURS
    # ========================================================

    if show_vorticity:

        vmax = np.nanpercentile(
            np.abs(vorticity),
            98,
        )

        if vmax > 1e-12:

            levels = np.linspace(
                -vmax,
                vmax,
                13,
            )

            contours = ax.contour(
                X,
                Y,
                vorticity,
                levels=levels,
                cmap="coolwarm",
                linewidths=0.7,
                alpha=0.45,
            )

            ax.clabel(
                contours,
                inline=True,
                fontsize=7,
                fmt="%.2f",
            )

    # ========================================================
    # CENTER / BODY LABEL
    # ========================================================

    cx = np.mean(
        body_points[:, 0]
    )

    cy = np.mean(
        body_points[:, 1]
    )

    ax.text(
        cx,
        cy,
        "UAV",
        fontsize=12,
        fontweight="bold",
        color="black",
        ha="center",
        va="center",
        zorder=15,
    )

    # ========================================================
    # INFORMATION PANEL
    # ========================================================

    speed_text = ""

    if physical_speed_kmh is not None:

        speed_text = (
            f"\nSpeed: "
            f"{physical_speed_kmh:.1f} km/h"
        )

    info = (
        "UAV-Sim CFD"
        f"\nAoA: {aoa_deg:+.1f}°"
        f"{speed_text}"
        "\nFlow: →"
    )

    ax.text(
        0.985,
        0.025,
        info,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=11,
        color="white",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="black",
            alpha=0.70,
        ),
        zorder=30,
    )

    # ========================================================
    # AXES
    # ========================================================

    ax.set_xlim(
        0,
        domain.width,
    )

    ax.set_ylim(
        0,
        domain.height,
    )

    ax.set_aspect(
        "equal"
    )

    ax.set_xlabel(
        "X — Flow direction"
    )

    ax.set_ylabel(
        "Y — Cross-flow direction"
    )

    title = (
        "UAV-Sim — D2Q9 LBM CFD"
    )

    if physical_speed_kmh is not None:

        title += (
            f" | {physical_speed_kmh:.0f} km/h"
        )

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
    )

    ax.grid(
        True,
        alpha=0.15,
    )

    plt.tight_layout()

    # ========================================================
    # SAVE
    # ========================================================

    if save_path is not None:

        fig.savefig(
            save_path,
            dpi=200,
            bbox_inches="tight",
        )

        print(
            f"Saved:\n{save_path}"
        )

    return fig, ax