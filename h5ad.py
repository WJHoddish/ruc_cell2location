from config import get_args
from utils import *


def main():
    args = get_args()

    if not os.path.exists(args.count_matrix_h5ad):
        # create an .h5ad version
        if args.count_matrix.endswith(".tsv"):
            df = pd.read_csv(args.count_matrix, sep="\t", index_col=0)
        else:
            assert args.count_matrix.endswith(".csv"), "File must be a .csv or .tsv"

            df = pd.read_csv(args.count_matrix, index_col=0).transpose()

        AnnData(df).write(args.count_matrix_h5ad)


if __name__ == "__main__":
    start = time.time()
    main()

    print_time(start, "transform to hdf5")
