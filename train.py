import numpy as np

from cell2location.models import RegressionModel
from cell2location.models import Cell2location

from config import get_args
from parse_single_cell import *


adata_sc = parse_single_cell()
adata_sc.X = np.floor(np.abs(adata_sc.X)).astype(int)


def train():
    args = get_args()

    # prepare anndata for the regression model
    RegressionModel.setup_anndata(adata=adata_sc, labels_key="CellType")

    # create and train the regression model
    mod = RegressionModel(adata_sc)
    mod.train(max_epochs=250, batch_size=2500, train_size=1, lr=0.002)  # use gpu

    # save module
    mod.save(args.regression_model, overwrite=True)


if __name__ == "__main__":
    train()

    args = get_args()
    mod = RegressionModel.load(args.regression_model, adata_sc)
