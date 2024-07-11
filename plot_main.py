import os
import re


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from matplotlib.patches import Wedge, Patch


from config import *
from utils import *


# 按照"Big_celltypes"选取"Sub_celltypes"
metadata_df = pd.read_csv("/work/wangjh/ruc_cell2location/LDX_all_meta.csv")

# 获取"Big_celltypes"
temp = metadata_df["Big_celltypes"].drop_duplicates().to_list()

filter_lst = [
    (
        i,
        metadata_df[
            metadata_df["Big_celltypes"].isin(
                [
                    i,
                ]
            )
        ]
        .drop_duplicates(subset=["Sub_celltypes"])["Sub_celltypes"]
        .to_list(),
    )
    for i in metadata_df["Big_celltypes"].drop_duplicates().to_list()
]


for i in filter_lst:
    print(i)
quit()


def plot(portion, position, des):
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

    plt.savefig(des, dpi=300)
    plt.close()


if __name__ == "__main__":
    for name, info in packages.items():
        path = {
            "dist": f"{name}/dist",
        }

        for _, value in path.items():
            os.makedirs(value, exist_ok=True)

        # each data
        for patient, stage in [(x, y) for x in patients for y in stages]:
            prefix = f"{patient}_{stage}"  # e.g. P1_pre
            print(f"> jiaheng: processing {prefix}")

            def get_position():
                df = pd.read_csv(
                    f"/work/wangjh/ruc_cell2location/all_count_data/{prefix}/spatial/tissue_positions_list.csv",
                    header=None,
                    names=[
                        "barcode",
                        "in_tissue",
                        "array_row",
                        "array_col",
                        "pxl_col_in_fullres",
                        "pxl_row_in_fullres",
                    ],
                )

                return df.set_index("barcode")

            def get_portion():
                df = pd.read_csv(
                    f"{info['path']}/{info['prefix']}{prefix}{info['surfix']}",
                    index_col=0,
                )

                # 去除公共部分
                common_substring = find_longest_common_substring(df.columns.tolist())
                df.columns = [re.sub(common_substring, "", col) for col in df.columns]

                # 只取上皮（成纤维）细胞
                df = df[filter]
                df = df.div(df.sum(axis=1), axis=0)
                return df

            plot(
                get_portion(),
                get_position(),
                f"{path['dist']}/{prefix}.png",
            )
