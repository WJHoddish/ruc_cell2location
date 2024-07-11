import itertools

import numpy as np

from cell2location.models import RegressionModel
from cell2location.models import Cell2location

from config import *
from parse_single_cell import *
from parse_spatial import *


adata_sc = parse_single_cell()
adata_sc.X = np.floor(np.abs(adata_sc.X)).astype(int)


def train_regression():
    args = get_args()

    # prepare anndata for the regression model
    RegressionModel.setup_anndata(adata=adata_sc, labels_key="CellType")

    # create and train the regression model
    mod = RegressionModel(adata_sc)
    mod.train(max_epochs=300, batch_size=2500, train_size=1, lr=0.002)

    # save module
    mod.save(args.regression_model, overwrite=True)


def train():
    pass


if __name__ == "__main__":
    args = get_args()

    if args.train_regression_model:
        train_regression()

    # read model
    mod = RegressionModel.load(args.regression_model, adata_sc)

    adata_sc = mod.export_posterior(
        adata_sc,
        sample_kwargs={
            "num_samples": 1000,
            "batch_size": 2500,
            # "use_gpu": False,
        },
    )

    # export estimated expression in each cluster
    if "means_per_cluster_mu_fg" in adata_sc.varm.keys():
        inf_aver = adata_sc.varm["means_per_cluster_mu_fg"][
            [
                f"means_per_cluster_mu_fg_{i}"
                for i in adata_sc.uns["mod"]["factor_names"]
            ]
        ].copy()
    else:
        inf_aver = adata_sc.var[
            [
                f"means_per_cluster_mu_fg_{i}"
                for i in adata_sc.uns["mod"]["factor_names"]
            ]
        ].copy()
    inf_aver.columns = adata_sc.uns["mod"]["factor_names"]

    assert not inf_aver.index.duplicated().any()

    # select spatial data
    for patient, stage in [
        list(itertools.product(patients, stages))[i] for i in args.ranks
    ]:
        prefix = f"{patient}_{stage}"
        path = f"{args.spatial}/{prefix}/filtered_feature_bc_matrix/"
        print(f"> jiaheng: processing {path}")

        # spatial data
        adata_st = parse_spatial(path)

        # NOTE: 检查并处理重复索引
        if adata_st.var_names.duplicated().any():
            adata_st = adata_st[:, ~adata_st.var_names.duplicated()].copy()

        # find shared genes and subset both anndata and reference signatures
        intersect = np.intersect1d(adata_st.var_names, inf_aver.index)

        assert np.array_equal(intersect, np.unique(intersect))

        adata_st = adata_st[:, intersect].copy()
        inf_aver = inf_aver.loc[intersect, :].copy()

        # prepare anndata for cell2location model
        Cell2location.setup_anndata(adata_st)

        # create and train the model
        mod = Cell2location(
            adata_st,
            cell_state_df=inf_aver,
            # the expected average cell abundance: tissue-dependent
            # hyper-prior which can be estimated from paired histology:
            N_cells_per_location=12,
            # hyperparameter controlling normalisation of
            # within-experiment variation in RNA detection (using default here):
            detection_alpha=200,
        )

        mod.train(
            max_epochs=30000,
            # train using full data (batch_size=None)
            batch_size=None,
            # use all data points in training because
            # we need to estimate cell abundance at all locations
            train_size=1,
        )

        # In this section, we export the estimated cell abundance (summary of the posterior distribution).
        adata_st = mod.export_posterior(
            adata_st,
            sample_kwargs={
                "num_samples": 1000,
                "batch_size": mod.adata.n_obs,
                # "use_gpu": False,
            },
        )

        # save data
        q05_cell_abundance = adata_st.obsm["q05_cell_abundance_w_sf"]
        q05_cell_abundance.to_csv(f"{args.result_dir}/{prefix}_q05_result.csv", sep=",")

        # means_cell_abundance = adata_st.obsm["means_cell_abundance_w_sf"]
        # means_cell_abundance.to_csv(
        #     f"{args.result_dir}/{prefix}_means_result.csv", sep=","
        # )
