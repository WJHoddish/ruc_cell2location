import os
import time

import pandas as pd
import anndata as ad

from anndata import AnnData


def print_time(start, msg):
    print(f"Running time ({msg}): {str(round((time.time() - start) / 60, 4))} min")
