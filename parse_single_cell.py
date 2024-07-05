from config import get_args
from utils import *


def parse_single_cell():
    args = get_args()

    start = time.time()

    # create AnnData
    adata_sc = ad.read_h5ad(args.count_matrix_h5ad)
    adata_sc.obs["sample"] = adata_sc.obs_names
    adata_sc.var["SYMBOL"] = adata_sc.var_names

    # read metadata
    metadata_df = pd.read_csv(
        args.metadata,
        header=None,
        skiprows=1,  #
    )

    metadata_df.set_index(metadata_df.columns[0], inplace=True)
    metadata_df.columns = ["sample", "cell_type", "sub_type"]

    # filter
    metadata_df = metadata_df.loc[adata_sc.obs_names]

    # NOTE (2024.07.05): focus on 29 sub-types
    adata_sc.obs["CellType"] = metadata_df["sub_type"].astype("category")

    print_time(start, "parse single-cell reference")
    return adata_sc


if __name__ == "__main__":
    adata_sc = parse_single_cell()

    print(adata_sc.obs)
    print(adata_sc.var)
