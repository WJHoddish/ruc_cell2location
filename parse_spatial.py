from config import get_args
from utils import *

from scipy.io import mmread


def parse_spatial(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """

    barcodes_path = file_path + "barcodes.tsv.gz"
    features_path = file_path + "features.tsv.gz"
    matrix_path = file_path + "matrix.mtx.gz"

    matrix = mmread(matrix_path).tocsc().T
    barcodes = pd.read_csv(barcodes_path, header=None, names=["barcodes"])
    features = pd.read_csv(
        features_path,
        header=None,
        sep="\t",
        names=["gene_ids", "gene_names", "feature_types"],
    )

    # create AnnData
    adata_st = AnnData(X=matrix, obs=barcodes, var=features)

    # fix AnnData
    adata_st.obs_names = adata_st.obs["barcodes"]
    adata_st.var_names = adata_st.var["gene_names"]

    # TODO: normalization (for that matrix)

    return adata_st


if __name__ == "__main__":
    adata_st = parse_spatial("/home/wangjh/Data/P1_pre/filtered_feature_bc_matrix/")
    print(adata_st)
    print(adata_st.obs)
    print(adata_st.var)
