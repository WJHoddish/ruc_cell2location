import os
import time


import pandas as pd


from anndata import AnnData
from config import *


def main():
    start = time.time()

    if args.count.endswith(".tsv"):
        df = pd.read_csv(args.count, sep="\t", index_col=0)

    else:
        assert args.count.endswith(".csv"), "File must be a .csv or .tsv"

        # FIXME: new data
        df = pd.read_csv(args.count, index_col=0).transpose()

    print(df)
    # AnnData(df).write(file_path)
    print(f"Running time: {str(round((time.time() - start) / 60, 4))} min")


if __name__ == "__main__":
    if os.path.exists(args.file_path):
        quit()

    main()
