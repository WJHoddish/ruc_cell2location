import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Wedge, Patch


def plot(position, portion, s):
    common_barcodes = position.index.intersection(portion.index)

    portion = portion.loc[common_barcodes]
    position = position.loc[common_barcodes]

    cell_types = portion.columns

    # plot
    fig, ax = plt.subplots(figsize=(10, 10))

    colors = plt.cm.tab20(np.linspace(0, 1, 8))

    # NOTE: 方案一
    radius = 175
    scale_factor = 1.5

    ax.set_xlim(
        position["pxl_col_in_fullres"].min() * scale_factor - 2000,
        position["pxl_col_in_fullres"].max() * scale_factor + 2000,
    )
    ax.set_ylim(
        position["pxl_row_in_fullres"].min() * scale_factor - 2000,
        position["pxl_row_in_fullres"].max() * scale_factor + 2000,
    )

    for barcode, row in position.iterrows():
        x = row["pxl_col_in_fullres"] * scale_factor
        y = row["pxl_row_in_fullres"] * scale_factor

        proportions = portion.loc[barcode]
        pie_sizes = proportions.values
        start_angle = 90

        # NOTE:
        if any(np.isnan(pie_sizes)):
            print("Warning: pie_sizes contains NaN values. Replacing NaNs with 0.")
            pie_sizes = np.nan_to_num(pie_sizes, nan=0.0)

        for i, size in enumerate(pie_sizes):
            angle = size * 360
            wedge = Wedge(
                center=(x, y),
                r=radius,
                theta1=start_angle,
                theta2=start_angle + angle,
                color=colors[i],
                alpha=0.8,
            )
            ax.add_patch(wedge)
            start_angle += angle

    ax.set_title("Spatial Distribution of Cell Types", fontsize=14)
    ax.set_xlabel("X Coordinate", fontsize=14)
    ax.set_ylabel("Y Coordinate", fontsize=14)

    plt.gca().invert_yaxis()
    plt.axis("equal")

    legend_patches = [
        Patch(color=colors[i], label=cell_types[i]) for i in range(len(cell_types))
    ]

    plt.legend(
        handles=legend_patches,
        title="Cell Type",
        bbox_to_anchor=(1, 1),
        loc="upper left",
        frameon=False,
        handletextpad=0.1,
        handlelength=0.6,
        handleheight=0.6,
        markerscale=0.75,
    )

    plt.savefig(s, dpi=300)
    plt.close()
